"""Tests for choice rules (XSD Choice Groups)."""

from akn_profiler.models.profile import ElementRestriction
from akn_profiler.validation.engine import validate_profile
from akn_profiler.xsd.schema_loader import AknSchema

_schema = AknSchema.load()


def _rule_ids(yaml_text: str) -> list[str]:
    return [e.rule_id for e in validate_profile(yaml_text, _schema)]


def _errors_for_rule(yaml_text: str, rule_id: str) -> list:
    return [e for e in validate_profile(yaml_text, _schema) if e.rule_id == rule_id]


# ==================================================================
# choice.required-group-empty
# ==================================================================


class TestRequiredGroupEmpty:
    """choice.required-group-empty — mandatory choice group with no members."""

    def test_body_with_hier_element_passes(self) -> None:
        """body with a hierarchy child satisfies the required choice group."""
        yaml = """\
profile:
  elements:
    body:
      children:
        chapter:
"""
        assert "choice.required-group-empty" not in _rule_ids(yaml)

    def test_body_with_component_ref_passes(self) -> None:
        """body with componentRef satisfies the required choice group."""
        yaml = """\
profile:
  elements:
    body:
      children:
        componentRef:
"""
        assert "choice.required-group-empty" not in _rule_ids(yaml)

    def test_body_with_empty_children_errors(self) -> None:
        """body with children containing no valid choice group member should error."""
        yaml_empty = """\
profile:
  elements:
    body:
      children:
        nonExistentElement:
"""
        errors = _errors_for_rule(yaml_empty, "choice.required-group-empty")
        assert len(errors) >= 1
        assert "<body>" in errors[0].message

    def test_no_children_key_still_errors_for_required_group(self) -> None:
        """body declared with no children: should error — XSD requires
        at least one child from the choice group (minOccurs=1)."""
        yaml = """\
profile:
  elements:
    body:
"""
        errors = _errors_for_rule(yaml, "choice.required-group-empty")
        assert len(errors) >= 1
        assert "<body>" in errors[0].message

    def test_optional_choice_no_error(self) -> None:
        """basehierarchy's choice (num, heading, subheading) has
        minOccurs=0, so not declaring any is fine."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        article:
"""
        # Should not complain about missing num/heading/subheading
        errors = _errors_for_rule(yaml, "choice.required-group-empty")
        base_errors = [e for e in errors if "num" in e.message or "heading" in e.message]
        assert len(base_errors) == 0

    def test_preamble_with_block_element_passes(self) -> None:
        """preamble (preambleopt) allows blockElements | preambleContainers.
        Having a block element should satisfy the requirement."""
        yaml = """\
profile:
  elements:
    preamble:
      children:
        p:
"""
        assert "choice.required-group-empty" not in _rule_ids(yaml)

    def test_mainBody_with_hier_element_passes(self) -> None:
        """mainBody (maincontent) allows hier|block|container elements."""
        yaml = """\
profile:
  elements:
    mainBody:
      children:
        chapter:
"""
        assert "choice.required-group-empty" not in _rule_ids(yaml)

    def test_choice_branch_satisfies_required_group(self) -> None:
        """An element in a choice: branch should satisfy a required group."""
        yaml = """\
profile:
  elements:
    body:
      children:
        choice:
          chapter:
          componentRef:
"""
        assert "choice.required-group-empty" not in _rule_ids(yaml)


# ==================================================================
# choice.incomplete-branches
# ==================================================================


class TestIncompleteBranches:
    """choice.incomplete-branches — choice: with fewer than 2 branches."""

    def test_empty_choice_errors(self) -> None:
        """choice: with no branches at all should error."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        choice:
"""
        errors = _errors_for_rule(yaml, "choice.incomplete-branches")
        assert len(errors) == 1
        assert "no children" in errors[0].message

    def test_one_branch_errors(self) -> None:
        """choice: with only 1 branch should error."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        choice:
          section:
"""
        errors = _errors_for_rule(yaml, "choice.incomplete-branches")
        assert len(errors) == 1
        assert "only 1" in errors[0].message

    def test_two_branches_ok(self) -> None:
        """choice: with 2 populated branches is valid."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        choice:
          section:
          subchapter:
"""
        assert "choice.incomplete-branches" not in _rule_ids(yaml)

    def test_no_choice_key_no_error(self) -> None:
        """Elements without choice: should not trigger this rule."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        article:
"""
        assert "choice.incomplete-branches" not in _rule_ids(yaml)


# ==================================================================
# choice.exclusive-branch-conflict
# ==================================================================


