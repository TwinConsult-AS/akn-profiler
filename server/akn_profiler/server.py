"""
AKN Profiler — Language Server Entry Point

This module initialises a pygls LanguageServer and registers LSP feature
handlers (completion, diagnostics, hover, etc.).  It is intended to be
launched as:

    python -m akn_profiler.server

Communication with the VS Code language client happens over stdio using
the Language Server Protocol (JSON-RPC).

Implementation roadmap:
  1. ✓ Initialise the LanguageServer instance
  2. ✓ Register basic lifecycle handlers (initialize, shutdown)
  3. ✓ Register document sync handlers (didOpen, didChange, didClose)
  4. ✓ Load and parse the AKN 3.0 XSD schema (via xsd/ subpackage)
  5. ✓ Build the Pydantic model registry (via models/ subpackage)
  6. ✓ Register @server.feature handlers:
       - textDocument/diagnostic  — validate profile against schema
  7. ✓ Register @server.feature handlers:
       - textDocument/completion  — profile key/value suggestions
       - textDocument/hover       — show AKN element documentation
       - textDocument/codeAction  — quick-fix for invalid restrictions
  8. ✓ Implement auto-generation of minimum viable profile skeleton
"""

from __future__ import annotations

import difflib
import functools
import logging
import re as _re
from collections.abc import Callable
from typing import Any, TypeVar

import yaml
from lsprotocol.types import (
    TEXT_DOCUMENT_CODE_ACTION,
    TEXT_DOCUMENT_CODE_LENS,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_CLOSE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    CodeAction,
    CodeActionKind,
    CodeActionParams,
    CodeLens,
    CodeLensParams,
    Command,
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionOptions,
    CompletionParams,
    Diagnostic,
    DiagnosticSeverity,
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    Hover,
    HoverParams,
    InitializeParams,
    InsertTextFormat,
    MarkupContent,
    MarkupKind,
    Position,
    PublishDiagnosticsParams,
    Range,
    SemanticTokenModifiers,
    SemanticTokens,
    SemanticTokensLegend,
    SemanticTokensParams,
    SemanticTokenTypes,
    TextEdit,
    WorkspaceEdit,
)
from pygls.lsp.server import LanguageServer

from akn_profiler.models.cascade import _ProfileDumper, collapse_element, expand_element
from akn_profiler.models.snippet_generator import generate_snippet, get_document_types
from akn_profiler.validation.engine import validate_profile
from akn_profiler.validation.errors import Severity, ValidationError
from akn_profiler.validation.yaml_context import Scope, resolve_context
from akn_profiler.xsd.schema_loader import AknSchema

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("akn_profiler")

# Create the language server instance
server = LanguageServer("akn-profiler", "v0.1.2")


# Module-level schema instance — populated during initialize
akn_schema: AknSchema | None = None

# Type variable for decorator
_T = TypeVar("_T")


def _safe_handler(fallback: _T) -> Callable:
    """Decorator that wraps an LSP feature handler in try/except.

    On unhandled exception the traceback is logged and *fallback* is returned
    so that a single malformed document cannot break the entire feature.
    """

    def decorator(fn: Callable[..., _T]) -> Callable[..., _T]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> _T:
            try:
                return fn(*args, **kwargs)
            except Exception:
                logger.exception("%s handler failed", fn.__name__)
                return fallback

        return wrapper

    return decorator


@server.feature("initialize")
def initialize(params: InitializeParams) -> None:
    """Handle the initialize request from the client."""
    global akn_schema
    logger.info("AKN Profiler language server initializing...")
    logger.info(f"Client: {params.client_info}")
    logger.info(f"Root URI: {params.root_uri}")

    # Read schema version from client initialization options (reserved for future use)
    schema_version = "3.0"
    if params.initialization_options and isinstance(params.initialization_options, dict):
        schema_version = params.initialization_options.get("schemaVersion", "3.0")
    logger.info(f"Schema version: {schema_version}")

    # Phase 1: Load the AKN XSD schema (currently only 3.0 is supported)
    akn_schema = AknSchema.load()
    logger.info(
        "AKN schema loaded: %d elements, %d enums",
        len(akn_schema.element_names()),
        len(akn_schema.all_enums()),
    )
    logger.info("✅ AKN Profiler server initialized")


@server.feature("shutdown")
def shutdown() -> None:
    """Handle the shutdown request from the client."""
    logger.info("AKN Profiler language server shutting down...")


@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(params: DidOpenTextDocumentParams) -> None:
    """Handle document open events — validate and publish diagnostics."""
    doc = params.text_document
    _validate_and_publish(doc.uri, doc.text)


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: DidChangeTextDocumentParams) -> None:
    """Handle document change events — re-validate."""
    doc = params.text_document
    # Get the latest full text from the server's workspace
    text_doc = server.workspace.get_text_document(doc.uri)
    _validate_and_publish(doc.uri, text_doc.source)


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(params: DidCloseTextDocumentParams) -> None:
    """Handle document close events — clear diagnostics."""
    doc = params.text_document
    server.text_document_publish_diagnostics(PublishDiagnosticsParams(uri=doc.uri, diagnostics=[]))


# ------------------------------------------------------------------
# Validation → LSP diagnostics bridge
# ------------------------------------------------------------------

_SEVERITY_MAP = {
    Severity.ERROR: DiagnosticSeverity.Error,
    Severity.WARNING: DiagnosticSeverity.Warning,
    Severity.INFO: DiagnosticSeverity.Information,
}


def _validate_and_publish(uri: str, source: str) -> None:
    """Run the validation engine and publish LSP diagnostics."""
    if akn_schema is None:
        logger.warning("Schema not loaded yet — skipping validation")
        return

    errors = validate_profile(source, akn_schema)
    diagnostics = [_error_to_diagnostic(e) for e in errors]

    server.text_document_publish_diagnostics(
        PublishDiagnosticsParams(uri=uri, diagnostics=diagnostics)
    )


def _error_to_diagnostic(error: ValidationError) -> Diagnostic:
    """Convert an internal ``ValidationError`` to an LSP ``Diagnostic``."""
    line = (error.line or 1) - 1  # LSP lines are 0-based
    col = error.column or 0
    return Diagnostic(
        range=Range(
            start=Position(line=line, character=col),
            end=Position(line=line, character=col + 1000),
        ),
        message=error.message,
        severity=_SEVERITY_MAP.get(error.severity, DiagnosticSeverity.Error),
        source="akn-profiler",
        code=error.rule_id,
    )


def start_server() -> None:
    """Start the language server over stdio."""
    logger.info("Starting AKN Profiler language server on stdio...")
    server.start_io()


# ==================================================================
# textDocument/completion
# ==================================================================

_PROFILE_KEYS = ["name", "version", "description", "documentTypes", "elements"]
_ELEMENT_BODY_KEYS = ["profileNote", "attributes", "children", "structure"]
_ATTRIBUTE_BODY_KEYS = ["required", "values"]


