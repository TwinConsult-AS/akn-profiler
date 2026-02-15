"""
YAML cursor-context resolver for AKN profile documents.

Analyses the raw YAML text and cursor position (line, column) to
determine where in the profile tree the user is editing.  This drives
contextual completions, hover info, and code-action suggestions.

The resolver works purely on indentation and key parsing — it does
**not** require a valid YAML parse.  This is intentional so that half-
written documents still get completions.

Public API
----------
``resolve_context(source, line, character) -> CursorContext``
"""

from __future__ import annotations

import dataclasses
import enum
import re


class Scope(enum.Enum):
    """Where in the profile tree the cursor currently is."""

    EMPTY = "empty"
    ROOT = "root"
    PROFILE = "profile"
    DOCUMENT_TYPES = "documentTypes"
    ELEMENTS = "elements"
    ELEMENT_NAME = "element_name"
    ELEMENT_BODY = "element_body"
    ATTRIBUTES = "attributes"
    ATTRIBUTE_NAME = "attribute_name"
    ATTRIBUTE_BODY = "attribute_body"
    ATTRIBUTE_VALUES = "attribute_values"
    CHILDREN = "children"
    CHOICE_BRANCHES = "choice_branches"
    STRUCTURE = "structure"


@dataclasses.dataclass
class CursorContext:
    """Result of cursor-context resolution."""

    scope: Scope
    """Current semantic scope."""

    element_name: str | None = None
    """The AKN element name being edited (when inside ``elements:``).

    ``None`` when the cursor is outside an element block.
    """

    attribute_name: str | None = None
    """The AKN attribute name being edited (when inside ``attributes:``).

    ``None`` when the cursor is outside an attribute block.
    """

    indent_level: int = 0
    """Number of leading spaces on the current line."""

    existing_keys: list[str] = dataclasses.field(default_factory=list)
    """Sibling keys already present at the same indent level.

    Used to exclude already-defined items from completions.
    """

    cross_block_keys: list[str] = dataclasses.field(default_factory=list)
    """Keys from a related sibling block that should also be excluded.

    When in ``CHILDREN`` scope, this contains keys under ``choice:``.
    When in ``CHOICE_BRANCHES`` scope, this contains keys under ``children:``
    (excluding ``choice`` itself).  This prevents the same element from
    being added in both places.
    """

    line_text: str = ""
    """The raw text of the line the cursor is on."""


# ------------------------------------------------------------------
# Key / indent helpers
# ------------------------------------------------------------------

_KEY_RE = re.compile(r"^(\s*)([A-Za-z_][\w-]*):")
_LIST_ITEM_RE = re.compile(r"^(\s*)-\s*(.*)")


def _indent(line: str) -> int:
    """Return the number of leading spaces."""
    return len(line) - len(line.lstrip(" "))


def _infer_blank_line_indent(lines: list[str], line: int) -> int:
    """Infer the logical indent of a blank line from its neighbours.

    When the cursor is on a blank line we look at the next non-blank
    line first (the indent the user is "about to continue at"), then
    fall back to the previous non-blank line.
    """
    # Look at next non-blank line
    for i in range(line + 1, len(lines)):
        if lines[i].strip():
            return _indent(lines[i])
    # Fall back to previous non-blank line
    for i in range(line - 1, -1, -1):
        if lines[i].strip():
            return _indent(lines[i])
    return 0


def _parse_key(line: str) -> tuple[int, str | None]:
    """Return (indent, key_name) or (indent, None) for non-key lines."""
    m = _KEY_RE.match(line)
    if m:
        return len(m.group(1)), m.group(2)
    return _indent(line), None


# ------------------------------------------------------------------
# Public resolver
# ------------------------------------------------------------------


def resolve_context(source: str, line: int, character: int) -> CursorContext:
    """Determine the cursor scope inside a ``.akn.yaml`` document.

    Parameters
    ----------
    source:
        Full document text.
    line:
        0-based line number.
    character:
        0-based column number.

    Returns
    -------
    A ``CursorContext`` with the resolved scope and related metadata.
    """
    lines = source.splitlines()

    if not lines or all(l.strip() == "" for l in lines):
        return CursorContext(scope=Scope.EMPTY)

    if line >= len(lines):
        line = len(lines) - 1

    current_line = lines[line] if line < len(lines) else ""
    cur_indent = _indent(current_line)

    # For truly empty lines (no content, no spaces), infer indent
    # from surrounding context.  Lines with only spaces keep their
    # measured indent — the user positioned the cursor intentionally.
    if current_line.strip() == "" and current_line == "":
        cur_indent = _infer_blank_line_indent(lines, line)

    # Walk backwards from the cursor line to build the scope chain.
    # We track the "key stack" — the sequence of mapping keys whose
    # blocks contain the cursor, ordered outermost → innermost.
    key_stack = _build_key_stack(lines, line)

    # Gather sibling keys at the same indent level around the cursor.
    existing_keys = _collect_sibling_keys(lines, line, cur_indent)

    # Determine scope from the key stack.
    scope, elem_name, attr_name = _scope_from_stack(key_stack, lines, line)

    # Gather keys from the related sibling block for cross-exclusion.
    cross_block_keys = _collect_cross_block_keys(lines, line, cur_indent, scope)

    return CursorContext(
        scope=scope,
        element_name=elem_name,
        attribute_name=attr_name,
        indent_level=cur_indent,
        existing_keys=existing_keys,
        cross_block_keys=cross_block_keys,
        line_text=current_line,
    )


