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
