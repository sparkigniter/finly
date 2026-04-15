"""Module responsible for handling portfolio analysis tasks using a queue system."""

import os
import json
from dotenv import load_dotenv
from datetime import datetime, timezone
from google.api_core import exceptions
from app.backend.services.queue.provider import (
    QueueServiceProvider,
)
from app.ai.google_vertex.workflows.finadvisory_orchestrator import (
    FinAdvisorOrchestrator,
)

from app.ai.google_vertex.agents.tools.firestore_datastore import get_stocks

from app.backend.queues.stocks_analyse import StocksAnalyseQueue
from app.backend.queues.stocks_process import StockProcessQueue


load_dotenv()


class ProtfolioAnalyseQueue:
    """Queue class responsible for handling portfolio analysis tasks."""

    JOB_NAME = "protfolio-analysis-queue"

    def __init__(
        self,
        queue_service_provider: QueueServiceProvider,
        orchestrator: FinAdvisorOrchestrator,
        stock_analysis_queue: StocksAnalyseQueue
    ):
        """Initializes a new instance of the class."""
        self.__queue_service_provider__ = queue_service_provider
        self.__orchestrator__ = orchestrator
        self.stock_analysis_queue = stock_analysis_queue

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
                print(f"ProtfolioAnalyseQueue Data: {data}")
                await self.__orchestrator__.analyze_protfolio(
                    user_id=data["user_id"], protfolio_data=data["protfolio"]
                )
                self.__queue_service_provider__.acknowledge(
                    message_id=msg.ack_id, queue=self.JOB_NAME
                )
                stocks = get_stocks(data["user_id"])
                batch_size = 10
                for batch in range(0, len(stocks), batch_size):
                    stocks_queue_data = {
                        "stocks": stocks[batch:batch + batch_size],
                        "pushed_at": datetime.now(
                            timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                        "user_id": data["user_id"],
                        "request_id": data["request_id"]
                    }
                    self.stock_analysis_queue.push(json.dumps(stocks_queue_data)) #push the stocks to process 
        except exceptions.DeadlineExceeded:
            return None
        return message

