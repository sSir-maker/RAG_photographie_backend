"""
Tests pour le pipeline OCR.
"""

import pytest
from pathlib import Path
from app.ocr_pipeline import ocr_any, extract_text_from_image
from app.pipeline_components import OCREngine, OCRCorrector


class TestOCREngine:
    """Tests du moteur OCR."""

    def test_ocr_engine_initialization(self):
        """Test d'initialisation du moteur OCR."""
        engine = OCREngine()
        assert engine is not None

    def test_extract_text_from_text_file(self, sample_text_file):
        """Test d'extraction de texte depuis un fichier texte."""
        engine = OCREngine()
        text, confidence = engine.extract_text(sample_text_file)
        assert text is not None
        assert len(text) > 0
        assert confidence == 1.0  # Fichier texte = confiance maximale

    @pytest.mark.slow
    def test_extract_text_from_pdf(self, sample_pdf_file):
        """Test d'extraction de texte depuis un PDF."""
        if sample_pdf_file is None:
            pytest.skip("Aucun PDF de test disponible")

        engine = OCREngine()
        text, confidence = engine.extract_text(sample_pdf_file)
        # Le texte peut être vide si le PDF est une image scannée
        # On vérifie juste que la fonction ne plante pas
        assert isinstance(text, str)
        assert 0.0 <= confidence <= 1.0


class TestOCRCorrector:
    """Tests du correcteur OCR."""

    def test_ocr_corrector_initialization(self):
        """Test d'initialisation du correcteur."""
        corrector = OCRCorrector()
        assert corrector is not None

    def test_enhance_ocr_output(self):
        """Test d'amélioration du texte OCR."""
        corrector = OCRCorrector()

        # Texte avec erreurs OCR typiques
        dirty_text = "  Ceci   est   un   test  \n\n  avec   des   espaces  .  "
        cleaned = corrector.enhance_ocr_output(dirty_text)

        assert cleaned is not None
        assert len(cleaned) > 0
        # Le texte devrait être nettoyé (espaces multiples réduits)
        assert "   " not in cleaned or cleaned.count("   ") < dirty_text.count("   ")


class TestOCRAny:
    """Tests de la fonction ocr_any."""

    def test_ocr_any_text_file(self, sample_text_file):
        """Test d'ocr_any avec un fichier texte."""
        result = ocr_any(sample_text_file)
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.slow
    def test_ocr_any_pdf_file(self, sample_pdf_file):
        """Test d'ocr_any avec un fichier PDF."""
        if sample_pdf_file is None:
            pytest.skip("Aucun PDF de test disponible")

        result = ocr_any(sample_pdf_file)
        # Le résultat peut être vide pour un PDF scanné
        assert isinstance(result, str)

    def test_ocr_any_invalid_file(self, test_data_dir):
        """Test d'ocr_any avec un fichier invalide."""
        invalid_file = test_data_dir / "invalid.xyz"
        invalid_file.write_text("test")

        # ocr_any devrait gérer les extensions non supportées
        result = ocr_any(invalid_file)
        # Le comportement dépend de l'implémentation
        assert isinstance(result, str)
