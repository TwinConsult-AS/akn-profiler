"""Tests for identity attribute add/remove operations."""

from __future__ import annotations

import pytest
import yaml

from akn_profiler.xsd.schema_loader import AknSchema


@pytest.fixture(scope="module")
def schema() -> AknSchema:
    return AknSchema.load()


PROFILE_WITH_ACT = """\
profile:
  name: "Test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    akomaNtoso:
      children:
        act: "1..1"
    act:
      children:
        meta: "1..1"
        body: "1..1"
      attributes:
        name:
          required: true
    meta:
    body:
    identification:
"""


class TestAddIdentityAttrs:
    """Test _add_identity_attrs_to_profile."""

    def test_add_eid_to_supported_elements(self, schema: AknSchema, monkeypatch) -> None:
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        result = srv._add_identity_attrs_to_profile(PROFILE_WITH_ACT, ["eId"])
        data = yaml.safe_load(result)

        # body supports eId (act doesn't — it only has name/contains)
        body = data["profile"]["elements"]["body"]
        assert isinstance(body, dict)
        assert "eId" in body["attributes"]

    def test_add_multiple_attrs(self, schema: AknSchema, monkeypatch) -> None:
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        result = srv._add_identity_attrs_to_profile(PROFILE_WITH_ACT, ["eId", "wId", "GUID"])
        data = yaml.safe_load(result)

        # body supports all three identity attrs
        body = data["profile"]["elements"]["body"]
        assert isinstance(body, dict)
        attrs = body["attributes"]
        assert "eId" in attrs
        assert "wId" in attrs
        assert "GUID" in attrs

    def test_preserves_existing_attrs(self, schema: AknSchema, monkeypatch) -> None:
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        result = srv._add_identity_attrs_to_profile(PROFILE_WITH_ACT, ["eId"])
        data = yaml.safe_load(result)

        # name should still be present
        act = data["profile"]["elements"]["act"]
        assert "name" in act["attributes"]

    def test_skip_unsupported_elements(self, schema: AknSchema, monkeypatch) -> None:
        """akomaNtoso does not support eId — should remain unchanged."""
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        result = srv._add_identity_attrs_to_profile(PROFILE_WITH_ACT, ["eId"])
        data = yaml.safe_load(result)

        akn = data["profile"]["elements"]["akomaNtoso"]
        if isinstance(akn, dict):
            attrs = akn.get("attributes", {})
            assert "eId" not in attrs

    def test_non_identity_attr_ignored(self, schema: AknSchema, monkeypatch) -> None:
        """Only identity attrs (eId, wId, GUID) should be added."""
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        result = srv._add_identity_attrs_to_profile(PROFILE_WITH_ACT, ["class"])
        data = yaml.safe_load(result)

        # act should not get 'class' added through this function
        act = data["profile"]["elements"]["act"]
        if isinstance(act, dict):
            assert "class" not in act.get("attributes", {})

    def test_invalid_yaml_unchanged(self, schema: AknSchema, monkeypatch) -> None:
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        text = "not_a_profile: true\n"
        assert srv._add_identity_attrs_to_profile(text, ["eId"]) == text

    def test_idempotent(self, schema: AknSchema, monkeypatch) -> None:
        """Adding the same attr twice should not duplicate anything."""
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        first = srv._add_identity_attrs_to_profile(PROFILE_WITH_ACT, ["eId"])
        second = srv._add_identity_attrs_to_profile(first, ["eId"])
        assert yaml.safe_load(first) == yaml.safe_load(second)

    def test_add_as_required_true(self, schema: AknSchema, monkeypatch) -> None:
        """as_required=True should set required: true on added attributes."""
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        result = srv._add_identity_attrs_to_profile(PROFILE_WITH_ACT, ["eId"], as_required=True)
        data = yaml.safe_load(result)

        body = data["profile"]["elements"]["body"]
        assert body["attributes"]["eId"]["required"] is True

    def test_add_as_required_false(self, schema: AknSchema, monkeypatch) -> None:
        """as_required=False should set required: false on added attributes."""
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        result = srv._add_identity_attrs_to_profile(PROFILE_WITH_ACT, ["eId"], as_required=False)
        data = yaml.safe_load(result)

        body = data["profile"]["elements"]["body"]
        assert body["attributes"]["eId"]["required"] is False


class TestRemoveIdentityAttrs:
    """Test _remove_identity_attrs_from_profile."""

    def test_remove_eid(self, schema: AknSchema, monkeypatch) -> None:
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        # First add, then remove
        with_eid = srv._add_identity_attrs_to_profile(PROFILE_WITH_ACT, ["eId"])
        result = srv._remove_identity_attrs_from_profile(with_eid, ["eId"])
        data = yaml.safe_load(result)

        act = data["profile"]["elements"]["act"]
        if isinstance(act, dict):
            attrs = act.get("attributes", {})
            assert "eId" not in attrs

    def test_remove_preserves_required(self, schema: AknSchema, monkeypatch) -> None:
        """Should not remove eId if it's XSD-required on the element."""
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        # Find an element where eId is required
        # For elements in idreq group, eId is required
        profile_with_required = """\
profile:
  name: "Test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    section:
      attributes:
        eId:
          required: true
"""
        result = srv._remove_identity_attrs_from_profile(profile_with_required, ["eId"])
        data = yaml.safe_load(result)

        section = data["profile"]["elements"]["section"]
        if isinstance(section, dict):
            # eId should be preserved if required by XSD
            info = schema.get_element_info("section")
            if info:
                eid_attr = next((a for a in info.attributes if a.name == "eId"), None)
                if eid_attr and eid_attr.required:
                    assert "eId" in section.get("attributes", {})

    def test_remove_cleans_empty_attributes(self, schema: AknSchema, monkeypatch) -> None:
        """Removing the only attribute should clean up the attributes section."""
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        only_eid = """\
profile:
  name: "Test"
  version: "1.0"
  documentTypes:
    - act
  elements:
    body:
      attributes:
        eId:
          required: false
"""
        result = srv._remove_identity_attrs_from_profile(only_eid, ["eId"])
        data = yaml.safe_load(result)

        body = data["profile"]["elements"]["body"]
        if isinstance(body, dict):
            assert "attributes" not in body or not body.get("attributes")

    def test_remove_non_identity_ignored(self, schema: AknSchema, monkeypatch) -> None:
        """Removing a non-identity attr name should be ignored."""
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        result = srv._remove_identity_attrs_from_profile(PROFILE_WITH_ACT, ["name"])
        data = yaml.safe_load(result)

        # name should still be in act's attributes
        act = data["profile"]["elements"]["act"]
        assert "name" in act["attributes"]

    def test_invalid_yaml_unchanged(self, schema: AknSchema, monkeypatch) -> None:
        import akn_profiler.server as srv

        monkeypatch.setattr(srv, "akn_schema", schema)

        text = "random: stuff\n"
        assert srv._remove_identity_attrs_from_profile(text, ["eId"]) == text
