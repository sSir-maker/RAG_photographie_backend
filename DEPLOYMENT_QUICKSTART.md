# 🚀 Déploiement Rapide - Guide Express

## Option 1 : Déploiement Local (Développement)

### Étapes rapides

```bash
# 1. Activer l'environnement
.\venv\Scripts\Activate.ps1

# 2. Démarrer Ollama (si pas déjà lancé)
ollama serve

# 3. Démarrer Phoenix (optionnel)
phoenix serve --port 6006

# 4. Démarrer l'API
python run_api.py

# 5. Démarrer le frontend (nouveau terminal)
cd frontend_RAG
npm run dev
```

**Accès** :
- API : http://localhost:8001/docs
- Frontend : http://localhost:3000
- Phoenix : http://localhost:6006

---

## Option 2 : Déploiement avec Docker

### Étapes rapides

```bash
# 1. Créer le fichier .env (copier .env.example)
cp .env.example .env
# Éditer .env avec tes valeurs

# 2. Démarrer tous les services
docker-compose up -d

# 3. Voir les logs
docker-compose logs -f

# 4. Arrêter
docker-compose down
```

---

## Option 3 : Déploiement Cloud

### Vercel (Frontend) + Railway (Backend)

#### Frontend sur Vercel

```bash
cd frontend_RAG
npm install -g vercel
vercel
```

#### Backend sur Railway

1. Connecter le repo GitHub
2. Configurer les variables d'environnement
3. Déployer automatiquement

---

## 📋 Checklist avant déploiement

- [ ] Variables d'environnement configurées (`.env`)
- [ ] Secrets générés (SECRET_KEY)
- [ ] Ollama configuré et accessible
- [ ] Documents dans `data/`
- [ ] Tests passent
- [ ] Base de données initialisée

---

## 📚 Documentation complète

Pour plus de détails, consulte **`DEPLOYMENT_GUIDE.md`**

