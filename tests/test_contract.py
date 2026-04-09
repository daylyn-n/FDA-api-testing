"""Purpose: Test that the live API response still matches the structure of the saved snapshot,
catching any breaking changes or regressions in the API contract

"""

import pytest

# --- Status ---

"""Check if the live API returns a 200 status code

Args:
    live_response: requests.Response from the live FDA API

Returns:
    Test return positive if live_response.status_code is 200
"""
def test_api_returns_200(live_response):
    assert live_response.status_code == 200


"""Check if the live API response is JSON

Args:
    live_response: requests.Response from the live FDA API

Returns:
    Test return positive if Content-Type header starts with "application/json"
"""
def test_response_is_json(live_response):
    assert live_response.headers["Content-Type"].startswith("application/json")


# --- Top-level structure matches snapshot ---

"""Check if the live response has the same top-level keys as the snapshot

Args:
    live_response: requests.Response from the live FDA API
    snapshot = data/sample_responses.json: dict[str, Any]

Returns:
    Test return positive if every key in the snapshot is also present in the live response
"""
def test_live_has_same_top_level_keys(live_response, snapshot):
    live = live_response.json()
    for key in snapshot.keys():
        assert key in live, f"Key '{key}' present in snapshot but missing from live response"


"""Check if the live response meta has the same keys as the snapshot meta

Args:
    live_response: requests.Response from the live FDA API
    snapshot = data/sample_responses.json: dict[str, Any]

Returns:
    Test return positive if every key in snapshot["meta"] is also present in live response["meta"]
"""
def test_live_meta_has_same_keys(live_response, snapshot):
    live_meta = live_response.json()["meta"]
    snapshot_meta = snapshot["meta"]
    for key in snapshot_meta.keys():
        assert key in live_meta, f"meta key '{key}' missing from live response"


"""Check if the live response results is a nonempty list

Args:
    live_response: requests.Response from the live FDA API

Returns:
    Test return positive if live response["results"] is a list with at least one item
"""
def test_live_results_is_nonempty_list(live_response):
    results = live_response.json()["results"]
    assert isinstance(results, list)
    assert len(results) > 0


# --- Report-level fields still exist ---

"""Check if every field seen in snapshot reports exists in at least one live report

Args:
    live_response: requests.Response from the live FDA API
    snapshot = data/sample_responses.json: dict[str, Any]

Returns:
    Test return positive if every field found across snapshot["results"] appears in at least one live report
"""
def test_live_reports_have_same_fields_as_snapshot(live_response, snapshot):
    snapshot_fields = set()
    for report in snapshot["results"]:
        snapshot_fields.update(report.keys())

    for report in live_response.json()["results"]:
        for field in snapshot_fields:
            if field in report:
                break
        # at least one live report should contain each field seen in the snapshot
    for field in snapshot_fields:
        found = any(field in report for report in live_response.json()["results"])
        assert found, f"Field '{field}' seen in snapshot but not found in any live report"


# --- Field types haven't changed ---

"""Check if safetyreportid is still a string in the live response

Args:
    live_response: requests.Response from the live FDA API

Returns:
    Test return positive if report["safetyreportid"] is a string for every live report
"""
def test_safetyreportid_still_a_string(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["safetyreportid"], str)


"""Check if serious is still a string in the live response

Args:
    live_response: requests.Response from the live FDA API

Returns:
    Test return positive if report["serious"] is a string for every live report
"""
def test_serious_still_a_string(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["serious"], str)


"""Check if patient is still a dict in the live response

Args:
    live_response: requests.Response from the live FDA API

Returns:
    Test return positive if report["patient"] is a dict for every live report
"""
def test_patient_still_a_dict(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["patient"], dict)


"""Check if reaction is still a list in the live response

Args:
    live_response: requests.Response from the live FDA API

Returns:
    Test return positive if report["patient"]["reaction"] is a list for every live report
"""
def test_reaction_still_a_list(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["patient"]["reaction"], list)


"""Check if drug is still a list in the live response

Args:
    live_response: requests.Response from the live FDA API

Returns:
    Test return positive if report["patient"]["drug"] is a list for every live report
"""
def test_drug_still_a_list(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["patient"]["drug"], list)
