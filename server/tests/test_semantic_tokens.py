"""Tests for semantic token generation.

Verifies that _build_semantic_tokens assigns the correct token types
to each kind of YAML construct:
    0 = Class           — element definitions
    1 = Property        — attribute names
    2 = Keyword         — structural/profile keys
    3 = EnumMember      — document types, enum values
    4 = Variable        — (unused)
    5 = Type            — child/choice/structure element references
    6 = String          — cardinality values
    7 = Macro           — boolean true/false
"""

import pytest

import akn_profiler.server as _srv
from akn_profiler.xsd.schema_loader import AknSchema

_schema = AknSchema.load()


@pytest.fixture(autouse=True)
def _ensure_schema():
    """Ensure the module-level schema is set for every test."""
    _srv.akn_schema = _schema
    yield


def _decode_tokens(data: list[int]) -> list[tuple[int, int, int, int, int]]:
    """Decode LSP delta-encoded tokens back to (line, col, len, type, mod)."""
    tokens = []
    line = 0
    col = 0
    for i in range(0, len(data), 5):
        d_line, d_col, length, token_type, mod = data[i : i + 5]
        line += d_line
        col = d_col if d_line > 0 else col + d_col
        tokens.append((line, col, length, token_type, mod))
    return tokens


def _tokens_for(source: str) -> list[tuple[int, int, int, int, int]]:
    """Return decoded tokens for *source*."""
    return _decode_tokens(_srv._build_semantic_tokens(source))


def _find_token(tokens, line, col):
    """Find a token at a given line/col (0-indexed)."""
    for t in tokens:
        if t[0] == line and t[1] == col:
            return t
    return None


# ------------------------------------------------------------------
# Structural keys — Keyword (type 2)
# ------------------------------------------------------------------


class TestStructuralKeys:
    """Top-level profile keys and element-body keys should be Keyword."""

    SOURCE = """\
profile:
  name: MyProfile
  version: "1.0"
  description: A test
  documentTypes:
    - act
  elements:
    act:
      profileNote: "Some note"
      attributes:
        name:
          required: true
      children:
        meta: "1..1"
      structure:
        - body
"""

    def test_profile_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 0, 0)
        assert t is not None and t[3] == 2  # Keyword

    def test_name_top_level_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 1, 2)
        assert t is not None and t[3] == 2

    def test_version_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 2, 2)
        assert t is not None and t[3] == 2

    def test_description_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 3, 2)
        assert t is not None and t[3] == 2

    def test_documentTypes_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 4, 2)
        assert t is not None and t[3] == 2

    def test_elements_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 6, 2)
        assert t is not None and t[3] == 2

    def test_profileNote_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 8, 6)
        assert t is not None and t[3] == 2

    def test_attributes_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 9, 6)
        assert t is not None and t[3] == 2

    def test_children_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 12, 6)
        assert t is not None and t[3] == 2

    def test_structure_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 14, 6)
        assert t is not None and t[3] == 2

    def test_required_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 11, 10)
        assert t is not None and t[3] == 2


# ------------------------------------------------------------------
# Attribute names — Property (type 1), even if name clashes
# ------------------------------------------------------------------


class TestAttributeNames:
    """Attribute names under attributes: must be Property, not Keyword."""

    SOURCE = """\
profile:
  elements:
    act:
      attributes:
        name:
          required: true
        contains:
          required: false
        version:
"""

    def test_name_attr_is_property(self):
        """'name' is in _STRUCTURAL_KEYS but under attributes: → Property."""
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 4, 8)
        assert t is not None and t[3] == 1  # Property

    def test_contains_attr_is_property(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 6, 8)
        assert t is not None and t[3] == 1

    def test_version_attr_is_property(self):
        """'version' is in _STRUCTURAL_KEYS but under attributes: → Property."""
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 8, 8)
        assert t is not None and t[3] == 1

    def test_required_under_attr_stays_keyword(self):
        """required: under an attribute body should still be Keyword."""
        tokens = _tokens_for(self.SOURCE)
        # required at line 5 col 10
        t = _find_token(tokens, 5, 10)
        assert t is not None and t[3] == 2  # Keyword


# ------------------------------------------------------------------
# Element definitions — Class (type 0)
# ------------------------------------------------------------------


class TestElementDefinitions:
    """Top-level element names under elements: should be Class."""

    SOURCE = """\
profile:
  elements:
    act:
    meta:
    body:
"""

    def test_act_is_class(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 2, 4)
        assert t is not None and t[3] == 0

    def test_meta_is_class(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 3, 4)
        assert t is not None and t[3] == 0


# ------------------------------------------------------------------
# Child references — Type (type 5) + cardinality
# ------------------------------------------------------------------


