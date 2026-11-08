"""Synthetic BYD case-study invoice exceptions and reproducible checks.

This is demonstrative data, not evidence of BYD internal practices.
"""
from decimal import Decimal
from typing import Any

CASES = [
    {"id":"INV-001","type":"Price mismatch","supplier":"Northstar Components","invoice":"SI-2401","po":"PO-451","invoice_qty":10,"invoice_unit_price":115,"po_qty":10,"po_unit_price":100,"received_qty":10,"currency":"CHF","notes":"Supplier claims a price increase; no approved amendment supplied."},
    {"id":"INV-002","type":"Quantity mismatch","supplier":"Atlas Industrial Parts","invoice":"SI-2402","po":"PO-452","invoice_qty":12,"invoice_unit_price":50,"po_qty":12,"po_unit_price":50,"received_qty":9,"currency":"CHF","notes":"Goods receipt reflects a partial delivery of nine units."},
    {"id":"INV-003","type":"Missing goods receipt","supplier":"Meridian Logistics","invoice":"SI-2403","po":"PO-453","invoice_qty":8,"invoice_unit_price":80,"po_qty":8,"po_unit_price":80,"received_qty":None,"currency":"CHF","notes":"Purchase order exists, but no goods receipt has been recorded."},
    {"id":"INV-004","type":"Missing PO","supplier":"Summit Facilities","invoice":"SI-2404","po":None,"invoice_qty":2,"invoice_unit_price":160,"po_qty":None,"po_unit_price":None,"received_qty":None,"currency":"CHF","notes":"Invoice refers to facilities work; no PO or confirmed cost-centre approval is supplied."}
]

def money(value: Any) -> Decimal:
    return Decimal(str(value))

def evaluate(case: dict) -> dict:
    """No LLM is involved in classification or arithmetic."""
    evidence = [
        f"Invoice {case['invoice']}: {case['invoice_qty']} × {case['currency']} {money(case['invoice_unit_price']):.2f}",
        f"Purchase order: {case['po'] or 'not supplied'}",
        "Goods receipt: " + (str(case['received_qty']) + " units" if case['received_qty'] is not None else "not supplied"),
        "Context: " + case["notes"]
    ]
    issues = []
    if not case["po"]:
        issues.append({"code":"MISSING_PO","detail":"No purchase order reference supplied.","action":"Request a verified PO reference or route for approved non-PO handling."})
    else:
        if case["po_unit_price"] is not None and money(case["invoice_unit_price"]) != money(case["po_unit_price"]):
            delta = (money(case["invoice_unit_price"]) - money(case["po_unit_price"])) * money(case["invoice_qty"])
            issues.append({"code":"PRICE_MISMATCH","detail":f"Unit price {case['currency']} {money(case['invoice_unit_price']):.2f} vs PO {case['currency']} {money(case['po_unit_price']):.2f}; invoice-line difference {case['currency']} {delta:+.2f}.","action":"Request Procurement confirmation and approved price amendment."})
        if case["received_qty"] is None:
            issues.append({"code":"MISSING_GR","detail":"No goods receipt evidence supplied.","action":"Ask Goods Receiving to confirm receipt or provide the missing record."})
        elif money(case["received_qty"]) < money(case["invoice_qty"]):
            issues.append({"code":"QUANTITY_MISMATCH","detail":f"Invoice quantity {case['invoice_qty']} exceeds received quantity {case['received_qty']} by {money(case['invoice_qty'])-money(case['received_qty'])} units.","action":"Ask Goods Receiving to verify the missing quantity or partial delivery."})
    return {
        "case_id":case["id"],"classification":case["type"],
        "invoice_total":str(money(case["invoice_qty"])*money(case["invoice_unit_price"])),
        "currency":case["currency"],"evidence":evidence,"issues":issues,
        "status":"Requires human review" if issues else "No rule exception found",
        "rule_version":"1.0",
        "note":"Synthetic educational case; checks are illustrative, not BYD policy."
    }
