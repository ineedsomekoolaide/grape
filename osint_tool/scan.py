from .core_runner import run, log
import os

def scan(target_file, domain, base):
    out = f"{base}/scan"
    os.makedirs(out, exist_ok=True)

    if not target_file:
        log("ERROR", "No target file provided to scan")
        return

    log("SCAN", "Starting technology detection")
    run(["whatweb", "-i", target_file], f"{out}/tech.txt", "SCAN")

    log("SCAN", "Running vulnerability scan (nuclei)")
    run([
        "nuclei",
        "-l", target_file,
        "-severity", "medium,high,critical"
    ], f"{out}/vulns.txt", "SCAN")

    log("SCAN", "Running directory brute force (ffuf)")
    run([
        "ffuf",
        "-w", "/usr/share/wordlists/dirb/common.txt",
        "-u", f"https://{domain}/FUZZ",
        "-rate", "50",
        "-mc", "200,403"
    ], f"{out}/dirs.txt", "SCAN")

    log("SCAN", "Scan complete")
