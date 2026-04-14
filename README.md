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

<p>
  <a href="https://youtu.be/ZZGMkcnkHlk?si=hh5CeFk8aYkVdbvS" target="_blank" rel="noreferrer"><img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/youtube.svg" width="32" height="32" /></a>
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
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Limitations](#limitations)
  - [Runtime Analysis (experimental)](#runtime-analysis-experimental)
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

1. Scan the directory containing the DLL/EXE
2. Extract:
   - Imports (via dumpbin)
   - Exports (via pefile)
3. Generate a static dependency graph
4. (Optional) Perform runtime analysis
5. Generate an HTML portal

---

## Architecture

Starting with the current version, BinNexus is no longer a monolithic script.

The tool is built as a modular system consisting of individual components:

- `analysis.static` — static analysis (imports / exports)
- `analysis.runtime` — dynamic dependency analysis
- `graph` — graph construction and aggregation
- `portal` — HTML interface generation
- `cli` — argument processing and pipeline management

This allows:

- easy functionality expansion
- adding new analyzers
- control over each processing stage

> [!NOTE]
> The architecture is designed with future expansion in mind (plugins, new analysis engines).

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

- Static analysis depends on dumpbin (x86 Native Tools)
- Runtime analysis is experimental
- Limited architecture support (main focus is x86)
- No call graph
- No function logic analysis

---

### Runtime Analysis (experimental)

BinNexus supports runtime dependency analysis.

This allows you to identify:

- dynamically loaded DLLs
- real dependencies missing from static dependencies
- application behavior at startup

Features:

- binary launch via an auxiliary runtime loader
- collecting a list of loaded modules
- integrating results into a common graph

> [!IMPORTANT]
> Runtime analysis complements static analysis and does not replace it.

> [!WARNING]
> This mode is currently x86-specific and requires testing on other architectures.

[Example](docs/BUILD.md)

---

## Purpose

BinNexus solves the problem of:

> quickly understanding the structure of a binary application before disassembly

And complements it by:

> identifying the actual application dependencies both at the file level and at runtime

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
