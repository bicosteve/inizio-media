from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from models.search import SearchResponse
from providers.google_provider import GoogleSearchProvider
from services.search_service import SearchService

router = APIRouter()

FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "google_serp.json"
)


provider = GoogleSearchProvider(fixture_path=FIXTURE_PATH)
search_service = SearchService(provider=provider)


@router.get("/search", response_model=SearchResponse)
def search(q: str = Query(..., min_length=1)) -> SearchResponse:
    query = q.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Search query is required")

    return search_service.search(query)
