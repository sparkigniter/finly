from .interfaces import FileService

class FileServiceProvider:

    async def parse_file(self, file_service_provider: FileService):
        return await file_service_provider.parse_file()
