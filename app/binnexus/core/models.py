# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 30 мая 2026 15:41:06
# Version: 1.0.53
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