# 🔧 Correction Installation Phoenix

## ❌ Problème

L'erreur indique que le package `arize-phoenix>=7.5.0` n'existe pas sur PyPI.

## ✅ Solution

Le package s'appelle **`phoenix`** (pas `arize-phoenix`) sur PyPI.

## 📦 Installation Correcte

```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer Phoenix avec le bon nom de package
pip install phoenix>=3.0.0 openinference-semantic-conventions>=1.0.0

# Vérifier l'installation
python -c "import phoenix; print('Phoenix installé!')"
```

## 🔍 Vérification

```bash
# Vérifier la version installée
pip show phoenix

# Tester l'import
python -c "from phoenix.trace import OpenInferenceTracer; print('OK')"
```

## 📝 Notes

- Le package sur PyPI s'appelle `phoenix` (pas `arize-phoenix`)
- Les versions récentes nécessitent Python 3.9-3.13
- `openinference-semantic-conventions` est un package séparé pour les conventions sémantiques

## 🚀 Après Installation

Une fois installé, tu peux :

1. Démarrer le dashboard :
   ```bash
   python -m phoenix.server.main --port 6006
   ```

2. Démarrer l'API (Phoenix s'initialisera automatiquement) :
   ```bash
   python run_api.py
   ```

3. Accéder au dashboard : http://localhost:6006

