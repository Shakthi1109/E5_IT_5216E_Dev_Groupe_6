from entities.Question import Question
from sqlite3 import Connection

class QuestionsService : 

    @staticmethod
    def create_question(conn: Connection, titre: str, image: str, content_question: str):
        return True

    def get_questions(conn: Connection):
        return 5
    
    @staticmethod
    def get_question_by_id(conn: Connection, id_question: int):
        return []
    
    @staticmethod
    def delete_results(conn: Connection):
        return True

    @staticmethod
    def delete_result_by_id(conn: Connection, id_result: int):
        return True