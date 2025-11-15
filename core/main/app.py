"""
Main module to run ASGI server with

@PythonVersion: 3.13.6
"""

# 3rd party modules
from fastapi import FastAPI

# local modules
from core.main.endpoints import router

APP = FastAPI()
APP.include_router(router)
