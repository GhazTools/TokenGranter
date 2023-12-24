"""
file_name = token.py
Created On: 2023/12/21
Lasted Updated: 2023/12/21
Description: _FILL OUT HERE_
Edit Log:
2023/12/21
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from typing import Final

...

# THIRD PARTY LIBRARY IMPORTS
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

...

# LOCAL LIBRARY IMPORTS
from utils.token_handler import token_handler
from routers.models.grant_model import GrantParam
from routers.models.validate_model import TokenParam

...

ROUTER: Final[APIRouter] = APIRouter(
    prefix="/token",
    tags=["token"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ROUTER.get("/")
async def home():
    return {"status": "App is running"}


@ROUTER.post("/grant")
async def grant(paramters: GrantParam):
    return token_handler.create_and_register_tokeN(
        paramters.username, paramters.password, paramters.temporary
    )


@ROUTER.post("/validate")
async def validate(parameters: TokenParam):
    return token_handler.validate_token(parameters.username, parameters.password)
