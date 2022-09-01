import spacy
from spacy.vocab import Vocab
from spacy.tokens import Doc
from spacy.pipeline import Tagger
from spacy.pipeline.tagger import DEFAULT_TAGGER_MODEL
from spacy.tokenizer import Tokenizer
from spacy import displacy

def main():
    nlp_model = spacy.load("en_core_web_sm")
    doc = nlp_model("the second largest continent, a southward projection of the Old World land mass divided roughly in two by the equator and surrounded by sea except where the Isthmus of Suez joins it to Asia.")
    print(len(doc))
    with doc.retokenize() as retokenizer:
        attrs = {"LEMMA": "Isthmus of Suez"}
        retokenizer.merge(doc[28:31], attrs=attrs)
    
    print("new len", len(doc))
    for token in doc:
        print(token, token.tag_)
    
    displacy.serve(doc, style="dep")


if __name__ == "__main__":
    main()
