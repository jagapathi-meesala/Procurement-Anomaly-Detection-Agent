from pathlib import Path
import sys
root = Path(__file__).resolve().parents[1]
required = ["agent.yaml","SOUL.md","README.md","RULES.md","DUTIES.md","AGENTS.md","EXPLAINABILITY.md","requirements.txt","pytest.ini","core/anomaly.py","tools/analyze-procurement-records.yaml","tools/explain-anomaly-flags.yaml","tools/generate-audit-summary.yaml","skills/procurement-data-review/SKILL.md","skills/anomaly-triage/SKILL.md","skills/audit-reporting/SKILL.md","tests/test_anomaly.py","verification/readiness_audit.py"]
missing = [p for p in required if not (root/p).is_file()]
if missing:
    print("FAIL: missing required files:", ", ".join(missing)); sys.exit(1)
print(f"PASS: all {len(required)}/{len(required)} required files present")
