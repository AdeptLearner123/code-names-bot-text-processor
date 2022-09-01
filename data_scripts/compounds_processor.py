from concurrent.futures import process
from oxford_definitions.oxford_definitions import OxfordDefinitions
from oxford_definitions.oxford_model import OxfordResults
from config import COMPOUNDS_LIST_PATH, PROCESSED_COMPOUNDS_LIST_PATH


oxford_definitions = OxfordDefinitions()

def main():
    with open(COMPOUNDS_LIST_PATH, "r") as file:
        compounds = file.read().splitlines()
    
    processed_compounds = []

    for compound in compounds:
        processed_compounds.append(get_word_form(compound))

    processed_compounds = list(map(format_compound, processed_compounds))

    with open(PROCESSED_COMPOUNDS_LIST_PATH, "w+") as file:
        file.write("\n".join(processed_compounds))


def get_word_form(compound):
    results = oxford_definitions.get_cached_result(compound)
    if results is None:
        return compound
    results = OxfordResults(results)

    for result in results.results:
        for lexical_entry in result.lexical_entries:
            for entry in lexical_entry.entries:
                if entry.notes is not None and entry.notes.word_form_notes is not None:
                    return entry.notes.word_form_notes[0]
    return compound


def format_compound(compound):
    compound = compound.lower()
    if ", " in compound:
        parts = compound.split(", ")
        return parts[1] + " " + parts[0]
    return compound


if __name__ == "__main__":
    main()
