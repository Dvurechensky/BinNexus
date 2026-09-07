# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 07 сентября 2026 08:14:01
# Version: 1.0.154
# ========================================
# app\binnexus\infra\fs.py

from pathlib import Path

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)