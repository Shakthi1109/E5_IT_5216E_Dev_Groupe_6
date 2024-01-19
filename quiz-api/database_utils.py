import uuid
from typing import TypeVar
from sqlite3 import Row, Connection
from dataclasses import is_dataclass

T = TypeVar("T")

def generate_uuid() -> str:
    return str(uuid.uuid4())

def convert_to_model(
    request_res: list[Row] | Row | None,
    model: T
) -> list[T] | T | None:
    if not request_res:
        return None
    
    if not is_dataclass(model):
        raise ValueError(f"{type(model)} is not a dataclass")

    if isinstance(request_res, list):
        res: list[T] = []
        for row in request_res:
            res.append(model(*[row[field.name] for field in model.__dataclass_fields__.values()]))
        return res

    return model(*[request_res[field.name] for field in model.__dataclass_fields__.values()])

def generate_structure(conn: Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id       TEXT (36) PRIMARY KEY,
            email    TEXT,
            password TEXT,
            type     INTEGER
        );"""
    )
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Participation (
            id     TEXT (36) PRIMARY KEY,
            pseudo TEXT,
            score  INTEGER,
            date   TEXT
        );"""
    )
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Question (
            id       TEXT (36) PRIMARY KEY,
            position INTEGER,
            question TEXT,
            titre    TEXT,
            image    TEXT
        );"""
    )
    conn.execute("""
        CREATE TABLE IF NOT EXISTS  Result (
            id     TEXT (36) PRIMARY KEY,
            pseudo TEXT,
            date   TEXT
        );"""
    )
    conn.execute("""
        CREATE TABLE IF NOT EXISTS AnswerQuestion (
            id          TEXT (36),
            id_question TEXT (36),
            text        TEXT,
            isCorrect   INTEGER,
            position    INTEGER,
            PRIMARY KEY (
                id
            ),
            FOREIGN KEY (
                id_question
            )
            REFERENCES Question (id) 
        );"""
    )
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ResultQuestion (
            id                 TEXT (36) PRIMARY KEY,
            id_question        TEXT (36) REFERENCES Question (id),
            id_answer_question TEXT (36) REFERENCES AnswerQuestion (id) 
        );"""
    )
    conn.commit()