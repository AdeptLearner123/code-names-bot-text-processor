import yaml

from config import DEFINITION_SENTENCES_PATH, TERMS_PATH
from nltk.corpus import wordnet

def main():
    terms = list(open(TERMS_PATH, "r").read().splitlines())
    output = []
    for term in terms:
        synsets = wordnet.synsets(term.lower())
        for synset in synsets:
            definition = "<SUBJ> is " + synset.definition()
            output.append({
                "word": term,
                "sentence": definition
            })
    
    with open(DEFINITION_SENTENCES_PATH, "w") as file:
        yaml.dump(output, file)


if __name__ == "__main__":
    main()