import json

import yaml
from tqdm import tqdm

from config import DEFINITION_SENTENCES_PATH, TERMS_PATH
from oxford_definitions.oxford_definitions import OxfordDefinitions


def add_definition(output, key, definition):
    if key in output:
        raise Exception("Key already exists", key)

    output[key] = {"definition": definition}


def add_result_definitions(output, result, query):
    if "error" in result:
        print("Skipping", query)
        return

    query = query.lower().replace(" ", "_")
    print(query)
    oxford_prefix = "OX"
    for i1 in range(0, len(result["results"])):
        search_result = result["results"][i1]
        for lexical_entry in search_result["lexicalEntries"]:
            pos = lexical_entry["lexicalCategory"]["id"]

            if pos == "noun":
                pos_tag = "n"
            elif pos == "verb":
                pos_tag = "v"
            elif pos == "adjective":
                pos_tag = "a"
            else:
                continue

            for i2 in range(0, len(lexical_entry["entries"])):
                entry = lexical_entry["entries"][i2]

                for i3 in range(0, len(entry["senses"])):
                    sense = entry["senses"][i3]
                    if "definitions" in sense:
                        for di in range(0, len(sense["definitions"])):
                            key = f"{query}.{oxford_prefix}.{i1}.{pos_tag}.{i2}.{i3}.d{di}"
                            add_definition(output, key, sense["definitions"][di])

                if "subsenses" in sense:
                    for i4 in range(0, len(sense["subsenses"])):
                        subsense = sense["subsenses"][i4]
                        if "definitions" in subsense:
                            for di in range(0, len(subsense["definitions"])):
                                key = f"{query}.{oxford_prefix}.{i1}.{pos_tag}.{i2}.{i3}.{i4}.d{di}"
                                add_definition(output, key, subsense["definitions"][di])


def main():
    terms = list(open(TERMS_PATH, "r").read().splitlines())
    output = dict()
    oxford_definitions = OxfordDefinitions()

    for term in tqdm(terms):
        result = oxford_definitions.get_result(term)
        add_result_definitions(output, result, term)

    print("Writing", len(output))
    with open(DEFINITION_SENTENCES_PATH, "w") as file:
        yaml.dump(output, file)


if __name__ == "__main__":
    main()
