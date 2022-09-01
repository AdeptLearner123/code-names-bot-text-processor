import spacy
from nltk.corpus import wordnet as wn

from config import PROCESSED_COMPOUNDS_LIST_PATH
from nltk.corpus import stopwords

class TermChunker:
    CONTENT_TAGS = {"NN", "JJ", "VB", "RB"}

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")
        
        with open(PROCESSED_COMPOUNDS_LIST_PATH, "r") as file:
            compounds = file.read().splitlines()
            compounds = list(map(self._format_compound, compounds))

        self._two_word_lemmas = set(
            [n for n in compounds if len(n.split(" ")) == 2]
        )
        self._three_word_lemmas = set(
            [n for n in compounds if len(n.split(" ")) == 3]
        )
        self._stopwords = set(stopwords.words('english'))

    def chunk(self, text):
        doc = self._nlp(text, disable=["parser", "ner"])
        labels = [None for _ in doc]
        self._set_multi_word_terms(doc, self._three_word_lemmas, labels, 3)
        self._set_multi_word_terms(doc, self._two_word_lemmas, labels, 2)
        self._set_single_word_terms(doc, labels)
        return labels

    def _format_compound(self, compound):
        compound = compound.lower()
        if ", " in compound:
            parts = compound.split(", ")
            return parts[1] + " " + parts[0]
        return compound

    def _set_single_word_terms(self, doc, labels):
        for i in range(len(doc)):
            if labels[i] is None:
                labels[i] = "BT" if doc[i].tag_[0:2] in self.CONTENT_TAGS and doc.text not in self._stopwords else "N"

    def _set_multi_word_terms(self, doc, lemmas, labels, length):
        for i in range(len(doc) - length + 1):
            if labels[i : i + length].count(None) == length:
                span = doc[i : i + length]
                span_lemmatized = " ".join(token.lemma_ for token in span).lower()
                if span_lemmatized in lemmas:
                    labels[i : i + length] = ["BT"] + ["T"] * (length - 1)
