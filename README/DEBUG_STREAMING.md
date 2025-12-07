# 🐛 Débogage du Streaming

Si tu rencontres une erreur 500 lors du streaming, voici comment diagnostiquer le problème.

## 🔍 Diagnostic

### 1. Vérifier les logs du serveur

Quand tu lances `python run_api.py`, regarde les erreurs dans le terminal. Elles indiquent généralement la cause du problème.

### 2. Tester le streaming directement

```powershell
.\venv\Scripts\Activate.ps1
python test_streaming.py
```

Ce script teste le streaming en local et affiche les erreurs détaillées.

### 3. Vérifier que Ollama fonctionne

Le streaming nécessite que Ollama soit démarré et que le modèle soit disponible :

```powershell
# Vérifier que Ollama tourne
curl http://localhost:11434/api/tags

# Si ça ne fonctionne pas, démarrer Ollama
# Voir SETUP_OLLAMA.md
```

### 4. Vérifier les erreurs dans la console du navigateur

Ouvre la console du navigateur (F12) et regarde les erreurs réseau. L'erreur 500 devrait afficher plus de détails.

## 🔧 Solutions courantes

### Problème : "Ollama connection error"

**Solution** : Démarrer Ollama et s'assurer que le modèle est téléchargé :
```powershell
ollama serve
# Dans un autre terminal
ollama pull llama3
```

### Problème : "No documents found"

**Solution** : Placer des documents dans `data/` :
- PDFs, images, fichiers texte
- Voir `README.md` pour les formats supportés

### Problème : Streaming ne fonctionne pas

**Solution** : Le système a un fallback automatique. Si le streaming natif échoue, il génère la réponse normalement et la stream caractère par caractère pour simuler l'effet.

## 📝 Logs utiles

Les erreurs sont loggées dans :
- Terminal où `python run_api.py` tourne
- Console du navigateur (F12)
- Fichier `test_streaming.py` pour les tests locaux

## 🆘 Si le problème persiste

1. Vérifie que toutes les dépendances sont installées :
   ```powershell
   pip install -r requirements.txt
   ```

2. Vérifie que la base de données est accessible :
   - Le fichier `storage/database.db` doit exister
   - Les permissions doivent être correctes

3. Teste l'endpoint non-streaming :
   ```powershell
   curl -X POST http://localhost:8001/ask \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{"question": "test", "conversation_id": 1}'
   ```

Si l'endpoint non-streaming fonctionne mais pas le streaming, c'est probablement un problème avec LangChain streaming.

