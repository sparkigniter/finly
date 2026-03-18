from app.apis.services.queue_service.queue_service_provider import QueueServiceProvider

class ProtfolioAnalyseQueue:

    JOB_NAME = "protfolio-analysis-queue"

    def __init__(self, queue_service_provider: QueueServiceProvider):
        self.__queue_service_provider__ = queue_service_provider
    
    def push(self, data):
        self.__queue_service_provider__.push(queue= self.JOB_NAME, data= data)
