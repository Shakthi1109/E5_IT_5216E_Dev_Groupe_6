import sqlite3
import os

from jwt_utils import * 

from flask import Flask, jsonify, request
from flask_cors import CORS
from services.question_services import *
from services.participations_services import *
import uuid 

def generate_uuid():
    return str(uuid.uuid4())

def get_db_connection():
    SCRIPT_DIR = os.path.dirname(__file__)
    DATABASE_FILE = os.path.join(SCRIPT_DIR, 'database.db')
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
CORS(app)


@app.route('/')
def main():
    
    routes_get = ["/questions", "/questions-all", "/answers-questions-all", "/quiz-info", "/questions/1", "/questions?position=1", "/simulate-post/participations", "/simulate-post/login", "/simulate-post/questions", "/simulate-put/questions", "/simulate-delete/questions-1","/simulate-delete/questions-all", "/simulate-delete/participations-all"]
    html = ""
    for r in routes_get : 
        html += f"<a href={r}><button>{r}</button></a><br/>"
    
    return html



######################################################################################################
"""
UNIQUEMENT POUR SIMULER LES TESTS
"""
import requests
def simulate_request(type, route, data):
    url = f"http://127.0.0.1:5000{route}"
    headers = {'Content-Type': 'application/json'}  
    response = None
    
    if type == "post":
        response = requests.post(url, json=data, headers=headers)
        
    elif type == "put":
        response = requests.put(url, json=data, headers=headers)
        
    elif type == "delete":
        response = requests.delete(url, json=data, headers=headers)
        
    return response

@app.route('/simulate-post/<route>', methods=['GET'])
def simulate_post(route):
    routes_post = {"/participations" : {'surnom':'Mathieu'}, "/login": {'password': 'mot de passe'}, "/questions": {'content': 'Quelle est la question ?'}}
    route = "/"+route
    data = routes_post[route]
    
    response = simulate_request("post", route, data)
    return response.json(), 200

@app.route('/simulate-put/<route>', methods=['GET'])
def simulate_put(route):
    routes_post = {"questions" : {"route_total" : "questions/1", "content": "La question a été changé", "Réponse": True}}
    data = routes_post[route]
    route = "/"+data["route_total"]
    
    response = simulate_request("put", route, data)
    resp = "OK"
    if response != None : resp = str(response)
    
    return resp, 200

@app.route('/simulate-delete/<route>', methods=['GET'])
def simulate_delete(route):
    routes_post = {"questions-1" : {"route_total" : "questions/1", "content": "La question a été supprimé"}, 
                   "questions-all" : {"route_total" : "questions/all", "content": "Toutes les questions ont été supprimé"},
                   "participations-all" : {"route_total" : "participations/all", "content": "Toutes les questions ont été supprimé"}
                   }
    data = routes_post[route]
    route = "/"+data["route_total"]
        
    response = simulate_request("delete", route, data)
    return "OK", 200


######################################################################################################




