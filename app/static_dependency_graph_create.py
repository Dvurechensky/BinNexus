# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 13 апреля 2026 12:56:43
# Version: 1.0.3
# ========================================
import shutil
import subprocess
import re
from pathlib import Path
import json
import pefile
import ctypes
import argparse
from ctypes import wintypes

parser = argparse.ArgumentParser(
    prog="binnexus",
    description="Static dependency graph generator for Windows binaries (DLL/EXE).",
    epilog="""
Examples:

  binnexus --input F:\\Game --exclude-system --exclude-crt
  binnexus --input . --output build --lang ru
  binnexus --input game --skip-dirs plugins temp cache

"""
)

parser = argparse.ArgumentParser(
    prog="binnexus",
    description="Static dependency graph generator for Windows binaries (DLL/EXE).",
    epilog="""
Examples:

  binnexus --input F:\\Game --exclude-system --exclude-crt
  binnexus --input . --output build --lang ru
  binnexus --input game --skip-dirs plugins temp cache
"""
)

parser.add_argument(
    "--input",
    required=True,
    metavar="PATH",
    help="Path to folder with binaries (DLL/EXE) to scan"
)

parser.add_argument(
    "--output",
    default="build",
    metavar="DIR",
    help="Output directory for generated portal (default: build)"
)

parser.add_argument(
    "--exclude-system",
    action="store_true",
    help="Exclude Windows system DLLs (kernel32, user32, etc.)"
)

parser.add_argument(
    "--exclude-crt",
    action="store_true",
    help="Exclude C/C++ runtime libraries (msvcrt, msvcp, api-ms-win-crt-*)"
)

parser.add_argument(
    "--lang",
    default="en",
    choices=["en", "ru"],
    help="Portal language (default: en)"
)

parser.add_argument(
    "--skip-dirs",
    nargs="*",
    default=["legacy"],
    metavar="DIR",
    help="Directories to skip during scan (default: legacy)"
)

parser.add_argument(
    "--version",
    action="version",
    version="binnexus 1.0"
)

args = parser.parse_args()

ROOT = Path(args.input)
DIR_BUILD = Path(args.output)

if not ROOT.exists():
    parser.error(f"--input path does not exist: {ROOT}")

if not ROOT.is_dir():
    parser.error(f"--input must be a directory: {ROOT}")

files = list(ROOT.rglob("*"))

if not any(f.suffix.lower() in [".dll", ".exe"] for f in files):
    print("WARNING: No DLL or EXE files found in input directory")

try:
    DIR_BUILD.mkdir(parents=True, exist_ok=True)
except Exception as e:
    parser.error(f"Cannot create output directory '{DIR_BUILD}': {e}")

if shutil.which("dumpbin") is None:
    parser.error(
        "dumpbin not found. Run from 'Developer Command Prompt for Visual Studio'."
    )  

if args.lang not in {"en", "ru"}:
    parser.error(f"Unsupported language: {args.lang}")

TEMPLATE_HTML_PATH = Path("template/template.html")
TEMPLATE_CSS_PATH = Path("template/css")
TEMPLATE_LIBS_PATH = Path("template/libs")
TEMPLATE_JS_PATH = Path("template/js")
TEMPLATE_IMG_PATH = Path("template/img")

for path in [
    TEMPLATE_HTML_PATH,
    TEMPLATE_CSS_PATH,
    TEMPLATE_LIBS_PATH,
    TEMPLATE_JS_PATH,
    TEMPLATE_IMG_PATH,
]:
    if not path.exists():
        parser.error(f"Missing template path: {path}")

DIR_PORTAL = Path(DIR_BUILD / "portal")
DIR_LIB_PORTAL = Path(DIR_PORTAL / "libs")
DIR_CSS_PORTAL = Path(DIR_PORTAL / "css")
DIR_JS_PORTAL = Path(DIR_PORTAL / "js")
DIR_IMG_PORTAL = Path(DIR_PORTAL / "img")

