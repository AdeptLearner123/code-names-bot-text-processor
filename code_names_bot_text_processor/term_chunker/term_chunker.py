import spacy
from nltk.corpus import wordnet as wn


class TermChunker:
    CONTENT_TAGS = {"NN", "JJ", "VB", "RB"}

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")
        self._two_word_lemmas = set(
            [n for n in wn.all_lemma_names() if len(n.split("_")) == 2]
        )
        self._three_word_lemmas = set(
            [n for n in wn.all_lemma_names() if len(n.split("_")) == 3]
        )

    def chunk(self, text):
        doc = self._nlp(text, disable=["parser", "ner"])
        labels = [None for _ in doc]
        self._set_multi_word_terms(doc, self._three_word_lemmas, labels, 3)
        self._set_multi_word_terms(doc, self._two_word_lemmas, labels, 2)
        self._set_single_word_terms(doc, labels)
        return labels

    def _set_single_word_terms(self, doc, labels):
        for i in range(len(doc)):
            if labels[i] is None:
                labels[i] = "BT" if doc[i].tag_[0:2] in self.CONTENT_TAGS else "N"

    def _set_multi_word_terms(self, doc, lemmas, labels, length):
        for i in range(len(doc) - length + 1):
            if labels[i : i + length].count(None) == length:
                span = doc[i : i + length]
                span_lemmatized = "_".join(token.lemma_ for token in span).lower()
                if span_lemmatized in lemmas:
                    labels[i : i + length] = ["BT"] + ["T"] * (length - 1)
