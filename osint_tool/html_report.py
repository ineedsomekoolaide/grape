import os

def generate_html_report(base, domain):
    out = f"{base}/report.html"

    vulns = f"{base}/scan/vulns.txt"
    shots = f"{base}/evidence/screenshots"

    with open(out, "w") as h:
        h.write(f"<h1>{domain} Security Report</h1>")

        h.write("<h2>Findings</h2>")

        if os.path.exists(vulns):
            h.write("<pre>")
            h.write(open(vulns).read())
            h.write("</pre>")

        h.write("<h2>Screenshots</h2>")

        if os.path.exists(shots):
            for img in os.listdir(shots):
                h.write(f'<img src="evidence/screenshots/{img}" width="600"><br>')
