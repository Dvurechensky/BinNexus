# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 27 апреля 2026 09:39:21
# Version: 1.0.20
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



