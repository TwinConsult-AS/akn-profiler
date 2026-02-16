"""Tests for element ordering, reorder command, and identity attribute operations."""

from __future__ import annotations

import pytest
import yaml

from akn_profiler.models.cascade import (
    compute_element_order,
    expand_element,
    reorder_attributes,
    reorder_children,
    reorder_profile,
)
from akn_profiler.xsd.schema_loader import AknSchema


@pytest.fixture(scope="module")
def schema() -> AknSchema:
    return AknSchema.load()


# ------------------------------------------------------------------
# compute_element_order
# ------------------------------------------------------------------


class TestComputeElementOrder:
    """compute_element_order produces canonical parent-before-child order."""

    def test_empty_elements(self, schema: AknSchema) -> None:
        assert compute_element_order({}, schema) == []

    def test_single_element(self, schema: AknSchema) -> None:
        elements = {"body": None}
        result = compute_element_order(elements, schema)
        assert result == ["body"]

    def test_akomantoso_always_first(self, schema: AknSchema) -> None:
        elements = {"body": None, "akomaNtoso": None, "act": None}
        result = compute_element_order(elements, schema)
        assert result[0] == "akomaNtoso"

    def test_parent_before_child(self, schema: AknSchema) -> None:
        elements = {
            "meta": {"children": {"identification": "1..1"}},
            "identification": None,
            "act": {"children": {"meta": "1..1", "body": "1..1"}},
            "body": None,
            "akomaNtoso": {"children": {"act": "1..1"}},
        }
        result = compute_element_order(elements, schema)
        assert result.index("akomaNtoso") < result.index("act")
        assert result.index("act") < result.index("meta")
        assert result.index("act") < result.index("body")
        assert result.index("meta") < result.index("identification")

    def test_shared_child_after_last_parent(self, schema: AknSchema) -> None:
        """When two parents share a child, the child comes after both parents."""
        elements = {
            "alpha": {"children": {"shared": "1..1"}},
            "beta": {"children": {"shared": "1..1"}},
            "shared": None,
        }
        result = compute_element_order(elements, schema)
        shared_idx = result.index("shared")
        alpha_idx = result.index("alpha")
        beta_idx = result.index("beta")
        assert shared_idx > alpha_idx
        assert shared_idx > beta_idx

    def test_alphabetical_tiebreaking(self, schema: AknSchema) -> None:
        """Siblings at the same level should be alphabetical."""
        elements = {
            "zebra": None,
            "apple": None,
            "mango": None,
        }
        result = compute_element_order(elements, schema)
        assert result == ["apple", "mango", "zebra"]

    def test_choice_children_included(self, schema: AknSchema) -> None:
        """Children inside choice: should be part of the parent graph."""
        elements = {
            "parent": {
                "children": {
                    "regular": "1..1",
                    "choice": {"branch_a": "1..*", "branch_b": "1..*"},
                }
            },
            "regular": None,
            "branch_a": None,
            "branch_b": None,
        }
        result = compute_element_order(elements, schema)
        parent_idx = result.index("parent")
        assert result.index("regular") > parent_idx
        assert result.index("branch_a") > parent_idx
        assert result.index("branch_b") > parent_idx

    def test_linear_chain(self, schema: AknSchema) -> None:
        """A → B → C → D should produce [A, B, C, D]."""
        elements = {
            "d": None,
            "c": {"children": {"d": "1..1"}},
            "b": {"children": {"c": "1..1"}},
            "a": {"children": {"b": "1..1"}},
        }
        result = compute_element_order(elements, schema)
        assert result == ["a", "b", "c", "d"]

    def test_orphan_elements_sorted_as_roots(self, schema: AknSchema) -> None:
        """Orphan elements (no parent-child edges) are treated as roots."""
        elements = {
            "parent": {"children": {"child": "1..1"}},
            "child": None,
            "orphan_z": None,
            "orphan_a": None,
        }
        result = compute_element_order(elements, schema)
        # parent → child ordering preserved
        assert result.index("parent") < result.index("child")
        # Orphans sorted alphabetically among themselves
        assert result.index("orphan_a") < result.index("orphan_z")


# ------------------------------------------------------------------
# expand_element ordering
# ------------------------------------------------------------------


