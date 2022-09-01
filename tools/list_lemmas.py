from nltk.corpus import wordnet as wn


def main():
    lemmas = [n for n in wn.all_lemma_names() if len(n.split("_")) == 1]
    print(len(lemmas))


if __name__ == "__main__":
    main()
