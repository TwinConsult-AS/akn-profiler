"""Tests for the YAML parser and Pydantic profile models."""

from akn_profiler.validation.yaml_parser import parse_profile


class TestYamlSyntax:
    """YAML syntax error detection."""

    def test_valid_yaml(self) -> None:
        yaml = "profile:\n  name: test\n"
        profile, errors, _ = parse_profile(yaml)
        assert profile is not None
        parse_errs = [e for e in errors if e.rule_id.startswith("parse.")]
        assert parse_errs == []

    def test_invalid_yaml_syntax(self) -> None:
        yaml = "profile:\n  name: [unterminated"
        profile, errors, _ = parse_profile(yaml)
        assert profile is None
        assert any(e.rule_id == "parse.yaml-syntax" for e in errors)

    def test_not_a_mapping(self) -> None:
        yaml = "- just\n- a\n- list\n"
        profile, errors, _ = parse_profile(yaml)
        assert profile is None
        assert any(e.rule_id == "parse.not-a-mapping" for e in errors)

    def test_missing_profile_key(self) -> None:
        yaml = "something:\n  name: test\n"
        profile, errors, _ = parse_profile(yaml)
        assert profile is None
        assert any(e.rule_id == "parse.missing-profile-key" for e in errors)


class TestProfileParsing:
    """Pydantic model structural validation."""

    def test_minimal_profile(self) -> None:
        yaml = "profile:\n  name: test\n"
        profile, errors, _ = parse_profile(yaml)
        assert profile is not None
        assert profile.name == "test"

    def test_full_profile(self) -> None:
        yaml = """\
profile:
  name: "Test Profile"
  version: "1.0"
  description: "A test"
  documentTypes:
    - bill
  elements:
    bill:
      children:
        meta:
        body:
      attributes:
        name:
          required: true
          values: ["x", "y"]
"""
        profile, errors, _ = parse_profile(yaml)
        assert profile is not None
        assert profile.name == "Test Profile"
        assert profile.documentTypes == ["bill"]
        assert "bill" in profile.elements
        assert profile.elements["bill"].children == {"meta": None, "body": None}
        assert "name" in profile.elements["bill"].attributes
        assert profile.elements["bill"].attributes["name"].required is True
        assert profile.elements["bill"].attributes["name"].values == ["x", "y"]

    def test_empty_profile(self) -> None:
        yaml = "profile: {}\n"
        profile, errors, _ = parse_profile(yaml)
        # Should succeed with defaults
        assert profile is not None
        assert profile.name == ""
        assert profile.elements == {}


class TestLineIndex:
    """Line-number tracking from YAML source."""

    def test_records_key_lines(self) -> None:
        yaml = "profile:\n  name: test\n  version: '1.0'\n"
        _, _, index = parse_profile(yaml)
        assert index.get("profile") is not None
        assert index.get("profile.name") is not None
        assert index.get("profile.version") is not None

    def test_records_sequence_lines(self) -> None:
        yaml = """\
profile:
  documentTypes:
    - bill
    - act
"""
        _, _, index = parse_profile(yaml)
        assert index.get("profile.documentTypes[0]") is not None
        assert index.get("profile.documentTypes[1]") is not None
