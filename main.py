import uvicorn
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Annotated
from contextlib import asynccontextmanager
from model import generate_response
from fastapi.staticfiles import StaticFiles
from routes import router, ml_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["llm"] = generate_response
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://127.0.0.1:5500",
    "http://0.0.0.0:8000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Serve frontend at "/"
@app.get("/")
async def serve_frontend():
    return {"bru": "uh"}
    return FileResponse("static/dist/index.html")

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)