"""
Rule category 3 — **Data-type rules** (XSD Simple Types).

Checks value-level constraints:
  - Enum subsetting: profile ``values`` must be a subset of the XSD
    enum for that attribute.
  - Pattern matching: if the XSD defines a ``pattern`` facet on an
    attribute, restricted values must conform.
  - No invented values: the profile must not introduce values that
    the XSD does not allow.

All checks are dynamic against ``AknSchema``.
"""

from __future__ import annotations

import re

from akn_profiler.models.profile import ProfileDocument
from akn_profiler.validation.errors import Severity, ValidationError
from akn_profiler.validation.yaml_parser import LineIndex
from akn_profiler.xsd.schema_loader import AknSchema, AttrInfo


def validate(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    errors.extend(_check_attribute_values(profile, schema, line_index))
    return errors


# ------------------------------------------------------------------
# Attribute value restrictions
# ------------------------------------------------------------------


def _check_attribute_values(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Validate every ``values`` list against the XSD type for that
    attribute.

    Two sub-checks per attribute:
      1. If the XSD attribute is enum-typed, every profile value must
         be a member of that enum.
      2. If the XSD attribute has a pattern facet, every profile value
         must match the pattern.
    """
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not schema.has_element(elem_name):
            continue  # vocabulary module

        elem_path = f"profile.elements.{elem_name}"
        # Build a lookup of attribute info by XML name
        attr_map: dict[str, AttrInfo] = {a.name: a for a in schema.get_attributes(elem_name)}

        for attr_name, attr_restriction in restriction.attributes.items():
            attr_path = f"{elem_path}.attributes.{attr_name}"

            if attr_name not in attr_map:
                continue  # vocabulary module reports this

            attr_info = attr_map[attr_name]

            if not attr_restriction.values:
                continue  # no value restriction to check

            # --- Enum subset check ----------------------------------
            if attr_info.enum_values:
                allowed_set = set(attr_info.enum_values)
                for i, val in enumerate(attr_restriction.values):
                    val_path = f"{attr_path}.values[{i}]"
                    if val not in allowed_set:
                        errors.append(
                            ValidationError(
                                rule_id="datatype.invalid-enum-value",
                                path=val_path,
                                message=(
                                    f"'{val}' is not a valid value for "
                                    f"attribute '{attr_name}' on "
                                    f"<{elem_name}>. "
                                    f"Allowed by XSD: "
                                    f"{sorted(allowed_set)}"
                                ),
                                severity=Severity.ERROR,
                                line=line_index.get(val_path),
                            )
                        )
            else:
                # The attribute is not enum-typed — the profile is
                # inventing an enum restriction.  This is valid
                # (profiles *tighten* the schema) but we issue an
                # informational note so the author knows the XSD
                # itself does not constrain these values.
                errors.append(
                    ValidationError(
                        rule_id="datatype.custom-enum-on-free-attribute",
                        path=f"{attr_path}.values",
                        message=(
                            f"Attribute '{attr_name}' on <{elem_name}> "
                            f"is not enum-typed in the XSD. The "
                            f"profile adds a custom value restriction "
                            f"[{', '.join(attr_restriction.values)}] — "
                            f"this is valid but not verifiable against "
                            f"the schema."
                        ),
                        severity=Severity.INFO,
                        line=line_index.get(f"{attr_path}.values"),
                    )
                )

            # --- Pattern check --------------------------------------
            _check_pattern(
                errors,
                attr_info,
                attr_restriction.values,
                elem_name,
                attr_name,
                attr_path,
                line_index,
            )

    return errors


def _check_pattern(
    errors: list[ValidationError],
    attr_info: AttrInfo,
    values: list[str],
    elem_name: str,
    attr_name: str,
    attr_path: str,
    line_index: LineIndex,
) -> None:
    """If the XSD defines a regex pattern facet, check each value."""
    if not attr_info.pattern:
        return

    try:
        compiled = re.compile(attr_info.pattern)
    except re.error:
        return  # malformed pattern in XSD — not the profile's fault

    for i, val in enumerate(values):
        if not compiled.fullmatch(val):
            val_path = f"{attr_path}.values[{i}]"
            errors.append(
                ValidationError(
                    rule_id="datatype.pattern-mismatch",
                    path=val_path,
                    message=(
                        f"'{val}' does not match the XSD pattern "
                        f"/{attr_info.pattern}/ for attribute "
                        f"'{attr_name}' on <{elem_name}>"
                    ),
                    severity=Severity.ERROR,
                    line=line_index.get(val_path),
                )
            )
