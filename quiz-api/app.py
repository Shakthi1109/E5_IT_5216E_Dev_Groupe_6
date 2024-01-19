import sqlite3
import os
import uuid 

from jwt_utils import *
from services.question_services import *
from services.participations_services import *
from services.result_services import *
from database_utils import generate_structure 

from datetime import datetime
from typing import Callable
from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps


def generate_uuid():
    return str(uuid.uuid4())

def get_db_connection():
    SCRIPT_DIR = os.path.dirname(__file__)
    DATABASE_FILE = os.path.join(SCRIPT_DIR, 'quiz.db')
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def is_admin_authenticated():
    def decorator(func: Callable):
        @wraps(func)
        def wrapped(*args, **kwargs):
            authorization_header = request.headers.get("Authorization")
            if authorization_header is None:
                return jsonify({'message': 'Unauthorized'}), 401
            
            token = authorization_header.replace("Bearer", "")
            decoded = decode_token(token)
            if decoded != "quiz-app-admiun":
                return jsonify({'message': 'Unauthorized'}), 401
            
            return func(*args, **kwargs)
        return wrapped
    return decorator


app = Flask(__name__)
CORS(app)


@app.before_first_request
def setup_db():
    generate_structure(get_db_connection())


@app.route('/')
def main():
    return "Hello world!"


"""
### Cette fonction permet de récupérer des informations d'ordre général sur le quiz.
"""
@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    
    size = QuestionsService.get_numbers_questions(get_db_connection())
    scores = ParticipationsService.get_all_participations(get_db_connection())
    if(scores == None) : scores = []
    
    participations = sorted(scores, key=lambda x: x.score, reverse=True)
    
    quiz_info = {
        'size': size,  
        'scores': participations
    }
    
    return jsonify(quiz_info), 200


@app.route('/questions-all', methods=['GET'])
def get_question_all():
    questions = QuestionsService.get_questions(get_db_connection())
    return jsonify({'questions': questions}), 200

@app.route('/answers-questions-all', methods=['GET'])
def get_answers_question_all():
    a = QuestionsService.get_all_answers(get_db_connection())
    return jsonify({'answers-questions': a}), 200

"""
### Route pour récupérer une question par son identifiant
"""
@app.route('/questions/<questionId>', methods=['GET'])
def get_question_by_id(questionId):
    
    question = QuestionsService.get_question_by_id(get_db_connection(), str(questionId))

    if(question == None) :
        return {}, 404
    
    answers = QuestionsService.get_answers(get_db_connection(), str(questionId))
    
    question_data = {
        #'question': {
            'id': question.id,
            'title': question.titre,
            'position': question.position,
            'text': question.question,
            'image': question.image,
            'possibleAnswers': answers
        #}
    }
    
    return jsonify(question_data), 200

"""
### Route pour récupérer une question par sa position
"""
@app.route('/questions', methods=['GET'])
def get_question_by_position():
    position = int(request.args.get('position', -1)) 
    question = QuestionsService.get_question_by_position(get_db_connection(), position)
    
    if(question == None) :
        return {}, 404
    
    answers = QuestionsService.get_answers(get_db_connection(), question.id)
    
    question_data = {
        'id': question.id,
        'title': question.titre,
        'position': question.position,
        'text': question.question,
        'image': question.image,
        'possibleAnswers': answers
    }
        
    return jsonify(question_data), 200


"""
### Route pour soumettre les réponses d'un joueur
"""
@app.route('/participations', methods=['POST'])
def submit_participation():
    data = request.json # data de la request POST 

    player_name = data.get('playerName')
    list_answers = data.get('answers')
    
    if(player_name == None or list_answers == None):
        return jsonify({"message": "La participation envoyée ne possède pas le bon format."}), 400
    
    
    nb_questions = QuestionsService.get_numbers_questions(get_db_connection())
    
    if(len(list_answers) != nb_questions) : 
        return jsonify({"message": "Le nombre de réponse n'est pas suffisant. Il n'est pas égal au nombre de questions."}), 400
    
    score = 0 
    index_position = 1 ; 
    for answer_index in list_answers :
        
        question = QuestionsService.get_question_by_position(get_db_connection(), index_position)
        answers_question = QuestionsService.get_answers_with_position(get_db_connection(), question.id, answer_index)
        
        if(answers_question == None): continue 
        
        if(answers_question.isCorrect == True) :
            score += 1
        
        index_position += 1 
       
    response = {
        'playerName': player_name,
        'score': score
    }
    
    part = Participation()
    part.id = generate_uuid()
    part.playerName = player_name
    part.score = score 
    part.date = datetime.now()
    
    ParticipationsService.create_new_participation(get_db_connection(), part)
    
    return jsonify(response), 200


