import spacy
from spacy.matcher import Matcher


class KeyTermsParser:
    INDIVIDUAL_TOKENS = ["ADJ", "VERB"]
    GROUPED_TOKENS = ["NOUN", "PROPN"]

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)
        self.matcher.add("ADJ", [[{"POS": "ADJ"}]])
        self.matcher.add("VERB", [[{"POS": "VERB"}]])
        self.matcher.add("NOUN", [[{"POS": "NOUN", "OP": "+"}]])
        self.matcher.add("PROPN", [[{"POS": "PROPN", "OP": "+"}]])

    def parse(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)

        spans = [doc[start:end] for _, start, end in matches]
        return spacy.util.filter_spans(spans)
