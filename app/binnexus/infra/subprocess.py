# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 20 сентября 2026 08:40:47
# Version: 1.0.167
# ========================================
# app\binnexus\infra\subprocess.py

import subprocess


def run_dumpbin(file):
    result = subprocess.run(
        ["dumpbin", "/imports", str(file)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    return result.stdout