from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.board import router as BoardRouter
from .const import const

app = FastAPI()

app.include_router(BoardRouter, tags=["Board"], prefix="/board")
# app.include_router(TaskRouter, tags=["Task"], prefix="/task")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    const.FE_DEV_ORIGIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}