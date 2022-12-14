import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Signal

from .labels import Label

LABEL_COLORS = {
    Label.NONE: "#f7f7f7",  # white
    Label.UNRELATED: "#ebdd4b",  # yellow
    Label.RELATED: "#eb4b4b",  # red
    Label.IS: "#4b5eeb",  # blue
    Label.EXAMPLE: "#564beb",  # blue - purple
    Label.EQUALS: "#6b4beb",  # purple,
    Label.COULD_BE: "#804beb",  # violet
    Label.IN: "#67b6bb",  # blue
    Label.CONTAINS: "#1083cc",  # blue
    Label.NOT: "#58c27d",  # green
}


class LabelerWindow(QtWidgets.QWidget):
    CONTENT_TAGS = {"NN", "JJ", "VB", "RB"}
    INPUT_KEYS = "0123456789abcdefg"

    next_signal = Signal(list)
    prev_signal = Signal(list)

    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.label_options = [label for label in Label]

        self._add_title()
        self._add_legend()
        self.sentence_widget = None

        self.cleanup_widgets = []

    def _add_legend(self):
        legend_widget = QtWidgets.QWidget()
        legend_layout = QtWidgets.QVBoxLayout()
        legend_layout.addStretch()
        legend_widget.setLayout(legend_layout)

        self.layout.addWidget(legend_widget)

        for i in range(len(self.label_options)):
            label = self.label_options[i]
            legend_label_widget = QtWidgets.QLabel(
                f'<span style="color:{LABEL_COLORS[label]};">[{self.INPUT_KEYS[i]}]  {label.value}</span>'
            )
            legend_layout.addWidget(legend_label_widget)

    def _add_title(self):
        self.title = QtWidgets.QLabel()
        self.layout.addWidget(self.title)

    def _add_sentence(self):
        sentence_widget = QtWidgets.QWidget()
        sentence_layout = QtWidgets.QHBoxLayout(self)
        sentence_layout.setSpacing(0)
        sentence_widget.setLayout(sentence_layout)

        self.layout.addWidget(sentence_widget)
        self.sentence_layout = sentence_layout
        self.sentence_widget = sentence_widget

    def _clear(self):
        if self.sentence_widget is not None:
            self.sentence_widget.destroy()
            self.sentence_widget.setParent(None)

        self._add_sentence()

    def set_definition(self, doc, labels, title):
        self.current = -1
        self.doc = doc
        self.labels = labels
        self.title.setText(f"<h1>{title}</h1>")
        self._next_term()
        self._render()

    def _render(self):
        self._clear()

        for i in range(len(self.doc)):
            self.sentence_layout.addWidget(self._create_token_widget(i)[0])

        self.sentence_layout.addStretch()

    def _create_token_widget(self, i):
        text = self.doc[i].text
        label = self.labels[i]

        item_widget = QtWidgets.QWidget()
        item_layout = QtWidgets.QVBoxLayout(self)
        item_layout.addStretch()
        item_widget.setLayout(item_layout)

        token_label_widget = QtWidgets.QLabel(
            f'<span style="color:{LABEL_COLORS[label]};">{self._underline_if_content(i, self._bold_if_current(i, text))}</span>'
        )
        label_label_widget = self._create_label_widget(label)
        item_layout.addWidget(token_label_widget)
        item_layout.addWidget(label_label_widget)

        return item_widget, item_layout

    def _create_label_widget(self, label):
        return QtWidgets.QLabel(
            f"<span style=\"color:{LABEL_COLORS[label]};\">{'' if label is Label.NONE else label.value}</span>"
        )

    def _underline_if_content(self, i, text):
        return f"{'<u>' if self._is_content(self.doc[i]) else ''}{text}{'</u>' if self._is_content(self.doc[i]) else ''}"

    def _bold_if_current(self, i, text):
        return f"{'<b>' if self.current == i else ''}{text}{'</b>' if self.current == i else ''}"

    def _prev_term(self):
        for i in range(self.current - 1, -1, -1):
            if self._is_content(self.doc[i]):
                self.current = i
                return

    def _next_term(self):
        for i in range(self.current + 1, len(self.doc)):
            if self._is_content(self.doc[i]):
                self.current = i
                return

    def _is_content(self, token):
        return token.tag_[:2] in self.CONTENT_TAGS

    def keyPressEvent(self, event):
        if event.key() == 16777237:  # Down
            self.next_signal.emit(self.labels)
            return
        elif event.key() == 16777235:  # Up
            self.prev_signal.emit(self.labels)
            return
        elif event.key() == 16777234:  # Left
            self._prev_term()
        elif event.key() == 16777236:  # Right
            self._next_term()
        elif event.text() in self.INPUT_KEYS:
            input_index = self.INPUT_KEYS.index(event.text())
            self.labels[self.current] = self.label_options[input_index]
        self._render()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = LabelerWindow()
    widget.resize(800, 600)
    widget.show()
    widget.set_definition(
        ["I", "saw", "a", "flying saucer"],
        [Label.NONE, Label.NONE, Label.NONE, Label.IS],
        [True, False, False, True],
    )

    sys.exit(app.exec())
