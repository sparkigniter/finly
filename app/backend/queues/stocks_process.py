"""Module responsible for handling portfolio analysis tasks using a queue system."""

import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from google.api_core import exceptions
from app.backend.services.queue.provider import (
    QueueServiceProvider,
)
from app.backend.services.protfolio.service import PortfolioService
from app.backend.queues.stocks_analyse import StocksAnalyseQueue


load_dotenv()


class StockProcessQueue:
    """Queue class responsible for handling portfolio analysis tasks."""

    JOB_NAME = "stocks-process-queue"

    def __init__(
        self,
        queue_service_provider: QueueServiceProvider,
        stock_analyse_queue: StocksAnalyseQueue
    ):
        self.__queue_service_provider__ = queue_service_provider
        self.stock_analyse_queue = stock_analyse_queue
    
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
                protflio_service = PortfolioService(data)
                stock_analyse_queue_data = {
                    "stocks": protflio_service.get_stocks(),
                    "pushed_at": datetime.now(
                        timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "user_id": data["user_id"],
                    "request_id": data["request_id"]
                }
                self.stock_analyse_queue.push(json.dumps(stock_analyse_queue_data))
                self.__queue_service_provider__.acknowledge(
                    message_id=msg.ack_id, queue=self.JOB_NAME
                )
        except exceptions.DeadlineExceeded:
            return None
        return message
