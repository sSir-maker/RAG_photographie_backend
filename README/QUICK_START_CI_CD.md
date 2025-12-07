# ⚡ Démarrage Rapide CI/CD

## 🚀 Configuration en 5 minutes

### 1. Installer les outils de développement

```bash
pip install -r requirements-dev.txt
```

### 2. Formater le code

**Windows (PowerShell)** :
```powershell
.\scripts\format.ps1
```

**Linux/Mac** :
```bash
make format
# Ou
python scripts/format_code.py
```

### 3. Vérifier le code

**Windows (PowerShell)** :
```powershell
.\scripts\lint.ps1
```

**Linux/Mac** :
```bash
make lint
# Ou
python scripts/lint_code.py
```

### 4. Configurer GitHub Actions

1. **Créer le repository GitHub** (si pas déjà fait)

2. **Ajouter les secrets** (Settings → Secrets) :
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
   - `DEPLOY_HOST`
   - `DEPLOY_USER`
   - `DEPLOY_SSH_KEY`

3. **Push le code** :
   ```bash
   git add .
   git commit -m "feat: ajouter CI/CD"
   git push origin main
   ```

### 5. Vérifier les workflows

- Aller sur GitHub → Actions
- Voir les workflows s'exécuter

## 📝 Commandes Utiles

**Windows (PowerShell)** :
```powershell
# Tests
.\scripts\test.ps1

# Formatage
.\scripts\format.ps1

# Linting
.\scripts\lint.ps1

# Nettoyer
.\scripts\clean.ps1
```

**Linux/Mac** :
```bash
# Tests
make test

# Formatage
make format

# Linting
make lint

# Nettoyer
make clean

# Docker
make docker-build
make docker-up
make docker-down
```

## ✅ Checklist

- [ ] Outils installés (`pip install -r requirements-dev.txt`)
- [ ] Code formaté (`make format`)
- [ ] Linting OK (`make lint`)
- [ ] Secrets GitHub configurés
- [ ] Workflow testé avec un push

---

**✅ CI/CD prêt !**

