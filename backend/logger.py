import logging

from backend.config import (
    LOG_DIR,
    LOG_FILE,
    LOG_LEVEL
)

# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger("EnglishTutor")

# Prevent duplicate handlers if imported multiple times
if not logger.handlers:

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # --------------------------------------
    # File logger
    # --------------------------------------

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # --------------------------------------
    # Console logger
    # --------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    logger.propagate = False