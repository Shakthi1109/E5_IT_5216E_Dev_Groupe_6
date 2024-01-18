Pour lancer l'API : 

docker build -t quiz-api .
docker run -d -p 5000:5000 [ID_Image]
docker logs -f [ID_Container]

Via mon VPS, connexion sur : http://172.17.0.2:5000