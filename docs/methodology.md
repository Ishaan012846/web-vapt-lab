# Security Assessment Methodology

This assessment follows an aligned methodology leveraging:
- **OWASP Web Security Testing Guide (WSTG v4.2)**
- **Penetration Testing Execution Standard (PTES)**
- **NIST SP 800-115**

## Assessment Lifecycle Phases

```
+---------------------+     +-----------------------+     +------------------------+
| 1. Scope & Setup    | --> | 2. Reconnaissance     | --> | 3. Automated Scanning  |
| (127.0.0.1 Binding) |     | (Nmap Service Scan)   |     | (OWASP ZAP Baseline)   |
+---------------------+     +-----------------------+     +------------------------+
                                                                     |
                                                                     v
+---------------------+     +-----------------------+     +------------------------+
| 6. Retest & Verify  | <-- | 5. Report & Dashboard | <-- | 4. Manual Validation   |
| (Patch Verification)|     | (Markdown & HTML)     |     | (Burp Suite Testing)   |
+---------------------+     +-----------------------+     +------------------------+
```

### Phase 1: Scope & Setup
- Confirm Docker container environment.
- Validate `config/scope.yaml` configuration to enforce 127.0.0.1 loopback targeting.

### Phase 2: Reconnaissance & Service Enumeration
- Execute Nmap to identify active listening services on TCP port 3000.
- Verify Express/Node.js web stack headers and application fingerprint.

### Phase 3: Automated Baseline Scanning
- Run OWASP ZAP passive baseline scan to identify security headers, cookie flags, and missing Anti-CSRF protections.

### Phase 4: Manual Validation
- Intercept HTTP traffic using Burp Suite.
- Validate SQL injection, XSS, IDOR, and authentication bypass vulnerabilities.

### Phase 5: Risk Assessment & Reporting
- Score confirmed findings via CVSS v3.1.
- Normalize findings JSON and render reports and executive dashboard.

### Phase 6: Retesting
- Verify patch implementation and update finding statuses.
