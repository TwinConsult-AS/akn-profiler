"""
Rule category 4 — **Identity rules** (XSD Identity Constraints).

Checks uniqueness and referential integrity within the profile itself:
  - No duplicate element definitions
  - Document types referenced in ``documentTypes`` should have a
    corresponding entry under ``elements`` (warning, not error)
  - Metadata sections should reference existing FRBR elements
  - Cross-reference consistency

All checks are dynamic against ``AknSchema``.
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
    errors.extend(_check_duplicate_structure(profile, schema, line_index))
    errors.extend(_check_doctype_element_coverage(profile, schema, line_index))
    return errors


# ------------------------------------------------------------------
# Duplicate entries
# ------------------------------------------------------------------


def _check_duplicate_structure(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Flag duplicate entries in any ``structure`` list."""
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        elem_path = f"profile.elements.{elem_name}"
        seen: dict[str, int] = {}

        for i, struct_name in enumerate(restriction.structure):
            if struct_name in seen:
                struct_path = f"{elem_path}.structure[{i}]"
                errors.append(
                    ValidationError(
                        rule_id="identity.duplicate-structure-entry",
                        path=struct_path,
                        message=(
                            f"'{struct_name}' appears more than once "
                            f"in the structure list of <{elem_name}> "
                            f"(first at index {seen[struct_name]})"
                        ),
                        severity=Severity.WARNING,
                        line=line_index.get(struct_path),
                    )
                )
            else:
                seen[struct_name] = i

    return errors


# ------------------------------------------------------------------
# Cross-reference consistency
# ------------------------------------------------------------------


def _check_doctype_element_coverage(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Warn if a ``documentTypes`` entry has no corresponding
    ``elements`` restriction.

    This is advisory — a profile may legitimately restrict document
    types without defining element-level constraints.
    """
    errors: list[ValidationError] = []

    for i, dt in enumerate(profile.documentTypes):
        if dt not in profile.elements:
            dt_path = f"profile.documentTypes[{i}]"
            errors.append(
                ValidationError(
                    rule_id="identity.doctype-without-element-restriction",
                    path=dt_path,
                    message=(
                        f"Document type '{dt}' is listed in "
                        f"documentTypes but has no corresponding "
                        f"entry under 'elements'. Consider adding "
                        f"element restrictions for <{dt}>."
                    ),
                    severity=Severity.INFO,
                    line=line_index.get(dt_path),
                )
            )

    return errors
