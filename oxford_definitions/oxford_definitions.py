import json
import sqlite3

import requests

from config import OXFORD_CACHE_PATH
from credentials import OXFORD_APP_ID, OXFORD_APP_KEY

API_PREFIX = "https://od-api.oxforddictionaries.com/api/v2/entries/en-us/"


class OxfordDefinitions:
    def __init__(self):
        self.con = sqlite3.connect(OXFORD_CACHE_PATH)
        self.cur = self.con.cursor()
        self.setup()

    def setup(self):
        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS oxford_cache (
                    query TEXT NOT NULL UNIQUE,
                    result TEXT NOT NULL
                );
            """
        )
        self.cur.execute(
            """
                CREATE INDEX IF NOT EXISTS query_index ON oxford_cache (query);
            """
        )

    def get_result(self, query):
        query = query.lower()
        cached_result = self.get_cached_result(query)
        if cached_result is not None:
            return cached_result

        url = f"{API_PREFIX}{query}"
        r = requests.get(
            url, headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY}
        )
        self.cache_result(query, json.dumps(r.json()))
        self.commit()
        return r.json()

    def get_cached_result(self, query):
        self.cur.execute(
            "SELECT result FROM oxford_cache WHERE query=? LIMIT 1", [query]
        )
        row = self.cur.fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    def cache_result(self, query, result):
        self.cur.execute(
            "INSERT INTO oxford_cache (query, result) VALUeS (?,?);", [query, result]
        )

    def commit(self):
        self.con.commit()
