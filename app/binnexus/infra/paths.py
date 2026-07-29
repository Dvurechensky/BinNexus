# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 29 июля 2026 15:42:50
# Version: 1.0.114
# ========================================
# app\binnexus\infra\paths.py

from pathlib import Path


def validate_input(path: Path):
    if not path.exists():
        raise ValueError(f"{path} is error")