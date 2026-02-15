"""Tests for the cascade add/remove operations."""

from __future__ import annotations

import pytest
import yaml

from akn_profiler.models.cascade import collapse_element, expand_element
from akn_profiler.xsd.schema_loader import AknSchema


@pytest.fixture(scope="module")
def schema() -> AknSchema:
    return AknSchema.load()


MINIMAL_PROFILE = """\
profile:
  name: "Test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    akomaNtoso:
"""


class TestExpandElement:
    """expand_element should recursively add required children."""

    def test_expand_adds_element(self, schema: AknSchema) -> None:
        result = expand_element(MINIMAL_PROFILE, "act", schema)
        data = yaml.safe_load(result)
        assert "act" in data["profile"]["elements"]

    def test_expand_adds_required_children(self, schema: AknSchema) -> None:
        result = expand_element(MINIMAL_PROFILE, "act", schema)
        data = yaml.safe_load(result)
        elements = data["profile"]["elements"]
        # act requires meta and body
        assert "meta" in elements
        assert "body" in elements

    def test_expand_cascades_recursively(self, schema: AknSchema) -> None:
        result = expand_element(MINIMAL_PROFILE, "act", schema)
        data = yaml.safe_load(result)
        elements = data["profile"]["elements"]
        # meta → identification → FRBRWork, FRBRExpression, FRBRManifestation
        assert "identification" in elements
        assert "FRBRWork" in elements
        assert "FRBRExpression" in elements
        assert "FRBRManifestation" in elements

    def test_expand_includes_required_attrs(self, schema: AknSchema) -> None:
        result = expand_element(MINIMAL_PROFILE, "act", schema)
        data = yaml.safe_load(result)
        act_elem = data["profile"]["elements"]["act"]
        assert isinstance(act_elem, dict)
        assert "attributes" in act_elem
        assert "name" in act_elem["attributes"]
        assert "contains" in act_elem["attributes"]

    def test_expand_is_idempotent(self, schema: AknSchema) -> None:
        first = expand_element(MINIMAL_PROFILE, "act", schema)
        second = expand_element(first, "act", schema)
        assert yaml.safe_load(first) == yaml.safe_load(second)

    def test_expand_includes_meta_children(self, schema: AknSchema) -> None:
        result = expand_element(MINIMAL_PROFILE, "meta", schema)
        data = yaml.safe_load(result)
        elements = data["profile"]["elements"]
        # meta requires identification, so it should be added
        assert "identification" in elements


class TestCollapseElement:
    """collapse_element should remove element and orphaned descendants."""

    FULL = """\
profile:
  name: "Test"
  documentTypes:
    - act
  elements:
    akomaNtoso:
    act:
      children:
        meta:
        body:
    meta:
      children:
        identification:
    identification:
    body:
"""

    def test_collapse_removes_element(self, schema: AknSchema) -> None:
        result = collapse_element(self.FULL, "body", schema)
        data = yaml.safe_load(result)
        assert "body" not in data["profile"]["elements"]

    def test_collapse_removes_orphans(self, schema: AknSchema) -> None:
        result = collapse_element(self.FULL, "meta", schema)
        data = yaml.safe_load(result)
        elements = data["profile"]["elements"]
        # meta and identification are both removed (identification is orphaned)
        assert "meta" not in elements
        assert "identification" not in elements

    def test_collapse_keeps_non_orphans(self, schema: AknSchema) -> None:
        result = collapse_element(self.FULL, "meta", schema)
        data = yaml.safe_load(result)
        elements = data["profile"]["elements"]
        # act and body should remain
        assert "act" in elements
        assert "body" in elements

    def test_collapse_cleans_children_list(self, schema: AknSchema) -> None:
        result = collapse_element(self.FULL, "meta", schema)
        data = yaml.safe_load(result)
        act_elem = data["profile"]["elements"]["act"]
        if isinstance(act_elem, dict) and "children" in act_elem:
            assert "meta" not in act_elem["children"]

    def test_collapse_removes_element_and_cleans_parent(self, schema: AknSchema) -> None:
        result = collapse_element(self.FULL, "identification", schema)
        data = yaml.safe_load(result)
        elements = data["profile"]["elements"]
        assert "identification" not in elements
