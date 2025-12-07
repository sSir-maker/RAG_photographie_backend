# 📊 État du Stack Technique - RAG Photographie

**Date de mise à jour** : 2024  
**Version** : 2.0.0  
**Statut** : ✅ Production Ready avec Monitoring Open-Source

---

## 🎯 Vue d'ensemble

Système RAG (Retrieval Augmented Generation) complet pour répondre à des questions sur la photographie, avec pipeline MLOps, interface web moderne, authentification, et **monitoring professionnel 100% open-source** via Arize Phoenix.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                       │
│  - Interface utilisateur moderne                           │
│  - Authentification JWT                                     │
│  - Streaming des réponses                                   │
│  - Gestion des conversations                                │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST + WebSocket (SSE)
┌──────────────────────▼──────────────────────────────────────┐
│                    BACKEND (FastAPI)                        │
│  - API REST avec authentification                           │
│  - Streaming Server-Sent Events                             │
│  - Gestion base de données                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  PIPELINE RAG                               │
│  - OCR (Tesseract)                                          │
│  - Embeddings (sentence-transformers)                       │
│  - Vector Store (FAISS)                                     │
│  - LLM (Ollama - local)                                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              PIPELINE MLOPS (Prefect)                       │
│  - Orchestration                                             │
│  - Monitoring                                                │
│  - Feedback Loop                                             │
└──────────────────────────────────────────────────────────────┘
```

---

## 🐍 Backend - Stack Python

### **Framework & API**
- **FastAPI** `0.115.2` - Framework web moderne et rapide
- **Uvicorn** `0.32.0` - Serveur ASGI
- **Pydantic** `2.9.2` - Validation de données
- **Python** `3.11` ou `3.12` (recommandé)

### **RAG & LLM**
- **LangChain** `0.3.2` - Framework pour applications LLM
  - `langchain-community` `0.3.1`
  - `langchain-core` `0.3.8`
  - `langchain-text-splitters` `0.3.0`
- **sentence-transformers** `3.1.1` - Modèles d'embeddings
- **FAISS** `>=1.12.0` - Vector store pour recherche sémantique
- **Ollama** (local) - LLM local (llama3 par défaut)

### **OCR & Document Processing**
- **pdfplumber** `0.11.4` - Extraction texte PDF
- **pytesseract** `0.3.13` - OCR (Tesseract)
- **Pillow** `10.4.0` - Traitement d'images
- **pypdfium2** `>=4.0.0` - Extraction images PDF

### **Base de données & Authentification**
- **SQLAlchemy** `>=2.0.0` - ORM
- **SQLite** - Base de données (fichier)
- **python-jose** `3.3.0` - JWT tokens
- **bcrypt** `>=4.0.0` - Hashage de mots de passe
- **email-validator** `>=2.0.0` - Validation emails

### **MLOps & Orchestration**
- **Prefect** `>=2.14.0` - Orchestration de workflows

### **🔥 Monitoring & Observability (NOUVEAU)**
- **Phoenix** `>=3.0.0` - Monitoring LLM/RAG open-source (package: `phoenix`)
- **openinference-semantic-conventions** `>=1.0.0` - Standard de tracing

### **Utilitaires**
- **python-dotenv** `1.0.1` - Gestion variables d'environnement

---

## ⚛️ Frontend - Stack React

### **Framework & Build**
- **React** `^18.3.1` - Bibliothèque UI
- **Vite** `6.3.5` - Build tool et dev server
- **TypeScript** - Typage statique

### **UI Components**
- **Radix UI** - Composants accessibles
  - Accordion, Alert Dialog, Avatar, Checkbox, Dialog, Dropdown, etc.
- **Tailwind CSS** - Framework CSS utility-first
- **Lucide React** `^0.487.0` - Icônes
- **next-themes** `^0.4.6` - Gestion thèmes (dark/light)

### **Formulaires & Validation**
- **react-hook-form** `^7.55.0` - Gestion formulaires
- **class-variance-authority** `^0.7.1` - Variantes de classes

### **Autres**
- **cmdk** `^1.1.1` - Command palette
- **sonner** `^2.0.3` - Notifications toast
- **recharts** `^2.15.2` - Graphiques
- **date-fns** - Manipulation dates

---

## 📁 Structure du Projet

```
RAG-Photographie/
├── app/                          # Backend Python
│   ├── api.py                   # API FastAPI principale
│   ├── auth.py                  # Authentification JWT
│   ├── config.py                # Configuration
│   ├── database.py              # Modèles SQLAlchemy
│   ├── db_auth.py               # Fonctions auth DB
│   ├── db_chat.py               # Fonctions chat DB
│   ├── ocr_pipeline.py          # Pipeline OCR
│   ├── pipeline_components.py   # Composants RAG
│   ├── rag_pipeline.py          # Pipeline RAG principal
│   └── 🔥 monitoring_phoenix.py  # NOUVEAU - Monitoring Phoenix
│
├── frontend_RAG/                 # Frontend React
│   ├── src/
│   │   ├── App.tsx              # Application principale
│   │   ├── components/
│   │   │   ├── AuthPage.tsx     # Page authentification
│   │   │   ├── ChatMessage.tsx  # Message chat
│   │   │   ├── ThinkingIndicator.tsx  # Animation typing
│   │   │   └── ui/              # Composants UI (48 fichiers)
│   │   └── styles/
│   └── vite.config.ts
│
├── mlops/                        # Pipeline MLOps
│   ├── pipeline.py              # Pipeline Prefect
│   ├── monitoring.py            # Monitoring & métriques
│   ├── feedback_loop.py         # Feedback utilisateurs
│   └── 🔥 phoenix_integration.py # NOUVEAU - Intégration Phoenix
│
├── data/                         # Documents source
│   └── *.pdf                    # 12+ documents PDF
│
├── storage/                      # Données persistantes
│   ├── database.db              # SQLite
│   └── vector_store/            # FAISS index
│
├── requirements.txt              # Dépendances Python
└── 🔥 docker-compose.monitoring.yml # NOUVEAU - Docker pour Phoenix
```

---

## 🔧 Composants Principaux

### **1. Pipeline RAG** (`app/rag_pipeline.py`)
- ✅ Collecte de documents
- ✅ OCR avec Tesseract
- ✅ Post-traitement et correction
- ✅ Découpage intelligent
- ✅ Génération d'embeddings
- ✅ Vector store FAISS
- ✅ Retrieval et génération
- ✅ **Streaming token par token**
- ✅ **🔥 Tracing Phoenix automatique**

### **2. API Backend** (`app/api.py`)
- ✅ Endpoints REST
- ✅ Authentification JWT
- ✅ Streaming Server-Sent Events (`/ask/stream`)
- ✅ Gestion conversations
- ✅ Gestion messages
- ✅ CORS configuré
- ✅ **🔥 Instrumentation Phoenix au démarrage**

### **3. Frontend** (`frontend_RAG/`)
- ✅ Interface moderne (design Figma)
- ✅ Authentification (login/signup)
- ✅ Chat avec streaming
- ✅ Animation typing réaliste
- ✅ Gestion thèmes (dark/light)
- ✅ Sidebar conversations
- ✅ Responsive design

### **4. Pipeline MLOps** (`mlops/`)
- ✅ Orchestration Prefect
- ✅ Monitoring automatique
- ✅ Collecte métriques
- ✅ Feedback loop
- ✅ Détection retraining
- ✅ **🔥 Intégration Phoenix pour tracing**

### **5. Monitoring Phoenix** (`app/monitoring_phoenix.py`) - NOUVEAU
- ✅ Tracing automatique LangChain
- ✅ Tracing manuel pipeline custom
- ✅ Métriques retrieval et génération
- ✅ Dashboard temps-réel
- ✅ Visualisation embeddings

---

## 🗄️ Base de Données

### **SQLite** (`storage/database.db`)

**Tables :**
- `users` - Utilisateurs (id, name, email, hashed_password, created_at)
- `conversations` - Conversations (id, user_id, title, created_at, updated_at)
- `messages` - Messages (id, conversation_id, role, content, image_url, created_at)

---

## 🔐 Sécurité

- ✅ **JWT** pour authentification
- ✅ **Bcrypt** pour hashage mots de passe
- ✅ **CORS** configuré
- ✅ **Validation** emails et données
- ✅ **HTTPS ready** (production)

---

## 📊 Fonctionnalités Implémentées

### **RAG**
- ✅ Extraction OCR multi-format (PDF, images, CSV)
- ✅ Post-traitement intelligent
- ✅ Chunking sémantique
- ✅ Embeddings avec sentence-transformers
- ✅ Recherche vectorielle FAISS
- ✅ Génération avec LLM local (Ollama)
- ✅ Streaming des réponses
- ✅ Sources citées

### **Interface**
- ✅ Authentification complète
- ✅ Chat en temps réel
- ✅ Streaming visuel
- ✅ Animation typing
- ✅ Gestion conversations
- ✅ Historique persistant
- ✅ Thèmes personnalisables

### **MLOps**
- ✅ Pipeline automatisé
- ✅ Monitoring métriques
- ✅ Logging structuré
- ✅ Feedback utilisateurs
- ✅ Détection retraining

---

## 🚀 Services & Outils Externes

### **Ollama** (Local)
- **Rôle** : LLM local pour génération
- **Modèle par défaut** : `llama3`
- **Port** : `11434`
- **Installation** : Voir `SETUP_OLLAMA.md`

### **Tesseract OCR**
- **Rôle** : OCR pour images et PDFs scannés
- **Installation** : Système requis

### **🔥 Arize Phoenix** (NOUVEAU)
- **Rôle** : Monitoring et observabilité LLM/RAG
- **Port** : `6006`
- **Dashboard** : `http://localhost:6006`
- **Installation** : `pip install phoenix openinference-semantic-conventions`
- **Docker** : `docker-compose -f docker-compose.monitoring.yml up`

