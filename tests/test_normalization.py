"""Unit tests for finding normalization and CVSS severity mapping using unittest."""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from normalize_findings import calculate_severity_from_cvss, validate_normalized_data, load_json


class TestNormalization(unittest.TestCase):

    def test_cvss_severity_calculation(self):
        """Verify CVSS v3.1 score to severity label mapping."""
        self.assertEqual(calculate_severity_from_cvss(9.8), "Critical")
        self.assertEqual(calculate_severity_from_cvss(9.0), "Critical")
        self.assertEqual(calculate_severity_from_cvss(8.9), "High")
        self.assertEqual(calculate_severity_from_cvss(7.0), "High")
        self.assertEqual(calculate_severity_from_cvss(6.5), "Medium")
        self.assertEqual(calculate_severity_from_cvss(4.0), "Medium")
        self.assertEqual(calculate_severity_from_cvss(3.7), "Low")
        self.assertEqual(calculate_severity_from_cvss(0.1), "Low")
        self.assertEqual(calculate_severity_from_cvss(0.0), "Informational")

    def test_example_findings_schema_validation(self):
        """Verify that findings.example.json structure is valid."""
        example_path = os.path.join("findings", "findings.example.json")
        schema_path = os.path.join("findings", "findings.schema.json")

        self.assertTrue(os.path.exists(example_path), "findings.example.json must exist")
        self.assertTrue(os.path.exists(schema_path), "findings.schema.json must exist")

        data = load_json(example_path)
        is_valid = validate_normalized_data(data, schema_path=schema_path)
        self.assertTrue(is_valid)


if __name__ == "__main__":
    unittest.main()
