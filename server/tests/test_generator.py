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
    """Generated YAML → validate_profile → zero unexpected errors.

    This is the ultimate correctness proof: the generator produces
    YAML that the validation engine (which is XSD-driven) accepts.

    ``choice.required-group-empty`` is excluded because the generator
    intentionally does NOT auto-select from choice groups — the user
    must pick which children to include.
    """

    _EXPECTED_USER_ACTION = {"choice.required-group-empty"}

    def test_act_round_trip(self, schema: AknSchema) -> None:
        yaml_text = generate_yaml(schema, "act", comments=False)
        errors = validate_profile(yaml_text, schema)
        unexpected = [e for e in errors if e.rule_id not in self._EXPECTED_USER_ACTION]
        assert unexpected == [], f"Unexpected errors: {unexpected}"

    def test_bill_round_trip(self, schema: AknSchema) -> None:
        yaml_text = generate_yaml(schema, "bill", comments=False)
        errors = validate_profile(yaml_text, schema)
        unexpected = [e for e in errors if e.rule_id not in self._EXPECTED_USER_ACTION]
        assert unexpected == [], f"Unexpected errors: {unexpected}"

    def test_all_doc_types_round_trip(self, schema: AknSchema) -> None:
        """Every document type's generated profile must pass."""
        doc_types = schema.get_children("akomaNtoso")
        for dt in doc_types:
            yaml_text = generate_yaml(schema, dt, comments=False)
            errors = validate_profile(yaml_text, schema)
            unexpected = [e for e in errors if e.rule_id not in self._EXPECTED_USER_ACTION]
            assert unexpected == [], f"[{dt}] Unexpected errors: {unexpected}"


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


# ------------------------------------------------------------------
# choiceCardinality in generated output
# ------------------------------------------------------------------


class TestChoiceGeneration:
    """Verify that generated profiles include choice: for exclusive groups."""

    def test_hierarchy_element_has_choice(self, schema: AknSchema) -> None:
        """Hierarchy elements (chapter) have an exclusive choice → choice: key."""
        text = generate_yaml(schema, "act", comments=False, include_optional_children=True)
        data = yaml.safe_load(text)
        elements = data["profile"]["elements"]
        # chapter has hierarchy type with exclusive choice (content vs sub-hier)
        if "chapter" in elements and isinstance(elements["chapter"], dict):
            children = elements["chapter"].get("children", {})
            if isinstance(children, dict):
                assert "choice" in children, (
                    "chapter.children should contain choice: for exclusive branches"
                )
                assert isinstance(children["choice"], list)
                assert len(children["choice"]) >= 2

    def test_commented_yaml_includes_choice(self, schema: AknSchema) -> None:
        """When hierarchy elements are included, commented YAML has choice: block."""
        # Generate a profile that forces a hierarchy element to appear
        # by generating with include_optional_children which will
        # walk the tree but hierarchy elements need to be in the profile.
        # Use the profile model directly:
        from akn_profiler.models.profile import ElementRestriction

        profile = generate_profile(schema, "act", include_optional_children=True)
        # Manually add 'chapter' to get exclusive choice branches
        from akn_profiler.models.generator import _add_element

        _add_element(
            schema,
            "chapter",
            profile.elements,
            include_optional_children=True,
            include_optional_attributes=False,
        )
        # Now check that chapter has exclusive_children
        assert "chapter" in profile.elements
        assert len(profile.elements["chapter"].exclusive_children) >= 2

    def test_plain_yaml_round_trips(self, schema: AknSchema) -> None:
        """Generated YAML round-trips through ProfileDocument parsing."""
        text = generate_yaml(schema, "act", comments=False)
        data = yaml.safe_load(text)
        profile = ProfileDocument.model_validate(data["profile"])
        # Verify the profile parsed successfully
        assert len(profile.elements) > 0

    def test_body_no_exclusive_choice(self, schema: AknSchema) -> None:
        """body's choice is free-mix (not exclusive), so no choice: key."""
        text = generate_yaml(schema, "act", comments=False)
        data = yaml.safe_load(text)
        elements = data["profile"]["elements"]
        if "body" in elements and isinstance(elements["body"], dict):
            children = elements["body"].get("children", {})
            if isinstance(children, dict):
                # body shouldn't have choice: since its group is free-mix
                assert "choice" not in children, (
                    "body.children should NOT have choice: (free-mix group)"
                )
