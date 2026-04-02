import pytest

# --- Top-level structure ---

def test_top_level_keys(snapshot):
    assert "meta" in snapshot
    assert "results" in snapshot


def test_results_is_nonempty_list(results):
    assert isinstance(results, list)
    assert len(results) > 0


# --- Meta ---

def test_meta_required_fields(snapshot):
    meta = snapshot["meta"]
    for field in ("disclaimer", "terms", "license", "last_updated", "results"):
        assert field in meta, f"meta missing field: {field}"


def test_meta_results_pagination(snapshot):
    pagination = snapshot["meta"]["results"]
    for field in ("skip", "limit", "total"):
        assert field in pagination
        assert isinstance(pagination[field], int)


# --- Report-level fields ---

def test_each_report_has_safetyreportid(results):
    for report in results:
        assert "safetyreportid" in report
        assert isinstance(report["safetyreportid"], str)


def test_each_report_has_serious(results):
    for report in results:
        assert "serious" in report


def test_each_report_has_patient(results):
    for report in results:
        assert "patient" in report
        assert isinstance(report["patient"], dict)


# --- Patient ---

def test_patient_has_reactions(results):
    for report in results:
        patient = report["patient"]
        assert "reaction" in patient
        assert isinstance(patient["reaction"], list)
        assert len(patient["reaction"]) > 0


def test_each_reaction_has_meddrapt(results):
    for report in results:
        for reaction in report["patient"]["reaction"]:
            assert "reactionmeddrapt" in reaction
            assert isinstance(reaction["reactionmeddrapt"], str)


def test_patient_has_drugs(results):
    for report in results:
        patient = report["patient"]
        assert "drug" in patient
        assert isinstance(patient["drug"], list)
        assert len(patient["drug"]) > 0


def test_each_drug_has_medicinalproduct(results):
    for report in results:
        for drug in report["patient"]["drug"]:
            assert "medicinalproduct" in drug
            assert isinstance(drug["medicinalproduct"], str)
