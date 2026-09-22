from fastapi.testclient import TestClient

from main import app
from routes.search import get_search_service


class FakeSearchService:
    def search(self, query: str):
        return {
            "query": query,
            "engine": "google",
            "page": 1,
            "results": [
                {
                    "position": 1,
                    "title": "FastAPI",
                    "url": "https://fastapi.tiangolo.com/",
                    "snippet": "FastAPI documentation",
                }
            ],
        }


def override_search_service():
    return FakeSearchService()


app.dependency_overrides[get_search_service] = override_search_service

client = TestClient(app)


def test_search_endpoint():
    response = client.get("/search?q=fastapi")

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "fastapi"
    assert data["engine"] == "google"
    assert data["page"] == 1

    assert len(data["results"]) == 1

    result = data["results"][0]

    assert result["position"] == 1
    assert result["title"] == "FastAPI"
    assert result["url"] == "https://fastapi.tiangolo.com/"
    assert result["snippet"] == "FastAPI documentation"


def test_search_endpoint_rejects_empty_query():
    response = client.get("/search?q=")

    assert response.status_code == 422
