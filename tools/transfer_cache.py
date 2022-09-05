from tqdm import tqdm

import sqlite3
import json
from oxford_definitions.oxford_definitions import OxfordDefinitions
from oxford_definitions.oxford_model import OxfordResults

old_con = sqlite3.connect("/Users/zonalu/oxford_cache/oxford_cache_old.sqlite")
old_cur = old_con.cursor()

oxford_definitions = OxfordDefinitions()

old_cur.execute("SELECT query, result FROM oxford_cache;")
rows = old_cur.fetchall()

for row in tqdm(rows):
    query, result = row
    results = OxfordResults(json.loads(result))
    if results.error is not None:
        print("Skipping since error ", query)
        continue

    print("Inserting", query)
    oxford_definitions.cache_entries(query, result)