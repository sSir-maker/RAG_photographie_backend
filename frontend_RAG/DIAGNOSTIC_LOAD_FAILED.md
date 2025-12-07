# 🔍 Diagnostic: Problème "Load failed" sur mobile

## 🐛 Problème
Le message "Load failed" apparaît sur mobile lors de la création de compte.

## ✅ Solutions appliquées

### 1. **Logs détaillés ajoutés**
- Logs de l'URL de l'API utilisée
- Logs des requêtes réseau
- Logs des erreurs détaillés

### 2. **Gestion d'erreurs améliorée**
- Messages d'erreur plus clairs
- Détection spécifique des erreurs réseau
- Timeout de 30 secondes

## 🔍 Comment diagnostiquer

### Étape 1: Ouvrir la console du navigateur
1. Sur mobile : Utiliser un outil de développement à distance (Chrome DevTools)
2. Sur desktop : Appuyer sur F12 ou clic droit > Inspecter

### Étape 2: Vérifier les logs
Cherchez dans la console les messages suivants :

```
🔧 API Configuration - VITE_API_URL: [URL]
🔧 API Configuration - Final API_URL: [URL]
🔍 Register - API URL: [URL complète]
📡 Register - Response status: [status]
✅ Register - Success
❌ Register - Error: [message]
```

### Étape 3: Vérifier l'URL de l'API
L'URL devrait être : `https://rag-photographie-backend.onrender.com`

Si vous voyez `http://localhost:8001`, cela signifie que `VITE_API_URL` n'est pas configuré sur Render.

## 🔧 Vérifications à faire

### 1. Vérifier la variable d'environnement sur Render
1. Aller sur https://dashboard.render.com
2. Sélectionner le service frontend
3. Aller dans "Environment"
4. Vérifier que `VITE_API_URL` est défini avec la valeur : `https://rag-photographie-backend.onrender.com`

### 2. Vérifier que le backend est accessible
Testez cette URL dans votre navigateur :
```
https://rag-photographie-backend.onrender.com/health
```

Vous devriez voir une réponse JSON. Si vous voyez une erreur, le backend n'est pas accessible.

### 3. Vérifier CORS
Le backend doit autoriser les requêtes depuis :
- `https://rag-photographie-frontend.onrender.com`

Vérifiez dans `backend/app/api.py` que cette origine est dans `default_origins`.

### 4. Redéployer le frontend
Après avoir modifié les variables d'environnement ou le code :
1. Aller sur Render
2. Cliquer sur "Manual Deploy" > "Deploy latest commit"
3. Attendre que le déploiement soit terminé

## 📊 Messages d'erreur possibles

| Message | Cause probable | Solution |
|---------|----------------|----------|
| "Impossible de se connecter au serveur" | Backend inaccessible | Vérifier que le backend est démarré sur Render |
| "La requête a pris trop de temps" | Timeout (30s) | Vérifier la connexion internet |
| "Erreur 404" | Endpoint incorrect | Vérifier l'URL de l'API |
| "Erreur 500" | Erreur serveur | Vérifier les logs du backend |
| "CORS error" | Problème CORS | Vérifier la configuration CORS du backend |

## 🚀 Actions immédiates

1. **Vérifier les logs de la console** du navigateur mobile
2. **Vérifier `VITE_API_URL`** sur Render
3. **Tester l'endpoint backend** : `https://rag-photographie-backend.onrender.com/health`
4. **Redéployer le frontend** si nécessaire

## 📝 Logs à partager pour diagnostic

Si le problème persiste, partagez :
1. Les logs de la console (messages avec 🔧, 🔍, 📡, ✅, ❌)
2. L'URL de l'API affichée dans les logs
3. Le message d'erreur exact
4. Le statut HTTP de la réponse (si disponible)

