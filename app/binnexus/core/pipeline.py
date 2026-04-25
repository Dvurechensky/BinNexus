# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 25 апреля 2026 08:09:10
# Version: 1.0.17
# ========================================
# app\binnexus\core\pipeline.py

from pathlib import Path

from app.binnexus.analysis.runtime.collector import collect_runtime_for_files
from app.binnexus.analysis.static.imports import get_imports
from app.binnexus.analysis.static.exports import extract_exports
from app.binnexus.core.graph import Graph
from app.binnexus.core.scanner import scan_files
from app.binnexus.export.writer import save_exports_report
from app.binnexus.utils.logging import app_logger


class AnalysisPipeline:

    def __init__(self, config):
        self.config = config

    def run(self):
        files = scan_files(self.config.root, self.config.skip_dirs)

        graph = Graph()
        export_stats = {}

        for file in files:
            name = file.name.lower()
            graph.add_node(name)

            # IMPORTS
            try:
                imports = get_imports(file)

                for imp in imports:
                    imp = Path(imp).name.strip().lower()

                    if not self._should_include(imp):
                        continue

                    graph.add_node(imp)
                    graph.add_edge(name, imp, "static")

            except Exception as e:
                print(f"[IMPORT ERROR] {file} -> {e}")

            # EXPORTS
            try:
                report = extract_exports(file)

                save_exports_report(report, self.config.exports_dir)

                export_stats[name] = {
                    "raw_count": report["raw_count"],
                    "clean_count": report["clean_count"],
                }

            except Exception as e:
                print(f"[EXPORT ERROR] {file} -> {e}")
                export_stats[name] = {
                    "raw_count": 0,
                    "clean_count": 0,
                }

        # RUNTIME
        if self.config.runtime:
            app_logger.info("Running runtime analysis...")

            before_nodes = len(graph.nodes)
            before_edges = len(graph.edge_map)

            collect_runtime_for_files(files, graph, self.config)

            after_nodes = len(graph.nodes)
            after_edges = len(graph.edge_map)

            app_logger.info(
                f"Runtime merged: +{after_nodes - before_nodes} nodes, +{after_edges - before_edges} edges"
            )
        else:
            app_logger.info("Runtime analysis skipped")

        return graph, export_stats

    def _should_include(self, dll_name: str) -> bool:
        return dll_name not in self.config.excluded_dlls