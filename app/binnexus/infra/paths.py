# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 16 ноября 2026 08:32:04
# Version: 1.0.223
# ========================================
# app\binnexus\infra\paths.py

from pathlib import Path


def validate_input(path: Path):
    if not path.exists():
        raise ValueError(f"{path} is error")