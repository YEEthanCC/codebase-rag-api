from fastapi import FastAPI
from controllers.graph_controller import router as graph_router
from controllers.repo_controller import router as repo_router
from fastapi.middleware.cors import CORSMiddleware
from sockets.server import sio
import socketio
import uvicorn

from sockets.server import sio
from sockets import events

app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Server is alive and active!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods
    allow_headers=["*"],          # Allow all headers
)
app.include_router(graph_router)
app.include_router(repo_router)

socket_app = socketio.ASGIApp(
	sio,
	other_asgi_app=app,
)

if __name__ == "__main__":
	uvicorn.run("main:socket_app", host="127.0.0.1", port=8000)

# if __name__ == "__main__":
#     from codebase_rag.main import app

#     app()
