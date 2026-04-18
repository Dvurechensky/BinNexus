# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 18 апреля 2026 14:42:40
# Version: 1.0.10
# ========================================
# app\binnexus\core\filters.py 


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

WINDOWS_SUBSYSTEM_DLLS = {
    "textinputframework.dll",
    "windows.storage.dll",
    "coremessaging.dll",
    "msctf.dll",
    "wintypes.dll",
    "cryptbase.dll",
    "cryptnet.dll",
    "mmdevapi.dll",
    "riched20.dll",
    "usp10.dll",
}

WINDOWS_INTERNAL_RUNTIME = {
    "kernelbase.dll",   # уже есть
    "win32u.dll",       # syscall bridge
    "gdi32full.dll",    # расширенный gdi
    "combase.dll",      # COM runtime
    "sechost.dll",      # security host
    "bcrypt.dll",       # crypto API
    "winmmbase.dll",    # winmm backend
    "shcore.dll",       # DPI / shell core
    "mswsock.dll",      # winsock extension
    "usp10.dll",        # unicode shaping
}

MODERN_WINDOWS_DLLS = {
    "ucrtbase.dll",
    "msvcp_win.dll",
    "msvcr100.dll",
    "vcruntime140.dll",
    "vcruntime140_1.dll",
    "api-ms-win-core.dll",
    "api-ms-win-core-libraryloader.dll",
    "api-ms-win-core-synch.dll",
    "api-ms-win-core-file.dll",
    "api-ms-win-core-heap.dll",
    "api-ms-win-core-handle.dll",
    "api-ms-win-core-processenvironment.dll",
    "api-ms-win-core-string.dll",
    "api-ms-win-core-errorhandling.dll",
    "api-ms-win-core-localization.dll",
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