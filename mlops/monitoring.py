"""
Système de monitoring pour le pipeline MLOps RAG.
Collecte et analyse les métriques de performance.
"""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class PipelineMetrics:
    """Métriques d'une exécution du pipeline."""
    timestamp: str
    duration_seconds: float
    documents_processed: int
    documents_failed: int
    avg_ocr_confidence: float
    vector_store_size_mb: float
    validation_passed: bool
    test_questions_count: int
    test_questions_passed: int


@dataclass
class RAGMetrics:
    """Métriques d'une requête RAG."""
    timestamp: str
    question: str
    answer_length: int
    sources_count: int
    response_time_ms: float
    user_rating: Optional[int] = None
    user_feedback: Optional[str] = None


class MetricsCollector:
    """Collecteur de métriques pour le monitoring."""
    
    def __init__(self, metrics_dir: Path = None):
        if metrics_dir is None:
            metrics_dir = Path("mlops/metrics")
        self.metrics_dir = metrics_dir
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        self.pipeline_metrics_file = self.metrics_dir / "pipeline_metrics.jsonl"
        self.rag_metrics_file = self.metrics_dir / "rag_metrics.jsonl"
    
    def log_pipeline_metrics(self, metrics: PipelineMetrics):
        """Enregistre les métriques d'une exécution du pipeline."""
        with open(self.pipeline_metrics_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(metrics), ensure_ascii=False) + '\n')
        logger.info(f"Métriques pipeline enregistrées: {metrics}")
    
    def log_rag_metrics(self, metrics: RAGMetrics):
        """Enregistre les métriques d'une requête RAG."""
        with open(self.rag_metrics_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(metrics), ensure_ascii=False) + '\n')
        logger.debug(f"Métriques RAG enregistrées: {metrics}")
    
    def get_pipeline_metrics(self, days: int = 7) -> List[Dict[str, Any]]:
        """Récupère les métriques du pipeline des N derniers jours."""
        metrics = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        if not self.pipeline_metrics_file.exists():
            return metrics
        
        with open(self.pipeline_metrics_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    metric = json.loads(line)
                    metric_date = datetime.fromisoformat(metric['timestamp'])
                    if metric_date >= cutoff_date:
                        metrics.append(metric)
                except Exception as e:
                    logger.warning(f"Erreur lecture métrique: {e}")
        
        return metrics
    
    def get_rag_metrics(self, days: int = 7) -> List[Dict[str, Any]]:
        """Récupère les métriques RAG des N derniers jours."""
        metrics = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        if not self.rag_metrics_file.exists():
            return metrics
        
        with open(self.rag_metrics_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    metric = json.loads(line)
                    metric_date = datetime.fromisoformat(metric['timestamp'])
                    if metric_date >= cutoff_date:
                        metrics.append(metric)
                except Exception as e:
                    logger.warning(f"Erreur lecture métrique RAG: {e}")
        
        return metrics
    
    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Calcule les statistiques agrégées."""
        pipeline_metrics = self.get_pipeline_metrics(days)
        rag_metrics = self.get_rag_metrics(days)
        
        stats = {
            "period_days": days,
            "pipeline_runs": len(pipeline_metrics),
            "rag_queries": len(rag_metrics),
        }
        
        if pipeline_metrics:
            stats["pipeline"] = {
                "avg_duration_seconds": sum(m.get("duration_seconds", 0) for m in pipeline_metrics) / len(pipeline_metrics),
                "avg_documents_processed": sum(m.get("documents_processed", 0) for m in pipeline_metrics) / len(pipeline_metrics),
                "avg_ocr_confidence": sum(m.get("avg_ocr_confidence", 0) for m in pipeline_metrics) / len(pipeline_metrics),
                "success_rate": sum(1 for m in pipeline_metrics if m.get("validation_passed")) / len(pipeline_metrics) * 100
            }
        
        if rag_metrics:
            stats["rag"] = {
                "avg_response_time_ms": sum(m.get("response_time_ms", 0) for m in rag_metrics) / len(rag_metrics),
                "avg_answer_length": sum(m.get("answer_length", 0) for m in rag_metrics) / len(rag_metrics),
                "avg_sources_count": sum(m.get("sources_count", 0) for m in rag_metrics) / len(rag_metrics),
                "avg_rating": sum(m.get("user_rating", 0) for m in rag_metrics if m.get("user_rating")) / max(1, sum(1 for m in rag_metrics if m.get("user_rating"))) if any(m.get("user_rating") for m in rag_metrics) else None
            }
        
        return stats


class HealthChecker:
    """Vérifie la santé du système RAG."""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
    
    def check_health(self) -> Dict[str, Any]:
        """Vérifie l'état de santé du système."""
        health = {
            "status": "healthy",
            "checks": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Vérifier le vector store
        from app.config import settings
        vector_store_path = settings.vector_store_dir / "index.faiss"
        health["checks"]["vector_store"] = {
            "exists": vector_store_path.exists(),
            "path": str(vector_store_path)
        }
        
        # Vérifier les données
        data_dir = settings.data_dir
        health["checks"]["data_dir"] = {
            "exists": data_dir.exists(),
            "file_count": len(list(data_dir.glob("*"))) if data_dir.exists() else 0
        }
        
        # Vérifier les métriques récentes
        stats = self.metrics_collector.get_statistics(days=1)
        health["checks"]["recent_activity"] = {
            "pipeline_runs_today": stats.get("pipeline_runs", 0),
            "rag_queries_today": stats.get("rag_queries", 0)
        }
        
        # Déterminer le statut global
        if not health["checks"]["vector_store"]["exists"]:
            health["status"] = "unhealthy"
        elif health["checks"]["recent_activity"]["pipeline_runs_today"] == 0:
            health["status"] = "warning"
        
        return health


if __name__ == "__main__":
    # Test du monitoring
    collector = MetricsCollector()
    stats = collector.get_statistics(days=7)
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    checker = HealthChecker()
    health = checker.check_health()
    print("\nSanté du système:")
    print(json.dumps(health, indent=2, ensure_ascii=False))

