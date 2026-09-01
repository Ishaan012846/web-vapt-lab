"""Unit tests for target scope validation module using unittest."""

import sys
import os
import unittest

# Add scripts directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from scope_validator import validate_target, load_scope_config


class TestScopeValidator(unittest.TestCase):

    def test_valid_loopback_targets(self):
        """Verify that legitimate local targets pass validation."""
        self.assertTrue(validate_target("http://127.0.0.1:3000"))
        self.assertTrue(validate_target("127.0.0.1:3000"))
        self.assertTrue(validate_target("http://localhost:3000"))

    def test_invalid_external_ip_rejection(self):
        """Verify that external IP addresses are strictly rejected."""
        with self.assertRaises(ValueError):
            validate_target("http://8.8.8.8:3000")

        with self.assertRaises(ValueError):
            validate_target("http://192.168.1.50:3000")

    def test_invalid_domain_rejection(self):
        """Verify that public domain names are strictly rejected."""
        with self.assertRaises(ValueError):
            validate_target("http://example.com:3000")

    def test_unauthorized_port_rejection(self):
        """Verify that non-allowed ports are rejected even on loopback."""
        with self.assertRaises(ValueError):
            validate_target("http://127.0.0.1:8080")


if __name__ == "__main__":
    unittest.main()
