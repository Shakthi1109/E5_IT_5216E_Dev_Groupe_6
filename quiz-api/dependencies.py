import uuid
import sqlite3
import os

from typing import Callable
from flask import request, jsonify
from functools import wraps
from jwt_utils import decode_token

def generate_uuid():
    return str(uuid.uuid4())

def get_db_connection():
    SCRIPT_DIR = os.path.dirname(__file__)
    DATABASE_FILE = os.path.join(SCRIPT_DIR, 'quiz.db')
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def is_admin_authenticated(*args):
    def decorator(func: Callable):
        @wraps(func)
        def wrapped(*args, **kwargs):
            authorization_header = request.headers.get("Authorization")
            if authorization_header is None:
                return jsonify({'message': 'Unauthorized'}), 401
            
            token = authorization_header.replace("Bearer ", "")
            decoded = decode_token(token)
            
            if decoded != "quiz-app-admin":
                return jsonify({'message': 'Unauthorized'}), 401
            
            return func(*args, **kwargs)
        return wrapped
    return decorator