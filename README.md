# Procurement Anomaly Detection Agent

An offline, advisory agent that flags unusual patterns in procurement data supplied by the user. It does not connect to procurement systems or determine fraud.

## Capabilities
- Validate common procurement fields and flag missing values.
- Identify duplicate-looking invoice/order references.
- Flag unusually high unit prices relative to supplied comparison values.
- Highlight split-looking purchases near a supplied approval threshold.
- Produce explainable findings with evidence and follow-up questions.

## Quick start
Python 3.10+:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python3 verification/readiness_audit.py
```

## Suggested fields
Record ID, supplier, date, item/category, quantity, unit price, total, invoice or PO reference, currency, and approval threshold where applicable. Remove unnecessary personal information before analysis.

## Limitations
Flags are screening signals, not proof of fraud, collusion, or policy violations. Data quality, seasonality, currency, taxes, shipping, contract terms, and category differences can explain unusual values. Review evidence and apply consistent procedures before taking action.
