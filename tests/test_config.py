"""
Tests pour la configuration.
"""
import pytest
import os
from pathlib import Path
from app.config import settings, BASE_DIR


class TestSettings:
    """Tests des paramètres de configuration."""
    
    def test_base_dir_exists(self):
        """Test que BASE_DIR existe."""
        assert BASE_DIR.exists()
        assert BASE_DIR.is_dir()
    
    def test_data_dir(self):
        """Test du répertoire de données."""
        assert settings.data_dir == BASE_DIR / "data"
    
    def test_vector_store_dir(self):
        """Test du répertoire de vector store."""
        assert settings.vector_store_dir == BASE_DIR / "storage" / "vector_store"
    
    def test_embedding_model_name(self):
        """Test du nom du modèle d'embedding."""
        assert settings.embedding_model_name is not None
        assert isinstance(settings.embedding_model_name, str)
        assert len(settings.embedding_model_name) > 0
    
    def test_llm_model_name(self):
        """Test du nom du modèle LLM."""
        assert settings.llm_model_name is not None
        assert isinstance(settings.llm_model_name, str)
        assert len(settings.llm_model_name) > 0
    
    def test_streaming_delay(self):
        """Test du délai de streaming."""
        assert settings.streaming_delay >= 0
        assert isinstance(settings.streaming_delay, float)
    
    def test_environment_variables(self):
        """Test que les variables d'environnement sont prises en compte."""
        # Sauvegarder la valeur originale
        original_value = os.environ.get("LLM_MODEL_NAME")
        
        try:
            # Définir une nouvelle valeur
            os.environ["LLM_MODEL_NAME"] = "test_model"
            
            # Recharger les settings (nécessite un reimport)
            from importlib import reload
            from app import config
            reload(config)
            
            # Vérifier que la nouvelle valeur est prise en compte
            assert config.settings.llm_model_name == "test_model"
        finally:
            # Restaurer la valeur originale
            if original_value:
                os.environ["LLM_MODEL_NAME"] = original_value
            elif "LLM_MODEL_NAME" in os.environ:
                del os.environ["LLM_MODEL_NAME"]
            
            # Recharger les settings
            from importlib import reload
            from app import config
            reload(config)

