from .core_runner import run, log
from .host_intel import host_intel
import os

def hosts(subs_file, base):
    log("HOSTS", "Starting live host probing")

    out = f"{base}/hosts"
    os.makedirs(out, exist_ok=True)

    live_file = f"{out}/live.txt"

    run([
        "httpx",
        "-l", subs_file,
        "-silent",
        "-status-code",
        "-title",
        "-follow-redirects"
    ], live_file, "HOSTS")

    log("HOSTS", "Running host intelligence layer")

    priority_file = host_intel(live_file, base)

    log("HOSTS", "Host intelligence complete")

    return priority_file
