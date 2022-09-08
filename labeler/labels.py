from enum import Enum


class Label(Enum):
    NONE = "X"
    UNRELATED = "UR"
    RELATED = "RE"
    NOT = "NT"

    IS = "IS"
    EXAMPLE = "EX"
    EQUALS = "EQ"
    COULD_BE = "CB"

    IN = "IN"
    CONTAINS = "CT"
