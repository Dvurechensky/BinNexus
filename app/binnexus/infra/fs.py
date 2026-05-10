# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 10 мая 2026 07:40:09
# Version: 1.0.33
# ========================================
# app\binnexus\infra\fs.py

from pathlib import Path

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)