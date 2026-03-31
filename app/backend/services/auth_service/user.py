
class User:
   
    def __init__(self, user_id: str, email: str, display_name: str = None):
        self.user_id = user_id
        self.email = email
        self.display_name = display_name
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "display_name": self.display_name,
            "token": self.token,
            "refresh_token": self.refresh_token
        }
    
    def get_name(self):
        return self.display_name
    
    def get_email(self):
        return self.email
    
    def get_id(self):
        return self.user_id
    
    def set_token(self, token: str):
        self.token = token
    
    def get_token(self) -> str:
        return self.token
    
    def set_refresh_token(self, refresh_token: str):
        self.refresh_token = refresh_token
    
    def get_refresh_token(self) -> str:
        return self.refresh_token
    