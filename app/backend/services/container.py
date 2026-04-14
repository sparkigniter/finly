"""Container module for managing service instances and dependencies."""

import os
import json
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
from app.backend.queues.stocks_analyse import StocksAnalyseQueue
from app.backend.services.auth.provider import AuthServiceProvider
from app.backend.queues.stocks_process import StockProcessQueue
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
        """Returns the singleton instance of the container."""
        if Container.__container is None:
            Container.__container = Container()
        return Container.__container

    def __init__(self):
        """Initializes the Firebase app and other services."""
        self.init_firebase()

    @cached_property
    def get_file_service(self) -> FileService:
        """Returns an instance of ZerodhaFileService for file handling."""
        return ZerodhaFileService()

    @cached_property
    def get_queue_service(self) -> QueueService:
        """Returns an instance of PubSub as the queue service."""
        return PubSub(
            project_id=os.environ["PROJECT_ID"],
        )

    @cached_property
    def get_queue_service_provider(self) -> QueueServiceProvider:
        """Returns a provider for the queue service."""
        return QueueServiceProvider(self.get_queue_service)

    @cached_property
    def get_firebase_auth(self) -> Auth:
        """Returns an instance of Firebase auth."""
        return Auth()

    @cached_property
    def get_auth_service_provider(self) -> AuthServiceProvider:
        """Returns a provider for the authentication service."""
        return AuthServiceProvider(self.get_firebase_auth)

    @cached_property
    def get_portfolio_analysis_queue(self) -> ProtfolioAnalyseQueue:
        """Returns an instance of Portfolio Analysis Queue."""
        return ProtfolioAnalyseQueue(
            self.get_queue_service_provider,
            self.get_finadvisory_orchestrator,
            self.get_stocks_analysis_queue,
        )

    @cached_property
    def get_stocks_analysis_queue(self) -> StocksAnalyseQueue:
        """Returns an instance of Stocks Analysis Queue."""
        return StocksAnalyseQueue(
            self.get_queue_service_provider, self.get_finadvisory_orchestrator
        )

    @cached_property
    def get_stock_process_queue(self) -> StockProcessQueue:
        """Returns an instance of Stocks Process Queue."""
        return StockProcessQueue(
            self.get_queue_service,
            self.get_stocks_analysis_queue)

    @cached_property
    def get_finadvisory_orchestrator(self):
        """Returns an instance of FinAdvisorOrchestrator."""
        return FinAdvisorOrchestrator()

    @cached_property
    def get_kite_client(self) -> KiteClient:
        """Returns an instance of KiteClient for Kite broker service."""
        return KiteClient()

    @cached_property
    def get_kite_service(self) -> KiteBrokerService:
        """Returns a Kite broker service instance."""
        return KiteBrokerService(self.get_kite_client, self.get_cache_provider)

    @cached_property
    def get_broker_service_provider(self) -> BrokerServiceProvider:
        """Returns a provider for the broker service."""
        return BrokerServiceProvider(self.get_kite_service)

    @cached_property
    def get_redis_client(self) -> RedisClient:
        """Returns an instance of RedisClient for caching."""
        return RedisClient()

    @cached_property
    def get_cache_provider(self) -> CacheProvider:
        """Returns a cache provider using Redis client."""
        return CacheProvider(self.get_redis_client)

    def init_firebase(self):
        """Initializes the Firebase app with the provided credentials and project ID.

        Expects FIREBASE_CERT env var to contain a JSON string with Firebase service account.
        Can also read from a local file at ./firebase-cert.json for local development.
        """

        try:
            if os.getenv("env") == "development":
                cert = os.getenv("FIREBASE_CERT_PATH")
            else:
                firebase_cert_json = os.environ.get("FIREBASE_CERT") or None
                if not firebase_cert_json:
                    raise ValueError(
                        "FIREBASE_CERT environment variable is not set.")
                cert = json.loads(firebase_cert_json)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid Firebase certificate JSON: {}".format(e))

        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(cert)
                firebase_admin.initialize_app(
                    cred, {"projectId": os.environ["FIREBASE_PROJECT_ID"]}
                )
                print("Firebase initialized successfully")
            except Exception as e:
                raise ValueError("Failed to initialize Firebase: {}".format(e))
