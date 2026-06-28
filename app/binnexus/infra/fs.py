# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 28 июня 2026 11:40:27
# Version: 1.0.82
# ========================================
# app\binnexus\infra\fs.py

from pathlib import Path

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)