@server.feature(
    TEXT_DOCUMENT_COMPLETION,
    CompletionOptions(trigger_characters=[":", "-", " ", "\n"]),
)
@_safe_handler(CompletionList(is_incomplete=False, items=[]))
def completion(params: CompletionParams) -> CompletionList:
    """Provide contextual completions for AKN profile YAML files."""
    if akn_schema is None:
        return CompletionList(is_incomplete=False, items=[])

    doc = server.workspace.get_text_document(params.text_document.uri)
    ctx = resolve_context(doc.source, params.position.line, params.position.character)
    items: list[CompletionItem] = []

    existing = set(ctx.existing_keys)
    # Cross-block exclusion: prevent adding the same element in both
    # children: and choice:, or duplicate attributes.
    excluded = existing | set(ctx.cross_block_keys)

    if ctx.scope == Scope.EMPTY:
        items.append(_key_completion("profile", "Top-level profile key", "profile:\n  "))

    elif ctx.scope == Scope.ROOT:
        if "profile" not in existing:
            items.append(_key_completion("profile", "Top-level profile key", "profile:\n  "))

    elif ctx.scope == Scope.PROFILE:
        for key in _PROFILE_KEYS:
            if key in existing:
                continue
            if key == "documentTypes":
                items.append(
                    _key_completion(key, "Valid AKN document types", f"{key}:\n    - $1\n")
                )
            elif key == "elements":
                items.append(
                    _key_completion(
                        key,
                        "Element restrictions",
                        f"{key}:\n    $1:\n",
                    )
                )
            else:
                items.append(_key_completion(key, f"Profile {key}", f'{key}: "$1"\n'))

    elif ctx.scope == Scope.DOCUMENT_TYPES:
        for dt in akn_schema.get_children("akomaNtoso"):
            if dt in existing:
                continue
            info = akn_schema.get_element_info(dt)
            doc_str = info.doc[:120] if info and info.doc else f"AKN document type: {dt}"
            items.append(
                CompletionItem(
                    label=dt,
                    kind=CompletionItemKind.EnumMember,
                    detail="document type",
                    documentation=MarkupContent(kind=MarkupKind.Markdown, value=doc_str),
                    insert_text=f"- {dt}",
                    insert_text_format=InsertTextFormat.PlainText,
                    sort_text=f"0{dt}",
                )
            )

    elif ctx.scope == Scope.ELEMENTS:
        for name in akn_schema.element_names():
            if name in existing:
                continue
            info = akn_schema.get_element_info(name)
            doc_str = _element_doc(name) if info else ""
            snippet = f"{name}:\n"
            items.append(
                CompletionItem(
                    label=name,
                    kind=CompletionItemKind.Class,
                    detail="AKN element",
                    documentation=MarkupContent(kind=MarkupKind.Markdown, value=doc_str),
                    insert_text=snippet,
                    insert_text_format=InsertTextFormat.Snippet,
                    sort_text=f"0{name}",
                )
            )

    elif ctx.scope == Scope.ELEMENT_NAME:
        # Cursor is on an existing element name — offer all element names
        # (VS Code will filter by what's already typed)
        for name in akn_schema.element_names():
            info = akn_schema.get_element_info(name)
            doc_str = _element_doc(name) if info else ""
            items.append(
                CompletionItem(
                    label=name,
                    kind=CompletionItemKind.Class,
                    detail="AKN element",
                    documentation=MarkupContent(kind=MarkupKind.Markdown, value=doc_str),
                    insert_text=name,
                    insert_text_format=InsertTextFormat.PlainText,
                    sort_text=f"0{name}",
                )
            )

    elif ctx.scope == Scope.ELEMENT_BODY:
        for key in _ELEMENT_BODY_KEYS:
            if key in existing:
                continue
            snippet = _element_body_snippet(key, ctx.element_name)
            items.append(_key_completion(key, f"Element {key}", snippet))

    elif ctx.scope == Scope.ATTRIBUTES:
        if ctx.element_name:
            for attr in akn_schema.get_attributes(ctx.element_name):
                if attr.name in existing:
                    continue
                detail = "required attribute" if attr.required else "optional attribute"
                doc_str = _attribute_doc(attr)
                # Build snippet with required field pre-filled
                req_str = "true" if attr.required else "false"
                snippet = f"{attr.name}:\n  required: {req_str}\n"
                if attr.enum_values:
                    snippet = f"{attr.name}:\n  required: {req_str}\n  values:\n    - $1\n"
                items.append(
                    CompletionItem(
                        label=attr.name,
                        kind=CompletionItemKind.Property,
                        detail=detail,
                        documentation=MarkupContent(kind=MarkupKind.Markdown, value=doc_str),
                        insert_text=snippet,
                        insert_text_format=InsertTextFormat.Snippet,
                        sort_text=f"{'0' if attr.required else '1'}{attr.name}",
                    )
                )

    elif ctx.scope == Scope.ATTRIBUTE_NAME:
        # Cursor is on an existing attribute name — offer all attributes
        # for the parent element (VS Code filters by typed text)
        if ctx.element_name:
            for attr in akn_schema.get_attributes(ctx.element_name):
                detail = "required attribute" if attr.required else "optional attribute"
                doc_str = _attribute_doc(attr)
                items.append(
                    CompletionItem(
                        label=attr.name,
                        kind=CompletionItemKind.Property,
                        detail=detail,
                        documentation=MarkupContent(kind=MarkupKind.Markdown, value=doc_str),
                        insert_text=attr.name,
                        insert_text_format=InsertTextFormat.PlainText,
                        sort_text=f"{'0' if attr.required else '1'}{attr.name}",
                    )
                )

    elif ctx.scope == Scope.ATTRIBUTE_BODY:
        for key in _ATTRIBUTE_BODY_KEYS:
            if key in existing:
                continue
            if key == "required":
                items.append(
                    _key_completion(
                        key,
                        "Whether this attribute is required",
                        "required: ${1|true,false|}\n",
                    )
                )
            elif key == "values":
                items.append(_key_completion(key, "Allowed enum values", "values:\n  - $1\n"))

    elif ctx.scope == Scope.ATTRIBUTE_VALUES:
        if ctx.element_name and ctx.attribute_name:
            for attr in akn_schema.get_attributes(ctx.element_name):
                if attr.name == ctx.attribute_name:
                    for val in attr.enum_values:
                        if val in existing:
                            continue
                        items.append(
                            CompletionItem(
                                label=val,
                                kind=CompletionItemKind.Value,
                                detail="enum value",
                                insert_text=f"- {val}",
                                insert_text_format=InsertTextFormat.PlainText,
                            )
                        )
                    break

    elif ctx.scope == Scope.CHILDREN:
        if ctx.element_name:
            # Offer 'choice:' for any element with 2+ possible children
            # so the user can create exclusive branches in their profile.
            all_children = akn_schema.get_children(ctx.element_name)
            if len(all_children) >= 2 and "choice" not in existing:
                examples = sorted(c for c in all_children if c not in excluded)[:6]
                examples_str = ", ".join(examples)
                ellipsis = ", …" if len(all_children) > 6 else ""
                items.append(
                    CompletionItem(
                        label="choice",
                        kind=CompletionItemKind.Property,
                        detail="restrict to exclusive branches",
                        documentation=MarkupContent(
                            kind=MarkupKind.Markdown,
                            value=(
                                "**choice** — Declare mutually exclusive "
                                "child groups.\n\n"
                                "Group children into branches. Only ONE "
                                "branch applies per element instance, "
                                "restricting the schema to your use case.\n\n"
                                f"Available children: {examples_str}{ellipsis}"
                            ),
                        ),
                        insert_text="choice:",
                        insert_text_format=InsertTextFormat.PlainText,
                        sort_text="0__choice",
                        command=Command(
                            title="Suggest branches",
                            command="akn-profiler.insertNewLineAndSuggest",
                        ),
                    )
                )

            # Build a child_name → choice group label map for richer details
            child_group_labels: dict[str, str] = {}
            choice_groups = akn_schema.get_choice_groups(ctx.element_name)
            for cg in choice_groups:
                for branch in cg.branches:
                    label = branch.label or branch.branch_id
                    for member in branch.elements:
                        child_group_labels.setdefault(member, label)

            for child_name in akn_schema.get_children(ctx.element_name):
                if child_name in excluded:
                    continue
                req_children = {c.name for c in akn_schema.get_required_children(ctx.element_name)}
                is_req = child_name in req_children
                detail = "required child" if is_req else "optional child"
                group_label = child_group_labels.get(child_name)
                if group_label:
                    detail = f"{detail} [{group_label}]"
                info = akn_schema.get_element_info(child_name)
                doc_str = info.doc[:120] if info and info.doc else ""
                # Find cardinality from parent's ChildInfo
                card = ""
                parent_info = akn_schema.get_element_info(ctx.element_name)
                if parent_info:
                    for c in parent_info.children:
                        if c.name == child_name:
                            card = c.cardinality
                            break
                snippet = f'{child_name}: "{card}"' if card else f"{child_name}:"
                # Sort by required first, then by group, then alphabetical
                group_sort = group_label or "zzz"
                items.append(
                    CompletionItem(
                        label=child_name,
                        kind=CompletionItemKind.Class,
                        detail=f"{detail} ({card})" if card else detail,
                        documentation=MarkupContent(kind=MarkupKind.Markdown, value=doc_str),
                        insert_text=snippet,
                        insert_text_format=InsertTextFormat.PlainText,
                        sort_text=f"{'0' if is_req else '1'}_{group_sort}_{child_name}",
                    )
                )

    elif ctx.scope == Scope.STRUCTURE:
        if ctx.element_name:
            for child_name in akn_schema.get_children(ctx.element_name):
                if child_name in existing:
                    continue
                items.append(
                    CompletionItem(
                        label=child_name,
                        kind=CompletionItemKind.Class,
                        detail="hierarchy level",
                        insert_text=f"- {child_name}",
                        insert_text_format=InsertTextFormat.PlainText,
                    )
                )

    elif ctx.scope == Scope.CHOICE_BRANCHES:
        if ctx.element_name:
            # Inside choice: — offer child elements as exclusive options.
            # Each entry is a dict key: "elementName: \"card\""
            all_children = akn_schema.get_children(ctx.element_name)
            parent_info = akn_schema.get_element_info(ctx.element_name)
            # Count how many valid choice elements already exist so we
            # can chain auto-suggest for the first two picks.
            existing_choice_count = len([k for k in existing if k in set(all_children)])
            for child_name in all_children:
                if child_name in excluded:
                    continue
                info = akn_schema.get_element_info(child_name)
                doc_str = info.doc[:120] if info and info.doc else ""
                # Look up XSD cardinality for this child
                card = ""
                if parent_info:
                    for c in parent_info.children:
                        if c.name == child_name:
                            card = c.cardinality
                            break
                if card:
                    branch_text = f'{child_name}: "{card}"'
                else:
                    branch_text = f"{child_name}:"
                # Chain auto-suggest: if fewer than 2 choice elements
                # exist, attach a command to prompt for the next one.
                chain_cmd = None
                if existing_choice_count < 1:
                    chain_cmd = Command(
                        title="Add next choice element",
                        command="akn-profiler.insertNewLineAndSuggest",
                    )
                items.append(
                    CompletionItem(
                        label=child_name,
                        kind=CompletionItemKind.Class,
                        detail=f"exclusive option ({card})" if card else "exclusive option",
                        documentation=MarkupContent(kind=MarkupKind.Markdown, value=doc_str)
                        if doc_str
                        else None,
                        insert_text=branch_text,
                        insert_text_format=InsertTextFormat.PlainText,
                        command=chain_cmd,
                    )
                )

    return CompletionList(is_incomplete=False, items=items)


