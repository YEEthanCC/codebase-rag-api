from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.graph_service import update_graph

router = APIRouter()

@router.post("/graph/create", status_code=status.HTTP_200_OK)
async def create_graph(repo_path: str):
    await create_graph(str)
    return JSONResponse(content={"result": 'graph created'}, status_code=status.HTTP_200_OK)

@router.patch("/graph/update", status_code=status.HTTP_200_OK)
def update_graph(repo_path: str):
    return JSONResponse(content={"response": 'update_graph() called!'}, status_code=status.HTTP_200_OK)

@router.get("/graph/export", status_code=status.HTTP_200_OK)
def export_graph(repo_path: str, file_name: str):
    return JSONResponse(content={"response": 'export_graph() called!'}, status_code=status.HTTP_200_OK)

