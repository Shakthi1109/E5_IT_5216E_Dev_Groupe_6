from dataclasses import dataclass
from datetime import datetime

@dataclass
class Participation :
    id: str = None 
    pseudo: str = None
    score: int = 0
    date: datetime = None

