import uvicorn
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from contextlib import asynccontextmanager
from model import generate_response
from fastapi.staticfiles import StaticFiles

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["llm"] = generate_response
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

# Serve frontend (Vite build) as static files
app.mount("/", StaticFiles(directory="static/dist", html=True), name="static")

class UserQuery(BaseModel):
    query:str

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://127.0.0.1:5500",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"succ":"ess"}

@app.post("/chatbot")
async def chatbot_response(request: Annotated[UserQuery, Form()]):
    user_query = request.query
    res = ml_models["llm"](user_query=user_query)
    return res


if __name__ == "__main__":
    logging.debug('Starting backend......')
    uvicorn.run(app=app, host="0.0.0.0", port=8000)