"""
Module de cache Redis pour améliorer les performances.
"""

import json
import logging
from typing import Optional, Any, Union
from functools import wraps
import hashlib

logger = logging.getLogger(__name__)

# Tentative d'import Redis
try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis non installé. Le cache sera désactivé.")


class CacheManager:
    """Gestionnaire de cache Redis."""

    def __init__(self, redis_url: Optional[str] = None, default_ttl: int = 3600):
        """
        Initialise le gestionnaire de cache.

        Args:
            redis_url: URL de connexion Redis (ex: redis://localhost:6379/0)
            default_ttl: Durée de vie par défaut en secondes (1h par défaut)
        """
        self.default_ttl = default_ttl
        self.redis_client = None
        self.enabled = False

        if not REDIS_AVAILABLE:
            logger.warning("Redis non disponible. Cache désactivé.")
            return

        try:
            if redis_url:
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
            else:
                # Connexion par défaut
                self.redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

            # Test de connexion
            self.redis_client.ping()
            self.enabled = True
            logger.info("✅ Cache Redis activé")
        except Exception as e:
            logger.warning(f"Redis non disponible: {e}. Cache désactivé.")
            self.enabled = False
            self.redis_client = None

    def get(self, key: str) -> Optional[Any]:
        """
        Récupère une valeur du cache.

        Args:
            key: Clé du cache

        Returns:
            Valeur en cache ou None si non trouvée
        """
        if not self.enabled or not self.redis_client:
            return None

        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du cache: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Stocke une valeur dans le cache.

        Args:
            key: Clé du cache
            value: Valeur à stocker (sera sérialisée en JSON)
            ttl: Durée de vie en secondes (None = default_ttl)

        Returns:
            True si succès, False sinon
        """
        if not self.enabled or not self.redis_client:
            return False

        try:
            ttl = ttl or self.default_ttl
            serialized = json.dumps(value, default=str)
            self.redis_client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.error(f"Erreur lors du stockage dans le cache: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Supprime une clé du cache.

        Args:
            key: Clé à supprimer

        Returns:
            True si succès, False sinon
        """
        if not self.enabled or not self.redis_client:
            return False

        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du cache: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """
        Supprime toutes les clés correspondant à un pattern.

        Args:
            pattern: Pattern Redis (ex: "user:*")

        Returns:
            Nombre de clés supprimées
        """
        if not self.enabled or not self.redis_client:
            return 0

        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression par pattern: {e}")
            return 0

    def clear(self) -> bool:
        """
        Vide tout le cache.

        Returns:
            True si succès, False sinon
        """
        if not self.enabled or not self.redis_client:
            return False

        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            logger.error(f"Erreur lors du vidage du cache: {e}")
            return False

    def exists(self, key: str) -> bool:
        """
        Vérifie si une clé existe dans le cache.

        Args:
            key: Clé à vérifier

        Returns:
            True si la clé existe, False sinon
        """
        if not self.enabled or not self.redis_client:
            return False

        try:
            return self.redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du cache: {e}")
            return False


# Instance globale
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """Récupère l'instance globale du gestionnaire de cache."""
    global _cache_manager
    if _cache_manager is None:
        import os

        redis_url = os.getenv("REDIS_URL", None)
        default_ttl = int(os.getenv("CACHE_TTL", "3600"))
        _cache_manager = CacheManager(redis_url=redis_url, default_ttl=default_ttl)
    return _cache_manager


def cache_key(*args, **kwargs) -> str:
    """
    Génère une clé de cache à partir d'arguments.

    Args:
        *args: Arguments positionnels
        **kwargs: Arguments nommés

    Returns:
        Clé de cache (hash)
    """
    key_data = {"args": args, "kwargs": sorted(kwargs.items())}
    key_string = json.dumps(key_data, default=str, sort_keys=True)
    return hashlib.md5(key_string.encode()).hexdigest()


def cached(ttl: Optional[int] = None, key_prefix: str = "cache"):
    """
    Décorateur pour mettre en cache le résultat d'une fonction.

    Args:
        ttl: Durée de vie en secondes (None = default_ttl)
        key_prefix: Préfixe pour la clé de cache

    Example:
        @cached(ttl=3600, key_prefix="rag")
        def answer_question(question: str):
            # ...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache_manager()

            # Générer la clé de cache
            cache_key_value = f"{key_prefix}:{func.__name__}:{cache_key(*args, **kwargs)}"

            # Essayer de récupérer depuis le cache
            cached_result = cache.get(cache_key_value)
            if cached_result is not None:
                logger.debug(f"Cache hit: {cache_key_value}")
                return cached_result

            # Exécuter la fonction
            logger.debug(f"Cache miss: {cache_key_value}")
            result = func(*args, **kwargs)

            # Stocker dans le cache
            cache.set(cache_key_value, result, ttl=ttl)

            return result

        return wrapper

    return decorator
