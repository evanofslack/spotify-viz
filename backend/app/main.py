import uvicorn
import tekore as tk
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers import users, auth
from db.database import create_db_and_tables
from config import get_settings, Settings


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.add_middleware(SessionMiddleware, secret_key="yeahyouthought")


origins = [
    'http://localhost',
    'localhost'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def pong(settings: Settings = Depends(get_settings)):
    return {
        "message": "Hello World",
        "environment": settings.environment,
        "testing": settings.testing
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8080, host='0.0.0.0', reload=True,
    )
