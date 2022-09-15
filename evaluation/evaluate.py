import sys
import yaml
from tqdm import tqdm

from sklearn.metrics import classification_report

from models import ModelType, get_model, get_predictions_file_path
from code_names_bot_text_processor.term_chunker.term_chunker import TermChunker
from labeler.labels import Label
from config import DEFINITIONS_PATH, LABELS_PATH
from .evaluation_utils import evaluate_doc

MODEL_TYPE = ModelType.CLASSICAL


def main():
    with open(LABELS_PATH, "r") as file:
        definition_labels = yaml.safe_load(file)
    
    with open(DEFINITIONS_PATH, "r") as file:
        definitions = yaml.safe_load(file)

    predictions = dict()
    term_chunker = TermChunker()
    model = get_model(MODEL_TYPE)

    y_true = []
    y_pred = []

    for key in tqdm(definition_labels):
        print("Evaluating", key)
        (filtered_true_labels, filtered_predictions, _), predicted_labels = evaluate_doc(definition_labels, definitions, key, term_chunker, model)
        y_true += filtered_true_labels
        y_pred += filtered_predictions
        predictions[key] = predicted_labels
    
    if len(sys.argv) == 3:
        y_true = binarize_labels(y_true)
        y_pred = binarize_labels(y_pred)

    print(classification_report(y_true, y_pred))

    with open(get_predictions_file_path(MODEL_TYPE), "w+") as file:
        yaml.dump(predictions, file, default_flow_style=None, sort_keys=False,)


def binarize_labels(labels):
    return list(map(lambda label: Label.RELATED.value if label != Label.UNRELATED.value else label, labels))


if __name__ == "__main__":
    main()
