# 🔍 Configuration du Linting et Formatage

## 📋 Vue d'ensemble

Le projet utilise plusieurs outils pour maintenir la qualité du code :
- **Black** : Formatage automatique
- **isort** : Tri des imports
- **Flake8** : Vérification du style
- **Pylint** : Analyse statique
- **MyPy** : Vérification de types

## 🚀 Installation

### Outils de développement

```bash
pip install -r requirements-dev.txt
```

Ou installer individuellement :

```bash
pip install black isort flake8 pylint mypy
```

## 🔧 Configuration

### Fichiers de configuration

- `pyproject.toml` : Configuration Black, isort, Pylint, MyPy, Pytest
- `.flake8` : Configuration Flake8
- `.pylintrc` : Configuration Pylint

## 📝 Utilisation

### Formatage automatique

**Windows (PowerShell)** :
```powershell
.\scripts\format.ps1
```

**Linux/Mac** :
```bash
# Formater tout le code
make format
# Ou
python scripts/format_code.py

# Ou manuellement
black app/ tests/ scripts/
isort app/ tests/ scripts/
```

### Vérification (sans modification)

**Windows (PowerShell)** :
```powershell
.\scripts\lint.ps1
```

**Linux/Mac** :
```bash
# Vérifier le formatage
make lint
# Ou
python scripts/lint_code.py

# Ou manuellement
black --check app/ tests/
isort --check-only app/ tests/
flake8 app/ tests/
pylint app/
mypy app/
```

## 🔄 Intégration dans le workflow

### Pre-commit Hook (optionnel)

Créer `.git/hooks/pre-commit` :

```bash
#!/bin/bash
python scripts/format_code.py
python scripts/lint_code.py
```

Rendre exécutable :

```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions

Le workflow `.github/workflows/lint.yml` vérifie automatiquement le code à chaque push.

## 📊 Règles de Linting

### Black (Formatage)

- Longueur de ligne : 120 caractères
- Cible : Python 3.11 et 3.12
- Formatage automatique selon PEP 8

### isort (Imports)

- Compatible avec Black
- Tri automatique des imports
- Groupes : stdlib, third-party, local

### Flake8 (Style)

- Longueur de ligne : 120 caractères
- Ignore : E203, W503, E501
- Vérifie PEP 8

### Pylint (Analyse)

- Désactivé : C0111, C0103, R0913, R0903, W0613
- Score minimum : Pas de limite (avertissements seulement)

### MyPy (Types)

- Mode permissif (ignore-missing-imports)
- Vérification optionnelle des types

## 🎯 Frontend Linting

### ESLint

Configuration dans `frontend_RAG/.eslintrc.json`

```bash
cd frontend_RAG
npm run lint
```

### Prettier (optionnel)

```bash
npm install --save-dev prettier
npm run format
```

## ✅ Checklist

- [ ] Outils installés (`pip install -r requirements-dev.txt`)
- [ ] Code formaté (`python scripts/format_code.py`)
- [ ] Linting OK (`python scripts/lint_code.py`)
- [ ] Pre-commit hook configuré (optionnel)
- [ ] GitHub Actions configuré

---

**✅ Linting et formatage configurés !**

