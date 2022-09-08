import urllib.parse

from concurrent.futures import process

from config import COMPOUNDS_LIST_PATH, WORDLIST_PATH
from oxford_definitions.oxford_definitions import OxfordDefinitions
from oxford_definitions.oxford_model import OxfordResults

MANUAL_IGNORE = ["the Atlantic", "get on", "small round"]
MANUAL_INCLUDE = ["East Berlin"]

oxford_definitions = OxfordDefinitions()

ignored_registers = ["informal", "rare"]

def main():
    with open(WORDLIST_PATH, "r") as file:
        lemmas = file.read().splitlines()

    compounds = []

    for lemma in lemmas:
        compounds += get_compounds(lemma)

    compounds = map(format_compound, compounds)
    compounds = map(set_compound_context, compounds)
    compounds = filter(lambda compound: compound not in MANUAL_IGNORE, compounds)
    compounds = list(compounds)
    compounds += MANUAL_INCLUDE

    test_passed = sanity_test(compounds)

    if test_passed:
        with open(COMPOUNDS_LIST_PATH, "w+") as file:
            file.write("\n".join(compounds))


def get_compounds(lemma):
    results = oxford_definitions.get_cached_words_result(lemma.lower())

    if results is None:
        if is_compound(lemma):
            return [lemma]
        return []

    results = OxfordResults(results)
    compounds = []

    for result in results.results:
        # Since Oxford API is case-insensitive, ensure that result id has same capitalization to verify is same lemma.
        if result.word != lemma:
            continue

        for lexical_entry in result.lexical_entries:
            if lexical_entry.lexical_category == "idiomatic":
                # Idiomatic phrases like "by sea" should not be considered a compound
                continue

            for entry in lexical_entry.entries:
                if entry.notes is not None and entry.notes.word_form_notes is not None:
                    compounds.append(entry.notes.word_form_notes[0])
                    continue

                inflections = []
                if entry.inflections is not None:
                    # don't include "the land" or "a time"
                    # don't include inflections if has word form note (other world)
                    inflections = list(filter(lambda inflection: not inflection.startswith("the ") and not inflection.startswith("a ") and not inflection.startswith("an "), entry.inflections))

                if entry.senses is None:
                    continue
                    
                for sense in entry.senses:
                    if sense.registers is not None and any(ir in sense.registers for ir in ignored_registers):
                        continue

                    if sense.variant_forms is not None:
                            compounds += list(filter(is_compound, sense.variant_forms))

                    if sense.notes is not None and sense.notes.word_form_notes is not None:
                        compounds.append(sense.notes.word_form_notes[0])  # ie "other world" is not a compound but "the other world" is
                        continue

                    compounds += inflections
                    compounds.append(lemma)

    if "the same" in compounds:
        print("Added same", lemma)
    return list(set(filter(is_compound, compounds)))

def set_compound_context(compound):
    compound_padded = " " + compound + " "
    compound_padded = compound_padded.replace(" do something ", " <VERB> ").replace(" something ", " <NOUN> ").replace(" someone ", " <NOUN> ")
    return compound_padded.strip()


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
        "chemical reactions",
        "ice sheets",
        "Square Mile",
        "South America",
        "Atlantic Ocean",
        "mountain system",
        "egg-shaped",
        "roe deer",
        "Republic of China"
    ]
    SHOULDNT_HAVE = ["other world", "by sea", "in the world", "the earth", "take in", "on behalf of", "such as", "in order", "the land", "that is", "a time", "a bomb", "by means of", "long robe"]

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
