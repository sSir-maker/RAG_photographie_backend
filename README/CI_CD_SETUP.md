# 🔄 Configuration CI/CD Complète

## 📋 Vue d'ensemble

Le projet utilise GitHub Actions pour :
- ✅ Tests automatiques
- ✅ Linting et formatage
- ✅ Build des images Docker
- ✅ Déploiement automatique

## 🚀 Workflows GitHub Actions

### 1. CI Pipeline (`.github/workflows/ci.yml`)

**Déclencheurs** :
- Push sur `main` ou `develop`
- Pull requests

**Jobs** :
- **test** : Tests Python (3.11 et 3.12)
- **lint-frontend** : Linting du frontend
- **build** : Build des images Docker
- **deploy** : Déploiement en production (uniquement sur `main`)

### 2. Lint Pipeline (`.github/workflows/lint.yml`)

**Déclencheurs** :
- Push sur `main` ou `develop`
- Pull requests
- Déclenchement manuel

**Jobs** :
- **python-lint** : Linting Python complet
- **format-check** : Vérification du formatage

### 3. Deploy Pipeline (`.github/workflows/deploy.yml`)

**Déclencheurs** :
- Push sur `main`
- Déclenchement manuel

**Actions** :
- Pull du code
- Pull des images Docker
- Redémarrage des services
- Migrations de base de données
- Health check

## 🔧 Configuration Requise

### Secrets GitHub

Dans GitHub : Settings → Secrets and variables → Actions

**Obligatoires pour le déploiement** :
- `DOCKER_USERNAME` : Nom d'utilisateur Docker Hub
- `DOCKER_PASSWORD` : Token Docker Hub
- `DEPLOY_HOST` : Adresse du serveur (ex: `example.com`)
- `DEPLOY_USER` : Utilisateur SSH (ex: `deploy`)
- `DEPLOY_SSH_KEY` : Clé SSH privée
- `DEPLOY_PORT` : Port SSH (optionnel, défaut: 22)
- `DEPLOY_PATH` : Chemin de déploiement (optionnel, défaut: `/opt/rag-photographie`)

### Configuration du Serveur

1. **Créer l'utilisateur de déploiement** :
```bash
sudo adduser deploy
sudo usermod -aG docker deploy
```

2. **Configurer SSH** :
```bash
# Générer une clé SSH
ssh-keygen -t ed25519 -C "github-actions" -f deploy_key

# Copier la clé publique sur le serveur
ssh-copy-id -i deploy_key.pub deploy@ton-serveur

# Ajouter la clé privée comme secret GitHub
cat deploy_key  # Copier dans DEPLOY_SSH_KEY
```

3. **Préparer le répertoire** :
```bash
sudo mkdir -p /opt/rag-photographie
sudo chown deploy:deploy /opt/rag-photographie
cd /opt/rag-photographie
git clone https://github.com/ton-username/rag-photographie.git .
```

## 📝 Utilisation Locale

### Tests

```bash
# Tous les tests
make test

# Tests spécifiques
pytest tests/test_database.py -v
```

### Linting

```bash
# Vérifier (sans modifier)
make lint

# Formater
make format
```

### Docker

```bash
# Build
make docker-build

# Démarrer
make docker-up

# Arrêter
make docker-down
```

## 🔄 Workflow de Développement

1. **Développement** :
   ```bash
   # Créer une branche
   git checkout -b feature/ma-feature
   
   # Développer...
   make format  # Formater le code
   make lint    # Vérifier
   make test    # Tester
   ```

2. **Commit** :
   ```bash
   git add .
   git commit -m "feat: ajouter nouvelle fonctionnalité"
   git push origin feature/ma-feature
   ```

3. **Pull Request** :
   - Créer une PR sur GitHub
   - Les tests et le linting s'exécutent automatiquement
   - Vérifier que tout passe

4. **Merge** :
   - Merge sur `main`
   - Déploiement automatique en production

## 📊 Monitoring

### Vérifier les Workflows

1. Aller sur GitHub → Actions
2. Voir l'historique des workflows
3. Cliquer sur un workflow pour voir les détails

### Logs de Déploiement

Sur le serveur :
```bash
cd /opt/rag-photographie
docker-compose -f docker-compose.prod.yml logs -f
```

## ✅ Checklist

- [ ] Secrets GitHub configurés
- [ ] Serveur de production préparé
- [ ] Clé SSH configurée
- [ ] Tests locaux passent
- [ ] Linting local OK
- [ ] Workflow CI testé avec une PR
- [ ] Déploiement testé

---

**✅ CI/CD configuré et prêt !**

