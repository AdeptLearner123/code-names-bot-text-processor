from labeler.labels import Label


def evaluate_doc(definition_labels, definitions, key, term_chunker, model):
    labels = definition_labels[key]
    text = definitions[key]["definition"]
    term_chunk_labels = definitions[key]["term_tags"]

    doc, term_labels, labels = term_chunker.chunk_and_merge(text, term_chunk_labels, labels)
    predicted_labels = model.label(doc, term_labels)

    return filter_none_labels(labels, predicted_labels, doc)


def filter_none_labels(y_true, y_pred, doc):
    y_true_filtered = []
    y_pred_filtered = []
    tokens = []
    for i in range(len(y_true)):
        if y_true[i] == Label.NONE.value:
            continue
        y_true_filtered.append(y_true[i])
        y_pred_filtered.append(y_pred[i])
        tokens.append(doc[i].text)
    return y_true_filtered, y_pred_filtered, tokens