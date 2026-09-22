import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query

from models.search import SearchResponse
from providers.google_provider import SearchProvider
from services.search_service import SearchService

load_dotenv()
router = APIRouter()


def get_search_service() -> SearchService:

    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        raise RuntimeError("SERPAPI_KEY not set")

    provider = SearchProvider(api_key=api_key)
    return SearchService(provider=provider)


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1),
    service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    query = q.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Search query is required",
        )

    return service.search(query)
