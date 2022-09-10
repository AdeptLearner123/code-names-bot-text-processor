from code_names_bot_text_processor.model.model import Model
from labeler.labels import Label


class BaselineModel(Model):
    TAGS = ["NN", "JJ"]

    def label(self, doc, term_labels, pos):
        labels = []

        for i in range(len(doc)):
            if doc[i].tag_[:2] in self.TAGS and term_labels[i] != "X":
                labels.append(Label.RELATED)
            else:
                labels.append(Label.UNRELATED)

        return [label.value for label in labels]