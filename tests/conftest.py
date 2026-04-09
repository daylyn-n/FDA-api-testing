"""
Purpose: Create pytest fixtures to reuse throughout all the
test_*.py files. 

Load the snapshot data to test on
Extract the ["results"] to test on the quality of data
Extract the actual API to test if the sample quality is the same
as the live API

snapshot: dict[str, Any]
snapshot["results"]: list[dict[str, Any]]
"""

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
