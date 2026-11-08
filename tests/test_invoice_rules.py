"""Tests for a 15-invoice synthetic batch: 10 clean, 5 exceptions."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from rules import CASES, evaluate

def test_fifteen_cases_and_unique_ids():
    assert len(CASES) == 15
    assert len({c["id"] for c in CASES}) == 15

def test_exactly_ten_pass_and_five_flagged():
    checks = [evaluate(c) for c in CASES]
    assert sum(not c["issues"] for c in checks) == 10
    assert sum(bool(c["issues"]) for c in checks) == 5

def test_all_four_exception_types_covered():
    flagged = {i["code"] for c in CASES for i in evaluate(c)["issues"]}
    assert flagged == {"PRICE_MISMATCH","QUANTITY_MISMATCH","MISSING_GR","MISSING_PO"}

def test_expected_flags_by_invoice():
    expected = {
        "INV-001": ["PRICE_MISMATCH"],
        "INV-002": ["QUANTITY_MISMATCH"],
        "INV-003": ["MISSING_GR"],
        "INV-004": ["MISSING_PO"],
        "INV-005": ["PRICE_MISMATCH"],
    }
    for c in CASES:
        actual = [i["code"] for i in evaluate(c)["issues"]]
        assert actual == expected.get(c["id"], []), c["id"]

def test_price_and_quantity_arithmetic():
    first = evaluate(CASES[0])
    assert "CHF +150.00" in first["issues"][0]["detail"]
    assert first["invoice_total"] == "1150"
    fifth = evaluate(CASES[4])
    assert "CHF +120.00" in fifth["issues"][0]["detail"]
    second = evaluate(CASES[1])
    assert "by 3 units" in second["issues"][0]["detail"]

def test_non_po_invoice_only_flags_missing_po():
    assert [i["code"] for i in evaluate(CASES[3])["issues"]] == ["MISSING_PO"]
