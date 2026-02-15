"""
AKN Profiler — Minimum Viable Profile Generator

Walks the XSD (via ``AknSchema``) and produces a profile that contains
exactly the **required** elements, attributes, and metadata according
to the Akoma Ntoso 3.0 schema.

The generated profile is guaranteed to pass validation with zero errors
— it is the XSD-derived "ground truth" baseline.

Public API::

    from akn_profiler.models.generator import generate_profile, generate_yaml

    # As a Pydantic model
    profile = generate_profile(schema, doc_type="act")

    # As a YAML string ready to write to disk
    yaml_text = generate_yaml(schema, doc_type="act")
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from akn_profiler.models.profile import (
    AttributeRestriction,
    ElementRestriction,
    ProfileDocument,
)

if TYPE_CHECKING:
    from akn_profiler.xsd.schema_loader import AknSchema, AttrInfo

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------


def generate_profile(
    schema: AknSchema,
    doc_type: str = "act",
    *,
    include_optional_children: bool = False,
    include_optional_attributes: bool = False,
) -> ProfileDocument:
    """Generate a minimum viable ``ProfileDocument`` from the XSD.

    Parameters
    ----------
    schema:
        The loaded AKN schema.
    doc_type:
        The document type to generate for (must be a child of
        ``<akomaNtoso>``).
    include_optional_children:
        If ``True``, list *all* allowed children (not just required
        ones) in each element restriction.  Useful for seeing what
        is available.
    include_optional_attributes:
        If ``True``, include optional attributes (marked as not
        required) in element restrictions.

    Returns
    -------
    A ``ProfileDocument`` that will pass validation with zero errors.
    """
    valid_doc_types = schema.get_children("akomaNtoso")
    if doc_type not in valid_doc_types:
        raise ValueError(f"'{doc_type}' is not a valid AKN document type. Valid: {valid_doc_types}")

    elements: dict[str, ElementRestriction] = {}

    # Recursively walk the required-child tree starting from the doc type
    _walk_required_tree(
        schema,
        elem_name=doc_type,
        elements=elements,
        include_optional_children=include_optional_children,
        include_optional_attributes=include_optional_attributes,
        visited=set(),
    )

    # Also include <akomaNtoso> itself (the root)
    _add_element(
        schema,
        "akomaNtoso",
        elements,
        include_optional_children=include_optional_children,
        include_optional_attributes=include_optional_attributes,
    )

    return ProfileDocument(
        name=f"Minimum viable profile ({doc_type})",
        version="1.0",
        description=(f"Minimum viable application profile for the {doc_type} document type."),
        documentTypes=[doc_type],
        elements=elements,
    )


def generate_yaml(
    schema: AknSchema,
    doc_type: str = "act",
    *,
    include_optional_children: bool = False,
    include_optional_attributes: bool = False,
    comments: bool = True,
) -> str:
    """Generate a YAML string for a minimum viable profile.

    Parameters are the same as ``generate_profile`` plus:

    comments:
        If ``True``, add inline ``# comments`` with XSD context
        (attribute type, enum values, whether optional).
    """
    profile = generate_profile(
        schema,
        doc_type,
        include_optional_children=include_optional_children,
        include_optional_attributes=include_optional_attributes,
    )

    if comments:
        return _to_commented_yaml(profile, schema)
    else:
        return _to_plain_yaml(profile)


# ------------------------------------------------------------------
# Recursive XSD walker
# ------------------------------------------------------------------


def _walk_required_tree(
    schema: AknSchema,
    elem_name: str,
    elements: dict[str, ElementRestriction],
    *,
    include_optional_children: bool,
    include_optional_attributes: bool,
    visited: set[str],
) -> None:
    """Recursively walk the required-child chain of *elem_name*.

    For each element encountered, create an ``ElementRestriction`` and
    recurse into its required children.
    """
    if elem_name in visited:
        return
    visited.add(elem_name)

    info = schema.get_element_info(elem_name)
    if info is None:
        return

    _add_element(
        schema,
        elem_name,
        elements,
        include_optional_children=include_optional_children,
        include_optional_attributes=include_optional_attributes,
    )

    # Recurse into required children
    for child in schema.get_required_children(elem_name):
        _walk_required_tree(
            schema,
            child.name,
            elements,
            include_optional_children=include_optional_children,
            include_optional_attributes=include_optional_attributes,
            visited=visited,
        )


def _add_element(
    schema: AknSchema,
    elem_name: str,
    elements: dict[str, ElementRestriction],
    *,
    include_optional_children: bool,
    include_optional_attributes: bool,
) -> None:
    """Add an ``ElementRestriction`` for *elem_name*."""
    info = schema.get_element_info(elem_name)
    if info is None:
        return

    # Attributes
    attrs: dict[str, AttributeRestriction] = {}
    for a in info.attributes:
        if a.required or include_optional_attributes:
            restriction = AttributeRestriction(required=a.required)
            # Include enum values so the profile documents what's allowed
            if a.enum_values:
                restriction = AttributeRestriction(
                    required=a.required,
                    values=list(a.enum_values),
                )
            attrs[a.name] = restriction

    # Children — dict mapping child name → cardinality string
    children: dict[str, str | None] = {}
    if include_optional_children:
        children = {c.name: c.cardinality for c in info.children}
    else:
        children = {c.name: c.cardinality for c in info.children if c.required}

    elements[elem_name] = ElementRestriction(
        attributes=attrs,
        children=children,
    )


# ------------------------------------------------------------------
# YAML serialisation
# ------------------------------------------------------------------


def _to_plain_yaml(profile: ProfileDocument) -> str:
    """Serialise to clean, human-readable YAML without comments."""
    lines: list[str] = []
    lines.append("profile:")
    lines.append(f'  name: "{profile.name}"')
    lines.append(f'  version: "{profile.version}"')
    if profile.description:
        lines.append(f'  description: "{profile.description}"')
    lines.append("")

    if profile.documentTypes:
        lines.append("  documentTypes:")
        for dt in profile.documentTypes:
            lines.append(f"    - {dt}")
        lines.append("")

    if profile.elements:
        lines.append("  elements:")
        for elem_name, restriction in profile.elements.items():
            has_content = restriction.attributes or restriction.children or restriction.structure
            if has_content:
                lines.append(f"    {elem_name}:")
            else:
                lines.append(f"    {elem_name}:")

            if restriction.attributes:
                lines.append("      attributes:")
                for attr_name, attr_r in restriction.attributes.items():
                    lines.append(f"        {attr_name}:")
                    lines.append(f"          required: {'true' if attr_r.required else 'false'}")
                    if attr_r.values:
                        lines.append("          values:")
                        for v in attr_r.values:
                            lines.append(f"            - {v}")

            if restriction.children:
                lines.append("      children:")
                for child_name, cardinality in restriction.children.items():
                    if cardinality:
                        lines.append(f'        {child_name}: "{cardinality}"')
                    else:
                        lines.append(f"        {child_name}:")

            if restriction.structure:
                lines.append("      structure:")
                for s in restriction.structure:
                    lines.append(f"        - {s}")

            lines.append("")

    return "\n".join(lines) + "\n"


def _to_commented_yaml(profile: ProfileDocument, schema: AknSchema) -> str:
    """Serialise to YAML with XSD-derived comments.

    We build the YAML string manually so we can inject ``# comments``
    that plain ``yaml.dump`` cannot produce.
    """
    lines: list[str] = []
    lines.append("# Auto-generated AKN Application Profile")
    lines.append(
        f"# Document type: {profile.documentTypes[0] if profile.documentTypes else 'generic'}"
    )
    lines.append("# Generated from Akoma Ntoso 3.0 XSD")
    lines.append("")
    lines.append("profile:")
    lines.append(f'  name: "{profile.name}"')
    lines.append(f'  version: "{profile.version}"')
    lines.append(f'  description: "{profile.description}"')
    lines.append("")

    # Document types
    if profile.documentTypes:
        valid_doc_types = schema.get_children("akomaNtoso")
        lines.append(f"  # Valid document types: {', '.join(valid_doc_types)}")
        lines.append("  documentTypes:")
        for dt in profile.documentTypes:
            lines.append(f"    - {dt}")
        lines.append("")

    # Elements
    if profile.elements:
        lines.append("  # Element restrictions (derived from XSD required-child chains)")
        lines.append("  elements:")
        for elem_name, restriction in profile.elements.items():
            info = schema.get_element_info(elem_name)
            doc = info.doc if info else ""
            if doc:
                # Truncate long docs
                doc = doc[:100] + "..." if len(doc) > 100 else doc
                lines.append(f"    # {doc}")
            lines.append(f"    {elem_name}:")

            # Attributes
            if restriction.attributes:
                lines.append("      attributes:")
                for attr_name, attr_r in restriction.attributes.items():
                    attr_info = _find_attr(schema, elem_name, attr_name)
                    comment = ""
                    if attr_info:
                        parts = []
                        if attr_info.required:
                            parts.append("XSD-required")
                        else:
                            parts.append("optional in XSD")
                        if attr_info.pattern:
                            parts.append(f"pattern: {attr_info.pattern}")
                        if attr_info.type_hint:
                            parts.append(f"type: {attr_info.type_hint}")
                        comment = f"  # {', '.join(parts)}"
                    lines.append(f"        {attr_name}:{comment}")
                    if attr_r.required:
                        lines.append("          required: true")
                    if attr_r.values:
                        vals = ", ".join(f'"{v}"' for v in attr_r.values)
                        lines.append(f"          values: [{vals}]")

            # Children
            if restriction.children:
                all_children = schema.get_children(elem_name) if info else []
                req_names = {c.name for c in schema.get_required_children(elem_name)}
                optional_names = [n for n in all_children if n not in req_names]
                if optional_names:
                    lines.append(
                        f"      # Also available: {', '.join(optional_names[:15])}"
                        + ("..." if len(optional_names) > 15 else "")
                    )
                lines.append("      children:")
                for child_name, cardinality in restriction.children.items():
                    tag = " # required" if child_name in req_names else ""
                    if cardinality:
                        lines.append(f'        {child_name}: "{cardinality}"{tag}')
                    else:
                        lines.append(f"        {child_name}:{tag}")

            lines.append("")

    return "\n".join(lines) + "\n"


def _find_attr(schema: AknSchema, elem_name: str, attr_name: str) -> AttrInfo | None:
    """Look up an ``AttrInfo`` by element and attribute name."""
    for a in schema.get_attributes(elem_name):
        if a.name == attr_name:
            return a
    return None
