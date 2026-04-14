#include <windows.h>
#include <iostream>

int wmain(int argc, wchar_t* argv[])
{
    if (argc < 2)
    {
        std::wcerr << L"Usage: dll_loader.exe <target.dll>\n";
        return 1;
    }

    const wchar_t* dllPath = argv[1];

    HMODULE mod = LoadLibraryW(dllPath);
    if (!mod)
    {
        std::wcerr << L"LoadLibraryW failed: " << GetLastError() << L"\n";
        return 2;
    }

    // Держим процесс живым, чтобы родитель успел снять модульный список
    Sleep(10000);

    FreeLibrary(mod);
    return 0;
}