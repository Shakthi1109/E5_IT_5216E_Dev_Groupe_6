from enum import Enum
from dataclasses import dataclass

class TypeUser(Enum):
    ADMIN = 0
    USER = 1

@dataclass
class User :
    id: str = None 
    email: str = None
    password: str = None
    type: int = TypeUser.USER