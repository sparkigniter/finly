from .interfaces.queue_service import QueueService

class QueueServiceProvider :

    __client = None

    def __init__(self, client: QueueService):
        self.__client = client
    

    def push(self, queue: str, data: dict):
        self.__client.push(queue= queue, data= data)
    
