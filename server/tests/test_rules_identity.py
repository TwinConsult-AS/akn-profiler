"""Tests for identity rules (XSD Identity Constraints)."""

from akn_profiler.validation.engine import validate_profile
from akn_profiler.validation.errors import Severity
from akn_profiler.xsd.schema_loader import AknSchema

_schema = AknSchema.load()


def _rule_ids(yaml_text: str) -> list[str]:
    return [e.rule_id for e in validate_profile(yaml_text, _schema)]


class TestDuplicateStructure:
    """identity.duplicate-structure-entry"""

    def test_duplicate_structure(self) -> None:
        yaml = """\
profile:
  elements:
    body:
      structure:
        - chapter
        - article
        - chapter
"""
        assert "identity.duplicate-structure-entry" in _rule_ids(yaml)


class TestDoctypeCoverage:
    """identity.doctype-without-element-restriction"""

    def test_covered_doctype(self) -> None:
        yaml = """\
profile:
  documentTypes:
    - bill
  elements:
    bill:
"""
        assert "identity.doctype-without-element-restriction" not in _rule_ids(yaml)

    def test_uncovered_doctype(self) -> None:
        yaml = """\
profile:
  documentTypes:
    - bill
"""
        errors = validate_profile(yaml, _schema)
        info_rules = [e.rule_id for e in errors if e.severity == Severity.INFO]
        assert "identity.doctype-without-element-restriction" in info_rules
