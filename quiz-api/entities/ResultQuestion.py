from dataclasses import dataclass

@dataclass
class ResultQuestion :
    #UUID Result, UUID Question, UUID AwnserQuestion
    id: str = None 
    id_question: str = None
    id_awnser_question: str = None

