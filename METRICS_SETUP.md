# 📊 Configuration des Métriques Personnalisées

## 📋 Vue d'ensemble

Le système de métriques permet de collecter et analyser les performances de l'application.

## 🚀 Utilisation

### Compteurs

```python
from app.metrics import get_metrics_collector

metrics = get_metrics_collector()

# Incrémenter
metrics.increment("requests.total")
metrics.increment("cache.hits", tags={"type": "rag"})

# Décrémenter
metrics.decrement("active_connections")
```

### Jauges (valeurs instantanées)

```python
# Définir une valeur
metrics.set_gauge("memory.used_mb", 512.5)
metrics.set_gauge("database.pool_size", 20)
```

### Histogrammes

```python
# Enregistrer une valeur
metrics.record_histogram("response.size_bytes", 1024)
metrics.record_histogram("document.pages", 10, tags={"type": "pdf"})
```

### Timers (durées)

```python
# Enregistrer une durée
metrics.record_timer("rag.generation_time", 2.5)

# Ou utiliser le décorateur
@metrics.time_function("expensive_operation")
def my_function():
    # ...
    pass
```

### Métriques système automatiques

Le système enregistre automatiquement :
- `requests.total` : Nombre total de requêtes
- `requests.success` : Requêtes réussies
- `requests.errors` : Requêtes en erreur
- `uptime_seconds` : Temps de fonctionnement

## 📊 Récupérer les métriques

### Via l'API

```bash
GET /metrics
```

Retourne :
```json
{
  "system": {
    "uptime_seconds": 3600,
    "request_count": 1000,
    "error_count": 50,
    "error_rate": 0.05
  },
  "counters": {
    "requests.total": 1000,
    "cache.hits": 750
  },
  "gauges": {
    "memory.used_mb": 512.5
  },
  "histograms": {
    "response.size_bytes": {
      "count": 1000,
      "min": 100,
      "max": 5000,
      "mean": 1500,
      "p50": 1200,
      "p95": 3000,
      "p99": 4500
    }
  },
  "timers": {
    "rag.generation_time": {
      "count": 1000,
      "min": 0.5,
      "max": 10.0,
      "mean": 2.5,
      "p50": 2.0,
      "p95": 5.0,
      "p99": 8.0
    }
  }
}
```

### En Python

```python
from app.metrics import get_metrics_collector

metrics = get_metrics_collector()

# Récupérer un compteur
count = metrics.get_counter("requests.total")

# Récupérer une jauge
memory = metrics.get_gauge("memory.used_mb")

# Statistiques d'histogramme
stats = metrics.get_histogram_stats("response.size_bytes")
print(f"Moyenne: {stats['mean']}, P95: {stats['p95']}")

# Statistiques de timer
timer_stats = metrics.get_timer_stats("rag.generation_time")
print(f"Temps moyen: {timer_stats['mean']}s")
```

## 🎯 Métriques Recommandées

### Performance

- `rag.response_time` : Temps de réponse RAG
- `rag.retrieval_time` : Temps de récupération
- `rag.generation_time` : Temps de génération
- `api.request_time` : Temps de traitement API

### Cache

- `cache.hits` : Nombre de hits
- `cache.misses` : Nombre de misses
- `cache.hit_rate` : Taux de hit

### Base de données

- `db.query_time` : Temps de requête
- `db.connection_pool_size` : Taille du pool
- `db.active_connections` : Connexions actives

### OCR

- `ocr.processing_time` : Temps de traitement OCR
- `ocr.confidence_score` : Score de confiance moyen
- `ocr.documents_processed` : Documents traités

## 📈 Intégration avec Alertes

Les métriques peuvent déclencher des alertes :

```python
from app.metrics import get_metrics_collector
from app.alerting import get_alert_manager

metrics = get_metrics_collector()
alerts = get_alert_manager()

# Récupérer les métriques
all_metrics = metrics.get_all_metrics_summary()

# Vérifier les seuils
metrics_dict = {
    "error_rate": all_metrics["system"]["error_rate"],
    "response_time": all_metrics["timers"].get("rag.response_time", {}).get("p95", 0),
}

alerts.check_thresholds(metrics_dict)
```

## ✅ Checklist

- [ ] Métriques enregistrées dans le code
- [ ] Endpoint `/metrics` accessible
- [ ] Intégration avec alertes configurée
- [ ] Dashboard de santé utilise les métriques

---

**✅ Métriques personnalisées configurées !**

