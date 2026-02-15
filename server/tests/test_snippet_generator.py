"""Tests for the snippet scaffold generator."""

from __future__ import annotations

import pytest

from akn_profiler.models.snippet_generator import generate_snippet, get_document_types
from akn_profiler.xsd.schema_loader import AknSchema


@pytest.fixture(scope="module")
def schema() -> AknSchema:
    return AknSchema.load()


class TestGetDocumentTypes:
    def test_returns_non_empty_list(self, schema: AknSchema) -> None:
        types = get_document_types(schema)
        assert isinstance(types, list)
        assert len(types) > 0

    def test_includes_act_and_bill(self, schema: AknSchema) -> None:
        types = get_document_types(schema)
        assert "act" in types
        assert "bill" in types


class TestGenerateSnippet:
    def test_returns_string(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "act")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_contains_profile_key(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "act")
        assert "profile:" in result

    def test_contains_tab_stops(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "act")
        assert "${1:" in result
        assert "${2:" in result
        assert "${3:" in result

    def test_contains_doc_type(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "bill")
        assert "- bill" in result

    def test_contains_final_cursor(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "act")
        assert "$0" in result

    def test_contains_elements_section(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "act")
        assert "elements:" in result

    def test_contains_document_types_key(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "act")
        assert "documentTypes:" in result

    def test_contains_document_types_section(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "act")
        assert "documentTypes:" in result

    def test_invalid_doc_type_raises(self, schema: AknSchema) -> None:
        with pytest.raises(ValueError):
            generate_snippet(schema, "nonexistent")

    def test_contains_akomantoso(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "act")
        assert "akomaNtoso:" in result

    def test_minimal_scaffold_no_element_details(self, schema: AknSchema) -> None:
        """The snippet should NOT contain element details like children/attributes.
        The cascade system adds those via diagnostics + quick-fixes."""
        result = generate_snippet(schema, "act")
        assert "children:" not in result
        assert "attributes:" not in result
        assert "required:" not in result

    def test_bill_snippet_has_bill_not_act(self, schema: AknSchema) -> None:
        result = generate_snippet(schema, "bill")
        assert "- bill" in result
        assert "- act" not in result
        assert "akomaNtoso:" in result
