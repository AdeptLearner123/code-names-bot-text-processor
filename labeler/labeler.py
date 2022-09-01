from enum import Enum

import spacy
import yaml
from tqdm import tqdm

from config import DEFINITIONS_PATH, LABELS_PATH

nlp = spacy.load("en_core_web_sm")


class Ansi:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    LINE_UP = "\033[1A"
    LINE_CLEAR = "\x1b[2K"


class Label(Enum):
    NONE = "X"
    UNRELATED = "UR"
    RELATED = "RE"
    RELATED_ADJ = "RA"
    RELATED_VERB = "RV"
    IS = "IS"
    EXAMPLE = "EX"
    EQUALS = "EQ"
    COULD_BE = "CB"


LABEL_COLORS = {
    Label.NONE: "",
    Label.UNRELATED: Ansi.YELLOW,
    Label.RELATED: Ansi.RED,
    Label.RELATED_ADJ: Ansi.RED,
    Label.RELATED_VERB: Ansi.RED,
    Label.IS: Ansi.BLUE,
    Label.EXAMPLE: Ansi.BLUE,
    Label.EQUALS: Ansi.BLUE,
    Label.COULD_BE: Ansi.BLUE
}


def label_definition(definition, term_labels, labels):
    print_legend()
    print()
    doc = nlp(definition, disable=["parser", "ner"])
    label_options = [label for label in Label]

    if labels is None:
        labels = [Label.NONE for token in doc]
    else:
        labels = [Label(label) for label in labels]

    for i in range(len(doc)):
        if term_labels[i] != "BT":
            continue

        print_state(doc, term_labels, i, labels)

        while True:
            key = input()
            try:
                idx = int(key)
                labels[i] = label_options[idx]
            except:
                pass
            break

        print(
            Ansi.LINE_UP,
            Ansi.LINE_CLEAR,
            Ansi.LINE_UP,
            Ansi.LINE_CLEAR,
            Ansi.LINE_UP,
            Ansi.LINE_CLEAR,
        )

    label_names = [label.value for label in labels]
    print_state(doc, term_labels, len(labels), labels)
    return label_names


def print_legend():
    label_options = [label for label in Label]

    for i in range(len(label_options)):
        print(f"{LABEL_COLORS[label_options[i]]}[{i}]: {label_options[i].value}{Ansi.END}")


def print_state(doc, term_labels, index, current_labels):
    output = ""
    for i in range(len(doc)):
        token = doc[i]

        if term_labels[i] == "N":
            output += token.text
        else:
            if term_labels[i] == "BT":
                output += LABEL_COLORS[current_labels[i]]
                output += Ansi.UNDERLINE

                if index == i:
                    output += Ansi.BOLD

            output += token.text

            if i + 1 >= len(term_labels) or term_labels[i + 1] != "T":
                if current_labels[i] is not None:
                    output += f"[{current_labels[i].value}]"
                output += Ansi.END

        output += " "
    print(output)


def main():
    with open(DEFINITIONS_PATH, "r") as file:
        definitions = yaml.safe_load(file)
    
    with open(LABELS_PATH, "r") as file:
        labels = yaml.safe_load(file)
    
    if labels is None:
        labels = dict()

    keys = list(
        filter(
            lambda key: key.endswith("OX.0.n.0.0.d0")
            or key.endswith("OX.0.v.0.0.d0")
            or key.endswith("OX.0.a.0.0.d0"),
            definitions.keys(),
        )
    )

    for key in tqdm(keys):
        curr_labels = labels[key] if key in labels else None
        definition_labels = label_definition(definitions[key]["definition"], definitions[key]["term_tags"], curr_labels)
        labels[key] = definition_labels

        with open(LABELS_PATH, "w+") as file:
            yaml.dump(labels, file, default_flow_style=None, sort_keys=False)


if __name__ == "__main__":
    main()
