import json
import sqlite3

import requests

from config import OXFORD_CACHE_PATH
from credentials import OXFORD_APP_ID, OXFORD_APP_KEY

GET_URL = lambda is_us: f"https://od-api.oxforddictionaries.com/api/v2/words/{'en-us' if is_us else 'en-gb'}"


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
                    words_result TEXT
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

    def get_words_result(self, term):
        term = term.lower()
        is_us, cached_words_result = self.get_cached_row(term)
        if cached_words_result is not None:
            return json.loads(cached_words_result), True

        url = GET_URL(is_us)
        r = requests.get(
            url, headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY}, params={"q": term}
        )
        if r.status_code == 200 and "error" not in r.json():
            self.cache_words_result(term, json.dumps(r.json()))
            self.commit()
        return r.json(), False

    def get_cached_row(self, term):
        self.cur.execute(
            "SELECT is_us, words_result FROM oxford_cache WHERE term=? LIMIT 1", [term]
        )
        row = self.cur.fetchone()
        return row

    def get_cached_words_result(self, term):
        row = self.get_cached_row(term)
        if row[1] is None:
            return None
        return json.loads(row[1])

    def cache_words_result(self, term, words_result):
        self.cur.execute(
            "UPDATE oxford_cache SET words_result=? WHERE term=?;", [words_result, term]
        )

    def get_all_cached(self):
        self.cur.execute("SELECT term FROM oxford_cache WHERE words_result IS NOT NULL;")
        rows = self.cur.fetchall()
        return [row[0] for row in rows]
    
    def get_term_to_region(self):
        self.cur.execute("SELECT term, is_us FROM oxford_cache;")
        rows = self.cur.fetchall()
        term_to_region = dict()
        for row in rows:
            term_to_region[row[0]] = bool(row[1])
        return term_to_region

    def commit(self):
        self.con.commit()
