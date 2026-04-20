# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 20 апреля 2026 16:19:56
# Version: 1.0.12
# ========================================
# app\binnexus\cli\args.py

import argparse
from pathlib import Path
import shutil


def parse_args():
    parser = argparse.ArgumentParser(
        prog="binnexus",
        description="Static dependency graph generator for Windows binaries (DLL/EXE).",
        epilog="""
    Examples:

      binnexus --input F:\\Game --exclude-system --exclude-crt
      binnexus --input . --output build --lang ru
      binnexus --input game --skip-dirs plugins temp cache
    """
    )

    parser.add_argument(
        "--build-portal",
        action="store_true",
        help="Build interactive HTML portal from graph.json (requires existing graph.json in output directory)"
    )

    parser.add_argument(
        "--input",
        metavar="PATH",
        help="Path to folder with binaries (DLL/EXE) to scan"
    )

    parser.add_argument(
        "--output",
        default="build",
        metavar="DIR",
        help="Output directory for generated portal (default: build)"
    )

    parser.add_argument(
        "--exclude-system",
        action="store_true",
        help="Exclude Windows system DLLs (kernel32, user32, etc.)"
    )

    parser.add_argument(
        "--exclude-crt",
        action="store_true",
        help="Exclude C/C++ runtime libraries (msvcrt, msvcp, api-ms-win-crt-*)"
    )

    parser.add_argument(
        "--lang",
        default="en",
        choices=["en", "ru"],
        help="Portal language (default: en)"
    )

    parser.add_argument(
        "--skip-dirs",
        nargs="*",
        default=["legacy"],
        metavar="DIR",
        help="Directories to skip during scan (default: legacy)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="binnexus 1.0"
    )

    parser.add_argument(
        "--runtime",
        action="store_true",
        help="Enable runtime module analysis via x32dbg"
    )

    parser.add_argument(
        "--runtime-include-system",
        action="store_true",
        help="Include system DLLs in runtime results (requires --runtime)"
    )

    parser.add_argument(
        "--runtime-engine",
        choices=["x32dbg", "x64dbg"],
        default="x32dbg",
        help="Runtime analysis engine (default: x32dbg)"
    )

    parser.add_argument(
        "--runtime-path",
        metavar="PATH",
        help="Path to debugger executable (x32dbg.exe or x64dbg.exe)"
    )

    parser.add_argument(
        "--runtime-timeout",
        type=int,
        default=3000,
        metavar="MS",
        help="Timeout for runtime analysis per file (ms)"
    )

    parser.add_argument(
        "--runtime-limit",
        type=int,
        default=50,
        help="Max number of binaries to analyze in runtime mode"
    )

    parser.add_argument(
        "--runtime-mode",
        choices=["all", "dll", "exe"],
        default="all",
        help="Which binaries to analyze in runtime (default: all)"
    )

    parser.add_argument(
        "--runtime-dump",
        action="store_true",
        help="Save raw runtime module lists for each binary"
    )

    parser.add_argument(
        "--runtime-verbose",
        action="store_true",
        help="Verbose runtime logging"
    )

    return parser, parser.parse_args()

def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> bool:
    state = True
    if args.build_portal:
        return True

    ROOT = Path(args.input)
    DIR_BUILD = Path(args.output)

    if not ROOT.exists():
        parser.error(f"--input path does not exist: {ROOT}")
        return False

    if not ROOT.is_dir():
        parser.error(f"--input must be a directory: {ROOT}")
        return False

    files = list(ROOT.rglob("*"))

    if not any(f.suffix.lower() in [".dll", ".exe"] for f in files):
      print("WARNING: No DLL or EXE files found in input directory")
    
    try:
        DIR_BUILD.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        parser.error(f"Cannot create output directory '{DIR_BUILD}': {e}")
        return False

    if shutil.which("dumpbin") is None:
        parser.error(
            "dumpbin not found. Run from 'Developer Command Prompt for Visual Studio'."
        )  
        return False
    
    if args.lang not in {"en", "ru"}:
        parser.error(f"Unsupported language: {args.lang}")
        return False

    return True