"""
Module d'authentification utilisant la base de données.
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from .database import User
from .auth import get_password_hash, verify_password


def create_user_db(db: Session, name: str, email: str, password: str) -> Optional[dict]:
    """
    Crée un nouvel utilisateur dans la base de données.
    Retourne l'utilisateur créé ou None si l'email existe déjà.
    """
    # Vérifier si l'email existe déjà
    existing_user = db.query(User).filter(User.email == email.lower()).first()
    if existing_user:
        return None
    
    # Créer le nouvel utilisateur
    hashed_password = get_password_hash(password)
    db_user = User(
        name=name,
        email=email.lower(),
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "created_at": db_user.created_at.isoformat(),
    }


def authenticate_user_db(db: Session, email: str, password: str) -> Optional[dict]:
    """
    Authentifie un utilisateur.
    Retourne l'utilisateur si les identifiants sont corrects, None sinon.
    """
    user = db.query(User).filter(User.email == email.lower()).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Récupère un utilisateur par son email."""
    return db.query(User).filter(User.email == email.lower()).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Récupère un utilisateur par son ID."""
    return db.query(User).filter(User.id == user_id).first()

