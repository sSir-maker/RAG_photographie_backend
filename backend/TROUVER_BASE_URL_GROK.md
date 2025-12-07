# Comment trouver le base_url de Grok

## 📍 Base URL de l'API Grok (X.AI)

D'après votre commande curl, voici comment identifier le base_url :

### ✅ Votre commande curl :
```bash
curl https://api.x.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer xai-..." \
    -d '{"messages": [...], "model": "grok-4-latest"}'
```

### 🔍 Analyse de l'URL :

1. **URL complète** : `https://api.x.ai/v1/chat/completions`
2. **Base URL** : `https://api.x.ai/v1` ← C'est ça !
3. **Endpoint** : `/chat/completions`

### 📝 Règle générale :

Pour trouver le base_url d'une API :
- Prenez l'URL complète : `https://api.x.ai/v1/chat/completions`
- Retirez le chemin de l'endpoint : `/chat/completions`
- Le reste est le base_url : `https://api.x.ai/v1`

## ✅ Configuration actuelle

Le base_url **`https://api.x.ai/v1`** est **déjà configuré par défaut** dans le code :

```python
# backend/app/llm_manager.py ligne 61
grok_base_url = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1")
```

## 🔧 Configuration dans votre `.env`

Vous n'avez **pas besoin** de spécifier le `GROK_BASE_URL` sauf si vous utilisez un proxy ou un service tiers.

Configuration minimale :
```bash
GROK_API_KEY=xai-E9sCz97XRN5AkTJZRMloETsK9DVjFUtWSGVuGX4knDqofEs9rttBO7PtZvjvQGeZqpr5CTcKzLIrAnZC
GROK_MODEL=grok-4-latest
```

Configuration complète (optionnelle) :
```bash
GROK_API_KEY=xai-E9sCz97XRN5AkTJZRMloETsK9DVjFUtWSGVuGX4knDqofEs9rttBO7PtZvjvQGeZqpr5CTcKzLIrAnZC
GROK_MODEL=grok-4-latest
GROK_BASE_URL=https://api.x.ai/v1
```

## 📚 Documentation officielle

- **Base URL** : `https://api.x.ai/v1`
- **Documentation** : [docs.x.ai](https://docs.x.ai)
- **Console** : [console.x.ai](https://console.x.ai)

## 🧪 Test de la connexion

Vous pouvez tester votre API avec le script PowerShell :
```powershell
.\backend\TEST_GROK_API.ps1 -ApiKey "xai-votre-cle-ici" -Model "grok-4-latest"
```

Ou avec curl :
```bash
curl https://api.x.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer xai-votre-cle-ici" \
    -d '{"messages": [{"role": "user", "content": "Hello!"}], "model": "grok-4-latest"}'
```

