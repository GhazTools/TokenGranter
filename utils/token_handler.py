"""
file_name = token_handler.py
Created On: 2023/12/16
Lasted Updated: 2023/12/16
Description: _FILL OUT HERE_
Edit Log:
2023/12/16
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from hashlib import sha256
from os import environ
from typing import TypeAlias
from uuid import uuid4

# THIRD PARTY LIBRARY IMPORTS
from firebase_admin import firestore

# LOCAL LIBRARY IMPORTS
from utils.token_metadata import TokenMetadata
from utils.logger import AppLogger
from utils.redis_client import RedisClient, KeyExpiredError, KeyDoesNotExistError

Token: TypeAlias = str


class TokenHandler:
    """
    TokenHandler class to handle token creation and validation
    """

    def __init__(self) -> None:
        self._redis_client: RedisClient = RedisClient()

    # PROPERTIES START HERE
    # PROPERTIES END HERE

    # PUBLIC METHODS START HERE
    def create_and_register_token(
        self, username: str, password: str, temporary=True
    ) -> Token:
        """
        Create and register a token for the user
        """
        if not self._validate_user(username, password):
            raise ValueError("Invalid username or password")

        return self._generate_and_register_token(username, temporary)

    def validate_token(self, username: str, token: Token) -> dict:
        """
        Validate the token for the user
        """

        token_key = self._get_token_key(username)

        try:
            token_metadata: TokenMetadata = self._redis_client.get(token_key)

            if token_metadata["token"] != token:
                return {"ErrorCode": 1, "ErrorMessage": "Invalid Token"}
        except KeyDoesNotExistError:
            return {"ErrorCode": 1, "ErrorMessage": "Invalid Token"}
        except KeyExpiredError:
            return {"ErrorCode": 2, "ErrorString": "Token Expired"}
        except Exception as e:  # pylint: disable=broad-except
            AppLogger.get_logger().error("ErrorWhileValidatingToken", e)
            return {"ErrorCode": 3, "ErrorString": "Server Uncaught Exception"}

        return {"ErrorCode": 0, "ErrorString": "Successfully Validated"}

    # PUBLIC METHODS END HERE

    # PRIVATE METHODS START HERE
    def _generate_and_register_token(self, username: str, temporary: bool) -> Token:
        token: Token = self._generate_token()

        token_key: str = self._get_token_key(username)

        try:
            token_metadata: TokenMetadata = self._redis_client.get(token_key)
            return token_metadata["token"]
        except Exception as e:  # pylint: disable=broad-except
            AppLogger.get_logger().info(
                "No valid registered key for the user %s. Generating new key with exception:  %s",
                username,
                e,
            )

        metadata: TokenMetadata = TokenMetadata(
            {"token_owner": username, "token": token}
        )

        self._redis_client.save(token_key, metadata, 30 if temporary else None)
        return token

    def _validate_user(self, username: str, password: str) -> bool:
        firestore_client = firestore.client()
        users_ref = firestore_client.collection(environ["FIRESTORE_SERVER"])

        token = users_ref.document(environ["FIRESTORE_DOC_ID"]).get().to_dict()
        if (username and username == token["username"]) and (
            password and password == token["password"]
        ):
            return True

        return False

    def _generate_token(self) -> Token:
        uuid: int = uuid4()
        token: Token = sha256(str(uuid).encode("UTF-8")).hexdigest()

        return token

    def _get_token_key(self, username: str) -> str:
        return f"token_granter_token_{username}"

    # PRIVATE METHODS END HERE


token_handler: TokenHandler = TokenHandler()
