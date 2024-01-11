from dataclasses import dataclass
import uuid

@dataclass
class Question :
    id: str = None
    position: int = None 
    question: str = None
    titre: str = None 
    image: str = None 