import sys

import spacy
import yaml
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from tqdm import tqdm

from config import DEFINITIONS_PATH, LABELS_PATH

from .labeler_window import LabelerWindow
from .labels import Label

nlp = spacy.load("en_core_web_sm")


class Labeler:
    def __init__(self):
        with open(DEFINITIONS_PATH, "r") as file:
            self.definitions = yaml.safe_load(file)

        with open(LABELS_PATH, "r") as file:
            self.definition_labels = yaml.safe_load(file)

        if self.definition_labels is None:
            self.definition_labels = dict()

        self.keys = list(
            filter(
                lambda key: key.endswith("OX.0.n.0.0.d0")
                or key.endswith("OX.0.v.0.0.d0")
                or key.endswith("OX.0.a.0.0.d0"),
                self.definitions.keys(),
            )
        )

        self.current = 0

    def start(self):
        app = QtWidgets.QApplication([])

        self.widget = LabelerWindow()
        self.widget.resize(800, 600)
        self.widget.show()

        self.set_definition()
        self.widget.next_signal.connect(self.next_handler)
        self.widget.prev_signal.connect(self.prev_handler)
        sys.exit(app.exec())

    def save_labels(self, labels):
        self.definition_labels[self.keys[self.current]] = [
            label.value for label in labels
        ]
        with open(LABELS_PATH, "w+") as file:
            yaml.dump(
                self.definition_labels, file, default_flow_style=None, sort_keys=False
            )

    @Slot(list)
    def next_handler(self, labels):
        self.save_labels(labels)
        self.current = min(self.current + 1, len(self.keys))
        self.set_definition()

    @Slot(list)
    def prev_handler(self, labels):
        self.save_labels(labels)
        self.current = max(self.current - 1, 0)
        self.set_definition()

    def set_definition(self):
        print("Current", str(self.current) + " / " + str(len(self.keys)))
        current_key = self.keys[self.current]
        definition = self.definitions[current_key]["definition"]
        doc = nlp(definition, disable=["parser", "ner"])
        tokens = [token.text for token in doc]
        term_tags = self.definitions[current_key]["term_tags"]
        if current_key in self.definition_labels:
            labels = [Label(label) for label in self.definition_labels[current_key]]
        else:
            labels = [Label.NONE for token in tokens]
        self.widget.set_definition(tokens, labels, term_tags)


def main():
    labeler = Labeler()
    labeler.start()


if __name__ == "__main__":
    main()
