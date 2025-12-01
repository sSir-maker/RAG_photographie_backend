"""
Tests supplémentaires pour les fonctions d'authentification de la base de données.
"""
import pytest
from app.db_auth import (
    create_user_db,
    authenticate_user_db,
    get_user_by_email,
    get_user_by_id,
)
from app.db_auth import create_user_db as create_user


class TestDBAuth:
    """Tests des fonctions d'authentification DB."""
    
    def test_get_user_by_id(self, test_db):
        """Test de récupération d'utilisateur par ID."""
        db = test_db()
        user = create_user_db(
            db=db,
            name="Test User",
            email="test@example.com",
            password="TestPassword123!"
        )
        
        found_user = get_user_by_id(db=db, user_id=user["id"])
        assert found_user is not None
        assert found_user.id == user["id"]
        assert found_user.email == user["email"]
        
        # Utilisateur inexistant
        not_found = get_user_by_id(db=db, user_id=99999)
        assert not_found is None
        db.close()
    
    def test_create_user_returns_dict(self, test_db):
        """Test que create_user_db retourne un dictionnaire."""
        db = test_db()
        user = create_user_db(
            db=db,
            name="Test User",
            email="test@example.com",
            password="TestPassword123!"
        )
        
        assert isinstance(user, dict)
        assert "id" in user
        assert "name" in user
        assert "email" in user
        assert "created_at" in user
        db.close()
    
    def test_authenticate_user_returns_dict(self, test_db):
        """Test que authenticate_user_db retourne un dictionnaire."""
        db = test_db()
        user = create_user_db(
            db=db,
            name="Test User",
            email="test@example.com",
            password="TestPassword123!"
        )
        
        authenticated = authenticate_user_db(
            db=db,
            email="test@example.com",
            password="TestPassword123!"
        )
        
        assert isinstance(authenticated, dict)
        assert "id" in authenticated
        assert "name" in authenticated
        assert "email" in authenticated
        db.close()
    
    def test_email_case_insensitive(self, test_db):
        """Test que les emails sont traités de manière insensible à la casse."""
        db = test_db()
        user = create_user_db(
            db=db,
            name="Test User",
            email="Test@Example.COM",
            password="TestPassword123!"
        )
        
        # Devrait trouver avec différentes casse
        found1 = get_user_by_email(db=db, email="test@example.com")
        found2 = get_user_by_email(db=db, email="TEST@EXAMPLE.COM")
        found3 = get_user_by_email(db=db, email="Test@Example.COM")
        
        assert found1 is not None
        assert found2 is not None
        assert found3 is not None
        assert found1.id == user["id"]
        assert found2.id == user["id"]
        assert found3.id == user["id"]
        db.close()

