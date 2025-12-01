"""
Tests pour la sécurité (input sanitization, rate limiting, secrets management).
"""
import pytest

from app.security import InputSanitizer, SecretsManager
from pathlib import Path
import tempfile
import os


class TestInputSanitizer:
    """Tests de sanitization des entrées."""
    
    def test_sanitize_text(self):
        """Test de sanitization de texte."""
        sanitizer = InputSanitizer()
        
        # Texte normal
        clean_text = sanitizer.sanitize_text("Hello World")
        assert clean_text == "Hello World"
        
        # XSS - Script tag
        xss_text = "<script>alert('XSS')</script>Hello"
        sanitized = sanitizer.sanitize_text(xss_text)
        assert "<script>" not in sanitized
        assert "Hello" in sanitized
        
        # XSS - Event handler
        xss_text2 = '<img onerror="alert(1)" src="x">'
        sanitized = sanitizer.sanitize_text(xss_text2)
        assert "onerror" not in sanitized
        
        # SQL Injection
        sql_text = "'; DROP TABLE users; --"
        sanitized = sanitizer.sanitize_text(sql_text)
        assert "DROP" not in sanitized or "TABLE" not in sanitized
    
    def test_sanitize_email(self):
        """Test de sanitization d'email."""
        sanitizer = InputSanitizer()
        
        email = "TEST@EXAMPLE.COM"
        sanitized = sanitizer.sanitize_email(email)
        assert sanitized == "test@example.com"  # Lowercase
        
        # Email avec caractères dangereux
        dangerous_email = "<script>test@example.com</script>"
        sanitized = sanitizer.sanitize_email(dangerous_email)
        assert "<script>" not in sanitized
    
    def test_sanitize_question(self):
        """Test de sanitization de question."""
        sanitizer = InputSanitizer()
        
        question = "Qu'est-ce que la photographie?"
        sanitized = sanitizer.sanitize_question(question)
        assert "photographie" in sanitized.lower()
        
        # Question trop longue
        long_question = "A" * 1000
        sanitized = sanitizer.sanitize_question(long_question)
        assert len(sanitized) <= 500
    
    def test_validate_password(self):
        """Test de validation de mot de passe."""
        sanitizer = InputSanitizer()
        
        # Mot de passe valide
        is_valid, message = sanitizer.validate_password("TestPassword123!")
        assert is_valid is True
        assert message is None
        
        # Trop court
        is_valid, message = sanitizer.validate_password("Short1!")
        assert is_valid is False
        assert "8 caractères" in message
        
        # Pas de majuscule
        is_valid, message = sanitizer.validate_password("testpassword123!")
        assert is_valid is False
        assert "majuscule" in message
        
        # Pas de minuscule
        is_valid, message = sanitizer.validate_password("TESTPASSWORD123!")
        assert is_valid is False
        assert "minuscule" in message
        
        # Pas de chiffre
        is_valid, message = sanitizer.validate_password("TestPassword!")
        assert is_valid is False
        assert "chiffre" in message
        
        # Pas de caractère spécial
        is_valid, message = sanitizer.validate_password("TestPassword123")
        assert is_valid is False
        assert "spécial" in message


class TestSecretsManager:
    """Tests de gestion des secrets."""
    
    def test_secrets_manager_creation(self):
        """Test de création d'un gestionnaire de secrets."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_file = Path(temp_dir) / ".secrets"
            manager = SecretsManager(secrets_file=secrets_file)
            assert manager is not None
    
    def test_set_and_get_secret(self):
        """Test de stockage et récupération de secret."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_file = Path(temp_dir) / ".secrets"
            manager = SecretsManager(secrets_file=secrets_file)
            
            # Définir un secret
            manager.set_secret("TEST_KEY", "test_value")
            
            # Récupérer le secret
            value = manager.get_secret("TEST_KEY")
            assert value == "test_value"
            
            # Secret inexistant
            not_found = manager.get_secret("NONEXISTENT", default="default")
            assert not_found == "default"
    
    def test_generate_key(self):
        """Test de génération de clé."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_file = Path(temp_dir) / ".secrets"
            manager = SecretsManager(secrets_file=secrets_file)
            
            key = manager.generate_key("TEST_KEY")
            assert key is not None
            assert len(key) > 0
            
            # Vérifier qu'elle est sauvegardée
            saved_key = manager.get_secret("TEST_KEY")
            assert saved_key == key
    
    def test_secrets_encryption(self):
        """Test que les secrets sont chiffrés."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_file = Path(temp_dir) / ".secrets"
            manager = SecretsManager(secrets_file=secrets_file)
            
            manager.set_secret("TEST_KEY", "sensitive_value")
            
            # Vérifier que le fichier existe et contient des données chiffrées
            assert secrets_file.exists()
            content = secrets_file.read_bytes()
            
            # Le contenu ne devrait pas contenir la valeur en clair
            assert b"sensitive_value" not in content


class TestSecretKeyGeneration:
    """Tests de génération de clés secrètes."""
    
    def test_generate_secret_key(self):
        """Test de génération de clé secrète."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_file = Path(temp_dir) / ".secrets"
            manager = SecretsManager(secrets_file=secrets_file)
            key = manager.generate_key("TEST_KEY")
            assert key is not None
            assert isinstance(key, str)
            assert len(key) > 0
    
    def test_generate_unique_keys(self):
        """Test que les clés générées sont uniques."""
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_file = Path(temp_dir) / ".secrets"
            manager = SecretsManager(secrets_file=secrets_file)
            key1 = manager.generate_key("TEST_KEY_1")
            key2 = manager.generate_key("TEST_KEY_2")
            assert key1 != key2

