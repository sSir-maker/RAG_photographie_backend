# 🔧 Configuration Python pour RAG Photographie

## Problème actuel

Python 3.14.0 est très récent et cause des problèmes de compatibilité avec plusieurs packages :
- NumPy : conflits de versions
- LangChain : nécessite NumPy < 2.0.0
- Autres dépendances : wheels précompilés pas toujours disponibles

## Solution : Utiliser Python 3.11 ou 3.12

### Option 1 : Python 3.12 (Recommandé)

**Avantages :**
- ✅ Très bien supporté par tous les packages
- ✅ Wheels précompilés disponibles pour la plupart des dépendances
- ✅ Compatible avec LangChain 0.3.x
- ✅ Compatible avec NumPy 2.x (si nécessaire)

**Installation :**

1. **Télécharger Python 3.12** :
   - Aller sur https://www.python.org/downloads/
   - Télécharger Python 3.12.x (dernière version 3.12)
   - ⚠️ **Important** : Cocher "Add Python to PATH" lors de l'installation

2. **Vérifier l'installation** :
   ```bash
   python3.12 --version
   # ou
   py -3.12 --version
   ```

3. **Créer un environnement virtuel avec Python 3.12** :
   ```bash
   # Option A : Avec py launcher (Windows)
   py -3.12 -m venv venv
   
   # Option B : Avec python3.12 directement
   python3.12 -m venv venv
   ```

4. **Activer l'environnement virtuel** :
   ```bash
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows CMD
   venv\Scripts\activate.bat
   ```

5. **Installer les dépendances** :
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Option 2 : Python 3.11 (Alternative stable)

**Avantages :**
- ✅ Très stable et testé
- ✅ Excellent support de tous les packages
- ✅ Compatible avec NumPy 1.x et 2.x

**Installation :**
- Même processus que Python 3.12, mais télécharger Python 3.11.x

### Option 3 : Utiliser pyenv (Gestionnaire de versions Python)

Si tu veux gérer plusieurs versions de Python facilement :

1. **Installer pyenv-win** (Windows) :
   ```powershell
   # Via Chocolatey
   choco install pyenv-win
   
   # Ou via Git
   git clone https://github.com/pyenv-win/pyenv-win.git $HOME\.pyenv
   ```

2. **Installer Python 3.12** :
   ```bash
   pyenv install 3.12.7
   pyenv local 3.12.7
   ```

3. **Créer l'environnement virtuel** :
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

## Mise à jour de requirements.txt

Une fois que tu as Python 3.11 ou 3.12, tu peux utiliser NumPy 2.x si tu veux :

```txt
# Avec Python 3.12, on peut utiliser NumPy 2.x
numpy>=2.0.0
```

Ou rester avec NumPy 1.x pour compatibilité maximale :

```txt
# NumPy 1.x pour compatibilité maximale avec LangChain 0.3.2
numpy>=1.26.0,<2.0.0
```

## Vérification

Après avoir installé Python 3.11 ou 3.12 et créé l'environnement virtuel :

```bash
# Vérifier la version Python
python --version

# Vérifier que pip fonctionne
pip --version

# Installer les dépendances
pip install -r requirements.txt
```

## Recommandation finale

**Utilise Python 3.12.7** (ou dernière version 3.12.x) :
- Meilleur équilibre entre nouveautés et compatibilité
- Support excellent de tous les packages
- Compatible avec LangChain et NumPy

