import json
from pathlib import Path

from parsers.organic_parser import extract_organic_results

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "google_serp.json"


def load_fixture() -> dict:
    with FIXTURE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_extract_organic_results():
    data = load_fixture()

    results = extract_organic_results(data)

    assert len(results) == 3

    assert results[0].position == 1
    assert results[0].title == "FastAPI"
    assert results[0].url == "https://fastapi.tiangolo.com/"
    assert results[0].snippet == (
        "FastAPI framework, high performance, easy to learn, fast to code."
    )


def test_only_organic_results_are_extracted():
    data = load_fixture()

    results = extract_organic_results(data)

    titles = [result.title for result in results]

    assert "Some Sponsored Result " not in titles
    assert "FastAPI" in titles
    assert "FastAPI - Wikipedia" in titles
    assert "Python" in titles


def test_positions_are_sequential():
    data = load_fixture()

    results = extract_organic_results(data)

    positions = [result.position for result in results]

    assert positions == [1, 2, 3]


def test_result_fields_have_correct_types():
    data = load_fixture()

    results = extract_organic_results(data)

    for result in results:
        assert isinstance(result.position, int)
        assert isinstance(result.title, str)
        assert isinstance(str(result.url), str)
        assert result.snippet is None or isinstance(result.snippet, str)
