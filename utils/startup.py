"""
file_name = startup.py
Created On: 2023/12/24
Lasted Updated: 2023/12/24
Description: _FILL OUT HERE_
Edit Log:
2023/12/24
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from os import environ

# THIRD PARTY LIBRARY IMPORTS
from dotenv import load_dotenv

from firebase_admin import (
    _DEFAULT_APP_NAME,
    credentials,
    _apps,
    initialize_app,
)

# LOCAL LIBRARY IMPORTS


def startup_tasks() -> None:
    """
    Function to run all startup tasks
    """

    load_dotenv()

    if _DEFAULT_APP_NAME not in _apps:
        initialize_app(credentials.Certificate(environ["FIRESTORE_TOKEN"]))
