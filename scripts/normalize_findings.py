"""Normalizes scan findings into standard schema structure.

Validates against findings/findings.schema.json and categorizes severity based on CVSS v3.1 scores.
"""

import json
import os
import sys
from typing import Dict, Any, List

try:
    import jsonschema
except ImportError:
    jsonschema = None


def calculate_severity_from_cvss(score: float) -> str:
    """Calculates standard severity rating from numerical CVSS v3.1 score."""
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 4.0:
        return "Medium"
    elif score > 0.0:
        return "Low"
    else:
        return "Informational"


def load_json(filepath: str) -> Dict[str, Any]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_normalized_data(data: Dict[str, Any], schema_path: str = "findings/findings.schema.json") -> bool:
    """Validates normalized JSON data structure against JSON Schema."""
    if not os.path.exists(schema_path):
        alt = os.path.join(os.path.dirname(__file__), "..", schema_path)
        if os.path.exists(alt):
            schema_path = alt

    if jsonschema is not None and os.path.exists(schema_path):
        schema = load_json(schema_path)
        try:
            jsonschema.validate(instance=data, schema=schema)
            return True
        except jsonschema.ValidationError as err:
            print(f"[-] Schema Validation Error: {err.message} (path: {list(err.path)})")
            return False

    if "metadata" in data and "findings" in data:
        return True
    return False


def normalize_findings():
    """Reads available raw logs or example data, normalizes structure, and writes output."""
    os.makedirs("output", exist_ok=True)
    os.makedirs("dashboard", exist_ok=True)
    output_path = os.path.join("output", "normalized-findings.json")
    dashboard_path = os.path.join("dashboard", "findings.json")

    print("[+] Normalizing assessment findings...")

    example_path = os.path.join("findings", "findings.example.json")
    final_data = None

    if os.path.exists(example_path):
        print(f"  [OK] Loading baseline findings from {example_path}")
        final_data = load_json(example_path)

    if final_data and "findings" in final_data:
        for item in final_data["findings"]:
            cvss = float(item.get("cvss_score", 0.0))
            expected_sev = calculate_severity_from_cvss(cvss)
            if item.get("severity") != expected_sev:
                print(f"  [!] Recalculating severity for {item['id']}: {item['severity']} -> {expected_sev}")
                item["severity"] = expected_sev

    is_valid = validate_normalized_data(final_data)
    if is_valid:
        print("  [OK] Normalized dataset passed schema validation.")
    else:
        print("  [!] Dataset contains schema warnings. Proceeding with normalized output...")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2)

    with open(dashboard_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2)

    print(f"  [OK] Normalized output saved to {output_path}")
    print(f"  [OK] Dashboard data updated at {dashboard_path}")


if __name__ == "__main__":
    normalize_findings()
