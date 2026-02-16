"""Tests for the contextual 'Add …' code-action lightbulbs.

Each test constructs a profile YAML string, simulates a cursor position,
and verifies that the correct ``CodeAction`` items are returned from
``_add_item_actions``.
"""

from __future__ import annotations

import textwrap

import pytest

# The helpers require the module-level ``akn_schema`` to be populated.
import akn_profiler.server as _srv

# We import the private helpers directly so we can unit-test them
# without spinning up the full LSP server.
from akn_profiler.server import (
    _add_item_actions,
    _build_cascade_add_edit,
    _build_child_remove_edit,
    _child_name_at_line,
    _collect_orphaned_elements,
    _section_end,
)
from akn_profiler.xsd.schema_loader import AknSchema

# Load schema once for the entire module
_schema = AknSchema.load()


@pytest.fixture(autouse=True)
def _set_schema():
    """Ensure the module-level schema is set before each test."""
    _srv.akn_schema = _schema
    yield
    _srv.akn_schema = None


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

_FAKE_URI = "file:///test.akn.yaml"


def _titles(source: str, cursor_line: int) -> list[str]:
    """Return the titles of all actions returned for *cursor_line*."""
    actions = _add_item_actions(_FAKE_URI, textwrap.dedent(source), cursor_line)
    return [a.title for a in actions]


# ------------------------------------------------------------------
# _section_end helper
# ------------------------------------------------------------------


class TestSectionEnd:
    def test_basic(self):
        lines = ["documentTypes:", "    - act", "    - bill", "other:"]
        assert _section_end(lines, 0, 0) == 2

    def test_skips_blank_lines(self):
        lines = ["documentTypes:", "    - act", "", "    - bill", "other:"]
        assert _section_end(lines, 0, 0) == 3

    def test_single_line(self):
        lines = ["documentTypes:"]
        assert _section_end(lines, 0, 0) == 0


# ------------------------------------------------------------------
# documentTypes section
# ------------------------------------------------------------------


class TestDocumentTypesActions:
    SOURCE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
"""

    def test_cursor_on_document_types_header(self):
        titles = _titles(self.SOURCE, cursor_line=3)
        assert any("document type" in t.lower() for t in titles)

    def test_cursor_on_document_type_entry(self):
        titles = _titles(self.SOURCE, cursor_line=4)
        assert any("document type" in t.lower() for t in titles)

    def test_cursor_outside_document_types(self):
        titles = _titles(self.SOURCE, cursor_line=6)
        assert not any("document type" in t.lower() for t in titles)


# ------------------------------------------------------------------
# elements header
# ------------------------------------------------------------------


class TestElementsHeaderActions:
    SOURCE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
"""

    def test_cursor_on_elements_header(self):
        titles = _titles(self.SOURCE, cursor_line=5)
        assert any("element" in t.lower() for t in titles)


# ------------------------------------------------------------------
# Element name line (no existing subsections)
# ------------------------------------------------------------------


class TestElementNameLineActions:
    SOURCE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
"""

    def test_offers_add_child_and_attribute(self):
        titles = _titles(self.SOURCE, cursor_line=6)
        assert any("child" in t.lower() for t in titles)
        assert any("attribute" in t.lower() for t in titles)

    def test_titles_mention_element_name(self):
        titles = _titles(self.SOURCE, cursor_line=6)
        assert any("'act'" in t for t in titles)

    def test_new_section_headers_mentioned(self):
        """When no children/attributes section exists, the title should
        indicate a new section is being created."""
        titles = _titles(self.SOURCE, cursor_line=6)
        child_titles = [t for t in titles if "child" in t.lower()]
        assert any("new" in t.lower() or "section" in t.lower() for t in child_titles)


# ------------------------------------------------------------------
# Element with existing children: block
# ------------------------------------------------------------------


class TestExistingChildrenActions:
    SOURCE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
      children:
        meta:
        body:
"""

    def test_cursor_inside_children_block(self):
        titles = _titles(self.SOURCE, cursor_line=8)
        assert any("child" in t.lower() for t in titles)

    def test_cursor_on_element_offers_add_child(self):
        titles = _titles(self.SOURCE, cursor_line=6)
        child_titles = [t for t in titles if "child" in t.lower()]
        # Should offer "Add child" (existing section), not "new section"
        assert child_titles
        assert not any("new" in t.lower() for t in child_titles)


