# 🔍 Diagnostic : Backend retourne HTML au lieu de JSON

## ✅ **Ce qui a été corrigé**

Les modifications ont été poussées sur GitHub et le backend retourne bien du JSON lorsque testé directement :

```bash
# Test direct du backend
curl -X POST https://rag-photographie-backend.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}'

# Résultat : JSON avec Content-Type: application/json ✅
```

## 🔄 **Prochaines étapes**

### 1. **Vérifier le déploiement Render**

Le backend doit être redéployé sur Render avec les nouvelles modifications :

1. **Allez sur Render Dashboard** : https://dashboard.render.com
2. **Vérifiez le service backend** : `rag-photographie-backend`
3. **Vérifiez les logs** : Cliquez sur "Logs" pour voir si le déploiement est en cours
4. **Déploiement manuel** : Si nécessaire, cliquez sur "Manual Deploy" → "Deploy latest commit"

### 2. **Tester après redéploiement**

Une fois le backend redéployé, testez depuis le frontend mobile :

```javascript
// Dans la console du navigateur (F12)
fetch('https://rag-photographie-backend.onrender.com/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'test@test.com',
    password: 'test123'
  })
})
.then(response => {
  console.log('Status:', response.status);
  console.log('Content-Type:', response.headers.get('content-type'));
  return response.text();
})
.then(data => {
  console.log('Réponse:', data.substring(0, 200));
  if (data.trim().startsWith('<!DOCTYPE') || data.trim().startsWith('<html')) {
    console.error('❌ HTML détecté !');
  } else {
    console.log('✅ JSON détecté !');
  }
});
```

### 3. **Si le problème persiste**

Si après redéploiement le problème persiste, vérifiez :

#### **A. Cache du navigateur**
- Videz le cache du navigateur mobile
- Utilisez le mode navigation privée
- Ou forcez le rechargement (Ctrl+F5)

#### **B. Vérification des logs Render**
- Allez sur Render Dashboard → Service backend → Logs
- Cherchez des erreurs au démarrage
- Vérifiez que FastAPI démarre correctement

#### **C. Vérification de l'URL**
- Vérifiez que le frontend utilise la bonne URL du backend
- Console du navigateur : `console.log(API_ENDPOINTS.auth.login)`
- Doit être : `https://rag-photographie-backend.onrender.com/auth/login`

#### **D. Vérification CORS**
- Ouvrez la console du navigateur (F12)
- Onglet "Network"
- Regardez la requête `/auth/login`
- Vérifiez les headers CORS dans la réponse

### 4. **Test direct du endpoint**

Testez directement depuis votre machine :

```bash
# PowerShell
$body = @{email="test@test.com";password="test"} | ConvertTo-Json
Invoke-WebRequest -Uri "https://rag-photographie-backend.onrender.com/auth/login" `
  -Method POST -Body $body -ContentType "application/json"
```

## 📝 **Modifications apportées**

### **Fichiers modifiés :**
- `backend/app/api.py`

### **Améliorations :**
1. ✅ Gestionnaire d'exceptions global (retourne JSON)
2. ✅ Gestionnaire rate limiting personnalisé (JSON)
3. ✅ Gestionnaire erreurs validation Pydantic (JSON)
4. ✅ Routes login/signup améliorées avec gestion d'erreurs
5. ✅ Logs détaillés pour debugging
6. ✅ Suppression route `/ask` dupliquée

### **Commit :**
- Hash : `b66aed9`
- Message : `fix: Forcer toutes les réponses API en JSON au lieu de HTML`

## 🚨 **Cas spéciaux**

### **Si Render retourne du HTML :**

Render peut retourner une page HTML dans certains cas :

1. **Service en cours de démarrage** : Attendez 30-60 secondes
2. **Service en erreur** : Vérifiez les logs Render
3. **Timeout** : Le service peut être "en sommeil" (free tier)
4. **Mauvaise configuration** : Vérifiez `render.yaml`

### **Solution temporaire :**

Si le service Render est "en sommeil", la première requête peut prendre 30-60 secondes. C'est normal sur le free tier.

## ✅ **Résultat attendu**

Après redéploiement, toutes les réponses du backend seront en JSON :

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

// Erreur (500)
{
  "detail": "Erreur interne du serveur",
  "error": "...",
  "type": "ExceptionType"
}
```

Plus jamais de HTML ! 🎉

