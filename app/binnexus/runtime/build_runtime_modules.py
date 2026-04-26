# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 26 апреля 2026 09:55:47
# Version: 1.0.19
# ========================================
# app\binnexus\runtime\build_runtime_modules.py

from pathlib import Path
import subprocess

def build_runtime_modules():
    root = Path(__file__).parent  # папка runtime

    runtime_cpp = root / "runtime_dump.cpp"
    dll_loader_cpp = root / "dll_loader.cpp"

    runtime_exe = root / "runtime_dump.exe"
    dll_loader_exe = root / "dll_loader.exe"

    print("[BinNexus] building runtime...")

    # dll loader
    subprocess.run([
        "cl",
        "/EHsc",
        "/nologo",
        str(dll_loader_cpp),
        "/Fe:" + str(dll_loader_exe)
    ], check=True, cwd=root)

    # runtime dump
    subprocess.run([
        "cl",
        "/EHsc",
        "/nologo",
        str(runtime_cpp),
        "psapi.lib",
        "/Fe:" + str(runtime_exe)
    ], check=True, cwd=root)