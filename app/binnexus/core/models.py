# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 03 ноября 2026 12:17:17
# Version: 1.0.210
# ========================================
# app\binnexus\core\models.py

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ExportSymbol:
    name: Optional[str]
    undecorated: Optional[str]
    ordinal: int
    address: str
    is_clean: bool

@dataclass
class BinaryFile:
    path: str
    name: str
    type: str  # dll/exe

@dataclass
class Edge:
    source: str
    target: str
    types: set[str]