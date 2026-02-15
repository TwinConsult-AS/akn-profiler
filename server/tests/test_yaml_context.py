"""Tests for the YAML cursor-context resolver."""

from __future__ import annotations

from akn_profiler.validation.yaml_context import Scope, resolve_context

# ------------------------------------------------------------------
# Empty / minimal documents
# ------------------------------------------------------------------


class TestEmptyDocument:
    def test_empty_string(self) -> None:
        ctx = resolve_context("", 0, 0)
        assert ctx.scope == Scope.EMPTY

    def test_whitespace_only(self) -> None:
        ctx = resolve_context("   \n  \n", 0, 0)
        assert ctx.scope == Scope.EMPTY


class TestRootLevel:
    def test_bare_document(self) -> None:
        source = "something:\n  foo: bar\n"
        ctx = resolve_context(source, 0, 0)
        assert ctx.scope == Scope.ROOT

    def test_profile_key(self) -> None:
        source = "profile:\n"
        ctx = resolve_context(source, 0, 0)
        assert ctx.scope == Scope.PROFILE


# ------------------------------------------------------------------
# Profile level
# ------------------------------------------------------------------


class TestProfileScope:
    PROFILE_DOC = 'profile:\n  name: "Test"\n  version: "1.0"\n  description: "Desc"\n  \n'

    def test_inside_profile_block(self) -> None:
        ctx = resolve_context(self.PROFILE_DOC, 4, 2)
        assert ctx.scope == Scope.PROFILE

    def test_existing_keys_collected(self) -> None:
        ctx = resolve_context(self.PROFILE_DOC, 4, 2)
        assert "name" in ctx.existing_keys
        assert "version" in ctx.existing_keys
        assert "description" in ctx.existing_keys


# ------------------------------------------------------------------
# Document types
# ------------------------------------------------------------------


class TestDocumentTypes:
    DOC = "profile:\n  documentTypes:\n    - act\n    - \n"

    def test_scope_is_document_types(self) -> None:
        ctx = resolve_context(self.DOC, 3, 6)
        assert ctx.scope == Scope.DOCUMENT_TYPES

    def test_existing_list_items(self) -> None:
        ctx = resolve_context(self.DOC, 3, 6)
        assert "act" in ctx.existing_keys


# ------------------------------------------------------------------
# Elements
# ------------------------------------------------------------------


class TestElements:
    DOC = "profile:\n  elements:\n    act:\n      attributes:\n        name:\n          required: true\n    \n"

    def test_new_element_scope(self) -> None:
        ctx = resolve_context(self.DOC, 6, 4)
        assert ctx.scope == Scope.ELEMENTS

    def test_element_name_scope(self) -> None:
        ctx = resolve_context(self.DOC, 2, 4)
        assert ctx.scope == Scope.ELEMENT_NAME
        assert ctx.element_name == "act"


class TestElementBody:
    DOC = "profile:\n  elements:\n    bill:\n      attributes:\n        name:\n          required: true\n      \n"

    def test_element_body_scope(self) -> None:
        ctx = resolve_context(self.DOC, 6, 6)
        assert ctx.scope == Scope.ELEMENT_BODY
        assert ctx.element_name == "bill"

    def test_existing_body_keys(self) -> None:
        ctx = resolve_context(self.DOC, 6, 6)
        assert "attributes" in ctx.existing_keys


# ------------------------------------------------------------------
# Attributes
# ------------------------------------------------------------------


class TestAttributes:
    DOC = (
        "profile:\n"
        "  elements:\n"
        "    act:\n"
        "      attributes:\n"
        "        name:\n"
        "          required: true\n"
        "        \n"
    )

    def test_new_attribute_scope(self) -> None:
        ctx = resolve_context(self.DOC, 6, 8)
        assert ctx.scope == Scope.ATTRIBUTES
        assert ctx.element_name == "act"

    def test_attribute_name_scope(self) -> None:
        ctx = resolve_context(self.DOC, 4, 8)
        assert ctx.scope == Scope.ATTRIBUTE_NAME
        assert ctx.element_name == "act"
        assert ctx.attribute_name == "name"

    def test_attribute_body_scope(self) -> None:
        ctx = resolve_context(self.DOC, 5, 10)
        assert ctx.scope == Scope.ATTRIBUTE_BODY
        assert ctx.element_name == "act"
        assert ctx.attribute_name == "name"


class TestAttributeValues:
    DOC = (
        "profile:\n"
        "  elements:\n"
        "    act:\n"
        "      attributes:\n"
        "        language:\n"
        "          required: true\n"
        "          values:\n"
        "            - nb\n"
        "            - \n"
    )

    def test_attribute_values_scope(self) -> None:
        ctx = resolve_context(self.DOC, 8, 14)
        assert ctx.scope == Scope.ATTRIBUTE_VALUES
        assert ctx.element_name == "act"
        assert ctx.attribute_name == "language"


# ------------------------------------------------------------------
# Children & Structure
# ------------------------------------------------------------------


class TestChildren:
    DOC = "profile:\n  elements:\n    act:\n      children:\n        meta:\n        \n"

    def test_children_scope(self) -> None:
        ctx = resolve_context(self.DOC, 5, 10)
        assert ctx.scope == Scope.CHILDREN
        assert ctx.element_name == "act"


class TestChoiceBranches:
    DOC = (
        "profile:\n"
        "  elements:\n"
        "    body:\n"
        "      children:\n"
        "        choice:\n"
        "          section:\n"
        "          \n"
    )

    def test_inside_choice_block(self) -> None:
        ctx = resolve_context(self.DOC, 6, 10)
        assert ctx.scope == Scope.CHOICE_BRANCHES
        assert ctx.element_name == "body"

    def test_on_choice_key_line(self) -> None:
        ctx = resolve_context(self.DOC, 4, 10)
        assert ctx.scope == Scope.CHOICE_BRANCHES
        assert ctx.element_name == "body"

    def test_children_scope_not_choice(self) -> None:
        """Lines under children: but NOT under choice: stay CHILDREN."""
        doc = "profile:\n  elements:\n    act:\n      children:\n        meta:\n"
        ctx = resolve_context(doc, 4, 10)
        assert ctx.scope == Scope.CHILDREN
        assert ctx.element_name == "act"


class TestStructure:
    DOC = "profile:\n  elements:\n    body:\n      structure:\n        - chapter\n        - \n"

    def test_structure_scope(self) -> None:
        ctx = resolve_context(self.DOC, 5, 10)
        assert ctx.scope == Scope.STRUCTURE
        assert ctx.element_name == "body"


# ------------------------------------------------------------------
# (Metadata tests removed — metadata section no longer exists)
# ------------------------------------------------------------------
