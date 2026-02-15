"""Tests for vocabulary rules (XSD Declarations)."""

from akn_profiler.validation.engine import validate_profile
from akn_profiler.xsd.schema_loader import AknSchema

_schema = AknSchema.load()


def _errors_with_rule(yaml_text: str, rule_prefix: str) -> list[str]:
    """Run validation and return rule_ids matching the prefix."""
    errors = validate_profile(yaml_text, _schema)
    return [e.rule_id for e in errors if e.rule_id.startswith(rule_prefix)]


class TestUnknownElement:
    """vocabulary.unknown-element"""

    def test_known_element_no_error(self) -> None:
        yaml = """\
profile:
  elements:
    act:
"""
        assert "vocabulary.unknown-element" not in _errors_with_rule(yaml, "vocabulary")

    def test_unknown_element(self) -> None:
        yaml = """\
profile:
  elements:
    foobar:
"""
        assert "vocabulary.unknown-element" in _errors_with_rule(yaml, "vocabulary")


class TestUnknownAttribute:
    """vocabulary.unknown-attribute"""

    def test_known_attribute_no_error(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      attributes:
        name:
          required: true
"""
        assert "vocabulary.unknown-attribute" not in _errors_with_rule(yaml, "vocabulary")

    def test_unknown_attribute(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      attributes:
        nonexistent_attr:
          required: true
"""
        assert "vocabulary.unknown-attribute" in _errors_with_rule(yaml, "vocabulary")


class TestUnknownDocumentType:
    """vocabulary.unknown-document-type"""

    def test_valid_doc_type(self) -> None:
        yaml = """\
profile:
  documentTypes:
    - bill
    - act
"""
        assert "vocabulary.unknown-document-type" not in _errors_with_rule(yaml, "vocabulary")

    def test_invalid_doc_type(self) -> None:
        yaml = """\
profile:
  documentTypes:
    - bill
    - fakeDocType
"""
        assert "vocabulary.unknown-document-type" in _errors_with_rule(yaml, "vocabulary")


class TestUnknownChildElement:
    """vocabulary.unknown-element for children entries."""

    def test_unknown_child_element(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      children:
        meta:
        nonexistentChild:
"""
        assert "vocabulary.unknown-element" in _errors_with_rule(yaml, "vocabulary")


class TestUnknownStructureElement:
    """vocabulary.unknown-element for structure entries."""

    def test_unknown_structure_element(self) -> None:
        yaml = """\
profile:
  elements:
    body:
      structure:
        - chapter
        - fakeLevel
"""
        assert "vocabulary.unknown-element" in _errors_with_rule(yaml, "vocabulary")
