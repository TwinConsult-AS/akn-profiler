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

from pydantic import BaseModel, Field, field_validator


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
    ``structure``
        Ordered list of hierarchical levels (e.g.
        ``[chapter, article, paragraph]``).  Each level must be a
        valid child of the previous one per the XSD.
    """

    attributes: dict[str, AttributeRestriction] = Field(default_factory=dict)
    children: dict[str, str | None] = Field(default_factory=dict)
    """Allowed children. Key = child name, value = cardinality or None."""
    structure: list[str] = Field(default_factory=list)

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
