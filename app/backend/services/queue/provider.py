"""Queue Service Provider module responsible for providing queue services to the application."""

from app.backend.services.queue.interfaces.queue_service import QueueService


class QueueServiceProvider:
    """Provider for queue services."""

    __client = None

    def __init__(self, client: QueueService):
        """Initializes a new instance of the class."""
        self.__client = client

    def push(self, queue: str, data: dict):
        """Pushes a new message to the specified queue."""
        self.__client.push(queue=queue, data=data)

    def pull(self, queue: str):
        """Pulls a message from the specified queue."""
        return self.__client.pull(queue=queue)

    def acknowledge(self, message_id: str, queue: str):
        """Acknowledges a message to prevent it from being redelivered."""
        self.__client.acknowledge(message_id=message_id, queue=queue)
