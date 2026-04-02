import pytest

# --- Status ---

def test_api_returns_200(live_response):
    assert live_response.status_code == 200


def test_response_is_json(live_response):
    assert live_response.headers["Content-Type"].startswith("application/json")


# --- Top-level structure matches snapshot ---

def test_live_has_same_top_level_keys(live_response, snapshot):
    live = live_response.json()
    for key in snapshot.keys():
        assert key in live, f"Key '{key}' present in snapshot but missing from live response"


def test_live_meta_has_same_keys(live_response, snapshot):
    live_meta = live_response.json()["meta"]
    snapshot_meta = snapshot["meta"]
    for key in snapshot_meta.keys():
        assert key in live_meta, f"meta key '{key}' missing from live response"


def test_live_results_is_nonempty_list(live_response):
    results = live_response.json()["results"]
    assert isinstance(results, list)
    assert len(results) > 0


# --- Report-level fields still exist ---

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

def test_safetyreportid_still_a_string(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["safetyreportid"], str)


def test_serious_still_a_string(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["serious"], str)


def test_patient_still_a_dict(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["patient"], dict)


def test_reaction_still_a_list(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["patient"]["reaction"], list)


def test_drug_still_a_list(live_response):
    for report in live_response.json()["results"]:
        assert isinstance(report["patient"]["drug"], list)
