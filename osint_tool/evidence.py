from .core_runner import log
import subprocess
import os

def screenshots(live_file, base):
    out = f"{base}/evidence/screenshots"
    os.makedirs(out, exist_ok=True)

    log("EVIDENCE", "Starting gowitness screenshot capture")

    if not os.path.exists(live_file):
        log("ERROR", "Live file missing")
        return

    try:
        subprocess.run([
            "gowitness",
            "scan",
            "file",
            "-f", live_file
        ], check=True)

        log("EVIDENCE", "Screenshots completed")

    except Exception as e:
        log("ERROR", f"gowitness failed: {e}")
