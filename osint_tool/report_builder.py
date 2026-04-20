import os
from datetime import datetime

def build_report(base, domain):
    file = f"{base}/FINAL_REPORT.md"

    vulns = f"{base}/scan/vulns.txt"

    with open(file, "w") as r:
        r.write(f"# Security Report\n")
        r.write(f"Target: {domain}\n")
        r.write(f"Date: {datetime.now()}\n\n")

        r.write("## Findings (raw nuclei output)\n\n")

        if os.path.exists(vulns):
            with open(vulns) as f:
                r.write(f.read())
        else:
            r.write("No data\n")
