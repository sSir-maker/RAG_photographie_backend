# 🔧 Fix : Erreur CORS

## ❌ **Problème identifié**

```
Access to fetch at 'https://rag-photographie-backend.onrender.com/health' 
from origin 'https://rag-photographie-frontend.onrender.com' has been blocked 
by CORS policy: Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## 🔍 **Causes**

1. Le middleware CORS était configuré APRÈS les gestionnaires d'exceptions
2. Les headers CORS n'étaient pas ajoutés dans les gestionnaires d'exceptions
3. Les requêtes OPTIONS (preflight) n'étaient pas gérées correctement

## ✅ **Solutions appliquées**

### **1. Déplacer CORS avant les gestionnaires d'exceptions**

Le middleware CORS doit être configuré AVANT les gestionnaires d'exceptions pour que les headers soient correctement ajoutés.

### **2. Ajouter headers CORS dans les gestionnaires d'exceptions**

Les gestionnaires d'exceptions ajoutent maintenant les headers CORS dans leurs réponses :

```python
# Obtenir l'origine de la requête pour les headers CORS
origin = request.headers.get("origin")
cors_headers = {}
if origin in default_origins:
    cors_headers = {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Credentials": "true",
    }
```

### **3. Ajouter endpoint OPTIONS pour preflight requests**

Un endpoint OPTIONS explicite a été ajouté pour gérer les requêtes preflight :

```python
@app.options("/{full_path:path}")
async def options_handler(full_path: str, request: Request):
    """Gère les requêtes OPTIONS (preflight CORS) pour tous les endpoints."""
    origin = request.headers.get("origin")
    if origin in default_origins:
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "3600",
            },
        )
```

### **4. Logger les origines CORS configurées**

Les origines CORS sont maintenant loggées au démarrage pour faciliter le debugging.

## 📋 **Origines CORS autorisées**

- `http://localhost:3000` (développement)
- `http://localhost:3001` (développement alternatif)
- `http://127.0.0.1:3000` (développement localhost)
- `https://rag-photographie-frontend.onrender.com` (production)

Plus toutes les origines définies dans :
- Variable d'environnement `CORS_ORIGINS` (séparées par des virgules)
- Variable d'environnement `FRONTEND_URL`

## 🚀 **Déploiement**

Les modifications ont été poussées sur GitHub :
- **Commit** : `4d89026`
- **Message** : `fix: Corriger configuration CORS`

Render redéploiera automatiquement le backend. Une fois déployé, les erreurs CORS devraient être résolues.

## ✅ **Résultat attendu**

Après redéploiement :
- ✅ Les requêtes depuis le frontend seront autorisées
- ✅ Les headers CORS seront présents dans toutes les réponses
- ✅ Les requêtes OPTIONS (preflight) seront gérées correctement
- ✅ Plus d'erreur "blocked by CORS policy"

## 🔍 **Vérification**

Pour vérifier que CORS fonctionne :

1. **Ouvrir la console du navigateur** (F12)
2. **Onglet Network**
3. **Faire une requête vers le backend**
4. **Vérifier les headers de la réponse** :
   - `Access-Control-Allow-Origin: https://rag-photographie-frontend.onrender.com`
   - `Access-Control-Allow-Credentials: true`
   - `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`

## 📝 **Note importante**

Le middleware CORS doit être configuré **AVANT** les gestionnaires d'exceptions dans FastAPI pour que les headers soient correctement ajoutés à toutes les réponses.

