from typing import Protocol
from fastapi import UploadFile

class FileService(Protocol):

    async def parse_file(self, file: UploadFile):
        pass