def _key_completion(label: str, detail: str, snippet: str) -> CompletionItem:
    """Helper to create a key-completion item with a snippet."""
    return CompletionItem(
        label=label,
        kind=CompletionItemKind.Property,
        detail=detail,
        insert_text=snippet,
        insert_text_format=InsertTextFormat.Snippet,
    )


def _element_body_snippet(key: str, element_name: str | None) -> str:
    """Return snippet text for a key inside an element body."""
    if key == "profileNote":
        return 'profileNote: "$1"\n'
    if key == "attributes":
        return "attributes:\n  $1:\n"
    if key == "children":
        return "children:\n  $1:\n"
    if key == "structure":
        return "structure:\n  - $1\n"
    return f"{key}: $1\n"


def _element_doc(name: str) -> str:
    """Build a Markdown documentation string for an AKN element."""
    if akn_schema is None:
        return ""
    info = akn_schema.get_element_info(name)
    if info is None:
        return ""
    parts = []
    if info.doc:
        parts.append(info.doc)
    # Children summary
    child_names = [c.name for c in info.children]
    req_names = [c.name for c in info.children if c.required]
    if req_names:
        parts.append(f"\n**Required children:** {', '.join(req_names)}")
    opt_names = [n for n in child_names if n not in set(req_names)]
    if opt_names:
        display = opt_names[:10]
        suffix = f" (+{len(opt_names) - 10} more)" if len(opt_names) > 10 else ""
        parts.append(f"**Optional children:** {', '.join(display)}{suffix}")
    # Attributes summary
    req_attrs = [a.name for a in info.attributes if a.required]
    opt_attrs = [a.name for a in info.attributes if not a.required]
    if req_attrs:
        parts.append(f"**Required attributes:** {', '.join(req_attrs)}")
    if opt_attrs:
        display = opt_attrs[:10]
        suffix = f" (+{len(opt_attrs) - 10} more)" if len(opt_attrs) > 10 else ""
        parts.append(f"**Optional attributes:** {', '.join(display)}{suffix}")
    # Choice group summary — only show exclusive choices.
    # Free-mix groups (maxOccurs > 1) are effectively optional children
    # and are already listed above.
    if info.choice_groups:
        for cg in info.choice_groups:
            if not cg.exclusive:
                continue  # skip free-mix groups
            branch_descs: list[str] = []
            for br in cg.branches:
                elems = sorted(br.elements)
                if len(elems) == 1:
                    branch_descs.append(f"`{elems[0]}`")
                elif len(elems) <= 4:
                    branch_descs.append(", ".join(f"`{e}`" for e in elems))
                else:
                    shown = ", ".join(f"`{e}`" for e in elems[:4])
                    branch_descs.append(f"{shown}, … (+{len(elems) - 4} more)")
            if branch_descs:
                either_parts = " OR ".join(branch_descs)
                req_text = "required" if cg.min_occurs >= 1 else "optional"
                parts.append(
                    f"**Either/or** ({req_text}): Must contain either "
                    f"{either_parts} — but not both."
                )
    return "\n\n".join(parts) if parts else name


def _attribute_doc(attr: Any) -> str:
    """Build a Markdown documentation string for an element attribute."""
    parts = []
    parts.append(f"**Type:** `{attr.type_hint}`")
    if attr.required:
        parts.append("**Required** in XSD")
    if attr.pattern:
        parts.append(f"**Pattern:** `{attr.pattern}`")
    if attr.enum_values:
        vals = attr.enum_values[:15]
        suffix = f" (+{len(attr.enum_values) - 15} more)" if len(attr.enum_values) > 15 else ""
        parts.append(f"**Values:** {', '.join(vals)}{suffix}")
    return "\n\n".join(parts) if parts else attr.name


# ==================================================================
# textDocument/codeLens
# ==================================================================


@server.feature(TEXT_DOCUMENT_CODE_LENS)
@_safe_handler([])
def code_lens(params: CodeLensParams) -> list[CodeLens]:
    """Show a CodeLens button on empty files to bootstrap a new profile."""
    doc = server.workspace.get_text_document(params.text_document.uri)
    source = doc.source
    lenses: list[CodeLens] = []

    if not source.strip():
        lenses.append(
            CodeLens(
                range=Range(start=Position(0, 0), end=Position(0, 0)),
                command=Command(
                    title="Initialize Profile Scaffold",
                    command="akn-profiler.insertScaffold",
                    arguments=[],
                ),
            )
        )

    return lenses


# ==================================================================
# textDocument/hover
# ==================================================================


