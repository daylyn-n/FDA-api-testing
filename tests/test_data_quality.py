"""Purpose: Test for mainly code quality, so if the data in snapshot["record"] is correct,
and checking for type correctness

"""

import pytest

# --- Data Accuracy ---

"""Check if the if ther serious level is accurate

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if report["serious"] is either "1" or "2"
"""
def test_serious(results):
    for report in results:
        assert report["serious"] in ("1", "2")

"""Check if the if ther patient sex is accurate

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if patient["patientsex"] in report["patient"] is either "0", "1" or "2"
"""
def test_patientsex_valid_code(results):
    for report in results:
        patient = report["patient"]
        if "patientsex" in patient:
            assert patient["patientsex"] in ("0", "1", "2"), \
                f"Invalid patientsex in report {report['safetyreportid']}"


"""Check if the patient onset age is numeric

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if patient["patientonsetage"] contains only digits
"""
def test_patientonsetage_is_numeric(results):
    for report in results:
        patient = report["patient"]
        if "patientonsetage" in patient:
            assert patient["patientonsetage"].isdigit(), \
                f"patientonsetage is not numeric in report {report['safetyreportid']}"

"""Check if the patient onset age is in a realistic range

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if patient["patientonsetage"] is between 0 and 130 when the age unit is "801" (years)
"""
def test_patientonsetage_in_realistic_range(results):
    for report in results:
        patient = report["patient"]
        if "patientonsetage" in patient and "patientonsetageunit" in patient:
            if patient["patientonsetageunit"] == "801":  # 801 = years
                age = int(patient["patientonsetage"])
                assert 0 <= age <= 130, \
                    f"Unrealistic age {age} in report {report['safetyreportid']}"

"""Check if the receive date is not after the transmission date

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if report["receivedate"] is before or equal to report["transmissiondate"]
"""
def test_receivedate_not_after_transmissiondate(results):
    for report in results:
        if "receivedate" in report and "transmissiondate" in report:
            assert report["receivedate"] <= report["transmissiondate"], \
                f"receivedate is after transmissiondate in report {report['safetyreportid']}"

"""Check if the date fields are in valid YYYYMMDD format

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if receivedate, receiptdate, and transmissiondate are 8-digit strings
"""
def test_dates_are_valid_format(results):
    for report in results:
        for date_field in ("receivedate", "receiptdate", "transmissiondate"):
            if date_field in report:
                value = report[date_field]
                assert len(value) == 8 and value.isdigit(), \
                    f"{date_field} '{value}' is not YYYYMMDD in report {report['safetyreportid']}"

"""Check if seriousness death implies serious

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if report["seriousnessdeath"] is "1" then report["serious"] is also "1"
"""
def test_seriousnessdeath_implies_serious(results):
    for report in results:
        if report.get("seriousnessdeath") == "1":
            assert report.get("serious") == "1", \
                f"seriousnessdeath is 1 but serious is not 1 in report {report['safetyreportid']}"

"""Check if duplicate flag has a reportduplicate object

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if report["duplicate"] is "1" then "reportduplicate" exists in the report
"""
def test_duplicate_flag_has_reportduplicate(results):
    for report in results:
        if report.get("duplicate") == "1":
            assert "reportduplicate" in report, \
                f"duplicate=1 but no reportduplicate object in report {report['safetyreportid']}"

"""Check if the reaction meddra preferred term is a nonempty string

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if reaction["reactionmeddrapt"] is not empty or whitespace
"""
def test_reaction_meddrapt_is_nonempty_string(results):
    for report in results:
        for reaction in report["patient"]["reaction"]:
            assert reaction["reactionmeddrapt"].strip() != "", \
                f"Empty reactionmeddrapt in report {report['safetyreportid']}"

"""Check if the drug medicinal product is a nonempty string

Args:
    results = snapshot["results"]: list[dict[str, Any]]

Returns:
    Test return positive if drug["medicinalproduct"] is not empty or whitespace
"""
def test_drug_medicinalproduct_is_nonempty_string(results):
    for report in results:
        for drug in report["patient"]["drug"]:
            assert drug["medicinalproduct"].strip() != "", \
                f"Empty medicinalproduct in report {report['safetyreportid']}"


   
