from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import ForwardRef

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlDuration, XmlTime


class EfficacyMods(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">EfficacyMods</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    simple type EfficacyMods lists all the types of modifications in
    efficacy as values for the type attribute of the efficacyMod
    element.</ns1:comment>.
    """

    ENTRY_INTO_EFFICACY = "entryIntoEfficacy"
    END_OF_EFFICACY = "endOfEfficacy"
    INAPPLICATION = "inapplication"
    RETROACTIVITY = "retroactivity"
    EXTRAEFFICACY = "extraefficacy"
    POSTPONEMENT_OF_EFFICACY = "postponementOfEfficacy"
    PROROGATION_OF_EFFICACY = "prorogationOfEfficacy"


class ForceMods(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">ForceMods</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    simple type ForceMods lists all the types of modifications in force as
    values for the type attribute of the forceMod element.</ns1:comment>.
    """

    ENTRY_INTO_FORCE = "entryIntoForce"
    END_OF_ENACTMENT = "endOfEnactment"
    POSTPONEMENT_OF_ENTRY_INTO_FORCE = "postponementOfEntryIntoForce"
    PROROGATION_OF_FORCE = "prorogationOfForce"
    RE_ENACTMENT = "reEnactment"
    UNCONSTITUTIONALITY = "unconstitutionality"


class LegalSystemMods(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">LegalSystemMods</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    simple type LegalSystemMods lists all the types of modifications in the
    legal system as values for the type attribute of the LegalSystemMod
    element.</ns1:comment>.
    """

    STATIC_REFERENCE = "staticReference"
    IMPLEMENTATION = "implementation"
    RATIFICATION = "ratification"
    APPLICATION = "application"
    LEGISLATIVE_DELEGATION = "legislativeDelegation"
    DEREGULATION = "deregulation"
    CONVERSION = "conversion"
    EXPIRATION = "expiration"
    REITERATION = "reiteration"
    REMAKING = "remaking"
    REPUBLICATION = "republication"
    COORDINATION = "coordination"


class MeaningMods(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">MeaningMods</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    simple type MeaningMods lists all the types of modifications in meaning
    as values for the type attribute of the meaningMod
    element.</ns1:comment>.
    """

    VARIATION = "variation"
    TERM_MODIFICATION = "termModification"
    AUTHENTIC_INTERPRETATION = "authenticInterpretation"


class ScopeMods(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">ScopeMods</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    simple type ScopeMods lists all the types of modifications in scope as
    values for the type attribute of the scopeMod element.</ns1:comment>.
    """

    EXCEPTION_OF_SCOPE = "exceptionOfScope"
    EXTENSION_OF_SCOPE = "extensionOfScope"


class TextualMods(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TextualMods</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    simple type TextualMods lists all the types of textual modifications as
    values for the type attribute of the textualMod element.</ns1:comment>.
    """

    REPEAL = "repeal"
    SUBSTITUTION = "substitution"
    INSERTION = "insertion"
    REPLACEMENT = "replacement"
    RENUMBERING = "renumbering"
    SPLIT = "split"
    JOIN = "join"


@dataclass(kw_only=True)
class AnyOtherType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">anyOtherType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type anyOtherType defines an open content model for elements
    that may use elements from other namespaces.</ns1:comment>.
    """

    class Meta:
        name = "anyOtherType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    href: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Basehierarchy:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">basehierarchy</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type basehierarchy is not used by any element, but is derived
    by other types to contain the basic structure of hierarchical
    elements</ns1:comment>.
    """

    class Meta:
        name = "basehierarchy"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    num: list[Num] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    heading: list[Heading] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subheading: list[Subheading] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )


@dataclass(kw_only=True)
class ComponentData:
    class Meta:
        name = "componentData"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    component_data: list[ComponentData] = field(
        default_factory=list,
        metadata={
            "name": "componentData",
            "type": "Element",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    show_as: str = field(
        metadata={
            "name": "showAs",
            "type": "Attribute",
            "required": True,
        }
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class CountType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">countType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type countType lists all the properties associated to elements
    of parliamentary count.</ns1:comment>.
    """

    class Meta:
        name = "countType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    value: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    href: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class EventType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">eventType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of allowed values for the type attribute of the eventRef
    element</ns1:comment>.
    """

    GENERATION = "generation"
    AMENDMENT = "amendment"
    REPEAL = "repeal"


@dataclass(kw_only=True)
class LinkType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">linkType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type linkType defines the empty content model and the list of
    attributes for Work- or Expression-level references to external
    resources</ns1:comment>.
    """

    class Meta:
        name = "linkType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    show_as: str = field(
        metadata={
            "name": "showAs",
            "type": "Attribute",
            "required": True,
        }
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Metaopt:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">metaopt</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type metaopt defines the content model and attributes shared by
    all metadata elements.

    Here the eId attribute is optional</ns1:comment>.
    """

    class Meta:
        name = "metaopt"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )


@dataclass(kw_only=True)
class Metareq:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">metareq</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type metareq defines the content model and attributes shared by
    all metadata elements.

    Here the eId attribute is required</ns1:comment>.
    """

    class Meta:
        name = "metareq"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )


class OpinionType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">opinionType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of allowed values for the type attribute of the opinion
    element</ns1:comment>.
    """

    DISSENTING = "dissenting"
    AGREEING = "agreeing"
    NULL = "null"


class PlacementType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">placementType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of allowed values for the placement attribute of
    notes</ns1:comment>.
    """

    SIDE = "side"
    LEFT = "left"
    RIGHT = "right"
    BOTTOM = "bottom"
    INLINE = "inline"


@dataclass(kw_only=True)
class PortionStructure:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">portionStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    portionStructure specifies the overall content model of the document
    type that is a portion of another document</ns1:comment>.
    """

    class Meta:
        name = "portionStructure"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    meta: MetaType = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    portion_body: PortionBody = field(
        metadata={
            "name": "portionBody",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    included_in: str = field(
        metadata={
            "name": "includedIn",
            "type": "Attribute",
            "required": True,
        }
    )


class PosType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">posType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of possible positions of the text being analyzed by the
    element in the analysis section</ns1:comment>.
    """

    START = "start"
    BEFORE = "before"
    INSIDE = "inside"
    AFTER = "after"
    END = "end"
    UNSPECIFIED = "unspecified"


@dataclass(kw_only=True)
class ReferenceType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">referenceType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type referenceType defines the empty content model and the list
    of attributes for metadata elements in the references
    section</ns1:comment>.
    """

    class Meta:
        name = "referenceType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    show_as: str = field(
        metadata={
            "name": "showAs",
            "type": "Attribute",
            "required": True,
        }
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )


class RemarkType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">remarkType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of allowed values for the type attribute of the remark element
    for the specification of editorial remarks (e.g., applauses, laughters,
    etc.) especially within debate records</ns1:comment>.
    """

    SCENE_DESCRIPTION = "sceneDescription"
    PHENOMENON = "phenomenon"
    CAPTION = "caption"
    TRANSLATION = "translation"


class RestrictionType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">restrictionType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of allowed values for the restriction type
    attribute</ns1:comment>.
    """

    JURISDICTION = "jurisdiction"


class ResultType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">resultType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of allowed values for the type attribute of the result
    element</ns1:comment>.
    """

    DENY = "deny"
    DISMISS = "dismiss"
    UPHOLD = "uphold"
    REVERT = "revert"
    REPLACE_ORDER = "replaceOrder"
    REMIT = "remit"
    DECIDE = "decide"
    APPROVE = "approve"


@dataclass(kw_only=True)
class SrcType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">srcType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type srcType defines the empty content model and the list of
    attributes for manifestation-level references to external
    resources</ns1:comment>.
    """

    class Meta:
        name = "srcType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    src: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    alt: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    show_as: str = field(
        metadata={
            "name": "showAs",
            "type": "Attribute",
            "required": True,
        }
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )


class StatusType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">statusType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of allowed values for the status attribute.

    This is the list of possible reasons for a dscrepancy between the
    manifestation as it should be (e.g., a faithful representation of the
    content of an expression), and the manifestation as it actually is.
    Values should be interpreted as follows: - removed: the content of the
    element is present in the markup (manifestation) but is not present in
    the real content of the document (expression level) because it has been
    definitely removed (either ex tunc, as in annullments, or ex nunc, as
    in abrogations). - temporarily removed: the content of the element is
    present in the markup (manifestation) but is not present in the real
    content of the document (expression level) because it has been
    temporarily removed (e.g., for a temporary suspension or limitation of
    efficacy). - translated: the content of the element is present in the
    markup (manifestation) in a different form than in the real content of
    the document (expression level) because it has been translated into a
    different language (e.g., to match the rest of the document or because
    of other editorial decisions). - editorial: the content of the element
    is present in the markup (manifestation) but is not present in the real
    content of the document (expression level) because it has been inserted
    as an editorial process when creating the XML markup. - edited: the
    content of the element is different in the markup (manifestation) than
    in the real content of the document (expression level) because it has
    been amended (e.g., to remove scurrilous or offensive remarks). -
    verbatim: the content of the element is present in the markup
    (manifestation) is EXACTLY as it was in the real content of the
    document (expression level) because usual silent fixes and edits were
    NOT performed (e.g. to punctuation, grammatical errors or other usually
    non-debatable problems). - incomplete: the content of the element or
    the value of a required attribute is NOT present in the markup
    (manifestation), although it should, because the missing data is not
    known at the moment, but in the future it might become known. This is
    especially appropriate for documents in drafting phase (e.g., the
    publication date of the act while drafting the bill) - unknown: the
    content of the element or the value of a required attribute is NOT
    present in the markup (manifestation), although it should, because the
    author of the manifestation does not know it. - undefined: the content
    of the element or the value of a required attribute is NOT present in
    the markup (manifestation), because the information is not defined in
    the original document, or it doesn't exist in some legal tradition
    (e.g. an anonymous speech cannot specify the attribute by, or some
    publications do not record the numbering of the items, etc.) - ignored:
    the content of the element or the value of a required attribute is NOT
    present in the markup (manifestation) because the information exists
    but the author of the manifestation is not interested in reporting it
    (e.g., omitted parts of the document due to editorial reasons,
    etc.)</ns1:comment>.
    """

    REMOVED = "removed"
    TEMPORARILY_REMOVED = "temporarilyRemoved"
    TRANSLATED = "translated"
    EDITORIAL = "editorial"
    EDITED = "edited"
    VERBATIM = "verbatim"
    INCOMPLETE = "incomplete"
    UNKNOWN = "unknown"
    UNDEFINED = "undefined"
    IGNORED = "ignored"


class TimeType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">timeType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of allowed values for the type attribute of the recordedTime
    element for the specification of an explicit mention of a time (e.g.,
    in a debate)</ns1:comment>.
    """

    START_EVENT = "startEvent"
    END_EVENT = "endEvent"


class VersionType(Enum):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Simple</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">versionType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> This is
    the list of allowed values for the contains attribute</ns1:comment>.
    """

    ORIGINAL_VERSION = "originalVersion"
    SINGLE_VERSION = "singleVersion"
    MULTIPLE_VERSIONS = "multipleVersions"


class LangValue(Enum):
    VALUE = ""


class SpaceValue(Enum):
    DEFAULT = "default"
    PRESERVE = "preserve"


@dataclass(kw_only=True)
class Frbrauthor(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRauthor</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRauthor is the metadata property containing a relevant
    author of the document in the respective level of the FRBR hierarchy.

    Attribute as specifies the role of the author.</ns1:comment>.
    """

    class Meta:
        name = "FRBRauthor"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Frbrdate(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRdate</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRdate is the metadata property containing a relevant date of
    the document in the respective level of the FRBR hierarchy.

    Attribute name specifies which actual date is contained
    here.</ns1:comment>.
    """

    class Meta:
        name = "FRBRdate"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    date: XmlDate | XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Frbrlanguage(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRlanguage</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRlanguage is the metadata property containing a RFC4646
    (three-letter code) of the main human language used in the content of
    this expression</ns1:comment>.
    """

    class Meta:
        name = "FRBRlanguage"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    language: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class FrbrmasterExpression(LinkType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRmasterExpression</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRmasterExpression is the metadata property identifying the
    master expression, i.e., the expression whose ids are used as permanent
    ids in the wId attributes.

    An expression without the FRBRmasterExpression element is considered a
    master expression itself, i.e., the first version, or the most
    important version, of a document expressed in the only language, or in
    the most important language. Any other situation (subsequent versions,
    or language variants, or content variants) must have the
    FRBRmasterExpression element pointing to the URI of the master
    expression. If the FRBRmasterEpression is specified, but without a href
    pointing to the masterExpression, it is assumed that NO master
    expression exist in reality, but an UR-Expression exist, whose ids are
    used in this expression as wIds.</ns1:comment>.
    """

    class Meta:
        name = "FRBRmasterExpression"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrportion(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRportion</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRportion is the metadata property containing the eId of the
    portion contained in a manifestation-level portion.

    If the portion contains an interval of elements, the range attributes
    specifies the first and last one.</ns1:comment>.
    """

    class Meta:
        name = "FRBRportion"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    show_as: None | str = field(
        default=None,
        metadata={
            "name": "showAs",
            "type": "Attribute",
        },
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )
    from_value: str = field(
        metadata={
            "name": "from",
            "type": "Attribute",
            "required": True,
        }
    )
    up_to: None | str = field(
        default=None,
        metadata={
            "name": "upTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Frbrtranslation(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRtranslation</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRtranslation is the metadata property specifying the source
    of which this expression is a translation of.</ns1:comment>.
    """

    class Meta:
        name = "FRBRtranslation"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    from_language: str = field(
        metadata={
            "name": "fromLanguage",
            "type": "Attribute",
            "required": True,
        }
    )
    authoritative: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    pivot: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    by: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Tlcconcept(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCConcept</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCConcept is a metadata reference to the Akoma Ntoso IRI of an
    ontology instance of the class Concept</ns1:comment>.
    """

    class Meta:
        name = "TLCConcept"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tlcevent(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCEvent</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCEvent is a metadata reference to the Akoma Ntoso IRI of an
    ontology instance of the class Event</ns1:comment>.
    """

    class Meta:
        name = "TLCEvent"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tlclocation(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCLocation</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCLocation is a metadata reference to the Akoma Ntoso IRI of
    an ontology instance of the class Location</ns1:comment>.
    """

    class Meta:
        name = "TLCLocation"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tlcobject(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCObject</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCObject is a metadata reference to the Akoma Ntoso IRI of an
    ontology instance of the class Object</ns1:comment>.
    """

    class Meta:
        name = "TLCObject"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tlcorganization(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCOrganization</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCOrganization is a metadata reference to the Akoma Ntoso IRI
    of an ontology instance of the class Organization</ns1:comment>.
    """

    class Meta:
        name = "TLCOrganization"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tlcperson(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCPerson</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCPerson is a metadata reference to the Akoma Ntoso IRI of an
    ontology instance of the class Person</ns1:comment>.
    """

    class Meta:
        name = "TLCPerson"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tlcprocess(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCProcess</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCProcess is a metadata reference to the Akoma Ntoso IRI of an
    ontology instance of the class Process</ns1:comment>.
    """

    class Meta:
        name = "TLCProcess"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tlcreference(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCReference</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCreference is a generic metadata reference to the Akoma Ntoso
    IRI of an ontology instance of a class specified through the name
    attribute</ns1:comment>.
    """

    class Meta:
        name = "TLCReference"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Tlcrole(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCRole</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCRole is a metadata reference to the Akoma Ntoso IRI of an
    ontology instance of the class Role</ns1:comment>.
    """

    class Meta:
        name = "TLCRole"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tlcterm(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">TLCTerm</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element TLCTerm is a metadata reference to the Akoma Ntoso IRI of an
    ontology instance of the class Term</ns1:comment>.
    """

    class Meta:
        name = "TLCTerm"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class ActiveRef(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">activeRef</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element activeRef is a metadata reference to the Akoma Ntoso IRI of a
    document that is modified by this document (i.e., an active
    references)</ns1:comment>.
    """

    class Meta:
        name = "activeRef"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AlternativeReference(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">alternativeReference</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element alternativeReference contains an alternative reference (e.g.,
    using a different namespace) for a legal reference.</ns1:comment>.
    """

    class Meta:
        name = "alternativeReference"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    for_value: None | str = field(
        default=None,
        metadata={
            "name": "for",
            "type": "Attribute",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    show_as: None | str = field(
        default=None,
        metadata={
            "name": "showAs",
            "type": "Attribute",
        },
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentType(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">argumentType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type argumentType defines the empty content model and the list
    of attributes for metadata elements in the analysis
    section</ns1:comment>.
    """

    class Meta:
        name = "argumentType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    pos: None | PosType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    exclusion: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    incomplete: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    up_to: None | str = field(
        default=None,
        metadata={
            "name": "upTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AttachmentOf(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">attachmentOf</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element attachmentOf is a metadata reference to the Akoma Ntoso IRI of
    a document of which this document is an attachment</ns1:comment>.
    """

    class Meta:
        name = "attachmentOf"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BooleanValueType(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">booleanValueType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The type
    booleanValueType specifies a boolean value attribute to FRBR
    elements.</ns1:comment>.
    """

    class Meta:
        name = "booleanValueType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    value: bool = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ComponentInfo:
    class Meta:
        name = "componentInfo"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    component_data: list[ComponentData] = field(
        default_factory=list,
        metadata={
            "name": "componentData",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class ComponentRef(SrcType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">componentRef</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element componentRef is a reference to a separate manifestation-level
    resource that holds the content of the component of the document not
    physically placed at the position specified.

    Actual resources can either be external (e.g. in the package or even in
    a different position) or internal (within the components
    element)</ns1:comment>.
    """

    class Meta:
        name = "componentRef"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Condition(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">condition</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element condition is a metadata element specifying an open set of
    conditions on the modification (non managed by Akoma
    Ntoso).</ns1:comment>.
    """

    class Meta:
        name = "condition"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    frozen: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Count(CountType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">count</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element count is a metadata container containing the value of a count
    in a vote or a quorum verification.</ns1:comment>.
    """

    class Meta:
        name = "count"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocumentRef(LinkType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">documentRef</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element documentRef is a reference to a separate work- or
    expression-level resource that should be placed in this position.

    Actual resources are external (e.g. in the package or even in a
    different position) and are (an expression or any expression of) a
    separate Work.</ns1:comment>.
    """

    class Meta:
        name = "documentRef"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Domain(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">domain</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element domain is a metadata element containing (in some non-managed
    form) the domain to which the modification applies.</ns1:comment>.
    """

    class Meta:
        name = "domain"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class EventRef(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">eventRef</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element eventRef is a metadata element specifying facts about an event
    that had an effect on the document.

    For each event, a date, a type and a document that generated the event
    must be referenced.</ns1:comment>.
    """

    class Meta:
        name = "eventRef"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    date: XmlDate | XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    type_value: None | EventType = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    originating_expression: None | bool = field(
        default=None,
        metadata={
            "name": "originatingExpression",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Foreign(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">foreign</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element foreign is a generic container for elements not belonging to
    the Akoma Ntoso namespace (e.g., mathematical formulas).

    It is a block element and thus can be placed in a
    container.</ns1:comment>.
    """

    class Meta:
        name = "foreign"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class HasAttachment(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">hasAttachment</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element hasAttachment is a metadata reference to the Akoma Ntoso IRI of
    an attachment of this document</ns1:comment>.
    """

    class Meta:
        name = "hasAttachment"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ImplicitReference(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">implicitReference</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element implicitReference contains a legal reference to a document that
    is not explicitly mentioned in the content of the
    document.</ns1:comment>.
    """

    class Meta:
        name = "implicitReference"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    for_value: None | str = field(
        default=None,
        metadata={
            "name": "for",
            "type": "Attribute",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    show_as: None | str = field(
        default=None,
        metadata={
            "name": "showAs",
            "type": "Attribute",
        },
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Jurisprudence(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">jurisprudence</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element jurisprudence is a metadata reference to the Akoma Ntoso IRI of
    a document providing jurisprudence on this document</ns1:comment>.
    """

    class Meta:
        name = "jurisprudence"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Keyword(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">keyword</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element keyword is a metadata element specifying a keyword associated
    to the FRBR expression of the document.

    Attribute dictionary (required) specifies the thesaurus out of which
    the keyword has been taken. Attribute href points to the fragment of
    text this keyword is associated to. Keywords without href attribute
    refer to the content as a whole.</ns1:comment>.
    """

    class Meta:
        name = "keyword"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    href: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    value: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    show_as: str = field(
        metadata={
            "name": "showAs",
            "type": "Attribute",
            "required": True,
        }
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    dictionary: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ListItems:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">listItems</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type listItems specifies the content model of elements ul and
    ol, and specifies just a sequence of list items (elements
    li).</ns1:comment>.
    """

    class Meta:
        name = "listItems"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    li: list[Li] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Mapping(Metareq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">mapping</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element mapping contains a reference to the permanent wId (attribute
    original) of a structure, and to the eId (attribute current) such
    structure had during the time interval included between an initial
    temporalGroup and a final temporalGroup.

    This is useful for tracking the evolving ids of documents frequently
    renumbered (e,g., bills). Every single element whose wId does not match
    its eId needs to be represented here.</ns1:comment>.
    """

    class Meta:
        name = "mapping"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    original: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    current: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    start: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    end: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Markeropt:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">markeropt</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type markeropt defines the content model and attributes shared
    by all marker elements.

    Here the eId attribute is optional</ns1:comment>.
    """

    class Meta:
        name = "markeropt"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Markerreq:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">markerreq</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type markerreq defines the content model and attributes shared
    by all marker elements.

    Here the eId attribute is required</ns1:comment>.
    """

    class Meta:
        name = "markerreq"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class New(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">new</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element new is a metadata element containing (in some non-managed form)
    the new text of the modification.

    Attribute href points to the eId of the element old it is
    substituting.</ns1:comment>.
    """

    class Meta:
        name = "new"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Old(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">old</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element old is a metadata element containing (in some non-managed form)
    the old text of the modification.

    Attribute href points to the eId of the element new it is being
    substituted by.</ns1:comment>.
    """

    class Meta:
        name = "old"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Original(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">original</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element original is a metadata reference to the Akoma Ntoso IRI of the
    original version of this document (i.e., the first
    expression)</ns1:comment>.
    """

    class Meta:
        name = "original"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class OtherAnalysis(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">otherAnalysis</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element otherAnalysis is a metadata container of any additional
    metadata analysis element that does not belong to the specific
    categories provided before.

    Anything can be placed in this element..</ns1:comment>.
    """

    class Meta:
        name = "otherAnalysis"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class PassiveRef(ReferenceType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">passiveRef</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element passiveRef is a metadata reference to the Akoma Ntoso IRI of a
    document providing modifications on this document (i.e., a passive
    references)</ns1:comment>.
    """

    class Meta:
        name = "passiveRef"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class PeriodType(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">periodType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type periodType defines the empty content model and the list of
    attributes for metadata elements in the analysis section using
    periods</ns1:comment>.
    """

    class Meta:
        name = "periodType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Portion(PortionStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">portion</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    portion is used for describing the structure and content of an
    independent portion of a document</ns1:comment>.
    """

    class Meta:
        name = "portion"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Presentation(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">presentation</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element presentation is a metadata container of any presentation
    specification for the visual rendering of Akoam Ntoso elements.

    Anything can be placed in this element.</ns1:comment>.
    """

    class Meta:
        name = "presentation"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Preservation(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">preservation</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element preservation is the metadata property containing an arbitrary
    list of elements detailing the preservation actions taken for the
    document is the respective level of the FRBR hierarchy..</ns1:comment>.
    """

    class Meta:
        name = "preservation"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Previous(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">previous</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element previous is a metadata element referring to the element (rather
    than the text) of the modification in the previous version of the
    document.

    This is especially useful when renumbering occurs, so as to specify the
    eId of the instance that was modified in the previous version.
    Attribute href points to the eId of the element being modified in the
    old version, using a full expression-level URI.</ns1:comment>.
    """

    class Meta:
        name = "previous"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Proprietary(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">proprietary</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element proprietary is a metadata container of any additional metadata
    property that does not belong to the Akoma Ntoso properties.

    Anything can be placed in this element.</ns1:comment>.
    """

    class Meta:
        name = "proprietary"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Publication(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">publication</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element publication is the metadata container specifying an official
    publication event for the FRBR expression of the
    document.</ns1:comment>.
    """

    class Meta:
        name = "publication"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    date: XmlDate | XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    show_as: str = field(
        metadata={
            "name": "showAs",
            "type": "Attribute",
            "required": True,
        }
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    number: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )


@dataclass(kw_only=True)
class Quorum(CountType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">quorum</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element quorum is a metadata container containing the value of a quorum
    in a vote or a quorum verification.</ns1:comment>.
    """

    class Meta:
        name = "quorum"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Restriction(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">restriction</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element restriction specifies information about a restriction (such as
    a jurisdiction specification) by pointing to a specific legislative,
    geographic or temporal events through the refersTo
    attribute</ns1:comment>.
    """

    class Meta:
        name = "restriction"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    type_value: RestrictionType = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Result(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">result</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element result is a metadata element specifying the overall result of
    the judgment.</ns1:comment>.
    """

    class Meta:
        name = "result"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    type_value: ResultType = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Step(AnyOtherType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">step</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element step is a metadata element specifying facts about a workflow
    step occurred to the document.

    For each event, a date, a type, an agent (and the corresponding role)
    that generated the action must be referenced. The outcome, too, can be
    specified.</ns1:comment>.
    """

    class Meta:
        name = "step"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    date: XmlDate | XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    by: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    outcome: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TimeInterval(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">timeInterval</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element timeInterval contains all the data needed to identify a
    specific time interval.

    It is built either with two dates or with a date and a duration
    (exactly two of the 'start', 'end' and 'duration' attributes can be
    specified). Values of the 'start' and 'end' attributes are NOT dates,
    but references to event elements in the corresponding metadata section.
    The refers attribute is a reference to a temporal concept belonging to
    the Akoma Ntoso ontology and specified in the references
    section</ns1:comment>.
    """

    class Meta:
        name = "timeInterval"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    start: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    end: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    duration: None | XmlDuration = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )


@dataclass(kw_only=True)
class ValueType(Metaopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">valueType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The type
    valueType specifies a value attribute to FRBR elements.</ns1:comment>.
    """

    class Meta:
        name = "valueType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    value: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    show_as: None | str = field(
        default=None,
        metadata={
            "name": "showAs",
            "type": "Attribute",
        },
    )
    short_form: None | str = field(
        default=None,
        metadata={
            "name": "shortForm",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Frbralias(ValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRalias</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRalias is the metadata property containing additional
    well-known names of the document in the respective level of the FRBR
    hierarchy</ns1:comment>.
    """

    class Meta:
        name = "FRBRalias"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Frbrauthoritative(BooleanValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRauthoritative</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRauthoritative is the metadata property containing a boolean
    value to determine whether the document contains authoritative text
    (i.e., content that is the official, authoritative product of an
    official workflow from an entity that is entrusted with generating an
    official, authoriative version of the document.</ns1:comment>.
    """

    class Meta:
        name = "FRBRauthoritative"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrcountry(ValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRcountry</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRcountry is the metadata property containing a ISO 3166-1
    Alpha-2 code for the country or jurisdiction to be used in the
    work-level IRI of this document</ns1:comment>.
    """

    class Meta:
        name = "FRBRcountry"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrformat(ValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRformat</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRformat is the metadata property containing the Internet
    Media Type specification for the data format to be used in the
    manifestation-level IRI of this document.</ns1:comment>.
    """

    class Meta:
        name = "FRBRformat"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrname(ValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRname</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRname is the metadata property containing a string for the
    title to be used in the work-level IRI of this document</ns1:comment>.
    """

    class Meta:
        name = "FRBRname"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrnumber(ValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRnumber</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRnumber is the metadata property containing a string or
    number for the number to be used in the work-level IRI of this
    document</ns1:comment>.
    """

    class Meta:
        name = "FRBRnumber"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrprescriptive(BooleanValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRprescriptive</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRprescriptive is the metadata property containing a boolean
    value to determine whether the document contains prescriptive text
    (i.e., text that is or might become prescriptive, such as an act or a
    bill) or not (such as, for instance, a non-normative resolution from an
    assembly.</ns1:comment>.
    """

    class Meta:
        name = "FRBRprescriptive"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrsubtype(ValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRsubtype</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRsubtype is the metadata property containing a string for
    the specific subtype of the document to be used in the work-level IRI
    of this document</ns1:comment>.
    """

    class Meta:
        name = "FRBRsubtype"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrthis(ValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRthis</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRthis is the metadata property containing the IRI of the
    specific component of the document</ns1:comment>.
    """

    class Meta:
        name = "FRBRthis"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbruri(ValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRuri</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRuri is the metadata property containing the IRI of the
    whole document.</ns1:comment>.
    """

    class Meta:
        name = "FRBRuri"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class FrbrversionNumber(ValueType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRversionNumber</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRversionNumber is the metadata property containing the value
    of the version number if appropriate to identify the specific
    expression here contained.

    It allows an arbitrary string.</ns1:comment>.
    """

    class Meta:
        name = "FRBRversionNumber"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Althierarchy(Basehierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">althierarchy</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type althierarchy is used by most or all the hierarchical
    elements of documents that are not act-like.</ns1:comment>.
    """

    class Meta:
        name = "althierarchy"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    administration_of_oath: list[AdministrationOfOath] = field(
        default_factory=list,
        metadata={
            "name": "administrationOfOath",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    roll_call: list[RollCall] = field(
        default_factory=list,
        metadata={
            "name": "rollCall",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    prayers: list[Prayers] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    oral_statements: list[OralStatements] = field(
        default_factory=list,
        metadata={
            "name": "oralStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    written_statements: list[WrittenStatements] = field(
        default_factory=list,
        metadata={
            "name": "writtenStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    personal_statements: list[PersonalStatements] = field(
        default_factory=list,
        metadata={
            "name": "personalStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ministerial_statements: list[MinisterialStatements] = field(
        default_factory=list,
        metadata={
            "name": "ministerialStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    resolutions: list[Resolutions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    national_interest: list[NationalInterest] = field(
        default_factory=list,
        metadata={
            "name": "nationalInterest",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    declaration_of_vote: list[DeclarationOfVote] = field(
        default_factory=list,
        metadata={
            "name": "declarationOfVote",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    communication: list[Communication] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    petitions: list[Petitions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    papers: list[Papers] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    notices_of_motion: list[NoticesOfMotion] = field(
        default_factory=list,
        metadata={
            "name": "noticesOfMotion",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    questions: list[Questions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    procedural_motions: list[ProceduralMotions] = field(
        default_factory=list,
        metadata={
            "name": "proceduralMotions",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    point_of_order: list[PointOfOrder] = field(
        default_factory=list,
        metadata={
            "name": "pointOfOrder",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    adjournment: list[Adjournment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate_section: list[DebateSection] = field(
        default_factory=list,
        metadata={
            "name": "debateSection",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    div: list[Div] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    container: list[Container] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    component_ref: list[ComponentRef] = field(
        default_factory=list,
        metadata={
            "name": "componentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    speech_group: list[SpeechGroup] = field(
        default_factory=list,
        metadata={
            "name": "speechGroup",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    question: list[Question] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other: list[Other] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    scene: list[Scene] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    narrative: list[Narrative] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    summary: list[Summary] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Application(PeriodType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">application</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element application is a metadata element specifying the period of the
    application modification.</ns1:comment>.
    """

    class Meta:
        name = "application"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Blocksopt:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">blocksopt</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type blocksopt defines the content model and attributes shared
    by all containers.

    Here the eId attribute is optional</ns1:comment>.
    """

    class Meta:
        name = "blocksopt"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Blocksreq:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">blocksreq</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type blocksreq defines the content model and attributes shared
    by all containers.

    Here the eId attribute is required</ns1:comment>.
    """

    class Meta:
        name = "blocksreq"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Br(Markeropt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">br</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element br is an HTML element and is used in Akoma Ntoso as in HTML,
    for the breaking of a line</ns1:comment>.
    """

    class Meta:
        name = "br"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Classification:
    class Meta:
        name = "classification"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    keyword: list[Keyword] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Destination(ArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">destination</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element destination is a metadata element specifying the IRI of the
    destination of the modification.</ns1:comment>.
    """

    class Meta:
        name = "destination"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Duration(PeriodType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">duration</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element duration is a metadata element specifying the period of the
    duration modification.</ns1:comment>.
    """

    class Meta:
        name = "duration"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Efficacy(PeriodType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">efficacy</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element efficacy is a metadata element specifying the period of the
    efficacy modification.</ns1:comment>.
    """

    class Meta:
        name = "efficacy"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class EolType(Markeropt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">eolType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type eolType is shared by eol and eop elements as being able to
    specify a hyphen character and a position within the next word in which
    the break can happen, and the number if any, associated to the page or
    line at issue</ns1:comment>.
    """

    class Meta:
        name = "eolType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    number: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    break_at: None | int = field(
        default=None,
        metadata={
            "name": "breakAt",
            "type": "Attribute",
        },
    )
    break_with: None | str = field(
        default=None,
        metadata={
            "name": "breakWith",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Force(PeriodType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">force</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element force is a metadata element specifying the period of the force
    modification.</ns1:comment>.
    """

    class Meta:
        name = "force"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Hierarchy(Basehierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">hierarchy</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type hierarchy is used by most or all the hierarchical elements
    of act-like documents.</ns1:comment>.
    """

    class Meta:
        name = "hierarchy"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    intro: None | Intro = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    component_ref: list[ComponentRef] = field(
        default_factory=list,
        metadata={
            "name": "componentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    clause: list[Clause] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    section: list[Section] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    part: list[Part] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    chapter: list[Chapter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    title: list[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    book: list[Book] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tome: list[Tome] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    division: list[Division] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    point: list[Point] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    indent: list[Indent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    alinea: list[Alinea] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    rule: list[Rule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subrule: list[Subrule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    proviso: list[Proviso] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subsection: list[Subsection] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subpart: list[Subpart] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subparagraph: list[Subparagraph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subchapter: list[Subchapter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subtitle: list[Subtitle] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subdivision: list[Subdivision] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subclause: list[Subclause] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    sublist: list[Sublist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    level: list[Level] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    transitional: list[Transitional] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    hcontainer: list[Hcontainer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    cross_heading: list[CrossHeading] = field(
        default_factory=list,
        metadata={
            "name": "crossHeading",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    wrap_up: None | WrapUp = field(
        default=None,
        metadata={
            "name": "wrapUp",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    content: None | Content = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title_attribute: None | str = field(
        default=None,
        metadata={
            "name": "title",
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Img(Markeropt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">img</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element img is an HTML element and is used in Akoma Ntoso as in HTML,
    for including an image.

    It is a marker.</ns1:comment>.
    """

    class Meta:
        name = "img"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    src: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    alt: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    height: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Lifecycle:
    class Meta:
        name = "lifecycle"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    event_ref: list[EventRef] = field(
        default_factory=list,
        metadata={
            "name": "eventRef",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Mappings:
    class Meta:
        name = "mappings"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    mapping: list[Mapping] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Marker(Markerreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">marker</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element marker is a generic element for a marker.

    It can be placed in a block instead of any of the other markers. The
    attribute name is required and gives a name to the
    element.</ns1:comment>.
    """

    class Meta:
        name = "marker"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class NoteRef(Markeropt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">noteRef</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element noteRef is a reference to a editorial note placed in the notes
    metadata section</ns1:comment>.
    """

    class Meta:
        name = "noteRef"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    marker: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    placement: None | PlacementType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    placement_base: None | str = field(
        default=None,
        metadata={
            "name": "placementBase",
            "type": "Attribute",
        },
    )
    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Ol(ListItems):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">ol</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element ol is an HTML element and is used in Akoma Ntoso as in HTML,
    for an ordered list of list item (elements li)</ns1:comment>.
    """

    class Meta:
        name = "ol"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class OtherReferences:
    class Meta:
        name = "otherReferences"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    implicit_reference: list[ImplicitReference] = field(
        default_factory=list,
        metadata={
            "name": "implicitReference",
            "type": "Element",
        },
    )
    alternative_reference: list[AlternativeReference] = field(
        default_factory=list,
        metadata={
            "name": "alternativeReference",
            "type": "Element",
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class ParliamentaryAnalysisType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">parliamentaryAnalysisType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type parliamentaryAnalysisType lists all the properties
    associated to elements in the parliamentary analysis.</ns1:comment>.
    """

    class Meta:
        name = "parliamentaryAnalysisType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    quorum: list[Quorum] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    count: list[Count] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    outcome: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    href: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class RefItems:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">refItems</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type refItems is a list of types of references used in the
    references section.</ns1:comment>.
    """

    class Meta:
        name = "refItems"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    original: list[Original] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    passive_ref: list[PassiveRef] = field(
        default_factory=list,
        metadata={
            "name": "passiveRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    active_ref: list[ActiveRef] = field(
        default_factory=list,
        metadata={
            "name": "activeRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    jurisprudence: list[Jurisprudence] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    has_attachment: list[HasAttachment] = field(
        default_factory=list,
        metadata={
            "name": "hasAttachment",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    attachment_of: list[AttachmentOf] = field(
        default_factory=list,
        metadata={
            "name": "attachmentOf",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlcperson: list[Tlcperson] = field(
        default_factory=list,
        metadata={
            "name": "TLCPerson",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlcorganization: list[Tlcorganization] = field(
        default_factory=list,
        metadata={
            "name": "TLCOrganization",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlcconcept: list[Tlcconcept] = field(
        default_factory=list,
        metadata={
            "name": "TLCConcept",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlcobject: list[Tlcobject] = field(
        default_factory=list,
        metadata={
            "name": "TLCObject",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlcevent: list[Tlcevent] = field(
        default_factory=list,
        metadata={
            "name": "TLCEvent",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlclocation: list[Tlclocation] = field(
        default_factory=list,
        metadata={
            "name": "TLCLocation",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlcprocess: list[Tlcprocess] = field(
        default_factory=list,
        metadata={
            "name": "TLCProcess",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlcrole: list[Tlcrole] = field(
        default_factory=list,
        metadata={
            "name": "TLCRole",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlcterm: list[Tlcterm] = field(
        default_factory=list,
        metadata={
            "name": "TLCTerm",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tlcreference: list[Tlcreference] = field(
        default_factory=list,
        metadata={
            "name": "TLCReference",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Restrictions:
    class Meta:
        name = "restrictions"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    restriction: list[Restriction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Source(ArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">source</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element source is a metadata element specifying the IRI of the source
    of the modification.</ns1:comment>.
    """

    class Meta:
        name = "source"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class TemporalGroup:
    class Meta:
        name = "temporalGroup"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    time_interval: list[TimeInterval] = field(
        default_factory=list,
        metadata={
            "name": "timeInterval",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )


@dataclass(kw_only=True)
class Ul(ListItems):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">ul</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element ul is an HTML element and is used in Akoma Ntoso as in HTML,
    for an unordered list of list item (elements li)</ns1:comment>.
    """

    class Meta:
        name = "ul"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Workflow:
    class Meta:
        name = "workflow"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    step: list[Step] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Address(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">address</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that are
    relevant to addresses</ns1:comment>.
    """

    class Meta:
        name = "address"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Adjournment(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">adjournment</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    adjournment notices</ns1:comment>.
    """

    class Meta:
        name = "adjournment"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AdministrationOfOath(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">administrationOfOath</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    the administration of an oath</ns1:comment>.
    """

    class Meta:
        name = "administrationOfOath"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Alinea(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">alinea</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "alinea" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "alinea"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AmendmentContent(Blocksopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">amendmentContent</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of an amendment
    containing the actual amendment text</ns1:comment>.
    """

    class Meta:
        name = "amendmentContent"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AmendmentHeading(Blocksopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">amendmentHeading</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of an amendment
    containing the heading</ns1:comment>.
    """

    class Meta:
        name = "amendmentHeading"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AmendmentJustification(Blocksopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">amendmentJustification</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of an amendment
    containing the justification</ns1:comment>.
    """

    class Meta:
        name = "amendmentJustification"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AmendmentReference(Blocksopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">amendmentReference</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of an amendment
    containing the reference</ns1:comment>.
    """

    class Meta:
        name = "amendmentReference"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Article(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">article</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "article" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "article"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Book(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">book</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "book" either explicitly or
    due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "book"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Chapter(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">chapter</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "chapter" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "chapter"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Clause(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">clause</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "clause" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "clause"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Communication(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">communication</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    communications from the house</ns1:comment>.
    """

    class Meta:
        name = "communication"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Content(Blocksreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">content</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element content is the final container in a hierarchy, and is where the
    blocks of text of the content of the structure are finally
    specified</ns1:comment>.
    """

    class Meta:
        name = "content"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class CoreProperties:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">coreProperties</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complexType coreProperties lists the identifying properties available
    at any of the FRBR hierarchy levels.</ns1:comment>.
    """

    class Meta:
        name = "coreProperties"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    frbrthis: Frbrthis = field(
        metadata={
            "name": "FRBRthis",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    frbruri: list[Frbruri] = field(
        default_factory=list,
        metadata={
            "name": "FRBRuri",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    frbralias: list[Frbralias] = field(
        default_factory=list,
        metadata={
            "name": "FRBRalias",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    frbrdate: list[Frbrdate] = field(
        default_factory=list,
        metadata={
            "name": "FRBRdate",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    frbrauthor: list[Frbrauthor] = field(
        default_factory=list,
        metadata={
            "name": "FRBRauthor",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    component_info: None | ComponentInfo = field(
        default=None,
        metadata={
            "name": "componentInfo",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preservation: None | Preservation = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )


@dataclass(kw_only=True)
class DebateSection(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">debateSection</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a generic structural container for all other parts of a
    debates that are not explicitly supported with a named
    element</ns1:comment>.
    """

    class Meta:
        name = "debateSection"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DeclarationOfVote(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">declarationOfVote</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that are
    relevant to the declaration of votes</ns1:comment>.
    """

    class Meta:
        name = "declarationOfVote"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Div(Blocksreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">div</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element div is an HTML element, but is NOT used in Akoma Ntoso as in
    HTML.

    Instead of being used as a generic block, Akoma Ntoso uses div as a
    generic container (as in common practice)</ns1:comment>.
    """

    class Meta:
        name = "div"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Division(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">division</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "division" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "division"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Eol(EolType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">eol</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element eol (end of line) is a marker for where in the original text
    the line breaks.

    If the line breaks within a word, place the element BEFORE the word and
    place the number of characters before the break in the attribute
    breakAt. One can also specify, if relevant, the hyphen or other
    character used to signal the break of a word at the end of the line
    with the attribute breakWith.</ns1:comment>.
    """

    class Meta:
        name = "eol"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Eop(EolType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">eop</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element eop (end of page) is a marker for where in the original text
    the page breaks.

    Do NOT use a eol element, too. If the page breaks within a word, place
    the element BEFORE the word and place the number of characters before
    the break in the attribute breakAt. One can also specify, if relevant,
    the hyphen or other character used to signal the break of a word at the
    end of the page with the attribute breakWith.</ns1:comment>.
    """

    class Meta:
        name = "eop"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Formula(Blocksreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">formula</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element formula is a section of the preface or preamble that contains a
    formulaic expression that is systematically or frequently present in a
    preface or a preamble and has e precise legal meaning (e.g. an enacting
    formula).

    Use the refersTo attribute for the specification of the actual type of
    formula.</ns1:comment>.
    """

    class Meta:
        name = "formula"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Hcontainer(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">hcontainer</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element hcontainer is a generic element for a hierarchical container.

    It can be placed in a hierarchy instead of any of the other
    hierarchical containers. The attribute name is required and gives a
    name to the element.</ns1:comment>.
    """

    class Meta:
        name = "hcontainer"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Header(Blocksopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">header</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element header is used as a container of all prefacing material of
    judgments (e.g. headers, formulas, etc.)</ns1:comment>.
    """

    class Meta:
        name = "header"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Indent(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">indent</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "indent" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "indent"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Interstitial(Blocksreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">interstitial</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element interstitial is used as a container of text elements and blocks
    that are placed for any reason between individual documents in a
    collection of documents</ns1:comment>.
    """

    class Meta:
        name = "interstitial"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Intro(Blocksreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">intro</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element intro is a heading element in a hierarchy that contains
    paragraphs introducing one or more lower hierarchical
    elements.</ns1:comment>.
    """

    class Meta:
        name = "intro"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class JudicialArgumentType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">judicialArgumentType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type judicialArgumentType lists all the properties associated
    to judicial elements.</ns1:comment>.
    """

    class Meta:
        name = "judicialArgumentType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    source: list[Source] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    destination: list[Destination] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    condition: None | Condition = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    exclusion: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    incomplete: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )


@dataclass(kw_only=True)
class Level(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">level</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "level" either explicitly or
    due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "level"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class List(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">list</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "list" either explicitly or
    due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "list"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class LongTitle(Blocksreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">longTitle</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element longTitle is the section of the preface or coverPage that is
    called long title</ns1:comment>.
    """

    class Meta:
        name = "longTitle"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class MinisterialStatements(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">ministerialStatements</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    written statements by participants</ns1:comment>.
    """

    class Meta:
        name = "ministerialStatements"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class ModificationType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">modificationType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type modificationType lists all the properties associated to
    modification elements.</ns1:comment>.
    """

    class Meta:
        name = "modificationType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    source: list[Source] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    destination: list[Destination] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    force: None | Force = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    efficacy: None | Efficacy = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    application: None | Application = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    duration: None | Duration = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    condition: None | Condition = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    exclusion: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    incomplete: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )


@dataclass(kw_only=True)
class NationalInterest(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">nationalInterest</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    resolutions</ns1:comment>.
    """

    class Meta:
        name = "nationalInterest"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class NoticesOfMotion(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">noticesOfMotion</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that are
    relevant to the notices of motions</ns1:comment>.
    """

    class Meta:
        name = "noticesOfMotion"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class OralStatements(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">oralStatements</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    oral statements by participants</ns1:comment>.
    """

    class Meta:
        name = "oralStatements"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Other(Blocksreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">other</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element other is a container of parts of a debate that are not
    speeches, nor scene comments (e.g., lists of papers,
    etc.)</ns1:comment>.
    """

    class Meta:
        name = "other"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Papers(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">papers</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that are
    relevant to the display of papers</ns1:comment>.
    """

    class Meta:
        name = "papers"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Paragraph(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">paragraph</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "paragraph" either
    explicitly or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "paragraph"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Part(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">part</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "part" either explicitly or
    due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "part"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class PersonalStatements(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">personalStatements</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    written statements by participants</ns1:comment>.
    """

    class Meta:
        name = "personalStatements"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Petitions(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">petitions</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that are
    relevant to petitions</ns1:comment>.
    """

    class Meta:
        name = "petitions"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Point(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">point</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "point" either explicitly or
    due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "point"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class PointOfOrder(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">pointOfOrder</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that are
    relevant to points of order</ns1:comment>.
    """

    class Meta:
        name = "pointOfOrder"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Prayers(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">prayers</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    prayers</ns1:comment>.
    """

    class Meta:
        name = "prayers"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class ProceduralMotions(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">proceduralMotions</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that are
    relevant to procedural motions</ns1:comment>.
    """

    class Meta:
        name = "proceduralMotions"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Proviso(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">proviso</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "proviso" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "proviso"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Questions(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">questions</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that are
    relevant to questions</ns1:comment>.
    """

    class Meta:
        name = "questions"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class QuorumVerification(ParliamentaryAnalysisType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">quorumVerification</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element quorumVerification is a metadata container containing
    information about an event of quorum verification happened within a
    debate.</ns1:comment>.
    """

    class Meta:
        name = "quorumVerification"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Recount(ParliamentaryAnalysisType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">recount</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element recount is a metadata container containing information about an
    event of a recount happened within a debate.</ns1:comment>.
    """

    class Meta:
        name = "recount"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class References(RefItems):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">references</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element references is a metadata container of all the references to
    entities external to the document mentioned in the document.

    They include references to legal documents of any form,a s well as
    references to people, organizations, events, roles, concepts, and
    anything else is managed by the Akoma Ntoso ontology.</ns1:comment>.
    """

    class Meta:
        name = "references"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Resolutions(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">resolutions</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    resolutions</ns1:comment>.
    """

    class Meta:
        name = "resolutions"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class RollCall(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">rollCall</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain a
    roll call of individuals</ns1:comment>.
    """

    class Meta:
        name = "rollCall"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Rule(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">rule</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "rule" either explicitly or
    due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "rule"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Section(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">section</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "section" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "section"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class SpeechGroup(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">speechGroup</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element speechGroup is a container of speech elements.

    This element is meant to pooint out, in a complex sequence of
    individual speech elements, the main contributor, i.e., the individual
    speech who was introducedand expected and that is causing the complex
    sequence that follows. Attributes by, as and to are those of the main
    speech.</ns1:comment>.
    """

    class Meta:
        name = "speechGroup"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    by: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )
    start_time: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "startTime",
            "type": "Attribute",
        },
    )
    end_time: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "endTime",
            "type": "Attribute",
        },
    )
    to: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subchapter(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subchapter</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "subchapter" either
    explicitly or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "subchapter"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Subclause(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subclause</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "subclause" either
    explicitly or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "subclause"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Subdivision(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subdivision</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "subdivision" either
    explicitly or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "subdivision"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Sublist(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">sublist</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "sublist" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "sublist"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Subparagraph(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subparagraph</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "subparagraph" either
    explicitly or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "subparagraph"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Subpart(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subpart</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "subpart" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "subpart"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Subrule(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subrule</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "subrule" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "subrule"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Subsection(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subsection</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "subsection" either
    explicitly or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "subsection"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Subtitle(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subtitle</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "subtitle" either explicitly
    or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "subtitle"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Td(Blocksopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">td</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element td is an HTML element and is used in Akoma Ntoso as in HTML,
    for a data cell of a table</ns1:comment>.
    """

    class Meta:
        name = "td"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    rowspan: int = field(
        default=1,
        metadata={
            "type": "Attribute",
        },
    )
    colspan: int = field(
        default=1,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TemporalData:
    class Meta:
        name = "temporalData"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    temporal_group: list[TemporalGroup] = field(
        default_factory=list,
        metadata={
            "name": "temporalGroup",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Th(Blocksopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">th</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element th is an HTML element and is used in Akoma Ntoso as in HTML,
    for a header cell of a table</ns1:comment>.
    """

    class Meta:
        name = "th"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    rowspan: int = field(
        default=1,
        metadata={
            "type": "Attribute",
        },
    )
    colspan: int = field(
        default=1,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Title(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">title</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "title" either explicitly or
    due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "title"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tome(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">tome</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "tome" either explicitly or
    due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "tome"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Transitional(Hierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">transitional</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a hierarchical container called "transitional" either
    explicitly or due to the local tradition</ns1:comment>.
    """

    class Meta:
        name = "transitional"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Voting(ParliamentaryAnalysisType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">voting</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element voting is a metadata container containing information about an
    event of a vote happened within a debate.</ns1:comment>.
    """

    class Meta:
        name = "voting"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class WrapUp(Blocksreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">wrapUp</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element wrapUp is a concluding element in a hierarchy that contains
    paragraphs wrapping up the preceding lower hierarchical
    elements.</ns1:comment>.
    """

    class Meta:
        name = "wrapUp"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class WrittenStatements(Althierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">writtenStatements</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for parts of a debates that contain
    written statements by participants</ns1:comment>.
    """

    class Meta:
        name = "writtenStatements"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrexpression(CoreProperties):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRExpression</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRExpression is the metadata container of identifying
    properties related to the Expression level according to the FRBR
    hierarchy</ns1:comment>.
    """

    class Meta:
        name = "FRBRExpression"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    frbrversion_number: None | FrbrversionNumber = field(
        default=None,
        metadata={
            "name": "FRBRversionNumber",
            "type": "Element",
        },
    )
    frbrauthoritative: None | Frbrauthoritative = field(
        default=None,
        metadata={
            "name": "FRBRauthoritative",
            "type": "Element",
        },
    )
    frbrmaster_expression: None | FrbrmasterExpression = field(
        default=None,
        metadata={
            "name": "FRBRmasterExpression",
            "type": "Element",
        },
    )
    frbrlanguage: list[Frbrlanguage] = field(
        default_factory=list,
        metadata={
            "name": "FRBRlanguage",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    frbrtranslation: list[Frbrtranslation] = field(
        default_factory=list,
        metadata={
            "name": "FRBRtranslation",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Frbritem(CoreProperties):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRItem</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRItem is the metadata container of identifying properties
    related to the Item level according to the FRBR
    hierarchy.</ns1:comment>.
    """

    class Meta:
        name = "FRBRItem"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Frbrmanifestation(CoreProperties):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRManifestation</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRManifestation is the metadata container of identifying
    properties related to the Manifestation level according to the FRBR
    hierarchy</ns1:comment>.
    """

    class Meta:
        name = "FRBRManifestation"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    frbrportion: None | Frbrportion = field(
        default=None,
        metadata={
            "name": "FRBRportion",
            "type": "Element",
        },
    )
    frbrformat: None | Frbrformat = field(
        default=None,
        metadata={
            "name": "FRBRformat",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Frbrwork(CoreProperties):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">FRBRWork</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element FRBRWork is the metadata container of identifying properties
    related to the Work level according to the FRBR
    hierarchy</ns1:comment>.
    """

    class Meta:
        name = "FRBRWork"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    frbrcountry: Frbrcountry = field(
        metadata={
            "name": "FRBRcountry",
            "type": "Element",
            "required": True,
        }
    )
    frbrsubtype: None | Frbrsubtype = field(
        default=None,
        metadata={
            "name": "FRBRsubtype",
            "type": "Element",
        },
    )
    frbrnumber: list[Frbrnumber] = field(
        default_factory=list,
        metadata={
            "name": "FRBRnumber",
            "type": "Element",
        },
    )
    frbrname: list[Frbrname] = field(
        default_factory=list,
        metadata={
            "name": "FRBRname",
            "type": "Element",
        },
    )
    frbrprescriptive: None | Frbrprescriptive = field(
        default=None,
        metadata={
            "name": "FRBRprescriptive",
            "type": "Element",
        },
    )
    frbrauthoritative: None | Frbrauthoritative = field(
        default=None,
        metadata={
            "name": "FRBRauthoritative",
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class AmendmentBodyType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">amendmentBodyType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    amendmentBodyType specifies a content model of the main hierarchy of a
    amendment document</ns1:comment>.
    """

    class Meta:
        name = "amendmentBodyType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    amendment_heading: list[AmendmentHeading] = field(
        default_factory=list,
        metadata={
            "name": "amendmentHeading",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    amendment_content: list[AmendmentContent] = field(
        default_factory=list,
        metadata={
            "name": "amendmentContent",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    amendment_reference: list[AmendmentReference] = field(
        default_factory=list,
        metadata={
            "name": "amendmentReference",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    amendment_justification: list[AmendmentJustification] = field(
        default_factory=list,
        metadata={
            "name": "amendmentJustification",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Applies(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">applies</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element applies is a metadata element specifying a reference to a
    source applyed by the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "applies"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class BodyType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">bodyType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    bodyType specifies a content model of the main hierarchy of a
    hierarchical document (e.g, an act or a bill)</ns1:comment>.
    """

    class Meta:
        name = "bodyType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    component_ref: list[ComponentRef] = field(
        default_factory=list,
        metadata={
            "name": "componentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    clause: list[Clause] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    section: list[Section] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    part: list[Part] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    chapter: list[Chapter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    title: list[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    book: list[Book] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tome: list[Tome] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    division: list[Division] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    point: list[Point] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    indent: list[Indent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    alinea: list[Alinea] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    rule: list[Rule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subrule: list[Subrule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    proviso: list[Proviso] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subsection: list[Subsection] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subpart: list[Subpart] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subparagraph: list[Subparagraph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subchapter: list[Subchapter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subtitle: list[Subtitle] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subdivision: list[Subdivision] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subclause: list[Subclause] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    sublist: list[Sublist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    level: list[Level] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    transitional: list[Transitional] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    hcontainer: list[Hcontainer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title_attribute: None | str = field(
        default=None,
        metadata={
            "name": "title",
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Contrasts(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">contrasts</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element contrasts is a metadata element specifying a reference to a
    source contrasted by the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "contrasts"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DebateBodyType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">debateBodyType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    debateBodyType specifies a content model of the main hierarchy of a
    debate</ns1:comment>.
    """

    class Meta:
        name = "debateBodyType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    administration_of_oath: list[AdministrationOfOath] = field(
        default_factory=list,
        metadata={
            "name": "administrationOfOath",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    roll_call: list[RollCall] = field(
        default_factory=list,
        metadata={
            "name": "rollCall",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    prayers: list[Prayers] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    oral_statements: list[OralStatements] = field(
        default_factory=list,
        metadata={
            "name": "oralStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    written_statements: list[WrittenStatements] = field(
        default_factory=list,
        metadata={
            "name": "writtenStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    personal_statements: list[PersonalStatements] = field(
        default_factory=list,
        metadata={
            "name": "personalStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    ministerial_statements: list[MinisterialStatements] = field(
        default_factory=list,
        metadata={
            "name": "ministerialStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    resolutions: list[Resolutions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    national_interest: list[NationalInterest] = field(
        default_factory=list,
        metadata={
            "name": "nationalInterest",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    declaration_of_vote: list[DeclarationOfVote] = field(
        default_factory=list,
        metadata={
            "name": "declarationOfVote",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    communication: list[Communication] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    petitions: list[Petitions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    papers: list[Papers] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    notices_of_motion: list[NoticesOfMotion] = field(
        default_factory=list,
        metadata={
            "name": "noticesOfMotion",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    questions: list[Questions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    procedural_motions: list[ProceduralMotions] = field(
        default_factory=list,
        metadata={
            "name": "proceduralMotions",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    point_of_order: list[PointOfOrder] = field(
        default_factory=list,
        metadata={
            "name": "pointOfOrder",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    adjournment: list[Adjournment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    debate_section: list[DebateSection] = field(
        default_factory=list,
        metadata={
            "name": "debateSection",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Derogates(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">derogates</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element derogates is a metadata element specifying a reference to a
    source derogated by the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "derogates"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DissentsFrom(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">dissentsFrom</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element dissentsFrom is a metadata element specifying a reference to a
    source dissented from the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "dissentsFrom"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Distinguishes(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">distinguishes</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element distinguishes is a metadata element specifying a reference to a
    source being distinguished by the argument being
    described.</ns1:comment>.
    """

    class Meta:
        name = "distinguishes"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class EfficacyMod(ModificationType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">efficacyMod</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element efficacyMod is a metadata element specifying an (active or
    passive) modification in efficacy for the document.</ns1:comment>.
    """

    class Meta:
        name = "efficacyMod"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    type_value: EfficacyMods = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Extends(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">extends</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element extends is a metadata element specifying a reference to a
    source extended by the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "extends"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class ForceMod(ModificationType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">forceMod</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element forceMod is a metadata element specifying an (active or
    passive) modification in force for the document.</ns1:comment>.
    """

    class Meta:
        name = "forceMod"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    type_value: ForceMods = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Inline1:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">inline</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type inline defines the content model and attributes shared by
    all blocks and inlines.

    Here the eId attribute is optional</ns1:comment>.
    """

    class Meta:
        name = "inline"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "ref",
                    "type": ForwardRef("Ref"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mref",
                    "type": ForwardRef("Mref"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "rref",
                    "type": ForwardRef("Rref"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mod",
                    "type": ForwardRef("Mod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mmod",
                    "type": ForwardRef("Mmod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "rmod",
                    "type": ForwardRef("Rmod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "remark",
                    "type": ForwardRef("Remark"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "recordedTime",
                    "type": ForwardRef("RecordedTime"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "vote",
                    "type": ForwardRef("Vote"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "outcome",
                    "type": ForwardRef("Outcome"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "ins",
                    "type": ForwardRef("Ins"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "del",
                    "type": ForwardRef("Del"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "omissis",
                    "type": ForwardRef("Omissis"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "embeddedText",
                    "type": ForwardRef("EmbeddedText"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "embeddedStructure",
                    "type": ForwardRef("EmbeddedStructure"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "opinion",
                    "type": ForwardRef("Opinion"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "placeholder",
                    "type": ForwardRef("Placeholder"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "fillIn",
                    "type": ForwardRef("FillIn"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "decoration",
                    "type": ForwardRef("Decoration"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "b",
                    "type": ForwardRef("B"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "i",
                    "type": ForwardRef("I"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "a",
                    "type": ForwardRef("A"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "u",
                    "type": ForwardRef("U"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "abbr",
                    "type": ForwardRef("Abbr"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "span",
                    "type": ForwardRef("Span"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docType",
                    "type": ForwardRef("DocType"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docTitle",
                    "type": ForwardRef("DocTitle"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docNumber",
                    "type": ForwardRef("DocNumber"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docProponent",
                    "type": ForwardRef("DocProponent"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docDate",
                    "type": ForwardRef("DocDate"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "legislature",
                    "type": ForwardRef("Legislature"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "session",
                    "type": ForwardRef("Session"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "shortTitle",
                    "type": ForwardRef("ShortTitle"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docAuthority",
                    "type": ForwardRef("DocAuthority"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docPurpose",
                    "type": ForwardRef("DocPurpose"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docCommittee",
                    "type": ForwardRef("DocCommittee"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docIntroducer",
                    "type": ForwardRef("DocIntroducer"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docStage",
                    "type": ForwardRef("DocStage"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docStatus",
                    "type": ForwardRef("DocStatus"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docJurisdiction",
                    "type": ForwardRef("DocJurisdiction"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docketNumber",
                    "type": ForwardRef("DocketNumber"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "date",
                    "type": ForwardRef("Date"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "time",
                    "type": ForwardRef("Time"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "person",
                    "type": ForwardRef("Person"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "organization",
                    "type": ForwardRef("Organization"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "concept",
                    "type": ForwardRef("Concept"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "object",
                    "type": ForwardRef("Object"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "event",
                    "type": ForwardRef("Event"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "location",
                    "type": ForwardRef("Location"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "process",
                    "type": ForwardRef("Process"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "role",
                    "type": ForwardRef("Role"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "term",
                    "type": ForwardRef("Term"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "quantity",
                    "type": ForwardRef("Quantity"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "def",
                    "type": ForwardRef("Def"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "entity",
                    "type": ForwardRef("Entity"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "courtType",
                    "type": ForwardRef("CourtType"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "neutralCitation",
                    "type": ForwardRef("NeutralCitation"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "party",
                    "type": ForwardRef("Party"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "judge",
                    "type": ForwardRef("Judge"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "lawyer",
                    "type": ForwardRef("Lawyer"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "signature",
                    "type": ForwardRef("Signature"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "argument",
                    "type": ForwardRef("Argument"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "affectedDocument",
                    "type": ForwardRef("AffectedDocument"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "relatedDocument",
                    "type": ForwardRef("RelatedDocument"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "change",
                    "type": ForwardRef("Change"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "inline",
                    "type": ForwardRef("Inline"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "noteRef",
                    "type": NoteRef,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "eol",
                    "type": Eol,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "eop",
                    "type": Eop,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "marker",
                    "type": Marker,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "authorialNote",
                    "type": ForwardRef("AuthorialNote"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "subFlow",
                    "type": ForwardRef("SubFlow"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
            ),
        },
    )


@dataclass(kw_only=True)
class IsAnalogTo(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">isAnalogTo</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element isAnalogTo is a metadata element specifying a reference to a
    source analog to the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "isAnalogTo"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class LegalSystemMod(ModificationType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">legalSystemMod</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element legalSystemMod is a metadata element specifying an (active or
    passive) modification in the legal system for the
    document.</ns1:comment>.
    """

    class Meta:
        name = "legalSystemMod"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    type_value: LegalSystemMods = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class MeaningMod(ModificationType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">meaningMod</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element meaningMod is a metadata element specifying an (active or
    passive) modification in meaning for the document.</ns1:comment>.
    """

    class Meta:
        name = "meaningMod"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    domain: None | Domain = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    type_value: MeaningMods = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Overrules(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">overrules</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element overrules is a metadata element specifying a reference to a
    source overruled by the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "overrules"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class ParliamentaryAnalysis:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">parliamentaryAnalysis</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type parliamentaryAnalysis is a list of all the parliamentary
    analysis elements that can be used on the analysis of a
    debate</ns1:comment>.
    """

    class Meta:
        name = "parliamentaryAnalysis"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    quorum_verification: list[QuorumVerification] = field(
        default_factory=list,
        metadata={
            "name": "quorumVerification",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    voting: list[Voting] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    recount: list[Recount] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )


@dataclass(kw_only=True)
class PutsInQuestion(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">putsInQuestion</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element putsInQuestions is a metadata element specifying a reference to
    a source questioned by the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "putsInQuestion"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Restricts(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">restricts</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element restricts is a metadata element specifying a reference to a
    source restricted by the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "restricts"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class ScopeMod(ModificationType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">scopeMod</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element scopeMod is a metadata element specifying an (active or
    passive) modification in scope for the document.</ns1:comment>.
    """

    class Meta:
        name = "scopeMod"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    domain: None | Domain = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    type_value: ScopeMods = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Supports(JudicialArgumentType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">supports</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element supports is a metadata element specifying a reference to a
    source supported by the argument being described.</ns1:comment>.
    """

    class Meta:
        name = "supports"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class TextualMod(ModificationType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">textualMod</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element textualMod is a metadata element specifying an (active or
    passive) textual modification for the document.</ns1:comment>.
    """

    class Meta:
        name = "textualMod"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    previous: None | Previous = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    old: list[Old] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    new: list[New] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    type_value: TextualMods = field(
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Tr:
    class Meta:
        name = "tr"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    th: list[Th] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    td: list[Td] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Amendments:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Amendments</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type Amendments is a list of all the amendment elements that
    can be used on a document analysis</ns1:comment>.
    """

    class Meta:
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    textual_mod: list[TextualMod] = field(
        default_factory=list,
        metadata={
            "name": "textualMod",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    meaning_mod: list[MeaningMod] = field(
        default_factory=list,
        metadata={
            "name": "meaningMod",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    scope_mod: list[ScopeMod] = field(
        default_factory=list,
        metadata={
            "name": "scopeMod",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    force_mod: list[ForceMod] = field(
        default_factory=list,
        metadata={
            "name": "forceMod",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    efficacy_mod: list[EfficacyMod] = field(
        default_factory=list,
        metadata={
            "name": "efficacyMod",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    legal_system_mod: list[LegalSystemMod] = field(
        default_factory=list,
        metadata={
            "name": "legalSystemMod",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )


@dataclass(kw_only=True)
class A(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">a</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element a is an HTML element and is used in Akoma Ntoso as in HTML, for
    the generic link to a web resource (NOT to an Akoma Ntoso document: use
    ref for that).

    It is an inline.</ns1:comment>.
    """

    class Meta:
        name = "a"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    target: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Abbr(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">abbr</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element abbr is an HTML element and is used in Akoma Ntoso as in HTML,
    for the specification of an abbreviation or an acronym (an inline).

    As in HTML, use attribute title to specify the full expansion of the
    abbreviation or acronym.</ns1:comment>.
    """

    class Meta:
        name = "abbr"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AffectedDocument(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">affectedDocument</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element affectedDocument is an inline element within preamble to
    identify the document that this amendment affects</ns1:comment>.
    """

    class Meta:
        name = "affectedDocument"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class AmendmentBody(AmendmentBodyType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">amendmentBody</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element amendmentBody is the container of the main hierarchy of a
    amendment document</ns1:comment>.
    """

    class Meta:
        name = "amendmentBody"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Argument(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">argument</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element argument is an inline element within judgments for classifying
    the arguments in the motivation part of the judgment</ns1:comment>.
    """

    class Meta:
        name = "argument"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class B(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">b</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element b is an HTML element and is used in Akoma Ntoso as in HTML, for
    the bold style (an inline)</ns1:comment>.
    """

    class Meta:
        name = "b"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Block(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">block</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element block is a generic element for a block.

    It can be placed in a container instead of any of the other blocks. The
    attribute name is required and gives a name to the
    element.</ns1:comment>.
    """

    class Meta:
        name = "block"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Body(BodyType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">body</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element body is the container of the main hierarchy of a hierarchical
    document (e.g, an act or a bill)</ns1:comment>.
    """

    class Meta:
        name = "body"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Caption(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">caption</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element caption is an HTML element and is used in Akoma Ntoso as in
    HTML, for the caption of a table (a block)</ns1:comment>.
    """

    class Meta:
        name = "caption"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Change(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">change</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element change is an inline element that identifies the changes
    expressed in the two columns of an amendment document</ns1:comment>.
    """

    class Meta:
        name = "change"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class CourtType(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">courtType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element courtType is an inline element within judgments to identify the
    string used by the document for the type of the court doing the
    judgment</ns1:comment>.
    """

    class Meta:
        name = "courtType"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Date(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">date</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element date is an inline element to identify a date expressed in the
    text and to propose a normalized representation in the date
    attribute.</ns1:comment>.
    """

    class Meta:
        name = "date"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    date: XmlDate | XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DebateBody(DebateBodyType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">debateBody</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element debateBody is the container of the main hierarchy of a
    debate</ns1:comment>.
    """

    class Meta:
        name = "debateBody"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Decoration(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">decoration</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element decoration is an inline element to represent a decorative
    aspect that is present in the orignal text and that is meant as
    additional information to the text (e.g., the annotation 'new' on the
    side of a freshly inserted structure.</ns1:comment>.
    """

    class Meta:
        name = "decoration"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Def(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">def</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element def is an inline element used for the definition of a term used
    in the rest of the document</ns1:comment>.
    """

    class Meta:
        name = "def"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Del(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">del</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element del is an inline element for the specification of editorial
    deletions</ns1:comment>.
    """

    class Meta:
        name = "del"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocAuthority(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docAuthority</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docAuthority is an inline element within preface to identify
    the string used by the document detailing the Auhtority to which the
    document was submitted</ns1:comment>.
    """

    class Meta:
        name = "docAuthority"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocCommittee(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docCommittee</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docCommittee is an inline element within preface to identify
    the string used by the document detailing the committee within which
    the document originated</ns1:comment>.
    """

    class Meta:
        name = "docCommittee"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    value: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DocDate(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docDate</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docDate is an inline element within preface to identify the
    string used by the document for its own date(s).

    Documents with multiple dates may use multiple docDate
    elements.</ns1:comment>.
    """

    class Meta:
        name = "docDate"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    date: XmlDate | XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class DocIntroducer(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docIntroducer</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docIntroducer is an inline element within preface to identify
    the string used by the document detailing the individual introducing of
    the document</ns1:comment>.
    """

    class Meta:
        name = "docIntroducer"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocJurisdiction(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docJurisdiction</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docJurisdiction is an inline element within preface to identify
    the string used by the document detailing the jurisdiction of the
    document</ns1:comment>.
    """

    class Meta:
        name = "docJurisdiction"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocNumber(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docNumber</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docNumber is an inline element within preface to identify the
    string used by the document for its own number</ns1:comment>.
    """

    class Meta:
        name = "docNumber"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocProponent(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docProponent</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docProponent is an inline element within preface to identify
    the string used by the document for its proponent</ns1:comment>.
    """

    class Meta:
        name = "docProponent"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DocPurpose(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docPurpose</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docPurpose is an inline element within preface to identify the
    string used by the document detailing its own purpose</ns1:comment>.
    """

    class Meta:
        name = "docPurpose"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocStage(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docStage</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docStage is an inline element within preface to identify the
    string used by the document detailing the stage in which the document
    sits</ns1:comment>.
    """

    class Meta:
        name = "docStage"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocStatus(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docStatus</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docStatus is an inline element within preface to identify the
    string used by the document detailing the status of the
    document</ns1:comment>.
    """

    class Meta:
        name = "docStatus"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocTitle(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docTitle</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docTitle is an inline element within preface to identify the
    string used by the document for its own title</ns1:comment>.
    """

    class Meta:
        name = "docTitle"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocType(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docType is an inline element within preface to identify the
    string used by the document for its own type</ns1:comment>.
    """

    class Meta:
        name = "docType"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocketNumber(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docketNumber</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element docketNumber is an inline element within preface to identify
    the string used by the document for the number of the docket, case,
    file, etc which the document belongs to</ns1:comment>.
    """

    class Meta:
        name = "docketNumber"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class EmbeddedText(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">embeddedText</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element embeddedText is an inline element containing a string used as
    an extract from another document.

    Attribute quote is used to specify the quote character used in the
    original; no quote attribute implies that the quote is left in the
    text; quote="" implies that there is no quote character.</ns1:comment>.
    """

    class Meta:
        name = "embeddedText"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    start_quote: None | str = field(
        default=None,
        metadata={
            "name": "startQuote",
            "type": "Attribute",
        },
    )
    end_quote: None | str = field(
        default=None,
        metadata={
            "name": "endQuote",
            "type": "Attribute",
        },
    )
    inline_quote: None | str = field(
        default=None,
        metadata={
            "name": "inlineQuote",
            "type": "Attribute",
        },
    )
    href: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class FillIn(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">fillIn</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element fillIn is an inline element shown as a dotted line or any other
    typoaphical characteristics to represent a fill-in element in a printed
    form, that is as ane example of an actual form.

    It is NOT meant to be used for form elements as in HTML, i.e. as a way
    to collect input from the reader and deliver to some server-side
    process.</ns1:comment>.
    """

    class Meta:
        name = "fillIn"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    width: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class From(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">from</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element from is a heading element in a debate that contains the name or
    role or a reference to the person doing the speech</ns1:comment>.
    """

    class Meta:
        name = "from"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class I(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">i</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element i is an HTML element and is used in Akoma Ntoso as in HTML, for
    the italic style (an inline)</ns1:comment>.
    """

    class Meta:
        name = "i"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Identification:
    class Meta:
        name = "identification"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    frbrwork: Frbrwork = field(
        metadata={
            "name": "FRBRWork",
            "type": "Element",
            "required": True,
        }
    )
    frbrexpression: Frbrexpression = field(
        metadata={
            "name": "FRBRExpression",
            "type": "Element",
            "required": True,
        }
    )
    frbrmanifestation: Frbrmanifestation = field(
        metadata={
            "name": "FRBRManifestation",
            "type": "Element",
            "required": True,
        }
    )
    frbritem: None | Frbritem = field(
        default=None,
        metadata={
            "name": "FRBRItem",
            "type": "Element",
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Inline(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">inline</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element inline is a generic element for an inline.

    It can be placed inside a block instead of any of the other inlines.
    The attribute name is required and gives a name to the
    element.</ns1:comment>.
    """

    class Meta:
        name = "inline"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Ins(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">ins</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element ins is an inline element for the specification of editorial
    insertions</ns1:comment>.
    """

    class Meta:
        name = "ins"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class JudicialArguments:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">judicialArguments</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type judicialArguments is a list of all the judicial analysis
    elements that can be used on the analysis of a judgment</ns1:comment>.
    """

    class Meta:
        name = "judicialArguments"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    result: Result = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    supports: list[Supports] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    is_analog_to: list[IsAnalogTo] = field(
        default_factory=list,
        metadata={
            "name": "isAnalogTo",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    applies: list[Applies] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    extends: list[Extends] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    restricts: list[Restricts] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    derogates: list[Derogates] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    contrasts: list[Contrasts] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    overrules: list[Overrules] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    dissents_from: list[DissentsFrom] = field(
        default_factory=list,
        metadata={
            "name": "dissentsFrom",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    puts_in_question: list[PutsInQuestion] = field(
        default_factory=list,
        metadata={
            "name": "putsInQuestion",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    distinguishes: list[Distinguishes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )


@dataclass(kw_only=True)
class Legislature(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">legislature</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element legislature is an inline element within preface to identify the
    string used by the document for the legislature relative to the
    document.

    Use #refersTo to a TLCEvent to refer to the event of the specific
    legislature.</ns1:comment>.
    """

    class Meta:
        name = "legislature"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    value: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ListIntroduction(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">listIntroduction</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element listIntroduction is an optional element of blockList before any
    item of the list itself.</ns1:comment>.
    """

    class Meta:
        name = "listIntroduction"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class ListWrapUp(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">listWrapUp</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element listWrapUp is an optional element of blockList after all items
    of the list itself.</ns1:comment>.
    """

    class Meta:
        name = "listWrapUp"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Mref(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">mref</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element mref is an inline element containing multiple references (each
    in turn represented by a ref element)</ns1:comment>.
    """

    class Meta:
        name = "mref"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Narrative(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">narrative</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element narrative is a block element in a debate to mark description in
    the third person of events taking place in the meeting, e.g. "Mr X.
    takes the Chair"</ns1:comment>.
    """

    class Meta:
        name = "narrative"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class NeutralCitation(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">neutralCitation</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element neutralCitation is an inline element within judgments to
    identify the string declared by the document as being the neutral
    citation for the judgment</ns1:comment>.
    """

    class Meta:
        name = "neutralCitation"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Num(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">num</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element num is a heading element in a hierarchy that contains a number
    or any other ordered mechanism to identify the
    structure.</ns1:comment>.
    """

    class Meta:
        name = "num"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Omissis(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">omissis</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element omissis is an inline element for the specification of a text
    that substitutes a textual omission (e.g., dots, spaces, the word
    "omissis", etc.</ns1:comment>.
    """

    class Meta:
        name = "omissis"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Opinion(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">opinion</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element opinion is an inline element to identify where the document
    defines the opinion of an actor</ns1:comment>.
    """

    class Meta:
        name = "opinion"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    by: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    type_value: None | OpinionType = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Outcome(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">outcome</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element outcome is an inline that wraps the outcome of a
    vote</ns1:comment>.
    """

    class Meta:
        name = "outcome"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class P(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">p</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element p is an HTML element and is used in Akoma Ntoso as in HTML, for
    the generic paragraph of text (a block)</ns1:comment>.
    """

    class Meta:
        name = "p"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Parliamentary(ParliamentaryAnalysis):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">parliamentary</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element parliamentary is a metadata container of the analysis of the
    events of a debate.</ns1:comment>.
    """

    class Meta:
        name = "parliamentary"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Placeholder(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">placeholder</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element placeholder is an inline element containing the text of a
    computable expression (e.g., '30 days after the publication of this
    act') that can be replaced editorially with an actual
    value</ns1:comment>.
    """

    class Meta:
        name = "placeholder"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    original_text: None | str = field(
        default=None,
        metadata={
            "name": "originalText",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class QuotedText(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">quotedText</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element quotedText is an inline element containing a small string that
    is used either as the text being replaced, or the replacement, or the
    positioning at which some modification should take place.

    Attribute quote is used to specify the quote character used in the
    original; no quote attribute implies that the quote is left in the
    text; quote="" implies that there is no quote character. Attribute for
    is used to point to the eId of the corresponding ref
    element.</ns1:comment>.
    """

    class Meta:
        name = "quotedText"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    start_quote: None | str = field(
        default=None,
        metadata={
            "name": "startQuote",
            "type": "Attribute",
        },
    )
    end_quote: None | str = field(
        default=None,
        metadata={
            "name": "endQuote",
            "type": "Attribute",
        },
    )
    inline_quote: None | str = field(
        default=None,
        metadata={
            "name": "inlineQuote",
            "type": "Attribute",
        },
    )
    for_value: None | str = field(
        default=None,
        metadata={
            "name": "for",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class RecordedTime(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">recordedTime</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element recordedTime is an inline element for the specification of an
    explicit mention of a time (e.g., in a debate)</ns1:comment>.
    """

    class Meta:
        name = "recordedTime"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    type_value: None | TimeType = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    time: XmlTime | XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class RelatedDocument(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">relatedDocument</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element relatedDocument is an inline element to identify the document
    for which this document is a report of</ns1:comment>.
    """

    class Meta:
        name = "relatedDocument"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Remark(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">remark</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element remark is an inline element for the specification of editorial
    remarks (e.g., applauses, laughters, etc.) especially within debate
    records</ns1:comment>.
    """

    class Meta:
        name = "remark"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    type_value: None | RemarkType = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Scene(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">scene</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element scene is a container of descriptions of the scene elements
    happening in a given moment during a debate (e.g.,
    applauses)</ns1:comment>.
    """

    class Meta:
        name = "scene"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Session(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">session</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element session is an inline element within preface to identify the
    string used by the document for the session of the legislature relative
    to the document.

    Use #refersTo to a TLCEvent to refer to the event of the specific
    session.</ns1:comment>.
    """

    class Meta:
        name = "session"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    value: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ShortTitle(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">shortTitle</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element shortTitle is an inline element within preface to identify the
    string used by the document for the short title of the
    document.</ns1:comment>.
    """

    class Meta:
        name = "shortTitle"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Signature(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">signature</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element signature is an inline element within conclusions to identify
    where the document defines one of the signatures</ns1:comment>.
    """

    class Meta:
        name = "signature"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Span(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">span</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element span is an HTML element and is used in Akoma Ntoso as in HTML,
    for the generic inline</ns1:comment>.
    """

    class Meta:
        name = "span"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Sub(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">sub</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element sub is an HTML element and is used in Akoma Ntoso as in HTML,
    for the subscript style (an inline)</ns1:comment>.
    """

    class Meta:
        name = "sub"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Summary(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">summary</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element summary is a block element in a debate to mark summaries of
    speeches that are individually not interesting (e.g.: "Question put and
    agreed to")</ns1:comment>.
    """

    class Meta:
        name = "summary"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Sup(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">sup</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element sup is an HTML element and is used in Akoma Ntoso as in HTML,
    for the superscript style (an inline)</ns1:comment>.
    """

    class Meta:
        name = "sup"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Time(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">time</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element time is an inline element to identify a time expressed in the
    text and to propose a normalized representation in the time
    attribute.</ns1:comment>.
    """

    class Meta:
        name = "time"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    time: XmlTime | XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class TocItem(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">tocItem</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element tocItem is a component of the table of content and contains
    header information about sections or parts of the rest of the
    document</ns1:comment>.
    """

    class Meta:
        name = "tocItem"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    level: int = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class U(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">u</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element u is an HTML element and is used in Akoma Ntoso as in HTML, for
    the underline style (an inline)</ns1:comment>.
    """

    class Meta:
        name = "u"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Vote(Inline1):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">vote</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element vote is an inline that wraps either the name of the voter (when
    organized by choice) or the vote (when organized by name) in a voting
    report.</ns1:comment>.
    """

    class Meta:
        name = "vote"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    by: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )
    choice: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ActiveModifications(Amendments):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">activeModifications</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element activeModifications is a metadata container of the active
    modifications generated by the document.</ns1:comment>.
    """

    class Meta:
        name = "activeModifications"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Inlinereq:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">inlinereq</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type inlinereq defines the content model and attributes shared
    by all blocks and inlines.

    Here the eId attribute is required</ns1:comment>.
    """

    class Meta:
        name = "inlinereq"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "ref",
                    "type": ForwardRef("Ref"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mref",
                    "type": Mref,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "rref",
                    "type": ForwardRef("Rref"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mod",
                    "type": ForwardRef("Mod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mmod",
                    "type": ForwardRef("Mmod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "rmod",
                    "type": ForwardRef("Rmod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "remark",
                    "type": Remark,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "recordedTime",
                    "type": RecordedTime,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "vote",
                    "type": Vote,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "outcome",
                    "type": Outcome,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "ins",
                    "type": Ins,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "del",
                    "type": Del,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "omissis",
                    "type": Omissis,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "embeddedText",
                    "type": EmbeddedText,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "embeddedStructure",
                    "type": ForwardRef("EmbeddedStructure"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "opinion",
                    "type": Opinion,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "placeholder",
                    "type": Placeholder,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "fillIn",
                    "type": FillIn,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "decoration",
                    "type": Decoration,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "b",
                    "type": B,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "i",
                    "type": I,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "a",
                    "type": A,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "u",
                    "type": U,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "sub",
                    "type": Sub,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "sup",
                    "type": Sup,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "abbr",
                    "type": Abbr,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "span",
                    "type": Span,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docType",
                    "type": DocType,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docTitle",
                    "type": DocTitle,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docNumber",
                    "type": DocNumber,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docProponent",
                    "type": DocProponent,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docDate",
                    "type": DocDate,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "legislature",
                    "type": Legislature,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "session",
                    "type": Session,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "shortTitle",
                    "type": ShortTitle,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docAuthority",
                    "type": DocAuthority,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docPurpose",
                    "type": DocPurpose,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docCommittee",
                    "type": DocCommittee,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docIntroducer",
                    "type": DocIntroducer,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docStage",
                    "type": DocStage,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docStatus",
                    "type": DocStatus,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docJurisdiction",
                    "type": DocJurisdiction,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docketNumber",
                    "type": DocketNumber,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "date",
                    "type": Date,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "time",
                    "type": Time,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "person",
                    "type": ForwardRef("Person"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "organization",
                    "type": ForwardRef("Organization"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "concept",
                    "type": ForwardRef("Concept"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "object",
                    "type": ForwardRef("Object"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "event",
                    "type": ForwardRef("Event"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "location",
                    "type": ForwardRef("Location"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "process",
                    "type": ForwardRef("Process"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "role",
                    "type": ForwardRef("Role"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "term",
                    "type": ForwardRef("Term"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "quantity",
                    "type": ForwardRef("Quantity"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "def",
                    "type": Def,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "entity",
                    "type": ForwardRef("Entity"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "courtType",
                    "type": CourtType,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "neutralCitation",
                    "type": NeutralCitation,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "party",
                    "type": ForwardRef("Party"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "judge",
                    "type": ForwardRef("Judge"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "lawyer",
                    "type": ForwardRef("Lawyer"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "signature",
                    "type": Signature,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "argument",
                    "type": Argument,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "affectedDocument",
                    "type": AffectedDocument,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "relatedDocument",
                    "type": RelatedDocument,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "change",
                    "type": Change,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "inline",
                    "type": Inline1,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "noteRef",
                    "type": NoteRef,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "eol",
                    "type": Eol,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "eop",
                    "type": Eop,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "marker",
                    "type": Marker,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "authorialNote",
                    "type": ForwardRef("AuthorialNote"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "subFlow",
                    "type": ForwardRef("SubFlow"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Judicial(JudicialArguments):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">judicial</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element judicial is a metadata container of the analysis of the
    judicial arguments of a judgment.</ns1:comment>.
    """

    class Meta:
        name = "judicial"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class PassiveModifications(Amendments):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">passiveModifications</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element passiveModifications is a metadata container of the passive
    modifications affecting the document.</ns1:comment>.
    """

    class Meta:
        name = "passiveModifications"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Table:
    class Meta:
        name = "table"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    caption: None | Caption = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )
    width: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    border: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cellspacing: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cellpadding: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Toc:
    class Meta:
        name = "toc"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    toc_item: list[TocItem] = field(
        default_factory=list,
        metadata={
            "name": "tocItem",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Analysis:
    class Meta:
        name = "analysis"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    active_modifications: None | ActiveModifications = field(
        default=None,
        metadata={
            "name": "activeModifications",
            "type": "Element",
        },
    )
    passive_modifications: None | PassiveModifications = field(
        default=None,
        metadata={
            "name": "passiveModifications",
            "type": "Element",
        },
    )
    restrictions: None | Restrictions = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    judicial: None | Judicial = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    parliamentary: None | Parliamentary = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    mappings: None | Mappings = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    other_references: list[OtherReferences] = field(
        default_factory=list,
        metadata={
            "name": "otherReferences",
            "type": "Element",
        },
    )
    other_analysis: list[OtherAnalysis] = field(
        default_factory=list,
        metadata={
            "name": "otherAnalysis",
            "type": "Element",
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class CrossHeading(Inlinereq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">crossHeading</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element crossHeading is a heading element that is placed side by side
    with hierarchical containers .</ns1:comment>.
    """

    class Meta:
        name = "crossHeading"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocContainerType(Basehierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">docContainerType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type docContainerType defines a shared content model for
    elements that contain whole documents, namely attachment,
    collectionItem, component.</ns1:comment>.
    """

    class Meta:
        name = "docContainerType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    amendment_list: None | AmendmentList = field(
        default=None,
        metadata={
            "name": "amendmentList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    official_gazette: None | OfficialGazette = field(
        default=None,
        metadata={
            "name": "officialGazette",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    document_collection: None | DocumentCollection = field(
        default=None,
        metadata={
            "name": "documentCollection",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    act: None | Act = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    bill: None | Bill = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate_report: None | DebateReport = field(
        default=None,
        metadata={
            "name": "debateReport",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate: None | Debate = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    statement: None | Statement = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    amendment: None | Amendment = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    judgment: None | Judgment = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    portion: None | Portion = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    doc: None | Doc = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    interstitial: None | Interstitial = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: None | Toc = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    document_ref: None | DocumentRef = field(
        default=None,
        metadata={
            "name": "documentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Heading(Inlinereq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">heading</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element heading is a heading element in a hierarchy that contains a
    title or any other textual content to describe the
    structure.</ns1:comment>.
    """

    class Meta:
        name = "heading"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class ItemType(Basehierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">itemType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    complex type itemType is similar to a hierarchical element, but is
    isolated and does not belong to a full hierarchy.</ns1:comment>.
    """

    class Meta:
        name = "itemType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Maincontent:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">maincontent</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type maincontent is used by container elements that can contain
    basically any other Akoma Ntoso structure</ns1:comment>.
    """

    class Meta:
        name = "maincontent"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    component_ref: list[ComponentRef] = field(
        default_factory=list,
        metadata={
            "name": "componentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    clause: list[Clause] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    section: list[Section] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    part: list[Part] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    chapter: list[Chapter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    title: list[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    book: list[Book] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tome: list[Tome] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    division: list[Division] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    point: list[Point] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    indent: list[Indent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    alinea: list[Alinea] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    rule: list[Rule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subrule: list[Subrule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    proviso: list[Proviso] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subsection: list[Subsection] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subpart: list[Subpart] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subparagraph: list[Subparagraph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subchapter: list[Subchapter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subtitle: list[Subtitle] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subdivision: list[Subdivision] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subclause: list[Subclause] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    sublist: list[Sublist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    level: list[Level] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    transitional: list[Transitional] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    hcontainer: list[Hcontainer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    administration_of_oath: list[AdministrationOfOath] = field(
        default_factory=list,
        metadata={
            "name": "administrationOfOath",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    roll_call: list[RollCall] = field(
        default_factory=list,
        metadata={
            "name": "rollCall",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    prayers: list[Prayers] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    oral_statements: list[OralStatements] = field(
        default_factory=list,
        metadata={
            "name": "oralStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    written_statements: list[WrittenStatements] = field(
        default_factory=list,
        metadata={
            "name": "writtenStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    personal_statements: list[PersonalStatements] = field(
        default_factory=list,
        metadata={
            "name": "personalStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ministerial_statements: list[MinisterialStatements] = field(
        default_factory=list,
        metadata={
            "name": "ministerialStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    resolutions: list[Resolutions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    national_interest: list[NationalInterest] = field(
        default_factory=list,
        metadata={
            "name": "nationalInterest",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    declaration_of_vote: list[DeclarationOfVote] = field(
        default_factory=list,
        metadata={
            "name": "declarationOfVote",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    communication: list[Communication] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    petitions: list[Petitions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    papers: list[Papers] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    notices_of_motion: list[NoticesOfMotion] = field(
        default_factory=list,
        metadata={
            "name": "noticesOfMotion",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    questions: list[Questions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    procedural_motions: list[ProceduralMotions] = field(
        default_factory=list,
        metadata={
            "name": "proceduralMotions",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    point_of_order: list[PointOfOrder] = field(
        default_factory=list,
        metadata={
            "name": "pointOfOrder",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    adjournment: list[Adjournment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate_section: list[DebateSection] = field(
        default_factory=list,
        metadata={
            "name": "debateSection",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    div: list[Div] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    container: list[Container] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title_attribute: None | str = field(
        default=None,
        metadata={
            "name": "title",
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Ref(Inlinereq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">ref</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element ref is an inline element containing a legal
    reference</ns1:comment>.
    """

    class Meta:
        name = "ref"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    href: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Rref(Inlinereq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">rref</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element rref is an inline element containing a range of references
    between the IRI specified in the from attribute and the one specified
    in the upTo attribute.</ns1:comment>.
    """

    class Meta:
        name = "rref"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    from_value: str = field(
        metadata={
            "name": "from",
            "type": "Attribute",
            "required": True,
        }
    )
    up_to: str = field(
        metadata={
            "name": "upTo",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SpeechType(Basehierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">speechType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type speechType defines the content model and attributes shared
    by all speech elements.

    Here the eId attribute is optional</ns1:comment>.
    """

    class Meta:
        name = "speechType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    from_value: None | From = field(
        default=None,
        metadata={
            "name": "from",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )
    by: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )
    start_time: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "startTime",
            "type": "Attribute",
        },
    )
    end_time: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "endTime",
            "type": "Attribute",
        },
    )
    to: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Subheading(Inlinereq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subheading</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element subheading is a heading element in a hierarchy that contains a
    subtitle or any other textual content to further describe the
    structure.</ns1:comment>.
    """

    class Meta:
        name = "subheading"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Answer(SpeechType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">answer</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element answer is a container of a single official answer to a
    question</ns1:comment>.
    """

    class Meta:
        name = "answer"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Arguments(Maincontent):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">arguments</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of a judgment
    containing the arguments</ns1:comment>.
    """

    class Meta:
        name = "arguments"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Attachment(DocContainerType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">attachment</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element attachment is used as a container of individual attachment
    elements</ns1:comment>.
    """

    class Meta:
        name = "attachment"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Background(Maincontent):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">background</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of a judgment
    containing the background</ns1:comment>.
    """

    class Meta:
        name = "background"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Citation(ItemType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">citation</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element citation is the individual element of the preface that is
    called citation</ns1:comment>.
    """

    class Meta:
        name = "citation"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Component(DocContainerType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">component</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element component is a container of a subdocument specified in a
    composite document</ns1:comment>.
    """

    class Meta:
        name = "component"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Decision(Maincontent):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">decision</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of a judgment
    containing the decision</ns1:comment>.
    """

    class Meta:
        name = "decision"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Inlinereqreq:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">inlinereqreq</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type inlinereq defines the content model and attributes shared
    by all blocks and inlines.

    Here the eId attribute is required and also the refersTo is
    required</ns1:comment>.
    """

    class Meta:
        name = "inlinereqreq"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "ref",
                    "type": Ref,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mref",
                    "type": Mref,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "rref",
                    "type": Rref,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mod",
                    "type": ForwardRef("Mod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mmod",
                    "type": ForwardRef("Mmod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "rmod",
                    "type": ForwardRef("Rmod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "remark",
                    "type": Remark,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "recordedTime",
                    "type": RecordedTime,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "vote",
                    "type": Vote,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "outcome",
                    "type": Outcome,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "ins",
                    "type": Ins,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "del",
                    "type": Del,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "omissis",
                    "type": Omissis,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "embeddedText",
                    "type": EmbeddedText,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "embeddedStructure",
                    "type": ForwardRef("EmbeddedStructure"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "opinion",
                    "type": Opinion,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "placeholder",
                    "type": Placeholder,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "fillIn",
                    "type": FillIn,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "decoration",
                    "type": Decoration,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "b",
                    "type": B,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "i",
                    "type": I,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "a",
                    "type": A,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "u",
                    "type": U,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "sub",
                    "type": Sub,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "sup",
                    "type": Sup,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "abbr",
                    "type": Abbr,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "span",
                    "type": Span,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docType",
                    "type": DocType,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docTitle",
                    "type": DocTitle,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docNumber",
                    "type": DocNumber,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docProponent",
                    "type": DocProponent,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docDate",
                    "type": DocDate,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "legislature",
                    "type": Legislature,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "session",
                    "type": Session,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "shortTitle",
                    "type": ShortTitle,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docAuthority",
                    "type": DocAuthority,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docPurpose",
                    "type": DocPurpose,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docCommittee",
                    "type": DocCommittee,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docIntroducer",
                    "type": DocIntroducer,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docStage",
                    "type": DocStage,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docStatus",
                    "type": DocStatus,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docJurisdiction",
                    "type": DocJurisdiction,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docketNumber",
                    "type": DocketNumber,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "date",
                    "type": Date,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "time",
                    "type": Time,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "person",
                    "type": ForwardRef("Person"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "organization",
                    "type": ForwardRef("Organization"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "concept",
                    "type": ForwardRef("Concept"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "object",
                    "type": ForwardRef("Object"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "event",
                    "type": ForwardRef("Event"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "location",
                    "type": ForwardRef("Location"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "process",
                    "type": ForwardRef("Process"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "role",
                    "type": ForwardRef("Role"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "term",
                    "type": ForwardRef("Term"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "quantity",
                    "type": ForwardRef("Quantity"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "def",
                    "type": Def,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "entity",
                    "type": ForwardRef("Entity"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "courtType",
                    "type": CourtType,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "neutralCitation",
                    "type": NeutralCitation,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "party",
                    "type": ForwardRef("Party"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "judge",
                    "type": ForwardRef("Judge"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "lawyer",
                    "type": ForwardRef("Lawyer"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "signature",
                    "type": Signature,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "argument",
                    "type": Argument,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "affectedDocument",
                    "type": AffectedDocument,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "relatedDocument",
                    "type": RelatedDocument,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "change",
                    "type": Change,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "inline",
                    "type": Inline1,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "noteRef",
                    "type": NoteRef,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "eol",
                    "type": Eol,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "eop",
                    "type": Eop,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "marker",
                    "type": Marker,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "authorialNote",
                    "type": ForwardRef("AuthorialNote"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "subFlow",
                    "type": ForwardRef("SubFlow"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Introduction(Maincontent):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">introduction</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of a judgment
    containing introductory material</ns1:comment>.
    """

    class Meta:
        name = "introduction"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Item(ItemType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">item</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element item is a container belonging to a blockList</ns1:comment>.
    """

    class Meta:
        name = "item"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class MainBody(Maincontent):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">mainBody</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element mainBody is the container of the main part of all other
    document types</ns1:comment>.
    """

    class Meta:
        name = "mainBody"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Motivation(Maincontent):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">motivation</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of a judgment
    containing the motivation</ns1:comment>.
    """

    class Meta:
        name = "motivation"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Question(SpeechType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">question</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element question is a container of a single official question as
    proposed by an MP to a person holding an official
    position</ns1:comment>.
    """

    class Meta:
        name = "question"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Recital(ItemType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">recital</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element recital is the individual element of the preface that is called
    recital</ns1:comment>.
    """

    class Meta:
        name = "recital"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Remedies(Maincontent):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">remedies</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> this
    element is a structural container for the section of a judgment
    containing the remedies</ns1:comment>.
    """

    class Meta:
        name = "remedies"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Speech(SpeechType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">speech</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element speech is a container of a single speech utterance in a debate.

    Dialogs between speakers need a speech element each</ns1:comment>.
    """

    class Meta:
        name = "speech"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Tblock(ItemType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">tblock</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element tblock (titled block) is used to specify a container for blocks
    introduced by heading elements, similarly to a hierarchical
    structure</ns1:comment>.
    """

    class Meta:
        name = "tblock"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Attachments:
    class Meta:
        name = "attachments"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    attachment: list[Attachment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class BlockListType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">blockListType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    blockListType is the type of element blockList</ns1:comment>.
    """

    class Meta:
        name = "blockListType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    list_introduction: None | ListIntroduction = field(
        default=None,
        metadata={
            "name": "listIntroduction",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    item: list[Item] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    list_wrap_up: None | ListWrapUp = field(
        default=None,
        metadata={
            "name": "listWrapUp",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class CitationHierarchy(Basehierarchy):
    class Meta:
        name = "citationHierarchy"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    intro: None | Intro = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    component_ref: list[ComponentRef] = field(
        default_factory=list,
        metadata={
            "name": "componentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    citation: list[Citation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    wrap_up: None | WrapUp = field(
        default=None,
        metadata={
            "name": "wrapUp",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class CollectionBodyType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">collectionBodyType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    collectionBodyType specifies a content model of a container of a list
    of other documents (e.g, acts, bills, amendments, etc.) possibly
    interspersed with interstitial elements with content that does not form
    an individual document</ns1:comment>.
    """

    class Meta:
        name = "collectionBodyType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    component: list[Component] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "min_occurs": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Components:
    class Meta:
        name = "components"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    component: list[Component] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )


@dataclass(kw_only=True)
class Concept(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">concept</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element concept is is an inline element to identify a text fragment
    introducing or referring to a concept in the ontology</ns1:comment>.
    """

    class Meta:
        name = "concept"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Entity(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">entity</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element entity is a generic inline element to identify a text fragment
    introducing or referring to a concept in the ontology</ns1:comment>.
    """

    class Meta:
        name = "entity"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Event(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">event</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element event is an inline element to identify a text fragment
    introducing or referring to an event in the ontology</ns1:comment>.
    """

    class Meta:
        name = "event"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Judge(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">judge</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element judge is an inline element within judgments to identify where
    the document defines one of the judges, and his/her role</ns1:comment>.
    """

    class Meta:
        name = "judge"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class JudgmentBodyType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">judgmentBodyType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    judgmentBodyType specifies a content model of the main hierarchy of a
    judgment document</ns1:comment>.
    """

    class Meta:
        name = "judgmentBodyType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    introduction: list[Introduction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    background: list[Background] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    arguments: list[Arguments] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    remedies: list[Remedies] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    motivation: list[Motivation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    decision: list[Decision] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "sequence": 1,
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Lawyer(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">lawyer</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element lawyer is an inline element within judgments to identify where
    the document defines one of the lawyers, his/her role, which party it
    represents, and the other lawyer, if any, this lawyer received the
    power delegation of power in some role</ns1:comment>.
    """

    class Meta:
        name = "lawyer"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )
    for_value: None | str = field(
        default=None,
        metadata={
            "name": "for",
            "type": "Attribute",
        },
    )
    empowered_by: None | str = field(
        default=None,
        metadata={
            "name": "empoweredBy",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Location(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">location</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element location is an inline element to identify a text fragment
    introducing or referring to a location in the ontology</ns1:comment>.
    """

    class Meta:
        name = "location"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Object(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">object</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element object is is an inline element to identify a text fragment
    introducing or referring to an object in the ontology</ns1:comment>.
    """

    class Meta:
        name = "object"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Organization(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">organization</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element organization is an inline element to identify a text fragment
    introducing or referring to an organization in the
    ontology</ns1:comment>.
    """

    class Meta:
        name = "organization"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Party(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">party</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element party is an inline element within judgments to identify where
    the document defines one of the parties</ns1:comment>.
    """

    class Meta:
        name = "party"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Person(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">person</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element person is an inline element to identify a text fragment
    introducing or referring to a person in the ontology.

    Attribute as allows to specify a TLCrole the person is holding in the
    context of the document's mention</ns1:comment>.
    """

    class Meta:
        name = "person"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    as_value: None | str = field(
        default=None,
        metadata={
            "name": "as",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Process(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">process</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element process is an inline element to identify a text fragment
    introducing or referring to a process in the ontology</ns1:comment>.
    """

    class Meta:
        name = "process"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Quantity(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">quantity</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element quantity is an inline element to identify a text fragment
    introducing or referring to a quantity.

    This could be a dimensionless number, or a number referring to a
    length, weight, duration, etc. or even a sum of money. The attribute
    normalized contains the value normalized in a number, if
    appropriate.</ns1:comment>.
    """

    class Meta:
        name = "quantity"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    normalized: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class RecitalHierarchy(Basehierarchy):
    class Meta:
        name = "recitalHierarchy"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    intro: None | Intro = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    component_ref: list[ComponentRef] = field(
        default_factory=list,
        metadata={
            "name": "componentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    recital: list[Recital] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    wrap_up: None | WrapUp = field(
        default=None,
        metadata={
            "name": "wrapUp",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Role(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">role</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element role is an inline element to identify a text fragment
    introducing or referring to a role in the ontology</ns1:comment>.
    """

    class Meta:
        name = "role"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Term(Inlinereqreq):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">term</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element term is an inline element to identify a text fragment
    introducing or referring to a term in the ontology</ns1:comment>.
    """

    class Meta:
        name = "term"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AmendmentStructure:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">amendmentStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    amendmentStructure specifies the overall content model of the document
    types that describe amendments</ns1:comment>.
    """

    class Meta:
        name = "amendmentStructure"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    meta: MetaType = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    cover_page: None | CoverPage = field(
        default=None,
        metadata={
            "name": "coverPage",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preface: None | Preface = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    amendment_body: AmendmentBody = field(
        metadata={
            "name": "amendmentBody",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    conclusions: None | Conclusions = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    attachments: None | Attachments = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    components: None | Components = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    contains: VersionType = field(
        default=VersionType.ORIGINAL_VERSION,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BlockList(BlockListType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">blockList</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element blockList is used as in a block context as a container of many
    individual item elements to be treated as in a list</ns1:comment>.
    """

    class Meta:
        name = "blockList"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Citations(CitationHierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">citations</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element citations is the section of the preamble that contains
    citations</ns1:comment>.
    """

    class Meta:
        name = "citations"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class CollectionBody(CollectionBodyType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">collectionBody</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element collectionBody is the container of a list of other documents
    (e.g, acts, bills, amendments, etc.) possibly interspersed with
    interstitial elements with content that does not form an individual
    document</ns1:comment>.
    """

    class Meta:
        name = "collectionBody"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DebateStructure:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">debateStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    debateStructure specifies the overall content model of the document
    types that describe debates</ns1:comment>.
    """

    class Meta:
        name = "debateStructure"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    meta: MetaType = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    cover_page: None | CoverPage = field(
        default=None,
        metadata={
            "name": "coverPage",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preface: None | Preface = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate_body: DebateBody = field(
        metadata={
            "name": "debateBody",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    conclusions: None | Conclusions = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    attachments: None | Attachments = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    components: None | Components = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    contains: VersionType = field(
        default=VersionType.ORIGINAL_VERSION,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class HierarchicalStructure:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">hierarchicalStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    hierarchicalStructure specifies the overall content model of the
    document types that are hierarchical in nature, especially acts and
    bills</ns1:comment>.
    """

    class Meta:
        name = "hierarchicalStructure"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    meta: MetaType = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    cover_page: None | CoverPage = field(
        default=None,
        metadata={
            "name": "coverPage",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preface: None | Preface = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preamble: None | Preamble = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    body: Body = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    conclusions: None | Conclusions = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    attachments: None | Attachments = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    components: None | Components = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    contains: VersionType = field(
        default=VersionType.ORIGINAL_VERSION,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class JudgmentBody(JudgmentBodyType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">judgmentBody</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element judgmentBody is the container of the main hierarchy of a
    judgment document</ns1:comment>.
    """

    class Meta:
        name = "judgmentBody"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class ModType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">modType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type modType specifies the content that is allowed within mod,
    mmod and rmod elements, i.e. it adds quotedText and quotedStructure to
    the normal list of inline elements.

    Attribute for is used to point to the eId of the corresponding ref
    element.</ns1:comment>.
    """

    class Meta:
        name = "modType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )
    for_value: None | str = field(
        default=None,
        metadata={
            "name": "for",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "ref",
                    "type": Ref,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mref",
                    "type": Mref,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "rref",
                    "type": Rref,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mod",
                    "type": ForwardRef("Mod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "mmod",
                    "type": ForwardRef("Mmod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "rmod",
                    "type": ForwardRef("Rmod"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "remark",
                    "type": Remark,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "recordedTime",
                    "type": RecordedTime,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "vote",
                    "type": Vote,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "outcome",
                    "type": Outcome,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "ins",
                    "type": Ins,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "del",
                    "type": Del,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "omissis",
                    "type": Omissis,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "embeddedText",
                    "type": EmbeddedText,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "embeddedStructure",
                    "type": ForwardRef("EmbeddedStructure"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "opinion",
                    "type": Opinion,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "placeholder",
                    "type": Placeholder,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "fillIn",
                    "type": FillIn,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "decoration",
                    "type": Decoration,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "b",
                    "type": B,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "i",
                    "type": I,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "a",
                    "type": A,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "u",
                    "type": U,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "sub",
                    "type": Sub,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "sup",
                    "type": Sup,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "abbr",
                    "type": Abbr,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "span",
                    "type": Span,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docType",
                    "type": DocType,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docTitle",
                    "type": DocTitle,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docNumber",
                    "type": DocNumber,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docProponent",
                    "type": DocProponent,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docDate",
                    "type": DocDate,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "legislature",
                    "type": Legislature,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "session",
                    "type": Session,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "shortTitle",
                    "type": ShortTitle,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docAuthority",
                    "type": DocAuthority,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docPurpose",
                    "type": DocPurpose,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docCommittee",
                    "type": DocCommittee,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docIntroducer",
                    "type": DocIntroducer,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docStage",
                    "type": DocStage,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docStatus",
                    "type": DocStatus,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docJurisdiction",
                    "type": DocJurisdiction,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "docketNumber",
                    "type": DocketNumber,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "date",
                    "type": Date,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "time",
                    "type": Time,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "person",
                    "type": Person,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "organization",
                    "type": Organization,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "concept",
                    "type": Concept,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "object",
                    "type": Object,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "event",
                    "type": Event,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "location",
                    "type": Location,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "process",
                    "type": Process,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "role",
                    "type": Role,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "term",
                    "type": Term,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "quantity",
                    "type": Quantity,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "def",
                    "type": Def,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "entity",
                    "type": Entity,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "courtType",
                    "type": CourtType,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "neutralCitation",
                    "type": NeutralCitation,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "party",
                    "type": Party,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "judge",
                    "type": Judge,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "lawyer",
                    "type": Lawyer,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "signature",
                    "type": Signature,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "argument",
                    "type": Argument,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "affectedDocument",
                    "type": AffectedDocument,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "relatedDocument",
                    "type": RelatedDocument,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "change",
                    "type": Change,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "inline",
                    "type": Inline1,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "noteRef",
                    "type": NoteRef,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "eol",
                    "type": Eol,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "eop",
                    "type": Eop,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "marker",
                    "type": Marker,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "authorialNote",
                    "type": ForwardRef("AuthorialNote"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "subFlow",
                    "type": ForwardRef("SubFlow"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "quotedText",
                    "type": QuotedText,
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
                {
                    "name": "quotedStructure",
                    "type": ForwardRef("QuotedStructure"),
                    "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
                },
            ),
        },
    )


@dataclass(kw_only=True)
class OpenStructure:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">openStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    openStructure specifies the overall content model of all the document
    types that do not have a specific and peculiar structure</ns1:comment>.
    """

    class Meta:
        name = "openStructure"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    meta: MetaType = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    cover_page: None | CoverPage = field(
        default=None,
        metadata={
            "name": "coverPage",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preface: None | Preface = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preamble: None | Preamble = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    main_body: MainBody = field(
        metadata={
            "name": "mainBody",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    conclusions: None | Conclusions = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    attachments: None | Attachments = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    components: None | Components = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    contains: VersionType = field(
        default=VersionType.ORIGINAL_VERSION,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Recitals(RecitalHierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">recitals</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element recitals is the section of the preamble that contains
    recitals</ns1:comment>.
    """

    class Meta:
        name = "recitals"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Act(HierarchicalStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">act</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    act is used for describing the structure and content of an
    act</ns1:comment>.
    """

    class Meta:
        name = "act"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Amendment(AmendmentStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">amendment</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    amendment is used for describing the structure and content of an
    amendment</ns1:comment>.
    """

    class Meta:
        name = "amendment"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Bill(HierarchicalStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">bill</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    bill is used for describing the structure and content of a
    bill</ns1:comment>.
    """

    class Meta:
        name = "bill"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class BlockContainerType(Basehierarchy):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">blockContainerType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    blockContainerType is the type of element blockContainer</ns1:comment>.
    """

    class Meta:
        name = "blockContainerType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    intro: None | Intro = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    component_ref: list[ComponentRef] = field(
        default_factory=list,
        metadata={
            "name": "componentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    cross_heading: list[CrossHeading] = field(
        default_factory=list,
        metadata={
            "name": "crossHeading",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    wrap_up: None | WrapUp = field(
        default=None,
        metadata={
            "name": "wrapUp",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class CollectionStructure:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">collectionStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    collectionStructure specifies the overall content model of the document
    types that are collections of other documents</ns1:comment>.
    """

    class Meta:
        name = "collectionStructure"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    meta: MetaType = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    cover_page: None | CoverPage = field(
        default=None,
        metadata={
            "name": "coverPage",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preface: None | Preface = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preamble: None | Preamble = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    collection_body: CollectionBody = field(
        metadata={
            "name": "collectionBody",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    conclusions: None | Conclusions = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    attachments: None | Attachments = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    components: None | Components = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    contains: VersionType = field(
        default=VersionType.ORIGINAL_VERSION,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Debate(DebateStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">debate</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    debate is used for describing the structure and content of a debate
    record</ns1:comment>.
    """

    class Meta:
        name = "debate"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DebateReport(OpenStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">debateReport</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    debateReport is used for describing the structure and content of a
    report</ns1:comment>.
    """

    class Meta:
        name = "debateReport"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Doc(OpenStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">doc</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    doc is used for describing the structure and content of any other
    document that is not included in the list of document explicitly
    managed by Akoma Ntoso</ns1:comment>.
    """

    class Meta:
        name = "doc"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class JudgmentStructure:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">judgmentStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    judgmentStructure specifies the overall content model of the document
    types that describe judgments</ns1:comment>.
    """

    class Meta:
        name = "judgmentStructure"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    meta: MetaType = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    cover_page: None | CoverPage = field(
        default=None,
        metadata={
            "name": "coverPage",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    header: Header = field(
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    judgment_body: JudgmentBody = field(
        metadata={
            "name": "judgmentBody",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "required": True,
        }
    )
    conclusions: None | Conclusions = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    attachments: None | Attachments = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    components: None | Components = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    contains: VersionType = field(
        default=VersionType.ORIGINAL_VERSION,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Mmod(ModType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">mmod</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element mmod is an inline element containing multiple specifications of
    modifications on another document</ns1:comment>.
    """

    class Meta:
        name = "mmod"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Mod(ModType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">mod</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element mod is an inline element containing the specification of a
    modification on another document</ns1:comment>.
    """

    class Meta:
        name = "mod"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Rmod(ModType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">rmod</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element rmod is an inline element containing the specification of a
    range of modifications on another document</ns1:comment>.
    """

    class Meta:
        name = "rmod"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    from_value: str = field(
        metadata={
            "name": "from",
            "type": "Attribute",
            "required": True,
        }
    )
    up_to: str = field(
        metadata={
            "name": "upTo",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Statement(OpenStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">statement</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    statement is used for describing the structure and content of an
    official document of a body that may or may not be normative in
    structure (e.g., statements, resolutions, etc.).</ns1:comment>.
    """

    class Meta:
        name = "statement"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AmendmentList(CollectionStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">amendmentList</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    amendmentList is used for describing the structure and content of a
    collection of amendments</ns1:comment>.
    """

    class Meta:
        name = "amendmentList"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class BlockContainer(BlockContainerType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">blockContainer</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element blockContainer is used as a container of many individual block
    elements in a block context</ns1:comment>.
    """

    class Meta:
        name = "blockContainer"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class DocumentCollection(CollectionStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">documentCollection</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    documentCollection is used for describing the structure and content of
    a collection of other documents chosen and combined for any reason
    whatsoever</ns1:comment>.
    """

    class Meta:
        name = "documentCollection"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Judgment(JudgmentStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">judgment</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    judgment is used for describing the structure and content of a
    judgment</ns1:comment>.
    """

    class Meta:
        name = "judgment"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class OfficialGazette(CollectionStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">officialGazette</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> Element
    officialGazette is used for describing the structure and content of an
    issue of an official gazette</ns1:comment>.
    """

    class Meta:
        name = "officialGazette"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AkomaNtosoType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">akomaNtosoType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type akomaNtosoType is the type for the root element in Akoma
    Ntoso.</ns1:comment>.
    """

    class Meta:
        name = "akomaNtosoType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    amendment_list: None | AmendmentList = field(
        default=None,
        metadata={
            "name": "amendmentList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    official_gazette: None | OfficialGazette = field(
        default=None,
        metadata={
            "name": "officialGazette",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    document_collection: None | DocumentCollection = field(
        default=None,
        metadata={
            "name": "documentCollection",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    act: None | Act = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    bill: None | Bill = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate_report: None | DebateReport = field(
        default=None,
        metadata={
            "name": "debateReport",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate: None | Debate = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    statement: None | Statement = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    amendment: None | Amendment = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    judgment: None | Judgment = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    portion: None | Portion = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    doc: None | Doc = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    components: None | Components = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )


@dataclass(kw_only=True)
class ContainerType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">containerType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type containerType is the content model for the generic element
    for a container.

    It can be placed in a container instead of any of the other containers.
    The attribute name is required and gives a name to the
    element.</ns1:comment>.
    """

    class Meta:
        name = "containerType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    container: list[Container] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SubFlowStructure:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subFlowStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    subFlowStructure specifies the overall content model of the elements
    that are subFlows</ns1:comment>.
    """

    class Meta:
        name = "subFlowStructure"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    amendment_list: None | AmendmentList = field(
        default=None,
        metadata={
            "name": "amendmentList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    official_gazette: None | OfficialGazette = field(
        default=None,
        metadata={
            "name": "officialGazette",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    document_collection: None | DocumentCollection = field(
        default=None,
        metadata={
            "name": "documentCollection",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    act: None | Act = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    bill: None | Bill = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate_report: None | DebateReport = field(
        default=None,
        metadata={
            "name": "debateReport",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate: None | Debate = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    statement: None | Statement = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    amendment: None | Amendment = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    judgment: None | Judgment = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    portion: None | Portion = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    doc: None | Doc = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    administration_of_oath: list[AdministrationOfOath] = field(
        default_factory=list,
        metadata={
            "name": "administrationOfOath",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    roll_call: list[RollCall] = field(
        default_factory=list,
        metadata={
            "name": "rollCall",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    prayers: list[Prayers] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    oral_statements: list[OralStatements] = field(
        default_factory=list,
        metadata={
            "name": "oralStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    written_statements: list[WrittenStatements] = field(
        default_factory=list,
        metadata={
            "name": "writtenStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    personal_statements: list[PersonalStatements] = field(
        default_factory=list,
        metadata={
            "name": "personalStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ministerial_statements: list[MinisterialStatements] = field(
        default_factory=list,
        metadata={
            "name": "ministerialStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    resolutions: list[Resolutions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    national_interest: list[NationalInterest] = field(
        default_factory=list,
        metadata={
            "name": "nationalInterest",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    declaration_of_vote: list[DeclarationOfVote] = field(
        default_factory=list,
        metadata={
            "name": "declarationOfVote",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    communication: list[Communication] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    petitions: list[Petitions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    papers: list[Papers] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    notices_of_motion: list[NoticesOfMotion] = field(
        default_factory=list,
        metadata={
            "name": "noticesOfMotion",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    questions: list[Questions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    procedural_motions: list[ProceduralMotions] = field(
        default_factory=list,
        metadata={
            "name": "proceduralMotions",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    point_of_order: list[PointOfOrder] = field(
        default_factory=list,
        metadata={
            "name": "pointOfOrder",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    adjournment: list[Adjournment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate_section: list[DebateSection] = field(
        default_factory=list,
        metadata={
            "name": "debateSection",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    div: list[Div] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    container: list[Container] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    th: list[Th] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    td: list[Td] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    clause: list[Clause] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    section: list[Section] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    part: list[Part] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    paragraph: list[Paragraph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    chapter: list[Chapter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    title: list[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    article: list[Article] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    book: list[Book] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tome: list[Tome] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    division: list[Division] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    point: list[Point] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    indent: list[Indent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    alinea: list[Alinea] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    rule: list[Rule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subrule: list[Subrule] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    proviso: list[Proviso] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subsection: list[Subsection] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subpart: list[Subpart] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subparagraph: list[Subparagraph] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subchapter: list[Subchapter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subtitle: list[Subtitle] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subdivision: list[Subdivision] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subclause: list[Subclause] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    sublist: list[Sublist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    level: list[Level] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    transitional: list[Transitional] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    hcontainer: list[Hcontainer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    content: list[Content] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    speech_group: list[SpeechGroup] = field(
        default_factory=list,
        metadata={
            "name": "speechGroup",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    question: list[Question] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other: list[Other] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    scene: list[Scene] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    narrative: list[Narrative] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    summary: list[Summary] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    formula: list[Formula] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    recitals: list[Recitals] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    citations: list[Citations] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    long_title: list[LongTitle] = field(
        default_factory=list,
        metadata={
            "name": "longTitle",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    recital: list[Recital] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    citation: list[Citation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    component_ref: list[ComponentRef] = field(
        default_factory=list,
        metadata={
            "name": "componentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    document_ref: list[DocumentRef] = field(
        default_factory=list,
        metadata={
            "name": "documentRef",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    intro: list[Intro] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    wrap_up: list[WrapUp] = field(
        default_factory=list,
        metadata={
            "name": "wrapUp",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    heading: list[Heading] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subheading: list[Subheading] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    num: list[Num] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title_attribute: None | str = field(
        default=None,
        metadata={
            "name": "title",
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AkomaNtoso(AkomaNtosoType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element
    (root)</ns1:type> <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">akomaNtoso</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> NAME
    akomaNtoso the element akomaNtoso is the root element of all document
    types in Akoma Ntoso.

    It follows the pattern Universal Root
    (http://www.xmlpatterns.com/UniversalRootMain.shtml)</ns1:comment>.
    """

    class Meta:
        name = "akomaNtoso"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class AuthorialNote(SubFlowStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">authorialNote</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element authorialNote is a subFlow element containing an authorial
    (non-editorial) note in the main flow of the text.</ns1:comment>.
    """

    class Meta:
        name = "authorialNote"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    marker: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    placement: None | PlacementType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    placement_base: None | str = field(
        default=None,
        metadata={
            "name": "placementBase",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Container(ContainerType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">container</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element container is a generic element for a container.</ns1:comment>.
    """

    class Meta:
        name = "container"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class EmbeddedStructure(SubFlowStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">embeddedStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element embeddedStructure is a subFlow element containing a full
    structure used as an extract from another document or position.

    Attribute quote is used to specify the quote character used in the
    original; no quote attribute implies that the quote is left in the
    text; quote="" implies that there is no quote character.</ns1:comment>.
    """

    class Meta:
        name = "embeddedStructure"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    start_quote: None | str = field(
        default=None,
        metadata={
            "name": "startQuote",
            "type": "Attribute",
        },
    )
    end_quote: None | str = field(
        default=None,
        metadata={
            "name": "endQuote",
            "type": "Attribute",
        },
    )
    inline_quote: None | str = field(
        default=None,
        metadata={
            "name": "inlineQuote",
            "type": "Attribute",
        },
    )
    href: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Note(SubFlowStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">note</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> The
    element note is a metadata element containing the text of the footnote
    and endnote specified.</ns1:comment>.
    """

    class Meta:
        name = "note"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    marker: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    placement: None | PlacementType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    placement_base: None | str = field(
        default=None,
        metadata={
            "name": "placementBase",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class QuotedStructure(SubFlowStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">quotedStructure</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element quotedStructure is a subFlow element containing a full
    structure proposed as an insertion or a replacement.

    Attribute quote is used to specify the quote character used in the
    original; no quote attribute implies that the quote is left in the
    text; quote="" implies that there is no quote character. Attribute for
    is used in a mmod or rmod to point to the eId of the corresponding ref
    element.</ns1:comment>.
    """

    class Meta:
        name = "quotedStructure"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    start_quote: None | str = field(
        default=None,
        metadata={
            "name": "startQuote",
            "type": "Attribute",
        },
    )
    end_quote: None | str = field(
        default=None,
        metadata={
            "name": "endQuote",
            "type": "Attribute",
        },
    )
    inline_quote: None | str = field(
        default=None,
        metadata={
            "name": "inlineQuote",
            "type": "Attribute",
        },
    )
    for_value: None | str = field(
        default=None,
        metadata={
            "name": "for",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class SubFlow(SubFlowStructure):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">subFlow</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element subFlow is a generic element for a subFlow.</ns1:comment>.
    """

    class Meta:
        name = "subFlow"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Basicopt:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">basicopt</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type basicopt defines the content model and attributes used by
    basic containers such as coverPage and conclusions.

    Here the eId attribute is optional</ns1:comment>.
    """

    class Meta:
        name = "basicopt"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    long_title: list[LongTitle] = field(
        default_factory=list,
        metadata={
            "name": "longTitle",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    formula: list[Formula] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    container: list[Container] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Li:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">li</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> TYPE
    Element NAME li The element li is an HTML element and is used in Akoma
    Ntoso as in HTML, for the generic list item (not a
    pattern)</ns1:comment>.
    """

    class Meta:
        name = "li"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    value: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "ref",
                    "type": Ref,
                },
                {
                    "name": "mref",
                    "type": Mref,
                },
                {
                    "name": "rref",
                    "type": Rref,
                },
                {
                    "name": "mod",
                    "type": Mod,
                },
                {
                    "name": "mmod",
                    "type": Mmod,
                },
                {
                    "name": "rmod",
                    "type": Rmod,
                },
                {
                    "name": "remark",
                    "type": Remark,
                },
                {
                    "name": "recordedTime",
                    "type": RecordedTime,
                },
                {
                    "name": "vote",
                    "type": Vote,
                },
                {
                    "name": "outcome",
                    "type": Outcome,
                },
                {
                    "name": "ins",
                    "type": Ins,
                },
                {
                    "name": "del",
                    "type": Del,
                },
                {
                    "name": "omissis",
                    "type": Omissis,
                },
                {
                    "name": "embeddedText",
                    "type": EmbeddedText,
                },
                {
                    "name": "embeddedStructure",
                    "type": EmbeddedStructure,
                },
                {
                    "name": "opinion",
                    "type": Opinion,
                },
                {
                    "name": "placeholder",
                    "type": Placeholder,
                },
                {
                    "name": "fillIn",
                    "type": FillIn,
                },
                {
                    "name": "decoration",
                    "type": Decoration,
                },
                {
                    "name": "b",
                    "type": B,
                },
                {
                    "name": "i",
                    "type": I,
                },
                {
                    "name": "a",
                    "type": A,
                },
                {
                    "name": "u",
                    "type": U,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "abbr",
                    "type": Abbr,
                },
                {
                    "name": "span",
                    "type": Span,
                },
                {
                    "name": "docType",
                    "type": DocType,
                },
                {
                    "name": "docTitle",
                    "type": DocTitle,
                },
                {
                    "name": "docNumber",
                    "type": DocNumber,
                },
                {
                    "name": "docProponent",
                    "type": DocProponent,
                },
                {
                    "name": "docDate",
                    "type": DocDate,
                },
                {
                    "name": "legislature",
                    "type": Legislature,
                },
                {
                    "name": "session",
                    "type": Session,
                },
                {
                    "name": "shortTitle",
                    "type": ShortTitle,
                },
                {
                    "name": "docAuthority",
                    "type": DocAuthority,
                },
                {
                    "name": "docPurpose",
                    "type": DocPurpose,
                },
                {
                    "name": "docCommittee",
                    "type": DocCommittee,
                },
                {
                    "name": "docIntroducer",
                    "type": DocIntroducer,
                },
                {
                    "name": "docStage",
                    "type": DocStage,
                },
                {
                    "name": "docStatus",
                    "type": DocStatus,
                },
                {
                    "name": "docJurisdiction",
                    "type": DocJurisdiction,
                },
                {
                    "name": "docketNumber",
                    "type": DocketNumber,
                },
                {
                    "name": "date",
                    "type": Date,
                },
                {
                    "name": "time",
                    "type": Time,
                },
                {
                    "name": "person",
                    "type": Person,
                },
                {
                    "name": "organization",
                    "type": Organization,
                },
                {
                    "name": "concept",
                    "type": Concept,
                },
                {
                    "name": "object",
                    "type": Object,
                },
                {
                    "name": "event",
                    "type": Event,
                },
                {
                    "name": "location",
                    "type": Location,
                },
                {
                    "name": "process",
                    "type": Process,
                },
                {
                    "name": "role",
                    "type": Role,
                },
                {
                    "name": "term",
                    "type": Term,
                },
                {
                    "name": "quantity",
                    "type": Quantity,
                },
                {
                    "name": "def",
                    "type": Def,
                },
                {
                    "name": "entity",
                    "type": Entity,
                },
                {
                    "name": "courtType",
                    "type": CourtType,
                },
                {
                    "name": "neutralCitation",
                    "type": NeutralCitation,
                },
                {
                    "name": "party",
                    "type": Party,
                },
                {
                    "name": "judge",
                    "type": Judge,
                },
                {
                    "name": "lawyer",
                    "type": Lawyer,
                },
                {
                    "name": "signature",
                    "type": Signature,
                },
                {
                    "name": "argument",
                    "type": Argument,
                },
                {
                    "name": "affectedDocument",
                    "type": AffectedDocument,
                },
                {
                    "name": "relatedDocument",
                    "type": RelatedDocument,
                },
                {
                    "name": "change",
                    "type": Change,
                },
                {
                    "name": "inline",
                    "type": Inline1,
                },
                {
                    "name": "noteRef",
                    "type": NoteRef,
                },
                {
                    "name": "eol",
                    "type": Eol,
                },
                {
                    "name": "eop",
                    "type": Eop,
                },
                {
                    "name": "img",
                    "type": Img,
                },
                {
                    "name": "br",
                    "type": Br,
                },
                {
                    "name": "marker",
                    "type": Marker,
                },
                {
                    "name": "authorialNote",
                    "type": AuthorialNote,
                },
                {
                    "name": "subFlow",
                    "type": SubFlow,
                },
                {
                    "name": "ul",
                    "type": Ul,
                },
                {
                    "name": "ol",
                    "type": Ol,
                },
                {
                    "name": "p",
                    "type": P,
                },
            ),
        },
    )


@dataclass(kw_only=True)
class Notes:
    class Meta:
        name = "notes"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    note: list[Note] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    source: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass(kw_only=True)
class Preambleopt:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">preambleopt</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type preambleopt defines the content model and attributes used
    by preambles.

    Here the eId attribute is optional</ns1:comment>.
    """

    class Meta:
        name = "preambleopt"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    recitals: list[Recitals] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    citations: list[Citations] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    formula: list[Formula] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    container: list[Container] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Prefaceopt:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">prefaceopt</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    complex type prefaceopt defines the content model and attributes used
    by preface.

    Here the eId attribute is optional</ns1:comment>.
    """

    class Meta:
        name = "prefaceopt"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    block_list: list[BlockList] = field(
        default_factory=list,
        metadata={
            "name": "blockList",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block_container: list[BlockContainer] = field(
        default_factory=list,
        metadata={
            "name": "blockContainer",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tblock: list[Tblock] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    toc: list[Toc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ul: list[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ol: list[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    foreign: list[Foreign] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    block: list[Block] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    long_title: list[LongTitle] = field(
        default_factory=list,
        metadata={
            "name": "longTitle",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    formula: list[Formula] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    container: list[Container] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Conclusions(Basicopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">conclusions</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element conclusion is used as a container of all concluding material
    (e.g. dates, signatures, formulas, etc.)</ns1:comment>.
    """

    class Meta:
        name = "conclusions"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class CoverPage(Basicopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">coverPage</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element coverPage is used as a container of the text that acts as a
    cover page</ns1:comment>.
    """

    class Meta:
        name = "coverPage"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class MetaType:
    class Meta:
        name = "meta"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    identification: Identification = field(
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    publication: None | Publication = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    classification: list[Classification] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    lifecycle: list[Lifecycle] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    workflow: list[Workflow] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    analysis: list[Analysis] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    temporal_data: list[TemporalData] = field(
        default_factory=list,
        metadata={
            "name": "temporalData",
            "type": "Element",
        },
    )
    references: list[References] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    notes: list[Notes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    proprietary: list[Proprietary] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    presentation: list[Presentation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Preamble(Preambleopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">preamble</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element preamble is used as a container of the text that opens the main
    body of the document as a preamble</ns1:comment>.
    """

    class Meta:
        name = "preamble"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class Preface(Prefaceopt):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">preface</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element preface is used as a container of all prefacing material (e.g.
    headers, formulas, etc.)</ns1:comment>.
    """

    class Meta:
        name = "preface"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"


@dataclass(kw_only=True)
class PortionBodyType:
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Complex</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">portionBodyType</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the type
    portionBodyType specifies a content model of a container of a portion
    of another document</ns1:comment>.
    """

    class Meta:
        name = "portionBodyType"
        target_namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"

    administration_of_oath: None | AdministrationOfOath = field(
        default=None,
        metadata={
            "name": "administrationOfOath",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    roll_call: None | RollCall = field(
        default=None,
        metadata={
            "name": "rollCall",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    prayers: None | Prayers = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    oral_statements: None | OralStatements = field(
        default=None,
        metadata={
            "name": "oralStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    written_statements: None | WrittenStatements = field(
        default=None,
        metadata={
            "name": "writtenStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    personal_statements: None | PersonalStatements = field(
        default=None,
        metadata={
            "name": "personalStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    ministerial_statements: None | MinisterialStatements = field(
        default=None,
        metadata={
            "name": "ministerialStatements",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    resolutions: None | Resolutions = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    national_interest: None | NationalInterest = field(
        default=None,
        metadata={
            "name": "nationalInterest",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    declaration_of_vote: None | DeclarationOfVote = field(
        default=None,
        metadata={
            "name": "declarationOfVote",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    communication: None | Communication = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    petitions: None | Petitions = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    papers: None | Papers = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    notices_of_motion: None | NoticesOfMotion = field(
        default=None,
        metadata={
            "name": "noticesOfMotion",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    questions: None | Questions = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    address: None | Address = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    procedural_motions: None | ProceduralMotions = field(
        default=None,
        metadata={
            "name": "proceduralMotions",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    point_of_order: None | PointOfOrder = field(
        default=None,
        metadata={
            "name": "pointOfOrder",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    adjournment: None | Adjournment = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    debate_section: None | DebateSection = field(
        default=None,
        metadata={
            "name": "debateSection",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    div: None | Div = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    container: None | Container = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    clause: None | Clause = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    section: None | Section = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    part: None | Part = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    paragraph: None | Paragraph = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    chapter: None | Chapter = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    title: None | Title = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    article: None | Article = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    book: None | Book = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    tome: None | Tome = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    division: None | Division = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    list_value: None | List = field(
        default=None,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    point: None | Point = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    indent: None | Indent = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    alinea: None | Alinea = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    rule: None | Rule = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subrule: None | Subrule = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    proviso: None | Proviso = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subsection: None | Subsection = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subpart: None | Subpart = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subparagraph: None | Subparagraph = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subchapter: None | Subchapter = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subtitle: None | Subtitle = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subdivision: None | Subdivision = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    subclause: None | Subclause = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    sublist: None | Sublist = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    level: None | Level = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    transitional: None | Transitional = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    hcontainer: None | Hcontainer = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    speech_group: None | SpeechGroup = field(
        default=None,
        metadata={
            "name": "speechGroup",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    speech: None | Speech = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    question: None | Question = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    answer: None | Answer = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other: None | Other = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    scene: None | Scene = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    narrative: None | Narrative = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    summary: None | Summary = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    recitals: None | Recitals = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    recital: None | Recital = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    citations: None | Citations = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    citation: None | Citation = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    long_title: None | LongTitle = field(
        default=None,
        metadata={
            "name": "longTitle",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    formula: None | Formula = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    cover_page: None | CoverPage = field(
        default=None,
        metadata={
            "name": "coverPage",
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preface: None | Preface = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    preamble: None | Preamble = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
        },
    )
    other_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##other",
        },
    )
    class_value: None | str = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        },
    )
    style: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title_attribute: None | str = field(
        default=None,
        metadata={
            "name": "title",
            "type": "Attribute",
        },
    )
    period: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: None | StatusType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e_id: None | str = field(
        default=None,
        metadata={
            "name": "eId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    w_id: None | str = field(
        default=None,
        metadata={
            "name": "wId",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "GUID",
            "type": "Attribute",
            "pattern": r"[^\s]+",
        },
    )
    refers_to: list[object] = field(
        default_factory=list,
        metadata={
            "name": "refersTo",
            "type": "Attribute",
            "tokens": True,
        },
    )
    lang: None | str | LangValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: None | SpaceValue = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    alternative_to: None | str = field(
        default=None,
        metadata={
            "name": "alternativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class PortionBody(PortionBodyType):
    """
    <ns1:type
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">Element</ns1:type>
    <ns1:name
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">portionBody</ns1:name>
    <ns1:comment
    xmlns:ns1="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"> the
    element portionBody is the container of a portion of another
    document</ns1:comment>.
    """

    class Meta:
        name = "portionBody"
        namespace = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
