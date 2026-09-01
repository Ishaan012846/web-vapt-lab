"""Setup script for VAPT Lab environment.

Verifies prerequisites, validates scope configuration, and initializes output directory structures.
"""

import os
import subprocess
import sys
from scope_validator import load_scope_config, validate_target


def check_prerequisites():
    """Checks for required software tools and libraries."""
    print("[+] Checking environment prerequisites...")

    # Check Python version
    if sys.version_info < (3, 8):
        print("[-] Error: Python 3.8+ is required.")
        sys.exit(1)
    print(f"  [OK] Python version: {sys.version.split()[0]}")

    # Check Docker CLI
    try:
        res = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
        print(f"  [OK] Docker detected: {res.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  [!] Warning: Docker CLI not found or daemon not running.")
        print("      Ensure Docker Desktop is installed and started before running 'make start'.")

    # Check Nmap
    try:
        res = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
        first_line = res.stdout.splitlines()[0] if res.stdout else "Installed"
        print(f"  [OK] Nmap detected: {first_line}")
    except FileNotFoundError:
        print("  [!] Note: Nmap binary not found in PATH. 'run_nmap.py' will offer fallback guidance.")


def init_directories():
    """Creates output and evidence directories if they do not exist."""
    print("[+] Creating workspace output directories...")
    directories = [
        "output",
        "output/nmap",
        "output/zap",
        "evidence",
        "reports/generated"
    ]
    for d in directories:
        os.makedirs(d, exist_ok=True)
        print(f"  [OK] Directory ready: {d}")


def main():
    print("==================================================")
    print("   Web Application VAPT Lab - Environment Setup   ")
    print("==================================================")

    init_directories()
    check_prerequisites()

    print("[+] Validating scope configuration...")
    try:
        config = load_scope_config()
        target_url = config.get("target", {}).get("base_url", "http://127.0.0.1:3000")
        validate_target(target_url)
        print(f"  [OK] Scope configuration verified for target: {target_url}")
    except Exception as e:
        print(f"[-] Scope Validation Failed: {e}")
        sys.exit(1)

    print("\n[+] Setup completed successfully! You can now start the lab using 'make start'.")


if __name__ == "__main__":
    main()
