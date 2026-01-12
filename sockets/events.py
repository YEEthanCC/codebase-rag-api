from .server import sio
from codebase_rag.tools.file_reader import FileReader
from codebase_rag.tools.file_extension_reader import FileExtensionReader

@sio.on("connect")
async def connect(sid, environ):
    print("Client connected: ", sid)

@sio.on("disconnect")
async def disconnect(sid, environ): 
    print("Client disconnected: ", sid)

@sio.on("read_file")
async def read_file(sid, data: str):
    print(data)