from entities.Question import Question
from sqlite3 import Connection
from database_utils import convert_to_model

class QuestionsService : 

    @staticmethod
    def create_question(conn: Connection, titre: str, image: str, content_question: str):
        return True

    @staticmethod
    def get_questions(conn: Connection) -> list[Question]:
        res = conn.execute("SELECT * FROM Question;").fetchall()
        return convert_to_model(res, Question)
    
    @staticmethod
    def get_question_by_id(conn: Connection, id_question: str):
        query = "SELECT * FROM Question WHERE id = ?;"
        return convert_to_model(
            conn.execute(query, (id_question,)),
            Question
        )
    
    @staticmethod
    def delete_results(conn: Connection):
        return True

    @staticmethod
    def delete_result_by_id(conn: Connection, id_result: str):
        return True