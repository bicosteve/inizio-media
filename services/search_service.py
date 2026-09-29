import logging

from models.search import SearchResponse
from parsers.organic_parser import extract_organic_results
from providers.google_provider import SearchProvider
from repository.search_history import SearchHistoryRepository

logger = logging.getLogger(__name__)


class SearchService:
    """
    SearchService is a cordinator for the operation.

    Receives:
    - search request,
    - ask the provider for results
    - parse/process the results
    - store the search in json via repository
    - return the results to the application mode.

    :: provider -> raw dict -> parser -> SearchResult[] -> SearchResponse

    """

    def __init__(
        self,
        provider: SearchProvider,
        history_repository: SearchHistoryRepository,
    ):
        self.provider = provider
        self.history_repository = history_repository

    def search(self, query: str) -> SearchResponse:
        raw_results = self.provider.search(query)

        results = extract_organic_results(raw_results)

        response = SearchResponse(
            query=query,
            engine="google",
            page=1,
            results=results,
        )

        try:
            self.history_repository.save(response)
        except Exception:
            logger.exception("Failed to store search history for %s", query)

        return response

    def get_history(self) -> list[dict]:
        try:
            return self.history_repository.get_all()
        except Exception:
            logger.exception("Failed to fetch search history")
            return []
