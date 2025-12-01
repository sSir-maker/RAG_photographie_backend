"""
Module d'authentification pour le RAG Photographie.
Gère l'inscription, la connexion et la génération de tokens JWT.
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from .config import BASE_DIR

# Clé secrète pour JWT (en production, utiliser une variable d'environnement)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 jours

# Fichier de stockage des utilisateurs
USERS_FILE = BASE_DIR / "storage" / "users.json"


def get_password_hash(password: str) -> str:
    """Hash un mot de passe avec bcrypt."""
    # Générer un salt et hasher le mot de passe
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe contre son hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def load_users() -> dict:
    """Charge les utilisateurs depuis le fichier JSON."""
    if not USERS_FILE.exists():
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users: dict) -> None:
    """Sauvegarde les utilisateurs dans le fichier JSON."""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def create_user(name: str, email: str, password: str) -> dict:
    """
    Crée un nouvel utilisateur.
    Retourne l'utilisateur créé ou None si l'email existe déjà.
    """
    users = load_users()
    
    # Vérifier si l'email existe déjà
    if email.lower() in users:
        return None
    
    # Créer le nouvel utilisateur
    user = {
        "name": name,
        "email": email.lower(),
        "hashed_password": get_password_hash(password),
        "created_at": datetime.utcnow().isoformat(),
    }
    
    users[email.lower()] = user
    save_users(users)
    
    return {
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
    }


def authenticate_user(email: str, password: str) -> Optional[dict]:
    """
    Authentifie un utilisateur.
    Retourne l'utilisateur si les identifiants sont corrects, None sinon.
    """
    users = load_users()
    user = users.get(email.lower())
    
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return {
        "name": user["name"],
        "email": user["email"],
        "created_at": user.get("created_at"),
    }


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crée un token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Vérifie et décode un token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

