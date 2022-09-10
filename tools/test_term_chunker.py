from lib2to3.pytree import Base
import sys

from code_names_bot_text_processor.term_chunker.term_chunker import TermChunker
from code_names_bot_text_processor.model.baseline_model import BaselineModel


def main():
    term_chunker = TermChunker()
    doc, term_labels, _ = term_chunker.chunk_and_merge(sys.argv[1])

    model = BaselineModel()
    predicted_labels = model.label(doc, term_labels)

    for i in range(len(doc)):
        print("Token", doc[i], "Label", predicted_labels[i])


if __name__ == "__main__":
    main()
