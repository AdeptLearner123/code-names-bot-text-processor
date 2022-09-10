import sys
import yaml
from tqdm import tqdm

from sklearn.metrics import classification_report

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

    y_true = []
    y_pred = []

    for key in tqdm(definition_labels):
        labels, predicted_labels, _ = evaluate_doc(definition_labels, definitions, key, term_chunker, model)
        y_true += labels
        y_pred += predicted_labels
    
    if len(sys.argv) == 3:
        y_true = binarize_labels(y_true)
        y_pred = binarize_labels(y_pred)

    print(classification_report(y_true, y_pred))


def binarize_labels(labels):
    return list(map(lambda label: Label.RELATED.value if label != Label.UNRELATED.value else label, labels))


if __name__ == "__main__":
    main()
