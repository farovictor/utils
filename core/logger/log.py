# -*- coding: utf-8 -*-
from logging import getLevelName
from logging import getLogger
from logging import Logger
from os import getenv
from typing import Optional

from core.logger.constants import LOG_CONFIG


def get_logger(
    name: Optional[str] = None, level: str = getenv("LOGLEVEL", "INFO")
) -> Logger:
    """
    This function retrieves a logger and configure it.
    It reads from env var (LOGLEVEL), if not set uses "INFO" as default.

    Returns:
        (Logger): Logger configured
    """

    if name is not None:
        logger = getLogger(name)
    else:
        logger = getLogger()
    logger.setLevel(getLevelName(level))
    return logger


def logging_reformatting():
    """
    This function reconfigure logging.

    Parameters
    ----------
    format: Optional[str]
        A logging format string. If none, BASIC_LOG_FORMAT will be used.
    """
    from logging import config

    # Apply the custom logging configuration
    config.dictConfig(LOG_CONFIG)
