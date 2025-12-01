"""
Dashboard de santé amélioré pour le monitoring.
"""
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import text

from .database import engine, check_db_connection, IS_POSTGRESQL
from .cache import get_cache_manager
from .metrics import get_metrics_collector
from .alerting import get_alert_manager, AlertLevel

logger = logging.getLogger(__name__)


class HealthChecker:
    """Vérificateur de santé du système."""
    
    def __init__(self):
        self.cache = get_cache_manager()
        self.metrics = get_metrics_collector()
        self.alerts = get_alert_manager()
    
    def check_database(self) -> Dict[str, Any]:
        """Vérifie la santé de la base de données."""
        status = {
            "status": "healthy",
            "connected": False,
            "response_time_ms": 0.0,
            "pool_size": 0,
            "active_connections": 0,
        }
        
        try:
            import time
            start = time.time()
            connected = check_db_connection()
            response_time = (time.time() - start) * 1000
            
            status["connected"] = connected
            status["response_time_ms"] = round(response_time, 2)
            
            if IS_POSTGRESQL:
                try:
                    with engine.connect() as conn:
                        # Vérifier le pool de connexions
                        result = conn.execute(text("""
                            SELECT count(*) as active_connections
                            FROM pg_stat_activity
                            WHERE datname = current_database()
                        """))
                        row = result.fetchone()
                        if row:
                            status["active_connections"] = row[0]
                        
                        # Taille du pool
                        pool = engine.pool
                        status["pool_size"] = pool.size()
                        status["checked_out"] = pool.checkedout()
                        status["overflow"] = pool.overflow()
                except Exception as e:
                    logger.warning(f"Impossible de récupérer les stats DB: {e}")
            
            if not connected:
                status["status"] = "unhealthy"
                status["error"] = "Impossible de se connecter à la base de données"
        except Exception as e:
            status["status"] = "unhealthy"
            status["error"] = str(e)
            logger.error(f"Erreur vérification DB: {e}")
        
        return status
    
    def check_cache(self) -> Dict[str, Any]:
        """Vérifie la santé du cache Redis."""
        status = {
            "status": "healthy" if self.cache.enabled else "disabled",
            "enabled": self.cache.enabled,
            "connected": False,
            "response_time_ms": 0.0,
        }
        
        if not self.cache.enabled:
            return status
        
        try:
            import time
            start = time.time()
            # Test de connexion
            test_key = "health_check_test"
            self.cache.set(test_key, "test", ttl=1)
            value = self.cache.get(test_key)
            response_time = (time.time() - start) * 1000
            
            status["connected"] = value == "test"
            status["response_time_ms"] = round(response_time, 2)
            
            if not status["connected"]:
                status["status"] = "unhealthy"
        except Exception as e:
            status["status"] = "unhealthy"
            status["error"] = str(e)
            logger.error(f"Erreur vérification cache: {e}")
        
        return status
    
    def check_llm(self) -> Dict[str, Any]:
        """Vérifie la santé du service LLM (Ollama)."""
        status = {
            "status": "unknown",
            "available": False,
            "response_time_ms": 0.0,
        }
        
        try:
            import requests
            import time
            from .config import settings
            
            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            start = time.time()
            
            response = requests.get(f"{ollama_url}/api/tags", timeout=2)
            response_time = (time.time() - start) * 1000
            
            status["available"] = response.status_code == 200
            status["response_time_ms"] = round(response_time, 2)
            status["status"] = "healthy" if status["available"] else "unhealthy"
            
            if status["available"]:
                try:
                    models = response.json().get("models", [])
                    status["models_count"] = len(models)
                    status["model_names"] = [m.get("name", "") for m in models[:5]]
                except:
                    pass
        except Exception as e:
            status["status"] = "unhealthy"
            status["error"] = str(e)
            logger.debug(f"Ollama non disponible: {e}")
        
        return status
    
    def get_system_health(self) -> Dict[str, Any]:
        """Récupère l'état de santé complet du système."""
        db_health = self.check_database()
        cache_health = self.check_cache()
        llm_health = self.check_llm()
        
        # Déterminer le statut global
        overall_status = "healthy"
        if db_health["status"] != "healthy":
            overall_status = "unhealthy"
        elif cache_health["status"] == "unhealthy" and cache_health["enabled"]:
            overall_status = "degraded"
        elif llm_health["status"] == "unhealthy":
            overall_status = "degraded"
        
        # Métriques système
        system_metrics = self.metrics.get_system_metrics()
        
        # Alertes récentes
        recent_alerts = self.alerts.get_recent_alerts(hours=1)
        critical_alerts = [a for a in recent_alerts if a.level == AlertLevel.CRITICAL]
        error_alerts = [a for a in recent_alerts if a.level == AlertLevel.ERROR]
        
        if critical_alerts:
            overall_status = "critical"
        elif error_alerts:
            overall_status = "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": system_metrics.get("uptime_seconds", 0),
            "services": {
                "database": db_health,
                "cache": cache_health,
                "llm": llm_health,
            },
            "metrics": {
                "requests": {
                    "total": system_metrics.get("request_count", 0),
                    "success": system_metrics.get("success_count", 0),
                    "errors": system_metrics.get("error_count", 0),
                    "error_rate": system_metrics.get("error_rate", 0.0),
                    "success_rate": system_metrics.get("success_rate", 0.0),
                },
            },
            "alerts": {
                "recent_count": len(recent_alerts),
                "critical_count": len(critical_alerts),
                "error_count": len(error_alerts),
                "recent": [
                    {
                        "title": a.title,
                        "level": a.level.value,
                        "timestamp": a.timestamp.isoformat(),
                    }
                    for a in recent_alerts[:10]
                ],
            },
        }
    
    def get_detailed_health(self) -> Dict[str, Any]:
        """Récupère un rapport de santé détaillé."""
        health = self.get_system_health()
        
        # Ajouter plus de détails
        health["detailed_metrics"] = self.metrics.get_all_metrics_summary()
        
        # Statistiques de performance
        timer_stats = {}
        for name in self.metrics.timers.keys():
            base_name = name.split("[")[0]
            if base_name not in timer_stats:
                timer_stats[base_name] = self.metrics.get_timer_stats(base_name)
        
        health["performance"] = {
            "timers": timer_stats,
        }
        
        return health

