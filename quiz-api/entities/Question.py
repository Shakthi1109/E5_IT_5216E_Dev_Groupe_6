from dataclasses import dataclass

@dataclass
class Question :
    id: str = None
    position: int = None 
    question: str = None
    titre: str = None 
    image: str = None 