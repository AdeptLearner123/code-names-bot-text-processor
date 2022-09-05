import spacy
from spacy import displacy
from spacy.pipeline import Tagger
from spacy.pipeline.tagger import DEFAULT_TAGGER_MODEL
from spacy.tokenizer import Tokenizer
from spacy.tokens import Doc
from spacy.vocab import Vocab


def main():
    nlp_model = spacy.load("en_core_web_sm")
    doc = nlp_model(
        "a solid or hollow spherical or egg-shaped object that is kicked, thrown, or hit in a game"
    )
    print(len(doc))
    with doc.retokenize() as retokenizer:
        attrs = {"LEMMA": "egg-shaped"}
        retokenizer.merge(doc[6:9], attrs=attrs)

    print("new len", len(doc))
    for token in doc:
        print(token, token.tag_)

    displacy.serve(doc, style="dep")


if __name__ == "__main__":
    main()
