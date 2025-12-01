"""
Intégration Phoenix dans le pipeline MLOps Prefect.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Import Phoenix avec gestion d'erreur
try:
    from phoenix.otel import register
    from phoenix.trace.otel import INPUT_VALUE, OUTPUT_VALUE
    from opentelemetry import trace as otel_trace
    PHOENIX_AVAILABLE = True
except ImportError as e:
    PHOENIX_AVAILABLE = False
    logger.warning(f"Phoenix non installé. Monitoring MLOps désactivé. Erreur: {e}")


def get_phoenix_tracer():
    """Récupère un tracer Phoenix pour Prefect."""
    if not PHOENIX_AVAILABLE:
        return None
    
    try:
        register()  # Enregistrer Phoenix
        return otel_trace.get_tracer(__name__)
    except Exception as e:
        logger.error(f"Erreur création tracer Phoenix: {e}")
        return None


def monitor_rag_quality(
    query: str,
    response: str,
    documents_used: list,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Monitor la qualité d'une requête RAG dans Prefect.
    
    Args:
        query: Question posée
        response: Réponse générée
        documents_used: Documents utilisés
        metadata: Métadonnées supplémentaires
        
    Returns:
        Métriques de qualité
    """
    tracer = get_phoenix_tracer()
    
    if not tracer:
        return {"monitoring": "disabled"}
    
    try:
        with tracer.start_as_current_span("prefect_rag_task") as span:
            # Attributs de base
            span.set_attribute(INPUT_VALUE, query)
            span.set_attribute(OUTPUT_VALUE, response[:500])
            
            # Métriques retrieval
            span.set_attribute("retrieval.documents_count", len(documents_used))
            span.set_attribute("retrieval.documents", [
                doc.get("document", "Unknown") for doc in documents_used[:5]
            ])
            
            # Métadonnées
            if metadata:
                for key, value in metadata.items():
                    span.set_attribute(f"metadata.{key}", str(value))
            
            # Métriques calculées
            metrics = {
                "query_length": len(query),
                "response_length": len(response),
                "documents_count": len(documents_used),
                "timestamp": datetime.now().isoformat(),
                "monitoring": "enabled"
            }
            
            return metrics
            
    except Exception as e:
        logger.error(f"Erreur monitoring RAG quality: {e}")
        return {"monitoring": "error", "error": str(e)}


def monitor_pipeline_execution(
    pipeline_name: str,
    duration_seconds: float,
    documents_processed: int,
    success: bool,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Monitor l'exécution d'un pipeline MLOps.
    
    Args:
        pipeline_name: Nom du pipeline
        duration_seconds: Durée d'exécution
        documents_processed: Nombre de documents traités
        success: Succès ou échec
        metadata: Métadonnées supplémentaires
    """
    tracer = get_phoenix_tracer()
    
    if not tracer:
        return
    
    try:
        with tracer.start_as_current_span("mlops_pipeline") as span:
            span.set_attribute("pipeline.name", pipeline_name)
            span.set_attribute("pipeline.duration_seconds", duration_seconds)
            span.set_attribute("pipeline.documents_processed", documents_processed)
            span.set_attribute("pipeline.success", success)
            
            if metadata:
                for key, value in metadata.items():
                    span.set_attribute(f"pipeline.{key}", str(value))
                    
    except Exception as e:
        logger.error(f"Erreur monitoring pipeline: {e}")

