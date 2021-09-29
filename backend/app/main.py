import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

from routers import users, auth, status, overview, playlists
from db.database import init_db


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(status.router)
app.include_router(overview.router)
app.include_router(playlists.router)

load_dotenv()

app.add_middleware(SessionMiddleware,
                   secret_key=os.environ["SESSION_KEY"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost', 'localhost'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def on_startup():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8080, host='0.0.0.0', reload=True,
    )