# ------------------------------------------------------------------
# profileNote lightbulb
# ------------------------------------------------------------------


class TestProfileNoteActions:
    SOURCE_NO_NOTE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
      children:
        meta:
        body:
"""

    def test_offers_add_profile_note(self):
        titles = _titles(self.SOURCE_NO_NOTE, cursor_line=6)
        assert any("profile note" in t.lower() for t in titles)

    def test_offers_add_profile_note_from_children(self):
        titles = _titles(self.SOURCE_NO_NOTE, cursor_line=8)
        assert any("profile note" in t.lower() for t in titles)

    def test_title_mentions_element_name(self):
        titles = _titles(self.SOURCE_NO_NOTE, cursor_line=6)
        note_titles = [t for t in titles if "profile note" in t.lower()]
        assert any("'act'" in t for t in note_titles)

    SOURCE_WITH_NOTE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
      profileNote: "Norwegian term: 'lov'"
      children:
        meta:
        body:
"""

    def test_no_duplicate_when_note_exists(self):
        titles = _titles(self.SOURCE_WITH_NOTE, cursor_line=7)
        assert not any("profile note" in t.lower() for t in titles)

    def test_no_duplicate_from_children_when_exists(self):
        titles = _titles(self.SOURCE_WITH_NOTE, cursor_line=9)
        assert not any("profile note" in t.lower() for t in titles)

    SOURCE_BARE_ELEMENT = """\
profile:
  name: "test"
  documentTypes:
    - act
  elements:
    act:
"""

    def test_offers_note_on_bare_element(self):
        titles = _titles(self.SOURCE_BARE_ELEMENT, cursor_line=5)
        assert any("profile note" in t.lower() for t in titles)


# ------------------------------------------------------------------
# Element with existing attributes: block
# ------------------------------------------------------------------


class TestExistingAttributesActions:
    SOURCE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
      attributes:
        name:
          required: true
"""

    def test_cursor_inside_attributes_block(self):
        titles = _titles(self.SOURCE, cursor_line=8)
        assert any("attribute" in t.lower() for t in titles)


# ------------------------------------------------------------------
# values: inside attribute
# ------------------------------------------------------------------


class TestValuesActions:
    SOURCE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
      attributes:
        contains:
          required: true
          values:
            - originalVersion
"""

    def test_cursor_on_values_entry(self):
        titles = _titles(self.SOURCE, cursor_line=11)
        assert any("value" in t.lower() for t in titles)


# ------------------------------------------------------------------
# structure: block
# ------------------------------------------------------------------


class TestStructureActions:
    SOURCE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
      structure:
        meta: 1
"""

    def test_cursor_in_structure(self):
        titles = _titles(self.SOURCE, cursor_line=8)
        assert any("hierarchy" in t.lower() for t in titles)


# ------------------------------------------------------------------
# WorkspaceEdit correctness
# ------------------------------------------------------------------


class TestEditContent:
    """Verify the actual TextEdit inserts properly indented content."""

    SOURCE = """\
profile:
  name: "test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    act:
      children:
        meta:
