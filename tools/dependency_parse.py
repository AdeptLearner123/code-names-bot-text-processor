import spacy
from spacy import displacy


def main():
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("a teddy bear.")

    for token in doc:
        print(token.text, token.pos_)

    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)

    displacy.serve(doc, style="dep")


if __name__ == "__main__":
    main()
