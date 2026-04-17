# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 17 апреля 2026 06:50:20
# Version: 1.0.9
# ========================================
# app\binnexus\analysis\static\exports.py

import pefile

from pathlib import Path

from app.binnexus.export.search_index import SEARCH_INDEX
from app.binnexus.utils.symbols import is_bad_symbol, undecorate_symbol


def extract_exports(file_path: Path) -> dict:
    result = {
        "file": file_path.name.lower(),
        "raw_count": 0,
        "clean_count": 0,
        "exports": []
    }

    try:
        pe = pefile.PE(str(file_path))
    except Exception as e:
        result["error"] = str(e)
        return result

    if not hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
        return result

    image_base = pe.OPTIONAL_HEADER.ImageBase

    for sym in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        name = sym.name.decode("utf-8", errors="ignore") if sym.name else None
        forwarder = sym.forwarder.decode("utf-8", errors="ignore") if getattr(sym, "forwarder", None) else None
        undecorated = undecorate_symbol(name) if name else None

        if name:
            SEARCH_INDEX.append({
                "dll": file_path.name.lower(),
                "symbol": name,
                "undec": undecorated,
                "address": f"{image_base + sym.address:08X}",
                "ordinal": sym.ordinal,
            })

        entry = {
            "address": f"{image_base + sym.address:08X}",
            "rva": f"{sym.address:08X}",
            "type": "Export",
            "ordinal": sym.ordinal,
            "symbol": name,
            "symbol_undecorated": undecorated,
            "forwarder": forwarder,
            "is_clean": False,
            "reason": None,
        }

        result["raw_count"] += 1

        if name is None:
            entry["reason"] = "ordinal_only"
        else:
            bad, reason = is_bad_symbol(name, forwarder)
            if bad:
                entry["reason"] = reason
            else:
                entry["is_clean"] = True
                result["clean_count"] += 1

        result["exports"].append(entry)

    result["exports"].sort(
        key=lambda x: (int(x["address"], 16), x["ordinal"])
    )

    return result