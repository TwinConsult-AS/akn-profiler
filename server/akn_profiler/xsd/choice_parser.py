"""
XSD Choice Group Parser

Parses the Akoma Ntoso 3.0 XSD to extract ``xs:choice`` and ``xs:group``
structures that are lost when xsdata flattens the schema into Python
dataclasses.

This module provides:

- Resolution of named ``<xsd:group>`` definitions to their member elements.
- Extraction of ``<xsd:choice>`` content model constraints per complex type,
  including:
  - Whether the choice is **exclusive** (``maxOccurs=1`` — pick exactly
    one branch) or **free-mix** (``maxOccurs=unbounded`` — any combination).
  - ``minOccurs`` on the choice (``0`` means optional, ``1`` means at
    least one member is required).
  - Branch membership: which element names belong to each branch.

All data is derived dynamically from the XSD — no element names are
hard-coded.
"""

from __future__ import annotations

import dataclasses
import logging
from pathlib import Path
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)

# XSD namespace
_XS = "http://www.w3.org/2001/XMLSchema"
_XS_PREFIX = f"{{{_XS}}}"

# Path to the bundled AKN 3.0 XSD
_SCHEMA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "schemas"
_AKN_XSD = _SCHEMA_DIR / "akomantoso30.xsd"


# ------------------------------------------------------------------
# Data classes
# ------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ChoiceBranch:
    """One branch inside an ``xs:choice``.

    All element names reachable through this branch (recursively
    resolving ``xs:group ref`` references) are collected into
    ``elements``.
    """

    branch_id: str
    """Identifier within the parent choice (e.g. ``'branch_0'``)."""

    elements: frozenset[str]
    """XML element names reachable via this branch."""

    label: str | None = None
    """Human-readable label (group name if the branch is a group ref)."""


@dataclasses.dataclass(frozen=True)
class ChoiceGroup:
    """An ``xs:choice`` occurrence inside a complex type's content model.

    Attributes
    ----------
    group_id
        Unique identifier scoped to the parent type
        (e.g. ``"bodyType:choice_0"``).
    min_occurs
        Minimum occurrences of the choice particle (XSD default ``1``).
    max_occurs
        Maximum occurrences (``None`` = unbounded).
    exclusive
        ``True`` when ``max_occurs == 1`` — the user must pick exactly
        one branch and cannot mix elements from different branches.
    branches
        The branches of this choice.
    """

    group_id: str
    min_occurs: int
    max_occurs: int | None
    exclusive: bool
    branches: tuple[ChoiceBranch, ...]

    @property
    def all_elements(self) -> frozenset[str]:
        """Union of elements across all branches."""
        result: set[str] = set()
        for b in self.branches:
            result |= b.elements
        return frozenset(result)


# ------------------------------------------------------------------
# Parser
# ------------------------------------------------------------------


