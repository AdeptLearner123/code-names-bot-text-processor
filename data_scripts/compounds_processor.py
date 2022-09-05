from concurrent.futures import process

from config import COMPOUNDS_LIST_PATH, WORDLIST_PATH
from oxford_definitions.oxford_definitions import OxfordDefinitions
from oxford_definitions.oxford_model import OxfordResults

oxford_definitions = OxfordDefinitions()


def main():
    with open(WORDLIST_PATH, "r") as file:
        lemmas = file.read().splitlines()

    compounds = []

    for lemma in lemmas:
        compounds += get_compounds(lemma)

    compounds = list(map(format_compound, compounds))

    test_passed = sanity_test(compounds)

    if test_passed:
        with open(COMPOUNDS_LIST_PATH, "w+") as file:
            file.write("\n".join(compounds))


def get_compounds(lemma):
    compounds = []

    if is_compound(lemma):
        compounds.append(lemma)

    results = oxford_definitions.get_cached_result(lemma)
    if results is None:
        return compounds

    results = OxfordResults(results)

    for result in results.results:
        for lexical_entry in result.lexical_entries:
            if lexical_entry.lexical_category == "idiomatic":
                # Idiomatic phrases like "by sea" should not be considered a compound
                if lemma in compounds:
                    compounds.remove(lemma)
                continue

            for entry in lexical_entry.entries:
                if entry.notes is not None and entry.notes.word_form_notes is not None:
                    compounds.append(entry.notes.word_form_notes[0])

                    if lemma in compounds:
                        compounds.remove(
                            lemma
                        )  # ie "other world" is not a compound but "the other world" is

                for sense in entry.senses:
                    if sense.variant_forms is not None:
                        compounds += list(filter(is_compound, sense.variant_forms))

    return compounds


def is_compound(word):
    return " " in word or "-" in word


def format_compound(compound):
    if ", " in compound:
        parts = compound.split(", ")
        return parts[1] + " " + parts[0]
    return compound


def sanity_test(compounds):
    passed = True
    SHOULD_HAVE = [
        "Old World",
        "the other world",
        "South Pole",
        "the Commonwealth of Nations",
        "Isthmus of Suez",
        "chemical reaction",
        "Square Mile",
        "on behalf of",
        "South America",
        "Atlantic Ocean",
        "mountain system",
        "egg-shaped",
    ]
    SHOULDNT_HAVE = ["other world", "by sea", "in the world"]

    for compound in SHOULD_HAVE:
        if compound not in compounds:
            passed = False
            print("Failed test, should have", compound)

    for compound in SHOULDNT_HAVE:
        if compound in compounds:
            passed = False
            print("Failed test, shouldn't have", compound)

    return passed


if __name__ == "__main__":
    main()
