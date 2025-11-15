from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.repo_service import query, optimize
from typing import Optional

router = APIRouter()

@router.get("/repo/query", status_code=status.HTTP_200_OK)
async def query_repo(question: str, repo_path: str):
    response = await query(question, repo_path)
    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)

@router.post("/repo/optimize", status_code=status.HTTP_200_OK)
async def optimize_repo(repo_path: str, language: str, ref: Optional[str] = None):
    response = await optimize(repo_path, language, ref)
    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)    
