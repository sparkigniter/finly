from google.cloud import tasks_v2

class CloudTask :

    __project_id = None
    __locatopn = None
    __client = None
    __parent = None

    
    QUEUE_NAME: str = ""

    def __init__(self, project_id: str, locatoin: str):
        self.__project_id = project_id
        self.__locatopn = locatoin
        self.__client = tasks_v2.CloudTasksClient()
        self.__parent = self.__client.queue_path(self.__project_id, self.__locatopn, self.QUEUE_NAME)

    def push(self, data) -> None:
        self.__client.create_task(data)

    
        