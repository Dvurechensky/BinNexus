# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 18 апреля 2026 14:42:40
# Version: 1.0.10
# ========================================
# app\binnexus\analysis\runtime\collector.py

import json
from pathlib import Path
import subprocess

from app.binnexus.utils.logging import app_logger

RUNTIME_DIR = Path(__file__).resolve().parents[2] / "runtime"

RUNTIME_EXE = RUNTIME_DIR / "runtime_dump.exe"
app_logger.debug(f"[runtime] exe path: {RUNTIME_EXE}")

SYSTEM_DLL_PREFIXES = (
    "c:\\windows\\",
    "c:\\windows\\system32\\",
    "c:\\windows\\syswow64\\",
)

INTERNAL_BINNEXUS = (
    "dll_loader.exe",
    "runtime_dump.exe",
)

def is_valid_runtime_module(path: str, config) -> bool:
    p = path.lower()

    # убираем свои тулзы
    if any(x in p for x in INTERNAL_BINNEXUS):
        return False

    return True

def collect_runtime_modules(file: Path, config) -> list[str]:
    if not RUNTIME_EXE.exists():
        raise RuntimeError(f"runtime_dump.exe not found: {RUNTIME_EXE}")

    cmd = [str(RUNTIME_EXE), str(file)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=config.runtime_timeout / 1000
        )
    except subprocess.TimeoutExpired:
        app_logger.error(f"[runtime] timeout: {file}")
        return []

    if result.returncode != 0:
        app_logger.error(
            f"[runtime] failed ({result.returncode}): {file}\n"
            f"stderr: {result.stderr.strip()}"
        )
        return []

    output = result.stdout.strip()

    if not output:
        return []

    try:
        modules = json.loads(output)
    except Exception as e:
        app_logger.error(f"[runtime] json parse error: {e}")
        app_logger.debug(f"[runtime] raw output:\n{output}")
        return []

    # нормализуем пути
    normalized = []
    for m in modules:
        try:
            normalized.append(Path(m).name.lower())
        except Exception:
            continue

    return normalized

def collect_runtime_for_files(files: list[Path], graph, config):
    if not config.runtime:
        app_logger.debug("[runtime] skipped (disabled)")
        return

    runtime_files: list[Path] = []

    for file in files:
        suffix = file.suffix.lower()

        if config.runtime_mode == "dll" and suffix != ".dll":
            continue

        if config.runtime_mode == "exe" and suffix != ".exe":
            continue

        runtime_files.append(file)

    runtime_files = runtime_files[:config.runtime_limit]

    app_logger.info(
        f"[runtime] files selected: {len(runtime_files)} "
        f"(limit={config.runtime_limit}, mode={config.runtime_mode})"
    )

    if config.runtime_verbose:
        app_logger.info(
            f"[runtime] include_system={config.runtime_include_system}, "
            f"dump={config.runtime_dump}"
        )

    for i, file in enumerate(runtime_files, 1):
        name = file.name.lower()

        app_logger.info(f"[runtime] [{i}/{len(runtime_files)}] {name}")

        try:
            runtime_mods = collect_runtime_modules(file, config)
        except Exception as e:
            app_logger.error(f"[runtime] error: {file} -> {e}")
            continue

        if not runtime_mods:
            if config.runtime_verbose:
                app_logger.info(f"[runtime] no modules: {name}")
            continue

        app_logger.info(f"[runtime] found {len(runtime_mods)} modules in {name}")

        for mod in runtime_mods:
            if mod == name:
                continue

            if not is_valid_runtime_module(mod, config):
                continue

            if not config.runtime_include_system and mod in config.excluded_dlls:
                if config.runtime_verbose:
                    app_logger.info(f"[runtime] skip system: {mod}")
                continue

            key = (name, mod)
            existing = graph.edge_map.get(key)

            if existing:
                # если уже есть static → НЕ добавляем runtime
                if "static" in existing["types"]:
                    app_logger.info(f"[runtime] is static: {mod}")
                    continue

            graph.add_node(mod)
            graph.add_edge(name, mod, "runtime")

            if config.runtime_verbose:
                app_logger.info(f"[runtime] edge: {name} -> {mod}")

        if config.runtime_dump:
            app_logger.info(f"[runtime] raw dump requested for {name} (TODO)")