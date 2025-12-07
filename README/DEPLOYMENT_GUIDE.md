# 🚀 Guide de Déploiement - RAG Photographie

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Checklist de pré-déploiement](#checklist-de-pré-déploiement)
3. [Déploiement Local (Développement)](#déploiement-local-développement)
4. [Déploiement avec Docker](#déploiement-avec-docker)
5. [Déploiement Cloud](#déploiement-cloud)
6. [Configuration Production](#configuration-production)
7. [Sécurité](#sécurité)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 📦 Prérequis

### Système
- **Python 3.11 ou 3.12** (recommandé : 3.12)
- **Node.js 18+** (pour le frontend)
- **Ollama** installé et configuré (voir `SETUP_OLLAMA.md`)
- **Tesseract OCR** installé (pour l'OCR)
- **Git** (pour le versioning)

### Services externes (optionnels)
- Base de données PostgreSQL (pour production, remplace SQLite)
- Redis (pour le cache, optionnel)
- Service de stockage cloud (S3, Azure Blob, etc.)

---

## ✅ Checklist de pré-déploiement

### 1. Tests locaux
- [ ] Tous les tests passent
- [ ] L'API répond correctement (`python run_api.py`)
- [ ] Le frontend se connecte à l'API
- [ ] Phoenix monitoring fonctionne
- [ ] Les documents sont indexés correctement
- [ ] L'authentification fonctionne (signup/login)

### 2. Configuration
- [ ] Variables d'environnement configurées (`.env`)
- [ ] Secrets stockés de manière sécurisée
- [ ] Ports configurés (8001 pour API, 3000 pour frontend, 6006 pour Phoenix)
- [ ] Base de données initialisée

### 3. Documentation
- [ ] README à jour
- [ ] Variables d'environnement documentées
- [ ] Procédures de backup documentées

---

## 🏠 Déploiement Local (Développement)

### Étape 1 : Préparation de l'environnement

```bash
# 1. Cloner le projet (si nécessaire)
git clone <repo-url>
cd RAG-Photographie

# 2. Créer l'environnement virtuel
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# ou
source venv/bin/activate  # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Installer les dépendances frontend
cd frontend_RAG
npm install
cd ..
```

### Étape 2 : Configuration

Créer un fichier `.env` à la racine :

```env
# API Configuration
API_PORT=8001
API_HOST=0.0.0.0

# LLM Configuration
LLM_MODEL_NAME=llama3
OLLAMA_BASE_URL=http://localhost:11434

# Embedding Model
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

# Phoenix Monitoring
PHOENIX_ENDPOINT=http://localhost:6006

# Database (SQLite pour dev, PostgreSQL pour prod)
DATABASE_URL=sqlite:///./storage/database.db

# JWT Secret (GÉNÉRER UN SECRET FORT EN PRODUCTION !)
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Streaming
STREAMING_DELAY=0.03

# Frontend URL (pour CORS)
FRONTEND_URL=http://localhost:3000
```

### Étape 3 : Préparer les données

```bash
# Placer les documents dans data/
# Les documents seront automatiquement indexés au premier lancement
```

### Étape 4 : Démarrer les services

**Terminal 1 - Ollama** (si pas déjà lancé) :
```bash
ollama serve
```

**Terminal 2 - Phoenix Monitoring** :
```bash
phoenix serve --port 6006
```

**Terminal 3 - Backend API** :
```bash
.\venv\Scripts\Activate.ps1
python run_api.py
```

**Terminal 4 - Frontend** :
```bash
cd frontend_RAG
npm run dev
```

### Étape 5 : Vérification

- API : http://localhost:8001/docs
- Frontend : http://localhost:3000
- Phoenix : http://localhost:6006

---

## 🐳 Déploiement avec Docker

### Étape 1 : Créer un Dockerfile

Créer `Dockerfile` à la racine :

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Exposer le port
EXPOSE 8001

# Commande par défaut
CMD ["python", "run_api.py"]
```

### Étape 2 : Créer docker-compose.yml

```yaml
version: '3.8'

services:
  # Backend API
  backend:
    build: .
    container_name: rag-backend
    ports:
      - "8001:8001"
    environment:
      - PHOENIX_ENDPOINT=http://phoenix:6006
      - DATABASE_URL=sqlite:///./storage/database.db
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - ./data:/app/data
      - ./storage:/app/storage
    depends_on:
      - phoenix
      - ollama
    networks:
      - rag-network
    restart: unless-stopped

  # Phoenix Monitoring
  phoenix:
    image: arizephoenix/phoenix:latest
    container_name: rag-phoenix
    ports:
      - "6006:6006"
    volumes:
      - ./phoenix_data:/data
    networks:
      - rag-network
    restart: unless-stopped

  # Ollama (LLM local)
  ollama:
    image: ollama/ollama:latest
    container_name: rag-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - rag-network
    restart: unless-stopped

  # Frontend (optionnel - peut être déployé séparément)
  frontend:
    build:
      context: ./frontend_RAG
      dockerfile: Dockerfile
    container_name: rag-frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8001
    depends_on:
      - backend
    networks:
      - rag-network
    restart: unless-stopped

volumes:
  ollama_data:

networks:
  rag-network:
    driver: bridge
```

### Étape 3 : Dockerfile pour le frontend

Créer `frontend_RAG/Dockerfile` :

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host"]
```

### Étape 4 : Déployer

```bash
# Construire et démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

---

## ☁️ Déploiement Cloud

### Option 1 : Vercel (Frontend) + Railway/Render (Backend)

#### Frontend sur Vercel

```bash
cd frontend_RAG
npm install -g vercel
vercel
```

Configuration dans Vercel :
- Build Command: `npm run build`
- Output Directory: `dist`
- Environment Variables:
  - `VITE_API_URL`: URL de ton backend

#### Backend sur Railway/Render

1. **Railway** :
   - Connecter le repo GitHub
   - Configurer les variables d'environnement
   - Déployer automatiquement

2. **Render** :
   - Créer un nouveau Web Service
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run_api.py`

### Option 2 : AWS/GCP/Azure

#### Architecture recommandée

```
┌─────────────┐
│   Frontend  │ (S3 + CloudFront)
└──────┬──────┘
       │
┌──────▼──────┐
│  API Gateway│
└──────┬──────┘
       │
┌──────▼──────┐     ┌──────────┐
│   Backend   │────▶│  Ollama  │
│  (ECS/Fargate)│     │  (EC2)   │
└──────┬──────┘     └──────────┘
       │
┌──────▼──────┐
│  PostgreSQL │
│   (RDS)     │
└─────────────┘
```

### Option 3 : Kubernetes

Créer les fichiers de déploiement Kubernetes :

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-backend
  template:
    metadata:
      labels:
        app: rag-backend
    spec:
      containers:
      - name: backend
        image: rag-backend:latest
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: rag-secrets
              key: database-url
---
apiVersion: v1
kind: Service
metadata:
  name: rag-backend-service
spec:
  selector:
    app: rag-backend
  ports:
  - port: 80
    targetPort: 8001
  type: LoadBalancer
```

---

## 🔧 Configuration Production

### Variables d'environnement critiques

```env
# Sécurité
SECRET_KEY=<générer-un-secret-fort>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Base de données (PostgreSQL recommandé)
DATABASE_URL=postgresql://user:password@host:5432/rag_db

# CORS
ALLOWED_ORIGINS=https://ton-domaine.com,https://www.ton-domaine.com

# Monitoring
PHOENIX_ENDPOINT=http://phoenix:6006
ENABLE_MONITORING=true

# Performance
WORKERS=4  # Pour uvicorn
MAX_CONNECTIONS=100
```

### Configuration Uvicorn pour production

Modifier `run_api.py` :

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8001,
        workers=4,  # Multi-workers pour production
        log_level="info",
        access_log=True,
    )
```

### Optimisations

1. **Cache Redis** (optionnel) :
```python
# Ajouter dans requirements.txt
redis>=5.0.0

# Utiliser pour cache des embeddings
```

2. **CDN pour le frontend** :
   - Utiliser CloudFront/Cloudflare pour servir les assets statiques

3. **Load Balancer** :
   - Utiliser un load balancer pour distribuer le trafic

---

## 🔒 Sécurité

### Checklist sécurité

- [ ] **Secrets** : Ne jamais commiter les secrets dans Git
- [ ] **HTTPS** : Utiliser HTTPS en production
- [ ] **CORS** : Configurer CORS correctement
- [ ] **Rate Limiting** : Implémenter rate limiting
- [ ] **Validation** : Valider toutes les entrées utilisateur
- [ ] **SQL Injection** : Utiliser SQLAlchemy (déjà fait ✅)
- [ ] **JWT** : Utiliser des secrets forts et rotation
- [ ] **Dépendances** : Mettre à jour régulièrement

### Implémenter Rate Limiting

Ajouter dans `app/api.py` :

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/ask")
@limiter.limit("10/minute")  # 10 requêtes par minute
async def ask_question(...):
    ...
```

---

## 📊 Monitoring & Maintenance

### Monitoring

1. **Phoenix Dashboard** : http://localhost:6006
   - Traces des requêtes RAG
   - Performance des embeddings
   - Qualité des réponses

2. **Logs** :
```bash
# Logs Docker
docker-compose logs -f backend

# Logs système
journalctl -u rag-backend -f
```

3. **Métriques** :
   - Temps de réponse API
   - Taux d'erreur
   - Utilisation CPU/Mémoire
   - Taille de la base de données

### Maintenance

#### Backup régulier

```bash
# Backup base de données
pg_dump rag_db > backup_$(date +%Y%m%d).sql

# Backup vector store
tar -czf vector_store_backup_$(date +%Y%m%d).tar.gz storage/vector_store/
```

#### Mise à jour

```bash
# Mettre à jour les dépendances
pip install --upgrade -r requirements.txt

# Reconstruire le vector store si nécessaire
python run_example.py  # Avec force_rebuild=True
```

#### Nettoyage

```bash
# Nettoyer les logs anciens
find logs/ -name "*.log" -mtime +30 -delete

# Nettoyer les backups anciens (> 90 jours)
find backups/ -name "*.sql" -mtime +90 -delete
```

---

## 🚨 Troubleshooting

### Problèmes courants

1. **Port déjà utilisé** :
```bash
# Trouver le processus
netstat -ano | findstr :8001
# Tuer le processus
taskkill /PID <pid> /F
```

2. **Ollama non accessible** :
```bash
# Vérifier qu'Ollama est lancé
ollama serve

# Vérifier le modèle
ollama list
```

3. **Erreurs de dépendances** :
```bash
# Réinstaller dans un environnement propre
rm -rf venv
python -m venv venv
pip install -r requirements.txt
```

---

## 📚 Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Phoenix](https://docs.arize.com/phoenix)
- [Documentation Docker](https://docs.docker.com/)
- [Documentation Vercel](https://vercel.com/docs)

---

## ✅ Checklist finale

Avant de déployer en production :

- [ ] Tests passent
- [ ] Variables d'environnement configurées
- [ ] Secrets sécurisés
- [ ] HTTPS activé
- [ ] Monitoring configuré
- [ ] Backup configuré
- [ ] Documentation à jour
- [ ] Rate limiting activé
- [ ] CORS configuré
- [ ] Logs configurés

---

**Bon déploiement ! 🚀**

