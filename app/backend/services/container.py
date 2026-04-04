"""Container module for managing service instances and dependencies."""

import os
from functools import cached_property
from typing import Optional
import firebase_admin
from firebase_admin import credentials
from app.backend.services.broker.provider import BrokerServiceProvider
from app.backend.services.broker.kite.client import KiteClient
from app.backend.services.file.zeroda.service import ZerodhaFileService
from app.backend.services.file.interfaces.file_service import FileService
from app.backend.services.queue.interfaces.queue_service import QueueService
from app.backend.services.queue.google_pubsub.pubsub import PubSub
from app.backend.services.queue.provider import QueueServiceProvider
from app.backend.queues.protfolio_analyse import ProtfolioAnalyseQueue
from app.backend.services.auth.provider import AuthServiceProvider
from app.backend.services.auth.google_firebase.auth import Auth
from app.ai.google_vertex.workflows.finadvisory_orchestrator import (
    FinAdvisorOrchestrator,
)
from app.backend.services.broker.kite.service import KiteBrokerService
from app.backend.services.cache.redis.client import RedisClient
from app.backend.services.cache.provider import CacheProvider


class Container:
    """Container class for managing service instances and dependencies."""

    __container: Optional["Container"] = None

    @staticmethod
    def get() -> "Container":
        if Container.__container is None:
            Container.__container = Container()
        return Container.__container

    def __init__(self):
        self.init_firebase()

    @cached_property
    def get_file_service(self) -> FileService:
        return ZerodhaFileService()

    @cached_property
    def get_queue_service(self) -> QueueService:
        return PubSub(
            project_id=os.environ["PROJECT_ID"],
        )

    @cached_property
    def get_queue_service_provider(self) -> QueueServiceProvider:
        return QueueServiceProvider(self.get_queue_service)

    @cached_property
    def get_firebase_auth(self) -> Auth:
        return Auth()

    @cached_property
    def get_auth_service_provider(self) -> AuthServiceProvider:
        return AuthServiceProvider(self.get_firebase_auth)

    @cached_property
    def get_finadvisory_orchestrator(self):
        return FinAdvisorOrchestrator()

    @cached_property
    def get_portfolio_analysis_queue(self) -> ProtfolioAnalyseQueue:
        return ProtfolioAnalyseQueue(
            self.get_queue_service_provider, self.get_finadvisory_orchestrator
        )

    @cached_property
    def get_kite_client(self) -> KiteClient:
        return KiteClient()

    @cached_property
    def get_kite_service(self) -> KiteBrokerService:
        return KiteBrokerService(self.get_kite_client, self.get_cache_provider)
    
    @cached_property
    def get_broker_service_provider(self) -> BrokerServiceProvider:
        return BrokerServiceProvider(self.get_kite_service)
    
    @cached_property
    def get_redis_client(self) -> RedisClient:
        return RedisClient()
    
    @cached_property
    def get_cache_provider(self) -> CacheProvider:
        return CacheProvider(self.get_redis_client)
    

    def init_firebase(self):
        cert_path = os.environ["FIREBASE_CERT_PATH"]
        if not firebase_admin._apps:
            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(
                cred, {"projectId": os.environ["FIREBASE_PROJECT_ID"]}
            )
