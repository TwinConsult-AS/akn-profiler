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
from typing import Any

from akn_profiler.xsd import generated as gen

logger = logging.getLogger(__name__)

AKN_NS = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


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
        schema._index_enums()
        schema._index_elements()
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
                attrs.append(
                    AttrInfo(
                        name=xml_name,
                        python_name=f.name,
                        required=required,
                        type_hint=type_str,
                        enum_values=enum_vals,
                        pattern=pattern,
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
