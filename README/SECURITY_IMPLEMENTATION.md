# 🔒 Implémentation Sécurité - RAG Photographie

## ✅ Fonctionnalités Implémentées

### 1. Rate Limiting ✅

**Package** : `slowapi>=0.1.9`

**Limites configurées** :
- `/auth/signup` : 5 requêtes/minute
- `/auth/login` : 10 requêtes/minute
- `/ask` : 20 requêtes/minute
- `/ask/stream` : 20 requêtes/minute

**Utilisation** :
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/endpoint")
@limiter.limit("20/minute")
async def endpoint(request: Request, ...):
    ...
```

### 2. Input Sanitization ✅

**Module** : `app/security.py`

**Fonctionnalités** :
- Échappement HTML
- Suppression des scripts dangereux
- Protection contre SQL injection
- Validation des emails
- Validation des mots de passe
- Limitation de longueur

**Utilisation** :
```python
from app.security import input_sanitizer

# Sanitize texte
clean_text = input_sanitizer.sanitize_text(user_input, max_length=1000)

# Sanitize question RAG
clean_question = input_sanitizer.sanitize_question(user_question)

# Valider mot de passe
is_valid, error = input_sanitizer.validate_password(password)
```

**Validation automatique** :
- Les modèles Pydantic utilisent automatiquement la sanitization via `@validator`

### 3. Secrets Management ✅

**Module** : `app/security.py` - `SecretsManager`

**Fonctionnalités** :
- Chiffrement des secrets avec Fernet (AES-128)
- Stockage sécurisé dans `.secrets` (chiffré)
- Priorité : Variables d'environnement > Fichier chiffré
- Génération de clés sécurisées

**Utilisation** :
```python
from app.security import get_secrets_manager, generate_secret_key

# Récupérer un secret
secrets_mgr = get_secrets_manager()
secret_key = secrets_mgr.get("SECRET_KEY")

# Générer une nouvelle clé
new_key = generate_secret_key(length=32)
```

**Fichiers créés** :
- `.secrets` : Fichier chiffré des secrets
- `.encryption_key` : Clé de chiffrement (permissions 600)

### 4. HTTPS/SSL Configuration ✅

**Fichiers créés** :
- `nginx.conf` : Configuration Nginx avec SSL
- `SSL_SETUP.md` : Guide d'installation

**Options disponibles** :
1. Let's Encrypt (gratuit, recommandé)
2. Traefik (reverse proxy avec SSL automatique)
3. Cloudflare (gratuit, facile)

## 📋 Checklist Sécurité

### Implémenté ✅
- [x] Rate Limiting
- [x] Input Sanitization
- [x] Secrets Management
- [x] HTTPS/SSL Configuration
- [x] Validation Pydantic
- [x] Échappement HTML
- [x] Protection SQL Injection
- [x] Headers de sécurité (dans nginx.conf)

### À configurer en production
- [ ] Certificat SSL installé
- [ ] Nginx/Traefik configuré
- [ ] Variables d'environnement sécurisées
- [ ] Secrets dans gestionnaire de secrets (AWS Secrets Manager, etc.)
- [ ] Monitoring des tentatives d'attaque
- [ ] Logs de sécurité

## 🚀 Déploiement

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Générer un SECRET_KEY

```python
from app.security import generate_secret_key
print(generate_secret_key())
```

Ajouter dans `.env` :
```env
SECRET_KEY=ton-secret-key-genere
```

### 3. Configurer HTTPS

Voir `SSL_SETUP.md` pour les instructions détaillées.

### 4. Vérifier la configuration

```bash
# Tester l'API
curl http://localhost:8001/health

# Tester le rate limiting
for i in {1..10}; do curl http://localhost:8001/auth/login; done
```

## 📊 Monitoring Sécurité

### Logs à surveiller

1. **Rate limiting** : Les requêtes bloquées sont loggées
2. **Input sanitization** : Les tentatives de XSS/SQL injection sont loggées
3. **Authentification** : Les échecs de connexion sont loggés

### Métriques recommandées

- Nombre de requêtes bloquées par rate limiting
- Tentatives d'injection détectées
- Échecs d'authentification
- Requêtes suspectes

## 🔧 Configuration Avancée

### Ajuster les limites de rate limiting

Dans `app/api.py` :
```python
@limiter.limit("30/minute")  # Augmenter la limite
```

### Personnaliser la sanitization

Dans `app/security.py` :
```python
# Ajouter des patterns personnalisés
DANGEROUS_PATTERNS.append((r'pattern', 'Description'))
```

### Utiliser un gestionnaire de secrets externe

Modifier `app/security.py` pour intégrer :
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault

## ⚠️ Notes Importantes

1. **Ne jamais commiter** :
   - `.secrets`
   - `.encryption_key`
   - `.env` (avec secrets)

2. **Permissions** :
   - `.secrets` : 600 (rw-------)
   - `.encryption_key` : 600 (rw-------)

3. **Backup** :
   - Sauvegarder `.encryption_key` de manière sécurisée
   - Sans cette clé, les secrets chiffrés sont inutilisables

4. **Production** :
   - Utiliser un gestionnaire de secrets cloud
   - Ne pas stocker les secrets dans le code
   - Utiliser HTTPS partout
   - Activer le monitoring

