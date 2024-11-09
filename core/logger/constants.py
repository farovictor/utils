# -*- coding: utf-8 -*-
from logging import BASIC_FORMAT
from os import getenv


# Formatter to use on K8S Pods
POD_LOG_FORMAT = "%(filename)s:%(lineno)d %(levelname)s - %(message)s"

# Formatter recommended for debugging process
BASIC_LOG_FORMAT = "[%(asctime)s] %(filename)s:%(lineno)d %(log_color)s%(levelname)s%(reset)s - %(message)s"

# Formatter for thread debugging (dispatchers)
THREAD_LOG_FORMAT = "[%(asctime)s] T-%(thread)d %(filename)s:%(lineno)d %(log_color)s%(levelname)s%(reset)s - %(message)s"

# Formatter for process debugging (dispatchers)
PROCESS_LOG_FORMAT = "[%(asctime)s] P-%(process)d %(filename)s:%(lineno)d %(log_color)s%(levelname)s%(reset)s - %(message)s"

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
        "thread_format": {
            "()": "colorlog.ColoredFormatter",
            "format": THREAD_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": LOG_COLORS,
        },
        "process_format": {
            "()": "colorlog.ColoredFormatter",
            "format": PROCESS_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": LOG_COLORS,
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
        "console_thread": {
            "class": "logging.StreamHandler",
            "formatter": "thread_format",
        },
        "console_process": {
            "class": "logging.StreamHandler",
            "formatter": "process_format",
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
        # This is the logger intended for kubernetes pods
        "pod.handler": {
            "level": "INFO",
            "handlers": ["console_pod"],
            "propagate": False,
        },
        # This is a custom logger. It uses the format passed through env var: ENVVAR_LOG_FORMATTER
        "envvar.handler": {
            "level": "INFO",
            "handlers": ["console_envvar"],
            "propagate": False,
        },
        "thread.handler": {
            "level": "INFO",
            "handlers": ["console_thread"],
            "propagate": False,
        },
        "process.handler": {
            "level": "INFO",
            "handlers": ["console_process"],
            "propagate": False,
        },
    },
}
