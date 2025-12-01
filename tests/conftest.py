"""
Configuration et fixtures pour les tests pytest.
"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Ajouter le répertoire parent au PYTHONPATH
import sys
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.database import Base, get_db
from app.api import app
from app.config import BASE_DIR


@pytest.fixture(scope="session")
def test_data_dir():
    """Répertoire temporaire pour les données de test."""
    temp_dir = tempfile.mkdtemp(prefix="rag_test_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def test_db():
    """Base de données SQLite temporaire pour les tests."""
    # Créer une base de données en mémoire pour les tests
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal
    
    # Nettoyer
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(test_db):
    """Client de test FastAPI."""
    return TestClient(app)


@pytest.fixture(scope="function")
def test_user_data():
    """Données d'utilisateur de test."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPassword123!"
    }


@pytest.fixture(scope="function")
def authenticated_client(client, test_user_data):
    """Client authentifié avec un utilisateur de test."""
    # Créer l'utilisateur
    response = client.post("/auth/signup", json=test_user_data)
    assert response.status_code == 200
    
    # Se connecter
    login_response = client.post(
        "/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Ajouter le token aux headers
    client.headers = {"Authorization": f"Bearer {token}"}
    
    return client


@pytest.fixture(scope="function")
def sample_text_file(test_data_dir):
    """Fichier texte de test."""
    test_file = test_data_dir / "test.txt"
    test_file.write_text("Ceci est un test de document sur la photographie.")
    return test_file


@pytest.fixture(scope="function")
def sample_pdf_file(test_data_dir):
    """Fichier PDF de test (utilise un PDF existant si disponible)."""
    # Utiliser un PDF existant du projet si disponible
    existing_pdf = BASE_DIR / "data" / "Cours_Photo.pdf"
    if existing_pdf.exists():
        test_pdf = test_data_dir / "test.pdf"
        shutil.copy(existing_pdf, test_pdf)
        return test_pdf
    return None


@pytest.fixture(autouse=True)
def reset_environment():
    """Réinitialise les variables d'environnement avant chaque test."""
    # Sauvegarder les variables d'environnement importantes
    original_db_url = os.environ.get("DATABASE_URL")
    
    yield
    
    # Restaurer
    if original_db_url:
        os.environ["DATABASE_URL"] = original_db_url
    elif "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]