DIR_BUILD.mkdir(exist_ok=True)
DIR_PORTAL.mkdir(exist_ok=True)
DIR_LIB_PORTAL.mkdir(exist_ok=True)
DIR_CSS_PORTAL.mkdir(exist_ok=True)
DIR_JS_PORTAL.mkdir(exist_ok=True)
DIR_IMG_PORTAL.mkdir(exist_ok=True)

shutil.copytree(TEMPLATE_CSS_PATH, DIR_CSS_PORTAL, dirs_exist_ok=True)
shutil.copytree(TEMPLATE_LIBS_PATH, DIR_LIB_PORTAL, dirs_exist_ok=True)
shutil.copytree(TEMPLATE_JS_PATH, DIR_JS_PORTAL, dirs_exist_ok=True)
shutil.copytree(TEMPLATE_IMG_PATH, DIR_IMG_PORTAL, dirs_exist_ok=True)

dll_pattern = re.compile(r"^\s+([A-Za-z0-9_\-\.]+\.dll)", re.IGNORECASE)

nodes = set()
edges = []
export_stats = {}
SEARCH_INDEX = []
EXCLUDED_DLLS = set()
SKIP_DIRS = {
    d.strip().lower()
    for d in args.skip_dirs
    if d and d.strip()
}

# CORE WINDOWS SYSTEM DLLS
# Базовые системные библиотеки Windows (ядро API)
# → НЕ имеют отношения к логике приложения
SYSTEM_DLLS = {
    "kernel32.dll",   # базовые системные функции (файлы, память, потоки)
    "user32.dll",     # окна, ввод, сообщения (GUI)
    "ntdll.dll",      # низкоуровневое NT API (ядро Windows)
    "gdi32.dll",      # графика (рисование, шрифты)
    "advapi32.dll",   # безопасность, реестр, сервисы
    "ws2_32.dll",     # Winsock (сетевые сокеты)
    "winmm.dll",      # мультимедиа (звук, таймеры)
    "ole32.dll",      # COM / OLE объекты
    "oleaut32.dll",   # автоматизация COM (VARIANT, BSTR)
    "msvcrt.dll"      # стандартная C runtime (printf, malloc и т.д.)
}

# COMMON WINDOWS LIBRARIES
# Часто используемые WinAPI DLL (UI, shell, утилиты)
# → создают шум, но не несут бизнес-логики
WINDOWS_COMMON_DLLS = {
    "shell32.dll",    # работа с оболочкой Windows (Explorer, пути, shell API)
    "shlwapi.dll",    # вспомогательные функции shell (строки, пути, registry)
    "comdlg32.dll",   # стандартные диалоги (open/save file)
    "comctl32.dll",   # стандартные UI-контролы (кнопки, списки)
    "oleacc.dll",     # accessibility API (для экранных читалок)
    "oledlg.dll",     # OLE диалоги
    "wininet.dll",    # HTTP/FTP через WinAPI
    "imm32.dll",      # Input Method Editor (ввод текста, языки)
    "mpr.dll",        # сетевые ресурсы (network providers)
    "version.dll",    # информация о версии файла
    "msimg32.dll",    # простая графика (альфа-блендинг)
    "msvfw32.dll",    # Video for Windows (старое видео API)
    "avicap32.dll"    # захват видео (webcam и т.п.)
}

# C/C++ RUNTIME (CRT)
# Стандартные библиотеки компилятора
# → НЕ часть логики приложения, просто runtime
CRT_DLLS = {
    "msvcp60.dll",    # C++ runtime (STL, iostream и т.д.) Visual C++ 6.0
    "msvcrt.dll",     # C runtime (printf, malloc)
    "crtdll.dll"      # старый CRT (устаревший)
}

# DIRECTX / INPUT / RENDER
# Графика и ввод (можно оставить или убрать)
# → зависит от цели анализа
DIRECTX_DLLS = {
    "d3d8.dll",       # Direct3D 8 (рендеринг)
    "d3d9.dll",       # Direct3D 9 (рендеринг)
    "ddraw.dll",      # DirectDraw (старый 2D рендер)
    "dinput8.dll"     # DirectInput (клавиатура, мышь, геймпады)
}

