from pathlib import Path
from typing import List, Optional
import time
import threading

from langchain_community.vectorstores import FAISS

from .config import settings
from .pipeline_components import (
    DocumentCollector,
    EmbeddingGenerator,
    OCRCorrector,
    OCREngine,
    OCRQualityMonitor,
    RAGGenerator,
    RetrievalEngine,
    SmartChunker,
    VectorStoreManager,
    analyze_document_structure,
)
from .monitoring_phoenix import get_phoenix_monitor
from .cache import get_cache_manager
from .llm_manager import get_llm_manager
import hashlib
import logging

logger = logging.getLogger(__name__)

# Cache global du vector store en mémoire pour améliorer les performances
_vector_store_cache: Optional[FAISS] = None
_vector_store_lock = threading.Lock()
_vector_store_loading = False


def _build_vector_store_from_raw_documents(data_dir: Path) -> FAISS:
    """
    Implémente ton pipeline MLOps OCR -> correction -> structuration -> chunking -> embeddings.
    """
    collector = DocumentCollector(root_dir=data_dir)
    ocr_engine = OCREngine()
    corrector = OCRCorrector()
    chunker = SmartChunker()
    embedder = EmbeddingGenerator()
    monitor = OCRQualityMonitor()

    docs = []

    for path in collector.get_documents():
        suffix = path.suffix.lower()
        base_metadata = {
            "source_document": path.name,
            "path": str(path),
            "date_extraction": None,
            "section_type": "texte",
        }

        if suffix in {".txt", ".md"}:
            raw_text = path.read_text(encoding="utf-8", errors="ignore")
            confidence = 1.0
        else:
            raw_text, confidence = ocr_engine.extract_text(path)
        if not raw_text:
            continue

        monitor.log_sample(confidence=confidence, source=path.name)
        cleaned_text = corrector.enhance_ocr_output(raw_text)
        structured = analyze_document_structure(cleaned_text)

        metadata = {
            **base_metadata,
            "confidence_ocr": confidence,
            "date_extraction": monitor.metrics[-1]["timestamp"],
        }

        docs.extend(chunker.create_chunks(structured, metadata))

    if not docs:
        raise RuntimeError("Aucun document exploitable n'a été trouvé pour construire le vector store.")

    vector_store = embedder.generate_vectors(docs)

    vs_manager = VectorStoreManager(storage_dir=settings.vector_store_dir)
    vs_manager.save(vector_store)

    return vector_store


def _load_or_build_vector_store(force_rebuild: bool = False) -> FAISS:
    """
    Charge ou construit le vector store avec cache en mémoire pour améliorer les performances.
    Le vector store est mis en cache en mémoire après le premier chargement.
    """
    global _vector_store_cache, _vector_store_loading

    # Si on force la reconstruction, vider le cache
    if force_rebuild:
        with _vector_store_lock:
            _vector_store_cache = None

    # Si le cache existe, le retourner immédiatement (OPTIMISATION MAJEURE)
    if _vector_store_cache is not None:
        logger.debug("✅ Utilisation du vector store en cache (beaucoup plus rapide)")
        return _vector_store_cache

    # Éviter les chargements multiples simultanés
    with _vector_store_lock:
        # Vérifier à nouveau après avoir acquis le lock
        if _vector_store_cache is not None:
            return _vector_store_cache

        if _vector_store_loading:
            # Attendre que le chargement se termine
            while _vector_store_loading:
                time.sleep(0.1)
            return _vector_store_cache

        _vector_store_loading = True

    try:
        logger.info("📦 Chargement du vector store depuis le disque...")
        start_time = time.time()

        vs_manager = VectorStoreManager(storage_dir=settings.vector_store_dir)
        if not force_rebuild and settings.vector_store_dir.exists():
            try:
                _vector_store_cache = vs_manager.load()
                load_duration = time.time() - start_time
                logger.info(f"✅ Vector store chargé en {load_duration:.2f}s (mis en cache)")
            except Exception as e:
                logger.warning(f"Erreur lors du chargement, reconstruction: {e}")
                _vector_store_cache = _build_vector_store_from_raw_documents(settings.data_dir)
                build_duration = time.time() - start_time
                logger.info(f"✅ Vector store reconstruit en {build_duration:.2f}s (mis en cache)")
        else:
            # Force la reconstruction
            if force_rebuild and settings.vector_store_dir.exists():
                import shutil

                shutil.rmtree(settings.vector_store_dir)
            _vector_store_cache = _build_vector_store_from_raw_documents(settings.data_dir)
            build_duration = time.time() - start_time
            logger.info(f"✅ Vector store reconstruit en {build_duration:.2f}s (mis en cache)")

        return _vector_store_cache
    finally:
        _vector_store_loading = False


def clear_vector_store_cache():
    """Vide le cache du vector store. Utile pour forcer un rechargement."""
    global _vector_store_cache
    with _vector_store_lock:
        _vector_store_cache = None
    logger.info("🗑️ Cache du vector store vidé")


