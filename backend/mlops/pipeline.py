"""
Pipeline MLOps complet pour le RAG Photographie.
Orchestration avec Prefect pour automatiser le cycle de vie du RAG.
"""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import json
import logging

from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from prefect.blocks.system import Secret
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag_pipeline import _build_vector_store_from_raw_documents, _load_or_build_vector_store
from app.pipeline_components import OCRQualityMonitor
from app.config import settings
from mlops.phoenix_integration import monitor_pipeline_execution

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mlops/pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@task(name="collect_documents", retries=2, retry_delay_seconds=60)
def collect_documents_task(data_dir: Path) -> List[Path]:
    """
    Tâche 1 : Collecte des documents à traiter.
    """
    logger.info(f"Collecte des documents depuis {data_dir}")
    from app.pipeline_components import DocumentCollector
    
    collector = DocumentCollector(root_dir=data_dir)
    documents = collector.get_documents()
    
    logger.info(f"{len(documents)} documents trouvés")
    return documents


@task(name="extract_and_ocr", retries=2, retry_delay_seconds=60)
def extract_and_ocr_task(documents: List[Path]) -> Dict[str, Any]:
    """
    Tâche 2 : Extraction de texte et OCR.
    """
    logger.info(f"Extraction OCR pour {len(documents)} documents")
    from app.pipeline_components import OCREngine
    from app.ocr_pipeline import ocr_any
    
    ocr_engine = OCREngine()
    results = {
        "processed": [],
        "failed": [],
        "total_confidence": 0.0,
        "count": 0
    }
    
    for doc_path in documents:
        try:
            raw_text, confidence = ocr_engine.extract_text(doc_path)
            if raw_text:
                results["processed"].append({
                    "path": str(doc_path),
                    "confidence": confidence,
                    "text_length": len(raw_text)
                })
                results["total_confidence"] += confidence
                results["count"] += 1
            else:
                results["failed"].append(str(doc_path))
        except Exception as e:
            logger.error(f"Erreur OCR pour {doc_path}: {e}")
            results["failed"].append(str(doc_path))
    
    if results["count"] > 0:
        results["avg_confidence"] = results["total_confidence"] / results["count"]
    else:
        results["avg_confidence"] = 0.0
    
    logger.info(f"OCR terminé: {results['count']} réussis, {len(results['failed'])} échoués")
    return results


