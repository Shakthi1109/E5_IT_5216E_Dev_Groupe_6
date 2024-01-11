from dataclasses import dataclass

@dataclass
class AnswerQuestion :
    id: str = None
    id_question: str = None 
    content: str = None
    is_correct: bool = False
    