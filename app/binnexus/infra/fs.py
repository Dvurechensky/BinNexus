# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 28 ноября 2026 11:57:30
# Version: 1.0.235
# ========================================
# app\binnexus\infra\fs.py

from pathlib import Path

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)