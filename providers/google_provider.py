import serpapi


class SearchProvider:
    """
    - This pattern is good for abstraction and dependency isolation.
    - My service need not know the details of the SearchProvider.
    - We can introduce another provider in this package without changing the service that much.
    - It is also useful for testing since we will not be calling the serpapi directly but we can mock it meaning it will be independent of network calls.
    """

    def __init__(self, api_key: str):
        self.client = serpapi.Client(api_key=api_key, timeout=10)

    def search(self, query: str) -> dict:
        results = self.client.search(
            {
                "engine": "google",
                "q": query,
                "num": 10,
            },
        )

        return dict(results)
