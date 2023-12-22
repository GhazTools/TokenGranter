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
from typing import Final, TypeAlias
from os import environ

...

# THIRD PARTY LIBRARY IMPORTS
from firebase_admin import credentials, firestore, initialize_app, _DEFAULT_APP_NAME, _apps
from hashlib import sha256
from uuid import uuid4

...

# LOCAL LIBRARY IMPORTS
from utils.token_metadata import TokenMetadata

...

# Initialize firebase before continuing if not created already
if not _DEFAULT_APP_NAME in _apps:
    CREDENTIALS = credentials.Certificate(environ["FIRESTORE_TOKEN"])
    initialize_app(CREDENTIALS)

Token: TypeAlias = str

class TokenHandler:
    # TODO: Create app config file
    token_duration: Final[int] = 3600

    def __init__(self) -> None:
        self.tokens: Dict[Token, TokenMetadata] = {}

    # PROPERTIES START HERE
    # PROPERTIES END HERE

    # PUBLIC METHODS START HERE
    def create_and_register_tokeN(
        self, username: str, password: str, temporary=True
    ) -> Token:
        if not self._validate_user(username, password):
            raise ValueError("Invalid username or password")

        return self._generate_and_register_token(username)

    def validate_token(self, username: str, token: Token) -> dict:
        if not token in self.tokens:
            return {"ErrorCode": 1, "ErrorMessage": "Invalid Token"}

        token_metadata: Final[TokenMetadata] = self.tokens[token]

        if token_metadata.token_owner == username:
            return {"ErrorCode": 1, "ErrorString": "Invalid Token"}

        current_time: Final[datetime] = datetime.now()

        if current_time > token_metadata.expires_on:
            del self.tokens[token]

            return {"ErrorCode": 2, "ErrorString": "Token Expired"}

        return {"ErrorCode": 0, "ErrorString": "Successfully Validated"}

    # PUBLIC METHODS END HERE

    # PRIVATE METHODS START HERE
    def _generate_and_register_token(self, username: str) -> Token:
        token: Token = None
        valid_token: bool = False

        # Generate till we obtain a unique token
        while not valid_token:
            uuid: int = uuid4()
            token: Token = sha256(str(uuid).encode("UTF-8")).hexdigest()

            if not token in self.tokens.keys():
                valid_token = True

        created_on: datetime = datetime.now()
        expires_on: datetime = created_on + timedelta(seconds=self.token_duration)

        metadata: TokenMetadata = TokenMetadata(
            {
                "token_owner": username,
                "created_on": created_on,
                "expires_on": expires_on,
            }
        )

        # Register token
        self.tokens[token] = metadata
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

    # PRIVATE METHODS END HERE

token_handler: TokenHandler = TokenHandler()
    
