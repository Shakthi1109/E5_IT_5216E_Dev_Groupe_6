from dataclasses import dataclass
from datetime import datetime

@dataclass
class Participation :
    id: str = None 
    pseudo: str = None
<<<<<<< HEAD
=======
    score: int = 0
>>>>>>> b5dff3f6c3367d89ab2cd8c8a78d05829988de78
    date: datetime = None

