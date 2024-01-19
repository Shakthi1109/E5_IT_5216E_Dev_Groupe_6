from dataclasses import dataclass

@dataclass
class AnswerQuestion :
    id: str = None
    id_question: str = None 
    text: str = None 
    isCorrect: bool = False
    position : int = None
    
    def convert_int_to_bool(self):
        self.isCorrect = True if self.isCorrect else False
        
    