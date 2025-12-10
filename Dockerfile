FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY backend/ .

# Créer les dossiers nécessaires
RUN mkdir -p storage/vector_store data phoenix_data

# Exposer le port de l'API
EXPOSE 8001

# Commande par défaut
CMD ["python", "run_api.py"]

