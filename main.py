from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from model import classify_intent, generate_response, intents, BASE_URL

app = FastAPI()

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

    # Classify intent
    intent = classify_intent(user_query)

    if intent:
        # Generate AI response
        ai_response = generate_response(intent)
        response_data = {
            "intent": intent,
            "response": ai_response,
            "link": intents[intent]["link"]
        }
        return response_data
    else:
        return {"intent": "None", "response": "I'm not sure how to help with that."}
