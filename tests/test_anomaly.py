import pytest
from core.anomaly import analyze_records, explain_flag

def test_non_list_rejected():
    with pytest.raises(ValueError): analyze_records("bad")
def test_missing_fields_flagged():
    assert any(f["type"] == "missing-fields" for f in analyze_records([{"supplier":"A"}])["findings"])
def test_duplicate_reference_flagged():
    rows = [{"supplier":"A","quantity":1,"unit_price":2,"invoice_ref":"I1"},
            {"supplier":"B","quantity":1,"unit_price":2,"invoice_ref":"I1"}]
    assert sum(f["type"] == "duplicate-invoice-reference" for f in analyze_records(rows)["findings"]) == 2
def test_price_outlier_uses_supplied_benchmark():
    rows = [{"supplier":"A","category":"laptop","quantity":1,"unit_price":2000}]
    assert any(f["type"] == "unit-price-outlier" for f in analyze_records(rows, {"laptop":1000})["findings"])
def test_no_external_benchmark_assumed():
    rows = [{"supplier":"A","category":"x","quantity":1,"unit_price":9999}]
    assert not any(f["type"] == "unit-price-outlier" for f in analyze_records(rows)["findings"])
def test_malformed_record_flagged():
    assert analyze_records([None])["findings"][0]["type"] == "malformed-record"
def test_explain_flag_lists_alternatives():
    r = explain_flag({"type":"duplicate-invoice-reference"})
    assert r["possible_explanations_to_check"]
def test_explanation_requires_review():
    assert "Verify source documents" in explain_flag({"type":"unknown"})["next_step"]
