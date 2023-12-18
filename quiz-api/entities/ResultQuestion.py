from dataclasses import dataclass

@dataclass
class ResultQuestion :
    #UUID Result, UUID Question, UUID AwnserQuestion
    id: str = None 
    id_question: str = None
    id_answer_question: str = None

