from typing import Literal

from pydantic import BaseModel


class SearchResult(BaseModel):
    position: int
    title: str
    url: str
    snippet: str | None


class SearchResponse(BaseModel):
    query: str
    engine: str
    page: Literal[1]
    results: list[SearchResult]
