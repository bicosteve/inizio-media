from models.schemas import SearchResult


def extract_organic_results(data: dict) -> list[SearchResult]:
    """
    Extract and normalize organic Google search results.

    It deliberately read only the `organic_results` section of the provider response. Ads, knowledge panels, peopel also ask, and other modules are not included.
    """

    organic_result = data.get("organic_results", [])

    results: list[SearchResult] = []

    for position, result in enumerate(organic_result, start=1):
        search_result = SearchResult(
            position=position,
            title=result["title"],
            url=result["link"],
            snippet=result.get("snippet"),
        )

        results.append(search_result)

    return results
