from enum import Enum

class User :
    def __init__(self):
        self.id = None 
        self.email = None
        self.password = None
        self.type = TypeUser.USER


class TypeUser(Enum):
    ADMIN = 0
    USER = 1