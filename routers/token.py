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

# THIRD PARTY LIBRARY IMPORTS
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# LOCAL LIBRARY IMPORTS
from utils.token_handler import token_handler
from routers.models.grant_model import GrantParam
from routers.models.validate_model import TokenParam
from utils.logger import AppLogger

ROUTER: Final[APIRouter] = APIRouter(
    prefix="/token",
    tags=["token"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@ROUTER.get("/")
async def home():
    """
    Function to check if the app is running.
    """

    return {"status": "App is running"}


@ROUTER.post("/grant")
async def grant(paramters: GrantParam):
    """
    Function to grant a token to the user
    """

    AppLogger.get_logger().info(
        "Recieved grant token request for user: %s", paramters.username
    )

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
    """
    Function to validate the token for the user
    """
    AppLogger.get_logger().info(
        "Recieved validate token request for user: %s", parameters.username
    )

    return JSONResponse(
        content=jsonable_encoder(
            token_handler.validate_token(parameters.username, parameters.token)
        ),
        status_code=status.HTTP_201_CREATED,
    )
