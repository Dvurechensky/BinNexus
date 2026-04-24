# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 24 апреля 2026 06:50:20
# Version: 1.0.16
# ========================================
# app\binnexus\core\graph.py

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edge_map = {}

    def add_node(self, name: str):
        self.nodes.add(name.lower())
        
    def add_edge(self, source: str, target: str, edge_type: str):
        key = (source.lower(), target.lower())

        if key not in self.edge_map:
            self.edge_map[key] = {
                "source": source.lower(),
                "target": target.lower(),
                "types": set(),
            }

        self.edge_map[key]["types"].add(edge_type)

    def to_dict(self):
        return {
            "nodes": list(self.nodes),
            "edges": [
                {
                    "source": e["source"],
                    "target": e["target"],
                    "types": list(e["types"]),
                }
                for e in self.edge_map.values()
            ]
        }