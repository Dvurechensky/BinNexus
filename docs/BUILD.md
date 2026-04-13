# Build & Run (Windows)

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

| Argument             | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| `-h, --help`         | Show help message and exit                                         |
| `--input PATH`       | Path to folder containing binaries (DLL/EXE) to analyze            |
| `--output DIR`       | Output directory for the generated portal (default: `build`)       |
| `--exclude-system`   | Exclude Windows system DLLs (kernel32, user32, etc.)               |
| `--exclude-crt`      | Exclude C/C++ runtime libraries (msvcrt, msvcp, api-ms-win-crt-\*) |
| `--lang {en,ru}`     | Portal language (default: `en`)                                    |
| `--skip-dirs DIR...` | Directories to skip during scanning (default: `legacy`)            |
| `--version`          | Show program version and exit                                      |

---

### Example

```sh
python static_dependency_graph_create.py ^
  --input "F:\TargetApp" ^
  --output "build" ^
  --exclude-system ^
  --exclude-crt ^
  --skip-dirs plugins temp cache logs ^
  --lang en
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
