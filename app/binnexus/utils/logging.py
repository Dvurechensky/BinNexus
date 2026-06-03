# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 03 июня 2026 15:14:28
# Version: 1.0.57
# ========================================
# app\binnexus\utils\logging.py

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)

app_logger = logging.getLogger("binnexus")