def answer_question(
    question: str, show_sources: bool = True, force_rebuild: bool = False, num_docs: Optional[int] = None
) -> dict:
    """
    Fonction utilitaire de haut niveau alignée sur ton schéma MLOps :
    - collecte + OCR + correction + structuration + chunking
    - embeddings + vector store
    - retrieval + génération RAG LangChain.

    Args:
        question: La question à poser
        show_sources: Afficher les sources
        force_rebuild: Forcer la reconstruction du vector store
        num_docs: Nombre de documents à récupérer (None = utiliser la valeur de la config, défaut optimisé: 3)

    Returns:
        dict avec 'answer' (réponse) et 'sources' (documents utilisés)
    """
    # Utiliser la valeur de la config si non spécifiée
    if num_docs is None:
        num_docs = settings.num_retrieval_docs

    # Vérifier le cache si pas de force_rebuild
    cache = get_cache_manager()
    if not force_rebuild and cache.enabled:
        cache_key = f"rag:answer:{hashlib.md5(question.encode()).hexdigest()}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug(f"Cache hit pour question: {question[:50]}...")
            return cached_result

    # Récupérer le monitor Phoenix
    monitor = get_phoenix_monitor()

    start_time = time.time()

    # OPTIMISATION: Timing détaillé pour identifier les goulots d'étranglement
    vs_start = time.time()
    vector_store = _load_or_build_vector_store(force_rebuild=force_rebuild)
    vs_duration = (time.time() - vs_start) * 1000
    logger.debug(f"📦 Vector store chargé en {vs_duration:.2f}ms")
    
    retriever_engine = RetrievalEngine(vector_store)

    # Récupérer les documents pertinents AVANT de générer la réponse
    retriever = retriever_engine.get_retriever()
    # OPTIMISATION: Réduire le nombre de documents récupérés pour plus de rapidité (2 au lieu de 3)
    if hasattr(retriever, "search_kwargs"):
        retriever.search_kwargs["k"] = num_docs
    else:
        retriever = vector_store.as_retriever(search_kwargs={"k": num_docs})

    retrieval_start = time.time()
    retrieved_docs = retriever.invoke(question)
    retrieval_duration = (time.time() - retrieval_start) * 1000  # ms

    # Monitor retrieval
    if monitor and monitor.enabled:
        sources_preview = []
        for doc in retrieved_docs[:5]:
            sources_preview.append(
                {"document": doc.metadata.get("source_document", "Inconnu"), "preview": doc.page_content[:100]}
            )
        monitor.trace_retrieval(question, sources_preview)

    # Générer la réponse avec le RAG
    rag_generator = RAGGenerator(retriever)
    generation_start = time.time()
    result = rag_generator.generate_answer(question)
    generation_duration = (time.time() - generation_start) * 1000  # ms

    # Extraire les sources réelles utilisées
    sources = []
    for doc in retrieved_docs:
        source_info = {
            "document": doc.metadata.get("source_document", "Inconnu"),
            "path": doc.metadata.get("path", ""),
            "page": doc.metadata.get("page", ""),
            "preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
        }
        sources.append(source_info)

    answer = result.get("answer", "")
    total_duration = (time.time() - start_time) * 1000  # ms

    # OPTIMISATION: Logging détaillé avec timing complet
    logger.info(
        f"⚡ RAG réponse générée en {total_duration:.2f}ms "
        f"(vector_store: {vs_duration:.2f}ms, retrieval: {retrieval_duration:.2f}ms, "
        f"generation: {generation_duration:.2f}ms)"
    )

    # Monitor génération et pipeline complet
    if monitor and monitor.enabled:
        monitor.trace_generation(question, answer, model=settings.llm_model_name, duration_ms=generation_duration)

        monitor.trace_rag_pipeline(
            query=question,
            response=answer,
            documents_used=sources,
            metadata={
                "retrieval_duration_ms": retrieval_duration,
                "generation_duration_ms": generation_duration,
                "total_duration_ms": total_duration,
                "num_sources": len(sources),
            },
        )

    result = {
        "answer": answer,
        "sources": sources,
        "num_sources": len(sources),
    }

    # Mettre en cache le résultat
    cache = get_cache_manager()  # Récupérer le cache manager
    if cache.enabled and not force_rebuild:
        cache_key = f"rag:answer:{hashlib.md5(question.encode()).hexdigest()}"
        cache.set(cache_key, result, ttl=3600)  # Cache 1h
        logger.debug(f"Résultat mis en cache: {cache_key}")

    return result


