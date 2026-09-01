"""Health check script for OWASP Juice Shop VAPT Lab target.

Validates that the target container is active and accepting connections on 127.0.0.1:3000.
"""

import sys
import urllib.request
import urllib.error
from scope_validator import load_scope_config, validate_target


def check_target_health(target_url: str = "http://127.0.0.1:3000", timeout: int = 5) -> bool:
    """Performs HTTP GET healthcheck against authorized local target."""
    validate_target(target_url)

    print(f"[+] Performing health check against local target: {target_url}")
    req = urllib.request.Request(
        target_url,
        headers={"User-Agent": "VAPT-Lab-HealthCheck/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.getcode()
            if status_code == 200:
                print(f"  [OK] Target is HEALTHY (HTTP {status_code}). OWASP Juice Shop is operational.")
                return True
            else:
                print(f"  [!] Target responded with HTTP status {status_code}.")
                return False
    except urllib.error.URLError as err:
        print(f"  [-] Target connection failed: {err.reason}")
        print("      Ensure OWASP Juice Shop container is running ('make start').")
        return False
    except Exception as e:
        print(f"  [-] Unexpected error during healthcheck: {e}")
        return False


def main():
    config = load_scope_config()
    target_url = config.get("target", {}).get("base_url", "http://127.0.0.1:3000")

    success = check_target_health(target_url)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
