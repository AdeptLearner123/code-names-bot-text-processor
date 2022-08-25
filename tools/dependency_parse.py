import spacy
from spacy import displacy


def main():
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(
        "A leprechaun is a diminutive supernatural being in Irish folklore, classed by some as a type of solitary fairy."
    )

    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)

    displacy.serve(doc, style="dep")


if __name__ == "__main__":
    main()
