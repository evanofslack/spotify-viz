import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from connections import redis_cache
from routers import auth, overview, playlists, status

load_dotenv()

app = FastAPI()
app.include_router(auth.router)
app.include_router(status.router)
app.include_router(overview.router)
app.include_router(playlists.router)

app.add_middleware(SessionMiddleware, secret_key=os.environ["SESSION_KEY"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await redis_cache.init_cache()


@app.on_event("shutdown")
async def shutdown():
    redis_cache.close()
    await redis_cache.wait_closed()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8080,
        host="0.0.0.0",
        reload=True,
    )
