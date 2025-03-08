from fastapi import APIRouter
from pydantic import BaseModel
from model import generate_response

class UserQuery(BaseModel):
    query: str

router = APIRouter()

@router.post("/chatbot")
async def chatbot_response(request: UserQuery):
    user_query = request.query
    res = generate_response(user_query=user_query)
    return res
