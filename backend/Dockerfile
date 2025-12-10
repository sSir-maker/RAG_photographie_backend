FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Mettre à jour pip avec timeout augmenté et retries
RUN pip install --no-cache-dir --upgrade pip setuptools wheel --timeout=300 --retries=5

# Copier d'abord requirements.txt pour utiliser le cache Docker
COPY backend/requirements.txt .

# Installer les dépendances Python avec gestion d'erreurs robuste
# Options pour gérer les problèmes de connexion réseau (BrokenPipeError) :
# - timeout augmenté (600 secondes = 10 minutes)
# - retries (10 tentatives)
# - Installation avec plusieurs tentatives et pauses
RUN set -e; \
    for i in 1 2 3; do \
        echo "🔄 Tentative d'installation $i/3..." && \
        pip install --no-cache-dir \
            --timeout=600 \
            --retries=10 \
            --default-timeout=600 \
            --progress-bar off \
            -r requirements.txt && \
        echo "✅ Installation réussie !" && \
        break || \
        (echo "⚠️ Tentative $i échouée, attente 15 secondes avant nouvelle tentative..." && \
         sleep 15); \
    done || \
    (echo "❌ Erreur : Impossible d'installer les dépendances après 3 tentatives" && exit 1)

# Nettoyer le cache pip après installation pour réduire la taille
RUN pip cache purge && \
    rm -rf /root/.cache/pip

# Copier uniquement les fichiers nécessaires (exclut data/ via .dockerignore)
COPY backend/ .

# Créer les dossiers nécessaires avec permissions
RUN mkdir -p storage/vector_store data phoenix_data && \
    chmod -R 755 storage data phoenix_data

# Vérifier que les fichiers essentiels existent
RUN test -f run_api.py || (echo "run_api.py manquant" && exit 1) && \
    test -d app || (echo "dossier app/ manquant" && exit 1)

# Nettoyer les fichiers inutiles pour réduire la taille
RUN find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true && \
    find . -type f -name "*.pyc" -delete && \
    find . -type f -name "*.pyo" -delete

# Exposer le port de l'API (Render utilise PORT dynamiquement)
EXPOSE 8001

# Healthcheck (Render utilise PORT dynamiquement, mais healthcheck utilise 8001 par défaut)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Commande par défaut
CMD ["python", "run_api.py"]

