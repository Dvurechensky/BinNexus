# Changelog

Все значимые изменения в проекте BinNexus.

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

<strong>Язык:</strong>

<span style="color: #F5F752;">
  🇷🇺 Русский (текущий)
</span>
|
<a href="./CHANGELOG.md">
  🇺🇸 English
</a>

</div>

---

## [1.1.0] — Runtime & Architecture Update

### Added

- Runtime-анализ зависимостей:
  - запуск бинарников через runtime loader
  - сбор списка загруженных модулей
  - интеграция runtime-данных в граф
- CLI параметры:
  - `--runtime`
  - `--runtime-mode`
  - `--runtime-limit`
  - `--runtime-timeout`
  - `--runtime-dump`
  - `--runtime-verbose`
  - `--runtime-include-system`
- Ограничение количества анализируемых файлов в runtime
- Логирование runtime-пайплайна

---

### Changed

- Полная переработка архитектуры проекта:
  - переход от монолитного скрипта к модульной системе
  - разделение на:
    - static analysis
    - runtime analysis
    - graph
    - portal
- Улучшена структура проекта и читаемость кода
- Обновлён CLI (расширенные аргументы)

---

### Notes

- Runtime-анализ находится в экспериментальной стадии
- Основной фокус — x86 окружение
- Поддержка других архитектур будет улучшаться по мере тестирования

---

## [1.0.0] — Initial Release

### Added

- Статический анализ бинарников (DLL / EXE)
- Построение графа зависимостей
- Export Explorer
- HTML-портал
- Фильтрация:
  - системные DLL
  - CRT
- Global Search
