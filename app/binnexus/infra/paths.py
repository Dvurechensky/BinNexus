# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 08 июля 2026 07:24:55
# Version: 1.0.93
# ========================================
# app\binnexus\infra\paths.py

from pathlib import Path


def validate_input(path: Path):
    if not path.exists():
        raise ValueError(f"{path} is error")