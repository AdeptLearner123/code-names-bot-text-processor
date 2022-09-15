import spacy
from labeler.labels import Label


nlp = spacy.load("en_core_web_sm")

def evaluate_doc(definition_labels, definitions, key, term_chunker, model):
    labels = definition_labels[key]
    text = definitions[key]["definition"]
    term_chunk_labels = definitions[key]["term_tags"]
    pos = key.split(".")[3]

    doc = nlp(text, disable=["ner"])
    term_chunker.merge_terms(doc, term_chunk_labels)
    predicted_labels = model.label(doc, pos)
    predicted_labels = [label.value for label in predicted_labels]

    return filter_none_labels(labels, predicted_labels, doc), predicted_labels


def filter_none_labels(y_true, y_pred, doc):
    y_true_filtered = []
    y_pred_filtered = []
    tokens = []
    for i in range(len(y_true)):
        if y_true[i] == Label.NONE:
            continue
        y_true_filtered.append(y_true[i])
        y_pred_filtered.append(y_pred[i])
        tokens.append(doc[i].text)
    return y_true_filtered, y_pred_filtered, tokens