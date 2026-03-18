from typing import Protocol
from fastapi import UploadFile

class FileServiceProvider(Protocol):

    async def parse_file(self, file: UploadFile):
        return file