"""
Rule category 2 — **Structure rules** (XSD Complex Types).

Checks containment and hierarchy:
  - Can ``<parent>`` contain ``<child>`` according to the XSD?
  - Does the ``structure`` ordering form a valid containment chain
    (each level can be a child of the previous one)?

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
    errors.extend(_check_children(profile, schema, line_index))
    errors.extend(_check_structure(profile, schema, line_index))
    return errors


# ------------------------------------------------------------------
# Children containment
# ------------------------------------------------------------------


def _check_children(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Each ``children`` entry must be a valid child of its parent
    element according to the XSD content model.

    (Vocabulary existence is checked by ``rules_vocabulary``; here we
    only test containment for elements that *do* exist.)
    """
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not schema.has_element(elem_name):
            continue  # vocabulary module reports this

        elem_path = f"profile.elements.{elem_name}"
        valid_children = set(schema.get_children(elem_name))

        for child_name in restriction.children:
            if not schema.has_element(child_name):
                continue  # vocabulary module reports this

            child_path = f"{elem_path}.children.{child_name}"
            if child_name not in valid_children:
                errors.append(
                    ValidationError(
                        rule_id="structure.invalid-child",
                        path=child_path,
                        message=(
                            f"<{elem_name}> cannot contain <{child_name}> "
                            f"according to the AKN schema. "
                            f"Valid children: {sorted(valid_children)}"
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(child_path),
                    )
                )

    return errors


# ------------------------------------------------------------------
# Structure hierarchy
# ------------------------------------------------------------------


def _check_structure(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Validate the ``structure`` ordering.

    ``structure: [chapter, article, paragraph]`` means the profile
    expects ``chapter`` to contain ``article`` and ``article`` to
    contain ``paragraph``.  We verify each consecutive pair is a valid
    parent→child relationship and that the first element in the chain
    is a valid child of the containing element.
    """
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not restriction.structure:
            continue
        if not schema.has_element(elem_name):
            continue

        elem_path = f"profile.elements.{elem_name}"
        struct = restriction.structure

        # First structure entry must be a valid child of the element itself
        first = struct[0]
        if schema.has_element(first):
            valid_children = set(schema.get_children(elem_name))
            if first not in valid_children:
                errors.append(
                    ValidationError(
                        rule_id="structure.invalid-structure-root",
                        path=f"{elem_path}.structure[0]",
                        message=(
                            f"<{first}> is not a valid child of "
                            f"<{elem_name}>, so it cannot be the first "
                            f"level of the structure hierarchy"
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(f"{elem_path}.structure[0]"),
                    )
                )

        # Each consecutive pair must form a valid parent→child
        for i in range(len(struct) - 1):
            parent_name = struct[i]
            child_name = struct[i + 1]

            # Skip pairs where either element is unknown (vocab error)
            if not schema.has_element(parent_name) or not schema.has_element(child_name):
                continue

            parent_children = set(schema.get_children(parent_name))
            if child_name not in parent_children:
                errors.append(
                    ValidationError(
                        rule_id="structure.invalid-structure-chain",
                        path=f"{elem_path}.structure[{i + 1}]",
                        message=(
                            f"<{parent_name}> cannot contain "
                            f"<{child_name}> according to the AKN "
                            f"schema, so the structure chain "
                            f"'{parent_name} > {child_name}' is invalid"
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(f"{elem_path}.structure[{i + 1}]"),
                    )
                )

    return errors
