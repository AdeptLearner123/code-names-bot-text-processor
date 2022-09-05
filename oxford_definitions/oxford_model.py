class OxfordResults:
    def __init__(self, json):
        self.error = json["error"] if "error" in json else None
        self.id = json["id"] if "id" in json else None
        self.results = (
            [OxfordResult(resultJson) for resultJson in json["results"]]
            if "results" in json
            else None
        )


class OxfordResult:
    def __init__(self, json):
        self.id = json["id"]
        self.lexical_entries = [
            LexicalEntry(lexical_entry_json)
            for lexical_entry_json in json["lexicalEntries"]
        ]


class LexicalEntry:
    def __init__(self, json):
        self.lexical_category = json["lexicalCategory"]["id"]
        self.entries = [Entry(entry_json) for entry_json in json["entries"]]


class Entry:
    def __init__(self, json):
        self.notes = Notes(json["notes"]) if "notes" in json else None
        self.senses = [Sense(sense_json) for sense_json in json["senses"]]


class Notes:
    def __init__(self, json):
        self.word_form_notes = None

        for note in json:
            if note["type"] == "wordFormNote":
                self.word_form_notes = note["text"].replace('"', "").split(",")


class Sense:
    def __init__(self, json):
        self.definitions = json["definitions"] if "definitions" in json else None
        self.subsenses = (
            [Subsense(subsense_json) for subsense_json in json["subsenses"]]
            if "subsenses" in json
            else None
        )
        self.notes = Notes(json["notes"]) if "notes" in json else None

        self.variant_forms = None
        if "variantForms" in json:
            self.variant_forms = []
            for variant_form_json in json["variantForms"]:
                self.variant_forms.append(variant_form_json["text"])


class Subsense:
    def __init__(self, json):
        self.definitions = json["definitions"] if "definitions" in json else None
