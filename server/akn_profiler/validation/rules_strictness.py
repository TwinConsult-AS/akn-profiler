"""
Rule category 5 — **Strictness rules** (XSD Cardinality).

Validates that a profile does not *loosen* what the XSD requires.
A profile may only be as strict or stricter than the schema.

Requirements enforced:
  - If an XSD-required child is omitted from a profile's ``children``
    list (when a ``children`` key is present), emit an ERROR.
  - If an XSD-required attribute is not listed under a profile element
    (when an ``attributes`` key is present), emit an ERROR.
  - Document-type coverage: the profile's ``elements`` should cover
    every required-child chain for its declared document types.

All diagnostics are ERRORs — loosening the XSD is not allowed.
"""

from __future__ import annotations

from akn_profiler.models.profile import ProfileDocument
from akn_profiler.validation.errors import Severity, ValidationError
from akn_profiler.validation.yaml_parser import LineIndex
from akn_profiler.xsd.schema_loader import AknSchema


def validate(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    errors.extend(_check_required_children(profile, schema, line_index))
    errors.extend(_check_required_attributes(profile, schema, line_index))
    errors.extend(_check_required_chain(profile, schema, line_index))
    errors.extend(_check_child_cardinality(profile, schema, line_index))
    errors.extend(_check_attribute_required(profile, schema, line_index))
    errors.extend(_check_undeclared_child_elements(profile, schema, line_index))
    return errors


# ------------------------------------------------------------------
# Required children
# ------------------------------------------------------------------


def _check_required_children(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Warn when a profile's ``children`` list omits XSD-required children."""
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not restriction.children:
            # No explicit children list — nothing to check
            continue

        if not schema.has_element(elem_name):
            continue

        req_children = {c.name for c in schema.get_required_children(elem_name)}
        listed_children = set(restriction.children.keys())
        missing = req_children - listed_children

        elem_path = f"profile.elements.{elem_name}.children"
        for child_name in sorted(missing):
            errors.append(
                ValidationError(
                    rule_id="strictness.missing-required-child",
                    path=elem_path,
                    message=(
                        f"<{child_name}> is required by the XSD inside "
                        f"<{elem_name}> but is not listed in 'children'. "
                        f"The profile is loosening the schema."
                    ),
                    severity=Severity.ERROR,
                    line=line_index.get(elem_path),
                )
            )

    return errors


# ------------------------------------------------------------------
# Required attributes
# ------------------------------------------------------------------


def _check_required_attributes(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Warn when a profile's ``attributes`` mapping omits XSD-required attrs."""
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not restriction.attributes:
            # No explicit attributes — nothing to check
            continue

        if not schema.has_element(elem_name):
            continue

        req_attrs = {a.name for a in schema.get_required_attributes(elem_name)}
        listed_attrs = set(restriction.attributes.keys())
        missing = req_attrs - listed_attrs

        elem_path = f"profile.elements.{elem_name}.attributes"
        for attr_name in sorted(missing):
            errors.append(
                ValidationError(
                    rule_id="strictness.missing-required-attribute",
                    path=elem_path,
                    message=(
                        f"'{attr_name}' is XSD-required on <{elem_name}> "
                        f"but is not listed under 'attributes'. "
                        f"The profile is loosening the schema."
                    ),
                    severity=Severity.ERROR,
                    line=line_index.get(elem_path),
                )
            )

    return errors


# ------------------------------------------------------------------
# Required-chain coverage
# ------------------------------------------------------------------


def _check_required_chain(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Warn when the profile omits elements that are on the required-child
    chain of a declared document type.

    For example, if ``act`` requires ``meta`` which requires
    ``identification``, all three should appear in ``elements:``.
    """
    errors: list[ValidationError] = []

    for dt in profile.documentTypes:
        if not schema.has_element(dt):
            continue  # vocabulary module reports this
        missing = _walk_required_chain(schema, dt, set(profile.elements.keys()), set())
        for elem_name in sorted(missing):
            errors.append(
                ValidationError(
                    rule_id="strictness.missing-required-element",
                    path="profile.elements",
                    message=(
                        f"<{elem_name}> is on the required-child chain "
                        f"of document type '{dt}' but is not declared "
                        f"in the profile's 'elements' section."
                    ),
                    severity=Severity.ERROR,
                    line=line_index.get("profile.elements"),
                )
            )

    return errors


def _walk_required_chain(
    schema: AknSchema,
    elem_name: str,
    declared: set[str],
    visited: set[str],
) -> list[str]:
    """Recursively collect elements in the required chain that are not
    declared in the profile."""
    if elem_name in visited:
        return []
    visited.add(elem_name)

    missing: list[str] = []
    if elem_name not in declared:
        missing.append(elem_name)

    info = schema.get_element_info(elem_name)
    if info is None:
        return missing

    for child in info.children:
        if child.required:
            missing.extend(_walk_required_chain(schema, child.name, declared, visited))

    return missing


# ------------------------------------------------------------------
# Child cardinality strictness
# ------------------------------------------------------------------


def _parse_cardinality(card: str) -> tuple[int, int | None]:
    """Parse a cardinality string like ``'1..1'`` or ``'0..*'``.

    Returns ``(min_occurs, max_occurs)`` where max is ``None`` for
    unbounded (``*``).
    """
    parts = card.split("..")
    if len(parts) != 2:
        return 0, None
    lo = int(parts[0])
    hi = None if parts[1] == "*" else int(parts[1])
    return lo, hi


def _check_child_cardinality(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Warn when a profile's child cardinality is less strict than the XSD."""
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not restriction.children:
            continue
        if not schema.has_element(elem_name):
            continue

        # Build lookup of XSD child cardinalities
        info = schema.get_element_info(elem_name)
        if info is None:
            continue
        xsd_children = {c.name: c for c in info.children}

        for child_name, card_str in restriction.children.items():
            if card_str is None:
                continue  # uses XSD default — always valid
            if child_name not in xsd_children:
                continue  # vocabulary module reports this

            child_path = f"profile.elements.{elem_name}.children.{child_name}"
            xsd_child = xsd_children[child_name]
            p_min, p_max = _parse_cardinality(card_str)
            x_min = xsd_child.min_occurs
            x_max = xsd_child.max_occurs  # None = unbounded

            # Profile min must be >= XSD min (cannot lower minimum)
            if p_min < x_min:
                errors.append(
                    ValidationError(
                        rule_id="strictness.loosened-child-cardinality",
                        path=child_path,
                        message=(
                            f"Profile sets min_occurs={p_min} for "
                            f"<{child_name}> inside <{elem_name}>, but "
                            f"the XSD requires at least {x_min}. "
                            f"The profile is loosening the schema."
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(child_path),
                    )
                )

            # Profile max must be <= XSD max (cannot raise maximum)
            # unless XSD is unbounded (None)
            if x_max is not None:
                if p_max is None or p_max > x_max:
                    errors.append(
                        ValidationError(
                            rule_id="strictness.loosened-child-cardinality",
                            path=child_path,
                            message=(
                                f"Profile sets max_occurs="
                                f"{'*' if p_max is None else p_max} for "
                                f"<{child_name}> inside <{elem_name}>, but "
                                f"the XSD allows at most {x_max}. "
                                f"The profile is loosening the schema."
                            ),
                            severity=Severity.ERROR,
                            line=line_index.get(child_path),
                        )
                    )

    return errors


# ------------------------------------------------------------------
# Attribute required strictness
# ------------------------------------------------------------------


def _check_attribute_required(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Warn when a profile marks an XSD-required attribute as not required."""
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not restriction.attributes:
            continue
        if not schema.has_element(elem_name):
            continue

        xsd_attrs = {a.name: a for a in schema.get_attributes(elem_name)}

        for attr_name, attr_r in restriction.attributes.items():
            if attr_name not in xsd_attrs:
                continue  # vocabulary module reports this

            xsd_attr = xsd_attrs[attr_name]
            if xsd_attr.required and not attr_r.required:
                attr_path = f"profile.elements.{elem_name}.attributes.{attr_name}"
                errors.append(
                    ValidationError(
                        rule_id="strictness.loosened-attribute-required",
                        path=attr_path,
                        message=(
                            f"'{attr_name}' is required by the XSD on "
                            f"<{elem_name}> but the profile does not "
                            f"mark it as required. The profile is "
                            f"loosening the schema."
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(attr_path),
                    )
                )

    return errors


# ------------------------------------------------------------------
# Undeclared child elements
# ------------------------------------------------------------------


def _check_undeclared_child_elements(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Flag children listed under an element that are not themselves
    declared in the profile's ``elements`` section.

    Every child referenced in a ``children:`` block should have its own
    element definition so that the profile is self-consistent.
    """
    errors: list[ValidationError] = []
    declared = set(profile.elements.keys())

    for elem_name, restriction in profile.elements.items():
        if not restriction.children:
            continue
        if not schema.has_element(elem_name):
            continue  # vocabulary module reports this

        for child_name in restriction.children:
            if not schema.has_element(child_name):
                continue  # vocabulary module reports unknown elements
            if child_name not in declared:
                child_path = f"profile.elements.{elem_name}.children.{child_name}"
                errors.append(
                    ValidationError(
                        rule_id="strictness.undeclared-child-element",
                        path=child_path,
                        message=(
                            f"'{child_name}' is listed as a child of "
                            f"<{elem_name}> but has no element definition "
                            f"in the profile. Add it to 'elements' to keep "
                            f"the profile valid."
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(child_path),
                    )
                )

    return errors
