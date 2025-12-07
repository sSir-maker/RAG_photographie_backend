# 🎨 RAG Photographie - Frontend

Interface React/Vite moderne pour le système RAG de photographie.

## 📋 Vue d'ensemble

Ce repository contient le **frontend** du projet RAG Photographie :
- Interface React avec TypeScript
- Vite pour le build
- Tailwind CSS pour le styling
- Authentification JWT
- Chat interface avec streaming
- Gestion des conversations
- Design responsive et moderne

## 🚀 Installation Rapide

### Prérequis

- Node.js 18+ (recommandé : 20+)
- npm ou yarn

### Installation

```powershell
# Installer les dépendances
npm install
```

## ⚙️ Configuration

Créer un fichier `.env.local` à la racine du projet frontend :

```env
VITE_API_URL=http://localhost:8001
```

## 🏃 Démarrer le serveur de développement

```powershell
npm run dev
```

L'application sera accessible sur `http://localhost:3000`

## 🏗️ Build pour production

```powershell
# Build
npm run build

# Preview du build
npm run preview
```

Les fichiers seront générés dans le dossier `dist/`

## 🐳 Docker

```powershell
# Build l'image
docker build -t rag-frontend .

# Lancer le conteneur
docker run -p 80:80 rag-frontend
```

## 📚 Documentation

- `README.md` - Documentation complète
- `README_API.md` - Documentation de l'API backend

## 🔗 Backend

Le backend est dans un repository séparé :
**https://github.com/sSir-maker/RAG_photographie_backend**

Assure-toi que le backend est démarré et accessible à l'URL configurée dans `VITE_API_URL`.

## 🏗️ Structure du Projet

```
frontend_RAG/
├── src/
│   ├── components/        # Composants React
│   │   ├── AuthPage.tsx   # Page d'authentification
│   │   ├── ChatInput.tsx  # Input de chat
│   │   ├── ChatMessage.tsx # Message de chat
│   │   └── ...
│   ├── App.tsx            # Composant principal
│   └── main.tsx           # Point d'entrée
├── public/                # Assets statiques
├── Dockerfile             # Image Docker
├── nginx.conf             # Configuration Nginx
└── package.json           # Dépendances
```

## 🎨 Technologies

- **React** - Framework UI
- **TypeScript** - Typage statique
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - Composants UI

## 🔒 Authentification

Le frontend utilise JWT pour l'authentification :
- Inscription (`/auth/signup`)
- Connexion (`/auth/login`)
- Token stocké dans localStorage
- Redirection automatique si non authentifié

## 💬 Chat Interface

- Streaming des réponses en temps réel
- Gestion des conversations
- Historique des messages
- Sources des réponses
- Indicateur de frappe

## 📱 Responsive Design

L'interface est entièrement responsive et fonctionne sur :
- Desktop
- Tablette
- Mobile

## 🧪 Tests

```powershell
# Tests (si configurés)
npm test
```

## 🚀 Déploiement

### Vercel / Netlify

```powershell
# Build
npm run build

# Déployer le dossier dist/
```

### Docker

```powershell
docker build -t rag-frontend .
docker run -p 80:80 rag-frontend
```

### Nginx

Le fichier `nginx.conf` est fourni pour un déploiement avec Nginx.

---

**Frontend RAG Photographie** - Interface React moderne avec Tailwind CSS

