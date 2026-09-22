import json
from pathlib import Path


class GoogleSearchProvider:
    def __init__(self, fixture_path: Path):
        self.fixture_path = fixture_path

    def search(self, query: str) -> dict:
        with self.fixture_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

            data["query"] = query

            return data
