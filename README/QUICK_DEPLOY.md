# 🚀 Déploiement Rapide - Guide en 5 minutes

## ✅ État du Projet

**Le projet est prêt pour le déploiement !** (~90% complété)

### ✅ Ce qui est prêt :
- ✅ Backend API complet
- ✅ Frontend React
- ✅ Authentification JWT
- ✅ Base de données (PostgreSQL configuré)
- ✅ Cache Redis
- ✅ Monitoring (Phoenix, alertes, métriques)
- ✅ Sécurité (Rate limiting, HTTPS config, input sanitization)
- ✅ Docker & Docker Compose
- ✅ CI/CD GitHub Actions
- ✅ Tests (80% couverture)

## 🚀 Déploiement en 3 étapes

### Étape 1 : Préparer l'environnement

```powershell
# 1. Créer le fichier .env
# Copier depuis CREATE_ENV.md ou créer manuellement

# 2. Générer SECRET_KEY
python -c "from app.security import generate_secret_key; print(generate_secret_key())"

# 3. Configurer les variables minimales dans .env :
# - SECRET_KEY (obligatoire)
# - DATABASE_URL (PostgreSQL en production)
# - REDIS_URL (optionnel mais recommandé)
# - OLLAMA_BASE_URL (ou autres LLM)
# - FRONTEND_URL (pour CORS)
```

### Étape 2 : Déployer avec Docker (Recommandé)

```powershell
# Option A : Production complète
docker-compose -f docker-compose.prod.yml up -d

# Option B : Développement
docker-compose up -d

# Vérifier les logs
docker-compose logs -f

# Vérifier la santé
curl http://localhost:8001/health
```

### Étape 3 : Vérifier le déploiement

```powershell
# 1. Vérifier que l'API répond
curl http://localhost:8001/health

# 2. Vérifier le frontend
# Ouvrir http://localhost:3000 dans le navigateur

# 3. Tester l'authentification
# Créer un compte via l'interface
```

## 📋 Checklist Pré-Déploiement

### Minimum requis :
- [ ] Fichier `.env` créé avec `SECRET_KEY`
- [ ] PostgreSQL accessible (ou SQLite pour dev)
- [ ] Redis accessible (optionnel)
- [ ] Ollama ou autre LLM configuré
- [ ] Ports disponibles (8001 pour API, 3000 pour frontend)

### Recommandé pour production :
- [ ] HTTPS/SSL configuré (voir `SSL_SETUP.md`)
- [ ] Backup automatique configuré
- [ ] Alertes configurées (email/webhook)
- [ ] Monitoring Phoenix accessible
- [ ] Tests exécutés et passés

## 🔧 Configuration Rapide

### Variables .env minimales :

```env
# Obligatoire
SECRET_KEY=ton-secret-key-genere

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/rag_photographie
# Ou pour SQLite (dev) :
# DATABASE_URL=sqlite:///./storage/database.db

# Redis (optionnel)
REDIS_URL=redis://localhost:6379/0

# LLM
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3

# Frontend
FRONTEND_URL=http://localhost:3000

# Monitoring (optionnel)
PHOENIX_ENDPOINT=http://localhost:6006
```

## 🐳 Déploiement Docker

### Production :

```powershell
# 1. Construire les images
docker-compose -f docker-compose.prod.yml build

# 2. Démarrer les services
docker-compose -f docker-compose.prod.yml up -d

# 3. Vérifier
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs
```

### Services inclus :
- Backend API (port 8001)
- Frontend (port 3000)
- PostgreSQL (port 5432)
- Redis (port 6379)
- Phoenix (port 6006)

## 🌐 Déploiement Manuel (sans Docker)

```powershell
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Initialiser la base de données
python -c "from app.database import init_db; init_db()"

# 3. Démarrer l'API
python run_api.py
# Ou
uvicorn app.api:app --host 0.0.0.0 --port 8001

# 4. Démarrer le frontend (dans un autre terminal)
cd frontend_RAG
npm install
npm run dev
```

## ✅ Vérification Post-Déploiement

```powershell
# 1. Santé de l'API
curl http://localhost:8001/health

# 2. Métriques
curl http://localhost:8001/metrics

# 3. Frontend
# Ouvrir http://localhost:3000

# 4. Test complet
# - Créer un compte
# - Se connecter
# - Poser une question au RAG
```

## 🚨 En cas de problème

1. **Vérifier les logs** :
   ```powershell
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. **Vérifier les variables d'environnement** :
   ```powershell
   docker-compose config
   ```

3. **Vérifier la base de données** :
   ```powershell
   python -c "from app.database import check_db_connection; check_db_connection()"
   ```

## 📚 Documentation Complète

- `DEPLOYMENT_CHECKLIST.md` - Checklist détaillée
- `CREATE_ENV.md` - Configuration .env
- `SSL_SETUP.md` - Configuration HTTPS
- `PROJECT_STATUS.md` - État du projet

---

**✅ Tu peux déployer maintenant !**

Le projet est prêt pour un déploiement MVP. Pour la production, configure HTTPS et les backups automatiques.

