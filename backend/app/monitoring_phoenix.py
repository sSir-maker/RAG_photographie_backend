"""
Monitoring et observabilité avec Arize Phoenix pour le RAG.
Instrumentation automatique et manuelle des appels LLM/RAG.
"""

import os
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

# Import Phoenix avec gestion d'erreur si non installé
try:
    import phoenix as px
    from phoenix.otel import register
    from openinference.instrumentation.langchain import LangChainInstrumentor

    # Utiliser les constantes depuis phoenix.trace.otel
    from phoenix.trace.otel import (
        INPUT_VALUE,
        OUTPUT_VALUE,
    )
    from opentelemetry import trace as otel_trace

    PHOENIX_AVAILABLE = True
except ImportError as e:
    PHOENIX_AVAILABLE = False
    logger.warning(f"Phoenix non installé. Le monitoring sera désactivé. Erreur: {e}")


class PhoenixMonitor:
    """Gestionnaire de monitoring Phoenix pour le RAG."""

    def __init__(self, endpoint: Optional[str] = None):
        """
        Initialise le monitor Phoenix.

        Args:
            endpoint: URL du serveur Phoenix (optionnel, par défaut localhost:6006)
        """
        if not PHOENIX_AVAILABLE:
            self.enabled = False
            logger.warning("Phoenix non disponible. Monitoring désactivé.")
            return

        self.enabled = True
        self.endpoint = endpoint or os.getenv("PHOENIX_ENDPOINT", "http://localhost:6006")
        self.session = None
        self.tracer_provider = None
        self.instrumentor = None

        try:
            # Enregistrer Phoenix avec OpenTelemetry
            self.tracer_provider = register()

            # Créer l'instrumentor LangChain
            self.instrumentor = LangChainInstrumentor()

            logger.info(f"Phoenix Monitor initialisé (endpoint: {self.endpoint})")
        except Exception as e:
            logger.error(f"Erreur initialisation Phoenix: {e}")
            self.enabled = False

    def setup_instrumentation(self):
        """Configure l'instrumentation automatique de LangChain."""
        if not self.enabled or not self.instrumentor or not self.tracer_provider:
            return

        try:
            self.instrumentor.instrument(tracer_provider=self.tracer_provider)
            logger.info("Instrumentation LangChain activée")
        except Exception as e:
            logger.error(f"Erreur instrumentation: {e}")

    def trace_rag_pipeline(
        self,
        query: str,
        response: str,
        documents_used: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Trace manuel pour le pipeline RAG custom.

        Args:
            query: Question de l'utilisateur
            response: Réponse générée
            documents_used: Liste des documents utilisés
            metadata: Métadonnées supplémentaires
        """
        if not self.enabled or not self.tracer:
            return

        try:
            tracer = otel_trace.get_tracer(__name__)
            with tracer.start_as_current_span("rag_pipeline") as span:
                # Attributs de base
                span.set_attribute(INPUT_VALUE, query)
                span.set_attribute(OUTPUT_VALUE, response[:500])  # Truncate

                # Métadonnées
                if metadata:
                    for key, value in metadata.items():
                        span.set_attribute(f"metadata.{key}", str(value))

                # Documents utilisés
                if documents_used:
                    span.set_attribute("retrieval.documents_count", len(documents_used))
                    span.set_attribute(
                        "retrieval.documents", [doc.get("document", "Unknown") for doc in documents_used[:5]]
                    )

                logger.debug(f"Trace Phoenix créé pour query: {query[:50]}...")
        except Exception as e:
            logger.error(f"Erreur tracing Phoenix: {e}")

    def trace_retrieval(self, query: str, documents: List[Dict[str, Any]], scores: Optional[List[float]] = None):
        """
        Trace spécifique pour la phase de retrieval.

        Args:
            query: Question
            documents: Documents récupérés
            scores: Scores de similarité (optionnel)
        """
        if not self.enabled or not self.tracer:
            return

        try:
            tracer = otel_trace.get_tracer(__name__)
            with tracer.start_as_current_span("retrieval") as span:
                span.set_attribute(INPUT_VALUE, query)
                span.set_attribute("retrieval.count", len(documents))

                if scores:
                    avg_score = sum(scores) / len(scores) if scores else 0.0
                    span.set_attribute("retrieval.avg_score", avg_score)
                    span.set_attribute("retrieval.min_score", min(scores))
                    span.set_attribute("retrieval.max_score", max(scores))
        except Exception as e:
            logger.error(f"Erreur tracing retrieval: {e}")

    def trace_generation(
        self,
        query: str,
        response: str,
        model: str,
        tokens_used: Optional[int] = None,
        duration_ms: Optional[float] = None,
    ):
        """
        Trace spécifique pour la phase de génération.

        Args:
            query: Question
            response: Réponse générée
            model: Nom du modèle LLM
            tokens_used: Nombre de tokens utilisés
            duration_ms: Durée en millisecondes
        """
        if not self.enabled or not self.tracer:
            return

        try:
            tracer = otel_trace.get_tracer(__name__)
            with tracer.start_as_current_span("generation") as span:
                span.set_attribute(INPUT_VALUE, query)
                span.set_attribute(OUTPUT_VALUE, response[:500])
                span.set_attribute("llm.model_name", model)

                if tokens_used:
                    span.set_attribute("llm.tokens_used", tokens_used)

                if duration_ms:
                    span.set_attribute("performance.duration_ms", duration_ms)
        except Exception as e:
            logger.error(f"Erreur tracing generation: {e}")

    def launch_dashboard(self, port: int = 6006):
        """
        Lance le dashboard Phoenix (optionnel, pour développement).

        Args:
            port: Port du dashboard
        """
        if not self.enabled:
            logger.warning("Phoenix non disponible. Dashboard non lancé.")
            return

        try:
            # Phoenix 12+ utilise launch_app différemment
            self.session = px.launch_app(port=port)
            logger.info(f"Dashboard Phoenix lancé sur http://localhost:{port}")
            return self.session
        except Exception as e:
            logger.error(f"Erreur lancement dashboard: {e}")
            logger.info("Pour démarrer Phoenix manuellement: python -m phoenix.server.main --port 6006")
            return None


# Instance globale du monitor
_global_monitor: Optional[PhoenixMonitor] = None


def get_phoenix_monitor() -> PhoenixMonitor:
    """Récupère l'instance globale du monitor Phoenix."""
    global _global_monitor

    if _global_monitor is None:
        _global_monitor = PhoenixMonitor()
        _global_monitor.setup_instrumentation()

    return _global_monitor


def initialize_phoenix(endpoint: Optional[str] = None) -> PhoenixMonitor:
    """
    Initialise le monitor Phoenix globalement.

    Args:
        endpoint: URL du serveur Phoenix

    Returns:
        Instance du monitor
    """
    global _global_monitor

    _global_monitor = PhoenixMonitor(endpoint=endpoint)
    _global_monitor.setup_instrumentation()

    return _global_monitor
