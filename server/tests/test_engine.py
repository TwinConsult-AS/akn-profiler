"""Integration tests for the validation engine.

Every test here constructs a profile from scratch and validates it
against the live AknSchema.  Nothing depends on example.akn.yaml.
"""

from akn_profiler.validation.engine import validate_profile
from akn_profiler.validation.errors import Severity
from akn_profiler.xsd.schema_loader import AknSchema

_schema = AknSchema.load()


class TestXsdDrivenValidProfile:
    """A profile built entirely from what the XSD actually declares
    should produce zero errors."""

    VALID = """\
profile:
  name: "XSD-derived minimal profile"
  version: "1.0"
  documentTypes:
    - act
  elements:
    akomaNtoso:
    act:
      children:
        meta:
        body:
      attributes:
        name:
          required: true
        contains:
          required: true
          values: ["originalVersion"]
    meta:
      children:
        identification:
    identification:
      attributes:
        source:
          required: true
      children:
        FRBRWork:
        FRBRExpression:
        FRBRManifestation:
    FRBRWork:
      children:
        FRBRthis:
        FRBRuri:
        FRBRdate:
        FRBRauthor:
        FRBRcountry:
    FRBRExpression:
      children:
        FRBRthis:
        FRBRuri:
        FRBRdate:
        FRBRauthor:
        FRBRlanguage:
    FRBRManifestation:
      children:
        FRBRthis:
        FRBRuri:
        FRBRdate:
        FRBRauthor:
    FRBRthis:
      attributes:
        value:
          required: true
    FRBRuri:
      attributes:
        value:
          required: true
    FRBRdate:
      attributes:
        date:
          required: true
        name:
          required: true
    FRBRauthor:
      attributes:
        href:
          required: true
    FRBRcountry:
      attributes:
        value:
          required: true
    FRBRlanguage:
      attributes:
        language:
          required: true
    body:
      children:
        chapter:
      structure:
        - chapter
        - article
        - paragraph
    chapter:
"""

    # choice.required-group-empty is expected — the generator / hand-crafted
    # profile intentionally does NOT auto-pick from choice groups.
    _USER_ACTION_RULES = {"choice.required-group-empty"}

    def test_no_errors(self) -> None:
        errors = validate_profile(self.VALID, _schema)
        hard = [
            e
            for e in errors
            if e.severity == Severity.ERROR and e.rule_id not in self._USER_ACTION_RULES
        ]
        for e in hard:
            print(f"  {e.rule_id}: {e.message}")
        assert hard == [], f"Unexpected errors: {hard}"

    def test_only_info_level(self) -> None:
        """No warnings or errors — at most informational notes
        (besides expected choice-group prompts)."""
        errors = validate_profile(self.VALID, _schema)
        non_info = [
            e
            for e in errors
            if e.severity != Severity.INFO and e.rule_id not in self._USER_ACTION_RULES
        ]
        assert non_info == []


class TestCompletelyInvalidProfile:
    """A profile full of mistakes should produce multiple errors."""

    BAD_PROFILE = """\
profile:
  name: "Bad Profile"
  documentTypes:
    - fakeDocType
  elements:
    nonExistent:
    act:
      attributes:
        fakeAttr:
          required: true
      children:
        nonExistentChild:
        paragraph:
"""

    def test_catches_all_error_types(self) -> None:
        errors = validate_profile(self.BAD_PROFILE, _schema)
        rule_ids = {e.rule_id for e in errors}
        assert "vocabulary.unknown-document-type" in rule_ids
        assert "vocabulary.unknown-element" in rule_ids
        assert "vocabulary.unknown-attribute" in rule_ids
        # paragraph is a valid element but not a valid child of act
        assert "structure.invalid-child" in rule_ids

    def test_error_count(self) -> None:
        errors = validate_profile(self.BAD_PROFILE, _schema)
        hard = [e for e in errors if e.severity == Severity.ERROR]
        # fakeDocType + nonExistent + fakeAttr +
        # nonExistentChild + paragraph-not-child-of-act
        assert len(hard) >= 4


class TestEmptyProfile:
    """An empty profile should produce no errors."""

    def test_empty(self) -> None:
        yaml = "profile: {}\n"
        errors = validate_profile(yaml, _schema)
        assert errors == []


class TestErrorLineNumbers:
    """Errors should carry line numbers from the YAML source."""

    def test_line_numbers_present(self) -> None:
        yaml = """\
profile:
  elements:
    fakeElement:
"""
        errors = validate_profile(yaml, _schema)
        vocab_errors = [e for e in errors if e.rule_id == "vocabulary.unknown-element"]
        assert len(vocab_errors) == 1
        assert vocab_errors[0].line is not None
        assert vocab_errors[0].line == 3  # 'fakeElement' is on line 3 (1-indexed)


class TestEnumValuesFromXsd:
    """Datatype rules should use enum values from the XSD directly."""

    def test_valid_xsd_enum(self) -> None:
        # 'contains' on <act> is an XSD VersionType enum
        yaml = """\
profile:
  elements:
    act:
      attributes:
        contains:
          values: ["originalVersion", "singleVersion"]
"""
        errors = validate_profile(yaml, _schema)
        # Only check that there are no datatype errors (strictness may flag missing attrs)
        datatype_errors = [e for e in errors if e.rule_id.startswith("datatype.")]
        assert datatype_errors == []

    def test_invalid_xsd_enum(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      attributes:
        contains:
          values: ["notARealVersion"]
"""
        errors = validate_profile(yaml, _schema)
        rule_ids = {e.rule_id for e in errors}
        assert "datatype.invalid-enum-value" in rule_ids
