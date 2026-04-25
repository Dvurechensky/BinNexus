# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 25 апреля 2026 08:09:10
# Version: 1.0.17
# ========================================
# app\binnexus\cli\main.py

import argparse
from pathlib import Path
import shutil

from app.binnexus.cli.args import parse_args, validate_args
from app.binnexus.core.config import Config
from app.binnexus.core.pipeline import AnalysisPipeline
from app.binnexus.export.writer import build_graph_result, load_graph_json, save_graph_json
from app.binnexus.portal.builder import PortalBuilder
from app.binnexus.runtime.build_runtime_modules import build_runtime_modules
from app.binnexus.utils.logging import app_logger

def main():
    parser, args = parse_args()

    if args.build_portal:
        output = Path(args.output or "build")
        graph_path = output / "portal" / "graph.json"

        if not graph_path.exists():
            app_logger.error(f"Graph file not found: {graph_path}")
            return

        app_logger.info("Building portal from existing graph...")
        config = Config(
            input=Path("."),  # не используется
            output=Path(args.output),
            exclude_system=False,
            exclude_crt=False,
            lang=args.lang,
            skip_dirs=set(),
            runtime=False,
            runtime_limit=0,
            runtime_mode="all",
            runtime_timeout=0,
            runtime_dump=False,
            runtime_verbose=False,
            runtime_include_system=False,
        )

        builder = PortalBuilder(config)
        graph = load_graph_json(graph_path)
        builder.build(graph)

        app_logger.info("Portal rebuilt successfully")
        return
    
    app_logger.info("BinNexus starting...")
    app_logger.info(f"Input: {args.input}")
    app_logger.info(f"Output: {args.output}")
    app_logger.info(f"Runtime: {'ON' if args.runtime else 'OFF'}")

    if not validate_args(parser, args):
        app_logger.error("Argument validation failed")
        return

    config = Config(
        input=Path(args.input),
        output=Path(args.output),
        exclude_system=args.exclude_system,
        exclude_crt=args.exclude_crt,
        lang=args.lang,
        skip_dirs=set(args.skip_dirs),
        runtime=args.runtime,
        runtime_limit=args.runtime_limit,
        runtime_mode=args.runtime_mode,
        runtime_timeout=args.runtime_timeout,
        runtime_dump=args.runtime_dump,
        runtime_verbose=args.runtime_verbose,
        runtime_include_system=args.runtime_include_system,
    )

    app_logger.info("Validating config...")

    if not config.validate():
        app_logger.error("Config validation failed")
        return

    # Build runtime modules (if needed)
    build_runtime_modules()

    app_logger.info("Running analysis pipeline...")

    pipeline = AnalysisPipeline(config)
    graph, export_stats = pipeline.run()

    result = build_graph_result(graph, export_stats)

    app_logger.info(f"Graph nodes: {len(graph.nodes)}")
    app_logger.info(f"Graph edges: {len(graph.edge_map)}")

    app_logger.info("Saving graph...")
    save_graph_json(result, config.graph_path)

    app_logger.info("Building portal...")
    builder = PortalBuilder(config)
    builder.build(result)

    app_logger.info("Done")

if __name__ == "__main__":
    main()