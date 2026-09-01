# Security Policy

## Educational & Authorized Testing Notice

This repository contains security assessment scripts, documentation, and Docker configurations designed **STRICTLY for educational and authorized local laboratory testing**.

### Scope & Constraints
- The target application (OWASP Juice Shop) is bound ONLY to `127.0.0.1:3000`.
- All automated scanning scripts check `config/scope.yaml` and abort if directed against external IP addresses or non-loopback domain names.
- Do NOT modify scripts to target unauthorized external hosts, domain names, or networks.

## Reporting Vulnerabilities in this Repository

If you discover a vulnerability in the automation scripts or configuration of this repository, please report it privately via standard GitHub repository disclosure mechanisms or contact the maintainer.

Do NOT use the tools in this repository against any systems for which you do not have explicit, written authorization.
