"""Unit tests for report generation functionality using unittest."""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from generate_report import build_findings_summary_table, build_detailed_findings


class TestReportGenerator(unittest.TestCase):

    def test_build_summary_table(self):
        sample_findings = [
            {
                "id": "VAPT-2026-001",
                "title": "SQL Injection",
                "severity": "Critical",
                "cvss_score": 9.8,
                "owasp_category": "A03:2021-Injection",
                "validation_status": "confirmed"
            }
        ]
        table = build_findings_summary_table(sample_findings)
        self.assertIn("`VAPT-2026-001`", table)
        self.assertIn("**Critical**", table)
        self.assertIn("A03:2021-Injection", table)

    def test_build_detailed_findings(self):
        sample_findings = [
            {
                "id": "VAPT-2026-001",
                "title": "SQL Injection",
                "severity": "Critical",
                "cvss_score": 9.8,
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                "owasp_category": "A03:2021-Injection",
                "cwe_id": "CWE-89",
                "affected_component": "POST /rest/user/login",
                "discovery_source": "Manual Burp Suite",
                "validation_status": "confirmed",
                "description": "SQLi in login",
                "evidence": "Payload evidence",
                "reproduction_steps": "Steps to reproduce",
                "impact": "High impact",
                "remediation": "Use prepared statements",
                "references": ["https://owasp.org"]
            }
        ]
        details = build_detailed_findings(sample_findings)
        self.assertIn("### VAPT-2026-001: SQL Injection", details)
        self.assertIn("CWE-89", details)
        self.assertIn("Use prepared statements", details)


if __name__ == "__main__":
    unittest.main()
