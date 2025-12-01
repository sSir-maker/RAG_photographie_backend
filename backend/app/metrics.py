"""
Métriques personnalisées pour le monitoring.
"""

import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from threading import Lock

logger = logging.getLogger(__name__)


@dataclass
class Metric:
    """Représente une métrique."""

    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str]
    unit: Optional[str] = None


class MetricsCollector:
    """Collecteur de métriques personnalisées."""

    def __init__(self, max_history: int = 10000):
        self.metrics: deque = deque(maxlen=max_history)
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.timers: Dict[str, List[float]] = defaultdict(list)
        self.lock = Lock()

        # Métriques système
        self.start_time = datetime.utcnow()
        self.request_count = 0
        self.error_count = 0
        self.success_count = 0

    def increment(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Incrémente un compteur."""
        with self.lock:
            key = self._make_key(name, tags)
            self.counters[key] += value
            self._record_metric(name, float(self.counters[key]), tags, "count")

    def decrement(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Décrémente un compteur."""
        self.increment(name, -value, tags)

    def set_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Définit une jauge (valeur instantanée)."""
        with self.lock:
            key = self._make_key(name, tags)
            self.gauges[key] = value
            self._record_metric(name, value, tags, "gauge")

    def record_histogram(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Enregistre une valeur dans un histogramme."""
        with self.lock:
            key = self._make_key(name, tags)
            self.histograms[key].append(value)
            if len(self.histograms[key]) > 1000:  # Limiter la taille
                self.histograms[key] = self.histograms[key][-1000:]
            self._record_metric(name, value, tags, "histogram")

    def record_timer(self, name: str, duration_seconds: float, tags: Optional[Dict[str, str]] = None):
        """Enregistre une durée."""
        with self.lock:
            key = self._make_key(name, tags)
            self.timers[key].append(duration_seconds)
            if len(self.timers[key]) > 1000:
                self.timers[key] = self.timers[key][-1000:]
            self._record_metric(name, duration_seconds, tags, "timer")

    def time_function(self, name: str, tags: Optional[Dict[str, str]] = None):
        """Décorateur pour mesurer le temps d'exécution."""

        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start
                    self.record_timer(name, duration, tags)

            return wrapper

        return decorator

    def _make_key(self, name: str, tags: Optional[Dict[str, str]]) -> str:
        """Crée une clé unique pour une métrique avec tags."""
        if not tags:
            return name
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}[{tag_str}]"

    def _record_metric(self, name: str, value: float, tags: Optional[Dict[str, str]], unit: str):
        """Enregistre une métrique dans l'historique."""
        metric = Metric(name=name, value=value, timestamp=datetime.utcnow(), tags=tags or {}, unit=unit)
        self.metrics.append(metric)

    def get_counter(self, name: str, tags: Optional[Dict[str, str]] = None) -> int:
        """Récupère la valeur d'un compteur."""
        key = self._make_key(name, tags)
        return self.counters.get(key, 0)

    def get_gauge(self, name: str, tags: Optional[Dict[str, str]] = None) -> Optional[float]:
        """Récupère la valeur d'une jauge."""
        key = self._make_key(name, tags)
        return self.gauges.get(key)

    def get_histogram_stats(self, name: str, tags: Optional[Dict[str, str]] = None) -> Dict[str, float]:
        """Récupère les statistiques d'un histogramme."""
        key = self._make_key(name, tags)
        values = self.histograms.get(key, [])
        if not values:
            return {}

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "p50": self._percentile(values, 50),
            "p95": self._percentile(values, 95),
            "p99": self._percentile(values, 99),
        }

    def get_timer_stats(self, name: str, tags: Optional[Dict[str, str]] = None) -> Dict[str, float]:
        """Récupère les statistiques d'un timer."""
        key = self._make_key(name, tags)
        values = self.timers.get(key, [])
        if not values:
            return {}

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "p50": self._percentile(values, 50),
            "p95": self._percentile(values, 95),
            "p99": self._percentile(values, 99),
        }

    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calcule un percentile."""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]

    def get_system_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques système."""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()

        error_rate = 0.0
        if self.request_count > 0:
            error_rate = self.error_count / self.request_count

        success_rate = 0.0
        if self.request_count > 0:
            success_rate = self.success_count / self.request_count

        return {
            "uptime_seconds": uptime,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "success_count": self.success_count,
            "error_rate": error_rate,
            "success_rate": success_rate,
        }

    def get_all_metrics_summary(self) -> Dict[str, Any]:
        """Récupère un résumé de toutes les métriques."""
        return {
            "system": self.get_system_metrics(),
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {name: self.get_histogram_stats(name.split("[")[0]) for name in self.histograms.keys()},
            "timers": {name: self.get_timer_stats(name.split("[")[0]) for name in self.timers.keys()},
        }

    def record_request(self, success: bool = True):
        """Enregistre une requête."""
        with self.lock:
            self.request_count += 1
            if success:
                self.success_count += 1
            else:
                self.error_count += 1


# Instance globale
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Récupère l'instance globale du collecteur de métriques."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector
