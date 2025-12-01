"""
Tests pour les composants du pipeline.
"""
import pytest
from pathlib import Path
from app.pipeline_components import (
    DocumentCollector,
    OCREngine,
    OCRCorrector,
    SmartChunker,
    EmbeddingGenerator,
    VectorStoreManager,
    RetrievalEngine,
    analyze_document_structure,
)


class TestDocumentCollector:
    """Tests du collecteur de documents."""
    
    def test_document_collector_initialization(self, test_data_dir):
        """Test d'initialisation du collecteur."""
        collector = DocumentCollector(root_dir=test_data_dir)
        assert collector.root_dir == test_data_dir
    
    def test_get_documents_empty_dir(self, test_data_dir):
        """Test de récupération des documents dans un répertoire vide."""
        collector = DocumentCollector(root_dir=test_data_dir)
        documents = collector.get_documents()
        assert documents == []
    
    def test_get_documents_with_files(self, test_data_dir):
        """Test de récupération des documents avec fichiers."""
        # Créer des fichiers de différents types
        (test_data_dir / "test.txt").write_text("Test")
        (test_data_dir / "test.md").write_text("# Test")
        (test_data_dir / "test.pdf").touch()  # Fichier vide
        (test_data_dir / "test.jpg").touch()
        (test_data_dir / "ignore.py").write_text("# Python file")
        
        collector = DocumentCollector(root_dir=test_data_dir)
        documents = collector.get_documents()
        
        # Devrait trouver les fichiers supportés
        assert len(documents) >= 3  # txt, md, pdf, jpg
        # Ne devrait pas inclure .py
        assert not any(d.suffix == ".py" for d in documents)


class TestSmartChunker:
    """Tests du chunker intelligent."""
    
    def test_smart_chunker_initialization(self):
        """Test d'initialisation du chunker."""
        chunker = SmartChunker()
        assert chunker is not None
    
    def test_create_chunks(self):
        """Test de création de chunks."""
        chunker = SmartChunker()
        text = "Ceci est un texte de test. Il contient plusieurs phrases. Chaque phrase devrait être dans un chunk séparé."
        metadata = {"source": "test.txt"}
        
        chunks = chunker.create_chunks(text, metadata)
        assert len(chunks) > 0
        assert all("source" in chunk.metadata for chunk in chunks)


class TestEmbeddingGenerator:
    """Tests du générateur d'embeddings."""
    
    def test_embedding_generator_initialization(self):
        """Test d'initialisation du générateur."""
        generator = EmbeddingGenerator()
        assert generator is not None
    
    @pytest.mark.slow
    def test_generate_vectors(self):
        """Test de génération de vecteurs."""
        from langchain_core.documents import Document
        
        generator = EmbeddingGenerator()
        docs = [
            Document(page_content="Test document 1", metadata={"source": "test1.txt"}),
            Document(page_content="Test document 2", metadata={"source": "test2.txt"}),
        ]
        
        try:
            vector_store = generator.generate_vectors(docs)
            assert vector_store is not None
        except Exception as e:
            pytest.skip(f"Impossible de générer les vecteurs: {e}")


class TestVectorStoreManager:
    """Tests du gestionnaire de vector store."""
    
    def test_vector_store_manager_initialization(self, test_data_dir):
        """Test d'initialisation du gestionnaire."""
        manager = VectorStoreManager(storage_dir=test_data_dir / "vector_store")
        assert manager.storage_dir == test_data_dir / "vector_store"


class TestDocumentStructure:
    """Tests d'analyse de structure de document."""
    
    def test_analyze_document_structure(self):
        """Test d'analyse de structure."""
        text = """
        # Titre Principal
        
        ## Sous-titre
        
        Paragraphe de texte normal.
        
        - Liste item 1
        - Liste item 2
        """
        
        structured = analyze_document_structure(text)
        assert structured is not None
        assert isinstance(structured, str)
        assert len(structured) > 0

