"""
Configuration de la base de données avec SQLAlchemy.
Supporte SQLite (développement) et PostgreSQL (production).
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import NullPool, QueuePool
from datetime import datetime
from pathlib import Path
import os
import logging

from .config import BASE_DIR

logger = logging.getLogger(__name__)

# Configuration de la base de données depuis les variables d'environnement
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'storage' / 'database.db'}"
)

# Détecter le type de base de données
IS_POSTGRESQL = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgresql+psycopg2://")
IS_SQLITE = DATABASE_URL.startswith("sqlite:///")

# Créer le répertoire storage s'il n'existe pas (pour SQLite)
if IS_SQLITE:
    (BASE_DIR / 'storage').mkdir(parents=True, exist_ok=True)

# Configuration de l'engine selon le type de DB
if IS_POSTGRESQL:
    # PostgreSQL : utiliser connection pooling optimisé
    pool_size = int(os.getenv("DB_POOL_SIZE", "20"))  # Augmenté pour meilleure performance
    max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "40"))  # Augmenté
    pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))  # Timeout en secondes
    pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "3600"))  # Recycler les connexions après 1h
    
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=pool_recycle,  # Recycler les connexions pour éviter les timeouts
        pool_pre_ping=True,  # Vérifier les connexions avant utilisation
        echo=os.getenv("DB_ECHO", "false").lower() == "true",
        # Optimisations supplémentaires
        connect_args={
            "connect_timeout": 10,
            "application_name": "rag_photographie",
        } if "postgresql" in DATABASE_URL else {},
    )
    logger.info(f"✅ Connexion PostgreSQL configurée (pool_size={pool_size}, max_overflow={max_overflow})")
elif IS_SQLITE:
    # SQLite : configuration pour développement
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,  # Pas de pooling pour SQLite
        echo=os.getenv("DB_ECHO", "false").lower() == "true",
    )
    logger.info("✅ Connexion SQLite configurée")
else:
    raise ValueError(f"Type de base de données non supporté: {DATABASE_URL}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    """Modèle utilisateur."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Limite de longueur pour PostgreSQL
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relations
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")


class Conversation(Base):
    """Modèle conversation."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(Base):
    """Modèle message."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False)  # 'user' ou 'assistant'
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relations
    conversation = relationship("Conversation", back_populates="messages")


def init_db():
    """Initialise la base de données (crée les tables)."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Base de données initialisée avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
        raise


def check_db_connection():
    """Vérifie la connexion à la base de données."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Connexion à la base de données OK")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur de connexion à la base de données: {e}")
        return False


def get_db():
    """Dépendance pour obtenir une session de base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

