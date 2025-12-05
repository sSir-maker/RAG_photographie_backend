# Configuration Grok (X.AI)

Ce guide explique comment configurer Grok comme LLM pour le projet RAG Photographie.

## Prérequis

1. **Clé API X.AI** : Vous devez avoir une clé API X.AI pour utiliser Grok.
   - Inscrivez-vous sur [console.x.ai](https://console.x.ai) si vous n'avez pas encore de compte
   - Créez une clé API dans votre espace personnel

## Configuration

### Option 1 : Variables d'environnement (Recommandé)

Créez ou modifiez le fichier `.env` dans le répertoire `backend/` :

```bash
# Configuration Grok (X.AI)
GROK_API_KEY=xai-votre-cle-api-ici
GROK_MODEL=grok-beta
GROK_BASE_URL=https://api.x.ai/v1
```

**Note :** Vous pouvez aussi utiliser `XAI_API_KEY` au lieu de `GROK_API_KEY`.

### Option 2 : Variables d'environnement système

Configurez les variables d'environnement dans votre système :

**Linux/Mac :**
```bash
export GROK_API_KEY="xai-votre-cle-api-ici"
export GROK_MODEL="grok-beta"
```

**Windows (PowerShell) :**
```powershell
$env:GROK_API_KEY="xai-votre-cle-api-ici"
$env:GROK_MODEL="grok-beta"
```

## Modèles disponibles

Grok propose plusieurs modèles :

- `grok-beta` : Modèle par défaut (recommandé)
- `grok-2` : Dernière version (si disponible)

Consultez la [documentation X.AI](https://docs.x.ai) pour la liste complète des modèles.

## Vérification de la configuration

Une fois configuré, le système utilisera automatiquement Grok au lieu d'Ollama si la clé API est présente.

Vous pouvez vérifier que Grok est bien configuré en regardant les logs au démarrage :
```
🚀 Grok (X.AI) configuré comme LLM par défaut
```

## Fallback

Si `GROK_API_KEY` n'est pas configurée, le système utilisera automatiquement Ollama comme fallback.

## Dépannage

### Erreur : "GROK_API_KEY not found"
- Vérifiez que la variable d'environnement `GROK_API_KEY` est bien configurée
- Redémarrez l'application après avoir configuré la variable

### Erreur : "401 Unauthorized"
- Vérifiez que votre clé API est valide
- Assurez-vous que votre compte X.AI est actif et dispose de crédits

### Le système utilise toujours Ollama
- Vérifiez les logs au démarrage
- Assurez-vous que `GROK_API_KEY` est correctement configurée dans le fichier `.env` ou les variables d'environnement

## Support

Pour plus d'informations sur l'API X.AI :
- [Documentation officielle X.AI](https://docs.x.ai)
- [Console X.AI](https://console.x.ai)

