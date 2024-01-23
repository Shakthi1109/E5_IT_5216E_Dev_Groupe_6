# E5_IT_5216E_Dev_Groupe_6_TD_1

# Développement web full stack - TD 1

## Groupe 6
### Erwann MASSON
### Mathieu LESUR
### Shakthivel MURUGAVEL

Instructions to run:

cd to quiz-app(root)/quiz-ui:

docker image build -t quiz-local-ui .
docker container run -it --rm -p 3000:80 --name quiz-local-ui quiz-local-ui

Access http://localhost:3000

cd to quiz-app(root)/quiz-api:
docker image build -t quiz-local-api .
docker container run -it --rm -p 5000:5000 --name quiz-local-api quiz-local-api

Access http://localhost:5000




<!-- UI local:

cd quiz-ui
npm install
npm run dev -->