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
git clone https://github.com/Ishaan012846/web-vapt-lab.git
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

## 💡 VAPT & Application Security Interview Q&A

This section provides comprehensive technical interview questions and sample answers grounded in this project's architecture and security findings.

### 1. Scope & Lab Guardrails

#### Q1: Why is target scope validation critical in security automation scripts, and how did you enforce loopback-only scanning in Python?
> **Answer**: Unchecked automated security tools can inadvertently target production systems, third-party APIs, or local network devices, leading to unauthorized scanning, service disruption, or legal violations. In this project, `scripts/scope_validator.py` inspects target strings against `config/scope.yaml`. It parses URLs using `urllib.parse`, resolves hostnames via `socket.gethostbyname()`, and verifies that the target IP strictly belongs to the loopback subnet (`127.0.0.1` / `::1`). If an external IP, public domain name, or unauthorized port is supplied, the script raises a `ValueError` and aborts execution before firing network requests or scanning tools.

#### Q2: What is the security difference between binding a Docker container port to `127.0.0.1:3000:3000` vs `0.0.0.0:3000:3000`?
> **Answer**: Binding to `0.0.0.0` exposes the container service on all host network interfaces (Ethernet, Wi-Fi, public IP), making the intentionally vulnerable application accessible to anyone on the same local subnet or external network. Binding explicitly to `127.0.0.1:3000:3000` restricts access solely to the host loopback interface, ensuring remote hosts cannot connect to or attack the laboratory target.

---

### 2. VAPT Methodology & Scanner Automation

#### Q3: What is the difference between passive baseline scanning and active vulnerability scanning?
> **Answer**: Passive scanning (such as OWASP ZAP baseline mode) analyzes HTTP traffic responses without sending malicious payloads or mutating state; it flags missing security headers, insecure cookie attributes, and information disclosures. Active scanning submits exploit payloads (e.g., SQLi, XSS strings) to test parameter handling. In our VAPT workflow, passive scanning runs automatically first to establish a baseline without risking target instability, while active validation is performed manually with Burp Suite under strict control.

#### Q4: Why can automated scanner outputs never be declared as confirmed vulnerabilities without manual verification?
> **Answer**: Automated scanners rely on signature matching and heuristic detection, which frequently produce false positives (e.g., flagging generic error pages as SQLi) or false negatives (missing complex authorization flaws like IDOR). Manual verification via tools like Burp Suite is required to validate exploitability, assess real-world impact, record reproducible evidence, and filter out false positives before issuing a formal VAPT report.

---

### 3. Vulnerability Analysis & Technical Remediation

#### Q5: How did you discover and validate SQL Injection (CWE-89) in OWASP Juice Shop, and how do Parameterized Queries remediate it?
> **Answer**: 
> - **Discovery & Validation**: Intercepted the login request (`POST /rest/user/login`) in Burp Suite and injected `' OR 1=1--` into the JSON `email` parameter. The server returned HTTP 200 OK with an admin JWT session token because the backend constructed SQL queries via unsafe string concatenation.
> - **Remediation**: Use Parameterized Queries (Prepared Statements) or ORMs (e.g., Sequelize replacement placeholders). Parameterized queries separate SQL command logic from data input, treating user parameters strictly as literal values regardless of metacharacters.

#### Q6: Explain the difference between Reflected, Stored, and DOM-based XSS (CWE-79) and their defense strategies.
> **Answer**:
> - **Reflected XSS**: Malicious script payload is passed in an HTTP request (e.g. URL query string) and reflected immediately in the server HTTP response body.
> - **Stored XSS**: Payload is saved persistently in the database (e.g. user reviews) and rendered to any victim viewing the record.
> - **DOM-based XSS**: Vulnerability resides entirely in client-side JavaScript code parsing unsafe sources (`location.search`, `window.name`) into dangerous sinks (`eval()`, `innerHTML`).
> - **Defense**: Context-aware output encoding (HTML, JavaScript, attribute encoding), using secure client frameworks (Angular/React auto-escaping), and enforcing a strict Content Security Policy (`CSP`).

#### Q7: What is an Insecure Direct Object Reference (IDOR / CWE-639), and how is it remediated?
> **Answer**:
> - **Issue**: IDOR occurs when an application exposes a reference to an internal implementation object (such as a database primary key in `GET /rest/basket/{id}`) without validating that the authenticated session user has permission to access that specific resource.
> - **Validation**: Changing `GET /rest/basket/1` (User A) to `GET /rest/basket/2` returned User B's cart contents.
> - **Remediation**: Implement session-aware access control checks on the server side:
>   ```javascript
>   Basket.findOne({ where: { id: req.params.id, UserId: req.user.id } })
>   ```

#### Q8: How does Cross-Site Request Forgery (CSRF / CWE-352) work, and how do you protect state-changing endpoints?
> **Answer**:
> - **Mechanism**: An attacker tricks an authenticated browser into making an unintended HTTP request to a vulnerable site where the victim has an active session cookie. Because browsers automatically attach cookies to cross-site requests, the server executes the action.
> - **Mitigation**: Implement anti-CSRF request tokens (Custom Headers / Double Submit Cookie pattern) or enforce cookie `SameSite=Strict` or `SameSite=Lax` attributes to block cross-site automatic cookie transmission.

#### Q9: What essential HTTP Security Headers should be configured on every web application?
> **Answer**:
> 1. `Content-Security-Policy (CSP)`: Restricts origins for scripts, images, and frames to mitigate XSS and data injection.
> 2. `Strict-Transport-Security (HSTS)`: Enforces HTTPS connections and prevents SSL stripping.
> 3. `X-Content-Type-Options: nosniff`: Prevents browsers from MIME-sniffing response content types.
> 4. `X-Frame-Options: DENY` or `frame-ancestors 'none'`: Prevents clickjacking by blocking embedding inside `<iframe>` tags.
> 5. `Referrer-Policy: strict-origin-when-cross-origin`: Controls sensitive URL leakage in HTTP Referer headers.

---

### 4. CVSS Scoring & Risk Assessment

#### Q10: How is a CVSS v3.1 Base Score calculated, and how is it mapped to Risk Severity?
> **Answer**: CVSS v3.1 evaluates 8 Base Metrics: Attack Vector (AV), Attack Complexity (AC), Privileges Required (PR), User Interaction (UI), Scope (S), Confidentiality (C), Integrity (I), and Availability (A). The numerical score (0.0 to 10.0) maps to severity thresholds:
> - **Critical**: 9.0 – 10.0 (e.g., Unauthenticated Network RCE / SQLi with full compromise)
> - **High**: 7.0 – 8.9 (e.g., Auth Bypass / High Impact Privilege Escalation)
> - **Medium**: 4.0 – 6.9 (e.g., IDOR, CSRF, Reflected XSS requiring user interaction)
> - **Low**: 0.1 – 3.9 (e.g., Missing security headers, verbose error messages)
> - **Informational**: 0.0 (e.g., Banner disclosure without direct exploitability)

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
