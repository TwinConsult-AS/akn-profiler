"""Tests for the AKN profile generator."""

from __future__ import annotations

import pytest
import yaml

from akn_profiler.models.generator import generate_profile, generate_yaml
from akn_profiler.models.profile import ProfileDocument
from akn_profiler.validation.engine import validate_profile
from akn_profiler.xsd.schema_loader import AknSchema


@pytest.fixture(scope="module")
def schema() -> AknSchema:
    return AknSchema.load()


# ------------------------------------------------------------------
# Basic generation
# ------------------------------------------------------------------


class TestGenerateProfile:
    """Tests for ``generate_profile``."""

    def test_returns_profile_document(self, schema: AknSchema) -> None:
        profile = generate_profile(schema, "act")
        assert isinstance(profile, ProfileDocument)

    def test_act_has_required_elements(self, schema: AknSchema) -> None:
        profile = generate_profile(schema, "act")
        # The act document type requires at minimum:
        # akomaNtoso, act, meta, body, identification,
        # FRBRWork, FRBRExpression, FRBRManifestation, FRBRthis, FRBRcountry
        required_names = {
            "akomaNtoso",
            "act",
            "meta",
            "body",
            "identification",
            "FRBRWork",
            "FRBRExpression",
            "FRBRManifestation",
            "FRBRthis",
            "FRBRcountry",
        }
        assert required_names.issubset(profile.elements.keys())

    def test_act_document_type_listed(self, schema: AknSchema) -> None:
        profile = generate_profile(schema, "act")
        assert profile.documentTypes == ["act"]

    def test_invalid_doc_type_raises(self, schema: AknSchema) -> None:
        with pytest.raises(ValueError, match="not a valid AKN document type"):
            generate_profile(schema, "foobar")

    def test_act_has_required_attributes(self, schema: AknSchema) -> None:
        """``<act>`` requires ``name`` and ``contains``."""
        profile = generate_profile(schema, "act")
        act_elem = profile.elements["act"]
        assert "name" in act_elem.attributes
        assert act_elem.attributes["name"].required is True
        assert "contains" in act_elem.attributes
        assert act_elem.attributes["contains"].required is True
        assert act_elem.attributes["contains"].values  # enum values present

    def test_identification_has_source_attr(self, schema: AknSchema) -> None:
        """``<identification>`` requires a ``source`` attribute."""
        profile = generate_profile(schema, "act")
        ident = profile.elements["identification"]
        assert "source" in ident.attributes

    def test_required_chain_includes_identification(self, schema: AknSchema) -> None:
        profile = generate_profile(schema, "act")
        # identification is required under <meta>, so it must be in elements
        assert "identification" in profile.elements

    def test_include_optional_children(self, schema: AknSchema) -> None:
        """When include_optional_children=True, body lists all hierarchy children."""
        profile = generate_profile(schema, "act", include_optional_children=True)
        body_elem = profile.elements["body"]
        # body should have many children (chapter, article, section, etc.)
        assert len(body_elem.children) > 5

    def test_include_optional_attributes(self, schema: AknSchema) -> None:
        """When include_optional_attributes=True, elements pick up more attrs."""
        minimal = generate_profile(schema, "act")
        expanded = generate_profile(schema, "act", include_optional_attributes=True)
        # The expanded profile should have at least as many attrs on each element
        for elem_name in minimal.elements:
            if elem_name in expanded.elements:
                assert len(expanded.elements[elem_name].attributes) >= len(
                    minimal.elements[elem_name].attributes
                )


# ------------------------------------------------------------------
# Multiple document types
# ------------------------------------------------------------------


class TestAllDocumentTypes:
    """The generator should work for every AKN document type."""

    @pytest.fixture(scope="class")
    def doc_types(self, schema: AknSchema) -> list[str]:
        return schema.get_children("akomaNtoso")

    def test_at_least_one_doc_type(self, doc_types: list[str]) -> None:
        assert len(doc_types) >= 1

    def test_generate_all_doc_types(self, schema: AknSchema, doc_types: list[str]) -> None:
        for dt in doc_types:
            profile = generate_profile(schema, dt)
            assert dt in profile.documentTypes
            assert dt in profile.elements


# ------------------------------------------------------------------
# Round-trip: generated profile passes validation
# ------------------------------------------------------------------


class TestRoundTripValidation:
    """Generated YAML → validate_profile → zero errors.

    This is the ultimate correctness proof: the generator produces
    YAML that the validation engine (which is XSD-driven) accepts.
    """

    def test_act_round_trip(self, schema: AknSchema) -> None:
        yaml_text = generate_yaml(schema, "act", comments=False)
        errors = validate_profile(yaml_text, schema)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_bill_round_trip(self, schema: AknSchema) -> None:
        yaml_text = generate_yaml(schema, "bill", comments=False)
        errors = validate_profile(yaml_text, schema)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_all_doc_types_round_trip(self, schema: AknSchema) -> None:
        """Every document type's generated profile must pass."""
        doc_types = schema.get_children("akomaNtoso")
        for dt in doc_types:
            yaml_text = generate_yaml(schema, dt, comments=False)
            errors = validate_profile(yaml_text, schema)
            assert errors == [], f"[{dt}] Unexpected errors: {errors}"


# ------------------------------------------------------------------
# YAML serialisation
# ------------------------------------------------------------------


class TestGenerateYaml:
    """Tests for ``generate_yaml``."""

    def test_plain_yaml_is_parseable(self, schema: AknSchema) -> None:
        text = generate_yaml(schema, "act", comments=False)
        data = yaml.safe_load(text)
        assert "profile" in data
        assert data["profile"]["documentTypes"] == ["act"]

    def test_commented_yaml_is_parseable(self, schema: AknSchema) -> None:
        text = generate_yaml(schema, "act", comments=True)
        data = yaml.safe_load(text)
        assert "profile" in data

    def test_commented_yaml_has_comments(self, schema: AknSchema) -> None:
        text = generate_yaml(schema, "act", comments=True)
        assert text.startswith("# Auto-generated")
        assert "# required" in text or "# XSD-required" in text

    def test_version_and_name_present(self, schema: AknSchema) -> None:
        text = generate_yaml(schema, "act", comments=False)
        data = yaml.safe_load(text)
        assert data["profile"]["name"]
        assert data["profile"]["version"]
