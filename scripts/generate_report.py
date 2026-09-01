"""Report Generation Script for VAPT Lab.

Ingests normalized findings JSON and generates Markdown and HTML documentation reports.
"""

import json
import os
import sys
from typing import Dict, Any, List


def load_normalized_findings(json_path: str = "output/normalized-findings.json") -> Dict[str, Any]:
    if not os.path.exists(json_path):
        alt = os.path.join("dashboard", "findings.json")
        if os.path.exists(alt):
            json_path = alt
        else:
            raise FileNotFoundError(f"Normalized findings file not found at {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_findings_summary_table(findings: List[Dict[str, Any]]) -> str:
    lines = []
    for f in findings:
        lines.append(
            f"| `{f['id']}` | {f['title']} | **{f['severity']}** | {f['cvss_score']} | {f['owasp_category']} | `{f['validation_status']}` |"
        )
    return "\n".join(lines)


def build_detailed_findings(findings: List[Dict[str, Any]]) -> str:
    blocks = []
    for f in findings:
        ref_list = "\n".join([f"- [{r}]({r})" for r in f.get("references", [])])
        block = f"""### {f['id']}: {f['title']}

- **Severity**: **{f['severity']}** (CVSS v3.1: `{f['cvss_score']}` - `{f['cvss_vector']}`)
- **OWASP Category**: {f['owasp_category']}
- **CWE**: {f['cwe_id']}
- **Affected Component**: `{f['affected_component']}`
- **Discovery Source**: {f['discovery_source']}
- **Validation Status**: `{f['validation_status']}`

#### Description
{f['description']}

#### Evidence
```text
{f['evidence']}
```

#### Reproduction Steps
{f['reproduction_steps']}

#### Security Impact
{f['impact']}

#### Remediation Recommendation
{f['remediation']}

#### References
{ref_list}

#### Tester Notes
_{f.get('tester_notes', 'N/A')}_

---
"""
        blocks.append(block)
    return "\n".join(blocks)


def generate_reports():
    os.makedirs("reports/generated", exist_ok=True)
    data = load_normalized_findings()

    meta = data.get("metadata", {})
    findings = data.get("findings", [])

    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0}
    for f in findings:
        sev = f.get("severity", "Informational")
        counts[sev] = counts.get(sev, 0) + 1

    summary_table = build_findings_summary_table(findings)
    detailed_findings = build_detailed_findings(findings)

    template_path = os.path.join("reports", "report-template.md")
    exec_template_path = os.path.join("reports", "executive-summary-template.md")

    with open(template_path, "r", encoding="utf-8") as f:
        rep_template = f.read()

    with open(exec_template_path, "r", encoding="utf-8") as f:
        exec_template = f.read()

    # Safely replace placeholdes without str.format collision on code braces
    exec_summary_text = exec_template
    exec_replacements = {
        "{total_findings}": str(meta.get("total_findings", len(findings))),
        "{critical_count}": str(counts["Critical"]),
        "{high_count}": str(counts["High"]),
        "{medium_count}": str(counts["Medium"]),
        "{low_count}": str(counts["Low"]),
        "{info_count}": str(counts["Informational"])
    }
    for k, v in exec_replacements.items():
        exec_summary_text = exec_summary_text.replace(k, v)

    full_report_text = rep_template
    report_replacements = {
        "{generated_at}": str(meta.get("generated_at", "2026-09-01")),
        "{tester}": str(meta.get("tester", "Security Auditor")),
        "{executive_summary}": exec_summary_text,
        "{findings_summary_table}": summary_table,
        "{detailed_findings}": detailed_findings
    }
    for k, v in report_replacements.items():
        full_report_text = full_report_text.replace(k, v)

    exec_out_path = os.path.join("reports", "generated", "executive-summary.md")
    full_out_path = os.path.join("reports", "generated", "vapt-assessment-report.md")

    with open(exec_out_path, "w", encoding="utf-8") as f:
        f.write(exec_summary_text)

    with open(full_out_path, "w", encoding="utf-8") as f:
        f.write(full_report_text)

    print(f"[+] Markdown reports generated successfully!")
    print(f"  [OK] Executive Summary: {exec_out_path}")
    print(f"  [OK] Technical VAPT Report: {full_out_path}")


if __name__ == "__main__":
    generate_reports()
