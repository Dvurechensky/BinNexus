# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 04 июля 2026 08:45:44
# Version: 1.0.89
# ========================================
# app\binnexus\core\scanner.py

from pathlib import Path

def scan_files(root: Path, skip_dirs: set[str]) -> list[Path]:
    result = []

    for file in root.rglob("*"):
        if any(part.lower() in skip_dirs for part in file.parts):
            continue

        if file.suffix.lower() in (".dll", ".exe"):
            result.append(file)

    return result



