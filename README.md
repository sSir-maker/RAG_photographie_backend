## RAG Photographie avec LangChain

Ce projet met en place un RAG spécialisé pour répondre à des questions sur la photographie en utilisant **LangChain** et des outils gratuits.

### Structure générale

- `app/` : code Python principal (RAG, OCR, API).
- **`data/`** : **📁 C'est ici que tu places tes documents sur la photographie !** (PDF, textes, images, CSV).
- `models/` : éventuels modèles locaux personnalisés.
- `notebooks/` : explorations et tests.

> 📍 **Où mettre tes documents ?**  
> Place tous tes fichiers dans le dossier **`E:\RAG-Photographie\data\`**  
> Voir `data/README.md` pour plus de détails sur les formats supportés.

### ⚠️ Prérequis Python

**Important** : Ce projet nécessite **Python 3.11 ou 3.12** (recommandé : 3.12).

Python 3.14 est trop récent et cause des problèmes de compatibilité avec les dépendances.

Voir `SETUP_PYTHON.md` pour les instructions détaillées d'installation de Python.

### Installation rapide

1. **Créer un environnement virtuel Python 3.11 ou 3.12** :
   ```powershell
   # Avec Python 3.12 (recommandé)
   py -3.12 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Installer les dépendances de base :

```powershell
pip install -r requirements.txt
```

3. **Installer les outils de développement (optionnel)** :
   ```powershell
   .\scripts\install-dev.ps1
   # Ou
   pip install -r requirements-dev.txt
   ```

> ✅ **Note** : Le système utilise maintenant les loaders LangChain natifs (`PyPDFium2Loader`)  
> qui gèrent automatiquement l'extraction d'images des PDFs avec Tesseract.  
> Plus besoin d'installer PyMuPDF manuellement !

### 🪟 Windows - Scripts PowerShell

Sur Windows, utilise les scripts PowerShell au lieu de `make` :

```powershell
# Formater le code
.\scripts\format.ps1

# Vérifier le code
.\scripts\lint.ps1

# Exécuter les tests
.\scripts\test.ps1
```

Voir `WINDOWS_SCRIPTS.md` pour plus de détails.

4. **Vérifier l'installation** (optionnel) :

```bash
python test_installation.py
```

5. Lancer un premier index des documents et un exemple de question :

```bash
# Depuis la racine du projet (E:\RAG-Photographie)
python run_example.py
```

Ou si tu préfères utiliser le module :

```bash
python -m app.run_example
```

### Contenu

- Pipeline **OCR → structuration → chunking → embeddings → vector store**.
- **Extraction OCR avancée** :
  - Support des PDFs avec texte normal
  - **Extraction et OCR des images intégrées dans les PDFs** (via PyMuPDF - optionnel)
  - Support des images (JPG, PNG, TIFF) et fichiers CSV
  - Fallback OCR sur pages scannées complètes
  - ⚠️ **Note** : PyMuPDF est optionnel. Si l'installation échoue, le système fonctionne quand même pour les PDFs texte et scannés.
- Pipeline de **question/réponse** avec LangChain :
  - chargement des documents
  - création du vector store
  - chaîne de retrieval (`create_retrieval_chain`)
  - génération de réponse avec un LLM open‑source / API gratuite.


