# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 27 апреля 2026 09:39:21
# Version: 1.0.20
# ========================================
# app\binnexus\utils\symbols.py

from ctypes import wintypes
import ctypes

from app.binnexus.analysis.static.constants import BAD_PREFIXES, CRT_FORWARD_EXPORTS, IMAGEHLP_UNDECORATE_COMPLETE, MEMORY_FUNCS, SKIP_NAMES, STRING_FUNCS, WINAPI_STRING_HINTS

def pick_color(clean_count: int) -> str:
    if clean_count >= 20:
        return "#ff4d4f"
    if clean_count >= 10:
        return "#fa8c16"
    if clean_count >= 3:
        return "#fadb14"
    if clean_count >= 1:
        return "#52c41a"
    return "#595959"

def undecorate_symbol(name: str | None) -> str | None:
    if not name:
        return None

    s = name.strip()
    if not s:
        return None

    # Не пытаемся "undecorate" обычные экспортные имена.
    # Для x32dbg-подобного поведения оставляем undecorated
    # только для реально декорированных MSVC/C++ символов.
    is_decorated = (
        s.startswith("?") or
        s.startswith("@") or
        (s.startswith("_") and "@" in s)
    )

    if not is_decorated:
        return None

    try:
        dbghelp = ctypes.WinDLL("dbghelp.dll")
    except Exception:
        return None

    dbghelp.UnDecorateSymbolName.argtypes = [
        wintypes.LPCSTR,
        wintypes.LPSTR,
        wintypes.DWORD,
        wintypes.DWORD,
    ]
    dbghelp.UnDecorateSymbolName.restype = wintypes.DWORD

    input_bytes = s.encode("ascii", errors="ignore")
    output_buf = ctypes.create_string_buffer(8192)

    result_len = dbghelp.UnDecorateSymbolName(
        input_bytes,
        output_buf,
        ctypes.sizeof(output_buf),
        IMAGEHLP_UNDECORATE_COMPLETE,
    )

    if result_len == 0:
        return None

    text = output_buf.value.decode("utf-8", errors="ignore").strip()
    if not text:
        return None

    # Если dbghelp вернул то же самое имя — это неценный undecorated.
    if text == s:
        return None

    return text


def normalize_symbol_name(name: str) -> str:
    return name.strip()

def is_bad_symbol(name: str, forwarder: str | None = None) -> tuple[bool, str | None]:
    if not name:
        return True, "empty"

    s = normalize_symbol_name(name)

    if s in SKIP_NAMES:
        return True, "skip_name"

    if s in CRT_FORWARD_EXPORTS:
        return True, "crt_forward_name"

    if s.lower() in STRING_FUNCS:
        return True, "string_func"

    if s.lower() in MEMORY_FUNCS:
        return True, "memory_func"

    for prefix in BAD_PREFIXES:
        if s.startswith(prefix):
            return True, "code_fragment"

    if s in WINAPI_STRING_HINTS:
        return True, "winapi_forward"

    if forwarder:
        fl = forwarder.lower()
        if fl.startswith("msvcrt.") or fl.startswith("kernel32.") or fl.startswith("user32."):
            return True, "forward_to_system"

    return False, None