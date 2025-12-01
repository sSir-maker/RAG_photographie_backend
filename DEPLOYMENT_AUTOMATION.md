# 🚀 Déploiement Automatique

## 📋 Vue d'ensemble

Le déploiement automatique est configuré via GitHub Actions pour déployer automatiquement sur le serveur de production lors des pushes sur `main`.

## 🔧 Configuration

### 1. Secrets GitHub

Configurer les secrets suivants dans GitHub (Settings → Secrets and variables → Actions) :

- `DOCKER_USERNAME` : Nom d'utilisateur Docker Hub
- `DOCKER_PASSWORD` : Token Docker Hub
- `DEPLOY_HOST` : Adresse IP ou hostname du serveur de production
- `DEPLOY_USER` : Utilisateur SSH pour le déploiement
- `DEPLOY_SSH_KEY` : Clé SSH privée pour se connecter au serveur

### 2. Configuration du Serveur

Sur le serveur de production :

```bash
# Créer le répertoire de déploiement
sudo mkdir -p /opt/rag-photographie
cd /opt/rag-photographie

# Cloner le repository (ou utiliser git pull)
git clone https://github.com/ton-username/rag-photographie.git .

# Créer le fichier .env
cp .env.example .env
# Éditer .env avec les valeurs de production

# Démarrer les services
docker-compose up -d
```

### 3. Configuration SSH

Sur le serveur :

```bash
# Créer un utilisateur de déploiement
sudo adduser deploy
sudo usermod -aG docker deploy

# Configurer les permissions
sudo chown -R deploy:deploy /opt/rag-photographie
```

Générer une clé SSH :

```bash
# Sur ta machine locale
ssh-keygen -t ed25519 -C "github-actions" -f deploy_key

# Copier la clé publique sur le serveur
ssh-copy-id -i deploy_key.pub deploy@ton-serveur

# Ajouter la clé privée comme secret GitHub
cat deploy_key  # Copier le contenu dans DEPLOY_SSH_KEY
```

## 🔄 Workflow de Déploiement

### Déclencheurs

Le déploiement se déclenche automatiquement :
- Lors d'un push sur `main`
- Après que tous les tests passent
- Après le build des images Docker

### Étapes

1. **Tests** : Exécution de tous les tests
2. **Linting** : Vérification du code
3. **Build** : Construction des images Docker
4. **Push** : Envoi des images sur Docker Hub
5. **Deploy** : Déploiement sur le serveur de production

### Commandes de Déploiement

Sur le serveur, le workflow exécute :

```bash
cd /opt/rag-photographie
docker-compose pull          # Télécharger les nouvelles images
docker-compose up -d         # Redémarrer les services
docker-compose exec -T backend python -m alembic upgrade head  # Migrations DB
```

## 🐳 Docker Compose Production

Créer un `docker-compose.prod.yml` :

```yaml
version: '3.8'

services:
  backend:
    image: ton-username/rag-photographie-backend:latest
    restart: always
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - postgres
      - redis

  frontend:
    image: ton-username/rag-photographie-frontend:latest
    restart: always
    depends_on:
      - backend

  postgres:
    image: postgres:15-alpine
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    restart: always
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 🔒 Sécurité

### Bonnes Pratiques

1. **Secrets** : Ne jamais commiter les secrets
2. **SSH** : Utiliser des clés SSH, pas de mots de passe
3. **Firewall** : Limiter l'accès SSH
4. **Backup** : Sauvegarder avant chaque déploiement
5. **Rollback** : Avoir un plan de rollback

### Rollback

En cas de problème :

```bash
# Sur le serveur
cd /opt/rag-photographie
docker-compose down
docker-compose pull rag-photographie-backend:previous-tag
docker-compose up -d
```

## 📊 Monitoring du Déploiement

### Vérifier le statut

```bash
# Logs GitHub Actions
# Voir dans l'onglet "Actions" du repository

# Logs sur le serveur
docker-compose logs -f backend
docker-compose ps
```

### Health Checks

```bash
# Vérifier que l'API répond
curl http://ton-serveur/health

# Vérifier les services
docker-compose ps
```

## ✅ Checklist de Déploiement

- [ ] Secrets GitHub configurés
- [ ] Serveur de production configuré
- [ ] Clé SSH ajoutée
- [ ] Docker Compose production créé
- [ ] Variables d'environnement configurées
- [ ] Base de données initialisée
- [ ] Migrations appliquées
- [ ] Health checks fonctionnels

---

**✅ Déploiement automatique configuré !**

