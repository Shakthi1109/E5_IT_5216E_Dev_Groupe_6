from sqlite3 import Connection
from entities.ResultQuestion import ResultQuestion
from database_utils import convert_to_model
from dataclasses import astuple

class ResultsService : 

    @staticmethod
    def create_results(conn: Connection, result: ResultQuestion):
        conn.execute(
            "INSERT INTO ResultQuestion VALUES(?, ?, ?);",
            *astuple(result)
        )
        conn.commit()

    @staticmethod
    def get_results_sorted(conn: Connection) -> list[ResultQuestion]:
        res = conn.execute("SELECT * FROM ResultQuestion ORDER BY id;").fetchall()
        return convert_to_model(res, ResultQuestion)

    @staticmethod
    def delete_result(conn: Connection, id_result: str):
        conn.execute("DELETE FROM ResultQuestion WHERE id = ?", (id_result,))
        conn.commit()

    @staticmethod
    def delete_all_results(conn: Connection):
        conn.execute("DELETE FROM ResultQuestion;")
        conn.commit()