import sys

import spacy
from spacy import displacy


def main():
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sys.argv[1])

    displacy.serve(doc, style="ent")


if __name__ == "__main__":
    main()