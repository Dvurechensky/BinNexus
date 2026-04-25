# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 25 апреля 2026 08:09:10
# Version: 1.0.17
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