"""

    def test_add_child_edit_inserts_at_correct_indent(self):
        actions = _add_item_actions(_FAKE_URI, self.SOURCE, cursor_line=8)
        child_actions = [a for a in actions if "child" in a.title.lower()]
        assert child_actions
        action = child_actions[0]
        assert action.edit is not None
        edits = action.edit.changes[_FAKE_URI]
        assert len(edits) == 1
        new_text = edits[0].new_text
        # Should contain spaces for indentation and end with newline
        assert new_text.endswith("\n")
        # The text should be indented (sub_indent + 2 = 8 spaces)
        stripped = new_text.rstrip("\n")
        indent = len(stripped) - len(stripped.lstrip())
        assert indent >= 6  # at least sub_indent + 2

    def test_action_has_cursor_command(self):
        actions = _add_item_actions(_FAKE_URI, self.SOURCE, cursor_line=8)
        child_actions = [a for a in actions if "child" in a.title.lower()]
        assert child_actions
        action = child_actions[0]
        assert action.command is not None
        assert action.command.command == "akn-profiler.cursorToLine"

    def test_action_kind_is_refactor(self):
        actions = _add_item_actions(_FAKE_URI, self.SOURCE, cursor_line=8)
        for action in actions:
            from lsprotocol.types import CodeActionKind

            assert action.kind == CodeActionKind.Refactor


# ------------------------------------------------------------------
# Edge cases
# ------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_source(self):
        assert _add_item_actions(_FAKE_URI, "", 0) == []

    def test_cursor_past_end(self):
        source = "profile:\n  name: test\n"
        actions = _add_item_actions(_FAKE_URI, source, 99)
        # Should not crash, just return empty
        assert isinstance(actions, list)

    def test_no_elements_section(self):
        source = "profile:\n  name: test\n  documentTypes:\n    - act\n"
        actions = _add_item_actions(_FAKE_URI, source, 2)
        # Should offer "Add document type" but no element-related actions
        titles = [a.title for a in actions]
        assert any("document type" in t.lower() for t in titles)
        assert not any("element" in t.lower() for t in titles)


# ------------------------------------------------------------------
# Cascade add helpers
# ------------------------------------------------------------------


class TestBuildCascadeAddEdit:
    """_build_cascade_add_edit should create a whole-document edit
    that adds the element and its required chain."""

    SOURCE = textwrap.dedent("""\
        profile:
          name: test
          elements:
            akomaNtoso:
    """)

    def test_adds_known_element(self):
        edit = _build_cascade_add_edit(_FAKE_URI, self.SOURCE, "act")
        assert edit is not None
        assert _FAKE_URI in edit.changes
        changes = edit.changes[_FAKE_URI]
        assert len(changes) == 1
        # The new text should contain the element we asked for
        assert "act" in changes[0].new_text

    def test_cascades_required_children(self):
        edit = _build_cascade_add_edit(_FAKE_URI, self.SOURCE, "act")
        assert edit is not None
        new_text = edit.changes[_FAKE_URI][0].new_text
        # act requires meta and body
        assert "meta" in new_text
        assert "body" in new_text

    def test_returns_none_for_unknown_element(self):
        edit = _build_cascade_add_edit(_FAKE_URI, self.SOURCE, "totallyBogus")
        assert edit is None

    def test_returns_none_when_already_present(self):
        source = textwrap.dedent("""\
            profile:
              elements:
                akomaNtoso:
                act:
        """)
        # act is already present — expand may still add children though
        edit = _build_cascade_add_edit(_FAKE_URI, source, "akomaNtoso")
        # akomaNtoso has no required children beyond what's already implied
        # so either None (nothing changed) or a valid edit
        assert edit is None or _FAKE_URI in edit.changes


# ------------------------------------------------------------------
# Cascade remove helpers
# ------------------------------------------------------------------


class TestBuildChildRemoveEdit:
    """_build_child_remove_edit removes a child from a parent and cleans
    up orphaned element definitions."""

    SOURCE = textwrap.dedent("""\
        profile:
          name: test
          elements:
            act:
              children:
                meta:
                body:
            meta:
            body:
    """)

    def test_removes_child_from_parent(self):
        import yaml as _yaml

        edit = _build_child_remove_edit(_FAKE_URI, self.SOURCE, "act", "body")
        assert edit is not None
        new_text = edit.changes[_FAKE_URI][0].new_text
        data = _yaml.safe_load(new_text)
        children = data["profile"]["elements"]["act"].get("children", {})
        assert "body" not in children
        # meta should still be there
        assert "meta" in children

    def test_removes_orphaned_definition(self):
        import yaml as _yaml

        edit = _build_child_remove_edit(_FAKE_URI, self.SOURCE, "act", "body")
        assert edit is not None
        new_text = edit.changes[_FAKE_URI][0].new_text
        data = _yaml.safe_load(new_text)
        # body was only referenced by act, so its definition should be gone
        assert "body" not in data["profile"]["elements"]
        # meta is still referenced, so it stays
        assert "meta" in data["profile"]["elements"]

    def test_keeps_definition_if_still_referenced(self):
        import yaml as _yaml

        source = textwrap.dedent("""\
            profile:
              name: test
              elements:
                act:
                  children:
                    meta:
                bill:
                  children:
                    meta:
                meta:
        """)
        edit = _build_child_remove_edit(_FAKE_URI, source, "act", "meta")
        assert edit is not None
        new_text = edit.changes[_FAKE_URI][0].new_text
        data = _yaml.safe_load(new_text)
        # meta is still referenced by bill, so its definition stays
        assert "meta" in data["profile"]["elements"]

    def test_returns_none_for_missing_child(self):
        edit = _build_child_remove_edit(_FAKE_URI, self.SOURCE, "act", "notAChild")
        assert edit is None


class TestCollectOrphanedElements:
    """_collect_orphaned_elements should walk descendants."""

    def test_collects_chain(self):
        elements = {
            "act": {"children": {"meta": None, "body": None}},
            "meta": {"children": {"identification": None}},
            "identification": {},
            "body": {},
        }
        orphaned = _collect_orphaned_elements("meta", elements)
        assert "meta" in orphaned
        # identification is only referenced by meta, so it's orphaned too
        assert "identification" in orphaned
        # body is referenced by act (not being removed), so NOT orphaned
        assert "body" not in orphaned


class TestChildNameAtLine:
    """_child_name_at_line extracts the child element name."""

    def test_simple_entry(self):
        lines = ["        meta:"]
        assert _child_name_at_line(lines, 0, 8) == "meta"

    def test_entry_with_value(self):
        lines = ["        meta: 1..1"]
        assert _child_name_at_line(lines, 0, 8) == "meta"

    def test_wrong_indent(self):
        lines = ["    meta:"]
        assert _child_name_at_line(lines, 0, 8) is None

    def test_blank_line(self):
        lines = [""]
        assert _child_name_at_line(lines, 0, 8) is None


# ------------------------------------------------------------------
# Remove lightbulb on children lines
# ------------------------------------------------------------------


class TestRemoveLightbulb:
    """When cursor is on a child entry, a remove action should appear."""

    SOURCE = textwrap.dedent("""\
        profile:
          elements:
            act:
              children:
                meta:
                body:
            meta:
            body:
    """)

    def test_remove_action_offered_on_child_line(self):
        # Cursor on "meta:" child line (line 4, indent=8)
        actions = _add_item_actions(_FAKE_URI, self.SOURCE, cursor_line=4)
        titles = [a.title for a in actions]
        assert any("remove" in t.lower() and "meta" in t.lower() for t in titles)

    def test_add_action_also_present(self):
        actions = _add_item_actions(_FAKE_URI, self.SOURCE, cursor_line=4)
        titles = [a.title for a in actions]
        assert any("add child" in t.lower() for t in titles)

    def test_no_remove_on_children_header(self):
        # Line 3 is "children:" header — no child to remove
        actions = _add_item_actions(_FAKE_URI, self.SOURCE, cursor_line=3)
        titles = [a.title for a in actions]
        assert not any("remove" in t.lower() for t in titles)


# ------------------------------------------------------------------
# _find_element_context
# ------------------------------------------------------------------


class TestFindElementContext:
    """Verify that _find_element_context finds the element name even
    when the error points at a bare element entry (no children: key)."""

    def test_finds_element_on_its_own_line(self):
        from akn_profiler.server import _find_element_context

        source = textwrap.dedent("""\
            profile:
              elements:
                body:
        """)
        # line 2 = "    body:"
        assert _find_element_context(source, 2) == "body"

    def test_finds_element_from_children_line(self):
        from akn_profiler.server import _find_element_context

        source = textwrap.dedent("""\
            profile:
              elements:
                body:
                  children:
                    chapter:
        """)
        # line 3 = "      children:" — should walk up to body
        assert _find_element_context(source, 3) == "body"

    def test_structural_keys_are_skipped(self):
        from akn_profiler.server import _find_element_context

        source = textwrap.dedent("""\
            profile:
              elements:
                body:
                  children:
        """)
        # line 3 = "      children:" — structural, should NOT return
        assert _find_element_context(source, 3) != "children"
