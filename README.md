# Web Application VAPT Lab and Security Assessment

> **AUTHORIZATION NOTICE**: This project is designed strictly for educational purposes and authorized vulnerability assessments against a local, isolated instance of OWASP Juice Shop running on `127.0.0.1:3000`. Do not target or scan external networks or unauthorized systems.

---

## 🎯 Overview & Resume Description

**Resume Summary**:
> *Designed and implemented an isolated Web Application Vulnerability Assessment and Penetration Testing (VAPT) laboratory environment using Docker, OWASP Juice Shop, Nmap, OWASP ZAP, and Python automation. Engineered custom Python scope-validation modules enforcing strict loopback-only scanning policies (`127.0.0.1`), standardized VAPT finding schema definitions, automated report generation in Markdown, and built a zero-dependency HTML/CSS/JS security metrics dashboard.*

---

## ⚙️ Architecture & Technical Stack

- **Target Application**: OWASP Juice Shop (Containerized via Docker Compose)
- **Target Host Binding**: `127.0.0.1:3000` (Loopback isolation only)
- **Service Enumeration**: Nmap 7.9x (`-sV -p 3000`)
- **Automated Passive Scan**: OWASP ZAP Baseline Scanner
- **Manual Validation**: Burp Suite Community Edition
- **Orchestration & Validation**: Python 3.8+ (PyYAML, jsonschema, pytest)
- **Reporting & Dashboard**: Markdown report generator & static HTML5/CSS3/JavaScript dashboard

---

## 🚀 Quick Start Guide

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Python 3.8+](https://www.python.org/)
- Nmap & OWASP ZAP (Optional for live execution; scripts include fallback offline modes)

### Installation
```bash
# Clone the repository
git clone https://github.com/user/web-vapt-lab.git
cd web-vapt-lab

# Install Python dependencies
pip install -r requirements.txt

# Run environment pre-flight check
python scripts/setup_lab.py
```

---

## 🛠️ Lab Lifecycle Commands

| Command | Description |
| :--- | :--- |
| `make setup` | Validates prerequisites, directory structures, and scope YAML |
| `make start` | Launches OWASP Juice Shop container bound strictly to `127.0.0.1:3000` |
| `make check` | Runs HTTP health check against local target |
| `make scan` | Validates scope allowlist and executes Nmap & ZAP scans |
| `make report` | Normalizes scan findings against JSON schema and builds reports |
| `make test` | Runs unit test suite for scope validator, normalizer, and reports |
| `make stop` | Stops and removes local Juice Shop container |
| `make reset` | Requests confirmation and purges output/container state |

---

## 🔒 Scope & Security Enforcement

Every script validates the target against `config/scope.yaml` prior to execution.
- **Allowed Hosts**: `127.0.0.1`, `localhost`
- **Allowed Ports**: `3000`
- **Strict Prohibition**: Public IP addresses, subnets, and external domains are automatically rejected by `scripts/scope_validator.py`.

---

## 📊 Security Dashboard & Reports

After running `make report`, access the generated documentation artifacts:
1. **Interactive Dashboard**: Open `dashboard/index.html` in any modern web browser to view metric cards, severity filters, search inputs, and expandable finding cards.
2. **Markdown Reports**:
   - Technical Assessment Report: `reports/generated/vapt-assessment-report.md`
   - Executive Summary: `reports/generated/executive-summary.md`

---

## 🧪 Running Unit Tests

Run automated unit tests to verify scope enforcement, JSON schema validation, and severity scoring:
```bash
python -m pytest tests/ -v
```

---

## 📚 Documentation Index
- [Scope & Rules of Engagement](docs/scope-and-rules.md)
- [VAPT Methodology](docs/methodology.md)
- [Manual Testing Guide (Burp Suite)](docs/manual-testing-guide.md)
- [CVSS v3.1 Rating Guide](docs/cvss-guide.md)
- [Remediation Patterns](docs/remediation-guide.md)
- [Vulnerability Retest Guide](docs/retest-guide.md)

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
