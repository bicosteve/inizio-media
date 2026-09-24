from models.search import SearchResponse
from parsers.organic_parser import extract_organic_results
from repository.search_history import SearchHistoryRepository


class SearchService:
    """
    This layer coordinates:
    provider -> raw dict -> parser -> SearchResult[] -> SearchResponse
    """

    def __init__(self, provider, history_repository: SearchHistoryRepository):
        self.provider = provider
        self.history_repository = history_repository

    def search(self, query: str) -> SearchResponse:
        raw_results = self.provider.search(query)

        # provider_response = self.provider.search(query)

        results = extract_organic_results(raw_results)

        response = SearchResponse(
            query=query,
            engine="google",
            page=1,
            results=results,
        )

        self.history_repository.save(response)

        return response

    def get_history(self) -> list[dict]:
        return self.history_repository.get_all()
