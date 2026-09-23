from providers.google_provider import SearchProvider


def test_provider_search(mocker):
    mock_response = {
        "organic_results": [
            {
                "title": "FastAPI",
                "link": "https://fastapi.tiangolo.com/",
                "snippet": "FastAPI documentation",
            }
        ]
    }

    mock_client = mocker.Mock()
    mock_client.search.return_value = mock_response

    provider = SearchProvider(api_key="fake-api-key")
    provider.client = mock_client

    result = provider.search("fastapi")

    assert result == {
        "organic_results": [
            {
                "title": "FastAPI",
                "link": "https://fastapi.tiangolo.com/",
                "snippet": "FastAPI documentation",
            }
        ]
    }

    mock_client.search.assert_called_once_with(
        {
            "engine": "google",
            "q": "fastapi",
            "num": 10,
        }
    )
