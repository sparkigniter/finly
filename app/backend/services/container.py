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



class Container:

    def __init__(self):
        self.file_service: FileService = ZerodhaFileService()
        self.queue_service : QueueService = PubSub("massive-mantra-125114")
        self.queue_service_provider: QueueServiceProvider = QueueServiceProvider(self.queue_service)
        self.protfolio_analysis_queue = ProtfolioAnalyseQueue(self.queue_service_provider)
        self.firebase_auth = Auth()
        self.auth_service_provider = AuthServiceProvider(self.firebase_auth)
        self.init_firebase()


    def init_firebase(self):
        cert_path = "/Users/vikas/Desktop/finly-2a457-firebase-adminsdk-fbsvc-96f864b858.json"
        cred = credentials.Certificate(cert_path)
        if not firebase_admin._apps:
            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(cred, { 'projectId': 'finly-2a457'})


container = Container()
