from pathlib import Path
from typing import List
import time

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
import hashlib
import logging

logger = logging.getLogger(__name__)


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
    vs_manager = VectorStoreManager(storage_dir=settings.vector_store_dir)
    if not force_rebuild and settings.vector_store_dir.exists():
        try:
            return vs_manager.load()
        except Exception:
            # Si le chargement échoue, on reconstruit
            return _build_vector_store_from_raw_documents(settings.data_dir)
    # Force la reconstruction
    if force_rebuild and settings.vector_store_dir.exists():
        import shutil
        shutil.rmtree(settings.vector_store_dir)
    return _build_vector_store_from_raw_documents(settings.data_dir)


def answer_question(question: str, show_sources: bool = True, force_rebuild: bool = False) -> dict:
    """
    Fonction utilitaire de haut niveau alignée sur ton schéma MLOps :
    - collecte + OCR + correction + structuration + chunking
    - embeddings + vector store
    - retrieval + génération RAG LangChain.
    
    Returns:
        dict avec 'answer' (réponse) et 'sources' (documents utilisés)
    """
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
    
    vector_store = _load_or_build_vector_store(force_rebuild=force_rebuild)
    retriever_engine = RetrievalEngine(vector_store)
    
    # Récupérer les documents pertinents AVANT de générer la réponse
    retriever = retriever_engine.get_retriever()
    retrieval_start = time.time()
    retrieved_docs = retriever.invoke(question)
    retrieval_duration = (time.time() - retrieval_start) * 1000  # ms
    
    # Monitor retrieval
    if monitor and monitor.enabled:
        sources_preview = []
        for doc in retrieved_docs[:5]:
            sources_preview.append({
                "document": doc.metadata.get("source_document", "Inconnu"),
                "preview": doc.page_content[:100]
            })
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
    
    # Monitor génération et pipeline complet
    if monitor and monitor.enabled:
        monitor.trace_generation(
            question,
            answer,
            model=settings.llm_model_name,
            duration_ms=generation_duration
        )
        
        monitor.trace_rag_pipeline(
            query=question,
            response=answer,
            documents_used=sources,
            metadata={
                "retrieval_duration_ms": retrieval_duration,
                "generation_duration_ms": generation_duration,
                "total_duration_ms": total_duration,
                "num_sources": len(sources)
            }
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


def answer_question_stream(question: str, force_rebuild: bool = False):
    """
    Version streaming de answer_question qui génère la réponse token par token.
    Yields chaque token au fur et à mesure pour permettre à l'utilisateur de suivre le raisonnement.
    """
    try:
        from langchain_community.chat_models import ChatOllama
        use_chat_ollama = True
    except ImportError:
        from langchain_community.llms import Ollama
        use_chat_ollama = False
    from langchain_core.prompts import ChatPromptTemplate
    
    vector_store = _load_or_build_vector_store(force_rebuild=force_rebuild)
    retriever_engine = RetrievalEngine(vector_store)
    
    # Récupérer les documents pertinents AVANT de générer la réponse
    retriever = retriever_engine.get_retriever()
    retrieved_docs = retriever.invoke(question)
    
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
    
    # Construire le contexte à partir des documents récupérés
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Créer le prompt avec le contexte
    system_prompt = """
Tu es un expert en photographie (prise de vue, lumière, composition, matériel, post‑traitement).
Tu dois répondre **en français**, avec des explications claires et des conseils concrets :
- propose des réglages (ISO, ouverture, vitesse, focale) adaptés à la situation
- prends en compte que le contexte provient d'un OCR et peut contenir de petites erreurs
- cite les sources (fichier, numéro de page si disponible)
- si l'information n'est pas dans le contexte, dis‑le honnêtement.

Contexte :
{context}
"""
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", "{input}")]
    )
    
    # Formater le prompt avec le contexte et la question
    formatted_prompt = prompt.format_messages(context=context, input=question)
    
    # Créer le LLM pour le streaming
    if use_chat_ollama:
        llm = ChatOllama(model=settings.llm_model_name, temperature=0.7)
    else:
        llm = Ollama(model=settings.llm_model_name, temperature=0.7)
    
    full_answer = ""
    
    try:
        # Streamer directement depuis le LLM pour avoir les tokens un par un
        # Le streaming retourne des chunks (peut contenir un ou plusieurs tokens)
        for chunk in llm.stream(formatted_prompt):
            # Extraire le contenu du chunk
            token = None
            
            if hasattr(chunk, 'content'):
                # AIMessageChunk ou similaire
                token = chunk.content
            elif hasattr(chunk, 'text'):
                # Chunk avec attribut text
                token = chunk.text
            elif isinstance(chunk, str):
                # Chunk est directement une string
                token = chunk
            elif isinstance(chunk, dict):
                # Chunk est un dictionnaire
                token = chunk.get('content', chunk.get('text', chunk.get('token', '')))
            else:
                # Essayer de convertir en string
                token = str(chunk) if chunk else ""
            
            if token:
                full_answer += token
                # Yielder chaque token/chunk pour un streaming fluide
                # Si le chunk contient plusieurs tokens, on les envoie quand même
                # car Ollama peut retourner plusieurs tokens à la fois
                yield token
                # Ajouter un petit délai pour ralentir le streaming et permettre
                # à l'utilisateur de mieux suivre le raisonnement
                import time
                time.sleep(settings.streaming_delay)  # Délai configurable
                
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
            import time
            for char in full_answer:
                yield char
                time.sleep(0.05)  # 50ms entre les caractères pour ralentir le streaming
        except Exception as e2:
            raise RuntimeError(f"Erreur lors de la génération: {str(e2)}") from e2
    
    # Retourner les sources à la fin
    yield {"sources": sources, "full_answer": full_answer}



