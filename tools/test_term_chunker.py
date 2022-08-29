import sys

from code_names_bot_text_processor.term_chunker.term_chunker import TermChunker


def main():
    term_chunker = TermChunker()
    print(term_chunker.chunk(sys.argv[1]))


if __name__ == "__main__":
    main()
