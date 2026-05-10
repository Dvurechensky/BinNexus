# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 10 мая 2026 07:40:09
# Version: 1.0.33
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