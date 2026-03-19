from google.cloud import pubsub_v1
import json
from typing import Optional, Any, Callable
from google.api_core import exceptions

class PubSub:
    def __init__(self, project_id: str, topic_id: Optional[str] = None, subscription_id: Optional[str] = None):
        self.project_id = project_id
        self.subscription_id = subscription_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def _get_publisher_topic_path(self, queue:str) -> str:
        tid = queue
        if not tid:
             raise ValueError("Topic ID is required.")
        return self.publisher.topic_path(self.project_id, tid)

    def _get_subscription_topic_path(self, queue: str) -> str:
        if not queue:
             raise ValueError("Subscription ID is required.")
        return self.subscriber.subscription_path(self.project_id, queue)

    def __create_topic__(self, queue: str) -> None:
        try:
            topic_path = self._get_publisher_topic_path(queue)
            self.publisher.create_topic(request={"name": topic_path})
        except exceptions.AlreadyExists:
             pass
        except Exception as e:
            raise e
    
    def __create_subscription__(self, queue: str) -> None:
        try:
            topic_path = self._get_publisher_topic_path(queue)
            subscription_path = self._get_subscription_topic_path(queue)
            self.subscriber.create_subscription(
                request={
                    "name": subscription_path,
                    "topic": topic_path,
                }
            )
        except exceptions.AlreadyExists:
             pass
        except Exception as e:
            raise e
        
    def __create_queue__(self, queue: str) -> None:
        try:
            self.__create_topic__(queue)
            self.__create_subscription__(queue)
        except exceptions.AlreadyExists:
             pass
        except Exception as e:
            raise e

    def push(self, data: Any, queue: str) -> str:
        self.__create_queue__(queue)
        topic_path = self._get_publisher_topic_path(queue)
        if not isinstance(data, (str, bytes)):
             data = json.dumps(data)
        if isinstance(data, str):
             data = data.encode("utf-8") 
        future = self.publisher.publish(topic_path, data)
        return future.result()

    def pull(self,queue: str):
        subscription_path = self._get_subscription_topic_path(queue)
        data = self.subscriber.pull(
                request={
                    "subscription": subscription_path,
                    "max_messages": 100,
                }
        )
        return data

    def acknowledge(self, message_id: str, queue: str):
        self.subscriber.acknowledge(
            request={
                "subscription": self._get_subscription_topic_path(queue),
                "ack_ids": [message_id],
            }
        )
    
