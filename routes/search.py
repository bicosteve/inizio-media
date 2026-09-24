import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.search import SearchResponse
from providers.google_provider import SearchProvider
from repository.search_history import SearchHistoryRepository
from services.search_service import SearchService

load_dotenv()
templates = Jinja2Templates(directory="templates")
router = APIRouter()


def get_search_service() -> SearchService:

    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        raise RuntimeError("SERPAPI_KEY not set")

    provider = SearchProvider(api_key=api_key)
    history_repository = SearchHistoryRepository(file_path="data/searches.json")
    return SearchService(
        provider=provider,
        history_repository=history_repository,
    )


# ---- HTML Search Pages ----
@router.get("/", include_in_schema=False, response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "query": "",
            "response": None,
        },
    )


# ---- HTML: Perform search and render results ----
@router.get(
    "/search",
    include_in_schema=False,
    response_class=HTMLResponse,
    name="search_page",
)
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


# --- HTML : History Page
@router.get("/history/", response_class=HTMLResponse, include_in_schema=False)
def history_page(
    request: Request,
    service: SearchService = Depends(get_search_service),
):
    history = service.get_history()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "history": history,
        },
    )


# --- API: JSON Search ----
@router.get("/api/search", response_model=SearchResponse)
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


# --- API : Json History ---
@router.get("/api/history")
def search_history(service: SearchService = Depends(get_search_service)):
    return service.get_history()
