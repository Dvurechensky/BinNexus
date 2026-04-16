# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 16 апреля 2026 11:41:56
# Version: 1.0.8
# ========================================
# app\binnexus\analysis\static\constants.py

IMAGEHLP_UNDECORATE_COMPLETE = 0x0000

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
