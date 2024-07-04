"""
file_name = logger.py
Created On: 2024/02/29
Lasted Updated: 2024/02/29
Description: _FILL OUT HERE_
Edit Log:
2024/02/29
    - Created file
"""

# THIRD PARTY LIBRARY IMPORTS
import logging.config
from pathlib import Path
from typing import cast

# STANDARD LIBRARY IMPORTS
from enum import Enum
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Formatter, Logger
from logging.handlers import TimedRotatingFileHandler

# LOCAL LIBRARY IMPORTS


class LoggingLevel(Enum):
    """
    A class used to create a logging level
    """

    NOT_SET = NOTSET
    DEBUG = DEBUG
    INFO = INFO
    WARNING = WARNING
    ERROR = ERROR
    CRITICAL = CRITICAL


class AppLogger:
    """
    A class used to create a logger for the application
    """

    __is_logging_setup: bool = False
    __logger: Logger | None = None

    @staticmethod
    def add_handler(app_path: Path, logger: Logger) -> None:
        """
        A method used to add a handler to the logger
        """
        logging_directory_path: Path = app_path / "logs"

        # Create the directory if it does not exist
        logging_directory_path.mkdir(parents=True, exist_ok=True)

        handler: TimedRotatingFileHandler = logging.handlers.TimedRotatingFileHandler(
            logging_directory_path / "token_granter.log", when="midnight"
        )

        handler.suffix = "%m_%d_%Y"
        formatter: Formatter = Formatter(
            fmt="%(asctime)s | %(pathname)s | \
            %(levelname)-8s | %(filename)s-%(funcName)s-%(lineno)04d | \
            %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @staticmethod
    def logging_setup(logging_level=LoggingLevel.INFO) -> None:
        """
        A method used to setup the logging for the application
        """
        if AppLogger.__is_logging_setup:
            return

        app_path: Path = Path(__file__).resolve().parents[1]
        logging.config.fileConfig(app_path / "logging.conf")

        logger: Logger = logging.getLogger("TokenGranter")

        AppLogger.__logger = logger
        AppLogger.add_handler(app_path, logger)
        logger.setLevel(level=logging_level.value)

        AppLogger.__is_logging_setup = True

    @staticmethod
    def get_logger() -> Logger:
        """
        A method used to get the logger
        """

        AppLogger.logging_setup()
        return cast(Logger, AppLogger.__logger)
