# 🦙 Configuration Ollama pour le RAG Photographie

## Problème

L'erreur indique que **Ollama n'est pas en cours d'exécution** :

```
ConnectionRefusedError: [WinError 10061] Aucune connexion n'a pu être établie
HTTPConnectionPool(host='localhost', port=11434)
```

Le système essaie de se connecter à Ollama sur le port 11434, mais le serveur n'est pas démarré.

## Solution : Installer et démarrer Ollama

### Étape 1 : Installer Ollama

1. **Télécharger Ollama** :
   - Aller sur https://ollama.com/download
   - Télécharger la version Windows
   - Installer l'application

2. **Vérifier l'installation** :
   ```bash
   ollama --version
   ```

### Étape 2 : Télécharger un modèle LLM

Une fois Ollama installé, télécharge un modèle (par exemple `llama3`) :

```bash
ollama pull llama3
```

Cela peut prendre quelques minutes (le modèle fait plusieurs GB).

### Étape 3 : Démarrer Ollama

Ollama devrait démarrer automatiquement après l'installation. Si ce n'est pas le cas :

1. **Lancer Ollama manuellement** :
   - Chercher "Ollama" dans le menu Démarrer
   - Lancer l'application
   - Ollama démarre en arrière-plan

2. **Vérifier que Ollama fonctionne** :
   ```bash
   ollama list
   ```
   
   Tu devrais voir la liste des modèles téléchargés.

3. **Tester Ollama** :
   ```bash
   ollama run llama3 "Bonjour, comment ça va ?"
   ```

### Étape 4 : Relancer le RAG

Une fois Ollama démarré, tu peux relancer :

```bash
python run_example.py
```

## Alternatives si Ollama ne fonctionne pas

### Option 1 : Utiliser un autre LLM local

Tu peux modifier `app/config.py` pour utiliser un autre LLM :

```python
# Au lieu de Ollama, utiliser un autre LLM
from langchain_community.llms import HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="mistralai/Mistral-7B-Instruct-v0.1",
    task="text-generation",
)
```

### Option 2 : Utiliser une API LLM (gratuite)

Tu peux utiliser des APIs gratuites comme :

- **HuggingFace Inference API** (gratuit avec limitations)
- **Groq** (gratuit, très rapide)
- **Together AI** (gratuit avec crédits)

Exemple avec HuggingFace :

```python
from langchain_community.llms import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    endpoint_url="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
    huggingfacehub_api_token="ton_token_ici",
)
```

### Option 3 : Mode test sans LLM

Pour tester le système sans LLM, tu peux modifier temporairement le code pour retourner juste les documents récupérés.

## Vérification rapide

Pour vérifier si Ollama fonctionne :

```bash
# Vérifier que le serveur répond
curl http://localhost:11434/api/tags
```

Ou dans PowerShell :

```powershell
Invoke-WebRequest -Uri http://localhost:11434/api/tags
```

Si tu obtiens une réponse JSON, Ollama fonctionne !

## Configuration dans le projet

Le projet est configuré pour utiliser Ollama par défaut avec le modèle `llama3`.

Tu peux changer le modèle dans `.env` :

```env
LLM_MODEL_NAME=llama3
```

Ou utiliser un autre modèle compatible Ollama :
- `llama3`
- `mistral`
- `llama2`
- `codellama`
- etc.

