from models.search import SearchResponse
from parsers.organic_parser import extract_organic_results


class SearchService:
    """
    This layer coordinates:
    provider -> raw dict -> parser -> SearchResult[] -> SearchResponse
    """

    def __init__(self, provider):
        self.provider = provider

    def search(self, query: str) -> SearchResponse:
        provider_response = self.provider.search(query)

        results = extract_organic_results(provider_response)

        return SearchResponse(
            query=query,
            engine="google",
            page=1,
            results=results,
        )
