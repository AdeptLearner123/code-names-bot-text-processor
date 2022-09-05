from enum import Enum


class Label(Enum):
    NONE = "X"
    UNRELATED = "UR"
    RELATED = "RE"
    RELATED_ADJ = "RAJ"
    RELATED_VERB = "RV"
    RELATED_ADV = "RAV"
    IS = "IS"
    EXAMPLE = "EX"
    EQUALS = "EQ"
    COULD_BE = "CB"
    IN = "IN"
    CONTAINS = "CT"
    NOT = "NT"
