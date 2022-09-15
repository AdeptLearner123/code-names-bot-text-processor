from code_names_bot_text_processor.model.model import Model
from labeler.labels import Label


class BaselineModel(Model):
    TAGS = ["NN", "JJ"]

    def label(self, doc, pos):
        labels = []

        for i in range(len(doc)):
            if doc[i].tag_[:2] in self.TAGS:
                labels.append(Label.RELATED)
            else:
                labels.append(Label.UNRELATED)

        return labels