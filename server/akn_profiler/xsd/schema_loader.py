"""
AKN Profiler — Schema Loader

Introspects the xsdata-generated dataclasses to build a queryable
representation of the Akoma Ntoso 3.0 schema.

Usage:

    from akn_profiler.xsd.schema_loader import AknSchema

    schema = AknSchema.load()
    schema.has_element("act")               # True
    schema.has_element("foobar")            # False
    schema.get_children("akomaNtoso")       # ['act', 'bill', 'debate', ...]
    schema.get_attributes("block")          # [AttrInfo(name='class', ...)]
    schema.get_element_info("article")      # ElementInfo(...)
"""

from __future__ import annotations

import dataclasses
import inspect
import logging
import re
from dataclasses import fields
from enum import Enum
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from akn_profiler.xsd import generated as gen
from akn_profiler.xsd.choice_parser import ChoiceGroup, parse_xsd_choices

logger = logging.getLogger(__name__)

AKN_NS = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

# XSD namespace prefix for ElementTree tag matching
_XS = "http://www.w3.org/2001/XMLSchema"
_XS_PREFIX = f"{{{_XS}}}"

# Path to the bundled AKN 3.0 XSD
_SCHEMA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "schemas"
_AKN_XSD = _SCHEMA_DIR / "akomantoso30.xsd"


def _parse_attribute_group_docs(xsd_path: Path | None = None) -> dict[str, str]:
    """Parse ``<xsd:attributeGroup>`` definitions and map each directly
    defined attribute name to the group's documentation ``<comment>`` text.

    When an attribute name appears in multiple groups the **most specific**
    group (the one that directly defines it, not via a ``ref``) wins.

    Returns a mapping ``{xml_attribute_name: documentation_text}``.
    """
    path = xsd_path or _AKN_XSD
    tree = ET.parse(path)  # noqa: S314
    root = tree.getroot()

    attr_docs: dict[str, str] = {}

    for ag in root.iterfind(f"{_XS_PREFIX}attributeGroup"):
        # Only handle top-level definitions (those with a 'name')
        group_name = ag.get("name")
        if not group_name:
            continue

        # Extract <comment> text from <xsd:annotation><xsd:documentation>
        doc_text = ""
        annotation = ag.find(f"{_XS_PREFIX}annotation")
        if annotation is not None:
            documentation = annotation.find(f"{_XS_PREFIX}documentation")
            if documentation is not None:
                # <comment> lives in the AKN namespace
                comment_el = documentation.find(f"{{{AKN_NS}}}comment")
                if comment_el is None:
                    # Fallback: try without namespace
                    comment_el = documentation.find("comment")
                if comment_el is not None and comment_el.text:
                    doc_text = " ".join(comment_el.text.split()).strip()

        if not doc_text:
            continue

        # Map each directly-defined attribute in this group to the doc
        for attr_el in ag.findall(f"{_XS_PREFIX}attribute"):
            attr_name = attr_el.get("name") or attr_el.get("ref")
            if attr_name:
                # Only set if not already assigned (first/most-specific wins)
                if attr_name not in attr_docs:
                    attr_docs[attr_name] = doc_text

    return attr_docs


@dataclasses.dataclass(frozen=True)
class AttrInfo:
    """Describes a single attribute on an AKN element."""

    name: str
    """The XML attribute name (e.g. 'eId', 'wId', 'class')."""

    python_name: str
    """The Python field name on the dataclass (e.g. 'e_id', 'w_id', 'class_value')."""

    required: bool
    """Whether the attribute is required (no default / no None default)."""

    type_hint: str
    """String representation of the Python type annotation."""

    enum_values: list[str]
    """If the type is an Enum, the list of allowed string values; else empty."""

    pattern: str | None = None
    """XSD ``xs:pattern`` facet regex, if any (e.g. ``[^\\s]+`` for eId)."""

    doc: str = ""
    """Documentation extracted from the XSD attribute group annotation."""

    @property
    def cardinality(self) -> str:
        """Return cardinality notation: ``1..1`` if required, ``0..1`` if optional."""
        return "1..1" if self.required else "0..1"


