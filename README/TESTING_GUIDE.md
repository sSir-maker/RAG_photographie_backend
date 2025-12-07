# 🧪 Guide de Tests

## 📋 Vue d'ensemble

Ce projet inclut une suite de tests complète utilisant **pytest** pour valider tous les composants du système RAG Photographie.

## 🚀 Installation

### 1. Installer les dépendances de test

```bash
pip install -r requirements-test.txt
```

Ou installer manuellement :
```bash
pip install pytest pytest-asyncio pytest-cov httpx faker
```

### 2. Vérifier l'installation

```bash
pytest --version
```

## 🏃 Exécution des tests

### Tous les tests

```bash
# Méthode 1 : Directement avec pytest
pytest tests/ -v

# Méthode 2 : Avec le script Python
python run_tests.py

# Méthode 3 : Avec couverture
pytest tests/ --cov=app --cov-report=html
```

### Tests spécifiques

```bash
# Tests de base de données uniquement
pytest tests/test_database.py -v

# Tests d'authentification
pytest tests/test_auth.py -v

# Tests de sécurité
pytest tests/test_security.py -v

# Tests API
pytest tests/test_api.py -v

# Tests OCR
pytest tests/test_ocr.py -v
```

### Marqueurs de test

```bash
# Tests rapides uniquement (exclure les tests lents)
pytest tests/ -v -m "not slow"

# Tests unitaires uniquement
pytest tests/ -v -m "unit"

# Tests d'intégration
pytest tests/ -v -m "integration"
```

## 📁 Structure des tests

```
tests/
├── __init__.py
├── conftest.py          # Fixtures et configuration
├── test_database.py     # Tests base de données
├── test_auth.py         # Tests authentification
├── test_security.py     # Tests sécurité
├── test_api.py          # Tests API endpoints
└── test_ocr.py          # Tests OCR pipeline
```

## 🧩 Fixtures disponibles

Les fixtures suivantes sont disponibles dans `conftest.py` :

- `test_db` : Base de données SQLite en mémoire pour les tests
- `client` : Client FastAPI de test
- `test_user_data` : Données d'utilisateur de test
- `authenticated_client` : Client authentifié avec token
- `test_data_dir` : Répertoire temporaire pour les fichiers de test
- `sample_text_file` : Fichier texte de test
- `sample_pdf_file` : Fichier PDF de test (si disponible)

## 📝 Exemples de tests

### Test de base de données

```python
def test_create_user(test_db):
    """Test de création d'utilisateur."""
    db = test_db()
    user = create_user_db(
        db=db,
        name="Test User",
        email="test@example.com",
        password="TestPassword123!"
    )
    assert user is not None
    assert user.email == "test@example.com"
```

### Test d'API

```python
def test_signup(client, test_user_data):
    """Test d'inscription."""
    response = client.post("/auth/signup", json=test_user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Test de sécurité

```python
def test_xss_protection(authenticated_client):
    """Test que les attaques XSS sont bloquées."""
    xss_payload = "<script>alert('XSS')</script>"
    response = authenticated_client.post(
        "/ask",
        json={"question": xss_payload}
    )
    assert response.status_code in [200, 400, 500]
```

## ⚙️ Configuration

Le fichier `pytest.ini` contient la configuration par défaut :

- **testpaths** : `tests`
- **python_files** : `test_*.py`
- **python_classes** : `Test*`
- **python_functions** : `test_*`

## 🐛 Débogage

### Mode verbeux

```bash
pytest tests/ -v -s
```

### Arrêter au premier échec

```bash
pytest tests/ -x
```

### Afficher les print statements

```bash
pytest tests/ -s
```

### Tests avec traceback complet

```bash
pytest tests/ --tb=long
```

## 📊 Couverture de code

### Générer un rapport de couverture

```bash
pytest tests/ --cov=app --cov-report=html
```

Le rapport HTML sera généré dans `htmlcov/index.html`.

### Voir la couverture en ligne de commande

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## ✅ Checklist avant commit

- [ ] Tous les tests passent : `pytest tests/`
- [ ] Aucun warning : `pytest tests/ -W error`
- [ ] Couverture > 80% : `pytest tests/ --cov=app --cov-report=term-missing`
- [ ] Tests rapides uniquement : `pytest tests/ -m "not slow"`

## 🔧 Résolution de problèmes

### Erreur : ModuleNotFoundError

```bash
# Vérifier que l'environnement virtuel est activé
# Réinstaller les dépendances
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Erreur : Database locked (SQLite)

Les tests utilisent une base de données en mémoire (`:memory:`) pour éviter ce problème.

### Erreur : Rate limiting dans les tests

Les tests désactivent automatiquement le rate limiting via les fixtures.

## 📚 Ressources

- [Documentation pytest](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/core/testing.html)

---

**✅ Les tests sont maintenant prêts à être exécutés !**

