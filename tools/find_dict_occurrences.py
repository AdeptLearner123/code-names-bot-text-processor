from tqdm import tqdm
import spacy
import sys

from oxford_definitions.oxford_definitions import OxfordDefinitions
from oxford_definitions.oxford_model import OxfordResults

nlp = spacy.load("en_core_web_sm", disable=['ner', 'tagger', 'parser'])


def process_definition(definition, term):
    doc = nlp(definition)
    for token in doc:
        if token.lemma_ == sys.argv[1]:
            print(f"{term}: {definition}")
            return


def main():
    oxford_definitions = OxfordDefinitions()
    cached = oxford_definitions.get_all_cached()
    
    processed_ids = set()

    for term in cached:
        if term == "asia" or term == "europe" or term == "africa":
            print("Found term", term)

        json, _ = oxford_definitions.get_words_result(term)
        oxford_results = OxfordResults(json)
        for oxford_result in oxford_results.results:
            if oxford_result.id in processed_ids:
                continue
            processed_ids.add(oxford_result.id)

            for lexical_entry in oxford_result.lexical_entries:
                for entry in lexical_entry.entries:
                    if entry.senses is None:
                        continue
                    for sense in entry.senses:
                        if sense.definitions is not None:
                            for definition in sense.definitions:
                                process_definition(definition, term)
                        if sense.subsenses is not None:
                            for subsense in sense.subsenses:
                                if subsense.definitions is not None:
                                    for definition in subsense.definitions:
                                        process_definition(definition, term)


if __name__ == "__main__":
    main()
