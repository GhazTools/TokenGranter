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
from pathlib import Path

# THIRD PARTY LIBRARY IMPORTS
from dotenv import load_dotenv

from firebase_admin import (
    _DEFAULT_APP_NAME,
    credentials,
    _apps,
    initialize_app,
)

# LOCAL LIBRARY IMPORTS
from utils.environment import Environment, EnvironmentVariableKeys


def startup_tasks() -> None:
    """
    Function to run all startup tasks
    """

    app_path: Path = Path(__file__).resolve().parents[1]
    env_path = app_path
    load_dotenv(dotenv_path=env_path)

    if _DEFAULT_APP_NAME not in _apps:
        initialize_app(
            credentials.Certificate(
                Environment.get_environment_variable(
                    EnvironmentVariableKeys.FIRESTORE_TOKEN
                )
            )
        )
