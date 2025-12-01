# 🔴 Configuration Redis pour le Cache

## 📋 Vue d'ensemble

Redis est utilisé comme cache pour améliorer les performances en stockant les résultats de requêtes coûteuses.

## 🚀 Installation

### Windows

1. **Télécharger Redis** :
   - https://github.com/microsoftarchive/redis/releases
   - Ou utiliser WSL : `sudo apt install redis-server`

2. **Installer le client Python** :
   ```bash
   pip install redis
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### macOS

```bash
brew install redis
brew services start redis
```

### Docker

```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

## ⚙️ Configuration

### 1. Variables d'environnement

Dans `.env` :
```env
# Redis Cache
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600  # Durée de vie par défaut (1h)
```

### 2. Vérifier la connexion

```python
from app.cache import get_cache_manager

cache = get_cache_manager()
if cache.enabled:
    print("✅ Redis connecté")
    cache.set("test", "value")
    print(cache.get("test"))
else:
    print("❌ Redis non disponible")
```

## 🔧 Utilisation

### Cache manuel

```python
from app.cache import get_cache_manager

cache = get_cache_manager()

# Stocker
cache.set("user:123", {"name": "John"}, ttl=3600)

# Récupérer
user = cache.get("user:123")

# Supprimer
cache.delete("user:123")
```

### Décorateur @cached

```python
from app.cache import cached

@cached(ttl=3600, key_prefix="rag")
def expensive_function(param1, param2):
    # Calcul coûteux
    return result
```

## 📊 Monitoring

### Vérifier les statistiques Redis

```bash
redis-cli INFO stats
```

### Voir les clés en cache

```bash
redis-cli
> KEYS *
> GET cache_key
```

### Vider le cache

```python
from app.cache import get_cache_manager
cache = get_cache_manager()
cache.clear()
```

## 🐳 Docker Compose

```yaml
version: '3.8'

services:
  redis:
    image: redis:alpine
    container_name: rag-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  backend:
    # ...
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

volumes:
  redis_data:
```

## ✅ Avantages

- **Performance** : Réponses instantanées pour les données en cache
- **Réduction de charge** : Moins de requêtes à la base de données
- **Scalabilité** : Support de plusieurs instances
- **Flexibilité** : TTL configurable par clé

## 🔒 Sécurité

- Utiliser un mot de passe Redis en production
- Limiter l'accès réseau
- Utiliser SSL/TLS pour les connexions distantes

---

**✅ Redis configuré !**

