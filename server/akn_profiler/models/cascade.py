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

``compute_element_order(elements, schema) -> list[str]``
    Compute a canonical ordering for profile element definitions:
    parents before children, alphabetical tiebreaking.

``reorder_profile(yaml_text, schema) -> str``
    Reorder the entire profile — elements, children, and attributes —
    into canonical XSD-aware order.
"""

from __future__ import annotations

import logging
from collections import defaultdict
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
    *,
    auto_add_eid: bool = False,
    auto_add_wid: bool = False,
    auto_add_guid: bool = False,
    auto_id_required: bool = True,
) -> str:
    """Add *element_name* and its full required-child chain to the profile.

    Returns the modified YAML text.  If the element already exists it
    is left untouched but its required children are still ensured.

    When *auto_add_eid*, *auto_add_wid*, or *auto_add_guid* are set,
    the corresponding identity attributes are automatically included on
    elements that support them.  *auto_id_required* controls whether
    the auto-added identity attributes are marked ``required: true``
    or ``required: false``.
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

    auto_id_attrs = _build_auto_id_list(auto_add_eid, auto_add_wid, auto_add_guid)
    _recursive_add(
        schema,
        element_name,
        elements,
        visited=set(),
        auto_id_attrs=auto_id_attrs,
        auto_id_required=auto_id_required,
    )

    # Ensure akomaNtoso is present as root with document-type children,
    # and appears first in the elements dict.
    _ensure_akomantoso_root(profile, elements, schema)

    # Reorder elements into canonical order (parents before children)
    _apply_element_order(elements, schema)

    return _dump(raw)


def _build_auto_id_list(eid: bool, wid: bool, guid: bool) -> list[str]:
    """Build a list of identity attribute names to auto-add."""
    attrs: list[str] = []
    if eid:
        attrs.append("eId")
    if wid:
        attrs.append("wId")
    if guid:
        attrs.append("GUID")
    return attrs


def _recursive_add(
    schema: AknSchema,
    elem_name: str,
    elements: dict,
    visited: set[str],
    *,
    auto_id_attrs: list[str] | None = None,
    auto_id_required: bool = True,
) -> None:
    """Recursively ensure *elem_name* and its required chain exist."""
    if elem_name in visited:
        return
    visited.add(elem_name)

    info = schema.get_element_info(elem_name)
    if info is None:
        return

    # Build the set of identity attributes to auto-add for this element
    _id_attrs_for_elem: list[str] = []
    if auto_id_attrs:
        supported = {a.name for a in info.attributes}
        _id_attrs_for_elem = [a for a in auto_id_attrs if a in supported]

    # Ensure element entry exists
    if elem_name not in elements:
        entry: dict = {}
        # Add required attributes + auto-add identity attributes
        req_attrs = [a for a in info.attributes if a.required]
        all_attrs_to_add = list(req_attrs)
        # Add identity attrs that are not already required
        req_names = {a.name for a in req_attrs}
        for id_name in _id_attrs_for_elem:
            if id_name not in req_names:
                id_attr = next((a for a in info.attributes if a.name == id_name), None)
                if id_attr:
                    all_attrs_to_add.append(id_attr)

        if all_attrs_to_add:
            entry["attributes"] = {}
            for attr in all_attrs_to_add:
                # Identity attrs use auto_id_required; others use XSD required
                is_id = attr.name in ("eId", "wId", "GUID")
                req_val = (
                    auto_id_required
                    if (is_id and attr.name in _id_attrs_for_elem)
                    else attr.required
                )
                attr_entry: dict = {"required": req_val}
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
        if existing is None and (req_children or req_attrs or _id_attrs_for_elem):
            existing = {}
            elements[elem_name] = existing

        if isinstance(existing, dict):
            # Ensure required attributes
            if req_attrs or _id_attrs_for_elem:
                attrs_dict = existing.setdefault("attributes", {})
                for attr in req_attrs:
                    if attr.name not in attrs_dict:
                        attr_entry: dict = {"required": True}
                        if attr.enum_values:
                            attr_entry["values"] = list(attr.enum_values)
                        attrs_dict[attr.name] = attr_entry
                # Auto-add identity attributes
                for id_name in _id_attrs_for_elem:
                    if id_name not in attrs_dict:
                        id_attr = next((a for a in info.attributes if a.name == id_name), None)
                        if id_attr:
                            attrs_dict[id_name] = {"required": auto_id_required}

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
                _recursive_add(
                    schema,
                    child.name,
                    elements,
                    visited,
                    auto_id_attrs=auto_id_attrs,
                    auto_id_required=auto_id_required,
                )


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
# Element ordering
# ------------------------------------------------------------------


