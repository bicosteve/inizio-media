from models.search import SearchResult


def extract_organic_results(data: dict) -> list[SearchResult]:

    organic_results = data.get("organic_results", [])

    results: list[SearchResult] = []

    for position, result in enumerate(organic_results, start=1):
        if (
            not isinstance(result, dict)
            or not result.get("title")
            or not result.get("link")
            or not result.get("snippet")
        ):
            continue

        search_result = SearchResult(
            position=position,
            title=result["title"],
            url=result["link"],
            snippet=result["snippet"],
        )

        results.append(search_result)

    return results
