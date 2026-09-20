# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 20 сентября 2026 08:40:47
# Version: 1.0.167
# ========================================
# app\binnexus\utils\logging.py

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)

app_logger = logging.getLogger("binnexus")