---

## 📈 Métriques & Monitoring

### **Métriques Collectées**
- Pipeline : documents traités, confiance OCR, temps d'exécution
- RAG : temps de réponse, longueur réponses, sources utilisées
- Utilisateurs : ratings, feedbacks

### **🔥 Métriques Phoenix (NOUVEAU)**
- **Retrieval** : nombre documents, scores similarité, temps retrieval
- **Génération** : temps génération, tokens utilisés, modèle LLM
- **Qualité** : scores hallucination, pertinence réponses
- **Performance** : latence par phase, throughput

### **Logs**
- `mlops/pipeline.log` - Logs pipeline
- `mlops/metrics/` - Métriques JSON
- `mlops/feedback/` - Feedbacks utilisateurs
- **🔥 Phoenix Dashboard** - Traces temps-réel et visualisations

---

## 🔄 Workflow Complet

1. **Utilisateur** → Login/Signup
2. **Frontend** → Envoie question via API
3. **Backend** → Authentification JWT
4. **RAG Pipeline** → 
   - Retrieval documents pertinents
   - Génération réponse avec LLM
   - Streaming token par token
5. **Frontend** → Affiche réponse progressivement
6. **Base de données** → Sauvegarde conversation
7. **MLOps** → Collecte métriques et feedback

---

