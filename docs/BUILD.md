# Build & Run (Windows)

- [Build \& Run (Windows)](#build--run-windows)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Arguments](#arguments)
    - [Example](#example)
  - [Build UI portal](#build-ui-portal)
  - [Running the Portal](#running-the-portal)
  - [Verifying dumpbin](#verifying-dumpbin)
  - [Notes](#notes)

## Requirements

BinNexus relies on `dumpbin`, so it must be executed from one of the following environments:

- x86 Native Tools Command Prompt
- x64 Native Tools Command Prompt
- Developer Command Prompt for Visual Studio

---

## Installation

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### Arguments

| Argument                       | Description                                                           |
| ------------------------------ | --------------------------------------------------------------------- |
| `-h, --help`                   | Show help message and exit                                            |
| `--input PATH`                 | Path to folder containing binaries (DLL/EXE) to analyze               |
| `--output DIR`                 | Output directory for the generated portal (default: `build`)          |
| `--exclude-system`             | Exclude Windows system DLLs (kernel32, user32, etc.)                  |
| `--exclude-crt`                | Exclude C/C++ runtime libraries (msvcrt, msvcp, api-ms-win-crt-\*)    |
| `--lang {en,ru}`               | Portal language (default: `en`)                                       |
| `--skip-dirs DIR...`           | Directories to skip during scanning (default: `legacy`)               |
| `--build-portal`               | Build HTML portal from existing `graph.json` in output directory      |
| `--version`                    | Show program version and exit                                         |
| `--runtime`                    | Enable runtime module analysis via debugger (x32dbg/x64dbg)           |
| `--runtime-include-system`     | Include system DLLs in runtime results (requires `--runtime`)         |
| `--runtime-timeout MS`         | Timeout for runtime analysis per binary (default: `3000` ms)          |
| `--runtime-limit N`            | Maximum number of binaries to analyze in runtime mode (default: `50`) |
| `--runtime-mode {all,dll,exe}` | Which binaries to analyze in runtime (default: `all`)                 |
| `--runtime-dump`               | Save raw runtime module lists for each analyzed binary                |
| `--runtime-verbose`            | Enable verbose logging for runtime analysis                           |

---

### Example

> in root repo

```sh
python -m app.binnexus.cli.main --input "F:\LIZERIUM\LizeriumFreelancerMode" --output "build" --exclude-system --exclude-crt --lang en --skip-dirs plugins --runtime --runtime-limit 100 --runtime-mode all --runtime-timeout 3000 --runtime-verbose --runtime-dump
```

---

## Build UI portal

> in root repo

```sh
python -m app.binnexus.cli.main --build-portal
```

---

## Running the Portal

```sh
cd build/portal
python -m http.server 16801
```

Open in browser:

```
http://localhost:16801
```

---

## Verifying dumpbin

```sh
dumpbin
```

If the command is not recognized, the wrong terminal is being used.

---

## Notes

> [!TIP]
> Use the x86 toolchain for legacy applications and older DLLs.

> [!WARNING]
> Do not scan `system32` — it will generate excessive noise in the graph.

> [!NOTE]
> It is recommended to exclude directories like `plugins` and `legacy` for cleaner results.
