# Сборка & Запуск (Windows)

## Важно

BinNexus использует `dumpbin`, поэтому запуск должен выполняться из (на выбор):

- x86 Native Tools Command Prompt
- x64 Native Tools Command Prompt
- Developer Command Prompt for Visual Studio

---

## Установка

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Запуск

### Правила использования

| Аргумент              | Описание                                                                       |
| --------------------- | ------------------------------------------------------------------------------ |
| `-h, --help`          | Показать справку и выйти                                                       |
| `--input PATH`        | Путь к папке с бинарниками (DLL/EXE) для анализа                               |
| `--output DIR`        | Директория вывода портала (по умолчанию: `build`)                              |
| `--exclude-system`    | Исключить системные DLL Windows (kernel32, user32 и др.)                       |
| `--exclude-crt`       | Исключить библиотеки C/C++ runtime (msvcrt, msvcp, api-ms-win-crt-\*)          |
| `--lang {en,ru}`      | Язык портала (по умолчанию: `en`)                                              |
| `--skip-dirs DIR ...` | Директории, которые нужно пропустить при сканировании (по умолчанию: `legacy`) |
| `--version`           | Показать версию программы и выйти                                              |

### Пример старта

```sh
python static_dependency_graph_create.py ^
  --input "F:\TargetApp" ^
  --output "build" ^
  --exclude-system ^
  --exclude-crt ^
  --skip-dirs plugins temp cache logs
  --lang en
```

---

## Запуск портала

```sh
cd build/portal
python -m http.server 16801
```

Открыть:

```
http://localhost:16801
```

---

## Проверка dumpbin

```sh
dumpbin
```

Если команда не найдена — значит запущена неправильная консоль.

---

## Примечания

> [!TIP]
> Используйте x86 toolchain для старых игр и legacy DLL.

> [!WARNING]
> Не запускайте анализ system32 — это создаст огромное количество шума.

> [!NOTE]
> Рекомендуется исключать директории plugins / legacy для чистоты графа.
