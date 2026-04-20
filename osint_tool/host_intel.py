from .core_runner import log
import os


def classify(host):
    h = host.lower()

    # High-value entry points
    if "api" in h:
        return "API"

    if any(x in h for x in ["admin", "dashboard", "panel"]):
        return "ADMIN"

    if any(x in h for x in ["login", "auth", "signin", "sso"]):
        return "AUTH"

    if any(x in h for x in ["mail", "smtp", "imap", "pop"]):
        return "MAIL"

    if any(x in h for x in ["shop", "store", "cart", "checkout"]):
        return "ECOMMERCE"

    # Root domain (IMPORTANT)
    if h.count(".") == 1:
        return "ROOT"

    return "SUBDOMAIN"


def score(category):
    return {
        "API": 95,
        "ADMIN": 100,
        "AUTH": 90,
        "MAIL": 80,
        "ECOMMERCE": 75,
        "ROOT": 70,
        "SUBDOMAIN": 40
    }.get(category, 0)


def host_intel(live_file, base):
    log("INTEL", "Starting host intelligence analysis")

    if not os.path.exists(live_file):
        log("ERROR", "Live file not found")
        return None

    out_dir = f"{base}/intel"
    os.makedirs(out_dir, exist_ok=True)

    results = []

    with open(live_file, "r") as f:
        for line in f:
            host = line.strip()
            if not host:
                continue

            category = classify(host)
            sc = score(category)

            results.append((sc, category, host))

    results.sort(reverse=True)

    intel_file = f"{out_dir}/host_intel.txt"
    priority_file = f"{out_dir}/priority_targets.txt"

    with open(intel_file, "w") as f1, open(priority_file, "w") as f2:
        for sc, cat, host in results:
            f1.write(f"[{cat}] [score:{sc}] {host}\n")

            # Only high-value targets go forward
            if sc >= 70:
                f2.write(host + "\n")

    log("INTEL", f"Processed {len(results)} hosts")

    return priority_file
