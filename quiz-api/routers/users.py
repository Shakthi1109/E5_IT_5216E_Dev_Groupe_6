from flask import Blueprint, jsonify, request
from datetime import datetime

from jwt_utils import build_token
from dependencies import get_db_connection, generate_uuid
from entities.Participation import Participation
from services.question_services import QuestionsService
from services.participations_services import ParticipationsService


user_page = Blueprint("user_page", __name__)


"""
### Cette fonction permet de récupérer des informations d'ordre général sur le quiz.
"""
@user_page.route('/quiz-info', methods=['GET'])
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


@user_page.route('/questions-all', methods=['GET'])
def get_question_all():
    questions = QuestionsService.get_questions(get_db_connection())
    return jsonify({'questions': questions}), 200

@user_page.route('/answers-questions-all', methods=['GET'])
def get_answers_question_all():
    answers = QuestionsService.get_all_answers(get_db_connection())
    return jsonify({'answers-questions': answers}), 200

"""
### Route pour récupérer une question par son identifiant
"""
@user_page.route('/questions/<questionId>', methods=['GET'])
def get_question_by_id(questionId):
    
    question = QuestionsService.get_question_by_id(get_db_connection(), str(questionId))

    if (question == None) :
        return {}, 404
    
    answers = QuestionsService.get_answers(get_db_connection(), str(questionId))
    
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
### Route pour récupérer une question par sa position
"""
@user_page.route('/questions', methods=['GET'])
def get_question_by_position():
    position = int(request.args.get('position', -1)) 
    question = QuestionsService.get_question_by_position(get_db_connection(), position)
    
    if (question == None) :
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
@user_page.route('/participations', methods=['POST'])
def submit_participation():
    data = request.json # data de la request POST
    if not data:
        return jsonify({"message": "La participation envoyée ne possède pas le bon format."}), 400

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

@user_page.route("/participations", methods=["GET"])
def get_participations():
    data = ParticipationsService.get_all_participations(get_db_connection())
    return jsonify(data), 200

"""
### Route pour se connecter en tant qu'administrateur
"""
@user_page.route('/login', methods=['POST'])
def admin_login():
    data = request.json
    if not data:
        return jsonify({"message": "La requete envoyée ne possède pas le bon format."}), 400

    provided_password = data.get('password', '')
    admin_password = "flask2023"
    if provided_password == admin_password:
        admin_token = build_token()
        return jsonify({'token': str(admin_token)}), 200
    else:
        return jsonify({'message': 'Mot de passe incorrect'}), 401  # Unauthorized