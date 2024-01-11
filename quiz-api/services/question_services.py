from entities.Question import Question
from entities.AnswerQuestion import AnswerQuestion
from sqlite3 import Connection
from database_utils import convert_to_model
from dataclasses import astuple

class QuestionsService : 

    @staticmethod
    def create_question(conn: Connection, question: Question):
        conn.execute("INSERT INTO Question VALUES(?, ?, ?, ?, ?);", (astuple(question)) )
        conn.commit()
        return question

    @staticmethod
    def get_questions(conn: Connection) -> list[Question]:
        res = conn.execute("SELECT * FROM Question;").fetchall()
        return convert_to_model(res, Question)
    
    @staticmethod
    def get_numbers_questions(conn: Connection) -> int:
        res = conn.execute("SELECT COUNT(*) FROM Question;")
        count = res.fetchone()[0]
        return count
    
    @staticmethod
    def get_question_by_id(conn: Connection, id_question: str) -> Question:
        res = conn.execute("SELECT * FROM Question WHERE id = ?;", (id_question,)).fetchone()
        return convert_to_model(res, Question)

    @staticmethod
    def get_question_by_position(conn: Connection, position: int) -> Question:
        res = conn.execute("SELECT * FROM Question WHERE position = ?;", (position,)).fetchone()
        return convert_to_model(res, Question)
    
    @staticmethod
    def delete_question_by_id(conn: Connection, id_question: str):
        conn.execute("DELETE FROM Question WHERE id = ?;", (id_question,))
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
            SET position = ?,
                question = ?,
                titre = ?,
                image = ?
            WHERE id = ?;
            """,
            (question.position, question.question, question.titre, question.image, question.id)
        )
        conn.commit()
    
    @staticmethod
    def create_answer_question(conn: Connection, ans: AnswerQuestion):
        conn.execute("INSERT INTO AnswerQuestion VALUES(?, ?, ?, ?);",(astuple(ans)))
        conn.commit()
    
    @staticmethod
    def get_all_answers(conn: Connection) -> list[AnswerQuestion]:
        res = conn.execute("SELECT * FROM AnswerQuestion;",).fetchall()
        return convert_to_model(res, AnswerQuestion)
    
    @staticmethod
    def get_answers(conn: Connection, id_question: str) -> list[AnswerQuestion]:
        res = conn.execute("SELECT * FROM AnswerQuestion WHERE id_question = ?", (id_question,)).fetchall()
        return convert_to_model(res, AnswerQuestion)
    
    @staticmethod
    def get_answer_by_id(conn: Connection, id_answer: str) -> Question:
        res = conn.execute("SELECT * FROM AnswerQuestion WHERE id = ?;", (id_answer,)).fetchone()
        return convert_to_model(res, Question)
    
    @staticmethod
    def get_good_answer_with_question_id(conn: Connection, id_question: str) -> Question:
        res = conn.execute("SELECT * FROM AnswerQuestion WHERE id_question = ? AND is_correct = True;", (id_question,)).fetchone()
        return convert_to_model(res, Question)
    
    @staticmethod
    def update_answer_question(conn: Connection, ans: AnswerQuestion):
        conn.execute(
            """
            UPDATE AnswerQuestion
            SET id_question = ?,
                content = ?,
                is_correct = ?
            WHERE id = ?;
            """,

            (ans.id_question, ans.content, ans.is_correct, ans.id)
        )
        conn.commit()
        
    @staticmethod
    def delete_answers_question_by_id(conn: Connection, id_question: str):
        conn.execute("DELETE FROM AnswerQuestion WHERE id_question = ?;", (id_question,))
        conn.commit()
    
    @staticmethod
    def delete_all_anwsers_questions(conn: Connection):
        conn.execute("DELETE FROM AnswerQuestion;")
        conn.commit()