import spacy
from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")


    @abstractmethod
    def label(self, doc, term_labels, pos):
        pass