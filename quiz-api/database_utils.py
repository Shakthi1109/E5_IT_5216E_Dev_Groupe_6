import uuid
from typing import TypeVar
from sqlite3 import Row
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