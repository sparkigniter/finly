"""Module providing file_service functionality."""

from typing import Protocol
from fastapi import UploadFile


class FileService(Protocol):
    """FileService class implementation."""

    async def parse_file(self, file: UploadFile):
        """Performs the parse file operation."""
        pass