class TestExclusiveBranchConflict:
    """choice.exclusive-branch-conflict — mixing branches of exclusive choice
    in always-present children (not inside choice:)."""

    def test_chapter_with_only_sub_hierarchy_passes(self) -> None:
        """chapter with only sub-hierarchy children (article) is OK."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        article:
"""
        assert "choice.exclusive-branch-conflict" not in _rule_ids(yaml)

    def test_chapter_with_only_content_passes(self) -> None:
        """chapter with only content child is OK."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        content:
"""
        assert "choice.exclusive-branch-conflict" not in _rule_ids(yaml)

    def test_chapter_with_both_branches_errors(self) -> None:
        """chapter with both hierarchy children AND content should error."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        article:
        content:
"""
        errors = _errors_for_rule(yaml, "choice.exclusive-branch-conflict")
        assert len(errors) >= 1
        assert "<chapter>" in errors[0].message

    def test_article_with_both_branches_errors(self) -> None:
        """article with both paragraph + content should error."""
        yaml = """\
profile:
  elements:
    article:
      children:
        paragraph:
        content:
"""
        errors = _errors_for_rule(yaml, "choice.exclusive-branch-conflict")
        assert len(errors) >= 1

    def test_body_is_not_exclusive(self) -> None:
        """body's choice(componentRef, hierElements) is unbounded/free-mix,
        so mixing componentRef and chapter is fine."""
        yaml = """\
profile:
  elements:
    body:
      children:
        componentRef:
        chapter:
"""
        assert "choice.exclusive-branch-conflict" not in _rule_ids(yaml)

    def test_section_with_both_errors(self) -> None:
        """section with both sub-hierarchy AND content should error."""
        yaml = """\
profile:
  elements:
    section:
      children:
        article:
        content:
"""
        errors = _errors_for_rule(yaml, "choice.exclusive-branch-conflict")
        assert len(errors) >= 1

    def test_choice_key_avoids_conflict(self) -> None:
        """Using choice: to express exclusivity should NOT trigger conflict."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        num: "1..1"
        choice:
          article:
          content:
"""
        assert "choice.exclusive-branch-conflict" not in _rule_ids(yaml)


# ==================================================================
# choice.branch-invalid-child
# ==================================================================


class TestBranchInvalidChild:
    """choice.branch-invalid-child — branch contains invalid XSD child."""

    def test_valid_branch_children_pass(self) -> None:
        """All branch children are valid XSD children of chapter."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        num: "1..1"
        choice:
          section: "1..*"
          subchapter: "1..*"
"""
        assert "choice.branch-invalid-child" not in _rule_ids(yaml)

    def test_invalid_branch_child_errors(self) -> None:
        """A branch containing an element not valid per XSD should error."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        choice:
          nonExistentChild:
"""
        errors = _errors_for_rule(yaml, "choice.branch-invalid-child")
        assert len(errors) >= 1
        assert "nonExistentChild" in errors[0].message


# ==================================================================
# choice.branch-overlap
# ==================================================================


class TestBranchOverlap:
    """choice.branch-overlap — element in multiple branches or in both
    children and a branch."""

    def test_no_overlap_passes(self) -> None:
        """Disjoint branches and children should pass."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        num: "1..1"
        choice:
          section: "1..*"
          subchapter: "1..*"
"""
        assert "choice.branch-overlap" not in _rule_ids(yaml)

    def test_child_in_both_always_and_branch_errors(self) -> None:
        """An element in both children: and a choice: branch should error."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        section: "1..*"
        choice:
          section: "1..*"
          subchapter: "1..*"
"""
        errors = _errors_for_rule(yaml, "choice.branch-overlap")
        assert len(errors) >= 1
        assert "section" in errors[0].message

    def test_cross_element_overlap_impossible_with_dict(self) -> None:
        """With flat dict format, duplicate keys are merged by YAML parser.
        So cross-element overlap cannot happen — no error expected."""
        yaml = """\
profile:
  elements:
    chapter:
      children:
        choice:
          section: "1..*"
          subchapter: "1..*"
"""
        assert "choice.branch-overlap" not in _rule_ids(yaml)


# ==================================================================
# ElementRestriction model_validator — choice extraction
# ==================================================================


class TestElementRestrictionChoice:
    """Verify _extract_choice model_validator."""

    def test_extracts_choice_from_children_dict(self) -> None:
        """choice: key (dict format) is extracted from children."""
        r = ElementRestriction(
            children={
                "num": "1..1",
                "choice": {
                    "section": "1..*",
                    "subchapter": "1..*",
                },
            }
        )
        assert "choice" not in r.children
        assert "num" in r.children
        assert len(r.exclusive_children) == 2
        assert r.exclusive_children["section"] == "1..*"
        assert r.exclusive_children["subchapter"] == "1..*"

    def test_extracts_choice_from_children_legacy_list(self) -> None:
        """choice: key (legacy list format) is merged into flat dict."""
        r = ElementRestriction(
            children={
                "num": "1..1",
                "choice": [
                    {"section": "1..*"},
                    {"subchapter": "1..*"},
                ],
            }
        )
        assert "choice" not in r.children
        assert "num" in r.children
        assert len(r.exclusive_children) == 2
        assert r.exclusive_children["section"] == "1..*"
        assert r.exclusive_children["subchapter"] == "1..*"

    def test_no_choice_key(self) -> None:
        """Without choice: the exclusive_children stays empty."""
        r = ElementRestriction(children={"chapter": None})
        assert r.exclusive_children == {}

    def test_empty_children(self) -> None:
        """Empty children dict is fine."""
        r = ElementRestriction(children={})
        assert r.exclusive_children == {}
        assert r.children == {}

    def test_choice_only(self) -> None:
        """Children with only choice: → children becomes empty."""
        r = ElementRestriction(
            children={
                "choice": {
                    "section": "1..*",
                    "subchapter": "1..*",
                },
            }
        )
        assert r.children == {}
        assert len(r.exclusive_children) == 2

    def test_multiple_exclusive_elements(self) -> None:
        """All exclusive elements are stored as a flat dict."""
        r = ElementRestriction(
            children={
                "choice": {
                    "section": "1..*",
                    "subchapter": "1..*",
                    "crossHeading": "0..*",
                },
            }
        )
        assert len(r.exclusive_children) == 3
        assert r.exclusive_children == {
            "section": "1..*",
            "subchapter": "1..*",
            "crossHeading": "0..*",
        }