@dataclasses.dataclass(frozen=True)
class ChildInfo:
    """Describes a child element that an AKN element can contain."""

    name: str
    """The XML element name (e.g. 'meta', 'body', 'preface')."""

    python_name: str
    """The Python field name on the dataclass."""

    required: bool
    """Whether the child is required (min_occurs >= 1)."""

    is_list: bool
    """Whether the child can appear multiple times (list field)."""

    type_name: str
    """The Python class name of the child element's type."""

    min_occurs: int = 0
    """Minimum number of occurrences (from xsdata metadata or type analysis)."""

    max_occurs: int | None = None
    """Maximum occurrences.  ``None`` means unbounded (∞)."""

    choice_group_ids: tuple[str, ...] = ()
    """IDs of :class:`ChoiceGroup` instances this child belongs to."""

    @property
    def cardinality(self) -> str:
        """Return human-readable cardinality notation.

        Examples: ``1..1``, ``0..1``, ``1..*``, ``0..*``.
        """
        hi = "*" if self.max_occurs is None else str(self.max_occurs)
        return f"{self.min_occurs}..{hi}"


@dataclasses.dataclass(frozen=True)
class ElementInfo:
    """Full description of a single AKN element as defined in the XSD."""

    xml_name: str
    """The XML element name (e.g. 'act', 'article', 'akomaNtoso')."""

    class_name: str
    """The Python dataclass name (e.g. 'Act', 'Article', 'AkomaNtoso')."""

    parent_classes: list[str]
    """Base class names in the MRO (excluding object)."""

    attributes: list[AttrInfo]
    """All XML attributes available on this element."""

    children: list[ChildInfo]
    """All child XML elements this element can contain."""

    namespace: str
    """The XML namespace."""

    doc: str
    """Extracted documentation string."""

    choice_groups: tuple["ChoiceGroup", ...] = ()
    """Choice group constraints from the content model."""


