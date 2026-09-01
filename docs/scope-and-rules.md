# Scope & Rules of Engagement

## Scope Definition
The authorized assessment scope is strictly constrained to the local OWASP Juice Shop instance running inside the local Docker environment.

- **Authorized URL**: `http://127.0.0.1:3000`
- **Authorized IP**: `127.0.0.1` (Loopback interface)
- **Authorized Ports**: TCP 3000

## Rules of Engagement (RoE)
1. **Loopback Isolation**: Under no circumstances should scanning or request manipulation scripts target non-loopback IP addresses, local network subnets, or public internet hosts.
2. **Rate Limiting**: Automated scanner tools must observe a maximum request threshold of 10 requests per second to avoid crashing the local container runtime.
3. **No Destructive Exploits**: DoS/DDoS attacks, disk wiping, kernel exploitation, memory corruption, and host operating system breakout attempts are strictly prohibited.
4. **Data Handling**: Captured HTTP requests, tokens, or logs must not contain real-world Personal Identifiable Information (PII). All findings data must be sanitized before storing in version control.
