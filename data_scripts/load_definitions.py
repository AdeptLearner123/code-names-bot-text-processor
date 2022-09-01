import yaml
from tqdm import tqdm

from code_names_bot_text_processor.term_chunker.term_chunker import TermChunker
from config import DEFINITIONS_PATH, TERMS_PATH
from oxford_definitions.oxford_definitions import OxfordDefinitions
from oxford_definitions.oxford_model import OxfordResults

term_chunker = TermChunker()


def add_definition(output, key, definition):
    if key in output:
        raise Exception("Key already exists", key)

    output[key] = {
        "definition": definition,
        "term_tags": term_chunker.chunk(definition),
    }


def add_result_definitions(output, results: OxfordResults, query):
    if results.error is not None:
        print("Skipping", query)
        return

    query = query.lower().replace(" ", "_")
    oxford_prefix = "OX"
    for i1 in range(len(results.results)):
        search_result = results.results[i1]
        for lexical_entry in search_result.lexical_entries:
            pos = lexical_entry.lexical_category

            if pos == "noun":
                pos_tag = "n"
            elif pos == "verb":
                pos_tag = "v"
            elif pos == "adjective":
                pos_tag = "a"
            else:
                continue

            for i2 in range(len(lexical_entry.entries)):
                entry = lexical_entry.entries[i2]

                for i3 in range(len(entry.senses)):
                    sense = entry.senses[i3]
                    if sense.definitions is not None:
                        for di in range(len(sense.definitions)):
                            key = f"{query}.{oxford_prefix}.{i1}.{pos_tag}.{i2}.{i3}.d{di}"
                            add_definition(output, key, sense.definitions[di])

                if sense.subsenses is not None:
                    for i4 in range(0, len(sense.subsenses)):
                        subsense = sense.subsenses[i4]
                        if subsense.definitions is not None:
                            for di in range(len(subsense.definitions)):
                                key = f"{query}.{oxford_prefix}.{i1}.{pos_tag}.{i2}.{i3}.{i4}.d{di}"
                                add_definition(output, key, subsense.definitions[di])


def main():
    terms = list(open(TERMS_PATH, "r").read().splitlines())
    output = dict()
    oxford_definitions = OxfordDefinitions()

    for term in tqdm(terms):
        result = OxfordResults(oxford_definitions.get_result(term))
        add_result_definitions(output, result, term)

    print("Writing", len(output))
    with open(DEFINITIONS_PATH, "w") as file:
        yaml.dump(
            output,
            file,
            default_flow_style=None,
            sort_keys=False,
        )


if __name__ == "__main__":
    main()
