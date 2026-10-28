"""Logging configuration for the Local AI Platform."""

import copy
import logging
import logging.config
from pathlib import Path
from typing import Any

from local_ai_platform.config import APP_NAME

LOG_FILE_PATH = Path("logs/local_ai_platform.log")

DEFAULT_LOG_LEVEL = logging.DEBUG

logging_config: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(levelname)-8s] %(message)s",
        },
        "standard": {
            "format": (
                "[%(asctime)s.%(msecs)03d] "
                "[%(levelname)-8s] "
                "[%(name)s:%(lineno)d] - "
                "%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": (
                "[%(asctime)s.%(msecs)03d] "
                "[%(levelname)-8s] "
                "[%(name)s:%(lineno)d] "
                "[%(funcName)s] - "
                "%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": logging.INFO,
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": logging.DEBUG,
            "formatter": "detailed",
            "filename": str(LOG_FILE_PATH),
            "maxBytes": 5_000_000,
            "backupCount": 3,
            "encoding": "utf-8",
        },
    },
    "root": {
        "level": logging.DEBUG,
        "handlers": ["console", "file"],
    },
}


def configure_logging(log_level: int = DEFAULT_LOG_LEVEL) -> None:
    """
    Configure the logging settings for the application.

    Args:
        log_level: The logging level to set. Defaults to DEFAULT_LOG_LEVEL.

    Returns:
        None
    """
    LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    config = copy.deepcopy(logging_config)
    config["root"]["level"] = log_level

    logging.config.dictConfig(config)


def get_logger(component: str) -> logging.Logger:
    """Get a logger for a specific application component."""
    name = f"{APP_NAME}.{component}" if component else APP_NAME
    return logging.getLogger(name)
