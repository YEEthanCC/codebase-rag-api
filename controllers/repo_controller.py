from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.repo_service import RepoService

router = APIRouter()
repo_service = RepoService()

@router.get("/repo/query", status_code=status.HTTP_200_OK)
def query_repo(query: str, repo_path: str):
    return JSONResponse(content={"response": 'query_repo() called!'}, status_code=status.HTTP_200_OK)

@router.get("/repo/optimize", status_code=status.HTTP_200_OK)
def optimize_repo(query: str, repo_path: str, ref: str):
    return JSONResponse(content={"response": 'optimize_repo() called!'}, status_code=status.HTTP_200_OK)    
