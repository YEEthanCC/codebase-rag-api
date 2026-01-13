from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.repo_service import query, optimize, discard_changes
from typing import Optional
from typing import Any
from codebase_rag.tools.file_reader import FileReader
from codebase_rag.tools.file_extension_reader import FileExtensionReader
from codebase_rag.tools.directory_extension_lister import DirectoryExtensionLister
from codebase_rag.tools.directory_lister import DirectoryLister

router = APIRouter()

@router.get("/repo/extension/query", status_code=status.HTTP_200_OK)
async def query_repo(sid: str, question: str):
    directory_lister = DirectoryLister('/home/ethan/projects/flask-api')
    direcotry_extension_lister = DirectoryExtensionLister(sid)
    local_content = f"{directory_lister.list_directory_contents('app/controller')}"
    print(f"file reader output: \n{local_content}")
    extension_content = f"{await direcotry_extension_lister.list_directory_contents('app/controller')}"
    print(f"\nfile extension reader output: \n{extension_content}")
    if local_content == extension_content:
        print("\npass")
    else:
        print("\nfailed")
    return JSONResponse(content={"response": "get message from client"}, status_code=status.HTTP_200_OK)

@router.post("/repo/extension/optimize", status_code=status.HTTP_200_OK)
async def optimize_repo(repo_path: str, session_id: str, language: Optional[str] = None, ref: Optional[str] = None, question: Optional[str] = None):
    response, edit = await optimize(repo_path=repo_path, session_id=session_id, language=language, question=question, ref=ref)
    return JSONResponse(content={"response": response, "edit": edit}, status_code=status.HTTP_200_OK)    


@router.post("/repo/extension/reject", status_code=status.HTTP_200_OK)
async def reject(repo_path: str, session_id: str):
    await discard_changes(repo_path, session_id)
    return JSONResponse(content={"response": 'Changes have been discarded!!!'}, status_code=status.HTTP_200_OK) 