def answer_question_stream(
    question: str, force_rebuild: bool = False, num_docs: Optional[int] = None, streaming_delay: Optional[float] = None
):
    """
    Version streaming optimisée de answer_question qui génère la réponse token par token.
    Yields chaque token au fur et à mesure pour permettre à l'utilisateur de suivre le raisonnement.

    Args:
        question: La question à poser
        force_rebuild: Forcer la reconstruction du vector store
        num_docs: Nombre de documents à récupérer (None = utiliser la valeur de la config, défaut optimisé: 2)
        streaming_delay: Délai entre les tokens (None = utiliser la valeur optimisée)
    """
    start_time = time.time()  # OPTIMISATION: Timing pour le streaming
    from langchain_core.prompts import ChatPromptTemplate

    # Utiliser la valeur de la config si non spécifiée
    if num_docs is None:
        num_docs = settings.num_retrieval_docs

    # OPTIMISATION: Utiliser un délai de streaming réduit (0ms pour plus de rapidité)
    if streaming_delay is None:
        streaming_delay = 0.0  # OPTIMISATION: Pas de délai pour plus de rapidité

    vs_start = time.time()
    vector_store = _load_or_build_vector_store(force_rebuild=force_rebuild)
    vs_duration = (time.time() - vs_start) * 1000
    logger.debug(f"📦 Vector store chargé en {vs_duration:.2f}ms")
    
    retriever_engine = RetrievalEngine(vector_store)

    # Récupérer les documents pertinents AVANT de générer la réponse
    retriever = retriever_engine.get_retriever()
    # OPTIMISATION: Réduire le nombre de documents pour plus de rapidité (2 par défaut)
    if hasattr(retriever, "search_kwargs"):
        retriever.search_kwargs["k"] = num_docs
    else:
        retriever = vector_store.as_retriever(search_kwargs={"k": num_docs})

    retrieval_start = time.time()
    retrieved_docs = retriever.invoke(question)
    retrieval_duration = (time.time() - retrieval_start) * 1000
    logger.debug(f"🔍 Recherche vectorielle en {retrieval_duration:.2f}ms")

    # Préparer les sources
    sources = []
    for doc in retrieved_docs:
        source_info = {
            "document": doc.metadata.get("source_document", "Inconnu"),
            "path": doc.metadata.get("path", ""),
            "page": doc.metadata.get("page", ""),
            "preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
        }
        sources.append(source_info)

    # OPTIMISATION: Tronquer intelligemment le contexte pour réduire la latence
    max_context_chars = getattr(settings, 'max_context_length', 1500)
    context_parts = []
    current_length = 0
    for doc in retrieved_docs:
        content = doc.page_content[:500]  # Limiter chaque doc à 500 caractères
        if current_length + len(content) <= max_context_chars:
            context_parts.append(content)
            current_length += len(content)
        else:
            # Ajouter le reste jusqu'à la limite
            remaining = max_context_chars - current_length
            if remaining > 100:  # Ne pas ajouter de trop petits fragments
                context_parts.append(content[:remaining])
            break
    context = "\n\n".join(context_parts)

    # OPTIMISATION: Prompt plus court et concis
    system_prompt = """Expert photo. Réponds en français avec conseils concrets et réglages (ISO, ouverture, vitesse).
Contexte peut contenir des erreurs OCR. Cite les sources. Si info manquante, dis-le.

Contexte: {context}"""
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])

    # Formater le prompt avec le contexte et la question
    formatted_prompt = prompt.format_messages(context=context, input=question)

    # OPTIMISATION: Utiliser le gestionnaire LLM pour obtenir le LLM configuré (Grok, Ollama, etc.)
    llm_manager = get_llm_manager()
    llm = llm_manager.get_llm()  # Utilise le LLM par défaut (Grok si configuré)

    full_answer = ""

    try:
        # Streamer directement depuis le LLM pour avoir les tokens un par un
        # Le streaming retourne des chunks (peut contenir un ou plusieurs tokens)
        for chunk in llm.stream(formatted_prompt):
            # Extraire le contenu du chunk
            token = None

            if hasattr(chunk, "content"):
                # AIMessageChunk ou similaire
                token = chunk.content
            elif hasattr(chunk, "text"):
                # Chunk avec attribut text
                token = chunk.text
            elif isinstance(chunk, str):
                # Chunk est directement une string
                token = chunk
            elif isinstance(chunk, dict):
                # Chunk est un dictionnaire
                token = chunk.get("content", chunk.get("text", chunk.get("token", "")))
            else:
                # Essayer de convertir en string
                token = str(chunk) if chunk else ""

            if token:
                full_answer += token
                yield token
                # OPTIMISATION: Délai réduit pour plus de rapidité et fluidité
                if streaming_delay > 0:
                    time.sleep(streaming_delay)

    except Exception as e:
        # Si le streaming échoue, générer la réponse normalement et la streamer caractère par caractère
        print(f"Streaming direct échoué, utilisation du fallback: {e}")
        import traceback

        traceback.print_exc()
        try:
            # Fallback : générer la réponse complète puis la streamer
            rag_generator = RAGGenerator(retriever)
            result = rag_generator.generate_answer(question)
            full_answer = result.get("answer", "")

            # Streamer caractère par caractère pour simuler le streaming
            for char in full_answer:
                yield char
                if streaming_delay > 0:
                    time.sleep(streaming_delay)
        except Exception as e2:
            raise RuntimeError(f"Erreur lors de la génération: {str(e2)}") from e2

    # OPTIMISATION: Logging du temps total de streaming
    total_duration = (time.time() - start_time) * 1000
    logger.info(
        f"⚡ Streaming RAG terminé en {total_duration:.2f}ms "
        f"(vector_store: {vs_duration:.2f}ms, retrieval: {retrieval_duration:.2f}ms)"
    )
    
    # Retourner les sources à la fin
    yield {"sources": sources, "full_answer": full_answer}
