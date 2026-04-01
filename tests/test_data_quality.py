import json
import pytest

SNAPSHOT_PATH = "data/sample_responses.json"

@pytest.fixture(scope="module")
def snapshot() -> dict:
    with open(SNAPSHOT_PATH) as f:
        return json.load(f)

@pytest.fixture(scope="module")
def result(snapshot) -> dict:
    return snapshot["results"]

# --- Data Accuracy ---
def test_serious(result):
    for report in result:
        assert report["serious"] in ("1", "2")

def test_


   
