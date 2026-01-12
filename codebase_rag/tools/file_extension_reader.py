from loguru import logger
from pydantic_ai import Tool
from .file_reader import FileReadResult
from sockets.server import sio


class FileExtensionReader:
    """Service to read file content from the filesystem."""

    def __init__(self, socket_id: str):
        self.binary_extensions = {
            ".pdf",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".bmp",
            ".ico",
            ".tiff",
            ".webp",
        }
        self.socket_id = socket_id

    async def read_file(self, file_path: str) -> FileReadResult:
        result = await sio.call(
            "read_file",
            {"file_path": file_path},
            to=self.socket_id,
        )

        if not result["ok"]:
            raise RuntimeError(result["error"])

        return FileReadResult(
            file_path=file_path,
            content=result["content"]
        )



def create_file_reader_tool(file_reader: FileExtensionReader) -> Tool:
    """Factory function to create the file reader tool."""

    async def read_file_content(file_path: str) -> str:
        """
        Reads the content of a specified text-based file (e.g., source code, README.md, config files).
        This tool should NOT be used for binary files like PDFs or images. For those, use the 'analyze_document' tool.
        """
        result = await file_reader.read_file(file_path)
        if result.error_message:
            return f"Error: {result.error_message}"
        return result.content or ""

    return Tool(
        function=read_file_content,
        description="Reads the content of text-based files. For documents like PDFs or images, use the 'analyze_document' tool instead.",
    )