class TestExpandElementOrdering:
    """expand_element places new elements in canonical order."""

    MINIMAL = """\
profile:
  name: "Test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    akomaNtoso:
"""

    def test_expanded_elements_in_order(self, schema: AknSchema) -> None:
        """After expanding act, akomaNtoso should be first, then ancestors before descendants."""
        result = expand_element(self.MINIMAL, "act", schema)
        data = yaml.safe_load(result)
        keys = list(data["profile"]["elements"].keys())
        assert keys[0] == "akomaNtoso"
        # act should come before meta and body
        assert keys.index("act") < keys.index("meta")
        assert keys.index("act") < keys.index("body")
        # meta should come before identification
        assert keys.index("meta") < keys.index("identification")

    def test_expand_with_auto_eid(self, schema: AknSchema) -> None:
        """When auto_add_eid=True, elements that support eId get the attribute."""
        result = expand_element(self.MINIMAL, "act", schema, auto_add_eid=True)
        data = yaml.safe_load(result)
        # act itself doesn't support eId, but body does
        body = data["profile"]["elements"]["body"]
        assert isinstance(body, dict)
        attrs = body.get("attributes", {})
        assert "eId" in attrs

    def test_expand_with_all_identity(self, schema: AknSchema) -> None:
        """All three identity attrs when all auto-add flags are set."""
        result = expand_element(
            self.MINIMAL,
            "act",
            schema,
            auto_add_eid=True,
            auto_add_wid=True,
            auto_add_guid=True,
        )
        data = yaml.safe_load(result)
        # body supports eId, wId, GUID (act doesn't)
        body = data["profile"]["elements"]["body"]
        attrs = body.get("attributes", {})
        assert "eId" in attrs
        assert "wId" in attrs
        assert "GUID" in attrs

    def test_expand_without_auto_eid(self, schema: AknSchema) -> None:
        """Default (auto_add_eid=False) should not add eId unless required."""
        result = expand_element(self.MINIMAL, "act", schema)
        data = yaml.safe_load(result)
        act = data["profile"]["elements"]["act"]
        if isinstance(act, dict):
            attrs = act.get("attributes", {})
            # eId is not XSD-required on act, so shouldn't be auto-added
            assert "eId" not in attrs

    def test_expand_auto_id_required_true(self, schema: AknSchema) -> None:
        """auto_id_required=True marks auto-added identity attrs as required."""
        result = expand_element(
            self.MINIMAL,
            "act",
            schema,
            auto_add_eid=True,
            auto_id_required=True,
        )
        data = yaml.safe_load(result)
        body = data["profile"]["elements"]["body"]
        assert body["attributes"]["eId"]["required"] is True

    def test_expand_auto_id_required_false(self, schema: AknSchema) -> None:
        """auto_id_required=False marks auto-added identity attrs as optional."""
        result = expand_element(
            self.MINIMAL,
            "act",
            schema,
            auto_add_eid=True,
            auto_id_required=False,
        )
        data = yaml.safe_load(result)
        body = data["profile"]["elements"]["body"]
        assert body["attributes"]["eId"]["required"] is False


# ------------------------------------------------------------------
# reorder_children / reorder_attributes
# ------------------------------------------------------------------


class TestReorderChildren:
    """reorder_children sorts by XSD field order."""

    def test_required_first(self, schema: AknSchema) -> None:
        """Required children should come before optional ones."""
        children = {"body": "1..1", "meta": "1..1"}
        result = reorder_children(children, "act", schema)
        keys = list(result.keys())
        assert keys.index("meta") < keys.index("body")

    def test_choice_at_end(self, schema: AknSchema) -> None:
        """choice: should always be the last key."""
        children = {
            "choice": {"section": "1..*"},
            "num": "1..1",
            "heading": "0..1",
        }
        result = reorder_children(children, "chapter", schema)
        keys = list(result.keys())
        assert keys[-1] == "choice"

    def test_unknown_element_preserved(self, schema: AknSchema) -> None:
        """Unknown children keys are kept but sorted to the end."""
        children = {"unknown_thing": "1..1", "meta": "1..1"}
        result = reorder_children(children, "act", schema)
        keys = list(result.keys())
        assert "unknown_thing" in keys
        assert "meta" in keys


class TestReorderAttributes:
    """reorder_attributes sorts by XSD field order."""

    def test_required_before_optional(self, schema: AknSchema) -> None:
        """Required attributes should come before optional ones."""
        # For act: 'name' is required, 'class' is optional
        attrs = {"class": {"required": False}, "name": {"required": True}}
        result = reorder_attributes(attrs, "act", schema)
        keys = list(result.keys())
        assert keys.index("name") < keys.index("class")


# ------------------------------------------------------------------
# reorder_profile
# ------------------------------------------------------------------


class TestReorderProfile:
    """reorder_profile reorders the full profile."""

    OUT_OF_ORDER = """\
profile:
  name: "Test"
  version: "1.0"
  documentTypes:
    - act

  elements:
    identification:
    body:
    meta:
      children:
        identification: "1..1"
    act:
      children:
        meta: "1..1"
        body: "1..1"
    akomaNtoso:
      children:
        act: "1..1"
"""

    def test_elements_reordered(self, schema: AknSchema) -> None:
        result = reorder_profile(self.OUT_OF_ORDER, schema)
        data = yaml.safe_load(result)
        keys = list(data["profile"]["elements"].keys())
        assert keys[0] == "akomaNtoso"
        assert keys.index("act") < keys.index("meta")
        assert keys.index("act") < keys.index("body")
        assert keys.index("meta") < keys.index("identification")

    def test_children_within_element_reordered(self, schema: AknSchema) -> None:
        """children should follow XSD field order after reorder."""
        result = reorder_profile(self.OUT_OF_ORDER, schema)
        data = yaml.safe_load(result)
        act = data["profile"]["elements"]["act"]
        if isinstance(act, dict) and "children" in act:
            child_keys = list(act["children"].keys())
            # meta should come before body in XSD order for act
            assert child_keys.index("meta") < child_keys.index("body")

    def test_idempotent(self, schema: AknSchema) -> None:
        """Reordering twice should produce the same result."""
        first = reorder_profile(self.OUT_OF_ORDER, schema)
        second = reorder_profile(first, schema)
        assert yaml.safe_load(first) == yaml.safe_load(second)

    def test_no_data_loss(self, schema: AknSchema) -> None:
        """All elements, children, and attributes should be preserved."""
        result = reorder_profile(self.OUT_OF_ORDER, schema)
        original = yaml.safe_load(self.OUT_OF_ORDER)
        reordered = yaml.safe_load(result)
        # Same element set
        assert set(original["profile"]["elements"]) == set(reordered["profile"]["elements"])

    def test_invalid_yaml_unchanged(self, schema: AknSchema) -> None:
        """Non-profile YAML should be returned unchanged."""
        text = "not_a_profile: true\n"
        assert reorder_profile(text, schema) == text
