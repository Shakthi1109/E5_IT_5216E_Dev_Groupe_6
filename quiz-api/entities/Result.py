from dataclasses import dataclass
from datetime import datetime

@dataclass
class Result :
    id: str = None 
    pseudo: str = None
    date: datetime = None