# ------------------------------------------------------------------
# Internals
# ------------------------------------------------------------------


def _build_key_stack(lines: list[str], cursor_line: int) -> list[tuple[int, str]]:
    """Walk backwards from *cursor_line* and return the ancestor key stack.

    Returns a list of ``(indent, key_name)`` from outermost to innermost.
    """
    stack: list[tuple[int, str]] = []
    target_indent = _indent(lines[cursor_line]) if cursor_line < len(lines) else 0

    # For truly empty lines, use the inferred indent so parent lookup works correctly
    if cursor_line < len(lines) and lines[cursor_line] == "":
        target_indent = _infer_blank_line_indent(lines, cursor_line)

    # Also consider the current line's key as part of the stack
    cur_indent, cur_key = _parse_key(lines[cursor_line]) if cursor_line < len(lines) else (0, None)

    # Walk backwards to find parent keys
    max_indent = target_indent  # We're looking for keys with indent < max_indent
    for i in range(cursor_line - 1, -1, -1):
        indent_i, key_i = _parse_key(lines[i])
        if key_i is None:
            continue
        # A line is a parent if it has a strictly smaller indent than
        # anything we've already stacked (or the cursor line itself).
        if indent_i < max_indent:
            stack.append((indent_i, key_i))
            max_indent = indent_i
            if indent_i == 0:
                break

    stack.reverse()

    # If the cursor is on a key line, add it as the innermost entry.
    if cur_key is not None:
        stack.append((cur_indent, cur_key))

    return stack


def _collect_sibling_keys(lines: list[str], cursor_line: int, indent: int) -> list[str]:
    """Collect mapping keys at *indent* that are 'siblings' of the cursor line."""
    keys: list[str] = []

    # Find the parent indent (first line above cursor with indent < indent)
    parent_line = -1
    for i in range(cursor_line - 1, -1, -1):
        ind_i, key_i = _parse_key(lines[i])
        if key_i is not None and ind_i < indent:
            parent_line = i
            break

    # Scan forwards from the parent until we leave the block
    start = parent_line + 1 if parent_line >= 0 else 0
    for i in range(start, len(lines)):
        ind_i, key_i = _parse_key(lines[i])
        if key_i is not None:
            if ind_i == indent:
                keys.append(key_i)
            elif ind_i < indent and i > start:
                break  # left the block

    # Also collect list items if it's a list context
    for i in range(start, len(lines)):
        m = _LIST_ITEM_RE.match(lines[i])
        if m and len(m.group(1)) == indent:
            val = m.group(2).strip()
            # Strip inline YAML comments (e.g. "meta # required" → "meta")
            if "#" in val:
                val = val[: val.index("#")].strip()
            if val:
                keys.append(val)
        elif _indent(lines[i]) < indent and i > start and lines[i].strip():
            break

    return keys


def _collect_cross_block_keys(
    lines: list[str],
    cursor_line: int,
    cursor_indent: int,
    scope: Scope,
) -> list[str]:
    """Collect keys from a related sibling block for cross-exclusion.

    * **CHILDREN** scope → collect keys nested under ``choice:`` (one
      indent level deeper than the cursor).
    * **CHOICE_BRANCHES** scope → collect keys under ``children:`` at the
      same level as ``choice:`` itself (i.e. the cursor indent minus 2),
      excluding ``choice``.

    Returns an empty list for all other scopes.
    """
    if scope == Scope.CHILDREN:
        # Find the "choice:" key among our siblings; collect ITS children.
        # "choice:" is at cursor_indent; its children are at cursor_indent+2.
        for i in range(cursor_line - 1, -1, -1):
            ind_i, key_i = _parse_key(lines[i])
            if key_i is not None and ind_i < cursor_indent:
                break  # reached parent — start of our sibling block
        # parent_line found; now scan forward for "choice:"
        # But simpler: just scan all lines around cursor for "choice:" at cursor_indent
        choice_line = -1
        # Walk backwards to find the parent ("children:") line
        parent_start = 0
        for i in range(cursor_line, -1, -1):
            ind_i, key_i = _parse_key(lines[i])
            if key_i is not None and ind_i < cursor_indent:
                parent_start = i + 1
                break
        # Scan forward from parent to find choice: and the block end
        for i in range(parent_start, len(lines)):
            ind_i, key_i = _parse_key(lines[i])
            if key_i is not None and ind_i < cursor_indent and i > parent_start:
                break
            if key_i == "choice" and ind_i == cursor_indent:
                choice_line = i
                break
        if choice_line < 0:
            return []
        # Collect keys under choice: at cursor_indent + 2
        child_indent = cursor_indent + 2
        keys: list[str] = []
        for i in range(choice_line + 1, len(lines)):
            ind_i, key_i = _parse_key(lines[i])
            if key_i is not None:
                if ind_i == child_indent:
                    keys.append(key_i)
                elif ind_i <= cursor_indent:
                    break
        return keys

    if scope == Scope.CHOICE_BRANCHES:
        # Cursor is inside choice: — collect sibling keys from "children:"
        # that are at the same indent as "choice:" itself (cursor_indent - 2).
        children_indent = cursor_indent - 2
        if children_indent < 0:
            return []
        # Walk backwards to find "children:" line
        children_line = -1
        for i in range(cursor_line, -1, -1):
            ind_i, key_i = _parse_key(lines[i])
            if key_i == "children" and ind_i < cursor_indent:
                children_line = i
                break
            if key_i is not None and ind_i < children_indent:
                break  # passed the parent element, no children: found
        if children_line < 0:
            return []
        # Collect keys at children_indent + 2 under children:, excluding "choice"
        sibling_indent = children_indent + 2
        keys = []
        for i in range(children_line + 1, len(lines)):
            ind_i, key_i = _parse_key(lines[i])
            if key_i is not None:
                if ind_i == sibling_indent and key_i != "choice":
                    keys.append(key_i)
                elif ind_i <= children_indent:
                    break
        return keys

    return []


