"""
file_name = logging_setup.py
Created On: 2023/12/24
Lasted Updated: 2023/12/24
Description: _FILL OUT HERE_
Edit Log:
2023/12/24
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from os import environ

...

# THIRD PARTY LIBRARY IMPORTS
import logging.config
from fastapi import FastAPI

...

# LOCAL LIBRARY IMPORTS
...


def setupLogger(app: FastAPI) -> None:
    logging.config.fileConfig(environ["LOGGING_CONFIG_PATH"])
    app.logger = logging.getLogger("MainLogger")

    handler = logging.handlers.TimedRotatingFileHandler("logs/app.log", when="midnight")
    handler.prefix = "%Y%m%d"

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(pathname)s | \
            %(levelname)-8s | %(filename)s-%(funcName)s-%(lineno)04d | \
            %(message)s"
    )

    handler.setFormatter(formatter)
