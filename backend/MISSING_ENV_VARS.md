# ❌ Variables manquantes dans backend/.env

## 📊 État actuel

Ton fichier `backend/.env` contient uniquement :
```env
SECRET_KEY=mkBfPUojq4WPpO7kqXv0QGY8xOWmHp8L8LW0WgR1G0g
```

## 🔴 Variables OBLIGATOIRES manquantes

### 1. Base de données
```env
DATABASE_URL=sqlite:///./storage/database.db
```
**Pourquoi ?** L'application ne peut pas fonctionner sans base de données.

### 2. LLM (au moins un)
```env
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3
```
**Pourquoi ?** Le RAG a besoin d'un LLM pour générer les réponses.

## 🟡 Variables RECOMMANDÉES manquantes

### 3. Frontend URL
```env
FRONTEND_URL=http://localhost:3000
```
**Pourquoi ?** Pour la configuration CORS et les redirections.

### 4. Phoenix Monitoring
```env
PHOENIX_ENDPOINT=http://localhost:6006
```
**Pourquoi ?** Pour le monitoring et l'observabilité du RAG.

### 5. Redis Cache (optionnel mais recommandé)
```env
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600
```
**Pourquoi ?** Améliore les performances en cachant les réponses.

## 🟢 Variables OPTIONNELLES manquantes

### 6. Embeddings
```env
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```
**Note :** A une valeur par défaut, mais mieux de l'expliciter.

### 7. Streaming
```env
STREAMING_DELAY=0.03
```
**Note :** A une valeur par défaut (30ms).

### 8. Database Pool (production)
```env
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

### 9. Alertes (optionnel)
```env
ALERT_CHANNELS=log
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=ton-email@gmail.com
SMTP_PASSWORD=ton-mot-de-passe-app
ALERT_EMAIL_TO=admin@example.com
```

## ✅ Solution rapide

Copie ce contenu dans `backend/.env` :

```env
# ============================================
# 🔐 SÉCURITÉ
# ============================================
SECRET_KEY=mkBfPUojq4WPpO7kqXv0QGY8xOWmHp8L8LW0WgR1G0g
JWT_SECRET_KEY=mkBfPUojq4WPpO7kqXv0QGY8xOWmHp8L8LW0WgR1G0g

# ============================================
# 🗄️ BASE DE DONNÉES
# ============================================
DATABASE_URL=sqlite:///./storage/database.db

# ============================================
# 🤖 LLM
# ============================================
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3

# ============================================
# 🔍 EMBEDDINGS
# ============================================
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

# ============================================
# 📊 MONITORING
# ============================================
PHOENIX_ENDPOINT=http://localhost:6006

# ============================================
# 🌐 FRONTEND
# ============================================
FRONTEND_URL=http://localhost:3000

# ============================================
# ⚡ STREAMING
# ============================================
STREAMING_DELAY=0.03

# ============================================
# 💾 CACHE Redis (optionnel)
# ============================================
# REDIS_URL=redis://localhost:6379/0
# CACHE_TTL=3600
```

## 🚀 Pour générer un nouveau SECRET_KEY

```powershell
cd backend
python -c "from app.security import generate_secret_key; print(generate_secret_key())"
```

---

**📝 Note :** Voir `backend/.env.example` pour la liste complète avec toutes les options.

