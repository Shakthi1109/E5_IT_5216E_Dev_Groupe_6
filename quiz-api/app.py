import sqlite3
import os

from flask import Flask, jsonify
from flask_cors import CORS
from services.question_services import *

def get_db_connection():
    SCRIPT_DIR = os.path.dirname(__file__)
    DATABASE_FILE = os.path.join(SCRIPT_DIR, 'database.db')
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/questions')
def questions():
    conn = get_db_connection()
    return QuestionsService.get_questions(conn)

if __name__ == "__main__":
    app.run()