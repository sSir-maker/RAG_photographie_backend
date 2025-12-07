# 🔧 Activer l'environnement virtuel Python 3.12

## Problème

Tu utilises encore Python 3.14 au lieu de l'environnement virtuel Python 3.12 qu'on a créé.

## Solution : Activer l'environnement virtuel

### Étape 1 : Ouvrir PowerShell dans le dossier du projet

```bash
cd E:\RAG-Photographie
```

### Étape 2 : Activer l'environnement virtuel

```powershell
.\venv\Scripts\Activate.ps1
```

Si tu as une erreur de politique d'exécution, exécute d'abord :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis réessaie :

```powershell
.\venv\Scripts\Activate.ps1
```

### Étape 3 : Vérifier que Python 3.12 est utilisé

Tu devrais voir `(venv)` au début de ta ligne de commande, et :

```bash
python --version
# Devrait afficher : Python 3.12.10
```

### Étape 4 : Installer les dépendances

```bash
pip install -r requirements.txt
```

Cela peut prendre quelques minutes (PyTorch fait ~110 MB).

### Étape 5 : Vérifier l'installation

```bash
python test_installation.py
```

## Alternative : Utiliser CMD au lieu de PowerShell

Si PowerShell pose problème, utilise CMD :

```cmd
cd E:\RAG-Photographie
venv\Scripts\activate.bat
python --version
pip install -r requirements.txt
```

## Important

**À chaque fois que tu ouvres un nouveau terminal**, tu dois réactiver l'environnement virtuel :

```powershell
cd E:\RAG-Photographie
.\venv\Scripts\Activate.ps1
```

Sinon, Python 3.14 sera utilisé par défaut !

