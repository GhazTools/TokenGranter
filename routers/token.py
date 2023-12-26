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
from json import dumps
...

# THIRD PARTY LIBRARY IMPORTS
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

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
    return JSONResponse(
        content=jsonable_encoder(
            {
                "token": token_handler.create_and_register_token(
                    paramters.username, paramters.password, paramters.temporary
                )
            }
        ),
        status_code=status.HTTP_201_CREATED,
    )


@ROUTER.post("/validate")
async def validate(parameters: TokenParam):
    return JSONResponse(
        content=jsonable_encoder(
            token_handler.validate_token(parameters.username, parameters.token)
        ),
        status_code=status.HTTP_201_CREATED,
    )
