from .interfaces import FileServiceProvider

class FileService:

    async def parse_file(self, file_service_provider: FileServiceProvider):
        return await file_service_provider.parse_file()
