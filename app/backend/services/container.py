from .file_service.zeroda.zerodha_file_service import ZerodhaFileService
from .file_service.interfaces.file_service import FileService
from .queue_service.interfaces.queue_service import QueueService
from .queue_service.google_pubsub.pubsub import PubSub
from .queue_service.queue_service_provider import QueueServiceProvider
from app.backend.queues.protfolio_analyse import ProtfolioAnalyseQueue
from app.backend.services.auth_service.auth_service_provider import AuthServiceProvider 
from app.backend.services.auth_service.google_firebase.auth import Auth
import firebase_admin
from firebase_admin import credentials
from functools import cached_property
from typing import Optional
import os
from app.ai.google_vertex.workflows.finadvisory_orchestrator import FinAdvisorOrchestrator


class Container:

    __container:Optional['Container'] = None


    @staticmethod
    def get() -> 'Container':
        if Container.__container == None:
            Container.__container = Container()
        return Container.__container

    def __init__(self):
        self.init_firebase()

    @cached_property
    def get_file_service(self) -> FileService:
        return ZerodhaFileService()

    @cached_property
    def get_queue_service(self) -> QueueService:
        return PubSub(project_id= os.environ["PROJECT_ID"],)
    
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
        return ProtfolioAnalyseQueue(self.get_queue_service_provider, self.get_finadvisory_orchestrator)


    def init_firebase(self):
        cert_path = os.environ["FIREBASE_CERT_PATH"]
        if not firebase_admin._apps:
            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(cred, {'projectId': os.environ["FIREBASE_PROJECT_ID"]})