# LEGACY / COMPATIBILITY
# Устаревшие библиотеки для совместимости
# → обычно можно игнорировать полностью
LEGACY_DLLS = {
    "unicows.dll"     # Unicode wrapper для Windows 9x (очень старое)
}

# SEMI-SYSTEM / INFRASTRUCTURE DLLS
# Полусистемные библиотеки:
# → могут использоваться игрой
# → но НЕ являются частью её бизнес-логики
# → создают ложные связи в графе
EXTRA_NOISE = {
    "rpcrt4.dll",   # RPC (Remote Procedure Call) — межпроцессное/сетевое взаимодействие Windows
    "wsock32.dll",  # старый Winsock (сетевые сокеты, TCP/UDP)
    "msacm32.dll",  # Audio Compression Manager (обработка/кодирование звука)
    "mfc42.dll",    # Microsoft Foundation Classes (GUI/обёртка над WinAPI, Visual C++)
    "shfolder.dll"  # работа с системными папками (AppData, Program Files и т.д.)
}

# всегда убираем мусор (legacy — почти всегда не нужен)
EXCLUDED_DLLS |= LEGACY_DLLS

if args.exclude_system:
    EXCLUDED_DLLS |= SYSTEM_DLLS | WINDOWS_COMMON_DLLS | EXTRA_NOISE

if args.exclude_crt:
    EXCLUDED_DLLS |= CRT_DLLS

EXPORTS_DIR = Path(DIR_PORTAL) / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

CALLING_CONVENTIONS = {
    "__cdecl", "__stdcall", "__fastcall", "__thiscall", "__vectorcall",
}

SKIP_NAMES = {
    "__SEH_prolog",
    "__SEH_epilog",
    "_except_handler3",
    "_except_handler4_common",
    "__RTC_CheckEsp",
    "__security_check_cookie",
    "__report_gsfailure",
}

BAD_PREFIXES = (
    "if ", "while ", "for ", "switch ", "return ", "goto ", "case ",
)

STRING_FUNCS = {
    "strcmp", "strncmp", "stricmp", "_stricmp", "strlen",
    "strcpy", "strncpy", "strcat", "strncat",
    "lstrcmp", "lstrcmpi", "wsprintf", "sprintf",
}

MEMORY_FUNCS = {
    "memcpy", "memmove", "memset", "memcmp",
}

WINAPI_STRING_HINTS = {
    "CreateFileA", "CreateFileW",
    "LoadLibraryA", "LoadLibraryW",
    "GetModuleHandleA", "GetModuleHandleW",
    "GetProcAddress",
}

CRT_FORWARD_EXPORTS = {
    "stricmp": "msvcrt._stricmp",
    "_stricmp": "msvcrt._stricmp",
    "strcmp": "msvcrt.strcmp",
    "_strcmp": "msvcrt.strcmp",
    "strncmp": "msvcrt.strncmp",
    "_strncmp": "msvcrt.strncmp",
    "strlen": "msvcrt.strlen",
    "_strlen": "msvcrt.strlen",
    "strcpy": "msvcrt.strcpy",
    "_strcpy": "msvcrt.strcpy",
    "strncpy": "msvcrt.strncpy",
    "_strncpy": "msvcrt.strncpy",
    "strcat": "msvcrt.strcat",
    "_strcat": "msvcrt.strcat",
    "strncat": "msvcrt.strncat",
    "_strncat": "msvcrt.strncat",
    "memcpy": "msvcrt.memcpy",
    "_memcpy": "msvcrt.memcpy",
    "memmove": "msvcrt.memmove",
    "_memmove": "msvcrt.memmove",
    "memset": "msvcrt.memset",
    "_memset": "msvcrt.memset",
    "memcmp": "msvcrt.memcmp",
    "_memcmp": "msvcrt.memcmp",
    "malloc": "msvcrt.malloc",
    "_malloc": "msvcrt.malloc",
    "free": "msvcrt.free",
    "_free": "msvcrt.free",
    "realloc": "msvcrt.realloc",
    "_realloc": "msvcrt.realloc",
    "atoi": "msvcrt.atoi",
    "_atoi": "msvcrt.atoi",
    "atol": "msvcrt.atol",
    "_atol": "msvcrt.atol",
    "qsort": "msvcrt.qsort",
    "_qsort": "msvcrt.qsort",
    "bsearch": "msvcrt.bsearch",
    "_bsearch": "msvcrt.bsearch",
}


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