@server.feature(TEXT_DOCUMENT_HOVER)
@_safe_handler(None)
def hover(params: HoverParams) -> Hover | None:
    """Show XSD documentation when hovering over profile keys/values."""
    if akn_schema is None:
        return None

    doc = server.workspace.get_text_document(params.text_document.uri)
    ctx = resolve_context(doc.source, params.position.line, params.position.character)

    content: str | None = None

    # --- Profile-level key documentation ---
    _PROFILE_KEY_DOCS = {
        "profile": (
            "**profile** — Root key for an Akoma Ntoso application profile.\n\n"
            "Defines which elements, attributes, document types, and metadata "
            "sections are allowed in conforming AKN documents."
        ),
        "name": "**name** — Human-readable name for this profile (e.g. 'Minimum Act Profile').",
        "version": "**version** — Version string for this profile (e.g. '1.0').",
        "description": (
            "**description** — Free-text description of this profile's purpose and scope."
        ),
        "documentTypes": (
            "**documentTypes** — List of allowed AKN document types.\n\n"
            "Each entry must be a valid child of `<akomaNtoso>` (e.g. `act`, `bill`, `debate`)."
        ),
        "elements": (
            "**elements** — Element restrictions.\n\n"
            "Each key is an XSD element name. Presence means the element is allowed "
            "in this profile. Nested keys define attribute restrictions, allowed "
            "children with cardinality, and structural hierarchy."
        ),
        "children": (
            "**children** — Allowed child elements with optional cardinality overrides.\n\n"
            "Keys are child element names, values are cardinality strings "
            '(e.g. `"1..1"`, `"0..*"`) or empty for XSD defaults.\n\n'
            "Cardinality must be at least as strict as the XSD — "
            "loosening the schema is not allowed.\n\n"
            "Use `choice:` to declare mutually exclusive child branches "
            "(e.g. section OR subchapter, but not both)."
        ),
        "choice": (
            "**choice** — Mutually exclusive children.\n\n"
            "Each key is an exclusive child element — only ONE of the listed "
            "children may appear per element instance.\n\n"
            "Example:\n"
            "```yaml\n"
            "choice:\n"
            '  section: "1..*"\n'
            '  subchapter: "1..*"\n'
            "```"
        ),
        "attributes": (
            "**attributes** — Attribute restrictions.\n\n"
            "Each key is an XSD attribute name. Use `required: true/false` to "
            "indicate whether the attribute must be present, and optionally "
            "restrict `values:` to a subset of the XSD enum."
        ),
        "structure": (
            "**structure** — Ordered hierarchy of structural elements.\n\n"
            "Defines the nesting order (e.g. `chapter → article → paragraph`). "
            "Each consecutive pair must form a valid parent→child in the XSD."
        ),
        "values": (
            "**values** — Restricts allowed enum values.\n\n"
            "Must be a subset of the XSD-defined values for this attribute."
        ),
        "required": (
            "**required** — Whether this attribute must be present.\n\n"
            "Must be at least as strict as the XSD — setting `false` on an "
            "XSD-required attribute will emit an error."
        ),
        "profileNote": (
            "**profileNote** — Curator annotation for this element.\n\n"
            "Explanatory text for readers of the profile and documentation "
            "generators. Use it to record design rationale, mappings to local "
            "terminology, or original-language terms.\n\n"
            "Does **not** affect validation."
        ),
    }

    if ctx.scope == Scope.PROFILE:
        word = _word_at(doc.source, params.position.line, params.position.character)
        if word in _PROFILE_KEY_DOCS:
            content = _PROFILE_KEY_DOCS[word]

    elif ctx.scope in (Scope.ELEMENT_NAME, Scope.ELEMENT_BODY) and ctx.element_name:
        word = _word_at(doc.source, params.position.line, params.position.character)
        if word and word in _PROFILE_KEY_DOCS:
            content = _PROFILE_KEY_DOCS[word]
        else:
            content = _element_doc(ctx.element_name)

    elif (
        ctx.scope in (Scope.ATTRIBUTE_NAME, Scope.ATTRIBUTE_BODY)
        and ctx.element_name
        and ctx.attribute_name
    ):
        for attr in akn_schema.get_attributes(ctx.element_name):
            if attr.name == ctx.attribute_name:
                content = _attribute_doc(attr)
                break

    elif ctx.scope == Scope.ELEMENTS:
        word = _word_at(doc.source, params.position.line, params.position.character)
        if word and word in _PROFILE_KEY_DOCS:
            content = _PROFILE_KEY_DOCS[word]
        elif word and akn_schema.has_element(word):
            content = _element_doc(word)

    elif ctx.scope == Scope.DOCUMENT_TYPES:
        word = _word_at(doc.source, params.position.line, params.position.character)
        if word and akn_schema.has_element(word):
            info = akn_schema.get_element_info(word)
            content = info.doc if info and info.doc else f"AKN document type: {word}"

    elif ctx.scope == Scope.CHILDREN:
        word = _word_at(doc.source, params.position.line, params.position.character)
        if word and word in _PROFILE_KEY_DOCS:
            content = _PROFILE_KEY_DOCS[word]
        elif word and akn_schema.has_element(word):
            # Show element doc + cardinality context from parent
            elem_doc = _element_doc(word)
            if ctx.element_name:
                parent_info = akn_schema.get_element_info(ctx.element_name)
                if parent_info:
                    for c in parent_info.children:
                        if c.name == word:
                            elem_doc += (
                                f"\n\n**XSD cardinality in `<{ctx.element_name}>`:** "
                                f"`{c.cardinality}` "
                                f"(min={c.min_occurs}, max={'∞' if c.max_occurs is None else c.max_occurs})"
                            )
                            # Show choice group membership
                            if c.choice_group_ids:
                                for cgid in c.choice_group_ids:
                                    for cg in parent_info.choice_groups:
                                        if cg.group_id == cgid:
                                            mode = "exclusive" if cg.exclusive else "free mix"
                                            req = "required" if cg.min_occurs >= 1 else "optional"
                                            # Find the branch this child belongs to
                                            branch_label = None
                                            for br in cg.branches:
                                                if word in br.elements:
                                                    branch_label = br.label
                                                    break
                                            group_desc = (
                                                f"`{branch_label}`" if branch_label else cgid
                                            )
                                            elem_doc += (
                                                f"\n\n**Choice group:** {group_desc} "
                                                f"({mode}, {req})"
                                            )
                            break
            content = elem_doc

    # Fallback: check if the word on cursor matches a structural key
    if content is None:
        word = _word_at(doc.source, params.position.line, params.position.character)
        if word and word in _PROFILE_KEY_DOCS:
            content = _PROFILE_KEY_DOCS[word]

    if content:
        return Hover(
            contents=MarkupContent(kind=MarkupKind.Markdown, value=content),
        )
    return None


def _word_at(source: str, line: int, character: int) -> str | None:
    """Extract the word under the cursor."""
    lines = source.splitlines()
    if line >= len(lines):
        return None
    text = lines[line]
    if character >= len(text):
        return None

    # Find word boundaries
    start = character
    while start > 0 and (text[start - 1].isalnum() or text[start - 1] in ("_", "-")):
        start -= 1
    end = character
    while end < len(text) and (text[end].isalnum() or text[end] in ("_", "-")):
        end += 1

    word = text[start:end]
    return word if word else None


# ==================================================================
# textDocument/codeAction
# ==================================================================


