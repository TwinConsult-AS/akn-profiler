"""Tests for data-type rules (XSD Simple Types)."""

from akn_profiler.validation.engine import validate_profile
from akn_profiler.validation.errors import Severity
from akn_profiler.xsd.schema_loader import AknSchema

_schema = AknSchema.load()


def _errors_for(yaml_text: str) -> list[tuple[str, str]]:
    """Return (rule_id, severity) tuples."""
    return [(e.rule_id, e.severity.value) for e in validate_profile(yaml_text, _schema)]


def _rule_ids(yaml_text: str) -> list[str]:
    return [e.rule_id for e in validate_profile(yaml_text, _schema)]


class TestEnumSubset:
    """datatype.invalid-enum-value"""

    def test_valid_enum_values(self) -> None:
        # 'contains' on <act> is enum-typed (VersionType)
        # Valid values are 'originalVersion' and 'singleVersion'
        yaml = """\
profile:
  elements:
    act:
      attributes:
        contains:
          values: ["originalVersion"]
"""
        assert "datatype.invalid-enum-value" not in _rule_ids(yaml)

    def test_invalid_enum_value(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      attributes:
        contains:
          values: ["originalVersion", "madeUpValue"]
"""
        assert "datatype.invalid-enum-value" in _rule_ids(yaml)


class TestCustomEnumOnFreeAttribute:
    """datatype.custom-enum-on-free-attribute"""

    def test_custom_values_on_free_attr(self) -> None:
        # 'class' on <article> is a free string — not enum-typed
        yaml = """\
profile:
  elements:
    article:
      attributes:
        class:
          values: ["myClass"]
"""
        errors = validate_profile(yaml_text=yaml, schema=_schema)
        info_rules = [e.rule_id for e in errors if e.severity == Severity.INFO]
        assert "datatype.custom-enum-on-free-attribute" in info_rules
