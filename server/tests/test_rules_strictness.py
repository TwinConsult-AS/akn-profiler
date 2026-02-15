"""Tests for strictness rules (XSD Cardinality)."""

from akn_profiler.validation.engine import validate_profile
from akn_profiler.validation.errors import Severity
from akn_profiler.xsd.schema_loader import AknSchema

_schema = AknSchema.load()


def _warnings(yaml_text: str) -> list[str]:
    """Return rule_ids of ERROR-severity strictness errors."""
    errors = validate_profile(yaml_text, _schema)
    return [e.rule_id for e in errors if e.severity == Severity.ERROR]


class TestMissingRequiredChild:
    """strictness.missing-required-child"""

    def test_no_warning_when_children_complete(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      children:
        meta:
        body:
"""
        assert "strictness.missing-required-child" not in _warnings(yaml)

    def test_warning_when_required_child_omitted(self) -> None:
        # <act> requires meta and body; omitting body should warn
        yaml = """\
profile:
  elements:
    act:
      children:
        meta:
"""
        assert "strictness.missing-required-child" in _warnings(yaml)

    def test_no_warning_when_no_children_key(self) -> None:
        # If the profile doesn't declare children at all, no warning
        yaml = """\
profile:
  elements:
    act:
"""
        assert "strictness.missing-required-child" not in _warnings(yaml)


class TestMissingRequiredAttribute:
    """strictness.missing-required-attribute"""

    def test_no_warning_when_attrs_complete(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      attributes:
        name:
          required: true
        contains:
          required: true
"""
        assert "strictness.missing-required-attribute" not in _warnings(yaml)

    def test_warning_when_required_attr_omitted(self) -> None:
        # <act> requires 'name' and 'contains'; omitting one should warn
        yaml = """\
profile:
  elements:
    act:
      attributes:
        name:
          required: true
"""
        assert "strictness.missing-required-attribute" in _warnings(yaml)


class TestRequiredChainCoverage:
    """strictness.missing-required-element"""

    def test_no_warning_when_chain_complete(self) -> None:
        yaml = """\
profile:
  documentTypes:
    - act
  elements:
    akomaNtoso:
    act:
    meta:
    identification:
    FRBRWork:
    FRBRExpression:
    FRBRManifestation:
    FRBRthis:
    FRBRuri:
    FRBRdate:
    FRBRauthor:
    FRBRcountry:
    FRBRlanguage:
    body:
"""
        assert "strictness.missing-required-element" not in _warnings(yaml)

    def test_warning_when_chain_element_missing(self) -> None:
        yaml = """\
profile:
  documentTypes:
    - act
  elements:
    act:
"""
        assert "strictness.missing-required-element" in _warnings(yaml)


class TestUndeclaredChildElement:
    """strictness.undeclared-child-element"""

    def test_no_warning_when_child_declared(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      children:
        meta:
        body:
    meta:
    body:
"""
        assert "strictness.undeclared-child-element" not in _warnings(yaml)

    def test_warning_when_child_not_declared(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      children:
        meta:
        body:
    meta:
"""
        # 'body' listed as child of act but has no element definition
        assert "strictness.undeclared-child-element" in _warnings(yaml)

    def test_no_warning_when_no_children_key(self) -> None:
        yaml = """\
profile:
  elements:
    act:
"""
        assert "strictness.undeclared-child-element" not in _warnings(yaml)

    def test_no_warning_for_unknown_element(self) -> None:
        # If the child is not known to the schema, vocabulary rules handle it
        yaml = """\
profile:
  elements:
    act:
      children:
        notAnXsdElement:
"""
        assert "strictness.undeclared-child-element" not in _warnings(yaml)

    def test_multiple_undeclared_children(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      children:
        meta:
        body:
"""
        errs = [
            e.rule_id
            for e in validate_profile(yaml, _schema)
            if e.rule_id == "strictness.undeclared-child-element"
        ]
        # Both meta and body are undeclared
        assert len(errs) == 2

    def test_warning_for_undeclared_choice_child(self) -> None:
        """Elements under choice: should also trigger the diagnostic."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        choice:
          section:
          subchapter:
"""
        # section and subchapter are valid XSD children of chapter
        # but not declared in profile.elements
        assert "strictness.undeclared-child-element" in _warnings(yaml)

    def test_no_warning_for_declared_choice_child(self) -> None:
        """No warning when choice children ARE declared as elements."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        choice:
          section:
          subchapter:
    section:
    subchapter:
"""
        errs = [
            e.rule_id
            for e in validate_profile(yaml, _schema)
            if e.rule_id == "strictness.undeclared-child-element"
        ]
        assert len(errs) == 0

    def test_choice_only_no_direct_children(self) -> None:
        """Works when children: has only choice: (no always-present kids)."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        choice:
          section:
"""
        assert "strictness.undeclared-child-element" in _warnings(yaml)
