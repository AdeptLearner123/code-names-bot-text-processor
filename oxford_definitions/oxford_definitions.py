import json
import sqlite3

import requests

from config import OXFORD_CACHE_PATH
from credentials import OXFORD_APP_ID, OXFORD_APP_KEY

GET_URL = lambda is_us, term: f"https://od-api.oxforddictionaries.com/api/v2/entries/{'en-us' if is_us else 'en-gb'}/{term}"


class OxfordDefinitions:
    def __init__(self):
        self.con = sqlite3.connect(OXFORD_CACHE_PATH)
        self.cur = self.con.cursor()
        self.setup()

    def setup(self):
        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS oxford_cache (
                    term TEXT NOT NULL UNIQUE,
                    is_us INT NOT NULL,
                    entries TEXT,
                    inflections TEXT
                );
            """
        )
        self.cur.execute(
            """
                CREATE INDEX IF NOT EXISTS term_index ON oxford_cache (term);
            """
        )

    def insert_term(self, term, is_us):
        self.cur.execute("INSERT INTO oxford_cache (term, is_us) VALUES (?, ?);", [term, is_us])

    def get_entries(self, term):
        term = term.lower()
        is_us, cached_entries = self.get_cached_row(term)
        if cached_entries is not None:
            return json.loads(cached_entries), True

        url = GET_URL(is_us, term)
        r = requests.get(
            url, headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY}
        )
        self.cache_entries(term, json.dumps(r.json()))
        self.commit()
        return r.json(), False

    def get_cached_row(self, term):
        self.cur.execute(
            "SELECT is_us, entries FROM oxford_cache WHERE term=? LIMIT 1", [term]
        )
        row = self.cur.fetchone()
        return row

    def cache_entries(self, term, entries):
        self.cur.execute(
            "UPDATE oxford_cache SET entries=? WHERE term=?;", [entries, term]
        )

    def get_all_cached(self):
        self.cur.execute("SELECT term FROM oxford_cache WHERE entries IS NOT NULL")
        rows = self.cur.fetchall()
        return [row[0] for row in rows]

    def commit(self):
        self.con.commit()
