# 🪟 Scripts PowerShell pour Windows

## 📋 Vue d'ensemble

Sur Windows, `make` n'est pas disponible par défaut. Des scripts PowerShell équivalents ont été créés.

## 🚀 Scripts Disponibles

### 1. Installation des outils

```powershell
.\scripts\install-dev.ps1
```

Installe tous les outils de développement (black, isort, flake8, pylint, mypy, pytest).

### 2. Formatage du code

```powershell
.\scripts\format.ps1
```

Formate automatiquement le code avec Black et isort.

### 3. Vérification (Linting)

```powershell
.\scripts\lint.ps1
```

Vérifie le code sans le modifier (Black, isort, Flake8, Pylint).

### 4. Tests

```powershell
.\scripts\test.ps1
```

Exécute tous les tests avec couverture.

### 5. Nettoyage

```powershell
.\scripts\clean.ps1
```

Supprime les fichiers temporaires (__pycache__, .pyc, .pytest_cache, etc.).

## 🔧 Utilisation

### Workflow complet

```powershell
# 1. Installer les outils (une seule fois)
.\scripts\install-dev.ps1

# 2. Formater le code
.\scripts\format.ps1

# 3. Vérifier le code
.\scripts\lint.ps1

# 4. Exécuter les tests
.\scripts\test.ps1

# 5. Nettoyer (optionnel)
.\scripts\clean.ps1
```

## ⚠️ Permissions PowerShell

Si tu as une erreur de politique d'exécution :

```powershell
# Vérifier la politique actuelle
Get-ExecutionPolicy

# Autoriser les scripts (pour la session actuelle)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Ou de manière permanente (nécessite admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🔄 Alternatives

### Sans scripts PowerShell

Tu peux aussi exécuter directement :

```powershell
# Formatage
python -m black app/ tests/ scripts/
python -m isort app/ tests/ scripts/

# Linting
python -m black --check app/ tests/ scripts/
python -m isort --check-only app/ tests/ scripts/
python -m flake8 app/ tests/ scripts/
python -m pylint app/

# Tests
python -m pytest tests/ -v --cov=app --cov-report=html
```

### Installer Make sur Windows (optionnel)

Si tu veux utiliser `make` :

1. **Chocolatey** :
   ```powershell
   choco install make
   ```

2. **Scoop** :
   ```powershell
   scoop install make
   ```

3. **WSL** :
   ```powershell
   wsl make format
   ```

## ✅ Checklist

- [ ] Scripts PowerShell créés
- [ ] Outils installés (`.\scripts\install-dev.ps1`)
- [ ] Formatage testé (`.\scripts\format.ps1`)
- [ ] Linting testé (`.\scripts\lint.ps1`)

---

**✅ Scripts PowerShell prêts pour Windows !**

