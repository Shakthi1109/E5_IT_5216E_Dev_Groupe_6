from entities.Question import Question
from entities.AnswerQuestion import AnswerQuestion
from sqlite3 import Connection
from database_utils import convert_to_model
from dataclasses import astuple

class QuestionsService : 

    @staticmethod
    def create_question(conn: Connection, question: Question):
        conn.execute(
            "INSERT INTO Question VALUES(%s, %s, %s, %s, %s);",
            *astuple(question)
        )

    @staticmethod
    def get_questions(conn: Connection) -> list[Question]:
        res = conn.execute("SELECT * FROM Question;").fetchall()
        return convert_to_model(res, Question)
    
    @staticmethod
    def get_question_by_id(conn: Connection, id_question: str) -> Question:
        query = "SELECT * FROM Question WHERE id = %s;"
        return convert_to_model(conn.execute(query, (id_question,)),Question)

    @staticmethod
    def get_question_by_position(conn: Connection, position: int) -> Question:
        query = "SELECT * FROM Question WHERE position = %s;"
        return convert_to_model(conn.execute(query, (position,)),Question)
    
    @staticmethod
    def delete_question_by_id(conn: Connection, id_question: str):
        conn.execute("DELETE FROM Question WHERE id = %s;", (id_question,))
        conn.commit()
    
    @staticmethod
    def delete_all_questions(conn: Connection):
        conn.execute("DELETE FROM Question;")
        conn.commit()
    
    @staticmethod
    def update_question(conn: Connection, question: Question):
        conn.execute(
            """
            UPDATE Question
            SET position = %s,
                question = %s,
                titre = %s,
                image = %s
            WHERE id = %s;
            """,
            (question.position, question.question, question.titre, question.image, question.id)
        )
        conn.commit()
    
    @staticmethod
    def get_answers(conn: Connection, id_question: str):
        return convert_to_model(conn.execute("SELECT * FROM AnswerQuestion WHERE id_question = %s", (id_question,)).fetchall(), AnswerQuestion)
    