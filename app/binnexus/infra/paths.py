# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 23 сентября 2026 09:39:13
# Version: 1.0.170
# ========================================
# app\binnexus\infra\paths.py

from pathlib import Path


def validate_input(path: Path):
    if not path.exists():
        raise ValueError(f"{path} is error")