from datetime import datetime
import subprocess

# ---------- LOGGER ----------
def log(stage, message):
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] [{stage}] {message}")


# ---------- COMMAND RUNNER ----------
def run(cmd, outfile=None, stage="RUN"):
    try:
        log(stage, f"Executing: {' '.join(cmd)}")

        if outfile:
            with open(outfile, "w") as f:
                subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, check=True)
        else:
            subprocess.run(cmd, check=True)

    except Exception as e:
        log("ERROR", f"{cmd} -> {e}")
