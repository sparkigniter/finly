"""Module providing provider functionality."""

from .interfaces import FileService


class FileServiceProvider:
    """FileServiceProvider class implementation."""

    async def parse_file(self, file_service_provider: FileService):
        """Performs the parse file operation."""
        return await file_service_provider.parse_file()
