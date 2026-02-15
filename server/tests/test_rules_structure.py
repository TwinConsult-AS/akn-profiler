"""Tests for structure rules (XSD Complex Types)."""

from akn_profiler.validation.engine import validate_profile
from akn_profiler.xsd.schema_loader import AknSchema

_schema = AknSchema.load()


def _rule_ids(yaml_text: str) -> list[str]:
    return [e.rule_id for e in validate_profile(yaml_text, _schema)]


class TestInvalidChild:
    """structure.invalid-child"""

    def test_valid_children(self) -> None:
        yaml = """\
profile:
  elements:
    act:
      children:
        meta:
        body:
"""
        assert "structure.invalid-child" not in _rule_ids(yaml)

    def test_invalid_child(self) -> None:
        # <act> cannot directly contain <paragraph>
        yaml = """\
profile:
  elements:
    act:
      children:
        meta:
        paragraph:
"""
        assert "structure.invalid-child" in _rule_ids(yaml)


class TestStructureChain:
    """structure.invalid-structure-chain"""

    def test_valid_structure(self) -> None:
        # body > chapter, chapter > article, article > paragraph
        yaml = """\
profile:
  elements:
    body:
      structure:
        - chapter
        - article
        - paragraph
"""
        assert "structure.invalid-structure-chain" not in _rule_ids(yaml)

    def test_invalid_structure_chain(self) -> None:
        # <chapter> cannot contain <p> per the XSD (chapter has hierarchy children, not blocks)
        yaml = """\
profile:
  elements:
    body:
      structure:
        - chapter
        - p
"""
        ids = _rule_ids(yaml)
        assert "structure.invalid-structure-chain" in ids

    def test_structure_root_must_be_child_of_element(self) -> None:
        # <act> cannot contain <paragraph> as direct child,
        # so paragraph cannot be the first structure level
        yaml = """\
profile:
  elements:
    act:
      structure:
        - paragraph
"""
        ids = _rule_ids(yaml)
        assert "structure.invalid-structure-root" in ids

    def test_valid_structure_root(self) -> None:
        # <body> can contain <chapter>
        yaml = """\
profile:
  elements:
    body:
      structure:
        - chapter
"""
        ids = _rule_ids(yaml)
        assert "structure.invalid-structure-root" not in ids
