from .core_runner import run, log
import os

def osint(domain, base):
    log("OSINT", "Starting OSINT collection")

    out = f"{base}/osint"
    os.makedirs(out, exist_ok=True)

    run(["whois", domain], f"{out}/whois.txt", "OSINT")
    run(["theHarvester", "-d", domain, "-b", "all"], f"{out}/emails.txt", "OSINT")

    log("OSINT", "OSINT collection complete")
