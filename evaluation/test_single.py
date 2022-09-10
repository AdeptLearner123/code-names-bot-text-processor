import sys
import yaml

from code_names_bot_text_processor.model.baseline_model import BaselineModel
from code_names_bot_text_processor.term_chunker.term_chunker import TermChunker
from labeler.labels import Label
from config import DEFINITIONS_PATH, LABELS_PATH
from .evaluation_utils import evaluate_doc


def main():
    with open(LABELS_PATH, "r") as file:
        definition_labels = yaml.safe_load(file)

    with open(DEFINITIONS_PATH, "r") as file:
        definitions = yaml.safe_load(file)

    term_chunker = TermChunker()
    model = BaselineModel()

    y_true, y_pred, tokens = evaluate_doc(definition_labels, definitions, sys.argv[1], term_chunker, model)

    for i in range(len(y_true)):
        print(tokens[i], y_true[i], y_pred[i])

if __name__ == "__main__":
    main()
