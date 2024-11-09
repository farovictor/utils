# -*- coding: utf-8 -*-
from logging import BASIC_FORMAT
from os import getenv


# Formatter to use on K8S Pods
POD_LOG_FORMAT = "%(filename)s:%(lineno)d %(levelname)s - %(message)s"

# Formatter recommended for debugging process
BASIC_LOG_FORMAT = "[%(asctime)s] %(filename)s:%(lineno)d %(log_color)s%(levelname)s%(reset)s - %(message)s"

# Log level (color) table
LOG_COLORS = {
    "DEBUG": "bold_cyan",
    "INFO": "bold_green",
    "WARNING": "bold_yellow",
    "ERROR": "bold_red",
    "CRITICAL": "bold_purple",
}

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # keeps existing loggers active. Do not remove it.
    "formatters": {
        "regular_format": {
            "()": "colorlog.ColoredFormatter",
            "format": BASIC_LOG_FORMAT,
            "log_colors": LOG_COLORS,
        },
        "pod_format": {
            "format": POD_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "envvar_format": {
            "format": getenv("ENVVAR_LOG_FORMATTER", BASIC_FORMAT),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "regular_format",
        },
        "console_pod": {
            "class": "logging.StreamHandler",
            "formatter": "pod_format",
        },
        "console_envvar": {
            "class": "logging.StreamHandler",
            "formatter": "envvar_format",
        },
    },
    "root": {  # Applies to the root logger, covering all logs
        "level": "INFO",
        "handlers": ["console_envvar"],
    },
    "loggers": {
        # This is the logger intended for debugging processes
        "default": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
        # This is the logger intended for airflow pods
        "airflow.pod": {
            "level": "INFO",
            "handlers": ["console_airflow"],
            "propagate": False,
        },
        # This is a custom logger. It uses the format passed through env var: ENVVAR_LOG_FORMATTER
        "envvar.handler": {
            "level": "INFO",
            "handlers": ["console_envvar"],
            "propagate": False,
        },
    },
}
