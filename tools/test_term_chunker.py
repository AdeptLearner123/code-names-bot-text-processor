from lib2to3.pytree import Base
import sys

from code_names_bot_text_processor.term_chunker.term_chunker import TermChunker
from code_names_bot_text_processor.model.baseline_model import BaselineModel


def main():
    term_chunker = TermChunker()
    term_chunk_labels = term_chunker.get_term_chunk_labels(sys.argv[1])
    print(term_chunk_labels)


if __name__ == "__main__":
    main()
