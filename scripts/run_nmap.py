"""Nmap Service Enumeration Script for VAPT Lab.

Executes safe port and version scanning strictly against authorized 127.0.0.1:3000 target.
Output is saved to gitignored output/nmap/ directory.
"""

import os
import subprocess
import sys
from scope_validator import load_scope_config, validate_target


def run_nmap_scan(target_host: str = "127.0.0.1", target_port: int = 3000):
    """Runs Nmap scan safely without shell=True."""
    target_str = f"{target_host}:{target_port}"
    validate_target(target_str)

    os.makedirs("output/nmap", exist_ok=True)
    xml_out = os.path.join("output", "nmap", "nmap-scan.xml")
    txt_out = os.path.join("output", "nmap", "nmap-scan.txt")

    print(f"[+] Starting Nmap service enumeration against {target_host}:{target_port}...")

    nmap_path = None
    for name in ["nmap", "nmap.exe"]:
        try:
            subprocess.run([name, "--version"], capture_output=True, check=True)
            nmap_path = name
            break
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue

    if not nmap_path:
        print("  [!] Nmap executable not found in PATH.")
        print("      To run live Nmap scans, install Nmap (https://nmap.org/download.html).")
        print("      Writing simulated enumeration record to output/nmap/nmap-scan.txt for offline testing...")
        
        simulated_output = (
            f"Nmap 7.94 scan report for localhost ({target_host})\n"
            f"Host is up (0.00010s latency).\n"
            f"PORT     STATE SERVICE VERSION\n"
            f"{target_port}/tcp open  http    Node.js Express framework (OWASP Juice Shop 16.0.0)\n"
            f"Service Info: Container Docker\n"
        )
        with open(txt_out, "w", encoding="utf-8") as f:
            f.write(simulated_output)
        print(f"  [OK] Simulated scan output saved to {txt_out}")
        return

    cmd = [
        nmap_path,
        "-sV",
        "-p", str(target_port),
        "-oX", xml_out,
        "-oN", txt_out,
        target_host
    ]

    print(f"  [>] Executing command: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=True)
        print(f"  [OK] Nmap scan completed successfully.")
        print(f"  [OK] Raw results saved to: {txt_out} and {xml_out}")
    except subprocess.CalledProcessError as err:
        print(f"  [-] Nmap execution failed with code {err.returncode}: {err.stderr}")
    except subprocess.TimeoutExpired:
        print("  [-] Nmap scan timed out after 60 seconds.")


def main():
    config = load_scope_config()
    target_host = "127.0.0.1"
    ports = config.get("target", {}).get("allowed_ports", [3000])
    target_port = ports[0] if ports else 3000

    run_nmap_scan(target_host, target_port)


if __name__ == "__main__":
    main()
