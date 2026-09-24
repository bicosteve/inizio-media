from models.search import SearchResponse
from services.search_service import SearchService


class FakeProvider:

    def __init__(self, response: dict):
        self.response = response

    def search(self, query: str) -> dict:
        return self.response


class FakeHistoryRepository:
    def __init__(self):
        self.saved: list[SearchResponse] = []

    def save(self, search) -> None:
        self.saved.append(search)

    def get_all(self):
        return self.saved


def test_search_service_returns_search_response():
    provider_response = {
        "organic_results": [
            {
                "title": "FastAPI",
                "link": "https://fastapi.tiangolo.com/",
                "snippet": "FastAPI documentation",
            },
            {
                "title": "Python",
                "link": "https://python.org/",
                "snippet": "Python programming language",
            },
        ]
    }

    provider = FakeProvider(provider_response)
    history_repository = FakeHistoryRepository()

    service = SearchService(
        provider,
        history_repository=history_repository,
    )

    response = service.search("fastapi")

    assert response.query == "fastapi"
    assert response.engine == "google"
    assert response.page == 1
    assert len(response.results) == 2

    assert response.results[0].position == 1
    assert response.results[0].title == "FastAPI"

    assert response.results[1].position == 2
    assert response.results[1].title == "Python"
