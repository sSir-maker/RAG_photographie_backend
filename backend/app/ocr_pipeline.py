from pathlib import Path
from typing import List
import io

import pdfplumber
import pytesseract
from PIL import Image

# Utilisation des loaders LangChain pour les PDFs (plus robuste)
try:
    from langchain_community.document_loaders import PyPDFLoader, PyPDFium2Loader

    LANGCHAIN_PDF_AVAILABLE = True
except ImportError:
    LANGCHAIN_PDF_AVAILABLE = False

# Fallback : PyMuPDF (optionnel, nécessite compilation)
try:
    import fitz  # PyMuPDF

    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extraction de texte depuis un PDF avec support des images intégrées.
    Utilise les loaders LangChain natifs qui gèrent automatiquement l'OCR sur les images.
    """
    texts: List[str] = []

    # Stratégie 1 : Utiliser les loaders LangChain (recommandé)
    # Ils gèrent automatiquement l'extraction d'images avec Tesseract
    if LANGCHAIN_PDF_AVAILABLE:
        try:
            # Essayer d'abord PyPDFium2Loader (plus moderne)
            try:
                loader = PyPDFium2Loader(str(pdf_path))
                docs = loader.load()
                if docs:
                    # Combiner tous les documents
                    combined_text = "\n\n".join([doc.page_content for doc in docs])
                    if combined_text.strip():
                        return combined_text
            except Exception:
                # Fallback sur PyPDFLoader
                pass

            # Essayer PyPDFLoader avec Tesseract pour les images
            try:
                loader = PyPDFLoader(str(pdf_path))
                docs = loader.load()
                if docs:
                    combined_text = "\n\n".join([doc.page_content for doc in docs])
                    if combined_text.strip():
                        return combined_text
            except Exception:
                pass
        except Exception:
            # Si les loaders LangChain échouent, on continue avec pdfplumber
            pass

    # Stratégie 2 : Extraction simple avec pdfplumber (fallback)
    page_texts: List[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_text = (page.extract_text() or "").strip()
            page_texts.append(page_text)
            if page_text:
                texts.append(f"[Page {page_num + 1} - Texte]\n{page_text}")

    # Stratégie 3 : Si pas de texte, faire OCR sur la page entière
    if not texts and not any(page_texts):
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    pil_image = page.to_image(resolution=300).original.convert("RGB")
                    ocr_text = pytesseract.image_to_string(pil_image, lang="fra+eng").strip()
                    if ocr_text:
                        texts.append(f"[Page {page_num + 1} - OCR Page]\n{ocr_text}")
                except Exception:
                    continue

    return "\n\n".join(texts) if texts else "\n\n".join(page_texts)


def extract_text_from_image(image_path: Path) -> str:
    """Extraction OCR depuis une image (JPG, PNG, etc.)."""
    image = Image.open(image_path).convert("RGB")
    text = pytesseract.image_to_string(image, lang="fra+eng")
    return text.strip()


def ocr_any(path: Path) -> str:
    """Raccourci pour lancer l'OCR / extraction texte sur différents formats."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    if suffix in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}:
        return extract_text_from_image(path)
    if suffix == ".csv":
        # Pour les CSV, on considère que le contenu est déjà du texte structuré.
        # On le renvoie brut, à charge pour la couche supérieure de gérer les tableaux si besoin.
        return path.read_text(encoding="utf-8", errors="ignore")
    raise ValueError(f"Format non supporté pour l'OCR: {suffix}")
