from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Database.db import engine
from sqlmodel import SQLModel
from Routes.user_routes import router
from Routes.booking_routes import booking_router
from Deps.config import settings


app = FastAPI(title="Laundrex✨👗🗑")

app.include_router(router, prefix=settings.API_V1_STR)
app.include_router(booking_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