"""
### Route pour se connecter en tant qu'administrateur
"""
@app.route('/login', methods=['POST'])
def admin_login():
    data = request.json
    provided_password = data.get('password', '')
    admin_password = "flask2023"
    if provided_password == admin_password:
        admin_token = build_token()
        return jsonify({'token': str(admin_token)}), 200
    else:
        return jsonify({'message': 'Mot de passe incorrect'}), 401  # Unauthorized
    

#####################################################################################
#
#                               ROUTE ADMIN
#
#####################################################################################Z

"""
### Cette fonction permet d'ajouter une question au quiz.
"""
@app.route('/questions', methods=['POST'])
def create_question():
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    possibleAnswers = data.get('possibleAnswers')
    
    question = Question()
    question.id = generate_uuid()
    question.position = data.get('position')
    question.question = data.get('text')
    question.titre = data.get('title')
    question.image = data.get('image')
    QuestionsService.create_question(get_db_connection(), question)
    
    position_index_answer = 1
    for answer in possibleAnswers:
        a = AnswerQuestion()
        a.id = generate_uuid()
        a.id_question = question.id
        a.text = answer.get('text')
        a.isCorrect = answer.get('isCorrect')
        a.position = position_index_answer
        QuestionsService.create_answer_question(get_db_connection(), a)
        position_index_answer += 1
    
    return {'id': question.id}, 200

"""
### Cette fonction permet de mettre à jour une question du quiz à partir de son identifiant base de données.
"""
@app.route('/questions/<questionId>', methods=['PUT'])
def update_question(questionId):
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json    
    possibleAnswers = data.get('possibleAnswers')
   
    question = Question()
    question.id = questionId
    question.position = data.get('position')
    question.question = data.get('text')
    question.titre = data.get('title')
    question.image = data.get('image')
    
    if(QuestionsService.question_exists(get_db_connection(), question.id) == False):
        return {}, 404
    
    QuestionsService.update_question(get_db_connection(), question)
    QuestionsService.delete_answers_question_by_id(get_db_connection(), question.id)
    
    position_index_answer = 1
    for answer in possibleAnswers : 
        a = AnswerQuestion()
        a.id = generate_uuid()
        a.id_question = question.id
        a.text = answer.get('text')
        a.isCorrect = answer.get('isCorrect')
        a.position = position_index_answer
        QuestionsService.create_answer_question(get_db_connection(), a)
        position_index_answer += 1
        
    return jsonify({'ok': 'ok'}), 204


"""
### Cette fonction permet de supprimer une question du quiz à partir de son identifiant en base de données.
"""
@app.route('/questions/<questionId>', methods=['DELETE'])
def delete_question(questionId):

    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401


    if(QuestionsService.question_exists(get_db_connection(), questionId) == False):
        return {}, 404
    
    try:
        result = QuestionsService.delete_question_by_id(get_db_connection(), questionId)
        QuestionsService.delete_answers_question_by_id(get_db_connection(), questionId)
    except:
        pass
    
    # Service delete 

    return {}, 204

"""
### Cette fonction permet de supprimer toutes les questions (et leurs réponses respectives) du quiz.
"""
@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    QuestionsService.delete_all_questions(get_db_connection())
    QuestionsService.delete_all_anwsers_questions(get_db_connection())
    
    return {}, 204


"""
### Cette fonction permet de supprimer toutes les participations du quiz.
"""
@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    ParticipationsService.delete_all_results(get_db_connection())
    return {}, 204


"""
### Permet de rebuild la database
"""
@app.route('/rebuild-db', methods=['POST'])
@is_admin_authenticated
def rebuild_db():
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    generate_structure(get_db_connection())
    return jsonify({'message': 'Success'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)


