#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
from datetime import datetime

from configs.defaults import LOG_ROOT


class StampedPath(object):
    """
    A class to stamp timestamp with actual file path.
    """
    timestamp = datetime.now().strftime("%m-%d-%H-%M-%S")

    @staticmethod
    def stamp(dir_path, filename):
        """
        Insert a timestamp between directory part and filename part of an actual 
        path.
        :param dir_path: directory path.
        :param filename: filename.
        :return: a path stamped with timestamp.
        """
        return os.path.join(
            dir_path, StampedPath.timestamp + "_" + filename)


def _check_log_dir(log_root_dir):
    """
    Ensure that the directory storing log exists.
    :param log_root_dir: directory to be checked
    :return:
    """
    if not os.path.exists(log_root_dir):
        os.makedirs(log_root_dir)
    return os.path.exists(log_root_dir)


class LoggerConfig(object):
    log_root = os.path.join(LOG_ROOT, StampedPath.timestamp)
    has_log_root = _check_log_dir(log_root)

    config = {
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "DEBUG"
            },
            "default_debug": {
                "class": "logging.FileHandler",
                "filename": StampedPath.stamp(log_root, "debug.log"),
                "formatter": "default",
                "level": "DEBUG"
            },
            "default_error": {
                "class": "logging.FileHandler",
                "filename": StampedPath.stamp(log_root, "error.log"),
                "formatter": "default",
                "level": "ERROR"
            },
            "default_warning": {
                "class": "logging.FileHandler",
                "filename": StampedPath.stamp(log_root, "warning.log"),
                "formatter": "default",
                "level": "WARNING"
            },
            "default_info": {
                "class": "logging.FileHandler",
                "filename": StampedPath.stamp(log_root, "info.log"),
                "formatter": "default",
                "level": "INFO"
            },
            "test_file": {
                "class": "logging.FileHandler",
                "filename": StampedPath.stamp(log_root, "test.log"),
                "formatter": "default",
                "level": "DEBUG"
            },
            "debug_info": {
                "class": "logging.FileHandler",
                "filename": StampedPath.stamp(log_root, "debug_info.log"),
                "formatter": "default",
                "level": "DEBUG"
            },
        },
        "loggers": {
            "flowcog": {
                "handlers": [
                    "console",
                    "default_info",
                    "default_error",
                    "default_warning",
                    "default_debug"
                ],
                "level": "INFO"
            },
            "flowcog.test": {
                "handlers": [
                    "console",
                    "test_file"
                ],
                "level": "DEBUG",
            },
            "debug_info": {
                "handlers": [
                    "console",
                    "debug_info"
                ],
                "level": "DEBUG",
            }
        },
        "root": {
            "handlers": [
                "console",
                "default_info",
                "default_error",
                "default_debug"
            ],
            "level": "DEBUG"
        },
        "version": 1
    }
