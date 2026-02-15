"""
AKN Profiler — Cascade Operations

Provides recursive add/remove of elements through the required-child
chain.  Both ``expand_element`` and ``collapse_element`` return a new
YAML string representing the modified profile — they do **not** mutate
in-place.  The caller (server command / diff preview) compares old vs.
new text.

Public API
----------
``expand_element(yaml_text, element_name, schema) -> str``
    Recursively add *element_name* and all its required children,
    attributes, and metadata to the profile YAML.

``collapse_element(yaml_text, element_name, schema) -> str``
    Remove *element_name* and any children that become orphaned
    (not referenced by any remaining element) from the profile.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from akn_profiler.xsd.schema_loader import AknSchema

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Custom YAML dumper — ``None`` → blank (``key:``) not ``key: null``
# ------------------------------------------------------------------


class _ProfileDumper(yaml.SafeDumper):
    """YAML dumper that writes ``None`` as blank instead of ``null``."""


def _none_representer(dumper: yaml.Dumper, _data: object) -> yaml.Node:
    return dumper.represent_scalar("tag:yaml.org,2002:null", "")


_ProfileDumper.add_representer(type(None), _none_representer)


# ------------------------------------------------------------------
# Expand (cascade add)
# ------------------------------------------------------------------


def expand_element(
    yaml_text: str,
    element_name: str,
    schema: AknSchema,
) -> str:
    """Add *element_name* and its full required-child chain to the profile.

    Returns the modified YAML text.  If the element already exists it
    is left untouched but its required children are still ensured.
    """
    raw = yaml.safe_load(yaml_text)
    if not isinstance(raw, dict) or "profile" not in raw:
        return yaml_text

    profile = raw["profile"]
    if not isinstance(profile, dict):
        return yaml_text

    elements = profile.get("elements")
    if not isinstance(elements, dict):
        elements = {}
        profile["elements"] = elements

    _recursive_add(schema, element_name, elements, visited=set())

    # Ensure akomaNtoso is present as root with document-type children,
    # and appears first in the elements dict.
    _ensure_akomantoso_root(profile, elements, schema)

    return _dump(raw)


def _recursive_add(
    schema: AknSchema,
    elem_name: str,
    elements: dict,
    visited: set[str],
) -> None:
    """Recursively ensure *elem_name* and its required chain exist."""
    if elem_name in visited:
        return
    visited.add(elem_name)

    info = schema.get_element_info(elem_name)
    if info is None:
        return

    # Ensure element entry exists
    if elem_name not in elements:
        entry: dict = {}
        # Add required attributes
        req_attrs = [a for a in info.attributes if a.required]
        if req_attrs:
            entry["attributes"] = {}
            for attr in req_attrs:
                attr_entry: dict = {"required": True}
                if attr.enum_values:
                    attr_entry["values"] = list(attr.enum_values)
                entry["attributes"][attr.name] = attr_entry

        # Add required children as dict with cardinality
        req_children = [c for c in info.children if c.required]
        # Build exclusive choice branches if element has exclusive groups
        choice_groups = schema.get_choice_groups(elem_name)
        exclusive_cg = None
        for cg in choice_groups:
            if cg.exclusive:
                exclusive_cg = cg
                break

        if req_children or exclusive_cg:
            child_dict: dict = {}
            exclusive_members = exclusive_cg.all_elements if exclusive_cg else frozenset()
            for c in req_children:
                if c.name not in exclusive_members:
                    child_dict[c.name] = c.cardinality
            if exclusive_cg:
                choice_dict: dict[str, str | None] = {}
                for branch in exclusive_cg.branches:
                    for c in info.children:
                        if c.name in branch.elements and c.required:
                            choice_dict[c.name] = c.cardinality
                if choice_dict:
                    child_dict["choice"] = choice_dict
            if child_dict:
                entry["children"] = child_dict

        elements[elem_name] = entry if entry else None

    else:
        # Element exists — ensure required children and attrs are present
        existing = elements[elem_name]
        req_children = [c for c in info.children if c.required]
        req_attrs = [a for a in info.attributes if a.required]

        # Only promote None → dict when there's something to add
        if existing is None and (req_children or req_attrs):
            existing = {}
            elements[elem_name] = existing

        if isinstance(existing, dict):
            # Ensure required attributes
            if req_attrs:
                attrs_dict = existing.setdefault("attributes", {})
                for attr in req_attrs:
                    if attr.name not in attrs_dict:
                        attr_entry: dict = {"required": True}
                        if attr.enum_values:
                            attr_entry["values"] = list(attr.enum_values)
                        attrs_dict[attr.name] = attr_entry

            # Ensure required children (dict format)
            if req_children:
                child_dict = existing.get("children", {})
                if child_dict is None:
                    child_dict = {}
                if not isinstance(child_dict, dict):
                    child_dict = {}
                for c in req_children:
                    if c.name not in child_dict:
                        child_dict[c.name] = c.cardinality
                if child_dict:
                    existing["children"] = child_dict

    # Recurse into required children
    if info:
        for child in info.children:
            if child.required:
                _recursive_add(schema, child.name, elements, visited)


def _ensure_akomantoso_root(
    profile: dict,
    elements: dict,
    schema: AknSchema,
) -> None:
    """Ensure ``akomaNtoso`` exists with document-type children and is
    listed first in the elements dict.

    ``akomaNtoso`` is the root element — every document type declared
    in ``documentTypes`` should appear as a child, and the entry should
    sit at the top of the ``elements`` section for readability.
    """
    doc_types: list[str] = profile.get("documentTypes", []) or []
    # Only keep document types that actually have element definitions
    present_doc_types = [dt for dt in doc_types if dt in elements]

    # Build / update akomaNtoso entry
    akn_entry = elements.get("akomaNtoso")
    if akn_entry is None:
        akn_entry = {}
    if not isinstance(akn_entry, dict):
        akn_entry = {}

    if present_doc_types:
        children = akn_entry.get("children", {}) or {}
        if not isinstance(children, dict):
            children = {}
        for dt in present_doc_types:
            if dt not in children:
                children[dt] = "1..1"
        if children:
            akn_entry["children"] = children

    elements["akomaNtoso"] = akn_entry or None

    # Move akomaNtoso to the front
    if "akomaNtoso" in elements:
        reordered = {"akomaNtoso": elements.pop("akomaNtoso")}
        reordered.update(elements)
        elements.clear()
        elements.update(reordered)


# ------------------------------------------------------------------
# Collapse (cascade remove)
# ------------------------------------------------------------------


def collapse_element(
    yaml_text: str,
    element_name: str,
    schema: AknSchema,
) -> str:
    """Remove *element_name* and orphaned descendants from the profile.

    An element is orphaned if no other element in the profile lists it
    as a child.

    Returns the modified YAML text.
    """
    raw = yaml.safe_load(yaml_text)
    if not isinstance(raw, dict) or "profile" not in raw:
        return yaml_text

    profile = raw["profile"]
    if not isinstance(profile, dict):
        return yaml_text

    elements: dict = profile.get("elements", {})
    if not isinstance(elements, dict):
        return yaml_text

    # Collect the element and all its descendants
    to_remove = _collect_descendants(element_name, elements, schema)

    # Remove references from other elements' children dicts
    for e_name, e_data in list(elements.items()):
        if not isinstance(e_data, dict):
            continue
        child_dict = e_data.get("children")
        if isinstance(child_dict, dict):
            e_data["children"] = {
                k: v for k, v in child_dict.items() if k not in to_remove or k == "choice"
            }
            if not e_data["children"]:
                del e_data["children"]

    # Remove the elements themselves
    for name in to_remove:
        elements.pop(name, None)

    return _dump(raw)


def _collect_descendants(
    elem_name: str,
    elements: dict,
    schema: AknSchema,
) -> set[str]:
    """Collect *elem_name* and all descendants that would become orphaned."""
    to_remove: set[str] = {elem_name}
    _walk_orphans(elem_name, elements, schema, to_remove)
    return to_remove


def _walk_orphans(
    elem_name: str,
    elements: dict,
    schema: AknSchema,
    to_remove: set[str],
) -> None:
    """Recursively find orphaned children."""
    entry = elements.get(elem_name)
    if not isinstance(entry, dict):
        return

    children = entry.get("children", {})
    if not isinstance(children, dict):
        return

    for child_name in children:
        if child_name in to_remove:
            continue
        # Skip meta-keys that are not child element references
        if child_name == "choice":
            continue
        # Check if any other element (not being removed) also references this child
        is_orphan = True
        for other_name, other_data in elements.items():
            if other_name in to_remove:
                continue
            if not isinstance(other_data, dict):
                continue
            other_children = other_data.get("children", {})
            if isinstance(other_children, dict) and child_name in other_children:
                is_orphan = False
                break

        if is_orphan and child_name in elements:
            to_remove.add(child_name)
            _walk_orphans(child_name, elements, schema, to_remove)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _dump(data: dict) -> str:
    """Dump the modified profile back to YAML with readable blank lines."""
    raw = yaml.dump(
        data,
        Dumper=_ProfileDumper,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=120,
    )
    return _insert_blank_lines(raw)


def _insert_blank_lines(text: str) -> str:
    """Insert blank lines between profile sections and element entries.

    Rules:
    - Blank line before ``documentTypes:`` and ``elements:`` (the major
      profile sections at 2-space indent).
    - Blank line before each element entry (4-space indent key inside
      the ``elements:`` block).
    """
    _SECTION_KEYS = {"documentTypes:", "elements:"}
    lines = text.splitlines(True)  # keep newlines
    out: list[str] = []
    in_elements = False

    for i, line in enumerate(lines):
        stripped = line.rstrip("\n")

        # Detect entering the elements section
        if stripped == "  elements:":
            in_elements = True
        elif (
            stripped
            and not stripped.startswith(" ")
            or in_elements
            and stripped
            and not stripped.startswith("  ")
        ):
            in_elements = False

        # Blank line before major profile sections (documentTypes, elements)
        if i > 0 and stripped.startswith("  ") and not stripped.startswith("   "):
            key_part = stripped.strip().split(":")[0] + ":"
            if key_part in _SECTION_KEYS:
                prev = out[-1].rstrip("\n") if out else ""
                if prev:
                    out.append("\n")

        # Blank line before each element entry (4-space indent keys under elements)
        if in_elements and i > 0 and len(stripped) > 4:
            if stripped.startswith("    ") and not stripped.startswith("     "):
                key_part = stripped.lstrip()
                if key_part.endswith(":") or ": " in key_part:
                    prev = out[-1].rstrip("\n") if out else ""
                    if prev and prev != "  elements:":
                        out.append("\n")

        out.append(line)

    return "".join(out)
