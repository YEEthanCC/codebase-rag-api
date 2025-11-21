from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.repo_service import query, optimize
from typing import Optional
from typing import Any

router = APIRouter()

@router.get("/repo/query", status_code=status.HTTP_200_OK)
async def query_repo(question: str, repo_path: str, session_id: str):
    response = await query(question, repo_path, session_id)
    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)

@router.post("/repo/optimize", status_code=status.HTTP_200_OK)
async def optimize_repo(repo_path: str, session_id: str, language: Optional[str] = None, ref: Optional[str] = None, question: Optional[str] = None):
    response = await optimize(repo_path=repo_path, session_id=session_id, language=language, question=question, ref=ref)
    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)    
