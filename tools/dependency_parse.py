import spacy
from spacy import displacy


def main():
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(
        "A tablet computer, commonly shortened to tablet, is a mobile device, typically with a mobile operating system and touchscreen display processing circuitry, and a rechargeable battery in a single, thin and flat package."
    )

    for token in doc:
        print(token.text, token.pos_)

    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)

    displacy.serve(doc, style="dep")


if __name__ == "__main__":
    main()
