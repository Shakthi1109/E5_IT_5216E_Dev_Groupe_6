from entities.Question import Question
from sqlite3 import Connection
from database_utils import convert_to_model

class QuestionsService : 

    @staticmethod
    def create_question(conn: Connection, question: Question):
        return True

    @staticmethod
    def get_questions(conn: Connection) -> list[Question]:
        res = conn.execute("SELECT * FROM Question;").fetchall()
        return convert_to_model(res, Question)
    
    @staticmethod
    def get_question_by_id(conn: Connection, id_question: str) -> Question:
        query = "SELECT * FROM Question WHERE id = ?;"
        return convert_to_model(conn.execute(query, (id_question,)),Question)
        
    
    @staticmethod
    def get_question_by_position(conn: Connection, position: int) -> Question:
        return None
    
    @staticmethod
    def delete_question_by_id(conn: Connection):
        return None
    
    @staticmethod
    def delete_all_questions():
        return None
    
    @staticmethod
    def update_question(conn: Connection, question, Question):
        return None
    
    @staticmethod
    def get_answers(id_question: str):
        return None
    