from fastapi import APIRouter, status
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from services.remote_repo_service import query
from typing import Optional
from typing import Any

class Message(BaseModel):
    question: str
    socket_id: str
    session_id: Optional[str] = None

router = APIRouter()

@router.post("/remote/repo/query", status_code=status.HTTP_200_OK)
async def query_repo(message: Message):
    session_id, response = await query(question=message.question, socket_id=message.socket_id, session_id=message.session_id)
    return JSONResponse(content={"session_id": session_id, "response": response}, status_code=status.HTTP_200_OK)