## 📦 Dépendances Clés

### **Python (Backend)**
- 30+ packages
- Total : ~500MB (avec venv)

### **Node.js (Frontend)**
- 50+ packages
- Total : ~200MB (node_modules)

---

## 🎯 Points Forts

✅ **Stack moderne** : FastAPI + React + Vite  
✅ **Gratuit et open-source** : Tous les outils sont gratuits  
✅ **Local-first** : LLM local avec Ollama  
✅ **Streaming** : Réponses en temps réel  
✅ **MLOps** : Pipeline automatisé complet  
✅ **Sécurisé** : JWT, bcrypt, validation  
✅ **Scalable** : Architecture modulaire  

---

## 🔮 Prochaines Améliorations Possibles

- [ ] Déploiement Docker
- [ ] CI/CD avec GitHub Actions
- [ ] Monitoring avec Prometheus/Grafana
- [ ] Cache Redis pour performances
- [ ] Multi-LLM support
- [ ] Export conversations
- [ ] Recherche dans l'historique
- [ ] Partage de conversations

---

## 📚 Documentation

- `README.md` - Guide principal
- `MLOPS_GUIDE.md` - Guide MLOps
- `AUTH_SETUP.md` - Configuration auth
- `START_API.md` - Démarrage API
- `SETUP_OLLAMA.md` - Installation Ollama
- `SETUP_PYTHON.md` - Configuration Python

---

## 🛠️ Commandes Utiles

```bash
# Backend
python run_api.py                    # Démarrer API (port 8001)

# Frontend
cd frontend_RAG && npm run dev       # Démarrer frontend (port 3000)

# Pipeline MLOps
python mlops/pipeline.py             # Exécuter pipeline

# Monitoring
python mlops/monitoring.py           # Voir métriques

# 🔥 Phoenix Monitoring (NOUVEAU)
pip install arize-phoenix openinference-instrumentation-langchain  # Installer Phoenix
phoenix serve --port 6006  # Démarrer dashboard
# Alternative: python -m phoenix.server.main serve --port 6006
# Ou avec Docker:
docker-compose -f docker-compose.monitoring.yml up
```

## 🔥 Accès aux Dashboards

- **Frontend** : http://localhost:3000
- **API Docs** : http://localhost:8001/docs
- **🔥 Phoenix Dashboard** : http://localhost:6006 (NOUVEAU)

---

**Stack complet et opérationnel** ✅  
**Prêt pour la production** (après configuration serveur)

