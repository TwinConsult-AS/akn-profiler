"""
Rule category 6 — **Choice rules** (XSD Choice Groups).

Validates that profiles respect ``xs:choice`` constraints from the XSD
content model.  All checks are dynamically derived from the XSD — no
element names are hard-coded.

Rules:
  - ``choice.required-group-empty`` — a mandatory choice group requires
    at least one member element in the profile's ``children:`` or
    ``choice:`` branches, but none are present.
  - ``choice.incomplete-branches`` — a ``choice:`` key is declared but
    has fewer than 2 populated branches.  A choice needs at least 2
    alternatives.
  - ``choice.exclusive-branch-conflict`` — children from multiple
    branches of an XSD exclusive choice are listed in ``children:``
    (outside ``choice:``).  Use ``choice:`` to express exclusivity.
  - ``choice.branch-invalid-child`` — a ``choice:`` branch contains
    an element that is not a valid child per the XSD.
  - ``choice.branch-overlap`` — a child appears in both ``children:``
    (always-present) and inside a ``choice:`` branch, or in multiple
    branches.
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
    errors.extend(_check_required_group_empty(profile, schema, line_index))
    errors.extend(_check_incomplete_branches(profile, schema, line_index))
    errors.extend(_check_exclusive_branch_conflict(profile, schema, line_index))
    errors.extend(_check_branch_invalid_child(profile, schema, line_index))
    errors.extend(_check_branch_overlap(profile, schema, line_index))
    return errors


# ------------------------------------------------------------------
# Required choice group — at least one member must be present
# ------------------------------------------------------------------


def _check_required_group_empty(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Emit an error when a mandatory choice group has no members
    declared anywhere (``children:`` or ``choice:`` branches).
    """
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not schema.has_element(elem_name):
            continue

        choice_groups = schema.get_choice_groups(elem_name)
        # Build set of ALL declared children (always-present + all branches)
        all_declared: set[str] = set(restriction.children.keys())
        all_declared.update(restriction.exclusive_children.keys())

        elem_path = f"profile.elements.{elem_name}"

        for cg in choice_groups:
            if cg.min_occurs < 1:
                continue  # optional choice — no requirement

            if not (cg.all_elements & all_declared):
                # Build a helpful message listing example members
                branch_descriptions: list[str] = []
                for branch in cg.branches:
                    label = branch.label or branch.branch_id
                    examples = sorted(branch.elements)[:5]
                    suffix = (
                        f" (+{len(branch.elements) - 5} more)" if len(branch.elements) > 5 else ""
                    )
                    branch_descriptions.append(f"{label}: {', '.join(examples)}{suffix}")

                branches_text = "; ".join(branch_descriptions)

                # Point to children: line if it exists, otherwise
                # the element name line itself.
                error_line = line_index.get(f"{elem_path}.children") or line_index.get(elem_path)

                errors.append(
                    ValidationError(
                        rule_id="choice.required-group-empty",
                        path=f"{elem_path}.children",
                        message=(
                            f"<{elem_name}> requires at least one child "
                            f"from a choice group but none are declared. "
                            f"Available: [{branches_text}]"
                        ),
                        severity=Severity.ERROR,
                        line=error_line,
                    )
                )

    return errors


# ------------------------------------------------------------------
# Incomplete branches — choice: declared but < 2 populated branches
# ------------------------------------------------------------------


