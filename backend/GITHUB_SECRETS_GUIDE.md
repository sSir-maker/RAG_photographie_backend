# 🔑 Guide : Configurer les Secrets GitHub

## 📍 Où trouver les secrets dans GitHub

### Chemin complet :
1. Va sur ton repository GitHub
2. Clique sur **Settings** (en haut du repository)
3. Dans le menu de gauche, clique sur **Secrets and variables**
4. Clique sur **Actions**
5. Clique sur **New repository secret** (bouton vert en haut à droite)

## 🔐 Secrets à configurer

### ⚠️ IMPORTANT : Secrets optionnels pour Render

Si tu utilises **Render**, tu n'as **PAS BESOIN** de configurer ces secrets GitHub ! Render build directement depuis GitHub.

### 1. Secrets Docker Hub (optionnel)

Seulement si tu veux push les images Docker vers Docker Hub.

#### DOCKER_USERNAME
- **Valeur** : Ton nom d'utilisateur Docker Hub
- **Exemple** : `monusername`

#### DOCKER_PASSWORD
- **Valeur** : Ton token Docker Hub (PAS le mot de passe)
- **Comment obtenir** :
  1. Va sur https://hub.docker.com/settings/security
  2. Clique sur "New Access Token"
  3. Donne un nom (ex: "GitHub Actions")
  4. Copie le token généré
  5. Colle-le dans le secret `DOCKER_PASSWORD`

### 2. Secrets Déploiement SSH (optionnel)

Seulement si tu déploies sur ton propre serveur (pas Render).

#### PROD_HOST
- **Valeur** : IP ou hostname de ton serveur
- **Exemple** : `192.168.1.100` ou `server.example.com`

#### PROD_USER
- **Valeur** : Nom d'utilisateur SSH
- **Exemple** : `ubuntu` ou `root`

#### PROD_SSH_KEY
- **Valeur** : Clé SSH privée pour se connecter au serveur
- **Comment obtenir** :
  1. Génère une clé SSH : `ssh-keygen -t rsa`
  2. Copie le contenu de `~/.ssh/id_rsa` (clé privée)
  3. Colle-le dans le secret `PROD_SSH_KEY`
  4. Ajoute la clé publique (`~/.ssh/id_rsa.pub`) sur le serveur

## ✅ Pour Render (recommandé)

**Aucun secret GitHub nécessaire !**

Configure plutôt les variables d'environnement dans Render :
1. Va sur https://dashboard.render.com
2. Sélectionne ton service (backend ou frontend)
3. Va dans "Environment"
4. Ajoute les variables d'environnement

## 📝 Variables d'environnement Render

### Backend :
```env
SECRET_KEY=ton-secret-key
DATABASE_URL=postgresql://... (fourni par Render si tu ajoutes PostgreSQL)
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3
FRONTEND_URL=https://rag-photographie-frontend.onrender.com
# ... etc
```

### Frontend :
```env
VITE_API_URL=https://rag-photographie-backend.onrender.com
```

## 🎯 Résumé

- **Render** : Pas besoin de secrets GitHub, configure les variables dans Render
- **Docker Hub** : Secrets optionnels (DOCKER_USERNAME, DOCKER_PASSWORD)
- **SSH Déploiement** : Secrets optionnels (PROD_HOST, PROD_USER, PROD_SSH_KEY)

Les workflows GitHub Actions fonctionnent avec ou sans ces secrets grâce aux conditions ajoutées.

