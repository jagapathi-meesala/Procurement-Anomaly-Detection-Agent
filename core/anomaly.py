"""Transparent, offline checks for user-supplied procurement records."""
from collections import Counter

def analyze_records(rows: list[dict], price_benchmarks: dict | None = None, high_price_ratio: float = 1.5) -> dict:
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    price_benchmarks = price_benchmarks or {}
    findings, normalized = [], []
    refs = Counter(str(r.get("invoice_ref", "")).strip() for r in rows if isinstance(r, dict) and str(r.get("invoice_ref", "")).strip())
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            findings.append({"record_index": i, "type": "malformed-record", "evidence": "Row is not an object."})
            continue
        normalized.append(row)
        missing = [k for k in ("supplier", "quantity", "unit_price") if row.get(k) in (None, "")]
        if missing:
            findings.append({"record_index": i, "type": "missing-fields", "evidence": ", ".join(missing)})
        ref = str(row.get("invoice_ref", "")).strip()
        if ref and refs[ref] > 1:
            findings.append({"record_index": i, "type": "duplicate-invoice-reference", "evidence": f"invoice_ref={ref!r} appears {refs[ref]} times"})
        category = str(row.get("category", "")).strip()
        try:
            price = float(row.get("unit_price"))
        except (TypeError, ValueError):
            price = None
        benchmark = price_benchmarks.get(category)
        try:
            benchmark = float(benchmark) if benchmark is not None else None
        except (TypeError, ValueError):
            benchmark = None
        if price is not None and benchmark is not None and benchmark > 0 and price > benchmark * high_price_ratio:
            findings.append({"record_index": i, "type": "unit-price-outlier",
                             "evidence": f"unit_price={price:g} exceeds supplied benchmark={benchmark:g} by ratio > {high_price_ratio:g}"})
    return {"record_count": len(rows), "findings": findings,
            "note": "Screening signals only; not proof of misconduct."}

def explain_flag(flag: dict) -> dict:
    if not isinstance(flag, dict):
        raise ValueError("flag must be an object")
    alternatives = {
        "duplicate-invoice-reference": ["legitimate correction or resubmission", "data import duplication"],
        "unit-price-outlier": ["different specification or quality", "tax, shipping, currency, or quantity differences", "stale or non-comparable benchmark"],
        "missing-fields": ["source export omitted fields", "record incomplete at time of extraction"],
        "malformed-record": ["format or data pipeline issue"],
    }
    kind = flag.get("type", "unknown")
    return {"flag": flag, "possible_explanations_to_check": alternatives.get(kind, ["Insufficient context to interpret."]),
            "next_step": "Verify source documents and applicable procurement policy before drawing conclusions."}
