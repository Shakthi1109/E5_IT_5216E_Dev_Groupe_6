from sqlite3 import Connection
from entities.Participation import Participation
from database_utils import convert_to_model
from dataclasses import astuple

class ParticipationsService : 

    @staticmethod(function)
    def delete_all_results(conn : Connection) -> None:
        conn.execute("DELETE * FROM ResultQuestion;")
        conn.commit()

    @staticmethod(function)
    def delete_all_results_by_question(conn : Connection, id_question: str) -> None:
        conn.execute("DELETE * FROM ResultQuestion WHERE id_question = %s;", (id_question,))
        conn.commit()
    
    def create_new_participation(conn: Connection, part: Participation):
        conn.execute(
            "INSERT INTO Participation VALUES(%s, %s, %s, %s);",
            *astuple(part)
        )
        conn.commit()

    def get_all_participations(conn: Connection) -> list[Participation]:
        res = conn.execute("SELECT * FROM Participation;").fetchall()
        return convert_to_model(res, Participation)