@server.feature(TEXT_DOCUMENT_CODE_ACTION)
@_safe_handler([])
def code_action(params: CodeActionParams) -> list[CodeAction]:
    """Provide quick-fix code actions and contextual 'Add …' lightbulb actions."""
    if akn_schema is None:
        return []

    actions: list[CodeAction] = []
    uri = params.text_document.uri
    doc = server.workspace.get_text_document(uri)

    # ------------------------------------------------------------------
    # Phase 1: diagnostic-based quick-fixes
    # ------------------------------------------------------------------
    for diagnostic in params.context.diagnostics:
        if diagnostic.source != "akn-profiler":
            continue
        msg = diagnostic.message
        line = diagnostic.range.start.line

        # Get rule_id from diagnostic code field
        rule_id = str(diagnostic.code) if diagnostic.code else ""

        if rule_id == "vocab.unknown-element":
            # Suggest closest element name
            unknown = _extract_name_from_msg(msg)
            if unknown:
                suggestions = difflib.get_close_matches(
                    unknown, akn_schema.element_names(), n=3, cutoff=0.5
                )
                for suggestion in suggestions:
                    edit = _replace_word_edit(uri, doc.source, line, unknown, suggestion)
                    if edit:
                        actions.append(
                            CodeAction(
                                title=f"Replace with '{suggestion}'",
                                kind=CodeActionKind.QuickFix,
                                diagnostics=[diagnostic],
                                edit=edit,
                            )
                        )

        elif rule_id == "vocab.unknown-attribute":
            unknown = _extract_name_from_msg(msg)
            elem_name = _find_element_context(doc.source, line)
            if unknown and elem_name:
                attr_names = [a.name for a in akn_schema.get_attributes(elem_name)]
                suggestions = difflib.get_close_matches(unknown, attr_names, n=3, cutoff=0.5)
                for suggestion in suggestions:
                    edit = _replace_word_edit(uri, doc.source, line, unknown, suggestion)
                    if edit:
                        actions.append(
                            CodeAction(
                                title=f"Replace with '{suggestion}'",
                                kind=CodeActionKind.QuickFix,
                                diagnostics=[diagnostic],
                                edit=edit,
                            )
                        )

        elif rule_id == "vocab.unknown-doctype":
            unknown = _extract_name_from_msg(msg)
            if unknown:
                valid = akn_schema.get_children("akomaNtoso")
                suggestions = difflib.get_close_matches(unknown, valid, n=3, cutoff=0.4)
                for suggestion in suggestions:
                    edit = _replace_word_edit(uri, doc.source, line, unknown, suggestion)
                    if edit:
                        actions.append(
                            CodeAction(
                                title=f"Replace with '{suggestion}'",
                                kind=CodeActionKind.QuickFix,
                                diagnostics=[diagnostic],
                                edit=edit,
                            )
                        )

        elif rule_id == "parse.not-a-mapping":
            # Empty file or non-mapping content
            actions.append(
                CodeAction(
                    title="Insert profile scaffold",
                    kind=CodeActionKind.QuickFix,
                    diagnostics=[diagnostic],
                    edit=WorkspaceEdit(
                        changes={
                            uri: [
                                TextEdit(
                                    range=Range(
                                        start=Position(line=0, character=0),
                                        end=Position(line=0, character=0),
                                    ),
                                    new_text=(
                                        "profile:\n"
                                        '  name: ""\n'
                                        '  version: ""\n'
                                        '  description: ""\n'
                                        "\n"
                                        "  documentTypes:\n"
                                        "\n"
                                        "  elements:\n"
                                        "    akomaNtoso:\n"
                                    ),
                                )
                            ]
                        }
                    ),
                )
            )

        elif rule_id == "parse.missing-profile-key":
            actions.append(
                CodeAction(
                    title="Insert profile scaffold",
                    kind=CodeActionKind.QuickFix,
                    diagnostics=[diagnostic],
                    edit=WorkspaceEdit(
                        changes={
                            uri: [
                                TextEdit(
                                    range=Range(
                                        start=Position(line=0, character=0),
                                        end=Position(line=0, character=0),
                                    ),
                                    new_text=(
                                        "profile:\n"
                                        '  name: ""\n'
                                        '  version: ""\n'
                                        '  description: ""\n'
                                        "\n"
                                        "  documentTypes:\n"
                                        "\n"
                                        "  elements:\n"
                                        "    akomaNtoso:\n"
                                    ),
                                )
                            ]
                        }
                    ),
                )
            )

        elif rule_id == "identity.doctype-without-element-restriction":
            # Extract doc type: "Document type 'act' is listed in documentTypes …"
            dt_name = _extract_name_from_msg(msg)
            if dt_name:
                cascade_edit = _build_cascade_add_edit(uri, doc.source, dt_name)
                if cascade_edit:
                    actions.append(
                        CodeAction(
                            title=(f"Define '{dt_name}' with required attributes and children"),
                            kind=CodeActionKind.QuickFix,
                            diagnostics=[diagnostic],
                            edit=cascade_edit,
                            is_preferred=True,
                        )
                    )

        elif rule_id == "strictness.missing-required-element":
            # Extract element name: "<elemName> is on the required-child chain …"
            m = _re.search(r"<(\w[\w-]*)>", msg)
            if m:
                elem_name = m.group(1)
                cascade_edit = _build_cascade_add_edit(uri, doc.source, elem_name)
                if cascade_edit:
                    actions.append(
                        CodeAction(
                            title=(f"Define '{elem_name}' with required attributes and children"),
                            kind=CodeActionKind.QuickFix,
                            diagnostics=[diagnostic],
                            edit=cascade_edit,
                            is_preferred=True,
                        )
                    )

        elif rule_id == "strictness.undeclared-child-element":
            # Extract child element name: "'childName' is listed as a child …"
            child_name = _extract_name_from_msg(msg)
            if child_name:
                cascade_edit = _build_cascade_add_edit(uri, doc.source, child_name)
                if cascade_edit:
                    actions.append(
                        CodeAction(
                            title=(f"Define '{child_name}' with required attributes and children"),
                            kind=CodeActionKind.QuickFix,
                            diagnostics=[diagnostic],
                            edit=cascade_edit,
                            is_preferred=True,
                        )
                    )

        elif rule_id == "choice.required-group-empty":
            pass  # No quick-fix — user resolves via Add child completions

        elif rule_id == "choice.incomplete-branches":
            pass  # No quick-fix — user adds branches via completions

        elif rule_id == "choice.exclusive-branch-conflict":
            # Suggest using choice: to express exclusivity
            elem_ctx = _find_element_context(doc.source, line)
            if elem_ctx:
                actions.append(
                    CodeAction(
                        title="Use 'choice:' to declare exclusive branches",
                        kind=CodeActionKind.QuickFix,
                        diagnostics=[diagnostic],
                    )
                )

            # Also suggest removing conflicting children
            import re as _re_local

            conflict_m = _re_local.search(r"Conflicting: (.+)$", msg)
            if conflict_m:
                conflict_names = [n.strip() for n in conflict_m.group(1).split(",")]
                for cname in conflict_names:
                    remove_edit = _remove_child_line_edit(uri, doc.source, cname)
                    if remove_edit:
                        actions.append(
                            CodeAction(
                                title=f"Remove '{cname}' to resolve conflict",
                                kind=CodeActionKind.QuickFix,
                                diagnostics=[diagnostic],
                                edit=remove_edit,
                            )
                        )

    # ------------------------------------------------------------------
    # Phase 2: contextual "Add …" lightbulb actions
    # ------------------------------------------------------------------
    actions.extend(_add_item_actions(uri, doc.source, params.range.start.line))

    return actions


def _extract_name_from_msg(msg: str) -> str | None:
    """Extract a quoted name from a diagnostic message like \"'foo' is not ...\"."""
    import re

    m = re.search(r"'([^']+)'", msg)
    return m.group(1) if m else None


def _replace_word_edit(
    uri: str, source: str, line: int, old_word: str, new_word: str
) -> WorkspaceEdit | None:
    """Create a WorkspaceEdit that replaces *old_word* with *new_word* on *line*."""
    lines = source.splitlines()
    if line >= len(lines):
        return None
    text = lines[line]
    col = text.find(old_word)
    if col < 0:
        return None
    return WorkspaceEdit(
        changes={
            uri: [
                TextEdit(
                    range=Range(
                        start=Position(line=line, character=col),
                        end=Position(line=line, character=col + len(old_word)),
                    ),
                    new_text=new_word,
                )
            ]
        }
    )


def _find_element_context(source: str, line: int) -> str | None:
    """Walk backwards from *line* to find the enclosing element name.

    Also checks the *current* line so that bare element entries like
    ``body:`` (with no sub-keys) are recognised when the error line
    points directly at the element name.
    """
    import re

    _STRUCTURAL_NAMES = {
        "attributes",
        "children",
        "choice",
        "structure",
        "required",
        "values",
        "elements",
        "profile",
        "profileNote",
        "documentTypes",
        "name",
        "version",
        "description",
    }

    lines = source.splitlines()
    if line >= len(lines):
        return None

    # Check the current line first — covers bare element entries.
    cur = lines[line]
    m = re.match(r"^\s+(\w[\w-]*):", cur)
    if m:
        key = m.group(1)
        if key not in _STRUCTURAL_NAMES:
            return key

    target_indent = len(cur) - len(cur.lstrip())
    for i in range(line - 1, -1, -1):
        ln = lines[i]
        indent = len(ln) - len(ln.lstrip())
        m = re.match(r"^\s+(\w[\w-]*):", ln)
        if m and indent < target_indent:
            key = m.group(1)
            if key not in _STRUCTURAL_NAMES:
                return key
    return None


# ------------------------------------------------------------------
# Cascade add / remove helpers
# ------------------------------------------------------------------


def _build_cascade_add_edit(uri: str, source: str, element_name: str) -> WorkspaceEdit | None:
    """Build a WorkspaceEdit that adds *element_name* and its required chain
    to the profile using the cascade expand logic.

    Returns ``None`` if the schema doesn't know the element or no changes
    are needed.
    """
    if akn_schema is None or not akn_schema.has_element(element_name):
        return None

    new_text = expand_element(source, element_name, akn_schema)
    if new_text == source:
        return None  # nothing to change

    return _full_document_edit(uri, source, new_text)


def _build_child_remove_edit(
    uri: str, source: str, parent_name: str, child_name: str
) -> WorkspaceEdit | None:
    """Build a WorkspaceEdit that removes *child_name* from *parent_name*'s
    children list and, if no other element references *child_name*,
    also removes its element definition (and orphaned descendants).

    Returns ``None`` if no changes are needed.
    """
    if akn_schema is None:
        return None

    raw = yaml.safe_load(source)
    if not isinstance(raw, dict) or "profile" not in raw:
        return None

    profile = raw["profile"]
    if not isinstance(profile, dict):
        return None

    elements = profile.get("elements", {})
    if not isinstance(elements, dict):
        return None

    # Step 1: Remove child from parent's children list
    parent_data = elements.get(parent_name)
    if not isinstance(parent_data, dict):
        return None
    children = parent_data.get("children")
    if not isinstance(children, dict) or child_name not in children:
        return None

    del children[child_name]
    if not children:
        del parent_data["children"]

    # Step 2: Check if child_name is still referenced by any other element
    still_referenced = False
    for other_name, other_data in elements.items():
        if not isinstance(other_data, dict):
            continue
        other_children = other_data.get("children")
        if isinstance(other_children, dict) and child_name in other_children:
            still_referenced = True
            break

    # Step 3: If orphaned, remove child and its orphaned descendants
    if not still_referenced and child_name in elements:
        to_remove = _collect_orphaned_elements(child_name, elements)
        for name in to_remove:
            elements.pop(name, None)
        # Clean up any remaining references to removed elements
        for e_data in elements.values():
            if not isinstance(e_data, dict):
                continue
            ch = e_data.get("children")
            if isinstance(ch, dict):
                for removed in to_remove:
                    ch.pop(removed, None)
                if not ch:
                    del e_data["children"]

    new_text = yaml.dump(
        raw,
        Dumper=_ProfileDumper,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=120,
    )

    return _full_document_edit(uri, source, new_text)


