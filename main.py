"""
file_name = main.py
Created On: 2023/12/16
Lasted Updated: 2023/12/16
Description: _FILL OUT HERE_
Edit Log:
2023/12/16
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from fastapi import FastAPI


# LOCAL LIBRARY IMPORTS
from utils.startup import startupTasks
from routers.token import ROUTER as token_router


startupTasks()

app = FastAPI(dependencies=[])
app.include_router(token_router)
