# 🎨 Déploiement du Frontend

## 🚀 Options de déploiement gratuites

### 1. **Vercel** ⭐ (Recommandé pour frontend React)
- ✅ **100% gratuit** et illimité
- ✅ Déploiement depuis GitHub automatique
- ✅ HTTPS automatique
- ✅ CDN global (ultra rapide)
- ✅ Preview deployments pour chaque PR
- ✅ Pas de configuration nécessaire
- **URL** : https://vercel.com

### 2. **Netlify** ⭐ (Excellent aussi)
- ✅ **100% gratuit** (100 GB bandwidth/mois)
- ✅ Déploiement depuis GitHub
- ✅ HTTPS automatique
- ✅ CDN global
- ✅ Functions serverless incluses
- **URL** : https://netlify.com

### 3. **Render** (Static Site)
- ✅ Gratuit (750h/mois)
- ✅ Déploiement depuis GitHub
- ✅ HTTPS automatique
- ⚠️ Sleep après 15 min (gratuit)
- **URL** : https://render.com

### 4. **Fly.io** (Conteneur Docker)
- ✅ Gratuit (3 VMs)
- ✅ Services toujours actifs
- ✅ Support Docker
- **URL** : https://fly.io

## 🏆 Comparaison

| Service | Gratuit | CDN | Build | Meilleur pour |
|---------|---------|-----|-------|---------------|
| **Vercel** | ✅ Illimité | ✅ Global | ✅ Auto | React/Vite |
| **Netlify** | ✅ 100GB/mois | ✅ Global | ✅ Auto | Frontend général |
| **Render** | ✅ 750h/mois | ⚠️ Basique | ✅ Auto | Simplicité |
| **Fly.io** | ✅ 3 VMs | ❌ | ✅ Docker | Conteneurs |

## 🚀 Option 1 : Vercel (Recommandé)

### Étapes

1. **Va sur https://vercel.com**
2. **Crée un compte** (gratuit, avec GitHub)
3. **"Add New" → "Project"**
4. **Import ton repository** : `RAG_photographie_frontend`
5. **Configuration automatique** :
   - Vercel détecte automatiquement Vite/React
   - Framework Preset : **Vite**
   - Root Directory : `frontend_RAG` (si repo séparé) ou laisse vide
   - Build Command : `npm run build` (auto-détecté)
   - Output Directory : `dist` (auto-détecté)
6. **Variables d'environnement** :
   - Clique sur "Environment Variables"
   - Ajoute : `VITE_API_URL` = `https://ton-backend.onrender.com`
7. **"Deploy"**

### C'est tout ! 🎉

Vercel va :
- ✅ Build automatiquement
- ✅ Déployer sur CDN global
- ✅ Générer une URL HTTPS
- ✅ Redéployer à chaque push sur `main`

### Configuration avancée (optionnel)

Crée `vercel.json` à la racine du frontend :

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## 🚀 Option 2 : Netlify

### Étapes

1. **Va sur https://netlify.com**
2. **Crée un compte** (gratuit, avec GitHub)
3. **"Add new site" → "Import an existing project"**
4. **Connecte GitHub** → Sélectionne `RAG_photographie_frontend`
5. **Configuration** :
   - **Build command** : `npm run build`
   - **Publish directory** : `dist`
   - **Base directory** : (laisse vide si repo séparé)
6. **Variables d'environnement** :
   - "Site settings" → "Environment variables"
   - Ajoute : `VITE_API_URL` = `https://ton-backend.onrender.com`
7. **"Deploy site"**

### Configuration avancée (optionnel)

Crée `netlify.toml` à la racine :

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 🚀 Option 3 : Render (Static Site)

### Étapes

1. **Va sur https://render.com**
2. **Crée un compte** (gratuit)
3. **"New" → "Static Site"**
4. **Connecte GitHub** → Sélectionne `RAG_photographie_frontend`
5. **Configuration** :
   - **Name** : `rag-photographie-frontend`
   - **Branch** : `main`
   - **Root Directory** : (laisse vide)
   - **Build Command** : `npm install && npm run build`
   - **Publish Directory** : `dist`
6. **Environment Variables** :
   - Ajoute : `VITE_API_URL` = `https://ton-backend.onrender.com`
7. **"Create Static Site"**

Le fichier `render.yaml` est déjà créé pour automatiser cela.

## 🚀 Option 4 : Fly.io (Docker)

### Étapes

1. **Installer flyctl** :
   ```bash
   # Windows (PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Se connecter** :
   ```bash
   fly auth login
   ```

3. **Initialiser le projet** :
   ```bash
   cd frontend_RAG
   fly launch
   ```

4. **Configurer les variables** :
   ```bash
   fly secrets set VITE_API_URL=https://ton-backend.onrender.com
   ```

5. **Déployer** :
   ```bash
   fly deploy
   ```

## 📋 Variables d'environnement nécessaires

### Obligatoire
- `VITE_API_URL` : URL du backend
  - Exemple : `https://rag-photographie-backend.onrender.com`
  - Ou : `https://rag-backend.fly.dev`

### Important
- ✅ Utilise **HTTPS** (pas HTTP)
- ✅ Pas de slash (`/`) à la fin
- ✅ Remplace par **TON URL backend réelle**

## ✅ Après déploiement

1. **Copie l'URL du frontend** (ex: `https://rag-frontend.vercel.app`)
2. **Mets à jour `FRONTEND_URL` dans le backend** :
   - Va dans les variables d'environnement du backend
   - Modifie `FRONTEND_URL` avec l'URL du frontend
3. **Teste** : Ouvre l'URL du frontend dans le navigateur

## 🎯 Recommandation

**Pour le frontend, je recommande Vercel** :
- ✅ 100% gratuit et illimité
- ✅ CDN global (ultra rapide)
- ✅ Configuration automatique
- ✅ Parfait pour React/Vite
- ✅ Preview deployments pour chaque PR

## 🔗 URLs typiques après déploiement

- **Vercel** : `https://rag-photographie-frontend.vercel.app`
- **Netlify** : `https://rag-photographie-frontend.netlify.app`
- **Render** : `https://rag-photographie-frontend.onrender.com`
- **Fly.io** : `https://rag-photographie-frontend.fly.dev`

