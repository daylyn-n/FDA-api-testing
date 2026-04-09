"""
Purpose: Check if the JSON we got from the snapshot has the right "shape"

"""

import pytest

# --- Top-level structure ---

"""Checks if the top keys of the schema are correct

Args:
    snapshop: dict of the sample JSON data


Returns:
    Tests pass if the root object has "meta" and "results" keys
"""
def test_top_level_keys(snapshot):
    assert "meta" in snapshot
    assert "results" in snapshot

"""Checks if snapshot["results"] is a non-empty list

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Tests pass if results is of type list, and len of results is > 0
"""
def test_results_is_nonempty_list(results):
    assert isinstance(results, list)
    assert len(results) > 0


# --- Meta ---

"""Checks if meta contains the correct values

Args:
    takes in the json sample data

Returns:
    Tests pass after looping through meta to find if the correct keywords exist
"""
def test_meta_required_fields(snapshot):
    meta = snapshot["meta"]
    for field in ("disclaimer", "terms", "license", "last_updated", "results"):
        assert field in meta, f"meta missing field: {field}"

"""Checks if meta.results has the required methods for how the FDA API breaks up the dataset
Note:
    "skip" = offset of where the sample data is started in their database
    "limit" = maximum number of results returned in the API request
    "total" = actual number of records in the FDA database

Args:
    takes in the json sample data

Returns:
    Tests pass if the required values exist, and they are of type int

"""
def test_meta_results_pagination(snapshot):
    pagination = snapshot["meta"]["results"]
    for field in ("skip", "limit", "total"):
        assert field in pagination
        assert isinstance(pagination[field], int)


# --- Report-level fields ---

"""Check if every report has a "safetyreportid" and is of type string

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test pass if each report has the "safetyreportid" and is of type string
"""
def test_each_report_has_safetyreportid(results):
    for report in results:
        assert "safetyreportid" in report
        assert isinstance(report["safetyreportid"], str)

"""Check if every report has a "serious" key

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test pass if each report has the "serious" key
"""
def test_each_report_has_serious(results):
    for report in results:
        assert "serious" in report

"""Check if every report has a "patient" key and is of type dict

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test pass if each report has the "patient" key and is of type dict 
"""
def test_each_report_has_patient(results):
    for report in results:
        assert "patient" in report
        assert isinstance(report["patient"], dict)


# --- Patient ---
"""Check if every "patient" in every report has a "reaction" key and is of type list

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test pass if each "patient" in every report has a "reaction" key and is of type lits
"""
def test_patient_has_reactions(results):
    for report in results:
        patient = report["patient"]
        assert "reaction" in patient
        assert isinstance(patient["reaction"], list)
        assert len(patient["reaction"]) > 0

"""Check if every report["patient"]["reaction"] has a "meddrapt" key and is of type str

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test pass if each report["patient"]["reaction"] has a "meddrapt" key and is of type str
"""

def test_each_reaction_has_meddrapt(results):
    for report in results:
        for reaction in report["patient"]["reaction"]:
            assert "reactionmeddrapt" in reaction
            assert isinstance(reaction["reactionmeddrapt"], str)

"""Check if every "patient" in every report has a "drug" key and is of type list

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test pass if each "patient" in every report has a "drug" key and is of type lits
    And if patient["drug"] is non-empty
"""
def test_patient_has_drugs(results):
    for report in results:
        patient = report["patient"]
        assert "drug" in patient
        assert isinstance(patient["drug"], list)
        assert len(patient["drug"]) > 0

"""Check if every report["patient"]["drug"] has a "medicinalproduct" key and is of type str

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test pass if every report["patient"]["drug"] has a "medicinalproduct" key and is of type str
"""
def test_each_drug_has_medicinalproduct(results):
    for report in results:
        for drug in report["patient"]["drug"]:
            assert "medicinalproduct" in drug
            assert isinstance(drug["medicinalproduct"], str)
