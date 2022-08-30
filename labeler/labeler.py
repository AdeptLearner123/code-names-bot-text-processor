from enum import Enum

import spacy
import yaml
from tqdm import tqdm

from config import DATASET_PATH

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
    NONE = "", ""
    UNRELATED = "UR", Ansi.YELLOW
    RELATED = "RE", Ansi.RED
    IS = "IS", Ansi.BLUE
    EXAMPLE = "EX", Ansi.BLUE
    EQUALS = "EQ", Ansi.BLUE
    COULD_BE = "CB", Ansi.BLUE


def label(definition, term_labels):
    print_legend()
    print()
    doc = nlp(definition, disable=["parser", "ner"])
    label_options = [label for label in Label]
    labels = [Label.NONE for token in doc]

    for i in range(len(doc)):
        if term_labels[i] != "BT":
            continue

        print_state(doc, term_labels, i, labels)

        while True:
            key = input()
            try:
                idx = int(key)
            except:
                continue
            break

        labels[i] = label_options[idx]
        print(
            Ansi.LINE_UP,
            Ansi.LINE_CLEAR,
            Ansi.LINE_UP,
            Ansi.LINE_CLEAR,
            Ansi.LINE_UP,
            Ansi.LINE_CLEAR,
        )

    label_names = [label.value[0] for label in labels]
    print_state(doc, term_labels, len(labels), labels)
    return label_names


def print_legend():
    label_options = [label for label in Label]

    for i in range(len(label_options)):
        key, color = label_options[i].value
        print(f"{color}[{i}]: {key}{Ansi.END}")


def print_state(doc, term_labels, index, current_labels):
    output = ""
    for i in range(len(doc)):
        token = doc[i]

        if term_labels[i] == "N":
            output += token.text
        else:
            if term_labels[i] == "BT":
                output += current_labels[i].value[1]
                output += Ansi.UNDERLINE

                if index == i:
                    output += Ansi.BOLD

            output += token.text

            if i + 1 >= len(term_labels) or term_labels[i + 1] != "T":
                if current_labels[i] is not None:
                    output += f"[{current_labels[i].value[0]}]"
                output += Ansi.END

        output += " "
    print(output)


def main():
    with open(DATASET_PATH, "r") as file:
        definitions = yaml.safe_load(file)

    keys = list(
        filter(
            lambda key: key.endswith("OX.0.n.0.0.d0")
            or key.endswith("OX.0.v.0.0.d0")
            or key.endswith("OX.0.a.0.0.d0"),
            definitions.keys(),
        )
    )

    for key in tqdm(keys):
        labels = label(definitions[key]["definition"], definitions[key]["term_tags"])
        definitions[key]["labels"] = labels

        with open(DATASET_PATH, "w") as file:
            yaml.dump(definitions, file, default_flow_style=None, sort_keys=False)


if __name__ == "__main__":
    main()
