import sys
from datetime import datetime

from .core_runner import log
from .recon import recon
from .hosts import hosts
from .scan import scan
from .osint import osint
from .evidence import screenshots
from .report_builder import build_report
from .html_report import generate_html_report
from .attack_paths import attack_paths


def main():
    # ---------- INPUT VALIDATION ----------
    if len(sys.argv) != 2:
        print("Usage: python3 -m osint_tool.main <domain>")
        sys.exit(1)

    domain = sys.argv[1].strip()

    # ---------- SETUP ----------
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = f"assessment_{domain}_{timestamp}"

    log("SYSTEM", f"Starting full assessment for: {domain}")
    log("SYSTEM", f"Output directory: {base}")

    # ---------- PHASE 1: RECON ----------
    log("PHASE", "1/6 Reconnaissance")
    subs_file = recon(domain, base)

    if not subs_file:
        log("ERROR", "Recon failed. Stopping execution.")
        sys.exit(1)

    # ---------- PHASE 2: HOST DISCOVERY + INTEL ----------
    log("PHASE", "2/6 Host discovery + intelligence layer")
    target_file = hosts(subs_file, base)

    if not target_file:
        log("ERROR", "No targets found. Stopping execution.")
        sys.exit(1)

    # ---------- PHASE 3: VULNERABILITY SCAN ----------
    log("PHASE", "3/6 Vulnerability scanning")
    scan(target_file, domain, base)

    # ---------- PHASE 4: OSINT ----------
    log("PHASE", "4/6 External OSINT collection")
    osint(domain, base)

    # ---------- PHASE 5: EVIDENCE COLLECTION ----------
    log("PHASE", "5/6 Evidence gathering (screenshots)")
    screenshots(target_file, base)

    # ---------- PHASE 6: ATTACK PATH ENGINE ----------
    log("PHASE", "6/6 Attack path analysis")
    attack_paths(base)

    # ---------- REPORTING ----------
    log("PHASE", "Generating reports")
    build_report(base, domain)
    generate_html_report(base, domain)

    # ---------- DONE ----------
    log("SYSTEM", f"Assessment complete → {base}")


if __name__ == "__main__":
    main()
