import os
from core_runner import run

def scan(live_file, domain, base):
    out = f"{base}/scan"
    os.makedirs(out, exist_ok=True)

    run(["whatweb", "-i", live_file], f"{out}/tech.txt")

    run([
        "nuclei",
        "-l", live_file,
        "-severity", "medium,high,critical"
    ], f"{out}/vulns.txt")

    run([
        "ffuf",
        "-w", "/usr/share/wordlists/dirb/common.txt",
        "-u", f"https://{domain}/FUZZ",
        "-rate", "50",
        "-mc", "200,403"
    ], f"{out}/dirs.txt")
