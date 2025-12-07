# 🎯 RAG Photographie - Backend

API FastAPI pour le système RAG de photographie avec pipeline MLOps complet.

## 📋 Vue d'ensemble

Ce repository contient le **backend** du projet RAG Photographie :
- API FastAPI avec authentification JWT
- Pipeline RAG complet (OCR → Chunking → Embeddings → Vector Store)
- Base de données PostgreSQL/SQLite
- Cache Redis
- Monitoring Phoenix
- Système d'alertes et métriques
- Export, recherche, partage de conversations
- Support multi-LLM

## 🚀 Installation Rapide

### Prérequis

- Python 3.11 ou 3.12 (recommandé : 3.12)
- PostgreSQL (production) ou SQLite (développement)
- Redis (optionnel mais recommandé)
- Ollama ou autre LLM configuré

### Installation

```powershell
# 1. Créer l'environnement virtuel
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer le fichier .env
# Voir CREATE_ENV.md pour la configuration

# 4. Initialiser la base de données
python -c "from app.database import init_db; init_db()"
```

## 🏃 Démarrer l'API

```powershell
# Méthode 1 : Script Python
python run_api.py

# Méthode 2 : Uvicorn directement
uvicorn app.api:app --host 0.0.0.0 --port 8001 --reload
```

L'API sera accessible sur `http://localhost:8001`

## 🐳 Docker

```powershell
# Démarrer tous les services
docker-compose up -d

# Vérifier les logs
docker-compose logs -f backend

# Arrêter
docker-compose down
```

## 📝 Configuration

### Variables d'environnement minimales

Voir `CREATE_ENV.md` pour la liste complète.

**Minimum requis :**
```env
SECRET_KEY=ton-secret-key-genere
DATABASE_URL=postgresql://user:password@localhost:5432/rag_photographie
OLLAMA_BASE_URL=http://localhost:11434
FRONTEND_URL=http://localhost:3000
```

## 📚 Documentation

- `CREATE_ENV.md` - Configuration du fichier .env
- `AUTH_SETUP.md` - Configuration authentification
- `DATABASE_SETUP.md` - Configuration base de données
- `POSTGRESQL_SETUP.md` - Guide PostgreSQL
- `DEPLOYMENT_GUIDE.md` - Guide de déploiement complet
- `TESTING_GUIDE.md` - Guide des tests
- `MLOPS_GUIDE.md` - Guide du pipeline MLOps

## 🔗 Frontend

Le frontend est dans un repository séparé :
**https://github.com/sSir-maker/RAG_photographie_frontend**

## 🧪 Tests

```powershell
# Exécuter tous les tests
python run_tests.py

# Avec couverture
python run_coverage.py

# Ou avec pytest directement
pytest tests/ -v --cov=app
```

## 📊 Endpoints API

- `GET /health` - Santé du système
- `GET /health/detailed` - Santé détaillée
- `GET /metrics` - Métriques
- `POST /auth/signup` - Inscription
- `POST /auth/login` - Connexion
- `POST /ask` - Poser une question au RAG
- `POST /ask/stream` - Streaming de réponses
- `GET /conversations` - Liste des conversations
- `GET /conversations/{id}/export` - Export conversation
- `GET /search/messages` - Recherche dans messages
- `POST /conversations/{id}/share` - Partager conversation

Voir la documentation complète dans `DEPLOYMENT_GUIDE.md`.

## 🏗️ Structure du Projet

```
backend/
├── app/                    # Code Python principal
│   ├── api.py             # API FastAPI
│   ├── rag_pipeline.py    # Pipeline RAG
│   ├── database.py        # Modèles DB
│   ├── auth.py            # Authentification
│   └── ...
├── mlops/                  # Pipeline MLOps
├── tests/                  # Tests
├── scripts/                # Scripts utilitaires
├── data/                   # Documents pour le RAG
├── storage/                # Base de données, vector store
└── alembic/                # Migrations DB
```

## 🔒 Sécurité

- Authentification JWT
- Rate limiting
- Input sanitization
- Secrets management
- HTTPS/SSL ready

Voir `SECURITY_*.md` pour plus de détails.

## 📈 Monitoring

- Phoenix monitoring intégré
- Système d'alertes (email, webhook, logs)
- Métriques personnalisées
- Dashboard de santé

Voir `ALERTING_SETUP.md`, `METRICS_SETUP.md`, `HEALTH_DASHBOARD_SETUP.md`.

---

**Backend RAG Photographie** - API FastAPI avec pipeline MLOps complet

