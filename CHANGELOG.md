# Changelog

All notable changes to the BinNexus project.

---

- [Changelog](#changelog)
  - [\[1.1.0\] — Runtime \& Architecture Update](#110--runtime--architecture-update)
    - [Added](#added)
    - [Changed](#changed)
    - [Notes](#notes)
  - [\[1.0.0\] — Initial Release](#100--initial-release)
    - [Added](#added-1)

---

<div align="center" style="margin: 20px 0; padding: 10px; background: #1c1917; border-radius: 10px;">

<strong>Language:</strong>

<a href="./CHANGELOG.ru.md">
  🇷🇺 Russian
</a>
|
<span style="color: #F5F752;">
  🇺🇸 English (current)
</span>

</div>

---

## [1.1.0] — Runtime & Architecture Update

### Added

- Runtime dependency analysis:
  - executing binaries via runtime loader
  - collecting loaded module lists
  - integrating runtime data into the graph
- CLI options:
  - `--runtime`
  - `--runtime-mode`
  - `--runtime-limit`
  - `--runtime-timeout`
  - `--runtime-dump`
  - `--runtime-verbose`
  - `--runtime-include-system`
- Limit for number of binaries analyzed in runtime mode
- Runtime pipeline logging

---

### Changed

- Complete architecture redesign:
  - migrated from a monolithic script to a modular system
  - separated into:
    - static analysis
    - runtime analysis
    - graph
    - portal
- Improved project structure and code readability
- Updated CLI (extended arguments)

---

### Notes

- Runtime analysis is currently experimental
- Primary focus is x86 environment
- Support for other architectures will be improved over time

---

## [1.0.0] — Initial Release

### Added

- Static analysis of Windows binaries (DLL / EXE)
- Dependency graph generation
- Export Explorer
- HTML portal
- Filtering:
  - system DLLs
  - CRT
- Global Search
