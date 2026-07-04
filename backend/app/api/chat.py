from pydantic import BaseModel
from fastapi import APIRouter

from app.ai.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

service = ChatService()


class ChatRequest(BaseModel):
    message: str


@router.post("")
async def chat(request: ChatRequest):

    response = await service.chat(request.message)

    return {"response": response}
