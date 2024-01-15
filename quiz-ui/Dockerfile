FROM node:20.10.0-alpine

# définit le dossier 'app' comme dossier de travail
WORKDIR /app

# copie 'package.json' et 'package-lock.json' (si disponible)
COPY ./ /app

# installe les dépendances du projet
RUN npm install

# construit l'app pour la production en la minifiant
RUN npm run build

CMD [ "npm", "run", "dev" ]