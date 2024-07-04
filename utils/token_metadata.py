"""
file_name = token_metadata.py
Created On: 2023/12/19
Lasted Updated: 2023/12/19
Description: _FILL OUT HERE_
Edit Log:
2023/12/19
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from typing import TypedDict

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS


class TokenMetadata(TypedDict):
    """
    A class to represent the metadata that a token is associated with
    """

    token_owner: str  # Token owner name, firebase username
    token: str  # Token string
