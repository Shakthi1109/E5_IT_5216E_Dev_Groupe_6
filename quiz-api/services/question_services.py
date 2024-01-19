from entities.Question import Question
from entities.AnswerQuestion import AnswerQuestion
from sqlite3 import Connection
from database_utils import convert_to_model
from dataclasses import astuple

class QuestionsService : 

    @staticmethod
    def create_question(conn: Connection, question: Question):
        
        old_position = question.position
        question.position = 0
        
        conn.execute("INSERT INTO Question VALUES(?, ?, ?, ?, ?);", (astuple(question)) )
        conn.commit()
        
        question.position = old_position
        
        ### Appel de update_question pour pouvoir trier correctement les questions
        QuestionsService.update_question(conn, question)
        
        return question
    
    @staticmethod
    def get_question_by_position_with_not_id(conn, question_position, question_id):
        query = "SELECT * FROM Question WHERE position = ? AND id != ? LIMIT 1;"
        res = conn.execute(query, (question_position, question_id)).fetchone()
        return convert_to_model(res, Question)
    
    @staticmethod
    def get_highest_position(conn):
        query = "SELECT MAX(position) FROM Question;"
        result = conn.execute(query).fetchone()        
        return result[0] if result else None

    @staticmethod
    def get_unassigned_positions(conn):
        highest_position = QuestionsService.get_highest_position(conn)

        if highest_position is None:
            return []

        used_positions = conn.execute("SELECT position FROM Question;").fetchall()
        used_positions = [pos[0] for pos in used_positions]

        all_positions = set(range(1, highest_position + 1))
        unassigned_positions = list(all_positions - set(used_positions))

        return unassigned_positions

    
    @staticmethod
    def update_question(conn: Connection, question: Question):
        
        quest = QuestionsService.get_question_by_id(conn, question.id)
        old_position = -1
        if(quest != None): old_position = quest.position
        query = "UPDATE Question SET position = ?, question = ?, titre = ?, image = ? WHERE id = ?;"
        conn.execute(query, (question.position, question.question, question.titre, question.image, question.id))
        conn.commit()
                
        if(old_position != question.position):
            
            direction = 1 
            question_position = QuestionsService.get_question_by_position_with_not_id(conn, question.position, question.id)            
            highest_position = QuestionsService.get_highest_position(conn)
            number_questions = QuestionsService.get_numbers_questions(conn)
           
            if(question_position == None) : 
                return 
            
            if(old_position == 0) : 
                old_position = number_questions
                
            last_id = question.id
            
            direction = 1 
            if(question.position > old_position) : 
                direction = -1
            
            start = min(question.position, old_position)
            stop = max(number_questions, question.position)
            
            if(direction == -1) : start, stop = stop, start 
                
            for i in range(start, stop, direction):
                quest = QuestionsService.get_question_by_position_with_not_id(conn, i, last_id) 
                if(quest == None) : continue 
                
                last_id = quest.id
                quest.position += direction
                conn.execute(query, (quest.position, quest.question, quest.titre, quest.image, quest.id))
                conn.commit()
            

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
    def get_question_by_id(conn: Connection, id_question: str) -> Question :        
        res = conn.execute("SELECT * FROM Question WHERE id = ?;", (id_question,)).fetchone()
        return convert_to_model(res, Question)


    @staticmethod
    def get_question_by_position(conn: Connection, position: int) -> Question:
        res = conn.execute("SELECT * FROM Question WHERE position = ?;", (position,)).fetchone()
        return convert_to_model(res, Question)
    
    @staticmethod
    def delete_question_by_id(conn: Connection, id_question: str):
        
        quest = QuestionsService.get_question_by_id(conn, id_question)
        if(quest == None) : return 
        
        position = quest.position
        
        conn.execute("DELETE FROM Question WHERE id = ?;", (id_question,))
        conn.commit()
        
        query = "UPDATE Question SET position = ?, question = ?, titre = ?, image = ? WHERE id = ?;"
        
        nb_questions = QuestionsService.get_numbers_questions(conn)
        for i in range(position+1, nb_questions+2) :
            quest = QuestionsService.get_question_by_position(conn, i)
            quest.position -= 1 
            conn.execute(query, (quest.position, quest.question, quest.titre, quest.image, quest.id))
            conn.commit()

        
        
    
    @staticmethod
    def delete_all_questions(conn: Connection):
        conn.execute("DELETE FROM Question;")
        conn.commit()
        
    @staticmethod
    def question_exists(conn: Connection, question_id: str) -> bool :
        query = "SELECT COUNT(*) FROM Question WHERE id = ?;"
        result = conn.execute(query, (question_id,)).fetchone()
        if result and result[0] != 0:
            return True
        else:
            return False
        conn.commit()

    @staticmethod
    def create_answer_question(conn: Connection, ans: AnswerQuestion):
        conn.execute("INSERT INTO AnswerQuestion VALUES(?, ?, ?, ?, ?);",(astuple(ans)))
        conn.commit()
    
    @staticmethod
    def get_all_answers(conn: Connection) -> list[AnswerQuestion]:
        res = conn.execute("SELECT * FROM AnswerQuestion;",).fetchall()
        return convert_to_model(res, AnswerQuestion)
    
    @staticmethod
    def get_answers(conn: Connection, id_question: str) -> list[AnswerQuestion]:
        res = conn.execute("SELECT * FROM AnswerQuestion WHERE id_question = ?", (id_question,)).fetchall()
        l = convert_to_model(res, AnswerQuestion)
        
        if(l is None) : 
            return [] ; 
        
        for ans in l :
            ans.convert_int_to_bool()
        return l 
    
    @staticmethod
    def get_answers_with_position(conn: Connection, id_question: str, index : int) -> AnswerQuestion:
        res = conn.execute("SELECT * FROM AnswerQuestion WHERE id_question = ? AND position = ? ;", (id_question,index)).fetchone()
        ans = convert_to_model(res, AnswerQuestion)
        
        if(ans is None) : 
            return None ; 
        
        ans.convert_int_to_bool()
    
        return ans
    
    @staticmethod
    def get_answer_by_id(conn: Connection, id_answer: str) -> AnswerQuestion:
        res = conn.execute("SELECT * FROM AnswerQuestion WHERE id = ?;", (id_answer,)).fetchone()
        return convert_to_model(res, AnswerQuestion)
    
    @staticmethod
    def get_good_answer_with_question_id(conn: Connection, id_question: str) -> AnswerQuestion:
        res = conn.execute("SELECT * FROM AnswerQuestion WHERE id_question = ? AND isCorrect = True;", (id_question,)).fetchone()
        return convert_to_model(res, AnswerQuestion)
    
    @staticmethod
    def update_answer_question(conn: Connection, ans: AnswerQuestion):
        conn.execute(
            """
            UPDATE AnswerQuestion
            SET id_question = ?,
                content = ?,
                isCorrect = ?
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