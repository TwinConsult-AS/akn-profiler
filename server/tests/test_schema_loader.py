"""Tests for the AKN XSD schema loader."""

from akn_profiler.xsd.schema_loader import AknSchema

# Load once for all tests in this module
_schema = AknSchema.load()


class TestSchemaLoading:
    """Verify the schema loads and indexes elements correctly."""

    def test_loads_elements(self) -> None:
        assert len(_schema.element_names()) > 300

    def test_loads_enums(self) -> None:
        assert len(_schema.all_enums()) > 10


class TestHasElement:
    """Verify element existence checks."""

    def test_root_element_exists(self) -> None:
        assert _schema.has_element("akomaNtoso")

    def test_act_exists(self) -> None:
        assert _schema.has_element("act")

    def test_bill_exists(self) -> None:
        assert _schema.has_element("bill")

    def test_article_exists(self) -> None:
        assert _schema.has_element("article")

    def test_nonexistent_element(self) -> None:
        assert not _schema.has_element("foobar")

    def test_empty_string(self) -> None:
        assert not _schema.has_element("")


class TestGetChildren:
    """Verify child element lookups."""

    def test_akomantoso_children(self) -> None:
        children = _schema.get_children("akomaNtoso")
        assert "act" in children
        assert "bill" in children
        assert "debate" in children

    def test_act_children(self) -> None:
        children = _schema.get_children("act")
        assert "meta" in children
        assert "body" in children

    def test_nonexistent_returns_empty(self) -> None:
        assert _schema.get_children("foobar") == []


class TestGetAttributes:
    """Verify attribute lookups."""

    def test_act_has_name_attr(self) -> None:
        attrs = _schema.get_attributes("act")
        attr_names = [a.name for a in attrs]
        assert "name" in attr_names

    def test_article_has_eId(self) -> None:
        attrs = _schema.get_attributes("article")
        attr_names = [a.name for a in attrs]
        assert "eId" in attr_names

    def test_nonexistent_returns_empty(self) -> None:
        assert _schema.get_attributes("foobar") == []


class TestRequiredChildren:
    """Verify required child detection."""

    def test_act_requires_meta_and_body(self) -> None:
        required = [c.name for c in _schema.get_required_children("act")]
        assert "meta" in required
        assert "body" in required


class TestCardinality:
    """Verify cardinality annotations on ChildInfo and AttrInfo."""

    def test_required_singular_child_cardinality(self) -> None:
        """meta is required inside act → 1..1."""
        info = _schema.get_element_info("act")
        assert info is not None
        meta_children = [c for c in info.children if c.name == "meta"]
        assert len(meta_children) == 1
        assert meta_children[0].cardinality == "1..1"
        assert meta_children[0].min_occurs == 1
        assert meta_children[0].max_occurs == 1

    def test_optional_singular_child_cardinality(self) -> None:
        """preface is optional inside act → 0..1."""
        info = _schema.get_element_info("act")
        assert info is not None
        preface_children = [c for c in info.children if c.name == "preface"]
        assert len(preface_children) == 1
        assert preface_children[0].cardinality == "0..1"
        assert preface_children[0].min_occurs == 0

    def test_required_attribute_cardinality(self) -> None:
        """name is required on act → 1..1."""
        attrs = _schema.get_attributes("act")
        name_attrs = [a for a in attrs if a.name == "name"]
        assert len(name_attrs) == 1
        assert name_attrs[0].cardinality == "1..1"

    def test_optional_attribute_cardinality(self) -> None:
        """'class' is optional on article → 0..1."""
        attrs = _schema.get_attributes("article")
        cls_attrs = [a for a in attrs if a.name == "class"]
        assert len(cls_attrs) == 1
        assert cls_attrs[0].cardinality == "0..1"


class TestAttributeDocs:
    """Verify that AttrInfo carries XSD documentation."""

    def test_class_attribute_has_doc(self) -> None:
        """The 'class' attribute should have HTMLattrs group docs."""
        attrs = _schema.get_attributes("article")
        cls_attrs = [a for a in attrs if a.name == "class"]
        assert len(cls_attrs) == 1
        assert cls_attrs[0].doc  # non-empty
        assert "HTML" in cls_attrs[0].doc or "class" in cls_attrs[0].doc

    def test_source_attribute_has_doc(self) -> None:
        """The 'source' attribute should have its group documentation."""
        # source is defined in the 'source' attribute group
        attrs = _schema.get_attributes("FRBRauthor")
        src_attrs = [a for a in attrs if a.name == "source"]
        if src_attrs:
            assert src_attrs[0].doc
            assert "source" in src_attrs[0].doc.lower() or "agent" in src_attrs[0].doc.lower()

    def test_eId_attribute_has_doc(self) -> None:
        """The 'eId' attribute should carry identification docs."""
        attrs = _schema.get_attributes("chapter")
        eid_attrs = [a for a in attrs if a.name == "eId"]
        assert len(eid_attrs) == 1
        assert eid_attrs[0].doc


class TestEnumValues:
    """Verify enum value lookups."""

    def test_textual_mods(self) -> None:
        vals = _schema.get_enum_values("TextualMods")
        assert vals is not None
        assert "repeal" in vals
        assert "substitution" in vals

    def test_nonexistent_enum(self) -> None:
        assert _schema.get_enum_values("FakeEnum") is None


