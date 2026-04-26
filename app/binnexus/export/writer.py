# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 26 апреля 2026 06:50:20
# Version: 1.0.18
# ========================================
# app\binnexus\export\writer.py

import json
from pathlib import Path

from app.binnexus.core.graph import Graph
from app.binnexus.utils.symbols import pick_color

def save_exports_report(report: dict, exports_dir: Path):
    base = exports_dir / Path(report["file"]).stem

    json_path = base.with_suffix(".json")
    txt_path = base.with_suffix(".txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    with open(txt_path, "w", encoding="utf-8") as f:
        for item in report["exports"]:
            f.write(f"Address={item['address']}\n")
            f.write(f"Type={item['type']}\n")
            f.write(f"Ordinal={item['ordinal']}\n")

            if item["symbol"]:
                f.write(f"Symbol={item['symbol']}\n")

            if item["symbol_undecorated"]:
                f.write(f"Symbol (undecorated)={item['symbol_undecorated']}\n")

            if item["forwarder"]:
                f.write(f"Forwarder={item['forwarder']}\n")

def load_graph_json(input_file: Path) -> dict:
    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)
    
def build_graph_result(graph: Graph, export_stats, search_index=None) -> dict:
    edges = [
        {
            "source": e["source"],
            "target": e["target"],
            "types": sorted(e["types"]),
            "is_static": "static" in e["types"],
            "is_runtime": "runtime" in e["types"],
        }
        for e in graph.edge_map.values()
    ]

    nodes = sorted(graph.nodes)

    degree_static = {n: 0 for n in nodes}
    degree_runtime = {n: 0 for n in nodes}

    for e in edges:
        if e["is_static"]:
            degree_static[e["source"]] += 1
            degree_static[e["target"]] += 1

        if e["is_runtime"]:
            degree_runtime[e["source"]] += 1
            degree_runtime[e["target"]] += 1

    return {
        "nodes": [
            {
                "id": n,
                "type": "exe" if n.endswith(".exe") else "dll",
                "degree": degree_static[n] + degree_runtime[n],
                "degree_static": degree_static[n],
                "degree_runtime": degree_runtime[n],
                "export_count": export_stats.get(n, {}).get("clean_count", 0),
                "export_raw_count": export_stats.get(n, {}).get("raw_count", 0),
                "has_api": export_stats.get(n, {}).get("clean_count", 0) > 0,
                "color": pick_color(export_stats.get(n, {}).get("clean_count", 0)),
                "label": f"{n}\n{export_stats.get(n, {}).get('clean_count', 0)} exp",
                "is_runtime_only": (
                    export_stats.get(n, {}).get("clean_count", 0) == 0
                    and degree_runtime.get(n, 0) > 0
                ),
            }
            for n in nodes
        ],
        "edges": edges,
        "search_index": search_index or [],
    }

def save_graph_json(result: dict, output_file: Path):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)