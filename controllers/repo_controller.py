from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.repo_service import query

router = APIRouter()

@router.get("/repo/query", status_code=status.HTTP_200_OK)
async def query_repo(question: str, repo_path: str):
    response = await query(question, repo_path)
    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)

@router.get("/repo/optimize", status_code=status.HTTP_200_OK)
def optimize_repo(query: str, repo_path: str, ref: str):
    return JSONResponse(content={"response": 'optimize_repo() called!'}, status_code=status.HTTP_200_OK)    
