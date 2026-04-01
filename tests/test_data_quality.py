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


def test_patientsex_valid_code(result):
    for report in result:
        patient = report["patient"]
        if "patientsex" in patient:
            assert patient["patientsex"] in ("0", "1", "2"), \
                f"Invalid patientsex in report {report['safetyreportid']}"

def test_patientonsetage_is_numeric(result):
    for report in result:
        patient = report["patient"]
        if "patientonsetage" in patient:
            assert patient["patientonsetage"].isdigit(), \
                f"patientonsetage is not numeric in report {report['safetyreportid']}"

def test_patientonsetage_in_realistic_range(result):
    for report in result:
        patient = report["patient"]
        if "patientonsetage" in patient and "patientonsetageunit" in patient:
            if patient["patientonsetageunit"] == "801":  # 801 = years
                age = int(patient["patientonsetage"])
                assert 0 <= age <= 130, \
                    f"Unrealistic age {age} in report {report['safetyreportid']}"

def test_receivedate_not_after_transmissiondate(result):
    for report in result:
        if "receivedate" in report and "transmissiondate" in report:
            assert report["receivedate"] <= report["transmissiondate"], \
                f"receivedate is after transmissiondate in report {report['safetyreportid']}"

def test_dates_are_valid_format(result):
    for report in result:
        for date_field in ("receivedate", "receiptdate", "transmissiondate"):
            if date_field in report:
                value = report[date_field]
                assert len(value) == 8 and value.isdigit(), \
                    f"{date_field} '{value}' is not YYYYMMDD in report {report['safetyreportid']}"

def test_seriousnessdeath_implies_serious(result):
    for report in result:
        if report.get("seriousnessdeath") == "1":
            assert report.get("serious") == "1", \
                f"seriousnessdeath is 1 but serious is not 1 in report {report['safetyreportid']}"

def test_duplicate_flag_has_reportduplicate(result):
    for report in result:
        if report.get("duplicate") == "1":
            assert "reportduplicate" in report, \
                f"duplicate=1 but no reportduplicate object in report {report['safetyreportid']}"

def test_reaction_meddrapt_is_nonempty_string(result):
    for report in result:
        for reaction in report["patient"]["reaction"]:
            assert reaction["reactionmeddrapt"].strip() != "", \
                f"Empty reactionmeddrapt in report {report['safetyreportid']}"

def test_drug_medicinalproduct_is_nonempty_string(result):
    for report in result:
        for drug in report["patient"]["drug"]:
            assert drug["medicinalproduct"].strip() != "", \
                f"Empty medicinalproduct in report {report['safetyreportid']}"


   
