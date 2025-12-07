# 🚀 Démarrer l'API RAG Photographie

## Étape 1 : Activer l'environnement virtuel

```powershell
# Depuis la racine du projet (E:\RAG-Photographie)
.\venv\Scripts\Activate.ps1
```

Tu devrais voir `(venv)` au début de ta ligne de commande.

## Étape 2 : Démarrer l'API

```powershell
python run_api.py
```

L'API devrait démarrer et afficher quelque chose comme :

```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Étape 3 : Vérifier que l'API fonctionne

Ouvre un navigateur et va sur : http://localhost:8001

Tu devrais voir :
```json
{"message": "RAG Photographie API", "status": "running"}
```

Ou teste avec :
```powershell
curl http://localhost:8001/health
```

## Étape 4 : Démarrer le frontend

Dans un **autre terminal** :

```powershell
cd frontend_RAG
npm run dev
```

Le frontend sera accessible sur http://localhost:3000

## ⚠️ Problèmes courants

### L'API ne démarre pas

1. **Vérifie que l'environnement virtuel est activé** :
   ```powershell
   python --version
   # Devrait afficher Python 3.12.10
   ```

2. **Vérifie que les dépendances sont installées** :
   ```powershell
   pip list | Select-String "fastapi"
   pip list | Select-String "uvicorn"
   ```

3. **Si manquant, installe-les** :
   ```powershell
   pip install fastapi uvicorn
   ```

### Erreur "ModuleNotFoundError"

Assure-toi d'être dans le bon répertoire et que l'environnement virtuel est activé.

### Port 8001 déjà utilisé

Si le port 8001 est occupé, modifie `run_api.py` pour utiliser un autre port (par exemple 8002) :

```python
uvicorn.run("app.api:app", host="0.0.0.0", port=8002, reload=True)
```

Et modifie aussi `frontend_RAG/src/App.tsx` pour utiliser le même port.

## 📝 Note

L'API doit rester **ouverte** pendant que tu utilises le frontend. Ne ferme pas le terminal où l'API tourne.

