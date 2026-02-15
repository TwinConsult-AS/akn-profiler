"""Tests for CodeLens handler and initializeProfile command."""

from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock, patch

import pytest
import yaml
from lsprotocol.types import CodeLensParams, TextDocumentIdentifier

import akn_profiler.server as _srv
from akn_profiler.server import cmd_initialize_profile, code_lens
from akn_profiler.xsd.schema_loader import AknSchema

_schema = AknSchema.load()
_FAKE_URI = "file:///test.akn.yaml"


@pytest.fixture(autouse=True)
def _set_schema():
    _srv.akn_schema = _schema
    yield
    _srv.akn_schema = None


def _get_lenses(source: str):
    """Return CodeLens items for the given *source* text."""
    doc = MagicMock()
    doc.source = source
    mock_ws = MagicMock()
    mock_ws.get_text_document.return_value = doc
    params = CodeLensParams(text_document=TextDocumentIdentifier(uri=_FAKE_URI))
    with patch.object(
        type(_srv.server), "workspace", new_callable=PropertyMock, return_value=mock_ws
    ):
        return code_lens(params)


class TestEmptyFile:
    def test_empty_file_shows_scaffold_lens(self):
        lenses = _get_lenses("")
        assert len(lenses) == 1
        assert lenses[0].command.title == "Initialize Profile Scaffold"
        assert lenses[0].command.command == "akn-profiler.insertScaffold"

    def test_whitespace_only_shows_scaffold_lens(self):
        lenses = _get_lenses("   \n\n  ")
        assert len(lenses) == 1
        assert lenses[0].command.command == "akn-profiler.insertScaffold"


class TestNonEmpty:
    def test_non_empty_no_lens(self):
        lenses = _get_lenses("profile:\n  name: test\n")
        assert len(lenses) == 0

    def test_random_content_no_lens(self):
        lenses = _get_lenses("some random content\n")
        assert len(lenses) == 0


# ------------------------------------------------------------------
# cmd_initialize_profile
# ------------------------------------------------------------------


class TestInitializeProfile:
    def test_returns_valid_yaml(self):
        result = cmd_initialize_profile("act")
        assert result
        parsed = yaml.safe_load(result)
        assert "profile" in parsed

    def test_contains_selected_doctype(self):
        result = cmd_initialize_profile("act")
        parsed = yaml.safe_load(result)
        assert "act" in parsed["profile"]["documentTypes"]

    def test_contains_akomantoso(self):
        result = cmd_initialize_profile("act")
        parsed = yaml.safe_load(result)
        assert "akomaNtoso" in parsed["profile"]["elements"]

    def test_contains_doctype_element(self):
        result = cmd_initialize_profile("act")
        parsed = yaml.safe_load(result)
        assert "act" in parsed["profile"]["elements"]

    def test_has_required_children_of_doctype(self):
        """The selected doc type's required children should be present."""
        result = cmd_initialize_profile("act")
        parsed = yaml.safe_load(result)
        elements = parsed["profile"]["elements"]
        # 'act' requires 'meta' and 'body' (at minimum)
        assert "meta" in elements
        assert "body" in elements

    def test_bill_doctype(self):
        result = cmd_initialize_profile("bill")
        parsed = yaml.safe_load(result)
        assert "bill" in parsed["profile"]["documentTypes"]
        assert "bill" in parsed["profile"]["elements"]

    def test_no_schema_returns_empty(self):
        _srv.akn_schema = None
        result = cmd_initialize_profile("act")
        assert result == ""