IMAGEHLP_UNDECORATE_COMPLETE = 0x0000

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

def save_exports_report(report: dict) -> None:
    base = EXPORTS_DIR / Path(report["file"]).stem

    json_path = base.with_suffix(".json")
    txt_path = base.with_suffix(".txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    with open(txt_path, "w", encoding="utf-8") as f:
        for item in report["exports"]:
            f.write(f"Address={item['address']}\n")
            f.write(f"Type={item['type']}\n")
            f.write(f"Ordinal={item['ordinal']}\n")

            if item["symbol"]:
                f.write(f"Symbol={item['symbol']}\n")

            if item["symbol_undecorated"]:
                f.write(f"Symbol (undecorated)={item['symbol_undecorated']}\n")

            if item["forwarder"]:
                f.write(f"Forwarder={item['forwarder']}\n")


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

def run_dumpbin(file):
    result = subprocess.run(
        ["dumpbin", "/imports", str(file)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    return result.stdout

def should_skip(file: Path) -> bool:
    return any(part.lower() in SKIP_DIRS for part in file.parts)

def parse_imports(output):
    imports = set()
    for line in output.splitlines():
        match = dll_pattern.match(line)
        if match:
            imports.add(match.group(1).lower())
    return imports


for file in ROOT.rglob("*"):
    if should_skip(file):
        continue   

    if file.suffix.lower() not in [".dll", ".exe"]:
        continue

    name = file.name.lower()
    nodes.add(name)

    # imports
    try:
        output = run_dumpbin(file)
        imports = parse_imports(output)

        for imp in imports:
            if imp in EXCLUDED_DLLS:
                continue

            nodes.add(imp)

            edges.append({
                "source": name,
                "target": imp
            })

    except Exception as e:
        print(f"Error: {file} -> {e}")

    # exports
    try:
        export_report = extract_exports(file)
        save_exports_report(export_report)
        export_stats[name] = {
            "raw_count": export_report["raw_count"],
            "clean_count": export_report["clean_count"],
        }
    except Exception as e:
        print(f"Export error: {file} -> {e}")
        export_stats[name] = {
            "raw_count": 0,
            "clean_count": 0,
        }

# считаем degree
degree_map = {n: 0 for n in nodes}

for e in edges:
    degree_map[e["source"]] += 1
    degree_map[e["target"]] += 1

result = {
    "nodes": [
        {
            "id": n,
            "degree": degree_map[n],
            "export_count": export_stats.get(n, {}).get("clean_count", 0),
            "export_raw_count": export_stats.get(n, {}).get("raw_count", 0),
            "has_api": export_stats.get(n, {}).get("clean_count", 0) > 0,
            "color": pick_color(export_stats.get(n, {}).get("clean_count", 0)),
            "label": f"{n}\n{export_stats.get(n, {}).get('clean_count', 0)} exp",
        }
        for n in nodes
    ],
    "edges": edges
}

with open(DIR_PORTAL / "graph.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print("GRAPH GENERATED")

# грузим шаблон
template_html = TEMPLATE_HTML_PATH.read_text(encoding="utf-8")

# вставляем JSON в js
data_js = f"const data = {json.dumps(result)};"
(DIR_JS_PORTAL / "data.js").write_text(data_js, encoding="utf-8")
html = template_html.replace("__LANG__", args.lang)

with open(DIR_PORTAL / "index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open(DIR_PORTAL / "search_index.json", "w", encoding="utf-8") as f:
    json.dump(SEARCH_INDEX, f, ensure_ascii=False)

print("HTML GENERATED")

