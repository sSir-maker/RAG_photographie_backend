# 🔍 Diagnostic : Login retourne HTML au lieu de JSON

## 🚨 **Problème**

Le frontend reçoit du **HTML** avec un **status 200** au lieu de JSON lors de la connexion.

```
Status: 200 OK
Content: <!DOCTYPE html>...
```

## ✅ **Ce qui fonctionne**

- ✅ Le backend retourne bien du JSON quand testé directement avec PowerShell/curl
- ✅ Les modifications sont poussées sur GitHub (commit `b66aed9`)
- ✅ Les gestionnaires d'exceptions garantissent du JSON

## 🔍 **Causes possibles**

### **1. Render n'a pas redéployé le backend**

Les modifications ne sont peut-être pas encore actives sur Render.

**Solution :**
1. Allez sur https://dashboard.render.com
2. Vérifiez le service `rag-photographie-backend`
3. Regardez les logs pour voir si le déploiement est terminé
4. Déclenchez un redéploiement manuel si nécessaire

### **2. Service Render en sommeil (free tier)**

Sur le free tier, Render met les services en sommeil après 15 minutes d'inactivité.

**Symptômes :**
- La première requête peut prendre 30-60 secondes
- Render peut retourner une page HTML "Service starting" avec status 200

**Solution :**
- Attendez 30-60 secondes après la première requête
- Ou utilisez un plan payant pour éviter le sommeil

### **3. Problème de CORS**

Le navigateur peut bloquer la requête et afficher une page d'erreur HTML.

**Vérification :**
```javascript
// Dans la console du navigateur (F12)
fetch('https://rag-photographie-backend.onrender.com/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({email: 'test@test.com', password: 'test'})
})
.then(r => {
  console.log('Status:', r.status);
  console.log('CORS headers:', r.headers.get('access-control-allow-origin'));
  return r.text();
})
.then(t => {
  console.log('First 200 chars:', t.substring(0, 200));
  if (t.startsWith('<!DOCTYPE')) {
    console.error('❌ HTML détecté !');
  }
});
```

**Solution :** Vérifiez la configuration CORS dans `backend/app/api.py`

### **4. Proxy/CDN qui intercepte**

Un proxy ou CDN peut intercepter la requête et retourner du HTML.

**Vérification :**
- Vérifiez l'URL exacte appelée par le frontend
- Console : `console.log(API_ENDPOINTS.auth.login)`
- Doit être : `https://rag-photographie-backend.onrender.com/auth/login`

### **5. Cache du navigateur**

Le navigateur peut avoir mis en cache une ancienne réponse HTML.

**Solution :**
- Videz le cache du navigateur
- Utilisez le mode navigation privée
- Forcez le rechargement (Ctrl+F5)

## 🛠️ **Diagnostic étape par étape**

### **Étape 1 : Vérifier l'URL du backend**

Ouvrez la console du navigateur (F12) et vérifiez :

```javascript
console.log('API URL:', API_ENDPOINTS.auth.login);
```

Doit afficher : `https://rag-photographie-backend.onrender.com/auth/login`

### **Étape 2 : Tester directement le backend**

Depuis PowerShell :

```powershell
$body = @{email="test@test.com";password="test"} | ConvertTo-Json
Invoke-RestMethod -Uri "https://rag-photographie-backend.onrender.com/auth/login" -Method POST -Body $body -ContentType "application/json"
```

**Résultat attendu :** JSON (succès ou erreur 401)

### **Étape 3 : Vérifier les logs Render**

1. Allez sur Render Dashboard
2. Ouvrez le service backend
3. Cliquez sur "Logs"
4. Cherchez des erreurs au démarrage ou lors des requêtes

### **Étape 4 : Vérifier le Content-Type**

Dans la console du navigateur :

```javascript
fetch('https://rag-photographie-backend.onrender.com/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({email: 'test@test.com', password: 'test'})
})
.then(r => {
  console.log('Content-Type:', r.headers.get('content-type'));
  return r.text();
})
.then(t => {
  console.log('Premiers caractères:', t.substring(0, 100));
});
```

**Résultat attendu :**
- Content-Type : `application/json`
- Premiers caractères : `{"detail":...}` ou `{"access_token":...}`

## 🔧 **Solutions**

### **Solution 1 : Redéployer le backend**

1. Render Dashboard → Service backend
2. "Manual Deploy" → "Deploy latest commit"
3. Attendez 2-3 minutes
4. Testez à nouveau

### **Solution 2 : Vérifier la configuration CORS**

Vérifiez que le frontend est dans la liste des origines autorisées :

```python
# backend/app/api.py
default_origins = [
    "https://rag-photographie-frontend.onrender.com",  # Frontend déployé
    # ...
]
```

### **Solution 3 : Ajouter des logs détaillés**

Le frontend a été modifié pour ajouter des logs. Ouvrez la console (F12) et regardez :

- 🔍 L'URL appelée
- 📡 Le status de la réponse
- 📡 Le Content-Type
- 📡 Un aperçu de la réponse

### **Solution 4 : Vérifier les variables d'environnement Render**

Vérifiez que les variables d'environnement sont correctes sur Render :

- `FRONTEND_URL` : `https://rag-photographie-frontend.onrender.com`
- `ENVIRONMENT` : `production`

## 📝 **Modifications apportées au frontend**

Le frontend a été modifié pour :

1. ✅ Ajouter des logs détaillés
2. ✅ Détecter le HTML même avec status 200
3. ✅ Afficher des messages d'erreur plus clairs

## ✅ **Résultat attendu après correction**

```json
// Succès (200)
{
  "access_token": "eyJhbGciOiJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}

// Erreur (401)
{
  "detail": "Email ou mot de passe incorrect"
}
```

**Plus jamais de HTML !**

## 🚀 **Prochaines étapes**

1. **Vérifiez les logs dans la console du navigateur** (F12)
2. **Vérifiez les logs Render** pour voir si le backend a des erreurs
3. **Testez directement le backend** avec PowerShell pour confirmer qu'il retourne du JSON
4. **Redéployez le backend** si nécessaire
5. **Videz le cache du navigateur** et réessayez

