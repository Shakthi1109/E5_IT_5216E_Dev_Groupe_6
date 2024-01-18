from dataclasses import dataclass

@dataclass
class AnswerQuestion :
    id: str = None
    id_question: str = None 
    text: str = None 
    isCorrect: bool = False
    position : int = None
    