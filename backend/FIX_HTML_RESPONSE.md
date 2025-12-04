# 🔧 Fix : Backend retourne du HTML au lieu de JSON

## 🚨 **Problème identifié**

Le backend retournait des réponses **HTML** au lieu de **JSON** lors des tentatives de connexion, même avec un status code **200 OK**.

```
POST /auth/login → Attendu: JSON {token: "...", user: {...}}
                 → Reçu: HTML <!DOCTYPE html>... (Status: 200 OK)
```

## 🔍 **Causes possibles identifiées**

1. **Exceptions non gérées** → FastAPI retourne une page HTML d'erreur par défaut
2. **Rate limiting** → Le gestionnaire par défaut retourne du HTML
3. **Erreurs de validation Pydantic** → Retournent du HTML au lieu de JSON
4. **Route dupliquée** → Conflit de routes `/ask` causant des erreurs

## ✅ **Solutions implémentées**

### 1. **Gestionnaire d'exceptions global**

Ajout d'un gestionnaire qui intercepte **toutes** les exceptions et retourne du JSON :

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Gestionnaire d'exceptions global pour retourner du JSON au lieu de HTML."""
    logger.error(f"Exception non gérée: {type(exc).__name__}: {str(exc)}", exc_info=True)
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erreur interne du serveur",
            "error": str(exc),
            "type": type(exc).__name__,
        },
    )
```

### 2. **Gestionnaire de validation Pydantic**

Gestionnaire spécifique pour les erreurs de validation :

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Gestionnaire pour les erreurs de validation Pydantic (retourne JSON)."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Erreur de validation",
            "errors": exc.errors(),
        },
    )
```

### 3. **Gestionnaire de rate limiting personnalisé**

Le gestionnaire par défaut de `slowapi` retourne du HTML. Remplacement par un gestionnaire JSON :

```python
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Gestionnaire personnalisé pour les erreurs de rate limiting (retourne JSON)."""
    response = JSONResponse(
        status_code=429,
        content={
            "detail": "Trop de requêtes. Veuillez réessayer plus tard.",
            "retry_after": str(exc.retry_after) if exc.retry_after else None,
        },
        headers={"Retry-After": str(exc.retry_after)} if exc.retry_after else {},
    )
    return response
```

### 4. **Amélioration des routes login/signup**

- Ajout de gestion d'erreurs complète avec `try/except`
- Logs détaillés pour le debugging
- Forçage du `Content-Type: application/json`
- Utilisation de `JSONResponse` explicite

```python
@app.post("/auth/login", response_model=AuthResponse)
async def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Tentative de connexion pour: {login_data.email}")
        # ... logique de connexion ...
        
        return JSONResponse(
            status_code=200,
            content=response_data.dict(),
            headers={"Content-Type": "application/json"},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de la connexion: {str(e)}")
```

### 5. **Suppression route dupliquée**

Suppression de la route `/ask` en double qui causait un conflit.

## 📊 **Résultat attendu**

### **Avant** ❌
```
Status: 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head><title>500 Internal Server Error</title></head>
<body>...
```

### **Après** ✅
```json
Status: 200 OK
Content-Type: application/json

{
  "access_token": "eyJhbGciOiJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

## 🚀 **Déploiement**

Les modifications ont été poussées sur GitHub :
- **Commit** : `b66aed9`
- **Message** : `fix: Forcer toutes les réponses API en JSON au lieu de HTML`
- **Fichier modifié** : `backend/app/api.py`

Render redéploiera automatiquement le backend. Une fois déployé, toutes les réponses seront en JSON.

## ✅ **Vérifications à faire après déploiement**

1. **Test de connexion**
   ```bash
   curl -X POST https://rag-photographie-backend.onrender.com/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","password":"test"}'
   ```

2. **Vérifier le Content-Type**
   - Doit être `application/json`
   - Ne doit pas être `text/html`

3. **Tester depuis le frontend**
   - La connexion devrait fonctionner sans erreur "Unexpected token"
   - Les messages d'erreur devraient être en français et clairs

## 📝 **Notes**

- Toutes les exceptions sont maintenant loggées avec `exc_info=True` pour faciliter le debugging
- Le gestionnaire global capture toutes les exceptions non-HTTPException
- Les HTTPException sont toujours retournées en JSON grâce au gestionnaire global
- Le rate limiting retourne maintenant du JSON avec un status 429

