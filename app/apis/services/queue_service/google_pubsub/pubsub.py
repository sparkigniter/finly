from google.cloud import pubsub_v1
import json
from typing import Optional, Any, Callable

class PubSub:
    def __init__(self, project_id: str, topic_id: Optional[str] = None, subscription_id: Optional[str] = None):
        self.project_id = project_id
        self.topic_id = topic_id
        self.subscription_id = subscription_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def _get_topic_path(self, topic_id: Optional[str] = None) -> str:
        tid = topic_id or self.topic_id
        if not tid:
             raise ValueError("Topic ID is required.")
        return self.publisher.topic_path(self.project_id, tid)

    def _get_subscription_path(self, subscription_id: Optional[str] = None) -> str:
        sid = subscription_id or self.subscription_id
        if not sid:
             raise ValueError("Subscription ID is required.")
        return self.subscriber.subscription_path(self.project_id, sid)

    def push(self, data: Any, queue: Optional[str] = None) -> str:
        topic_path = self._get_topic_path(queue)
        
        if not isinstance(data, (str, bytes)):
             data = json.dumps(data)
        if isinstance(data, str):
             data = data.encode("utf-8")
        
        future = self.publisher.publish(topic_path, data)
        return future.result()

    def consume(self, callback: Callable, subscription_id: Optional[str] = None):
        subscription_path = self._get_subscription_path(subscription_id)
        return self.subscriber.subscribe(
            subscription_path,
            callback= callback
        )
