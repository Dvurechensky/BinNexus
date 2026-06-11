# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 11 июня 2026 13:23:38
# Version: 1.0.65
# ========================================
# app\binnexus\infra\paths.py

from pathlib import Path


def validate_input(path: Path):
    if not path.exists():
        raise ValueError(f"{path} is error")