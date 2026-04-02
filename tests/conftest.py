import json
import pytest
import requests

SNAPSHOT_PATH = "data/sample_responses.json"
API_URL = "https://api.fda.gov/drug/event.json?limit=5"


@pytest.fixture(scope="module")
def snapshot() -> dict:
    with open(SNAPSHOT_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def results(snapshot) -> list:
    return snapshot["results"]


@pytest.fixture(scope="module")
def live_response() -> requests.Response:
    response = requests.get(API_URL, timeout=10)
    return response