class AknSchema:
    """
    Queryable representation of the Akoma Ntoso 3.0 XSD schema.

    Built by introspecting the xsdata-generated dataclasses in
    ``akn_profiler.xsd.generated``.
    """

    def __init__(self) -> None:
        # xml_name -> ElementInfo
        self._elements: dict[str, ElementInfo] = {}
        # class_name -> xml_name
        self._class_to_xml: dict[str, str] = {}
        # All enum types: enum_class_name -> list of string values
        self._enums: dict[str, list[str]] = {}
        # attribute xml_name -> documentation from XSD attribute group
        self._attr_docs: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def load(cls) -> AknSchema:
        """
        Introspect every xsdata-generated class and build the schema
        index.  This is relatively fast (~50 ms) and should be called
        once at server start-up.
        """
        schema = cls()
        schema._attr_docs = _parse_attribute_group_docs()
        schema._index_enums()
        schema._index_elements()
        schema._attach_choice_groups()
        logger.info(
            "AKN schema loaded: %d elements, %d enums",
            len(schema._elements),
            len(schema._enums),
        )
        return schema

    # ------------------------------------------------------------------
    # Public query API
    # ------------------------------------------------------------------

    def has_element(self, xml_name: str) -> bool:
        """Does the AKN schema define an element with this XML name?"""
        return xml_name in self._elements

    def get_element_info(self, xml_name: str) -> ElementInfo | None:
        """Return full element information, or None if not found."""
        return self._elements.get(xml_name)

    def get_children(self, xml_name: str) -> list[str]:
        """Return XML names of allowed child elements for *xml_name*."""
        info = self._elements.get(xml_name)
        if info is None:
            return []
        return [c.name for c in info.children]

    def get_attributes(self, xml_name: str) -> list[AttrInfo]:
        """Return attribute descriptors for *xml_name*."""
        info = self._elements.get(xml_name)
        if info is None:
            return []
        return list(info.attributes)

    def get_required_attributes(self, xml_name: str) -> list[AttrInfo]:
        """Return only the required attributes for *xml_name*."""
        return [a for a in self.get_attributes(xml_name) if a.required]

    def get_required_children(self, xml_name: str) -> list[ChildInfo]:
        """Return only the required child elements for *xml_name*."""
        info = self._elements.get(xml_name)
        if info is None:
            return []
        return [c for c in info.children if c.required]

    def element_names(self) -> list[str]:
        """Return all known AKN element XML names, sorted."""
        return sorted(self._elements)

    def get_enum_values(self, enum_class_name: str) -> list[str] | None:
        """Return the allowed string values for an enum type, or None."""
        return self._enums.get(enum_class_name)

    def all_enums(self) -> dict[str, list[str]]:
        """Return a copy of the full enum registry."""
        return dict(self._enums)

    def get_choice_groups(self, xml_name: str) -> tuple[ChoiceGroup, ...]:
        """Return choice group constraints for *xml_name*'s content model."""
        info = self._elements.get(xml_name)
        if info is None:
            return ()
        return info.choice_groups

    def get_choice_cardinality(self, xml_name: str) -> str | None:
        """Return the XSD default choice cardinality for *xml_name*.

        Looks at the **primary** (first meaningful) choice group and
        converts its ``min_occurs`` / ``max_occurs`` to a ``"min..max"``
        string using the same notation as child cardinality.

        Returns ``None`` when the element has no choice groups.
        """
        groups = self.get_choice_groups(xml_name)
        if not groups:
            return None
        # Pick the first group with min_occurs >= 1 or exclusive; fall
        # back to the first group overall.
        primary = groups[0]
        for cg in groups:
            if cg.min_occurs >= 1 or cg.exclusive:
                primary = cg
                break
        max_str = "*" if primary.max_occurs is None else str(primary.max_occurs)
        return f"{primary.min_occurs}..{max_str}"

    # ------------------------------------------------------------------
    # Internal indexing
    # ------------------------------------------------------------------

    def _index_enums(self) -> None:
        """Walk the generated module and index every Enum subclass."""
        for name, obj in inspect.getmembers(gen, inspect.isclass):
            if issubclass(obj, Enum) and obj is not Enum:
                self._enums[name] = [member.value for member in obj]

    def _index_elements(self) -> None:
        """Walk the generated module and index every dataclass."""
        for name, obj in inspect.getmembers(gen, inspect.isclass):
            if not dataclasses.is_dataclass(obj) or issubclass(obj, Enum):
                continue

            xml_name = self._xml_name_of(obj)
            if xml_name is None:
                # Abstract/complex types without a Meta.name — index
                # them by their Python class name so they're still accessible.
                continue

            ns = self._namespace_of(obj)
            attrs, children = self._classify_fields(obj)

            parents = [base.__name__ for base in inspect.getmro(obj)[1:] if base is not object]

            info = ElementInfo(
                xml_name=xml_name,
                class_name=name,
                parent_classes=parents,
                attributes=attrs,
                children=children,
                namespace=ns,
                doc=self._extract_doc(obj),
            )
            self._elements[xml_name] = info
            self._class_to_xml[name] = xml_name

    def _attach_choice_groups(self) -> None:
        """Parse XSD choice groups and attach them to elements.

        For each element, we find the complex type it uses (via the
        xsdata-generated class name and its MRO) and attach:
        1. Choice groups to ``ElementInfo.choice_groups``
        2. Choice group IDs to each ``ChildInfo.choice_group_ids``
        """
        parser = parse_xsd_choices()

        # Build mapping: Python class name → complex type name used in XSD.
        # xsdata names the class after the element but uses the complex type
        # from the XSD as the base class.  We check both the class name
        # (PascalCase of the type) and MRO parent class names.
        for xml_name, info in list(self._elements.items()):
            # Collect candidate type names: the class itself and all parents
            candidates = [info.class_name] + info.parent_classes
            matched_groups: list[ChoiceGroup] = []

            for candidate in candidates:
                # xsdata class name → XSD type name mapping.
                # xsdata typically names the Python class identically to the
                # XSD type (with PascalCase).  We look up by exact name first,
                # then fall back to case-insensitive.
                type_name = candidate
                if type_name in parser.type_choice_groups:
                    matched_groups.extend(parser.type_choice_groups[type_name])
                else:
                    # Try case-insensitive
                    for tn, cgs in parser.type_choice_groups.items():
                        if tn.lower() == type_name.lower():
                            matched_groups.extend(cgs)
                            break

            if not matched_groups:
                continue

            # Deduplicate by group_id
            seen_ids: set[str] = set()
            unique_groups: list[ChoiceGroup] = []
            for cg in matched_groups:
                if cg.group_id not in seen_ids:
                    seen_ids.add(cg.group_id)
                    unique_groups.append(cg)

            # Annotate children with their choice group membership
            new_children: list[ChildInfo] = []
            for child in info.children:
                cg_ids: list[str] = []
                for cg in unique_groups:
                    if child.name in cg.all_elements:
                        cg_ids.append(cg.group_id)
                if cg_ids:
                    new_children.append(dataclasses.replace(child, choice_group_ids=tuple(cg_ids)))
                else:
                    new_children.append(child)

            # Replace the ElementInfo with an updated copy
            self._elements[xml_name] = dataclasses.replace(
                info,
                children=new_children,
                choice_groups=tuple(unique_groups),
            )

    # ------------------------------------------------------------------
    # Field classification helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _xml_name_of(cls: type) -> str | None:
        """Extract the XML element name from the inner Meta class."""
        meta = getattr(cls, "Meta", None)
        if meta is None:
            return None
        return getattr(meta, "name", None)

    @staticmethod
    def _namespace_of(cls: type) -> str:
        meta = getattr(cls, "Meta", None)
        if meta is None:
            return AKN_NS
        return getattr(meta, "namespace", getattr(meta, "target_namespace", AKN_NS))

    @staticmethod
    def _extract_doc(cls: type) -> str:
        """Pull a documentation string from the xsdata-generated class.

        xsdata embeds XML annotations in __doc__ as XML fragments like:
            <ns1:comment xmlns:ns1="..."> Element
            act is used for describing the structure and content of an
            act</ns1:comment>.

        We extract the text between <ns1:comment ...> and </ns1:comment>,
        strip XML tags, and join lines.  If no comment tag is found we
        return an empty string (avoiding Python type-signature fallback).
        """
        raw = cls.__doc__ or ""
        # Try to pull text from <ns1:comment ...>...</ns1:comment>
        m = re.search(
            r"<[^>]*:?comment[^>]*>(.*?)</[^>]*:?comment[^>]*>",
            raw,
            re.DOTALL | re.IGNORECASE,
        )
        if m:
            text = m.group(1)
            # Strip any remaining XML tags
            text = re.sub(r"<[^>]+>", "", text)
            # Normalise whitespace
            text = " ".join(text.split()).strip().rstrip(".")
            if text:
                return text + "."
        # No XML comment found — don't fall back to Python type signatures
        return ""

    def _classify_fields(self, cls: type) -> tuple[list[AttrInfo], list[ChildInfo]]:
        """
        Split a dataclass's fields into XML attributes and child elements
        based on the xsdata metadata ``type`` key.
        """
        attrs: list[AttrInfo] = []
        children: list[ChildInfo] = []

        for f in fields(cls):
            meta: dict[str, Any] = {}
            # xsdata stores metadata in the standard dataclass metadata mapping
            for key in ("type", "name", "namespace"):
                if key in f.metadata:
                    meta[key] = f.metadata[key]

            field_type = meta.get("type", "")
            xml_name = meta.get("name", f.name)

            type_str = self._type_hint_str(f)
            is_list = "list[" in type_str.lower() or "List[" in type_str

            # Determine min_occurs / max_occurs from xsdata metadata
            xsd_min_occurs: int = f.metadata.get("min_occurs", 0)
            xsd_required: bool = f.metadata.get("required", False)

            if field_type == "Attribute":
                required = self._is_required(f)
                enum_vals = self._enum_values_for_field(f)
                pattern = f.metadata.get("pattern")
                doc = self._attr_docs.get(xml_name, "")
                attrs.append(
                    AttrInfo(
                        name=xml_name,
                        python_name=f.name,
                        required=required,
                        type_hint=type_str,
                        enum_values=enum_vals,
                        pattern=pattern,
                        doc=doc,
                    )
                )
            elif field_type == "Element":
                # Singular element: max_occurs = 1
                if is_list:
                    min_occ = max(xsd_min_occurs, 1 if xsd_required else 0)
                    max_occ: int | None = None  # unbounded
                else:
                    min_occ = 1 if self._is_required(f) else 0
                    max_occ = 1
                required = min_occ >= 1
                type_name = self._element_type_name(f)
                children.append(
                    ChildInfo(
                        name=xml_name,
                        python_name=f.name,
                        required=required,
                        is_list=is_list,
                        type_name=type_name,
                        min_occurs=min_occ,
                        max_occurs=max_occ,
                    )
                )
            elif field_type in ("Elements", "Wildcard"):
                # Group/choice elements — always list, always unbounded
                min_occ = max(xsd_min_occurs, 1 if xsd_required else 0)
                required = min_occ >= 1
                type_name = self._element_type_name(f)
                children.append(
                    ChildInfo(
                        name=xml_name,
                        python_name=f.name,
                        required=required,
                        is_list=True,
                        type_name=type_name,
                        min_occurs=min_occ,
                        max_occurs=None,
                    )
                )
            elif field_type == "Text":
                # Mixed text content — not a child or attribute
                pass
            # else: ignore unknown metadata types

        return attrs, children

    @staticmethod
    def _is_required(f: dataclasses.Field) -> bool:  # type: ignore[type-arg]
        """
        A field is required if it has no default and its type does not
        include None.
        """
        if f.default is not dataclasses.MISSING:
            return f.default is not None
        if f.default_factory is not dataclasses.MISSING:  # type: ignore[arg-type]
            return False
        return True

    @staticmethod
    def _type_hint_str(f: dataclasses.Field) -> str:  # type: ignore[type-arg]
        """Return a human-readable type string for a field."""
        hint = f.type
        if hint is None:
            return "Any"
        if isinstance(hint, str):
            return hint
        return getattr(hint, "__name__", str(hint))

    def _enum_values_for_field(self, f: dataclasses.Field) -> list[str]:  # type: ignore[type-arg]
        """If the field's type is an Enum, return its allowed values."""
        hint = f.type
        if isinstance(hint, str):
            # Resolve forward reference against the generated module
            resolved = getattr(gen, hint, None)
            if resolved and inspect.isclass(resolved) and issubclass(resolved, Enum):
                return [m.value for m in resolved]
            # Handle 'None | EnumType' patterns
            for part in hint.split("|"):
                part = part.strip()
                resolved = getattr(gen, part, None)
                if resolved and inspect.isclass(resolved) and issubclass(resolved, Enum):
                    return [m.value for m in resolved]
        elif inspect.isclass(hint) and issubclass(hint, Enum):
            return [m.value for m in hint]
        return []

    @staticmethod
    def _element_type_name(f: dataclasses.Field) -> str:  # type: ignore[type-arg]
        """Extract the class name of a child element's type."""
        hint = f.type
        if isinstance(hint, str):
            # Strip None | ..., list[...], etc.
            for part in hint.replace("None", "").split("|"):
                part = part.strip()
                if part.startswith("list["):
                    part = part[5:].rstrip("]").strip()
                if part and part[0].isupper():
                    return part
            return hint
        return getattr(hint, "__name__", str(hint))
