from sqlite3 import Connection
from entities.Participation import Participation
from database_utils import convert_to_model
from dataclasses import astuple

class ParticipationsService : 

    @staticmethod
    def delete_all_results(conn : Connection) -> None:
        conn.execute("DELETE FROM Participation;")
        conn.commit()
    
    
    @staticmethod
    def delete_all_results_by_question(conn : Connection, id_question: str) -> None:
        conn.execute("DELETE * FROM ResultQuestion WHERE id_question = ?;", (id_question,))
        conn.commit()
    
    @staticmethod
    def create_new_participation(conn: Connection, part: Participation):
        conn.execute("INSERT INTO Participation VALUES(?, ?, ?, ?);",(astuple(part)))
        conn.commit()
    
    @staticmethod
    def get_all_participations(conn: Connection) -> list[Participation]:
        res = conn.execute("SELECT * FROM Participation;").fetchall()
        return convert_to_model(res, Participation)