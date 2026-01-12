from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.repo_service import query, optimize, discard_changes
from typing import Optional
from typing import Any
from codebase_rag.tools.file_reader import FileReader
from codebase_rag.tools.file_extension_reader import FileExtensionReader

router = APIRouter()

@router.get("/repo/extension/query", status_code=status.HTTP_200_OK)
async def query_repo(sid: str, question: str):
    file_reader = FileReader('/home/ethan/projects/flask-api')
    file_extension_reader = FileExtensionReader(sid)
    print(f"file reader output: \n{await file_reader.read_file('docker-compose.yml')}")
    content = await file_extension_reader.read_file('docker-compose.yml')
    print(f"file extension reader output: \n{content}")
    return JSONResponse(content={"response": "get message from client"}, status_code=status.HTTP_200_OK)

@router.post("/repo/extension/optimize", status_code=status.HTTP_200_OK)
async def optimize_repo(repo_path: str, session_id: str, language: Optional[str] = None, ref: Optional[str] = None, question: Optional[str] = None):
    response, edit = await optimize(repo_path=repo_path, session_id=session_id, language=language, question=question, ref=ref)
    return JSONResponse(content={"response": response, "edit": edit}, status_code=status.HTTP_200_OK)    


@router.post("/repo/extension/reject", status_code=status.HTTP_200_OK)
async def reject(repo_path: str, session_id: str):
    await discard_changes(repo_path, session_id)
    return JSONResponse(content={"response": 'Changes have been discarded!!!'}, status_code=status.HTTP_200_OK) 