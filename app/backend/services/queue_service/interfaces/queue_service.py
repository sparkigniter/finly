from typing import Protocol

class QueueService :

    def push(self, queue:str, data: dict) -> None:
        pass

    def pull(self, queue: str) -> None:
        pass

    def acknowledge(self, message_id: str, queue: str) -> None:
        pass
