from dataclasses import dataclass
from datetime import datetime

@dataclass
class Participation :
    id: str = None 
    pseudo: str = None
    date: datetime = None

