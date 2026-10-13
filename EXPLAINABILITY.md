# Explainability

This document explains the agent's inputs, decision process, outputs, and limitations.

## Inputs
The agent accepts user-supplied procurement records with fields such as record ID, supplier, date, item, quantity, unit price, total, invoice or purchase-order reference, currency, and optional approval thresholds or comparison prices. Missing data is reported, not invented.

## Decision
The agent uses transparent, simple checks to flag duplicate-looking references, unusually high prices compared with a supplied benchmark, and purchases that may be split near a supplied approval threshold. It records the triggering fields and treats each result as a screening signal.

## Limits
The agent does not connect to procurement systems, independently verify prices or suppliers, or establish intent. Currency, taxes, shipping, contracts, seasonality, category mix, and data-entry errors may explain anomalies. A flag is not proof of fraud or misconduct.

## Tool: analyze-procurement-records

### Inputs and Data Sources
Receives a list of procurement records supplied by the user and optional comparison benchmarks.

### Decision and Reasoning
Checks record completeness, duplicate-like invoice references, and unit-price outliers only where comparable values are available.

### Outputs and Evidence
Returns flags that identify record indices, triggering fields, and the comparison or rule used.

### Limits and Constraints
It cannot confirm that a transaction is improper or compare prices against external market data.

### Failure Handling
Malformed rows and missing values are reported. The tool does not silently fill missing values.

### Human Review
An authorized reviewer validates the source documents and obtains context before action.

## Tool: explain-anomaly-flags

### Inputs and Data Sources
Receives flagged records and the rules or benchmarks used to flag them.

### Decision and Reasoning
Explains which supplied fields triggered each flag and lists plausible non-misconduct explanations to check.

### Outputs and Evidence
Produces a neutral explanation and evidence checklist.

### Limits and Constraints
The explanation is limited to supplied records and cannot infer intent or collusion.

### Failure Handling
If evidence or benchmark context is missing, the finding is marked inconclusive.

### Human Review
Reviewers confirm the flag against invoices, contracts, delivery records, and approval policies.

## Tool: generate-audit-summary

### Inputs and Data Sources
Receives validated flags, review notes, and record-level evidence references.

### Decision and Reasoning
Groups findings by type and prioritizes follow-up based on the documented rule and available evidence, not presumed intent.

### Outputs and Evidence
Produces a draft summary with counts, evidence gaps, and next checks.

### Limits and Constraints
It is not an audit opinion, fraud determination, or substitute for procurement policy.

### Failure Handling
Incomplete evidence is listed as unresolved rather than presented as confirmed misconduct.

### Human Review
An authorized auditor approves conclusions and ensures consistent due process.

## Data Quality and Uncertainty
Incorrect totals, mixed currencies, inconsistent units, missing records, or non-comparable categories can create false positives. Findings should retain record identifiers and explain the applicable rule.

## Security and Responsible Use
Minimize personal data and restrict access to sensitive procurement details. Do not use anomaly scores alone to discipline staff, blacklist suppliers, or allege wrongdoing.

## Audit and Reproducibility
Retain the source dataset version, rules, benchmarks, flagged record IDs, reviewer notes, and final disposition according to organizational policy.
