from .interfaces.queue_service import QueueService

class QueueServiceProvider :

    __client = None

    def __init__(self, client: QueueService):
        self.__client = client

    def push(self, data):
        self.__client.push(data)