def _collect_orphaned_elements(elem_name: str, elements: dict) -> set[str]:
    """Collect *elem_name* and all descendants that would become orphaned
    (not referenced by any remaining element)."""
    to_remove: set[str] = {elem_name}
    queue = [elem_name]
    while queue:
        current = queue.pop()
        entry = elements.get(current)
        if not isinstance(entry, dict):
            continue
        children = entry.get("children", {})
        if not isinstance(children, dict):
            continue
        for child in children:
            if child in to_remove:
                continue
            # Check if any element NOT being removed still references this child
            orphan = True
            for other_name, other_data in elements.items():
                if other_name in to_remove or other_name == current:
                    continue
                if not isinstance(other_data, dict):
                    continue
                other_ch = other_data.get("children")
                if isinstance(other_ch, dict) and child in other_ch:
                    orphan = False
                    break
            if orphan and child in elements:
                to_remove.add(child)
                queue.append(child)
    return to_remove


def _full_document_edit(uri: str, old_source: str, new_text: str) -> WorkspaceEdit | None:
    """Replace the entire document content."""
    if new_text == old_source:
        return None
    lines = old_source.splitlines()
    last_line = max(0, len(lines) - 1)
    last_char = len(lines[last_line]) if lines else 0
    return WorkspaceEdit(
        changes={
            uri: [
                TextEdit(
                    range=Range(
                        start=Position(line=0, character=0),
                        end=Position(line=last_line, character=last_char),
                    ),
                    new_text=new_text,
                )
            ]
        }
    )


def _remove_child_line_edit(uri: str, source: str, child_name: str) -> WorkspaceEdit | None:
    """Build a WorkspaceEdit that removes the line declaring *child_name*
    from a ``children:`` section.
    """
    lines = source.splitlines()
    for i, text in enumerate(lines):
        m = _re.match(r"^(\s+)([\w][\w-]*)\s*:", text)
        if m and m.group(2) == child_name:
            # Remove the entire line (including the newline)
            return WorkspaceEdit(
                changes={
                    uri: [
                        TextEdit(
                            range=Range(
                                start=Position(line=i, character=0),
                                end=Position(line=i + 1, character=0),
                            ),
                            new_text="",
                        )
                    ]
                }
            )
    return None


def _child_name_at_line(lines: list[str], line_idx: int, expected_indent: int) -> str | None:
    """Extract the child element name from a children: entry line.

    Children entries look like ``        meta:`` or ``        meta: 1..1``
    at the expected indent level.
    """
    if line_idx >= len(lines):
        return None
    text = lines[line_idx]
    stripped = text.strip()
    if not stripped or ":" not in stripped:
        return None
    ind = len(text) - len(stripped)
    if ind != expected_indent:
        return None
    m = _re.match(r"^\s*([\w][\w-]*)\s*:", text)
    return m.group(1) if m else None


# ------------------------------------------------------------------
# Helpers for contextual "Add …" lightbulb actions
# ------------------------------------------------------------------

# Subsection keys that are NOT element names
_PROFILE_KEYS = frozenset(
    {
        "attributes",
        "children",
        "choice",
        "structure",
        "required",
        "values",
        "elements",
        "profile",
        "profileNote",
        "documentTypes",
        "name",
        "version",
        "description",
    }
)


def _section_end(lines: list[str], start: int, indent: int) -> int:
    """Return the last content line belonging to the block starting at *start*."""
    last = start
    for i in range(start + 1, len(lines)):
        s = lines[i].strip()
        if not s:
            continue
        if (len(lines[i]) - len(s)) <= indent:
            break
        last = i
    return last


def _make_add_action(
    title: str,
    uri: str,
    insert_after_line: int,
    item_indent: int,
    section_header: str | None = None,
    is_preferred: bool = False,
) -> CodeAction:
    """Build a CodeAction that inserts a blank item line (and optional header).

    After the edit is applied the client-side ``akn-profiler.cursorToLine``
    command positions the cursor on the new line and triggers completion.
    """
    padding = " " * item_indent
    insert_pos = Position(line=insert_after_line + 1, character=0)

    if section_header:
        header_padding = " " * max(0, item_indent - 2)
        new_text = f"{header_padding}{section_header}\n{padding}"
        cursor_line = insert_after_line + 2
    else:
        new_text = padding
        cursor_line = insert_after_line + 1

    # We insert *before* the next line (i.e. at col 0 of the line after
    # insert_after_line).  If insert_after_line is the last line of the
    # document we append after it with a leading newline.
    text_edit = TextEdit(
        range=Range(start=insert_pos, end=insert_pos),
        new_text=new_text + "\n",
    )

    return CodeAction(
        title=title,
        kind=CodeActionKind.Refactor,
        edit=WorkspaceEdit(changes={uri: [text_edit]}),
        command=Command(
            title="Position cursor",
            command="akn-profiler.cursorToLine",
            arguments=[cursor_line, item_indent],
        ),
        is_preferred=is_preferred,
    )


