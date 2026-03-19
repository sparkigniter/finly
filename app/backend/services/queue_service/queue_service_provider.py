from .interfaces.queue_service import QueueService

class QueueServiceProvider :

    __client = None

    def __init__(self, client: QueueService):
        self.__client = client
    

    def push(self, queue: str, data: dict):
        self.__client.push(queue= queue, data= data)

    def pull(self, queue: str):
        return self.__client.pull(queue= queue)
    
    def aknowledge(self, message_id: str, queue: str):
        self.__client.aknowledge(message_id= message_id, queue= queue)
    
