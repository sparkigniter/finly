from .file_service.zeroda.zerodha_file_service import ZerodhaFileService
from .file_service.interfaces.file_service import FileService
from .queue_service.interfaces.queue_service import QueueService
from .queue_service.google_pubsub.pubsub import PubSub
from .queue_service.queue_service_provider import QueueServiceProvider
from app.backend.queues.protfolio_analyse import ProtfolioAnalyseQueue

class Container:

    def __init__(self):
        self.file_service: FileService = ZerodhaFileService()
        self.queue_service : QueueService = PubSub("massive-mantra-125114")
        self.queue_service_provider: QueueServiceProvider = QueueServiceProvider(self.queue_service)
        self.protfolio_analysis_queue = ProtfolioAnalyseQueue(self.queue_service_provider)


container = Container()
