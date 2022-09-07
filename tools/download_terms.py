from tqdm import tqdm
import time

from config import TERMS_PATH
from oxford_definitions.oxford_definitions import OxfordDefinitions

def main():
    with open(TERMS_PATH, "r") as file:
        terms = file.read().splitlines()
    
    oxford_definitions = OxfordDefinitions()

    for term in tqdm(terms):
        try:
            used_cache = oxford_definitions.get_words_result(term.lower())
        except:
            print("Failed for", term)    

        if not used_cache:
            time.sleep(1)

if __name__ == "__main__":
    main()
