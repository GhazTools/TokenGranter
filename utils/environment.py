"""
file_name = environment.py
Created On: 2024/07/04
Lasted Updated: 2024/07/04
Description: _FILL OUT HERE_
Edit Log:
2024/07/04
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from enum import Enum
from pathlib import Path
from os import getenv

# THIRD PARTY LIBRARY IMPORTS
from dotenv import load_dotenv

# LOCAL LIBRARY IMPORTS


class EnvironmentVariableKeys(Enum):
    """
    An Enum class to specify the environment variable keys.
    """

    FIRESTORE_TOKEN = "FIRESTORE_TOKEN"
    FIRESTORE_SERVER = "FIRESTORE_SERVER"
    FIRESTORE_DOC_ID = "FIRESTORE_DOC_ID"
    LOGGING_CONFIG_PATH = "LOGGING_CONFIG_PATH"
    REDIS_HOST = "REDIS_HOST"
    REDIS_PORT = "REDIS_PORT"
    REDIS_PASSWORD = "REDIS_PASSWORD"


class Environment:
    """
    A class to handle the environment variables
    """

    is_loaded: bool = False

    @staticmethod
    def load_environment_variables() -> None:
        """
        A method to load the environment variables
        """

        if Environment.is_loaded:
            return

        app_path: Path = Path(__file__).resolve().parents[1]
        env_path = app_path / ".env"

        load_dotenv(dotenv_path=env_path)

        Environment.verify_environment_variables()
        Environment.is_loaded = True

    @staticmethod
    def verify_environment_variables() -> None:
        """
        A method to verify the environment
        """

        missing_keys = []
        for key in EnvironmentVariableKeys:
            key_value = key.value

            if getenv(key_value) is None:
                missing_keys.append(key_value)

        if missing_keys:
            raise ValueError("Missing environment variables:", ", ".join(missing_keys))

    @staticmethod
    def get_environment_variable(key: EnvironmentVariableKeys):
        """
        A method to get the environment variable
        """

        Environment.load_environment_variables()

        return getenv(key.value)
