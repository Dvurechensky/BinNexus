// runtime_dump.cpp

#include <windows.h>
#include <psapi.h>

#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>

#pragma comment(lib, "psapi.lib")

std::wstring ToWide(const std::string& s)
{
    if (s.empty())
        return L"";

    int len = MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, nullptr, 0);
    if (len <= 0)
        return L"";

    std::wstring out(len, L'\0'); // важно len, не len-1

    MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, &out[0], len);

    out.resize(len - 1); // убрать \0
    return out;
}

std::string ToUtf8(const std::wstring& s)
{
    if (s.empty())
        return "";

    int len = WideCharToMultiByte(CP_UTF8, 0, s.c_str(), -1, nullptr, 0, nullptr, nullptr);
    if (len <= 0)
        return "";

    std::string out(len, '\0');

    WideCharToMultiByte(CP_UTF8, 0, s.c_str(), -1, &out[0], len, nullptr, nullptr);

    out.resize(len - 1);
    return out;
}

static std::wstring GetExtensionLower(const std::wstring& path)
{
    size_t pos = path.find_last_of(L'.');
    if (pos == std::wstring::npos)
        return L"";

    std::wstring ext = path.substr(pos);
    std::transform(ext.begin(), ext.end(), ext.begin(), ::towlower);
    return ext;
}

static std::string EscapeJson(const std::string& s)
{
    std::ostringstream oss;
    for (unsigned char c : s)
    {
        switch (c)
        {
        case '\"': oss << "\\\""; break;
        case '\\': oss << "\\\\"; break;
        case '\b': oss << "\\b"; break;
        case '\f': oss << "\\f"; break;
        case '\n': oss << "\\n"; break;
        case '\r': oss << "\\r"; break;
        case '\t': oss << "\\t"; break;
        default:
            if (c < 0x20)
            {
                char buf[8];
                sprintf_s(buf, "\\u%04x", c);
                oss << buf;
            }
            else
            {
                oss << c;
            }
        }
    }
    return oss.str();
}

static bool StartProcess(const std::wstring& application,
                         std::wstring commandLine,
                         const std::wstring& workingDir,
                         PROCESS_INFORMATION& pi)
{
    STARTUPINFOW si = {};
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    std::vector<wchar_t> cmd(commandLine.begin(), commandLine.end());
    cmd.push_back(L'\0');

    return !!CreateProcessW(
        application.c_str(),
        cmd.data(),
        nullptr,
        nullptr,
        FALSE,
        0,
        nullptr,
        workingDir.c_str(), 
        &si,
        &pi
    );
}

std::wstring GetDirectory(const std::wstring& path)
{
    size_t pos = path.find_last_of(L"\\/");
    if (pos == std::wstring::npos)
        return L".";
    return path.substr(0, pos);
}

static bool EnumerateModules(HANDLE hProcess, std::vector<std::wstring>& outModules)
{
    HMODULE modules[2048] = {};
    DWORD cbNeeded = 0;

    if (!EnumProcessModules(hProcess, modules, sizeof(modules), &cbNeeded))
        return false;

    DWORD count = cbNeeded / sizeof(HMODULE);
    for (DWORD i = 0; i < count; ++i)
    {
        wchar_t path[MAX_PATH] = {};
        if (GetModuleFileNameExW(hProcess, modules[i], path, MAX_PATH))
            outModules.push_back(path);
    }

    return true;
}

int wmain(int argc, wchar_t* argv[])
{
    if (argc < 2)
    {
        std::wcerr << L"Usage: runtime_dump.exe <target.exe|target.dll>\n";
        return 1;
    }

    std::wstring target = argv[1];
    std::wstring ext = GetExtensionLower(target);

    PROCESS_INFORMATION pi = {};
    bool started = false;
    std::wstring workDir = GetDirectory(target);

    if (ext == L".exe")
    {
        std::wstring cmd = L"\"" + target + L"\"";

        started = StartProcess(target, cmd, workDir, pi);
    }
    else if (ext == L".dll")
    {
        // loader должен лежать рядом с runtime_dump.exe
        wchar_t selfPath[MAX_PATH] = {};
        GetModuleFileNameW(nullptr, selfPath, MAX_PATH);

        std::wstring loaderPath = selfPath;
        size_t slash = loaderPath.find_last_of(L"\\/");
        if (slash != std::wstring::npos)
            loaderPath = loaderPath.substr(0, slash + 1);
        loaderPath += L"dll_loader.exe";

        std::wstring cmd = L"\"" + loaderPath + L"\" \"" + target + L"\"";

        started = StartProcess(loaderPath, cmd, workDir, pi);
    }
    else
    {
        std::wcerr << L"Unsupported file type\n";
        return 2;
    }

    if (!started)
    {
        std::wcerr << L"CreateProcessW failed: " << GetLastError() << L"\n";
        return 3;
    }

    Sleep(1200);

    std::vector<std::wstring> modules;
    if (!EnumerateModules(pi.hProcess, modules))
    {
        std::wcerr << L"EnumProcessModules failed: " << GetLastError() << L"\n";
        TerminateProcess(pi.hProcess, 0);
        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
        return 4;
    }

    std::cout << "[\n";
    for (size_t i = 0; i < modules.size(); ++i)
    {
        std::string utf8 = ToUtf8(modules[i]);
        std::cout << "  \"" << EscapeJson(utf8) << "\"";
        if (i + 1 < modules.size())
            std::cout << ",";
        std::cout << "\n";
    }
    std::cout << "]\n";

    TerminateProcess(pi.hProcess, 0);
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return 0;
}