"""Module responsible for handling portfolio analysis tasks using a queue system."""

import os
import json
from dotenv import load_dotenv
from google.api_core import exceptions
from app.backend.services.queue.provider import (
    QueueServiceProvider,
)

load_dotenv()


class StocksAnalyseQueue:
    """Queue class responsible for handling portfolio analysis tasks."""

    JOB_NAME = "stocks-analysis-queue"

    def __init__(
        self,
        queue_service_provider: QueueServiceProvider,
        orchestrator: any,
    ):
        self.__queue_service_provider__ = queue_service_provider
        self.__orchestrator__ = orchestrator

    def push(self, data):
        """Pushes a new portfolio analysis task to the queue."""
        self.__queue_service_provider__.push(queue=self.JOB_NAME, data=data)

    async def consume(self):
        """Consumes messages from the queue and processes them using the orchestrator."""
        try:
            message = self.__queue_service_provider__.pull(queue=self.JOB_NAME)
            for msg in message.received_messages:
                print(f"Received message: {msg.message.data}")
                # Acknowledge the message so it's not redelivered
                data = json.loads(msg.message.data)
                print(f"Data: {data}")
                await self.__orchestrator__.analyze_stocks(
                    user_id=data["user_id"], stocks_data=data["stocks"]
                )
                self.__queue_service_provider__.acknowledge(
                    message_id=msg.ack_id, queue=self.JOB_NAME
                )
        except exceptions.DeadlineExceeded:
            return None
        return message
