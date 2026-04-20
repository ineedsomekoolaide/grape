from .core_runner import log
import os
import json


def attack_paths(base):
    log("ATTACK", "Building attack graph")

    scan_dir = f"{base}/scan"
    intel_dir = f"{base}/intel"
    out_dir = f"{base}/attack_graph"

    os.makedirs(out_dir, exist_ok=True)

    vulns_file = f"{scan_dir}/vulns.txt"
    dirs_file = f"{scan_dir}/dirs.txt"
    intel_file = f"{intel_dir}/host_intel.txt"

    nodes = []
    edges = []
    node_id = 0

    def add_node(label, group):
        nonlocal node_id
        nodes.append({
            "id": node_id,
            "label": label,
            "group": group
        })
        node_id += 1
        return node_id - 1

    # Load data safely
    vulns = open(vulns_file).read().splitlines() if os.path.exists(vulns_file) else []
    dirs = open(dirs_file).read().splitlines() if os.path.exists(dirs_file) else []
    intel = open(intel_file).read().splitlines() if os.path.exists(intel_file) else []

    entry_nodes = []

    # IMPORTANT FIX: broader matching
    for line in intel:
        if any(x in line for x in [
            "API", "ADMIN", "AUTH", "MAIL",
            "ECOMMERCE", "ROOT", "SUBDOMAIN"
        ]):
            entry_nodes.append(add_node(line, "entry"))

    vuln_nodes = []
    dir_nodes = []

    for v in vulns:
        if v.strip():
            vuln_nodes.append(add_node(v, "vuln"))

    for d in dirs:
        if d.strip():
            dir_nodes.append(add_node(d, "exposure"))

    # Connect graph
    for e in entry_nodes:
        for v in vuln_nodes:
            edges.append({"from": e, "to": v})
        for d in dir_nodes:
            edges.append({"from": e, "to": d})

    graph = {"nodes": nodes, "edges": edges}

    graph_file = f"{out_dir}/attack_graph.json"

    with open(graph_file, "w") as f:
        json.dump(graph, f, indent=2)

    log("ATTACK", f"Graph generated with {len(nodes)} nodes")

    generate_html(graph_file, out_dir)

    return graph_file


def generate_html(json_file, out_dir):
    log("ATTACK", "Generating HTML visualization")

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <title>Attack Graph</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    #network {{
      width: 100%;
      height: 900px;
      border: 1px solid #ccc;
    }}
  </style>
</head>
<body>

<h2>Attack Graph Visualization</h2>
<div id="network"></div>

<script>
fetch("attack_graph.json")
.then(res => res.json())
.then(data => {{
    const nodes = new vis.DataSet(data.nodes);
    const edges = new vis.DataSet(data.edges);

    const container = document.getElementById("network");

    new vis.Network(container, {{
        nodes: nodes,
        edges: edges
    }}, {{
        nodes: {{
            shape: "dot",
            size: 14
        }},
        physics: {{
            stabilization: true
        }}
    }});
}});
</script>

</body>
</html>
"""

    with open(f"{out_dir}/attack_graph.html", "w") as f:
        f.write(html)

    log("ATTACK", "HTML graph generated → attack_graph.html")
