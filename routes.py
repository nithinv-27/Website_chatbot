from fastapi import APIRouter
from pydantic import BaseModel

ml_models = {}

class UserQuery(BaseModel):
    query: str

router = APIRouter()

@router.post("/chatbot")
async def chatbot_response(request: UserQuery):
    user_query = request.query
    res = ml_models["llm"](user_query=user_query)
    return {"content": res}
