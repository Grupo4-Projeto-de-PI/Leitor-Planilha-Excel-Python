from fastapi import FastAPI
from app.controller import router

app = FastAPI()

app.include_router(router)