"""
# GET quiz-info
    Cette fonction permet de récupérer des informations d’ordre général sur le quiz.

## Authentification
    Publique

## Paramètres : 
    Aucun
    
## Retour
    HTTP : 200 - Ok
    Payload de retour :
    - size : Entier positif retournant le nombre de questions contenues dans le quiz
    - scores : tableau d’objets participation trié par scores décroissants et dont chaque entrée donne :
        - playerName : nom du joueur
        - score : score obtenu à l’époque
        - date : date de la participation au format dd/MM/yyyy hh:mm:ss
"""
@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    
    questions = QuestionsService.get_questions(get_db_connection())
    scores = ParticipationsService.get_all_participations(get_db_connection())
    size = 0
    if(scores == None) : scores = []
    if(questions != None) : len(questions)
    
    quiz_info = {
        'size': size,  
        'scores': scores
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
Route pour récupérer une question par son identifiant

## GET /questions/{questionId}
    Cette fonction permet de récupérer le contenu d’une question à partir de son identifiant de base de données.

Authentification : Publique

Paramètres d’URL : questionId - entier positif désignant l’identifiant de la question

Retour : HTTP : 200 - Ok

Payload de retour :
- question : objet contenant les détails de la question
    - id : id base de données de la question
    - title : texte contenant le titre de la question
    - position : position de la question dans le quiz (normalement identique au paramètre d’entrée...)
    - text : intitulé de la question
    - image : une image au format base 64 associée à la question
    - possibleAnswers : liste des réponses possibles contenant chacune :
        - id : id base de données de la réponse
        - text : intitulé de la réponse
        - isCorrect : booléen indiquant si la réponse est la bonne ou non
"""
@app.route('/questions/<int:questionId>', methods=['GET'])
def get_question_by_id(questionId):
    
    question = QuestionsService.get_question_by_id(get_db_connection(), str(questionId))
    answers = QuestionsService.get_answers(get_db_connection(), str(questionId))
    
    if(question == None) :
        return jsonify({"message": "La question correspondant à l'ID n'a pas été trouvé."}), 404
    
    question_data = {
        'question': {
            'id': question.id,
            'title': question.titre,
            'position': question.position,
            'text': question.question,
            'image': question.image,
            'possibleAnswers': answers
        }
    }
    return jsonify(question_data), 200

"""
Route pour récupérer une question par sa position

## GET /questions?position={position}
    Cette fonction permet de récupérer le contenu d’une question à partir de sa position dans le quiz.

Authentification : Publique

Paramètres d’URL : 
    - position : entier positif désignant le numéro de la question

Retour : HTTP : 200 - Ok

Payload de retour :
- question : objet contenant les détails de la question
    - id : id base de données de la question
    - title : texte contenant le titre de la question
    - position : position de la question dans le quiz (normalement identique au paramètre d’entrée...)
    - text : intitulé de la question
    - image : une image au format base 64 associée à la question
    - possibleAnswers : liste des réponses possibles contenant chacune :
        - id : id base de données de la réponse
        - text : intitulé de la réponse
        - isCorrect : booléen indiquant si la réponse est la bonne ou non
"""
@app.route('/questions', methods=['GET'])
def get_question_by_position():
    position = int(request.args.get('position', -1)) 
    question = QuestionsService.get_question_by_position(get_db_connection(), position)
    answers = QuestionsService.get_answers(get_db_connection(), position)
    
    if(question == None) :
        return jsonify({"message": "La question correspondant à la position donnée n'a pas été trouvée."}), 404
    
    question_data = {
        'question': {
            'id': question.id,
            'title': question.titre,
            'position': question.position,
            'text': question.question,
            'image': question.image,
            'possibleAnswers': answers
        }
    }
    return jsonify(question_data), 200


"""
Route pour soumettre les réponses d'un joueur

## POST /participations
    Cette fonction permet d’envoyer la liste des réponses sélectionnées par un participant pour l’ensemble du quiz.
    L’avantage est de permettre une validation d’un bloc de l’ensemble du questionnaire limitant ainsi fortement le nombre de cas à la marge susceptibles de générer des états incohérents.

Authentification : publique

Paramètres :
    - player_name : le nom du joueur qui poste son questionnaire
    - answers : la liste des positions de réponses choisies dans l’ordre des questions du quiz

Retour : HTTP : 200 - Ok

Payload de retour :
- answersSummaries : tableau de type answerSummary, dont chaque entrée donne, dans l’ordre des questions du quiz : 
    - correctAnswerPosition : position de la réponse correcte à la question
    - wasCorrect : état de la réponse fournie par le joueur
- playerName : nom du joueur tel qu’il a été saisi au début du quiz
- score : score obtenu
"""
@app.route('/participations', methods=['POST'])
def submit_participation():
    data = request.json # data de la request POST 
    """
    data = {
        'player_name': "Mathieu",
        'answers': [{'question_id':"1", "answer_choice_id":"3"}]
    }
    """
    
    player_name = data.get('player_name')
    if(player_name == None or data.get('answers') == None):
        return jsonify({"message": "La participation envoyée ne possède pas le bon format."}), 404
    
    answers = []
    score = 0 
    
    for answer in data.get('answers') :
        question_id = answer.get('question_id')
        answer_choice = answer.get('answer_choice_id')
        
        correctAnswer = QuestionsService.get_good_answer_with_question_id(get_db_connection(), question_id)
        correctAnswerPosition = None
        
        if(correctAnswer != None): correctAnswerPosition = correctAnswer.id
        
        wasCorrect = answer_choice == correctAnswerPosition 
        answers.append({
            'correctAnswerPosition':correctAnswerPosition,
            'wasCorrect': wasCorrect
        })
        if(wasCorrect) : score += 1
        

    response = {
        'answersSummaries': answers,
        'playerName': player_name,
        'score': score
    }
    
    return jsonify(response), 200


"""
Route pour se connecter en tant qu'administrateur

## POST /login
    Cette fonction permet d’obtenir un token d’authentification en tant qu’administrateur du site. 
    Ce token n’est fourni que si le mot de passe fourni est évidemment le bon 

Authentification : Publique

Paramètres :
    - password : mot de passe

Retour : HTTP : 200 - Ok

Payload de retour :
- token : le token en question si le mot de passe est le bon
"""
@app.route('/login', methods=['POST'])
def admin_login():
    data = request.json
    provided_password = data.get('password', '')
    admin_password = "mot de passe"
    if provided_password == admin_password:
        #admin_token = build_token()
        admin_token = 'zdk240FQpa24'
        return jsonify({'token': str(admin_token)}), 200
    else:
        return jsonify({'message': 'Mot de passe incorrect'}), 401  # Unauthorized



#####################################################################################
#
#                               ROUTE ADMIN
#
#####################################################################################

def is_admin_authenticated(authorization_header):
    
    # utiliser decode_token()
    return True 


"""
Créer une nouvelle question - POST /questions

Cette fonction permet d’ajouter une question au quiz.

Authentification : Administrateur

Paramètres du corps de requête :
- title : le titre de la question
- text : la question en tant que telle
- image : image en base 64
- position : la position de la question dans le quiz. Peut provoquer un décalage des positions des autres questions si cette position est déjà prise. Il est interdit de mettre une position supérieure au nombre de questions déjà en base.
- possibleAnswers : liste des réponses possibles contenant chacune :
  - text : l’intitulé de la réponse elle-même
  - isCorrect : booléen indiquant si la réponse est la bonne ou non (vérification à prévoir pour éviter les doublons)

Retour : HTTP : 200 - Ok
Payload de retour :
- id : identifiant en base de données de la question créée
"""
@app.route('/questions', methods=['POST'])
def create_question():
    
    #print("POST /questions")
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    possibleAnswers = data.get('possibleAnswers')
    
    possibleAnswers = [{'text': 'La réponse A', 'isCorrect': True}, {'text': 'La réponse B', 'isCorrect':False}, {'text': 'La réponse C', 'isCorrect':False}, {'text': 'La réponse D', 'isCorrect':False}]
    data = {
        'title': "Titre de la question",
        'text' : "Quelle est la question ?",
        'image' : None,
        'position' : 2,
        'possibleAnswers' : possibleAnswers
    }    
    
    question = Question()
    question.id = generate_uuid()
    question.position = data.get('position')
    question.question = data.get('text')
    question.titre = data.get('title')
    question.image = data.get('image')
    QuestionsService.create_question(get_db_connection(), question)
    
    #print("Question saved : ",question)
    
    for answer in possibleAnswers:
        a = AnswerQuestion()
        a.id = generate_uuid()
        a.id_question = question.id
        a.content = answer.get('text')
        a.is_correct = answer.get('isCorrect')
        QuestionsService.create_answer_question(get_db_connection(), a)
    
    return {'id': question.id}, 200

"""
Mettre à jour une question - PUT /questions/{questionId}

Cette fonction permet de mettre à jour une question du quiz à partir de son identifiant base de données.

Authentification : Administrateur

Paramètres d’URL :
- questionId : identifiant en base de données de la question

Paramètres de corps de requête :
- title : le titre de la question
- text : l’intitulé de la question
- image : image en base 64
- position : la position (potentiellement nouvelle) de la question dans le quiz. Peut provoquer un décalage des positions des autres questions si cette position est déjà prise. Il est interdit de mettre une position supérieure au nombre de questions déjà en base.
- possibleAnswers : liste des réponses possibles contenant chacune :
  - text : l’intitulé de la réponse
  - isCorrect : booléen indiquant si la réponse est la bonne ou non (vérification à prévoir pour éviter les doublons)

Retour : HTTP : 204 - No Content
Payload de retour : vide
"""
@app.route('/questions/<questionId>', methods=['PUT'])
def update_question(questionId):
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    possibleAnswers = data.get('possibleAnswers')
    
    questionId = '43a00831-1b67-408e-8ff7-cbb39cbd4c51'
    possibleAnswers = [{'text': 'La réponse A', 'isCorrect': True}, {'text': 'La réponse B', 'isCorrect':False}, {'text': 'La réponse C', 'isCorrect':False}, {'text': 'La réponse D', 'isCorrect':False}]
    data = {
        'title': "Titre de la question *updated",
        'text' : "Quelle est la question ?",
        'image' : None,
        'position' : 2,
        'possibleAnswers' : possibleAnswers
    }
    
    question = Question()
    question.id = questionId
    question.position = data.get('position')
    question.question = data.get('text')
    question.titre = data.get('title')
    question.image = data.get('image')
    QuestionsService.update_question(get_db_connection(), question)
    QuestionsService.delete_answers_question_by_id(get_db_connection(), question.id)
    
    for answer in possibleAnswers : 
        a = AnswerQuestion()
        a.id = generate_uuid()
        a.id_question = question.id
        a.content = answer.get('text')
        a.is_correct = answer.get('isCorrect')
        QuestionsService.create_answer_question(get_db_connection(), a)
        
    return jsonify({'ok': 'ok'}), 204


"""
Supprimer une question - DELETE /questions/{questionId}

Cette fonction permet de supprimer une question du quiz à partir de son identifiant en base de données.

Authentification : Administrateur

Paramètres d’URL :
- questionId : identifiant de la question en base de données

Retour : HTTP : 204 - No Content
Payload de retour : vide
"""
@app.route('/questions/<questionId>', methods=['DELETE'])
def delete_question(questionId):

    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    #questionId = "43a00831-1b67-408e-8ff7-cbb39cbd4c51"
    try:
        result = QuestionsService.delete_question_by_id(get_db_connection(), questionId)
        QuestionsService.delete_answers_question_by_id(get_db_connection(), questionId)
    except:
        pass
    
    # Service delete 

    return {}, 204

"""
Supprimer toutes les questions - DELETE /questions/all

Cette fonction permet de supprimer toutes les questions (et leurs réponses respectives) du quiz.

Authentification : Administrateur

Paramètres d’URL : Aucun

Retour : HTTP : 204 - No Content
Payload de retour : vide
"""
@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    QuestionsService.delete_all_questions(get_db_connection())
    QuestionsService.delete_all_anwsers_questions(get_db_connection())
    
    return {}, 204


"""
Supprimer toutes les participations - DELETE /participations/all

Cette fonction permet de supprimer toutes les participations du quiz.

Authentification : Administrateur

Paramètres d’URL : Aucun

Retour : HTTP : 204 - No Content
Payload de retour : vide
"""
@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    ResultsService.delete_all_results()
    return {}, 204

if __name__ == '__main__':
    app.run(debug=True)



"""
@app.route('/questions')
def questions():
    conn = get_db_connection()
    return QuestionsService.get_questions(conn)
"""
