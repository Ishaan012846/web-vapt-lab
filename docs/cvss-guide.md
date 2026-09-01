# CVSS v3.1 Scoring & Vulnerability Rating Guide

## CVSS v3.1 Metric Breakdown

CVSS (Common Vulnerability Scoring System) v3.1 provides a standardized framework for calculating severity based on Base Metrics:

### Base Metrics

1. **Attack Vector (AV)**: Network (N), Adjacent (A), Local (L), Physical (P)
2. **Attack Complexity (AC)**: Low (L), High (H)
3. **Privileges Required (PR)**: None (N), Low (L), High (H)
4. **User Interaction (UI)**: None (N), Required (R)
5. **Scope (S)**: Unchanged (U), Changed (C)
6. **Confidentiality (C)**: None (N), Low (L), High (H)
7. **Integrity (I)**: None (N), Low (L), High (H)
8. **Availability (A)**: None (N), Low (L), High (H)

## Severity Scale Mapping

| Rating | CVSS Score Range | Action SLA |
| :--- | :--- | :--- |
| **Critical** | 9.0 – 10.0 | Remediate within 24–48 hours |
| **High** | 7.0 – 8.9 | Remediate within 7 days |
| **Medium** | 4.0 – 6.9 | Remediate within 30 days |
| **Low** | 0.1 – 3.9 | Remediate within 90 days |
| **Informational** | 0.0 | Review during normal maintenance |

## Example CVSS Vector Breakdown

### SQL Injection (`VAPT-2026-001`)
- **Vector**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
- **Score**: **9.8 (Critical)**
- **Explanation**: Accessible over the Network (AV:N), Low Complexity (AC:L), No Privileges required (PR:N), No User Interaction (UI:N), Scope Unchanged (S:U), High impact to Confidentiality, Integrity, and Availability.
