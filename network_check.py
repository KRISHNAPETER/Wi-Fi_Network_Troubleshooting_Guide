#!/usr/bin/env python3
"""
network_check.py - Quick connectivity diagnosis (the "ping ladder").

Runs the same checks a support engineer does by hand:
  1. Loopback      (is the TCP/IP stack working on this PC?)
  2. Default gateway (can I reach my router?)
  3. Public IP     (can I reach the internet?)
  4. DNS           (can I resolve a domain name?)

Then it prints where the problem most likely is.
Works on Windows, Linux and macOS. No extra packages needed.

Usage:  python network_check.py
"""

import platform
import re
import socket
import subprocess

PUBLIC_IP = "8.8.8.8"
TEST_DOMAIN = "google.com"


def ping(host: str, count: int = 2) -> bool:
    """Return True if the host replies to ping."""
    flag = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", flag, str(count), host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_gateway():
    """Find the default gateway IP, or None if there isn't one."""
    system = platform.system().lower()
    try:
        if system == "windows":
            out = subprocess.run(["ipconfig"], stdout=subprocess.PIPE,
                                 text=True, timeout=10).stdout
            match = re.search(r"Default Gateway[ .]*:\s*(\d+\.\d+\.\d+\.\d+)", out)
        elif system == "darwin":
            out = subprocess.run(["route", "-n", "get", "default"],
                                 stdout=subprocess.PIPE, text=True, timeout=10).stdout
            match = re.search(r"gateway:\s*(\d+\.\d+\.\d+\.\d+)", out)
        else:  # Linux
            out = subprocess.run(["ip", "route"], stdout=subprocess.PIPE,
                                 text=True, timeout=10).stdout
            match = re.search(r"default via (\d+\.\d+\.\d+\.\d+)", out)
        return match.group(1) if match else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def dns_works(domain: str) -> bool:
    """Return True if the domain name can be resolved to an IP."""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


def show(label: str, ok: bool) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")


def main() -> None:
    print("\n=== Network Check ===\n")

    loopback = ping("127.0.0.1")
    show("Loopback (127.0.0.1) - TCP/IP stack on this PC", loopback)

    gateway = get_gateway()
    if gateway:
        gateway_ok = ping(gateway)
        show(f"Default gateway ({gateway}) - your router", gateway_ok)
    else:
        gateway_ok = False
        show("Default gateway - none found (no IP from DHCP?)", False)

    public_ok = ping(PUBLIC_IP)
    show(f"Public IP ({PUBLIC_IP}) - internet reachable", public_ok)

    dns_ok = dns_works(TEST_DOMAIN)
    show(f"DNS lookup ({TEST_DOMAIN}) - name resolution", dns_ok)

    print("\n--- Diagnosis ---")
    if not loopback:
        print("Problem with the TCP/IP stack or network adapter on this PC.")
        print("Try: restart the adapter, reset the stack (netsh int ip reset).")
    elif not gateway_ok:
        print("Cannot reach the router. Check Wi-Fi/cable, IP settings and DHCP.")
        print("Try: reconnect to Wi-Fi, ipconfig /release then /renew, restart router.")
    elif not public_ok:
        print("Router is reachable but the internet is not. Likely an ISP/modem issue.")
        print("Try: restart the modem, check WAN light, call the ISP.")
    elif not dns_ok:
        print("Internet works but names do not resolve. This is a DNS problem.")
        print("Try: ipconfig /flushdns, set DNS to 8.8.8.8 and 1.1.1.1.")
    else:
        print("All checks passed. If a site still fails, the problem is with that site")
        print("or the browser (clear cache, try another browser).")
    print()


if __name__ == "__main__":
    main()
