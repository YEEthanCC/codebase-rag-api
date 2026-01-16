from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.repo_service import query, optimize, discard_changes
from typing import Optional
from typing import Any
from codebase_rag.tools.file_reader import FileReader
from codebase_rag.tools.file_extension_reader import FileExtensionReader
from codebase_rag.tools.directory_extension_lister import DirectoryExtensionLister
from codebase_rag.tools.directory_lister import DirectoryLister
from codebase_rag.tools.document_analyzer import DocumentAnalyzer
from codebase_rag.tools.document_extension_analyzer import DocumentExtensionAnalyzer

router = APIRouter()

@router.get("/repo/extension/query", status_code=status.HTTP_200_OK)
async def query_repo(sid: str, question: str):
    document_analyzer = DocumentAnalyzer('/home/ethan/projects/flask-api')
    document_extension_analyzer = DocumentExtensionAnalyzer(sid)
    local_content = f"{document_analyzer.analyze(file_path='Q1 Learning Plan.pdf', question='What the file is about?')}"
    print(f"Local output: \n{local_content}")
    extension_content = f"{await document_extension_analyzer.analyze(file_path='Q1 Learning Plan.pdf', question='What the file is about?')}"
    print(f"\nExtension output: \n{extension_content}")
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