"""
Rule category 1 — **Vocabulary rules** (XSD Declarations).

Checks that every name used in the profile — element names, attribute
names, document types — actually exists in the AKN XSD.  Also flags
cardinality mismatches (e.g. marking something ``required`` that does
not exist).

All checks are dynamic: the only source of truth is ``AknSchema``,
nothing is hard-coded.
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
    errors.extend(_check_document_types(profile, schema, line_index))
    errors.extend(_check_elements(profile, schema, line_index))
    return errors


# ------------------------------------------------------------------
# Document types
# ------------------------------------------------------------------


def _check_document_types(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Every ``documentTypes`` entry must be a child of ``<akomaNtoso>``."""
    errors: list[ValidationError] = []
    valid_doc_types = set(schema.get_children("akomaNtoso"))

    for i, dt in enumerate(profile.documentTypes):
        path = f"profile.documentTypes[{i}]"
        if dt not in valid_doc_types:
            errors.append(
                ValidationError(
                    rule_id="vocabulary.unknown-document-type",
                    path=path,
                    message=(
                        f"'{dt}' is not a valid AKN document type. "
                        f"Valid types: {sorted(valid_doc_types)}"
                    ),
                    severity=Severity.ERROR,
                    line=line_index.get(path),
                )
            )
    return errors


# ------------------------------------------------------------------
# Elements and their attributes
# ------------------------------------------------------------------


def _check_elements(
    profile: ProfileDocument,
    schema: AknSchema,
    line_index: LineIndex,
) -> list[ValidationError]:
    """Every element and attribute name must exist in the XSD."""
    errors: list[ValidationError] = []

    for elem_name, restriction in profile.elements.items():
        elem_path = f"profile.elements.{elem_name}"

        # --- Does the element itself exist? -------------------------
        if not schema.has_element(elem_name):
            errors.append(
                ValidationError(
                    rule_id="vocabulary.unknown-element",
                    path=elem_path,
                    message=f"'{elem_name}' is not a known AKN element",
                    severity=Severity.ERROR,
                    line=line_index.get(elem_path),
                )
            )
            # Skip attribute / child checks — the element doesn't exist
            continue

        # --- Do the listed attributes exist on this element? --------
        known_attrs = {a.name for a in schema.get_attributes(elem_name)}

        for attr_name in restriction.attributes:
            attr_path = f"{elem_path}.attributes.{attr_name}"
            if attr_name not in known_attrs:
                errors.append(
                    ValidationError(
                        rule_id="vocabulary.unknown-attribute",
                        path=attr_path,
                        message=(
                            f"'{attr_name}' is not a valid attribute "
                            f"on <{elem_name}>. "
                            f"Known attributes: {sorted(known_attrs)}"
                        ),
                        severity=Severity.ERROR,
                        line=line_index.get(attr_path),
                    )
                )

        # --- Do the listed children exist as children of this elem? -
        known_children = set(schema.get_children(elem_name))

        for child_name in restriction.children:
            child_path = f"{elem_path}.children.{child_name}"
            # First check: is it even a known element?
            if not schema.has_element(child_name):
                errors.append(
                    ValidationError(
                        rule_id="vocabulary.unknown-element",
                        path=child_path,
                        message=f"'{child_name}' is not a known AKN element",
                        severity=Severity.ERROR,
                        line=line_index.get(child_path),
                    )
                )
            elif child_name not in known_children:
                # It exists in the XSD but is not a valid child here.
                # This is a *structure* error — but we flag the
                # vocabulary aspect (existence) here, structure rules
                # handle containment.
                pass  # Handled by rules_structure

        # --- Do the structure entries exist? -------------------------
        for i, struct_name in enumerate(restriction.structure):
            struct_path = f"{elem_path}.structure[{i}]"
            if not schema.has_element(struct_name):
                errors.append(
                    ValidationError(
                        rule_id="vocabulary.unknown-element",
                        path=struct_path,
                        message=(f"'{struct_name}' is not a known AKN element"),
                        severity=Severity.ERROR,
                        line=line_index.get(struct_path),
                    )
                )

    return errors
