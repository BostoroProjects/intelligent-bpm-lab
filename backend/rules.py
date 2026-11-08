"""Synthetic BYD case-study invoice exceptions and reproducible checks.

This is demonstrative data, not evidence of BYD internal practices.
"""
from decimal import Decimal
from typing import Any

CASES = [
    {"id":"INV-001","type":"Price mismatch","supplier":"Northstar Components","invoice":"SI-2401","po":"PO-451","invoice_qty":10,"invoice_unit_price":115,"po_qty":10,"po_unit_price":100,"received_qty":10,"currency":"CHF","notes":"Supplier claims a price increase; no approved amendment supplied."},
    {"id":"INV-002","type":"Quantity mismatch","supplier":"Atlas Industrial Parts","invoice":"SI-2402","po":"PO-452","invoice_qty":12,"invoice_unit_price":50,"po_qty":12,"po_unit_price":50,"received_qty":9,"currency":"CHF","notes":"Goods receipt reflects a partial delivery of nine units."},
    {"id":"INV-003","type":"Missing goods receipt","supplier":"Meridian Logistics","invoice":"SI-2403","po":"PO-453","invoice_qty":8,"invoice_unit_price":80,"po_qty":8,"po_unit_price":80,"received_qty":None,"currency":"CHF","notes":"Purchase order exists, but no goods receipt has been recorded."},
    {"id":"INV-004","type":"Missing PO","supplier":"Summit Facilities","invoice":"SI-2404","po":None,"invoice_qty":2,"invoice_unit_price":160,"po_qty":None,"po_unit_price":None,"received_qty":None,"currency":"CHF","notes":"Invoice refers to facilities work; no PO or confirmed cost-centre approval is supplied."},
    {"id":"INV-005","type":"Price mismatch","supplier":"Bluecrest Electronics","invoice":"SI-2405","po":"PO-455","invoice_qty":6,"invoice_unit_price":240,"po_qty":6,"po_unit_price":220,"received_qty":6,"currency":"CHF","notes":"Invoice includes a higher price; no signed price revision is attached."},
    {"id":"INV-006","type":"Standard invoice","supplier":"Ridgeway Metals","invoice":"SI-2406","po":"PO-456","invoice_qty":20,"invoice_unit_price":45,"po_qty":20,"po_unit_price":45,"received_qty":20,"currency":"CHF","notes":"Invoice, purchase order and receipt agree."},
    {"id":"INV-007","type":"Standard invoice","supplier":"Beacon Packaging","invoice":"SI-2407","po":"PO-457","invoice_qty":100,"invoice_unit_price":4.5,"po_qty":100,"po_unit_price":4.5,"received_qty":100,"currency":"CHF","notes":"All records are consistent."},
    {"id":"INV-008","type":"Standard invoice","supplier":"Horizon Fasteners","invoice":"SI-2408","po":"PO-458","invoice_qty":50,"invoice_unit_price":8,"po_qty":50,"po_unit_price":8,"received_qty":50,"currency":"CHF","notes":"Confirmed complete delivery at agreed price."},
    {"id":"INV-009","type":"Standard invoice","supplier":"Clearwater Plastics","invoice":"SI-2409","po":"PO-459","invoice_qty":30,"invoice_unit_price":27,"po_qty":30,"po_unit_price":27,"received_qty":30,"currency":"CHF","notes":"Invoice matches purchase order and goods receipt."},
    {"id":"INV-010","type":"Standard invoice","supplier":"Orion Industrial","invoice":"SI-2410","po":"PO-460","invoice_qty":15,"invoice_unit_price":125,"po_qty":15,"po_unit_price":125,"received_qty":15,"currency":"CHF","notes":"No discrepancies in supplied records."},
    {"id":"INV-011","type":"Standard invoice","supplier":"Silverline Components","invoice":"SI-2411","po":"PO-461","invoice_qty":40,"invoice_unit_price":18.75,"po_qty":40,"po_unit_price":18.75,"received_qty":40,"currency":"CHF","notes":"Complete receipt; contract unit price matches."},
    {"id":"INV-012","type":"Standard invoice","supplier":"Westbridge Tools","invoice":"SI-2412","po":"PO-462","invoice_qty":12,"invoice_unit_price":75,"po_qty":12,"po_unit_price":75,"received_qty":12,"currency":"CHF","notes":"Invoice is supported by matching PO and receipt."},
    {"id":"INV-013","type":"Standard invoice","supplier":"Helix Manufacturing","invoice":"SI-2413","po":"PO-463","invoice_qty":25,"invoice_unit_price":36,"po_qty":25,"po_unit_price":36,"received_qty":25,"currency":"CHF","notes":"Full quantity received at agreed price."},
    {"id":"INV-014","type":"Standard invoice","supplier":"Nova Machine Parts","invoice":"SI-2414","po":"PO-464","invoice_qty":7,"invoice_unit_price":310,"po_qty":7,"po_unit_price":310,"received_qty":7,"currency":"CHF","notes":"Purchase order, goods receipt and invoice all match."},
    {"id":"INV-015","type":"Standard invoice","supplier":"Harbor Supply","invoice":"SI-2415","po":"PO-465","invoice_qty":60,"invoice_unit_price":12.5,"po_qty":60,"po_unit_price":12.5,"received_qty":60,"currency":"CHF","notes":"No price or quantity deviation."}
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