class XsdChoiceParser:
    """Parses the AKN XSD to extract group definitions and choice groups.

    Usage::

        parser = XsdChoiceParser()
        parser.parse()
        # Named groups: parser.named_groups
        # Choice groups per complex type: parser.type_choice_groups
    """

    def __init__(self, xsd_path: Path | None = None) -> None:
        self._xsd_path = xsd_path or _AKN_XSD
        self.named_groups: dict[str, frozenset[str]] = {}
        """Resolved ``<xsd:group name="...">`` → member element names."""

        self.type_choice_groups: dict[str, list[ChoiceGroup]] = {}
        """Complex type name → list of ``ChoiceGroup`` in its content model."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(self) -> None:
        """Parse the XSD and populate :attr:`named_groups` and
        :attr:`type_choice_groups`."""
        tree = ET.parse(self._xsd_path)
        root = tree.getroot()

        # Phase 1: index all <xsd:group name="..."> definitions
        self._index_named_groups(root)

        # Phase 2: walk complex types and extract choice groups
        self._index_complex_types(root)

        logger.info(
            "XSD choice parser: %d named groups, %d complex types with choices",
            len(self.named_groups),
            len(self.type_choice_groups),
        )

    # ------------------------------------------------------------------
    # Phase 1 — named group resolution
    # ------------------------------------------------------------------

    def _index_named_groups(self, root: ET.Element) -> None:
        """Resolve every ``<xsd:group name="...">`` to its leaf elements."""
        # First pass: collect raw group definitions
        raw: dict[str, ET.Element] = {}
        for group_el in root.findall(f"{_XS_PREFIX}group"):
            name = group_el.get("name")
            if name:
                raw[name] = group_el

        # Resolve recursively (handles nested group refs)
        for name in raw:
            if name not in self.named_groups:
                self.named_groups[name] = self._resolve_group(name, raw, set())

    def _resolve_group(
        self,
        name: str,
        raw: dict[str, ET.Element],
        visited: set[str],
    ) -> frozenset[str]:
        """Recursively resolve a named group to its leaf element names."""
        if name in self.named_groups:
            return self.named_groups[name]

        if name in visited:
            logger.warning("Circular group reference: %s", name)
            return frozenset()

        visited = visited | {name}
        group_el = raw.get(name)
        if group_el is None:
            return frozenset()

        elements: set[str] = set()
        self._collect_elements(group_el, raw, visited, elements)
        result = frozenset(elements)
        self.named_groups[name] = result
        return result

    def _collect_elements(
        self,
        node: ET.Element,
        raw: dict[str, ET.Element],
        visited: set[str],
        out: set[str],
    ) -> None:
        """Walk an XSD subtree collecting element ref names."""
        for child in node:
            tag = child.tag
            if tag == f"{_XS_PREFIX}element":
                ref = child.get("ref")
                if ref:
                    out.add(ref)
            elif tag == f"{_XS_PREFIX}group":
                ref = child.get("ref")
                if ref:
                    resolved = self._resolve_group(ref, raw, visited)
                    out.update(resolved)
            elif tag in (
                f"{_XS_PREFIX}choice",
                f"{_XS_PREFIX}sequence",
                f"{_XS_PREFIX}all",
            ):
                self._collect_elements(child, raw, visited, out)

    # ------------------------------------------------------------------
    # Phase 2 — complex type choice extraction
    # ------------------------------------------------------------------

    def _index_complex_types(self, root: ET.Element) -> None:
        """Find all ``<xsd:complexType>`` and extract choice groups."""
        # Collect raw named groups for resolving group refs in types
        raw_groups: dict[str, ET.Element] = {}
        for group_el in root.findall(f"{_XS_PREFIX}group"):
            name = group_el.get("name")
            if name:
                raw_groups[name] = group_el

        for ct in root.findall(f"{_XS_PREFIX}complexType"):
            type_name = ct.get("name")
            if not type_name:
                continue

            choices: list[ChoiceGroup] = []
            # Walk the content model (may be under extension/restriction)
            self._walk_for_choices(ct, type_name, raw_groups, choices, counter=[0])

            if choices:
                self.type_choice_groups[type_name] = choices

    def _walk_for_choices(
        self,
        node: ET.Element,
        type_name: str,
        raw_groups: dict[str, ET.Element],
        out: list[ChoiceGroup],
        counter: list[int],
    ) -> None:
        """Recursively walk an XSD content model node looking for
        ``<xsd:choice>`` particles.

        Descends into ``<xsd:complexContent>``, ``<xsd:extension>``,
        ``<xsd:restriction>``, ``<xsd:sequence>`` to find choice groups,
        but does NOT descend into nested ``<xsd:choice>`` children when
        building branches (branch resolution handles that).
        """
        for child in node:
            tag = child.tag

            if tag == f"{_XS_PREFIX}choice":
                cg = self._build_choice_group(child, type_name, raw_groups, counter)
                if cg is not None:
                    out.append(cg)

            elif tag in (
                f"{_XS_PREFIX}complexContent",
                f"{_XS_PREFIX}extension",
                f"{_XS_PREFIX}restriction",
                f"{_XS_PREFIX}sequence",
            ):
                self._walk_for_choices(child, type_name, raw_groups, out, counter)

    def _build_choice_group(
        self,
        choice_el: ET.Element,
        type_name: str,
        raw_groups: dict[str, ET.Element],
        counter: list[int],
    ) -> ChoiceGroup | None:
        """Build a ``ChoiceGroup`` from a single ``<xsd:choice>`` element."""
        min_occ = int(choice_el.get("minOccurs", "1"))
        max_occ_str = choice_el.get("maxOccurs", "1")
        max_occ: int | None = None if max_occ_str == "unbounded" else int(max_occ_str)

        exclusive = max_occ == 1

        branches: list[ChoiceBranch] = []
        branch_idx = 0

        for child in choice_el:
            tag = child.tag

            if tag == f"{_XS_PREFIX}element":
                ref = child.get("ref")
                if ref:
                    branches.append(
                        ChoiceBranch(
                            branch_id=f"branch_{branch_idx}",
                            elements=frozenset({ref}),
                            label=ref,
                        )
                    )
                    branch_idx += 1

            elif tag == f"{_XS_PREFIX}group":
                ref = child.get("ref")
                if ref:
                    members = self.named_groups.get(ref, frozenset())
                    if members:
                        branches.append(
                            ChoiceBranch(
                                branch_id=f"branch_{branch_idx}",
                                elements=members,
                                label=ref,
                            )
                        )
                        branch_idx += 1

            elif tag == f"{_XS_PREFIX}sequence":
                # A sequence branch inside a choice (e.g., hierarchy type)
                elements: set[str] = set()
                label_parts: list[str] = []
                self._collect_branch_elements(child, raw_groups, elements, label_parts)
                if elements:
                    label = " + ".join(label_parts) if label_parts else None
                    branches.append(
                        ChoiceBranch(
                            branch_id=f"branch_{branch_idx}",
                            elements=frozenset(elements),
                            label=label,
                        )
                    )
                    branch_idx += 1

            elif tag == f"{_XS_PREFIX}choice":
                # Nested <xsd:choice> as a branch (e.g., subFlowStructure
                # has an outer exclusive choice between documentType OR
                # an inner unbounded choice of block/container/hier elements).
                # Collect all elements from the nested choice into one branch.
                elements_inner: set[str] = set()
                label_parts_inner: list[str] = []
                self._collect_branch_elements(child, raw_groups, elements_inner, label_parts_inner)
                if elements_inner:
                    label = " + ".join(label_parts_inner) if label_parts_inner else None
                    branches.append(
                        ChoiceBranch(
                            branch_id=f"branch_{branch_idx}",
                            elements=frozenset(elements_inner),
                            label=label,
                        )
                    )
                    branch_idx += 1

            elif tag == f"{_XS_PREFIX}any":
                # xs:any wildcard — skip, not relevant for profile validation
                pass

        if not branches:
            return None

        idx = counter[0]
        counter[0] += 1

        return ChoiceGroup(
            group_id=f"{type_name}:choice_{idx}",
            min_occurs=min_occ,
            max_occurs=max_occ,
            exclusive=exclusive,
            branches=tuple(branches),
        )

    def _collect_branch_elements(
        self,
        node: ET.Element,
        raw_groups: dict[str, ET.Element],
        out: set[str],
        label_parts: list[str],
    ) -> None:
        """Collect element names from a sequence/choice branch subtree."""
        for child in node:
            tag = child.tag
            if tag == f"{_XS_PREFIX}element":
                ref = child.get("ref")
                if ref:
                    out.add(ref)
                    label_parts.append(ref)
            elif tag == f"{_XS_PREFIX}group":
                ref = child.get("ref")
                if ref:
                    members = self.named_groups.get(ref, frozenset())
                    out.update(members)
                    label_parts.append(ref)
            elif tag in (
                f"{_XS_PREFIX}choice",
                f"{_XS_PREFIX}sequence",
            ):
                self._collect_branch_elements(child, raw_groups, out, label_parts)


# ------------------------------------------------------------------
# Module-level convenience function
# ------------------------------------------------------------------


def parse_xsd_choices(xsd_path: Path | None = None) -> XsdChoiceParser:
    """Parse the AKN XSD and return the populated parser instance.

    This is the main entry point used by :class:`AknSchema`.
    """
    parser = XsdChoiceParser(xsd_path)
    parser.parse()
    return parser
