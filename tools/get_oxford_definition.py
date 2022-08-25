import json
import sys

from oxford_definitions.oxford_definitions import OxfordDefinitions


def main():
    term = sys.argv[1]
    oxford_definitions = OxfordDefinitions()
    result = oxford_definitions.get_result(term)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
