import sqlite3
import os

from jwt_utils import * 

from flask import Flask, jsonify, request
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
def main():
    
    routes_get = ["/questions", "/quiz-info", "/questions/1", "/questions?position=1", "/simulate-post/participations", "/simulate-post/login", "/simulate-post/questions", "/simulate-put/questions", "/simulate-delete/questions-1","/simulate-delete/questions-all", "/simulate-delete/participations-all"]
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
    routes_post = {"/participations" : {'surnom':'Mathieu'}, "/login": {'password': 'your_password'}, "/questions": {'content': 'Quelle est la question ?'}}
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
    return response.json(), 200

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
    - scores : tableau d’objets participationResult trié par scores décroissants et dont chaque entrée donne :
        - playerName : nom du joueur
        - score : score obtenu à l’époque
        - date : date de la participation au format dd/MM/yyyy hh:mm:ss
"""
@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    
    quiz_info = {
        'size': 10,  # Nombre de questions dans le quiz
        'scores': [
            {'playerName': 'Joueur1', 'score': 80, 'date': '01/01/2023 10:30:45'},
            {'playerName': 'Joueur2', 'score': 75, 'date': '02/01/2023 12:15:20'},
        ]
    }
    
    return jsonify(quiz_info), 200

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
    
    question_data = {
        'id': 1,
        'title': 'Question 1',
        'position': 1,
        'text': 'Quelle est la capitale de la France?',
        'image': 'base64_encoded_image_data',
        'possibleAnswers': [
            {'id': 1, 'text': 'Paris', 'isCorrect': True},
            {'id': 2, 'text': 'Berlin', 'isCorrect': False},
        ]
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
    position = int(request.args.get('position', 1)) 
    question_data = {
        'id': 1,
        'title': f'Question {position}',
        'position': position,
        'text': f'Contenu de la question {position}',
        'image': 'base64_encoded_image_data',
        'possibleAnswers': [
            {'id': 1, 'text': 'Réponse 1', 'isCorrect': True},
            {'id': 2, 'text': 'Réponse 2', 'isCorrect': False},
        ]
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
    print(f"== POST Participations, Data :{data}")
    return data, 200


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
    print(f"== POST login, Data :{data}")
    provided_password = data.get('password', '')
    admin_password = "motdepasse"
    if provided_password == admin_password:
        admin_token = build_token()
        return jsonify({'token': admin_token}), 200
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
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json

    # Service Create question

    return {'OK': data}, 200

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
@app.route('/questions/<int:questionId>', methods=['PUT'])
def update_question(questionId):
    
    print(f"== UPDATE Question : {questionId}")
    
    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json

    # Service update questions
    
    return {'OK': data}, 200


"""
Supprimer une question - DELETE /questions/{questionId}

Cette fonction permet de supprimer une question du quiz à partir de son identifiant en base de données.

Authentification : Administrateur

Paramètres d’URL :
- questionId : identifiant de la question en base de données

Retour : HTTP : 204 - No Content
Payload de retour : vide
"""
@app.route('/questions/<int:questionId>', methods=['DELETE'])
def delete_question(questionId):

    if not is_admin_authenticated(request.headers.get('Authorization')):
        return jsonify({'message': 'Unauthorized'}), 401

    print(f"== Service delete questions {questionId}")
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

    print(f"== Service delete all questions")
    
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

    print("== Service delete ALL Participations")
    
    return {}, 204

if __name__ == '__main__':
    app.run(debug=True)



"""
@app.route('/questions')
def questions():
    conn = get_db_connection()
    return QuestionsService.get_questions(conn)
"""
