# 🆓 Services d'hébergement gratuits

## 🎯 Options gratuites recommandées

### 1. **Render** ⭐ (Recommandé)
- ✅ **Gratuit** : 750 heures/mois
- ✅ Déploiement depuis GitHub
- ✅ PostgreSQL gratuit (90 jours, puis $7/mois)
- ✅ Redis gratuit (limité)
- ✅ HTTPS automatique
- ✅ Auto-deploy depuis GitHub
- ✅ Support Docker
- **Limite** : Services "sleep" après 15 min d'inactivité (gratuit)
- **URL** : https://render.com

### 2. **Fly.io** ⭐ (Excellent pour conteneurs)
- ✅ **Gratuit** : 3 VMs partagées
- ✅ PostgreSQL gratuit (256 MB)
- ✅ Redis gratuit
- ✅ HTTPS automatique
- ✅ Scaling automatique
- ✅ Pas de "sleep" (services toujours actifs)
- **Limite** : 3 VMs gratuites
- **URL** : https://fly.io


### 4. **Vercel** (Excellent pour frontend)
- ✅ **Gratuit** : Illimité
- ✅ Déploiement depuis GitHub
- ✅ HTTPS automatique
- ✅ CDN global
- ⚠️ **Limite** : Backend serverless uniquement (pas de conteneurs long-running)
- **URL** : https://vercel.com

### 5. **Netlify** (Frontend + Functions)
- ✅ **Gratuit** : 100 GB bandwidth/mois
- ✅ Déploiement depuis GitHub
- ✅ HTTPS automatique
- ✅ Functions serverless
- ⚠️ **Limite** : Backend serverless uniquement
- **URL** : https://netlify.com

### 6. **Google Cloud Run** (Gratuit avec quota)
- ✅ **Gratuit** : 2 millions de requêtes/mois
- ✅ Conteneurs Docker
- ✅ Auto-scaling à zéro
- ✅ HTTPS automatique
- **Limite** : Quota gratuit limité
- **URL** : https://cloud.google.com/run

### 7. **Oracle Cloud Always Free**
- ✅ **Gratuit** : 2 VMs toujours gratuites
- ✅ PostgreSQL disponible
- ✅ Contrôle total
- ⚠️ **Limite** : Configuration manuelle requise
- **URL** : https://oracle.com/cloud/free

## 🏆 Comparaison rapide

| Service | Backend | Frontend | DB | Redis | Sleep | Limite principale |
|---------|---------|----------|----|----|-------|-------------------|
| **Render** | ✅ | ✅ | ✅ (90j) | ✅ | ⚠️ 15min | 750h/mois |
| **Fly.io** | ✅ | ✅ | ✅ | ✅ | ❌ | 3 VMs |
| **Vercel** | ⚠️ Serverless | ✅ | ❌ | ❌ | ❌ | Backend limité |
| **Cloud Run** | ✅ | ✅ | ❌ | ❌ | ✅ | 2M req/mois |

## 🎯 Recommandation pour ton projet

### Option 1 : **Render** (Meilleur compromis)
- ✅ Gratuit et généreux
- ✅ Support Docker
- ✅ PostgreSQL gratuit 90 jours
- ⚠️ Services "sleep" après 15 min (gratuit)

### Option 2 : **Fly.io** (Meilleur pour toujours-online)
- ✅ Services toujours actifs (pas de sleep)
- ✅ PostgreSQL gratuit
- ✅ Redis gratuit
- ✅ Excellent pour production
- ⚠️ Limite de 3 VMs


## 🚀 Déploiement sur Render (Recommandé)

### Backend

1. Va sur https://render.com
2. Crée un compte (gratuit)
3. "New" → "Web Service"
4. Connecte GitHub → Sélectionne `RAG_photographie_backend`
5. Configuration :
   - **Name** : `rag-backend`
   - **Environment** : `Docker`
   - **Region** : Choisis le plus proche
   - **Branch** : `main`
   - **Root Directory** : `backend`
   - **Dockerfile Path** : `backend/Dockerfile`
6. Variables d'environnement :
   ```
   DATABASE_URL=postgresql://... (Render fournit)
   SECRET_KEY=ton-secret-key
   OLLAMA_BASE_URL=http://localhost:11434
   FRONTEND_URL=https://ton-frontend.onrender.com
   ```
7. "Create Web Service"

### Frontend

1. "New" → "Static Site"
2. Connecte GitHub → Sélectionne `RAG_photographie_frontend`
3. Configuration :
   - **Build Command** : `npm install && npm run build`
   - **Publish Directory** : `dist`
   - **Environment Variable** : `VITE_API_URL=https://ton-backend.onrender.com`
4. "Create Static Site"

### PostgreSQL (Render)

1. "New" → "PostgreSQL"
2. Configuration :
   - **Name** : `rag-db`
   - **Database** : `rag_photographie`
   - **User** : (généré automatiquement)
3. Copie `DATABASE_URL` et colle-la dans les variables du backend

## 🚀 Déploiement sur Fly.io

### Backend

```bash
# Installer flyctl
curl -L https://fly.io/install.sh | sh

# Se connecter
fly auth login

# Initialiser le projet
cd backend
fly launch

# Déployer
fly deploy
```

### Frontend

```bash
cd frontend_RAG
fly launch
fly deploy
```

## 💡 Astuce : Combiner les services

- **Backend** : Render ou Fly.io
- **Frontend** : Vercel ou Netlify (gratuit, CDN global)
- **Base de données** : Render PostgreSQL (90j gratuit) ou Supabase (gratuit)

## ✅ Avantages des services gratuits

- ✅ Pas de coût
- ✅ Déploiement depuis GitHub
- ✅ HTTPS automatique
- ✅ Scaling basique
- ✅ Bon pour développement et petits projets

## ⚠️ Limitations

- ⚠️ Services peuvent "sleep" après inactivité (Render gratuit)
- ⚠️ Limites de ressources
- ⚠️ Pas de SLA garanti
- ⚠️ Pour production importante, considère un plan payant

