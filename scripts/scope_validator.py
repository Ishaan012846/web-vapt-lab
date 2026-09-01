"""Scope Validation Module for VAPT Lab.

Validates target hosts and URLs against config/scope.yaml rules of engagement.
Ensures testing is restricted exclusively to localhost (127.0.0.1 / ::1).
"""

import os
import socket
import urllib.parse
from typing import Dict, Any

try:
    import yaml
except ImportError:
    yaml = None


def load_scope_config(config_path: str = "config/scope.yaml") -> Dict[str, Any]:
    """Loads scope configuration from YAML file or returns secure default fallback."""
    if not os.path.exists(config_path):
        alt_path = os.path.join(os.path.dirname(__file__), "..", config_path)
        if os.path.exists(alt_path):
            config_path = alt_path

    if os.path.exists(config_path) and yaml is not None:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # Secure fallback configuration if PyYAML is not installed
    return {
        "target": {
            "name": "OWASP Juice Shop Local Lab",
            "base_url": "http://127.0.0.1:3000",
            "allowed_hosts": ["127.0.0.1", "localhost"],
            "allowed_ports": [3000],
            "protocol": "http"
        }
    }


def validate_target(target_input: str, config_path: str = "config/scope.yaml") -> bool:
    """Validates that a target URL or hostname is strictly authorized and loopback-only.

    Args:
        target_input: URL or hostname string (e.g., 'http://127.0.0.1:3000', '127.0.0.1')
        config_path: Path to scope YAML configuration.

    Returns:
        True if target is authorized.

    Raises:
        ValueError: If target violates scope rules or targets external systems.
    """
    config = load_scope_config(config_path)
    allowed_hosts = set(config.get("target", {}).get("allowed_hosts", ["127.0.0.1", "localhost"]))
    allowed_ports = set(config.get("target", {}).get("allowed_ports", [3000]))

    # Parse target string
    if "://" in target_input:
        parsed = urllib.parse.urlparse(target_input)
        hostname = parsed.hostname
        port = parsed.port or (80 if parsed.scheme == "http" else 443 if parsed.scheme == "https" else None)
    else:
        if ":" in target_input:
            parts = target_input.split(":")
            hostname = parts[0]
            port = int(parts[1])
        else:
            hostname = target_input
            port = 3000

    if not hostname:
        raise ValueError(f"Invalid target specification: '{target_input}'")

    # Check hostname direct match
    if hostname not in allowed_hosts:
        try:
            resolved_ip = socket.gethostbyname(hostname)
            if resolved_ip not in ("127.0.0.1", "::1") and not resolved_ip.startswith("127."):
                raise ValueError(f"Target '{hostname}' resolved to non-loopback IP '{resolved_ip}'. Access Denied.")
        except socket.gaierror as err:
            raise ValueError(f"Could not resolve target hostname '{hostname}': {err}")

    # Check port match
    if port and port not in allowed_ports:
        raise ValueError(f"Port {port} is not in allowed scope ports: {allowed_ports}")

    return True


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:3000"
    try:
        if validate_target(target):
            print(f"[SCOPE OK] Target '{target}' is strictly authorized.")
    except Exception as e:
        print(f"[SCOPE VIOLATION] {e}")
        sys.exit(1)
