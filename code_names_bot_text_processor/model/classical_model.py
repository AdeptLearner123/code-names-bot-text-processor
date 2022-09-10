from code_names_bot_text_processor.model.model import Model
from labeler.labels import Label


class ClassicalModel(Model):
    TAGS = ["NN", "JJ"]

    def label(self, doc, term_labels, pos):
        if pos == "v" or pos == "a":
            return [Label.NONE] * len(term_labels)
        return self.label_noun(doc)


    def label_noun(self, doc):
        token_labels = dict()
        self._process_is_noun(doc, token_labels)
        self._process_noun_chunks(doc, token_labels)

        labels = []
        for token in token_labels:
            labels.append(token_labels[token] if token in token_labels else Label.UNRELATED)
        return labels


    def _process_is_noun(self, doc, token_labels):
        is_noun = None
        unrelated_nouns = []
        adjectives = []

        current = self._find_root_noun(doc)

        while current is not None:
            if self._get_first_by_dep(current, "det", "the") is not None:
                is_noun = current
            
            prep = self._get_first_by_dep("prep", "of")
            prev = current
            current = None if prep is None else prep._get_first_by_dep("pobj")

            adjectives += self._get_children_by_dep(current, "amod")

            if current == None and is_noun is not None:
                is_noun = prev
            else:
                unrelated_nouns.append(prev)
        
        token_labels[is_noun] = Label.IS
        for token in unrelated_nouns:
            token_labels[token] = Label.UNRELATED
        for token in adjectives:
            token_labels[token] = Label.RELATED
    

    def _process_noun_chunks(self, doc, token_labels):
        for noun_chunk in doc.noun_chunks:
            for token in noun_chunk:
                if token.tag_[:2] != "NN":
                    continue
                if token not in token_labels:
                    token_labels[token] = Label.RELATED


    def _find_root_noun(self, doc):
        root = [token for token in doc if token.head == token][0]

        if root.tag_[:2] == "NN":
            return root        
        elif root.tag_[:2] == "VB":
            return self._get_first_by_dep(root, "nsubj")
        return None


    def _get_first_by_dep(self, token, dep, text = None):
        for child in token.children:
            if child.dep_ == dep and (text is None or child.text == text):
                return child
        return None
    

    def _get_children_by_dep(self, token, dep):
        return [child for child in token.children if child.dep_ == dep]