def _check_incomplete_branches(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Emit an error when ``choice:`` is present in the YAML but has
    fewer than 2 branches with at least one child.  A choice with 0 or
    1 branches is meaningless — you need at least 2 alternatives.
    """
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        elem_path = f"profile.elements.{elem_name}"
        choice_path = f"{elem_path}.children.choice"

        # Detect whether choice: was declared in the YAML by checking
        # the line index — the model validator already extracted it.
        choice_line = line_index.get(choice_path)
        if choice_line is None:
            continue  # no choice: key in the YAML

        # Count exclusive children (each key is one exclusive option)
        num_choices = len(restriction.exclusive_children)
        if num_choices >= 2:
            continue  # valid

        if num_choices == 0:
            msg = (
                f"<{elem_name}> has a 'choice:' with no children. "
                f"Add at least 2 exclusive child elements."
            )
        else:
            msg = (
                f"<{elem_name}> has a 'choice:' with only {num_choices} child. "
                f"A choice requires at least 2 exclusive children."
            )

        errors.append(
            ValidationError(
                rule_id="choice.incomplete-branches",
                path=choice_path,
                message=msg,
                severity=Severity.ERROR,
                line=choice_line,
            )
        )

    return errors


# ------------------------------------------------------------------
# Exclusive choice — no mixing of XSD-exclusive branches in children
# ------------------------------------------------------------------


def _check_exclusive_branch_conflict(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Emit an error when ``children:`` (always-present children, NOT
    inside ``choice:``) contains elements from multiple branches of an
    exclusive ``xs:choice`` group.

    This fires when the author puts mutually-exclusive elements in
    ``children:`` directly instead of using ``choice:``.
    """
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not restriction.children:
            continue

        if not schema.has_element(elem_name):
            continue

        choice_groups = schema.get_choice_groups(elem_name)
        declared_children = set(restriction.children.keys())
        elem_path = f"profile.elements.{elem_name}"

        for cg in choice_groups:
            if not cg.exclusive:
                continue  # free-mix — no conflict possible

            # Which branches have members in *always-present* children?
            active_branches: list[tuple[str, frozenset[str]]] = []
            for branch in cg.branches:
                overlap = branch.elements & declared_children
                if overlap:
                    label = branch.label or branch.branch_id
                    active_branches.append((label, overlap))

            if len(active_branches) <= 1:
                continue

            first_label = active_branches[0][0]
            for conflict_label, conflict_elements in active_branches[1:]:
                conflict_child = sorted(conflict_elements)[0]
                child_path = f"{elem_path}.children.{conflict_child}"

                errors.append(
                    ValidationError(
                        rule_id="choice.exclusive-branch-conflict",
                        path=child_path,
                        message=(
                            f"<{elem_name}> has an exclusive choice group: "
                            f"'{first_label}' and '{conflict_label}' cannot "
                            f"both appear in children. Use 'choice:' to "
                            f"express exclusive branches. "
                            f"Conflicting: "
                            f"{', '.join(sorted(conflict_elements))}"
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(child_path),
                    )
                )

    return errors


# ------------------------------------------------------------------
# Branch contains invalid child
# ------------------------------------------------------------------


def _check_branch_invalid_child(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Every element in a ``choice:`` branch must be a valid XSD child
    of the parent element.
    """
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not restriction.exclusive_children:
            continue

        if not schema.has_element(elem_name):
            continue

        valid_children = set(schema.get_children(elem_name))
        elem_path = f"profile.elements.{elem_name}"

        for child_name in restriction.exclusive_children:
            if child_name not in valid_children:
                errors.append(
                    ValidationError(
                        rule_id="choice.branch-invalid-child",
                        path=f"{elem_path}.children.choice.{child_name}",
                        message=(
                            f"<{child_name}> is not a valid child of <{elem_name}> per the XSD."
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(f"{elem_path}.children.choice"),
                    )
                )

    return errors


# ------------------------------------------------------------------
# Branch overlap — child in multiple branches or in both children + branch
# ------------------------------------------------------------------


def _check_branch_overlap(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """A child element must not appear in both ``children:`` (always-present)
    and ``choice:`` (exclusive).

    Cross-branch overlap is impossible with a flat dict (keys are unique).
    """
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        if not restriction.exclusive_children:
            continue

        elem_path = f"profile.elements.{elem_name}"
        always_present = set(restriction.children.keys())

        for child_name in restriction.exclusive_children:
            if child_name in always_present:
                errors.append(
                    ValidationError(
                        rule_id="choice.branch-overlap",
                        path=f"{elem_path}.children.choice.{child_name}",
                        message=(
                            f"<{child_name}> appears in both 'children:' "
                            f"and 'choice:' of <{elem_name}>. "
                            f"An element cannot be both always-present "
                            f"and exclusive."
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(f"{elem_path}.children.choice"),
                    )
                )

    return errors