def _scope_from_stack(
    key_stack: list[tuple[int, str]],
    lines: list[str],
    cursor_line: int,
) -> tuple[Scope, str | None, str | None]:
    """Derive the ``Scope``, element name, and attribute name from the key stack."""
    names = [k for _, k in key_stack]

    if not names:
        return Scope.ROOT, None, None

    # Check if the current line is a list item
    is_list_item = False
    if cursor_line < len(lines):
        is_list_item = bool(_LIST_ITEM_RE.match(lines[cursor_line]))

    # The innermost key determines primary scope
    # Walk through the names to build context
    elem_name: str | None = None
    attr_name: str | None = None

    # Pattern matching on the key stack
    # profile → PROFILE
    # profile.name/version/description → PROFILE (value position)
    # profile.documentTypes → DOCUMENT_TYPES
    # profile.elements → ELEMENTS
    # profile.elements.<name> → ELEMENT_NAME / ELEMENT_BODY
    # profile.elements.<name>.attributes → ATTRIBUTES
    # profile.elements.<name>.attributes.<attr> → ATTRIBUTE_NAME / ATTRIBUTE_BODY
    # profile.elements.<name>.attributes.<attr>.values → ATTRIBUTE_VALUES
    # profile.elements.<name>.children → CHILDREN
    # profile.elements.<name>.structure → STRUCTURE
    # profile.metadata → METADATA
    # profile.metadata.<name> → METADATA_NAME / METADATA_BODY

    depth = len(names)

    if depth == 1:
        if names[0] == "profile":
            return Scope.PROFILE, None, None
        return Scope.ROOT, None, None

    if names[0] != "profile":
        return Scope.ROOT, None, None

    # depth >= 2 and names[0] == "profile"
    section = names[1]

    if section == "documentTypes":
        return Scope.DOCUMENT_TYPES, None, None

    if section == "elements":
        if depth == 2:
            # Cursor is on the "elements:" key itself or directly below it
            # needing an element name
            return Scope.ELEMENTS, None, None
        # depth >= 3 → names[2] is an element name
        elem_name = names[2]
        if depth == 3:
            # Could be on the element key or inside its body
            # If we're on the key itself, it's ELEMENT_NAME context
            cur_indent, cur_key = (
                _parse_key(lines[cursor_line]) if cursor_line < len(lines) else (0, None)
            )
            if cur_key == elem_name:
                return Scope.ELEMENT_NAME, elem_name, None
            return Scope.ELEMENT_BODY, elem_name, None
        # depth >= 4
        subsection = names[3]
        if subsection == "attributes":
            if depth == 4:
                return Scope.ATTRIBUTES, elem_name, None
            # depth >= 5 → names[4] is an attribute name
            attr_name = names[4]
            if depth == 5:
                cur_indent, cur_key = (
                    _parse_key(lines[cursor_line]) if cursor_line < len(lines) else (0, None)
                )
                if cur_key == attr_name:
                    return Scope.ATTRIBUTE_NAME, elem_name, attr_name
                return Scope.ATTRIBUTE_BODY, elem_name, attr_name
            # depth >= 6
            if names[5] == "values":
                return Scope.ATTRIBUTE_VALUES, elem_name, attr_name
            return Scope.ATTRIBUTE_BODY, elem_name, attr_name
        if subsection == "children":
            if depth >= 5 and names[4] == "choice":
                return Scope.CHOICE_BRANCHES, elem_name, None
            return Scope.CHILDREN, elem_name, None
        if subsection == "structure":
            return Scope.STRUCTURE, elem_name, None
        if subsection in ("required",):
            return Scope.ELEMENT_BODY, elem_name, None
        return Scope.ELEMENT_BODY, elem_name, None

    # profile-level keys: name, version, description
    if section in ("name", "version", "description"):
        return Scope.PROFILE, None, None

    return Scope.PROFILE, None, None
