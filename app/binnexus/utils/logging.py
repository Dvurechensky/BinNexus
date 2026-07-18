# ========================================
# Author: Nikolay Dvurechensky
# Site: https://dvurechensky.pro/
# Gmail: dvurechenskysoft@gmail.com
# Last Updated: 18 июля 2026 07:25:08
# Version: 1.0.103
# ========================================
# app\binnexus\utils\logging.py

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)

app_logger = logging.getLogger("binnexus")