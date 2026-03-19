import json
from google.api_core import exceptions
from app.backend.services.queue_service.queue_service_provider import QueueServiceProvider
from app.ai.google_vertex.workflows.finadvisory_orchestrator import FinAdvisorOrchestrator



class ProtfolioAnalyseQueue:

    JOB_NAME = "protfolio-analysis-queue"

    def __init__(self, queue_service_provider: QueueServiceProvider):
        self.__queue_service_provider__ = queue_service_provider
    
    def push(self, data):
        self.__queue_service_provider__.push(queue= self.JOB_NAME, data= data)

    async def consume(self):
        try:
            message = self.__queue_service_provider__.pull(queue=self.JOB_NAME)
            print("Recieved message: {message}")
            for msg in message.received_messages:
                print(f"Received message: {msg.message.data}")
                # Acknowledge the message so it's not redelivered
                data = json.loads(msg.message.data)
                print(f"Data: {data}")
                await FinAdvisorOrchestrator.analyze_portfolio(user_id= 'test', file_content= data["data"])
                self.__queue_service_provider__.aknowledge(message_id= msg.ack_id, queue= self.JOB_NAME)
        except exceptions.DeadlineExceeded:
            return None
        return message

