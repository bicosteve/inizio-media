from typing import Literal

from pydantic import BaseModel, HttpUrl


class SearchResult(BaseModel):
    position: str
    title: str
    url: HttpUrl
    snippet: str | None


class SearchResponse(BaseModel):
    query: str
    engine: str
    page: Literal[1]
    results: list[SearchResult]
