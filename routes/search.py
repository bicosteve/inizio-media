import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates

from models.search import SearchResponse
from providers.google_provider import SearchProvider
from services.search_service import SearchService

load_dotenv()
templates = Jinja2Templates(directory="templates")
router = APIRouter()


def get_search_service() -> SearchService:

    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        raise RuntimeError("SERPAPI_KEY not set")

    provider = SearchProvider(api_key=api_key)
    return SearchService(provider=provider)


@router.get("/")
def search_page(
    request: Request,
    q: str = Query(default=""),
    service: SearchService = Depends(get_search_service),
):
    query = q.strip()

    if not query:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "query": "",
                "response": None,
            },
        )

    response = service.search(query)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "query": query,
            "response": response,
        },
    )


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
