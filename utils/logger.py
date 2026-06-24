# -*- coding: utf-8 -*-

import logging
import os


def setup_logger() -> logging.Logger:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    return logging.getLogger("whatsapp_sender")
