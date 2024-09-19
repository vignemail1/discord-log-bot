# Utiliser l'image officielle de Python
FROM python:3.12

# Créer et définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du bot dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install -r requirements.txt

# Démarrer le bot
CMD ["python", "bot.py"]
