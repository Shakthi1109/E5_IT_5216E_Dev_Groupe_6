from flask import Blueprint, jsonify

from dependencies import *
from database_utils import generate_structure
from entities.Question import Question
from entities.AnswerQuestion import AnswerQuestion
from services.question_services import QuestionsService
from services.participations_services import ParticipationsService


admin_page = Blueprint("admin_page", __name__)


"""
### Cette fonction permet d'ajouter une question au quiz.
"""
@admin_page.route('/questions', methods=['POST'])
@is_admin_authenticated()
def create_question():
    data = request.json
    if not data:
        return jsonify({"message": "La requete envoyée ne possède pas le bon format."}), 400

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
@admin_page.route('/questions/<questionId>', methods=['PUT'])
@is_admin_authenticated()
def update_question(questionId):
    data = request.json
    if not data:
        return jsonify({"message": "La requete envoyée ne possède pas le bon format."}), 400
  
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
@admin_page.route('/questions/<questionId>', methods=['DELETE'])
@is_admin_authenticated()
def delete_question(questionId):
    if(QuestionsService.question_exists(get_db_connection(), questionId) == False):
        return {}, 404
    
    QuestionsService.delete_question_by_id(get_db_connection(), questionId)
    QuestionsService.delete_answers_question_by_id(get_db_connection(), questionId)

    return {}, 204


"""
### Cette fonction permet de supprimer toutes les questions (et leurs réponses respectives) du quiz.
"""
@admin_page.route('/questions/all', methods=['DELETE'])
@is_admin_authenticated()
def delete_all_questions():
    QuestionsService.delete_all_questions(get_db_connection())
    QuestionsService.delete_all_anwsers_questions(get_db_connection())
    
    return {}, 204


"""
### Cette fonction permet de supprimer toutes les participations du quiz.
"""
@admin_page.route('/participations/all', methods=['DELETE'])
@is_admin_authenticated()
def delete_all_participations():
    ParticipationsService.delete_all_participations(get_db_connection())
    return {}, 204


"""
### Permet de rebuild la database
"""
@admin_page.route('/rebuild-db', methods=['POST'])
@is_admin_authenticated()
def rebuild_db():
    generate_structure(get_db_connection())
    return 'Ok', 200