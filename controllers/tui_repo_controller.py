from fastapi import APIRouter, status
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
# from services.repo_service import optimize, discard_changes
# from services.repo_extension_service import query
from services.tui_repo_service import query
from typing import Optional
from typing import Any

class Message(BaseModel):
    question: str
    socket_id: str
    session_id: Optional[str] = None

router = APIRouter()

@router.get("/tui/repo/query", status_code=status.HTTP_200_OK)
async def query_repo(message: Message):
    session_id, response = await query(question=message.question, socket_id=message.socket_id, session_id=message.session_id)
    return JSONResponse(content={"session_id": session_id, "response": response}, status_code=status.HTTP_200_OK)