def _add_item_actions(uri: str, source: str, cursor_line: int) -> list[CodeAction]:
    """Return contextual 'Add …' code actions for the current cursor line."""
    assert akn_schema is not None
    lines = source.splitlines()
    if not lines:
        return []

    actions: list[CodeAction] = []

    # --- Locate top-level sections ---
    doc_types_line: int | None = None
    doc_types_indent: int | None = None
    elements_line: int | None = None
    elements_indent: int | None = None

    for idx, lt in enumerate(lines):
        stripped = lt.strip()
        if not stripped:
            continue
        indent = len(lt) - len(stripped)
        if stripped == "documentTypes:":
            doc_types_line = idx
            doc_types_indent = indent
        elif stripped == "elements:":
            elements_line = idx
            elements_indent = indent

    # --- documentTypes section ---
    if doc_types_line is not None and doc_types_indent is not None:
        dt_end = _section_end(lines, doc_types_line, doc_types_indent)
        if doc_types_line <= cursor_line <= dt_end:
            item_indent = doc_types_indent + 4  # "    - "
            actions.append(
                _make_add_action(
                    "Add document type",
                    uri,
                    dt_end,
                    item_indent,
                    is_preferred=True,
                )
            )

    # --- elements section ---
    if elements_line is None or elements_indent is None:
        return actions

    elem_indent = elements_indent + 2
    sub_indent = elem_indent + 2

    # Build list of element entries
    element_entries: list[tuple[int, str]] = []  # (line, name)
    for i in range(elements_line + 1, len(lines)):
        stripped = lines[i].strip()
        if not stripped:
            continue
        ind = len(lines[i]) - len(stripped)
        if ind <= elements_indent:
            break
        if ind == elem_indent:
            m = _re.match(r"^\s*([\w][\w-]*)\s*:", lines[i])
            if m:
                element_entries.append((i, m.group(1)))

    elements_end = _section_end(lines, elements_line, elements_indent)

    # Cursor on "elements:" header or past last element → "Add element"
    if cursor_line == elements_line:
        actions.append(
            _make_add_action(
                "Add element to profile",
                uri,
                elements_end,
                elem_indent,
                is_preferred=True,
            )
        )
        return actions

    # --- Per-element analysis ---
    for eline, ename in element_entries:
        eend = eline
        for i in range(eline + 1, len(lines)):
            stripped = lines[i].strip()
            if not stripped:
                continue
            if (len(lines[i]) - len(stripped)) <= elem_indent:
                break
            eend = i

        if not (eline <= cursor_line <= eend):
            continue

        # Scan sub-sections of this element
        has_children = has_attributes = has_structure = False
        children_line = children_end = -1
        attributes_line = attributes_end = -1
        structure_line = structure_end = -1

        for i in range(eline + 1, eend + 1):
            stripped = lines[i].strip()
            if not stripped:
                continue
            ind = len(lines[i]) - len(stripped)
            if ind == sub_indent:
                if stripped == "children:":
                    has_children = True
                    children_line = i
                    children_end = _section_end(lines, i, sub_indent)
                elif stripped == "attributes:":
                    has_attributes = True
                    attributes_line = i
                    attributes_end = _section_end(lines, i, sub_indent)
                elif stripped == "structure:":
                    has_structure = True
                    structure_line = i
                    structure_end = _section_end(lines, i, sub_indent)

        # Determine which sub-section the cursor is inside
        in_children = has_children and children_line <= cursor_line <= children_end
        in_attributes = has_attributes and attributes_line <= cursor_line <= attributes_end
        in_structure = has_structure and structure_line <= cursor_line <= structure_end

        # Detect profileNote line
        profile_note_line = -1
        has_profile_note = False
        for i in range(eline + 1, eend + 1):
            stripped_i = lines[i].strip()
            if not stripped_i:
                continue
            ind_i = len(lines[i]) - len(stripped_i)
            if ind_i == sub_indent and stripped_i.startswith("profileNote:"):
                has_profile_note = True
                profile_note_line = i
                break
        in_profile_note = has_profile_note and cursor_line == profile_note_line

        # Detect choice: block within children:
        choice_line = -1
        choice_end = -1
        if has_children:
            for ci in range(children_line + 1, children_end + 1):
                if ci < len(lines) and lines[ci].strip().startswith("choice"):
                    choice_line = ci
                    choice_end = _section_end(lines, ci, sub_indent + 2)
                    break
        in_choice = in_children and choice_line >= 0 and choice_line <= cursor_line <= choice_end

        can_children = akn_schema.has_element(ename) and bool(akn_schema.get_children(ename))
        can_attrs = akn_schema.has_element(ename) and bool(akn_schema.get_attributes(ename))

        # =============================================================
        # Cascading lightbulb actions — deeper scopes inherit parent
        # actions so "Add child" and "Add attribute" are always visible.
        # Order: choice → children → attribute → profile note
        # =============================================================

        # --- Choice branch ---
        if in_choice:
            actions.append(
                _make_add_action(
                    f"Add choice branch to '{ename}'",
                    uri,
                    choice_end,
                    sub_indent + 4,
                    is_preferred=True,
                )
            )

        # --- Add child (always visible inside element) ---
        if in_children or in_choice or in_profile_note or cursor_line == eline:
            if has_children:
                actions.append(
                    _make_add_action(
                        f"Add child element to '{ename}'",
                        uri,
                        children_end,
                        sub_indent + 2,
                        is_preferred=not any(a.is_preferred for a in actions),
                    )
                )
            elif can_children:
                actions.append(
                    _make_add_action(
                        f"Add child element to '{ename}' (new children section)",
                        uri,
                        eend,
                        sub_indent + 2,
                        section_header="children:",
                    )
                )

        # --- Add attribute (always visible inside element) ---
        if in_attributes or in_children or in_choice or in_profile_note or cursor_line == eline:
            if has_attributes:
                actions.append(
                    _make_add_action(
                        f"Add attribute to '{ename}'",
                        uri,
                        attributes_end,
                        sub_indent + 2,
                        is_preferred=in_attributes and not any(a.is_preferred for a in actions),
                    )
                )
            elif can_attrs:
                actions.append(
                    _make_add_action(
                        f"Add attribute to '{ename}' (new attributes section)",
                        uri,
                        eend,
                        sub_indent + 2,
                        section_header="attributes:",
                    )
                )

        # --- Add profile note (always last) ---
        if not has_profile_note:
            padding = " " * sub_indent
            insert_pos = Position(line=eline + 1, character=0)
            note_text = f'{padding}profileNote: ""\n'
            # Cursor between the quotes: sub_indent + len('profileNote: "')
            cursor_col = sub_indent + 14
            actions.append(
                CodeAction(
                    title=f"Add profile note to '{ename}'",
                    kind=CodeActionKind.Refactor,
                    edit=WorkspaceEdit(
                        changes={
                            uri: [
                                TextEdit(
                                    range=Range(start=insert_pos, end=insert_pos),
                                    new_text=note_text,
                                )
                            ]
                        }
                    ),
                    command=Command(
                        title="Position cursor",
                        command="akn-profiler.cursorToLine",
                        arguments=[eline + 1, cursor_col, False],
                    ),
                )
            )

        # --- Remove child under cursor ---
        if in_children:
            child_on_cursor = _child_name_at_line(lines, cursor_line, sub_indent + 2)
            if child_on_cursor and child_on_cursor not in _PROFILE_KEYS:
                remove_edit = _build_child_remove_edit(uri, source, ename, child_on_cursor)
                if remove_edit:
                    actions.append(
                        CodeAction(
                            title=(
                                f"Remove '{child_on_cursor}' from '{ename}' "
                                f"and delete orphaned definitions"
                            ),
                            kind=CodeActionKind.Refactor,
                            edit=remove_edit,
                        )
                    )

        # --- Values inside attributes ---
        if in_attributes:
            for i in range(attributes_line + 1, attributes_end + 1):
                stripped = lines[i].strip()
                if not stripped:
                    continue
                ind = len(lines[i]) - len(stripped)
                if stripped == "values:" and ind > sub_indent:
                    vend = _section_end(lines, i, ind)
                    if i <= cursor_line <= vend:
                        actions.append(
                            _make_add_action(
                                "Add value to attribute",
                                uri,
                                vend,
                                ind + 2,
                            )
                        )

        # --- Structure ---
        if in_structure:
            actions.append(
                _make_add_action(
                    f"Add hierarchy level to '{ename}'",
                    uri,
                    structure_end,
                    sub_indent + 2,
                    is_preferred=True,
                )
            )

        # Only process the element whose range contains the cursor
        break

    # If cursor is past last element but still in elements: section,
    # offer "Add element"
    if element_entries:
        last_eline, _ = element_entries[-1]
        last_eend = last_eline
        for i in range(last_eline + 1, len(lines)):
            stripped = lines[i].strip()
            if not stripped:
                continue
            if (len(lines[i]) - len(stripped)) <= elem_indent:
                break
            last_eend = i
        if cursor_line > last_eend and cursor_line <= elements_end + 1:
            actions.append(
                _make_add_action(
                    "Add element to profile",
                    uri,
                    elements_end,
                    elem_indent,
                    is_preferred=True,
                )
            )

    return actions


# ==================================================================
# Semantic token legend (shared between server registration & client)
# ==================================================================

# Token types used for semantic highlighting of profile YAML
_TOKEN_TYPES = [
    SemanticTokenTypes.Class,  # 0 — AKN element names (definitions)
    SemanticTokenTypes.Property,  # 1 — attribute names
    SemanticTokenTypes.Keyword,  # 2 — profile-level keys (profile, name, version, …)
    SemanticTokenTypes.EnumMember,  # 3 — document type names, enum values
    SemanticTokenTypes.Variable,  # 4 — metadata section names
    SemanticTokenTypes.Type,  # 5 — child element references (under children:)
    SemanticTokenTypes.String,  # 6 — cardinality values ("1..1", "0..*")
    SemanticTokenTypes.Macro,  # 7 — boolean values (true/false)
]
_TOKEN_MODIFIERS = [
    SemanticTokenModifiers.Declaration,  # 0 — element/attr first definition
    SemanticTokenModifiers.Readonly,  # 1 — required items
]

_SEMANTIC_LEGEND = SemanticTokensLegend(
    token_types=[t.value for t in _TOKEN_TYPES],
    token_modifiers=[m.value for m in _TOKEN_MODIFIERS],
)

# Profile keys and structural keywords for highlighting
_STRUCTURAL_KEYS = {
    "profile",
    "name",
    "version",
    "description",
    "documentTypes",
    "elements",
    "required",
    "attributes",
    "children",
    "choice",
    "structure",
    "values",
    "profileNote",
}


@server.feature(
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    _SEMANTIC_LEGEND,
)
@_safe_handler(SemanticTokens(data=[]))
def semantic_tokens_full(params: SemanticTokensParams) -> SemanticTokens:
    """Provide semantic tokens so VS Code can highlight AKN-specific words.

    Element names, attribute names, document types, and profile keywords
    get distinct colors, making hoverable items visually obvious.
    """
    doc = server.workspace.get_text_document(params.text_document.uri)
    data = _build_semantic_tokens(doc.source)
    return SemanticTokens(data=data)


