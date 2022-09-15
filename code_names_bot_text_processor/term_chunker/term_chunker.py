import spacy

from config import COMPOUNDS_LIST_PATH


class TermChunker:

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")

        with open(COMPOUNDS_LIST_PATH, "r") as file:
            compounds = file.read().splitlines()

        self._two_word_lemmas = set([n for n in compounds if self._count_tokens(n) == 2])
        self._three_word_lemmas = set([n for n in compounds if self._count_tokens(n) == 3])
        self._four_word_lemmas = set([n for n in compounds if self._count_tokens(n) == 4])


    def get_term_chunk_labels(self, text):
        doc = self._nlp(text, disable=["parser", "ner"])
        labels = [None for _ in doc]
        self._set_multi_word_terms(doc, self._four_word_lemmas, labels, 4)
        self._set_multi_word_terms(doc, self._three_word_lemmas, labels, 3)
        self._set_multi_word_terms(doc, self._two_word_lemmas, labels, 2)
        labels = [label if label is not None else "BT" for label in labels]
        return labels
    

    def merge_terms(self, doc, term_chunk_labels):
        with doc.retokenize() as retokenizer:
            i = 0
            start = None
            while i < len(term_chunk_labels):
                if start is not None and term_chunk_labels[i] != "T":
                    if start != i:
                        retokenizer.merge(doc[start:i])
                    start = None
                if term_chunk_labels[i] == "BT":
                    start = i
                i += 1
            if start is not None:
                retokenizer.merge(doc[start:])

    def _count_tokens(self, lemma):
        return 1 + lemma.count(" ") + lemma.count("-") * 2

    def _set_multi_word_terms(self, doc, lemmas, labels, length):
        for i in range(len(doc) - length + 1):
            if labels[i : i + length].count(None) == length:
                span = doc[i : i + length]
                span_lemmatized = self._form_compound(span)
                if span_lemmatized in lemmas:
                    labels[i : i + length] = ["BT"] + ["T"] * (length - 1)

    def _form_compound(self, span):
        return " ".join(token.text for token in span).replace(" - ", "-")
