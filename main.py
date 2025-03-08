import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import router

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://127.0.0.1:5500",
    "http://0.0.0.0:8000",
    "http://localhost:8080",
    "http://localhost:8000",
    "https://websitechatbot-production.up.railway.app"
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

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)