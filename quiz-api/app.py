import sqlite3

from flask import Flask
from flask_cors import CORS
from services.QuestionsService import *

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/quiz-info')
def quiz_info():
    conn = get_db_connection()
    return str(QuestionsService.get_questions(conn))

if __name__ == "__main__":
    app.run()