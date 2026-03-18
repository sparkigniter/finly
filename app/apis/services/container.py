from .file_service.zeroda.zerodha_file_service import ZerodhaFileService
from .file_service.interfaces.file_service_provider import FileServiceProvider
from .queue_service.interfaces.queue_service import QueueService
from .queue_service.google_cloud_task.cloud_task import CloudTask

class Container:

    def __init__(self):
        self.file_service: FileServiceProvider = ZerodhaFileService()
        self.queue_service : QueueService = CloudTask("massoiv", "location")


container = Container()
