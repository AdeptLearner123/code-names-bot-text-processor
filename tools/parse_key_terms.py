from data_scripts.key_terms_parser import KeyTermsParser


def main():
    parser = KeyTermsParser()
    parser.parse(
        "a political theory derived from Karl Marx, advocating class war and leading to a society in which all property is publicly owned and each person works and is paid according to their abilities and needs."
    )


if __name__ == "__main__":
    main()
