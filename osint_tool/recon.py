from .core_runner import run, log
import os

def recon(domain, base):
    log("RECON", f"Starting subdomain discovery: {domain}")

    out = f"{base}/subs"
    os.makedirs(out, exist_ok=True)

    run(["subfinder", "-d", domain], f"{out}/subfinder.txt", "RECON")
    run(["amass", "enum", "-passive", "-d", domain], f"{out}/amass.txt", "RECON")
    run(["assetfinder", "--subs-only", domain], f"{out}/assetfinder.txt", "RECON")

    log("RECON", "Subdomain discovery complete")

    return f"{out}/subfinder.txt"
