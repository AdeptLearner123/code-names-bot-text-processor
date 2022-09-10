import spacy
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

from config import COMPOUNDS_LIST_PATH


class TermChunker:
    CONTENT_TAGS = {"NN", "JJ", "VB", "RB"}

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")

        with open(COMPOUNDS_LIST_PATH, "r") as file:
            compounds = file.read().splitlines()
            compounds = list(map(self._format_compound, compounds))

        self._two_word_lemmas = set([n for n in compounds if self._count_tokens(n) == 2])
        self._three_word_lemmas = set([n for n in compounds if self._count_tokens(n) == 3])
        self._four_word_lemmas = set([n for n in compounds if self._count_tokens(n) == 4])

        self._stopwords = set(stopwords.words("english"))


    def chunk_and_merge(self, text, term_chunk_labels = None, labels=None):
        doc = self._nlp(text, disable=["parser", "ner"])
    
        if term_chunk_labels is not None:
            term_chunk_labels = self._get_term_chunk_labels(doc)
    
        self._merge_terms(doc, term_chunk_labels)
        term_labels = list(filter(lambda label: label != "T", term_chunk_labels))

        if labels is not None:
            new_labels = []
            for i in range(len(term_chunk_labels)):
                if term_chunk_labels[i] != "T":
                    new_labels.append(labels[i])
            return doc, term_labels, new_labels

        return doc, term_labels, None


    def chunk(self, text):
        doc = self._nlp(text, disable=["parser", "ner"])
        return self._get_term_chunk_labels(doc)


    def _get_term_chunk_labels(self, doc):
        labels = [None for _ in doc]
        self._set_multi_word_terms(doc, self._four_word_lemmas, labels, 4)
        self._set_multi_word_terms(doc, self._three_word_lemmas, labels, 3)
        self._set_multi_word_terms(doc, self._two_word_lemmas, labels, 2)
        self._set_single_word_terms(doc, labels)
        return labels
    

    def _merge_terms(self, doc, term_chunk_labels):
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

    def _format_compound(self, compound):
        if ", " in compound:
            parts = compound.split(", ")
            return parts[1] + " " + parts[0]
        return compound

    def _set_single_word_terms(self, doc, labels):
        for i in range(len(doc)):
            if labels[i] is None:
                labels[i] = (
                    "BT"
                    if doc[i].tag_[0:2] in self.CONTENT_TAGS
                    and doc.text not in self._stopwords
                    else "N"
                )

    def _set_multi_word_terms(self, doc, lemmas, labels, length):
        for i in range(len(doc) - length + 1):
            if labels[i : i + length].count(None) == length:
                span = doc[i : i + length]
                span_lemmatized = self._form_compound(span)
                if span_lemmatized in lemmas:
                    labels[i : i + length] = ["BT"] + ["T"] * (length - 1)

    def _form_compound(self, span):
        return " ".join(token.text for token in span).replace(" - ", "-")
