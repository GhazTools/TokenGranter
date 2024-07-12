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
from fastapi.middleware.cors import CORSMiddleware


# LOCAL LIBRARY IMPORTS
from utils.startup import startup_tasks
from routers.token import ROUTER as token_router

startup_tasks()

app = FastAPI(dependencies=[])
app.include_router(token_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",], 
    allow_credentials=True,  
    allow_methods=["GET", "POST"],  
    allow_headers=["X-Requested-With", "Content-Type", "Authorization"], 
)
