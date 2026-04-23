# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 23 апреля 2026 06:50:21
# Version: 1.0.15
# ========================================
# app\binnexus\core\config.py

from dataclasses import dataclass
from pathlib import Path

from app.binnexus.core.filters import CRT_DLLS, EXTRA_NOISE, LEGACY_DLLS, MODERN_WINDOWS_DLLS, SYSTEM_DLLS, WINDOWS_COMMON_DLLS, WINDOWS_INTERNAL_RUNTIME, WINDOWS_SUBSYSTEM_DLLS


@dataclass
class Config:
    input: Path
    output: Path
    exclude_system: bool
    exclude_crt: bool
    lang: str
    skip_dirs: set[str]

    runtime: bool
    runtime_limit: int
    runtime_mode: str
    runtime_timeout: int
    runtime_dump: bool
    runtime_verbose: bool
    runtime_include_system: bool

    #  derived 
    root: Path = None
    portal_dir: Path = None
    exports_dir: Path = None

    graph_path: Path = None

    template_html: Path = None
    template_css: Path = None
    template_js: Path = None
    template_libs: Path = None
    template_img: Path = None

    portal_css: Path = None
    portal_js: Path = None
    portal_libs: Path = None
    portal_img: Path = None

    excluded_dlls: set[str] = None

    def __post_init__(self):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        templates = BASE_DIR / "template"

        # base 
        self.root = self.input
        self.portal_dir = self.output / "portal"
        self.exports_dir = self.portal_dir / "exports"
        self.graph_path = self.portal_dir / "graph.json"

        # templates 
        self.template_html = templates / "template.html"
        self.template_css = templates / "css"
        self.template_js = templates / "js"
        self.template_libs = templates / "libs"
        self.template_img = templates / "img"

        # portal dirs 
        self.portal_css = self.portal_dir / "css"
        self.portal_js = self.portal_dir / "js"
        self.portal_libs = self.portal_dir / "libs"
        self.portal_img = self.portal_dir / "img"

        # filters 
        self.excluded_dlls = self._build_excluded_set()
        self.skip_dirs = self._build_skip_dirs()

        #  create dirs 
        self._ensure_dirs()

    def _build_excluded_set(self) -> set[str]:
        EXCLUDED_DLLS = set()

        # всегда убираем мусор (legacy — почти всегда не нужен)
        EXCLUDED_DLLS |= LEGACY_DLLS

        if self.exclude_system:
            EXCLUDED_DLLS |= SYSTEM_DLLS | WINDOWS_COMMON_DLLS | EXTRA_NOISE | MODERN_WINDOWS_DLLS | WINDOWS_SUBSYSTEM_DLLS | WINDOWS_INTERNAL_RUNTIME

        if self.exclude_crt:
            EXCLUDED_DLLS |= CRT_DLLS

        return EXCLUDED_DLLS

    def _build_skip_dirs(self) -> set[str]:
        SKIP_DIRS = {
            d.strip().lower()
            for d in self.skip_dirs
            if d and d.strip()
        }
        return SKIP_DIRS

    def _ensure_dirs(self):
        self.output.mkdir(parents=True, exist_ok=True)
        self.portal_dir.mkdir(exist_ok=True)
        self.exports_dir.mkdir(exist_ok=True)

        self.portal_css.mkdir(exist_ok=True)
        self.portal_js.mkdir(exist_ok=True)
        self.portal_libs.mkdir(exist_ok=True)
        self.portal_img.mkdir(exist_ok=True)

    def validate(self):
        state = True
        for path in [
            self.template_html,
            self.template_css,
            self.template_js,
            self.template_libs,
            self.template_img,
        ]:
            if not path.exists():
                print(f"Missing template path: {path}")
                state = False
        return state

