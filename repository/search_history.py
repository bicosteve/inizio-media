import json
from datetime import datetime, timezone
from pathlib import Path

from models.search import SearchResponse


class SearchHistoryRepository:
    def __init__(self, file_path: str = "data/searches.json"):
        self.file_path = Path(file_path)

    def save(self, search: SearchResponse) -> None:
        searches = self.get_all()

        record = search.model_dump()
        # convert SearchResponse to normal Python dictionary
        record["searched_at"] = datetime.now(timezone.utc).isoformat()

        searches.append(record)

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(searches, file, indent=2, ensure_ascii=False)

    def get_all(self) -> list[dict]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            content = file.read().strip()

            if not content:
                return []

            return json.loads(content)