@task(name="post_process_ocr", retries=1)
def post_process_ocr_task(ocr_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tâche 3 : Post-traitement et correction OCR.
    """
    logger.info("Post-traitement OCR")
    from app.pipeline_components import OCRCorrector
    
    corrector = OCRCorrector()
    processed_texts = []
    
    for item in ocr_results["processed"]:
        try:
            # Relire le texte pour le corriger
            from pathlib import Path
            doc_path = Path(item["path"])
            
            # Simuler la correction (en production, on stockerait le texte brut)
            # Ici on suppose que le texte est déjà extrait
            processed_texts.append({
                "path": item["path"],
                "original_confidence": item["confidence"],
                "status": "corrected"
            })
        except Exception as e:
            logger.error(f"Erreur post-traitement pour {item['path']}: {e}")
    
    return {
        "corrected": len(processed_texts),
        "items": processed_texts
    }


@task(name="chunk_documents", retries=1)
def chunk_documents_task(post_process_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tâche 4 : Découpage intelligent des documents.
    """
    logger.info("Découpage des documents")
    from app.pipeline_components import SmartChunker, analyze_document_structure
    
    chunker = SmartChunker()
    # Cette tâche sera exécutée dans _build_vector_store_from_raw_documents
    # On retourne juste les métadonnées
    
    return {
        "status": "ready_for_chunking",
        "items_count": len(post_process_results["items"])
    }


@task(name="generate_embeddings", retries=2, retry_delay_seconds=120)
def generate_embeddings_task(chunk_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tâche 5 : Génération des embeddings et création du vector store.
    """
    logger.info("Génération des embeddings")
    
    try:
        vector_store = _build_vector_store_from_raw_documents(settings.data_dir)
        
        # Compter les documents dans le vector store
        # (approximation, car FAISS ne fournit pas directement cette info)
        vector_store_path = settings.vector_store_dir / "index.faiss"
        
        return {
            "status": "success",
            "vector_store_path": str(vector_store_path),
            "vector_store_exists": vector_store_path.exists()
        }
    except Exception as e:
        logger.error(f"Erreur génération embeddings: {e}")
        raise


@task(name="validate_pipeline", retries=1)
def validate_pipeline_task(embedding_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tâche 6 : Validation du pipeline et tests.
    """
    logger.info("Validation du pipeline")
    
    validation_results = {
        "vector_store_valid": False,
        "test_questions": [],
        "all_passed": False
    }
    
    try:
        # Vérifier que le vector store existe
        vector_store_path = Path(embedding_results["vector_store_path"])
        if vector_store_path.exists():
            validation_results["vector_store_valid"] = True
            
            # Tester avec quelques questions
            from app.rag_pipeline import answer_question
            
            test_questions = [
                "Qu'est-ce que l'ISO en photographie ?",
                "Comment fonctionne l'ouverture ?"
            ]
            
            for question in test_questions:
                try:
                    result = answer_question(question, force_rebuild=False)
                    validation_results["test_questions"].append({
                        "question": question,
                        "answer_length": len(result.get("answer", "")),
                        "sources_count": result.get("num_sources", 0),
                        "status": "success" if result.get("answer") else "failed"
                    })
                except Exception as e:
                    validation_results["test_questions"].append({
                        "question": question,
                        "status": "error",
                        "error": str(e)
                    })
            
            # Toutes les questions doivent avoir réussi
            validation_results["all_passed"] = all(
                q.get("status") == "success" 
                for q in validation_results["test_questions"]
            )
        else:
            logger.error("Vector store non trouvé")
            
    except Exception as e:
        logger.error(f"Erreur validation: {e}")
        validation_results["error"] = str(e)
    
    return validation_results


@task(name="log_metrics", retries=1)
def log_metrics_task(
    ocr_results: Dict[str, Any],
    embedding_results: Dict[str, Any],
    validation_results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Tâche 7 : Enregistrement des métriques et monitoring.
    """
    logger.info("Enregistrement des métriques")
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "ocr": {
            "processed": ocr_results.get("count", 0),
            "failed": len(ocr_results.get("failed", [])),
            "avg_confidence": ocr_results.get("avg_confidence", 0.0)
        },
        "embeddings": {
            "vector_store_created": embedding_results.get("vector_store_exists", False)
        },
        "validation": {
            "vector_store_valid": validation_results.get("vector_store_valid", False),
            "test_questions_passed": sum(
                1 for q in validation_results.get("test_questions", [])
                if q.get("status") == "success"
            ),
            "all_passed": validation_results.get("all_passed", False)
        }
    }
    
    # Sauvegarder les métriques
    metrics_dir = Path("mlops/metrics")
    metrics_dir.mkdir(parents=True, exist_ok=True)
    
    metrics_file = metrics_dir / f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Métriques sauvegardées dans {metrics_file}")
    
    return metrics


@flow(name="rag_mlops_pipeline", log_prints=True)
def rag_mlops_pipeline(
    data_dir: Path = None,
    force_rebuild: bool = True
) -> Dict[str, Any]:
    """
    Pipeline MLOps complet pour le RAG Photographie.
    
    Étapes :
    1. Collecte des documents
    2. Extraction OCR
    3. Post-traitement OCR
    4. Découpage intelligent
    5. Génération d'embeddings
    6. Validation
    7. Logging des métriques
    """
    import time
    
    if data_dir is None:
        data_dir = settings.data_dir
    
    pipeline_start_time = time.time()
    
    logger.info("=" * 80)
    logger.info("DÉMARRAGE DU PIPELINE MLOPS RAG")
    logger.info("=" * 80)
    
    # Étape 1 : Collecte
    documents = collect_documents_task(data_dir)
    
    # Étape 2 : OCR
    ocr_results = extract_and_ocr_task(documents)
    
    # Étape 3 : Post-traitement
    post_process_results = post_process_ocr_task(ocr_results)
    
    # Étape 4 : Découpage
    chunk_results = chunk_documents_task(post_process_results)
    
    # Étape 5 : Embeddings
    embedding_results = generate_embeddings_task(chunk_results)
    
    # Étape 6 : Validation
    validation_results = validate_pipeline_task(embedding_results)
    
    # Étape 7 : Métriques
    metrics = log_metrics_task(ocr_results, embedding_results, validation_results)
    
    # Monitor l'exécution du pipeline avec Phoenix
    pipeline_duration = time.time() - pipeline_start_time
    documents_processed = ocr_results.get("count", 0)
    pipeline_success = validation_results.get("all_passed", False)
    
    monitor_pipeline_execution(
        pipeline_name="rag_mlops_pipeline",
        duration_seconds=pipeline_duration,
        documents_processed=documents_processed,
        success=pipeline_success,
        metadata={
            "avg_ocr_confidence": ocr_results.get("avg_confidence", 0.0),
            "vector_store_created": embedding_results.get("vector_store_exists", False)
        }
    )
    
    logger.info("=" * 80)
    logger.info("PIPELINE MLOPS TERMINÉ")
    logger.info("=" * 80)
    
    return {
        "status": "success" if validation_results.get("all_passed") else "partial",
        "metrics": metrics,
        "validation": validation_results
    }


if __name__ == "__main__":
    # Exécuter le pipeline
    result = rag_mlops_pipeline(force_rebuild=True)
    print(f"\nRésultat: {result['status']}")
    print(f"Métriques: {json.dumps(result['metrics'], indent=2)}")

