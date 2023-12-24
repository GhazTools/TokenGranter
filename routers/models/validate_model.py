"""
file_name = validate_model.py
Created On: 2023/12/21
Lasted Updated: 2023/12/21
Description: _FILL OUT HERE_
Edit Log:
2023/12/21
    - Created file
"""

# STANDARD LIBRARY IMPORTS
...

# THIRD PARTY LIBRARY IMPORTS
from pydantic import BaseModel

...

# LOCAL LIBRARY IMPORTS
...


class TokenParam(BaseModel):
    username: str
    password: str
