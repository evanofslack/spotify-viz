import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers import users, auth, data
from db.database import init_db
from config import get_settings, Settings


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(data.router)

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
async def on_startup():
    await init_db()


@app.get("/")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "message": "Hello World",
        "environment": settings.environment,
        "testing": settings.testing
    }


@app.get("/react")
async def test_react():
    return {"message": "hello"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8080, host='0.0.0.0', reload=True,
    )
