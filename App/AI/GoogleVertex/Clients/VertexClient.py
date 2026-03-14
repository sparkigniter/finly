import vertexai

class VertexClient:
    
    def __init__(self):
        self.client = None  

    def __create_client(self):
        self.client = vertexai.Client(
            project="massive-mantra-125114",
            location="asia-south1",
        )

    @staticmethod
    def get_client(self):
        if self.client is None:
            self.__create_client()
        return self.client