class TestChildReferences:
    """Element names under children: should be Type, with cardinality."""

    SOURCE = """\
profile:
  elements:
    act:
      children:
        meta: "1..1"
        body: "0..*"
"""

    def test_child_meta_is_type(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 4, 8)
        assert t is not None and t[3] == 5  # Type

    def test_child_body_is_type(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 5, 8)
        assert t is not None and t[3] == 5

    def test_cardinality_is_string(self):
        tokens = _tokens_for(self.SOURCE)
        # Find the cardinality token on line 4
        card_tokens = [t for t in tokens if t[0] == 4 and t[3] == 6]
        assert len(card_tokens) == 1
        assert card_tokens[0][2] == 4  # "1..1" → length 4


# ------------------------------------------------------------------
# Choice branch elements — Type (type 5)
# ------------------------------------------------------------------


class TestChoiceBranches:
    """Element names under choice: should be Type with cardinality."""

    SOURCE = """\
profile:
  elements:
    act:
      children:
        choice:
          preface: "0..1"
          preamble: "0..1"
"""

    def test_choice_key_is_keyword(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 4, 8)
        assert t is not None and t[3] == 2  # Keyword

    def test_preface_in_choice_is_type(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 5, 10)
        assert t is not None and t[3] == 5  # Type

    def test_preamble_in_choice_is_type(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 6, 10)
        assert t is not None and t[3] == 5

    def test_cardinality_in_choice(self):
        tokens = _tokens_for(self.SOURCE)
        card_tokens = [t for t in tokens if t[0] == 5 and t[3] == 6]
        assert len(card_tokens) == 1


# ------------------------------------------------------------------
# Boolean values — Macro (type 7)
# ------------------------------------------------------------------


class TestBooleanValues:
    """true/false on required: lines should be Macro."""

    SOURCE = """\
profile:
  elements:
    act:
      attributes:
        name:
          required: true
        contains:
          required: false
"""

    def test_true_is_macro(self):
        tokens = _tokens_for(self.SOURCE)
        macro_tokens = [t for t in tokens if t[0] == 5 and t[3] == 7]
        assert len(macro_tokens) == 1

    def test_false_is_macro(self):
        tokens = _tokens_for(self.SOURCE)
        macro_tokens = [t for t in tokens if t[0] == 7 and t[3] == 7]
        assert len(macro_tokens) == 1


# ------------------------------------------------------------------
# Document types — EnumMember (type 3)
# ------------------------------------------------------------------


class TestDocumentTypes:
    """Document-type list items should be EnumMember."""

    SOURCE = """\
profile:
  documentTypes:
    - act
    - bill
"""

    def test_act_doctype_is_enum(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 2, 6)
        assert t is not None and t[3] == 3  # EnumMember

    def test_bill_doctype_is_enum(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 3, 6)
        assert t is not None and t[3] == 3


# ------------------------------------------------------------------
# Structure list items — Type (type 5)
# ------------------------------------------------------------------


class TestStructureItems:
    """Element names in structure: list should be Type."""

    SOURCE = """\
profile:
  elements:
    act:
      structure:
        - body
        - mainBody
"""

    def test_structure_body_is_type(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 4, 10)
        assert t is not None and t[3] == 5

    def test_structure_mainBody_is_type(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 5, 10)
        assert t is not None and t[3] == 5


# ------------------------------------------------------------------
# Enum values under values: — EnumMember (type 3)
# ------------------------------------------------------------------


class TestEnumValues:
    """Values under values: in an attribute body should be EnumMember."""

    SOURCE = """\
profile:
  elements:
    act:
      attributes:
        contains:
          values:
            - originalVersion
            - singleVersion
"""

    def test_enum_value_is_enum_member(self):
        tokens = _tokens_for(self.SOURCE)
        enum_tokens = [t for t in tokens if t[0] == 6 and t[3] == 3]
        assert len(enum_tokens) == 1


# ------------------------------------------------------------------
# Edge case: key appears in _STRUCTURAL_KEYS but is an attribute
# ------------------------------------------------------------------


class TestStructuralKeyAsAttribute:
    """Keys like 'description', 'choice', 'structure' under attributes:
    should be Property, not Keyword."""

    SOURCE = """\
profile:
  elements:
    act:
      attributes:
        description:
        choice:
        structure:
"""

    def test_description_attr_is_property(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 4, 8)
        assert t is not None and t[3] == 1

    def test_choice_attr_is_property(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 5, 8)
        assert t is not None and t[3] == 1

    def test_structure_attr_is_property(self):
        tokens = _tokens_for(self.SOURCE)
        t = _find_token(tokens, 6, 8)
        assert t is not None and t[3] == 1
