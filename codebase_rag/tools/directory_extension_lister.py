import os
from pathlib import Path

from loguru import logger
from pydantic_ai import Tool
from sockets.server import sio


class DirectoryLister:
    def __init__(self, project_root: str, socket_id: str):
        self.project_root = project_root
        self.socket_id = socket_id

    def list_directory_contents(self, directory_path: str) -> str:
        """
        Lists the contents of a specified directory.
        """

        try:
            # if not target_path.is_dir():
            #     return f"Error: '{directory_path}' is not a valid directory."

            # if contents := os.listdir(target_path):
            #     return "\n".join(contents)
            # else:
            #     return f"The directory '{directory_path}' is empty."
            return sio.call('list_dir', {'dir_path': directory_path}, to=self.socket_id)

        except Exception as e:
            logger.error(f"Error listing directory {directory_path}: {e}")
            return f"Error: Could not list contents of '{directory_path}'."




def create_directory_lister_tool(directory_lister: DirectoryLister) -> Tool:
    return Tool(
        function=directory_lister.list_directory_contents,
        description="Lists the contents of a directory to explore the codebase.",
    )
