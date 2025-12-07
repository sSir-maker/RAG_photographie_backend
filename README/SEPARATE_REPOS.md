# 🔀 Séparation du Projet en Backend et Frontend

## 📋 Vue d'ensemble

Ce guide explique comment séparer le projet en deux repositories Git distincts :
- **Backend** : API FastAPI, RAG pipeline, base de données
- **Frontend** : Interface React/Vite

## 🚀 Méthode 1 : Séparation Manuelle (Recommandée)

### Étape 1 : Créer les nouveaux repositories sur GitHub

1. **Backend Repository** :
   - Créer `https://github.com/sSir-maker/RAG_photographie_backend`
   
2. **Frontend Repository** :
   - Créer `https://github.com/sSir-maker/RAG_photographie_frontend`

### Étape 2 : Cloner et préparer le backend

```powershell
# Créer un dossier temporaire
cd E:\
mkdir RAG-Separation
cd RAG-Separation

# Cloner le repo actuel
git clone https://github.com/sSir-maker/RAG_photographie.git backend-temp
cd backend-temp

# Créer une nouvelle branche pour le backend
git checkout -b backend-only

# Supprimer le frontend
Remove-Item -Recurse -Force frontend_RAG
Remove-Item -Recurse -Force frontend

# Supprimer les fichiers frontend du .gitignore si nécessaire
# (garder les règles générales)

# Ajouter et commiter
git add .
git commit -m "Separate backend: remove frontend files"

# Changer l'URL remote pour pointer vers le nouveau repo backend
git remote set-url origin https://github.com/sSir-maker/RAG_photographie_backend.git

# Pousser vers le nouveau repo
git push -u origin backend-only
git checkout -b main
git merge backend-only
git push -u origin main
```

### Étape 3 : Préparer le frontend

```powershell
# Retourner au repo original
cd E:\RAG-Photographie

# Créer un nouveau repo pour le frontend
cd frontend_RAG
git init
git add .
git commit -m "Initial commit: Frontend RAG Photographie"

# Ajouter le remote
git remote add origin https://github.com/sSir-maker/RAG_photographie_frontend.git

# Pousser
git push -u origin main
```

## 🚀 Méthode 2 : Script Automatique

J'ai créé des scripts PowerShell pour automatiser la séparation.

### Utilisation

```powershell
# Séparer le backend
.\scripts\separate_backend.ps1

# Séparer le frontend
.\scripts\separate_frontend.ps1
```

## 📁 Structure Finale

### Backend Repository

```
RAG_photographie_backend/
├── app/                    # Code Python backend
├── mlops/                  # Pipeline MLOps
├── tests/                  # Tests backend
├── scripts/                # Scripts backend
├── data/                   # Documents pour le RAG
├── storage/                # Base de données, vector store
├── alembic/                # Migrations DB
├── docker-compose.yml      # Docker backend
├── Dockerfile              # Image Docker backend
├── requirements.txt        # Dépendances Python
└── README.md               # Documentation backend
```

### Frontend Repository

```
RAG_photographie_frontend/
├── src/                    # Code React/TypeScript
├── public/                 # Assets statiques
├── Dockerfile              # Image Docker frontend
├── nginx.conf              # Configuration Nginx
├── package.json            # Dépendances Node.js
└── README.md               # Documentation frontend
```

## 🔗 Configuration après séparation

### Backend

Dans `.env` du backend :
```env
FRONTEND_URL=https://ton-frontend.com
```

### Frontend

Dans `.env` ou `vite.config.ts` du frontend :
```env
VITE_API_URL=https://ton-backend.com
```

## ✅ Avantages de la séparation

- **Déploiement indépendant** : Backend et frontend peuvent être déployés séparément
- **Équipes séparées** : Backend et frontend peuvent être développés par des équipes différentes
- **CI/CD indépendant** : Chaque repo a son propre pipeline
- **Permissions** : Contrôle d'accès différent pour chaque repo
- **Versioning** : Versions indépendantes

## 📝 Notes importantes

- Les deux repos doivent être synchronisés pour les changements d'API
- Utiliser des tags de version pour la compatibilité
- Documenter les breaking changes dans les changelogs

---

**✅ Projet séparé avec succès !**

