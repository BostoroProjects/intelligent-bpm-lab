"""Deterministic synthetic invoice-exception cases."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from rules import CASES, evaluate

def test_four_case_types():
    assert [c["type"] for c in CASES] == [
        "Price mismatch", "Quantity mismatch", "Missing goods receipt", "Missing PO"
    ]

def test_expected_deterministic_issues():
    expected = ["PRICE_MISMATCH", "QUANTITY_MISMATCH", "MISSING_GR", "MISSING_PO"]
    for case, issue in zip(CASES, expected):
        result = evaluate(case)
        assert [i["code"] for i in result["issues"]] == [issue]
        assert result["status"] == "Requires human review"
        assert result["note"].startswith("Synthetic educational")

def test_price_difference():
    result = evaluate(CASES[0])
    assert "CHF +150.00" in result["issues"][0]["detail"]
    assert result["invoice_total"] == "1150"

def test_quantity_difference():
    result = evaluate(CASES[1])
    assert "by 3 units" in result["issues"][0]["detail"]

def test_missing_po_does_not_invent_receipt_requirement():
    result = evaluate(CASES[3])
    assert len(result["issues"]) == 1
    assert result["issues"][0]["code"] == "MISSING_PO"