def compute_element_order(elements: dict, schema: AknSchema) -> list[str]:
    """Compute a canonical ordering for profile element keys.

    Ordering principles:
    1. ``akomaNtoso`` is always first.
    2. Parents appear before their children — an element is placed after
       the **last** parent that references it, so siblings with a shared
       child appear together followed by the child.
    3. Ties are broken alphabetically.
    4. Elements with no parent references (orphans) go at the end,
       alphabetically.

    Only relationships *within the profile* are considered — the full
    XSD hierarchy is not imposed.
    """
    if not elements:
        return []

    elem_set = set(elements)

    # Build an in-profile parent→children graph.  A child is anything
    # referenced in an element's children: or choice: section.
    children_of: dict[str, list[str]] = defaultdict(list)
    parents_of: dict[str, list[str]] = defaultdict(list)
    for ename, edata in elements.items():
        if not isinstance(edata, dict):
            continue
        child_dict = edata.get("children")
        if isinstance(child_dict, dict):
            for cname in child_dict:
                if cname == "choice":
                    choice_dict = child_dict.get("choice")
                    if isinstance(choice_dict, dict):
                        for branch_name in choice_dict:
                            if branch_name in elem_set:
                                children_of[ename].append(branch_name)
                                parents_of[branch_name].append(ename)
                elif cname in elem_set:
                    children_of[ename].append(cname)
                    parents_of[cname].append(ename)

    # Topological sort via Kahn's algorithm.  For each element we
    # track in-degree (number of unprocessed parents in the profile).
    in_degree: dict[str, int] = {e: 0 for e in elem_set}
    for ename in elem_set:
        in_degree[ename] = len(parents_of.get(ename, []))

    # Roots: elements with no parents in the profile.
    # Sort initially so alphabetical tiebreaking is deterministic.
    ready = sorted([e for e in elem_set if in_degree[e] == 0])
    # Ensure akomaNtoso is always first
    if "akomaNtoso" in ready:
        ready.remove("akomaNtoso")
        ready.insert(0, "akomaNtoso")

    ordered: list[str] = []
    while ready:
        # Pop the first ready element (alphabetical among peers)
        current = ready.pop(0)
        ordered.append(current)
        # Decrement in-degree for children
        for child in sorted(children_of.get(current, [])):
            in_degree[child] -= 1
            if in_degree[child] == 0:
                # Insert in sorted position among other ready items
                _insert_sorted(ready, child)

    # Any remaining elements (cycles or disconnected) appended
    # alphabetically.
    remaining = sorted(e for e in elem_set if e not in set(ordered))
    ordered.extend(remaining)

    return ordered


def _insert_sorted(lst: list[str], item: str) -> None:
    """Insert *item* into *lst* maintaining alphabetical order."""
    for i, v in enumerate(lst):
        if item < v:
            lst.insert(i, item)
            return
    lst.append(item)


def _apply_element_order(elements: dict, schema: AknSchema) -> None:
    """Reorder *elements* dict in-place to canonical order."""
    order = compute_element_order(elements, schema)
    reordered = {name: elements[name] for name in order if name in elements}
    elements.clear()
    elements.update(reordered)


def reorder_children(children: dict, element_name: str, schema: AknSchema) -> dict:
    """Reorder a children dict to match XSD field order.

    Required children come first (in XSD order), then optional
    children (in XSD order), then ``choice:`` at the end.
    """
    info = schema.get_element_info(element_name)
    if info is None:
        return children

    # Build an ordered list of child names from XSD
    xsd_order = {c.name: (0 if c.required else 1, i) for i, c in enumerate(info.children)}

    reordered: dict = {}
    # Sort child entries by XSD order, with unknown keys at the end
    sorted_keys = sorted(
        (k for k in children if k != "choice"),
        key=lambda k: xsd_order.get(k, (2, 999)),
    )
    for k in sorted_keys:
        reordered[k] = children[k]
    # choice: always last
    if "choice" in children:
        choice_data = children["choice"]
        if isinstance(choice_data, dict):
            # Also reorder choice entries by XSD order
            sorted_choice = sorted(
                choice_data,
                key=lambda k: xsd_order.get(k, (2, 999)),
            )
            reordered["choice"] = {k: choice_data[k] for k in sorted_choice}
        else:
            reordered["choice"] = choice_data
    return reordered


def reorder_attributes(attributes: dict, element_name: str, schema: AknSchema) -> dict:
    """Reorder an attributes dict: required first (XSD order), then optional (XSD order)."""
    info = schema.get_element_info(element_name)
    if info is None:
        return attributes

    xsd_order = {a.name: (0 if a.required else 1, i) for i, a in enumerate(info.attributes)}
    sorted_keys = sorted(
        attributes,
        key=lambda k: xsd_order.get(k, (2, 999)),
    )
    return {k: attributes[k] for k in sorted_keys}


def reorder_profile(yaml_text: str, schema: AknSchema) -> str:
    """Reorder the entire profile into canonical order.

    - Elements: topological parent-before-child with alphabetical tiebreaking.
    - Children within each element: XSD field order (required first).
    - Attributes within each element: XSD field order (required first).

    Returns the modified YAML text.
    """
    raw = yaml.safe_load(yaml_text)
    if not isinstance(raw, dict) or "profile" not in raw:
        return yaml_text

    profile = raw["profile"]
    if not isinstance(profile, dict):
        return yaml_text

    elements = profile.get("elements")
    if not isinstance(elements, dict):
        return yaml_text

    # Reorder children and attributes within each element
    for ename, edata in elements.items():
        if not isinstance(edata, dict):
            continue
        if "children" in edata and isinstance(edata["children"], dict):
            edata["children"] = reorder_children(edata["children"], ename, schema)
        if "attributes" in edata and isinstance(edata["attributes"], dict):
            edata["attributes"] = reorder_attributes(edata["attributes"], ename, schema)

    # Reorder elements themselves
    _apply_element_order(elements, schema)

    return _dump(raw)


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