def _build_semantic_tokens(source: str) -> list[int]:
    """Walk the YAML source and emit encoded semantic token data.

    The LSP semantic-tokens data format is a flat list of integers
    encoded as groups of 5:
        [deltaLine, deltaStartChar, length, tokenType, tokenModifiers]
    """
    if akn_schema is None:
        return []

    lines = source.splitlines()
    tokens: list[tuple[int, int, int, int, int]] = []  # (line, col, len, type, mod)

    known_elements = set(akn_schema.element_names())
    known_doctypes = set(akn_schema.get_children("akomaNtoso"))

    # Track context via indentation-based section stack
    section_stack: list[tuple[int, str]] = []  # (indent, section_key)

    # Regex for cardinality values: "1..1", "0..*", etc.
    _cardinality_re = _re.compile(r'^["\']?(\d+\.\.(?:\d+|\*))["\'\s]?')

    for line_idx, line_text in enumerate(lines):
        stripped = line_text.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line_text) - len(stripped)

        # Maintain section stack — pop sections at same or lower indent
        while section_stack and indent <= section_stack[-1][0]:
            section_stack.pop()

        # Match "key:" or "key: value" or "key:  # comment"
        key_m = _re.match(r"^(\s*)([\w][\w-]*)\s*:(.*)", line_text)
        if key_m:
            key = key_m.group(2)
            col = len(key_m.group(1))
            length = len(key)
            rest = key_m.group(3).strip()

            # Resolve parent context before classification
            parent_section = section_stack[-1][1] if section_stack else ""

            if parent_section == "attributes" and key not in ("required", "values"):
                # Under attributes:, all keys except required/values are
                # attribute names — Property (yellow), regardless of whether
                # they also appear in _STRUCTURAL_KEYS or known_elements.
                tokens.append((line_idx, col, length, 1, 0))
            elif parent_section == "choice" and key in known_elements:
                # Choice branch element — Type (light blue) + cardinality
                tokens.append((line_idx, col, length, 5, 0))
                if rest:
                    comment_stripped = rest.split("#")[0].strip()
                    card_m = _cardinality_re.match(comment_stripped)
                    if card_m:
                        card_val = card_m.group(1)
                        card_start = line_text.find(card_val, col + length)
                        if card_start >= 0:
                            tokens.append((line_idx, card_start, len(card_val), 6, 0))
            elif key in _STRUCTURAL_KEYS:
                # Keyword token + track section
                tokens.append((line_idx, col, length, 2, 0))
                section_stack.append((indent, key))
                # Also tokenize boolean value on required: lines
                if key == "required" and rest:
                    bool_val = rest.split("#")[0].strip()
                    if bool_val in ("true", "false"):
                        bool_start = line_text.find(bool_val, col + length)
                        if bool_start >= 0:
                            tokens.append((line_idx, bool_start, len(bool_val), 7, 0))
            elif key in known_elements:
                # Determine context from section stack
                if parent_section == "children":
                    # Child reference — distinct type (5 = Type)
                    tokens.append((line_idx, col, length, 5, 0))
                    # Tokenize cardinality value if present (e.g., "1..1")
                    if rest:
                        comment_stripped = rest.split("#")[0].strip()
                        card_m = _cardinality_re.match(comment_stripped)
                        if card_m:
                            # Find position of the cardinality in the original line
                            card_val = card_m.group(1)
                            card_start = line_text.find(card_val, col + length)
                            if card_start >= 0:
                                tokens.append((line_idx, card_start, len(card_val), 6, 0))
                else:
                    # Top-level element definition — type 0 (class)
                    mod = 1 if _is_element_required_in_xsd(key) else 0
                    tokens.append((line_idx, col, length, 0, mod))
            continue

        # Match list items: "- value" or "- value # comment"
        list_m = _re.match(r"^(\s*)-\s+(\S+)", line_text)
        if list_m:
            val = list_m.group(2)
            col = len(list_m.group(1)) + 2  # after "- "
            # Strip trailing comment for matching
            clean_val = val.split("#")[0].strip().strip('"').strip("'")
            parent_section = section_stack[-1][1] if section_stack else ""
            if clean_val in known_doctypes:
                tokens.append((line_idx, col, len(clean_val), 3, 0))
            elif clean_val in known_elements:
                # Element name in a list (e.g., structure levels)
                if parent_section == "structure":
                    tokens.append((line_idx, col, len(clean_val), 5, 0))
                else:
                    tokens.append((line_idx, col, len(clean_val), 0, 0))
            elif parent_section == "values":
                # Attribute enum values — type 3 (enumMember)
                tokens.append((line_idx, col, len(clean_val), 3, 0))
            continue

    # Encode as delta-encoded flat list
    return _encode_tokens(tokens)


def _is_element_required_in_xsd(elem_name: str) -> bool:
    """Check if the element is required by any parent in the XSD."""
    if akn_schema is None:
        return False
    for parent_name in akn_schema.element_names():
        info = akn_schema.get_element_info(parent_name)
        if info is None:
            continue
        for child in info.children:
            if child.name == elem_name and child.required:
                return True
    return False


def _encode_tokens(tokens: list[tuple[int, int, int, int, int]]) -> list[int]:
    """Encode a list of (line, col, length, type, modifiers) into LSP delta format."""
    # Sort by (line, col)
    tokens.sort(key=lambda t: (t[0], t[1]))
    data: list[int] = []
    prev_line = 0
    prev_col = 0
    for line, col, length, token_type, modifiers in tokens:
        delta_line = line - prev_line
        delta_col = col - prev_col if delta_line == 0 else col
        data.extend([delta_line, delta_col, length, token_type, modifiers])
        prev_line = line
        prev_col = col
    return data


# ==================================================================
# Custom LSP commands for the VS Code client
# ==================================================================


@server.command("akn.documentTypes")
def cmd_document_types() -> list[str]:
    """Return the list of valid AKN document types."""
    if akn_schema is None:
        return []
    return get_document_types(akn_schema)


@server.command("akn.initializeProfile")
def cmd_initialize_profile(doc_type: str = "act") -> str:
    """Build a minimal valid profile for the given document type.

    Creates the scaffold, then recursively expands the document type
    element so all required children, attributes, and structure are
    present.
    """
    if akn_schema is None:
        return ""

    # 1. Build a bare scaffold
    scaffold = (
        "profile:\n"
        '  name: ""\n'
        '  version: ""\n'
        '  description: ""\n'
        "\n"
        "  documentTypes:\n"
        f"    - {doc_type}\n"
        "\n"
        "  elements:\n"
        "    akomaNtoso:\n"
    )

    # 2. Recursively expand the selected document type
    return expand_element(scaffold, doc_type, akn_schema)


@server.command("akn.generateSnippet")
def cmd_generate_snippet(doc_type: str = "act") -> str:
    """Generate a VS Code snippet scaffold for the given document type."""
    if akn_schema is None:
        return ""
    try:
        return generate_snippet(akn_schema, doc_type)
    except ValueError as exc:
        logger.error("Snippet generation failed: %s", exc)
        return ""


@server.command("akn.expandElement")
def cmd_expand_element(uri: str = "", elem_name: str = "") -> dict:
    """Cascade-add an element and its required children.

    Args:
        uri: document URI
        elem_name: element name to expand

    Returns a dict ``{"newText": "..."}`` with the full new YAML text.
    The client uses this for a diff preview.
    """
    if akn_schema is None:
        return {"newText": ""}
    if not uri or not elem_name:
        return {"newText": ""}

    doc = server.workspace.get_text_document(uri)
    new_text = expand_element(doc.source, elem_name, akn_schema)
    return {"newText": new_text}


@server.command("akn.collapseElement")
def cmd_collapse_element(uri: str = "", elem_name: str = "") -> dict:
    """Cascade-remove an element and orphaned descendants.

    Args:
        uri: document URI
        elem_name: element name to remove

    Returns a dict ``{"newText": "..."}`` with the full new YAML text.
    """
    if akn_schema is None:
        return {"newText": ""}
    if not uri or not elem_name:
        return {"newText": ""}

    doc = server.workspace.get_text_document(uri)
    new_text = collapse_element(doc.source, elem_name, akn_schema)
    return {"newText": new_text}
