from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from langchain_text_splitters import RecursiveCharacterTextSplitter

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    # Fallback pour compatibilité
    from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from .config import settings
from .llm_manager import get_llm_manager
from .ocr_pipeline import ocr_any


# ---------- Phase 1 : collecte & OCR ----------


@dataclass
class DocumentCollector:
    root_dir: Path

    def get_documents(self) -> List[Path]:
        """Retourne la liste des fichiers bruts à traiter."""
        exts = {".txt", ".md", ".pdf", ".csv", ".jpg", ".jpeg", ".png", ".tif", ".tiff"}
        return [p for p in self.root_dir.rglob("*") if p.is_file() and p.suffix.lower() in exts]


class OCREngine:
    """Moteur OCR simple avec fallback (ici Tesseract uniquement, extensible)."""

    def extract_text(self, path: Path) -> Tuple[str, float]:
        # Dans cette version, on utilise un seul moteur (Tesseract via ocr_any)
        # et on renvoie une confiance "approximative" basée sur la longueur.
        text = ocr_any(path)
        confidence = min(0.99, max(0.3, len(text) / 10_000)) if text else 0.0
        return text, confidence


# ---------- Phase 2 : post‑processing & structuration ----------


class OCRCorrector:
    """Corrections simples inspirées de ton pseudo‑code."""

    COMMON_CONFUSIONS = {
        " O ": " 0 ",
        " l ": " 1 ",
        " I ": " 1 ",
        " rn": "m",
        " cl": "d",
    }

    def enhance_ocr_output(self, raw_text: str) -> str:
        text = raw_text
        for wrong, right in self.COMMON_CONFUSIONS.items():
            text = text.replace(wrong, right)
        return text


def analyze_document_structure(text: str) -> Dict[str, Any]:
    """
    Stub léger pour la structuration :
    on segmente en 'paragraphes' par double saut de ligne.
    Cette fonction pourra être remplacée par LayoutParser / Docling plus tard.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return {
        "paragraphes": paragraphs,
        "en-tetes": [],
        "tableaux": [],
        "listes": [],
        "legendes": [],
        "ordre_lecture": list(range(len(paragraphs))),
    }


class SmartChunker:
    """Chunking intelligent basé sur RecursiveCharacterTextSplitter."""

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n## ", "\n### ", "\n", ". ", "! ", "? ", " "],
        )

    def create_chunks(self, structured_doc: Dict[str, Any], metadata: Dict[str, Any]) -> List[Any]:
        full_text = "\n\n".join(structured_doc.get("paragraphes", []))
        docs = self.splitter.create_documents([full_text], metadatas=[metadata])
        return docs


# ---------- Phase 3 : embeddings & vector store ----------


class EmbeddingGenerator:
    def __init__(self) -> None:
        self.embedding_model = HuggingFaceEmbeddings(model_name=settings.embedding_model_name)

    def generate_vectors(self, docs: Iterable[Any]) -> FAISS:
        return FAISS.from_documents(list(docs), self.embedding_model)


class VectorStoreManager:
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.embedding_model = HuggingFaceEmbeddings(model_name=settings.embedding_model_name)

    def save(self, vs: FAISS) -> None:
        vs.save_local(str(self.storage_dir))

    def load(self) -> FAISS:
        return FAISS.load_local(
            str(self.storage_dir),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )


# ---------- Phase 4 : retrieval & génération RAG ----------


class RetrievalEngine:
    def __init__(self, vector_store: FAISS) -> None:
        self.retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    def get_retriever(self):
        return self.retriever


class RAGGenerator:
    def __init__(self, retriever) -> None:
        # OPTIMISATION: Prompt plus court et concis pour réduire la latence
        system_prompt = """Expert photo. Réponds en français avec conseils concrets et réglages (ISO, ouverture, vitesse).
Contexte peut contenir des erreurs OCR. Cite les sources. Si info manquante, dis-le.

Contexte: {context}"""
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
        # Utiliser le gestionnaire LLM pour obtenir le LLM configuré (Grok, Ollama, etc.)
        llm_manager = get_llm_manager()
        llm = llm_manager.get_llm()  # Utilise le LLM par défaut (Grok si configuré)
        qa_chain = create_stuff_documents_chain(llm, prompt)
        self.rag_chain = create_retrieval_chain(retriever, qa_chain)

    def generate_answer(self, question: str) -> Dict[str, Any]:
        return self.rag_chain.invoke({"input": question})


# ---------- Phase 5 : monitoring (version légère) ----------


class OCRQualityMonitor:
    def __init__(self) -> None:
        self.metrics: List[Dict[str, Any]] = []

    def log_sample(self, confidence: float, source: str) -> None:
        self.metrics.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "confidence": confidence,
                "source": source,
            }
        )

    def get_basic_stats(self) -> Dict[str, float]:
        if not self.metrics:
            return {}
        confs = [m["confidence"] for m in self.metrics]
        return {"avg_confidence": sum(confs) / len(confs), "samples": len(confs)}


class RetrainingPipeline:
    """
    Stub pour intégrer plus tard une vraie boucle de ré‑entraînement
    (Tesseract, embeddings, etc.).
    """

    def should_retrain(self, ocr_stats: Dict[str, float]) -> bool:
        avg = ocr_stats.get("avg_confidence", 1.0)
        return avg < 0.7
