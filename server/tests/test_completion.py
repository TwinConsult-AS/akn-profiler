"""Tests for the LSP completion handler logic.

These tests exercise the completion-related helpers and the context
resolver integration — they do **not** start a real LSP server.
"""

from __future__ import annotations

import pytest

from akn_profiler.validation.yaml_context import Scope, resolve_context
from akn_profiler.xsd.schema_loader import AknSchema


@pytest.fixture(scope="module")
def schema() -> AknSchema:
    return AknSchema.load()


# ------------------------------------------------------------------
# Integration: context → expected completions
# ------------------------------------------------------------------


class TestCompletionContextMapping:
    """Verify that different cursor positions yield the expected scope,
    which will drive the completion item generation."""

    FULL_DOC = (
        "profile:\n"  # 0
        '  name: "Test"\n'  # 1
        '  version: "1.0"\n'  # 2
        '  description: "A test profile"\n'  # 3
        "\n"  # 4
        "  documentTypes:\n"  # 5
        "    - act\n"  # 6
        "\n"  # 7
        "  elements:\n"  # 8
        "    akomaNtoso:\n"  # 9
        "      attributes:\n"  # 10
        "        language:\n"  # 11
        "          required: true\n"  # 12
        "          values:\n"  # 13
        "            - nb\n"  # 14
        "      children:\n"  # 15
        "        act:\n"  # 16
        "\n"  # 17
        "    act:\n"  # 18
        "      children:\n"  # 19
        "        meta:\n"  # 20
        "        body:\n"  # 21
        "      structure:\n"  # 22
        "        - chapter\n"  # 23
        "      \n"  # 24  ← blank line in element body
        "\n"  # 25
    )

    def test_profile_level(self) -> None:
        """Inside profile: block, should get PROFILE scope."""
        ctx = resolve_context(self.FULL_DOC, 4, 2)
        assert ctx.scope == Scope.PROFILE

    def test_document_types_list(self) -> None:
        """On a list item under documentTypes."""
        ctx = resolve_context(self.FULL_DOC, 6, 6)
        assert ctx.scope == Scope.DOCUMENT_TYPES

    def test_elements_level(self) -> None:
        """After the last element entry, needing a new element name."""
        ctx = resolve_context(self.FULL_DOC, 8, 4)
        assert ctx.scope == Scope.ELEMENTS

    def test_element_body(self) -> None:
        """Blank line inside element block at body indent."""
        ctx = resolve_context(self.FULL_DOC, 24, 6)
        assert ctx.scope == Scope.ELEMENT_BODY
        assert ctx.element_name == "act"

    def test_children_scope(self) -> None:
        """On a dict key under children."""
        ctx = resolve_context(self.FULL_DOC, 21, 10)
        assert ctx.scope == Scope.CHILDREN
        assert ctx.element_name == "act"

    def test_attribute_values_list(self) -> None:
        """On a list item under values."""
        ctx = resolve_context(self.FULL_DOC, 14, 14)
        assert ctx.scope == Scope.ATTRIBUTE_VALUES
        assert ctx.element_name == "akomaNtoso"
        assert ctx.attribute_name == "language"

    def test_structure_scope(self) -> None:
        """On a list item under structure."""
        ctx = resolve_context(self.FULL_DOC, 23, 10)
        assert ctx.scope == Scope.STRUCTURE
        assert ctx.element_name == "act"


class TestElementCompletionData:
    """Verify schema can provide data needed for completions."""

    def test_schema_provides_element_names(self, schema: AknSchema) -> None:
        names = schema.element_names()
        assert "act" in names
        assert "bill" in names
        assert "akomaNtoso" in names

    def test_schema_provides_children(self, schema: AknSchema) -> None:
        children = schema.get_children("act")
        assert len(children) > 0
        # act should have meta and body as children
        assert "meta" in children
        assert "body" in children

    def test_schema_provides_attributes(self, schema: AknSchema) -> None:
        attrs = schema.get_attributes("act")
        attr_names = [a.name for a in attrs]
        assert len(attr_names) > 0

    def test_schema_provides_doc_types(self, schema: AknSchema) -> None:
        doc_types = schema.get_children("akomaNtoso")
        assert "act" in doc_types
        assert "bill" in doc_types


class TestProfileNoteCompletion:
    """profileNote should be offered in element body scope."""

    DOC_WITH_ELEMENT = (
        "profile:\n"  # 0
        "  elements:\n"  # 1
        "    act:\n"  # 2
        "      \n"  # 3  ← blank line in element body
    )

    def test_element_body_includes_profile_note(self) -> None:
        ctx = resolve_context(self.DOC_WITH_ELEMENT, 3, 6)
        assert ctx.scope == Scope.ELEMENT_BODY
        # profileNote should be in the existing_keys exclusion path,
        # and offered by the completion handler since it's in
        # _ELEMENT_BODY_KEYS.
        assert "profileNote" not in ctx.existing_keys

    DOC_WITH_NOTE = (
        "profile:\n"  # 0
        "  elements:\n"  # 1
        "    act:\n"  # 2
        '      profileNote: "test"\n'  # 3
        "      \n"  # 4  ← blank line in element body
    )

    def test_profile_note_in_existing_keys(self) -> None:
        ctx = resolve_context(self.DOC_WITH_NOTE, 4, 6)
        assert ctx.scope == Scope.ELEMENT_BODY
        assert "profileNote" in ctx.existing_keys
