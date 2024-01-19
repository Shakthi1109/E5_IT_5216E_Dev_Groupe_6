from dataclasses import dataclass

@dataclass
class AnswerQuestion :
    id: str = None
    id_question: str = None 
    text: str = None 
    isCorrect: bool = False
    position : int = None
    
    def convert_int_to_bool(self):
        if(self.isCorrect == 0) : 
            self.isCorrect = False
        else :
            self.isCorrect = True
        
        
    