<div align="center">

<div align="center">
<img src="media/logo.png" width="200" />
</div>

<p>
  <strong>Binary Dependency Graph & Export Explorer for Windows (x86)</strong>
</p>

<p>
  <img src="https://shields.dvurechensky.pro/badge/status-active-brightgreen" />
  <img src="https://shields.dvurechensky.pro/badge/platform-windows%20x86-blue" />
  <img src="https://shields.dvurechensky.pro/badge/focus-binary%20analysis-purple" />
  <img src="https://shields.dvurechensky.pro/badge/toolchain-pefile%20%2B%20dumpbin-orange" />
</p>

</div>

---

![BINNEXUS](media/BINNEXUS.gif)

---

<div align="center" style="margin: 20px 0; padding: 10px; background: #1c1917; border-radius: 10px;">

<strong>Language:</strong>

<a href="./README.ru.md">
  🇷🇺 Russian
</a>
|
<span style="color: #F5F752;">
  🇺🇸 English (current)
</span>

</div>

---

BinNexus is a tool for analyzing Windows binaries (DLL / EXE) that generates an **interactive web portal** with a dependency graph and export exploration.

It allows you to move from a set of files to understanding the **structure of the system**.

Live demo:
https://dvurechensky.github.io/Freelancer.Reverse.Runtime/

---

- [Features](#features)
  - [Dependency Graph](#dependency-graph)
  - [Export Explorer](#export-explorer)
  - [Global Search](#global-search)
  - [Noise Filtering](#noise-filtering)
- [How it works](#how-it-works)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Limitations](#limitations)
- [Purpose](#purpose)
- [Notes](#notes)

---

## Features

### Dependency Graph

- visualization of relationships between DLLs and EXEs
- identification of core modules
- fast architecture analysis

### Export Explorer

- export list with addresses
- support for undecorated symbols
- filtering:
  - all
  - reverse

### Global Search

- search by:
  - DLL
  - symbols
  - undecorated names
  - addresses

### Noise Filtering

- excludes:
  - CRT (msvcrt)
  - WinAPI
  - system DLLs
  - forward exports

---

## How it works

1. Scans a directory with DLL / EXE files
2. Extracts:
   - imports (via dumpbin)
   - exports (via pefile)
3. Builds a dependency graph
4. Generates an HTML portal

---

## Quick Start

See 👉 [Build & Run (Windows)](docs/BUILD.md)

---

## Requirements

- Windows
- Visual Studio / Build Tools
- Python 3.10+

---

## Limitations

- static analysis only
- no call graph
- no function logic analysis

---

## Purpose

BinNexus solves the problem of:

> quickly understanding the structure of a binary application before disassembly

---

## Notes

> [!TIP]
> Use x86 Native Tools when working with legacy applications — this ensures correct dumpbin results.

> [!WARNING]
> Running outside Developer Command Prompt will result in missing dumpbin and broken import analysis.

> [!NOTE]
> System DLLs are intentionally excluded to reduce noise and improve graph readability.

---

<h3 align="center">✨Dvurechensky✨</h3>
