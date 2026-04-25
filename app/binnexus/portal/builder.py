# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 25 апреля 2026 08:09:10
# Version: 1.0.17
# ========================================
# app\binnexus\portal\builder.py

import shutil
import json

from app.binnexus.core.config import Config
from app.binnexus.export.search_index import SEARCH_INDEX


class PortalBuilder:

    def __init__(self, config: Config):
        self.config = config

    def build(self, graph):
        self._copy_assets()
        self._write_graph(graph)
        self._write_html()
        self._write_search()

    def _copy_assets(self):
        shutil.copytree(self.config.template_css, self.config.portal_css, dirs_exist_ok=True)
        shutil.copytree(self.config.template_js, self.config.portal_js, dirs_exist_ok=True)
        shutil.copytree(self.config.template_libs, self.config.portal_libs, dirs_exist_ok=True)
        shutil.copytree(self.config.template_img, self.config.portal_img, dirs_exist_ok=True)

    def _write_graph(self, graph):
        data = f"const data = {json.dumps(graph)};"
        (self.config.portal_js / "data.js").write_text(data, encoding="utf-8")

    def _write_search(self):
        with open(self.config.portal_dir / "search_index.json", "w", encoding="utf-8") as f:
            json.dump(SEARCH_INDEX, f, ensure_ascii=False, indent=2)

    def _write_html(self):
        html = self.config.template_html.read_text(encoding="utf-8")
        html = html.replace("__LANG__", self.config.lang)

        (self.config.portal_dir / "index.html").write_text(html, encoding="utf-8")