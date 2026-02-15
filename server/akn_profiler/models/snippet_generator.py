"""
AKN Profiler — VS Code Snippet Scaffold Generator

Produces a VS Code snippet body (with ``$1``, ``$2``, … tab-stop
placeholders) for a minimum viable ``.akn.yaml`` profile.

The scaffold is intentionally **minimal** — field values are empty
placeholders that the user tabs through.  Further detail (elements,
metadata, etc.) is added via LSP completions.

Public API
----------
``generate_snippet(schema, doc_type) -> str``
``get_document_types(schema) -> list[str]``
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from akn_profiler.xsd.schema_loader import AknSchema


def get_document_types(schema: AknSchema) -> list[str]:
    """Return the list of valid AKN document types."""
    return schema.get_children("akomaNtoso")


def generate_snippet(schema: AknSchema, doc_type: str) -> str:
    """Generate a VS Code snippet body for a profile scaffold.

    The returned string uses VS Code snippet syntax (``$1``, ``$2``,
    ``${N:placeholder}``, ``$0`` for the final cursor).

    Parameters
    ----------
    schema:
        The loaded AKN schema.
    doc_type:
        The document type to pre-fill (e.g. ``"act"``).

    Returns
    -------
    A string with VS Code snippet tab stops.
    """
    # Build list of valid doc types for the choice placeholder
    valid_types = get_document_types(schema)

    if doc_type not in valid_types:
        raise ValueError(f"'{doc_type}' is not a valid AKN document type. Valid: {valid_types}")

    # Minimal scaffold — the cascade system (diagnostics + quick-fixes)
    # will guide the user to expand elements after the scaffold is
    # inserted.  This keeps the snippet small and the flow progressive:
    #
    #   1. Snippet inserts metadata + document type + akomaNtoso
    #   2. Diagnostic fires: "'act' has no element definition"
    #   3. Quick-fix: "Define 'act' with required attributes and children"
    #   4. One click → full cascade fills in all required elements
    lines = [
        "profile:",
        '  name: "${1:Profile Name}"',
        '  version: "${2:1.0}"',
        '  description: "${3:Description of this application profile}"',
        "",
        "  documentTypes:",
        f"    - {doc_type}",
        "",
        "  elements:",
        "    akomaNtoso:",
        "$0",
    ]

    return "\n".join(lines)
