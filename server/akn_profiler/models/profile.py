"""
Pydantic models for ``.akn.yaml`` application profile documents.

These models define what the YAML file *looks like* structurally.
They do **not** enforce XSD correctness — that is the job of the
rule modules in ``akn_profiler.validation.rules_*``.

Design philosophy — *presence means allowed*:

  - An element listed in ``elements:`` is allowed in conforming
    documents.
  - Cardinality on children is expressed as ``"min..max"`` strings
    (e.g. ``"1..1"``, ``"0..*"``).  A bare key (``None``) means
    "use the XSD default cardinality".
  - Attributes carry ``required: true/false`` to indicate whether
    the profile mandates the attribute.  This must be at least as
    strict as the XSD (an XSD-required attribute cannot be marked
    optional).

Pydantic catches:
  - wrong value types
  - unexpected nesting

The rule modules then cross-reference the *parsed* profile against
the live ``AknSchema`` to find semantic errors (including strictness
checks that prevent loosening XSD requirements).
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator


class AttributeRestriction(BaseModel):
    """Restriction placed on a single XML attribute.

    Presence in the profile means the attribute is *recognised* by this
    profile.

    ``required``
        Whether this attribute must be present on conforming elements.
        Must be at least as strict as the XSD — an XSD-required
        attribute cannot be marked ``required: false``.
    ``values``
        Restricts the allowed enum values (must be a subset of the
        XSD enum for that attribute).
    """

    required: bool = False
    """Whether this attribute is required by the profile."""

    values: list[str] = Field(default_factory=list)


class ElementRestriction(BaseModel):
    """Restriction placed on a single AKN element.

    Presence in the ``elements:`` section means the element is
    *allowed* in conforming documents.

    ``attributes``
        Per-attribute restrictions keyed by the XML attribute name.
    ``children``
        Allowed child elements with optional cardinality overrides.
        Keys are child element names, values are cardinality strings
        (e.g. ``"1..1"``, ``"0..*"``) or ``None`` for XSD defaults.
    ``exclusive_children``
        Exclusive children extracted from the ``choice:`` key
        inside ``children:``.  A flat ``dict[str, str|None]``
        mapping child names to cardinality strings.  Any given element
        instance must use exactly **one** of these children.

        Example YAML::

            children:
              num: "1..1"
              choice:
                section: "1..*"
                subchapter: "1..*"

        The ``model_validator`` moves the ``choice`` key out of
        ``children`` into ``exclusive_children`` so the ``children``
        dict contains only always-present child entries.
    ``structure``
        Ordered list of hierarchical levels (e.g.
        ``[chapter, article, paragraph]``).  Each level must be a
        valid child of the previous one per the XSD.
    """

    profileNote: str = ""
    """Curator annotation — explanatory text for readers of the profile."""

    attributes: dict[str, AttributeRestriction] = Field(default_factory=dict)
    children: dict[str, str | None] = Field(default_factory=dict)
    """Allowed children (always-present). Key = child name, value = cardinality or None."""
    exclusive_children: dict[str, str | None] = Field(default_factory=dict)
    """Exclusive children from ``choice:``.  Key = child name, value = cardinality."""
    structure: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _extract_choice(cls, data: object) -> object:
        """Pop ``choice`` from the ``children`` dict.

        In YAML the user writes::

            children:
              num: "1..1"
              choice:
                section: "1..*"
                subchapter: "1..*"

        This validator moves the ``choice`` key out of ``children``
        into ``exclusive_children`` so the ``children`` dict contains
        only always-present child entries.
        """
        if not isinstance(data, dict):
            return data
        children = data.get("children")
        if isinstance(children, dict) and "choice" in children:
            raw_choice = children.pop("choice")
            if isinstance(raw_choice, dict):
                data["exclusive_children"] = raw_choice
            elif isinstance(raw_choice, list):
                # Legacy list format: merge all branch dicts into one flat dict
                merged: dict[str, str | None] = {}
                for item in raw_choice:
                    if isinstance(item, dict):
                        merged.update(item)
                data["exclusive_children"] = merged
        return data

    @field_validator("attributes", mode="before")
    @classmethod
    def _coerce_attr_none(cls, v: object) -> object:
        """YAML bare keys (``name:``) parse as ``None`` — coerce to ``{}``."""
        if isinstance(v, dict):
            return {k: val if val is not None else {} for k, val in v.items()}
        return v

    @field_validator("children", mode="before")
    @classmethod
    def _coerce_children_none(cls, v: object) -> object:
        """Accept both dict and list formats; bare values become ``None``.

        Dict format (preferred)::

            children:
              meta: "1..1"
              body:           # bare key → None → XSD default
              choice:
                section: "1..*"
                subchapter: "1..*"

        ``None`` values stay as-is (meaning "use XSD default cardinality").
        """
        if isinstance(v, dict):
            return v  # already correct shape
        return v


class ProfileDocument(BaseModel):
    """Root model for a ``.akn.yaml`` application profile.

    Maps the top-level ``profile:`` key in the YAML.
    """

    name: str = ""
    version: str = ""
    description: str = ""

    documentTypes: list[str] = Field(default_factory=list)
    """Valid AKN document type names (children of ``<akomaNtoso>``)."""

    elements: dict[str, ElementRestriction] = Field(default_factory=dict)
    """Per-element restriction rules, keyed by XSD element name."""

    @field_validator("elements", mode="before")
    @classmethod
    def _coerce_elem_none(cls, v: object) -> object:
        """YAML bare keys (``act:``) parse as ``None`` — coerce to ``{}``."""
        if isinstance(v, dict):
            return {k: val if val is not None else {} for k, val in v.items()}
        return v