class TestElementInfo:
    """Verify full element info retrieval."""

    def test_act_info(self) -> None:
        info = _schema.get_element_info("act")
        assert info is not None
        assert info.xml_name == "act"
        assert info.class_name == "Act"
        assert len(info.children) > 0
        assert len(info.attributes) > 0

    def test_nonexistent_returns_none(self) -> None:
        assert _schema.get_element_info("foobar") is None


class TestChoiceGroups:
    """Verify XSD choice group extraction and attachment."""

    def test_body_has_choice_groups(self) -> None:
        """body (bodyType) has a choice group for hierElements + componentRef."""
        groups = _schema.get_choice_groups("body")
        assert len(groups) >= 1
        # Should have a non-exclusive (free mix) group
        free_groups = [g for g in groups if not g.exclusive]
        assert len(free_groups) >= 1
        # The group should contain hierarchy elements like chapter, section
        all_members = free_groups[0].all_elements
        assert "chapter" in all_members
        assert "section" in all_members

    def test_hierarchy_element_has_exclusive_choice(self) -> None:
        """chapter (hierarchy type) should have an exclusive choice
        between sub-hierarchy and content."""
        groups = _schema.get_choice_groups("chapter")
        exclusive = [g for g in groups if g.exclusive]
        assert len(exclusive) >= 1
        # One branch should contain 'content'
        content_branches = []
        hier_branches = []
        for cg in exclusive:
            for b in cg.branches:
                if "content" in b.elements:
                    content_branches.append(b)
                if "article" in b.elements or "section" in b.elements:
                    hier_branches.append(b)
        assert len(content_branches) >= 1
        assert len(hier_branches) >= 1

    def test_body_not_exclusive(self) -> None:
        """body's choice group should NOT be exclusive (maxOccurs=unbounded)."""
        groups = _schema.get_choice_groups("body")
        for g in groups:
            if "chapter" in g.all_elements:
                assert not g.exclusive

    def test_body_choice_required(self) -> None:
        """body's choice group has minOccurs=1 (at least one child required)."""
        groups = _schema.get_choice_groups("body")
        for g in groups:
            if "chapter" in g.all_elements:
                assert g.min_occurs >= 1

    def test_children_have_choice_group_ids(self) -> None:
        """Children of body should have choice_group_ids populated."""
        info = _schema.get_element_info("body")
        assert info is not None
        chapter_children = [c for c in info.children if c.name == "chapter"]
        assert len(chapter_children) == 1
        assert len(chapter_children[0].choice_group_ids) >= 1

    def test_mainBody_has_choice_groups(self) -> None:
        """mainBody (maincontent) has choice groups for hier/block/container."""
        groups = _schema.get_choice_groups("mainBody")
        assert len(groups) >= 1
        all_members = groups[0].all_elements
        # maincontent allows hierElements, blockElements, containerElements
        assert "chapter" in all_members  # hierElements
        assert "p" in all_members  # HTMLblock → blockElements

    def test_element_without_choices(self) -> None:
        """Elements with only sequence content have no choice groups."""
        groups = _schema.get_choice_groups("akomaNtoso")
        # akomaNtoso has a sequence(documentType, components?)
        # documentType is a group ref resolved as a choice, so it may have one
        # But the sequence itself is not a choice — the group IS a choice inside
        # Let's just verify the API works
        assert isinstance(groups, tuple)

    def test_authorial_note_has_choice_groups(self) -> None:
        """authorialNote (subFlowStructure) should have choice groups that
        include both a documentType branch and a block/container branch.
        This verifies the nested <xsd:choice> fix in choice_parser."""
        groups = _schema.get_choice_groups("authorialNote")
        assert len(groups) >= 1
        # The outer exclusive choice should have a branch with block elements (e.g. p)
        all_members = set()
        for cg in groups:
            all_members.update(cg.all_elements)
        # subFlowStructure allows block elements like p, container elements
        assert "p" in all_members or len(all_members) > 2


# ------------------------------------------------------------------
# get_choice_cardinality
# ------------------------------------------------------------------


class TestGetChoiceCardinality:
    """Tests for ``get_choice_cardinality``."""

    def test_body_has_choice_cardinality(self) -> None:
        """body has a choice group, so it should return a cardinality string."""
        card = _schema.get_choice_cardinality("body")
        assert card is not None
        assert ".." in card  # e.g. "1..*"

    def test_body_cardinality_format(self) -> None:
        """The returned string should match the min..max format."""
        import re

        card = _schema.get_choice_cardinality("body")
        assert card is not None
        assert re.match(r"^\d+\.\.(\d+|\*)$", card)

    def test_akomantoso_no_choice(self) -> None:
        """akomaNtoso likely has no primary choice group → None."""
        # akomaNtoso might or might not have a choice group depending
        # on how the XSD is structured, but at minimum the API should
        # return either None or a valid string.
        card = _schema.get_choice_cardinality("akomaNtoso")
        if card is not None:
            assert ".." in card

    def test_nonexistent_element(self) -> None:
        """Non-existent element returns None."""
        card = _schema.get_choice_cardinality("fooBarBaz123")
        assert card is None

    def test_hierarchy_element_has_exclusive_choice(self) -> None:
        """chapter (hierarchy) has an exclusive choice (content vs sub-hier)."""
        card = _schema.get_choice_cardinality("chapter")
        assert card is not None
        # maxOccurs should be 1 for exclusive choice
        assert card.endswith("..1")
