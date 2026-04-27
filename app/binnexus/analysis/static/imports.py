# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 27 апреля 2026 09:39:21
# Version: 1.0.20
# ========================================
# app\binnexus\analysis\static\imports.py

from pathlib import Path
import re

from app.binnexus.infra.subprocess import run_dumpbin


dll_pattern = re.compile(r"^\s+([A-Za-z0-9_\-\.]+\.dll)", re.IGNORECASE)

def parse_imports(output):
    imports = set()
    for line in output.splitlines():
        match = dll_pattern.match(line)
        if match:
            imports.add(match.group(1).lower())
    return imports

def get_imports(file: Path) -> set[str]:
    output = run_dumpbin(file)
    return parse_imports(output)