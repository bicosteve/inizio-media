import serpapi


class SearchProvider:
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
