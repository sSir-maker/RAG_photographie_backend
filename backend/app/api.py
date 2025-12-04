"""
API FastAPI pour exposer le RAG photographie au frontend.
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from fastapi import Query
import json
import re
import html
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .rag_pipeline import answer_question, answer_question_stream, _load_or_build_vector_store
from .pipeline_components import RetrievalEngine
from .monitoring_phoenix import initialize_phoenix, get_phoenix_monitor
from .auth import (
    create_access_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from .database import init_db, get_db, User
from .db_auth import create_user_db, authenticate_user_db, get_user_by_email
from .db_chat import (
    create_conversation,
    get_user_conversations,
    get_conversation,
    delete_conversation,
    add_message,
    get_conversation_messages,
    update_conversation_title,
)
from .security import (
    input_sanitizer,
    get_secrets_manager,
    generate_secret_key,
)
from sqlalchemy.orm import Session
from datetime import timedelta
import os
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Photographie API", version="1.0.0")

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# ⚠️ IMPORTANT: CORS DOIT être configuré AVANT les gestionnaires d'exceptions
# CORS pour permettre les requêtes depuis le frontend (Vite ou Next.js)
# Configuration depuis les variables d'environnement
default_origins = [
    "http://localhost:3000",  # Vite par défaut
    "http://localhost:3001",  # Alternative
    "http://127.0.0.1:3000",  # Alternative localhost
    "https://rag-photographie-frontend.onrender.com",  # Frontend déployé sur Render
]

# Ajouter les origines depuis la variable d'environnement CORS_ORIGINS (séparées par des virgules)
cors_origins_env = os.getenv("CORS_ORIGINS", "")
if cors_origins_env:
    additional_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
    default_origins.extend(additional_origins)

# Ajouter FRONTEND_URL si spécifié
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url not in default_origins:
    default_origins.append(frontend_url)

# Logger les origines CORS configurées
logger.info(f"CORS origins configurés: {default_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=default_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],  # Exposer tous les headers pour le streaming
    max_age=3600,  # Cache preflight requests for 1 hour (optimisation mobile)
)


# Gestionnaire personnalisé pour le rate limiting (retourne JSON au lieu de HTML)
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Gestionnaire personnalisé pour les erreurs de rate limiting (retourne JSON)."""
    # Obtenir l'origine de la requête pour les headers CORS
    origin = request.headers.get("origin")
    cors_headers = {}
    if origin in default_origins:
        cors_headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }
    
    response = JSONResponse(
        status_code=429,
        content={
            "detail": "Trop de requêtes. Veuillez réessayer plus tard.",
            "retry_after": str(exc.retry_after) if exc.retry_after else None,
        },
        headers={**cors_headers, **({"Retry-After": str(exc.retry_after)} if exc.retry_after else {})},
    )
    return response


# Gestionnaire d'exceptions global pour garantir des réponses JSON
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Gestionnaire d'exceptions global pour retourner du JSON au lieu de HTML."""
    logger.error(f"Exception non gérée: {type(exc).__name__}: {str(exc)}", exc_info=True)
    
    # Obtenir l'origine de la requête pour les headers CORS
    origin = request.headers.get("origin")
    cors_headers = {}
    if origin in default_origins:
        cors_headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }
    
    # Si c'est déjà une HTTPException, la retourner en JSON
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers={**cors_headers, **(exc.headers or {})},
        )
    
    # Pour toutes les autres exceptions, retourner une erreur 500 en JSON
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erreur interne du serveur",
            "error": str(exc),
            "type": type(exc).__name__,
        },
        headers=cors_headers,
    )


# Gestionnaire pour les erreurs de validation Pydantic
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Gestionnaire pour les erreurs de validation Pydantic (retourne JSON)."""
    # Obtenir l'origine de la requête pour les headers CORS
    origin = request.headers.get("origin")
    cors_headers = {}
    if origin in default_origins:
        cors_headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Erreur de validation",
            "errors": exc.errors(),
        },
        headers=cors_headers,
    )


# Initialiser la base de données au démarrage
@app.on_event("startup")
async def startup_event():
    init_db()

    # Initialiser Phoenix monitoring
    try:
        phoenix_endpoint = os.getenv("PHOENIX_ENDPOINT", "http://localhost:6006")
        initialize_phoenix(endpoint=phoenix_endpoint)
        logger.info(f"Phoenix monitoring initialisé (endpoint: {phoenix_endpoint})")
    except Exception as e:
        logger.warning(f"Phoenix monitoring non disponible: {e}")


# Sécurité pour les tokens JWT
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
) -> User:
    """Dépendance pour vérifier le token et récupérer l'utilisateur actuel."""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères")
        if len(v) > 100:
            raise ValueError("Le nom est trop long (max 100 caractères)")
        return input_sanitizer.sanitize_text(v, max_length=100)

    @validator("email")
    def validate_email(cls, v):
        return input_sanitizer.sanitize_email(v)

    @validator("password")
    def validate_password(cls, v):
        is_valid, error = input_sanitizer.validate_password(v)
        if not is_valid:
            raise ValueError(error)
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class QuestionRequest(BaseModel):
    question: str
    force_rebuild: bool = False

    @validator("question")
    def validate_question(cls, v):
        return input_sanitizer.sanitize_question(v)


class SourceInfo(BaseModel):
    document: str
    path: str
    page: Optional[str] = None
    preview: str


class AnswerResponse(BaseModel):
    answer: str
    sources: List[SourceInfo]
    num_sources: int


@app.get("/")
async def root():
    return {"message": "RAG Photographie API", "status": "running"}


@app.get("/health")
async def health():
    """Endpoint de santé basique."""
    from .health import HealthChecker

    checker = HealthChecker()
    return checker.get_system_health()


@app.get("/health/detailed")
async def health_detailed():
    """Endpoint de santé détaillé."""
    from .health import HealthChecker

    checker = HealthChecker()
    return checker.get_detailed_health()


@app.get("/metrics")
async def get_metrics():
    """Endpoint pour récupérer les métriques."""
    from .metrics import get_metrics_collector

    metrics = get_metrics_collector()
    return metrics.get_all_metrics_summary()


@app.get("/alerts")
async def get_alerts(hours: int = 24, level: Optional[str] = None, current_user: User = Depends(get_current_user)):
    """Récupère les alertes récentes (nécessite authentification)."""
    from .alerting import get_alert_manager, AlertLevel

    alert_manager = get_alert_manager()

    alert_level = None
    if level:
        try:
            alert_level = AlertLevel(level.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Niveau d'alerte invalide: {level}")

    alerts = alert_manager.get_recent_alerts(hours=hours, level=alert_level)

    return {
        "count": len(alerts),
        "alerts": [
            {
                "id": a.id,
                "title": a.title,
                "message": a.message,
                "level": a.level.value,
                "source": a.source,
                "timestamp": a.timestamp.isoformat(),
                "metadata": a.metadata,
            }
            for a in alerts
        ],
    }


@app.post("/auth/signup", response_model=AuthResponse)
@limiter.limit("5/minute")  # 5 inscriptions par minute
async def signup(request: Request, signup_data: SignupRequest, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur.
    """
    try:
        logger.info(f"Tentative d'inscription pour: {signup_data.email}")
        
        # Créer l'utilisateur dans la base de données
        user = create_user_db(db, signup_data.name, signup_data.email, signup_data.password)

        if user is None:
            logger.warning(f"Échec d'inscription pour: {signup_data.email} (email déjà utilisé)")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est déjà utilisé",
            )

        # Créer le token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"], "name": user["name"]},
            expires_delta=access_token_expires,
        )

        logger.info(f"Inscription réussie pour: {signup_data.email}")
        
        # Forcer le Content-Type à application/json
        response_data = AuthResponse(
            access_token=access_token,
            user=user,
        )
        
        return JSONResponse(
            status_code=200,
            content=response_data.dict(),
            headers={"Content-Type": "application/json"},
        )
        
    except HTTPException:
        # Relancer les HTTPException telles quelles (elles seront gérées par le gestionnaire)
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'inscription: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'inscription: {str(e)}",
        )


@app.post("/auth/login", response_model=AuthResponse)
@limiter.limit("10/minute")  # 10 tentatives de connexion par minute
async def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Connexion d'un utilisateur existant.
    """
    try:
        logger.info(f"Tentative de connexion pour: {login_data.email}")
        
        user = authenticate_user_db(db, login_data.email, login_data.password)

        if user is None:
            logger.warning(f"Échec de connexion pour: {login_data.email} (email ou mot de passe incorrect)")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Créer le token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"], "name": user["name"]},
            expires_delta=access_token_expires,
        )

        logger.info(f"Connexion réussie pour: {login_data.email}")
        
        # Forcer le Content-Type à application/json
        response_data = AuthResponse(
            access_token=access_token,
            user=user,
        )
        
        return JSONResponse(
            status_code=200,
            content=response_data.dict(),
            headers={"Content-Type": "application/json"},
        )
        
    except HTTPException:
        # Relancer les HTTPException telles quelles (elles seront gérées par le gestionnaire)
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue lors de la connexion: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la connexion: {str(e)}",
        )


@app.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Retourne les informations de l'utilisateur connecté."""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
    }


class ConversationRequest(BaseModel):
    conversation_id: Optional[int] = None
    question: str
    force_rebuild: bool = False

    @validator("question")
    def validate_question(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError("La question doit contenir au moins 3 caractères")
        return input_sanitizer.sanitize_question(v)


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    image_url: Optional[str] = None
    created_at: str


@app.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Récupère toutes les conversations de l'utilisateur."""
    conversations = get_user_conversations(db, current_user.id)
    return [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at.isoformat() if conv.created_at else "",
            "updated_at": conv.updated_at.isoformat() if conv.updated_at else "",
        }
        for conv in conversations
    ]


@app.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Récupère tous les messages d'une conversation."""
    messages = get_conversation_messages(db, conversation_id, current_user.id)
    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "image_url": msg.image_url,
            "created_at": msg.created_at.isoformat() if msg.created_at else "",
        }
        for msg in messages
    ]


@app.post("/conversations", response_model=ConversationResponse)
async def create_new_conversation(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Crée une nouvelle conversation."""
    conversation = create_conversation(db, current_user.id)
    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at.isoformat() if conversation.created_at else "",
        "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else "",
    }


@app.delete("/conversations/{conversation_id}")
async def delete_conversation_endpoint(
    conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Supprime une conversation."""
    success = delete_conversation(db, conversation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation non trouvée")
    return {"message": "Conversation supprimée"}


async def generate_streaming_response(
    question: str, conversation_id: int, db: Session, current_user: User, force_rebuild: bool = False
):
    """
    Génère une réponse en streaming et sauvegarde dans la DB.
    """
    full_answer = ""
    sources = []

    try:
        # Stream la réponse
        for chunk in answer_question_stream(question, force_rebuild=force_rebuild):
            # Vérifier si c'est le dernier chunk avec sources
            if isinstance(chunk, dict) and "sources" in chunk:
                sources = chunk["sources"]
                full_answer = chunk.get("full_answer", full_answer)
                if not full_answer:
                    # Si full_answer est vide, utiliser la réponse complète générée
                    full_answer = chunk.get("answer", "")

                # Sauvegarder la réponse complète dans la DB
                if full_answer:
                    add_message(db, conversation_id, "assistant", full_answer)

                # Envoyer les sources
                yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"
                # Envoyer le signal de fin
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                break
            elif isinstance(chunk, str):
                # C'est un chunk de texte
                full_answer += chunk
                # Envoyer le chunk au client
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
            else:
                # Format inattendu, logger pour debug
                print(f"Chunk inattendu: {type(chunk)} - {chunk}")

        # Si on n'a pas reçu de sources, les récupérer manuellement
        if not sources and full_answer:
            try:
                vector_store = _load_or_build_vector_store(force_rebuild=force_rebuild)
                retriever_engine = RetrievalEngine(vector_store)
                retriever = retriever_engine.get_retriever()
                retrieved_docs = retriever.invoke(question)

                for doc in retrieved_docs:
                    source_info = {
                        "document": doc.metadata.get("source_document", "Inconnu"),
                        "path": doc.metadata.get("path", ""),
                        "page": doc.metadata.get("page", ""),
                        "preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    }
                    sources.append(source_info)

                if sources:
                    yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"
            except Exception as e:
                print(f"Erreur lors de la récupération des sources: {e}")

        # S'assurer que le message est sauvegardé si ce n'est pas déjà fait
        if full_answer:
            try:
                # Vérifier si le message existe déjà
                existing_messages = get_conversation_messages(db, conversation_id, current_user.id)
                if not existing_messages or existing_messages[-1].content != full_answer:
                    add_message(db, conversation_id, "assistant", full_answer)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde du message: {e}")

    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        print(f"Erreur dans generate_streaming_response: {error_details}")
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"


@app.options("/ask/stream")
async def ask_question_stream_options():
    """Gère les requêtes OPTIONS pour le streaming (CORS preflight)."""
    from fastapi.responses import Response

    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )


@app.post("/ask/stream")
@limiter.limit("20/minute")  # 20 requêtes par minute par utilisateur
async def ask_question_stream(
    request: Request,
    conversation_data: ConversationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Pose une question au RAG et retourne la réponse en streaming (Server-Sent Events).
    Sauvegarde automatiquement les messages dans la base de données.
    """
    try:
        # Créer ou récupérer la conversation
        if conversation_data.conversation_id:
            conversation = get_conversation(db, conversation_data.conversation_id, current_user.id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation non trouvée")
        else:
            conversation = create_conversation(db, current_user.id, conversation_data.question[:50])

        # Ajouter le message utilisateur
        add_message(db, conversation.id, "user", conversation_data.question)

        return StreamingResponse(
            generate_streaming_response(
                conversation_data.question, conversation.id, db, current_user, conversation_data.force_rebuild
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        print(f"Erreur dans ask_question_stream: {error_details}")

        # Retourner une réponse d'erreur en streaming
        async def error_stream():
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        return StreamingResponse(
            error_stream(),
            media_type="text/event-stream",
            status_code=500,
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )


@app.post("/ask", response_model=AnswerResponse)
@limiter.limit("20/minute")  # 20 requêtes par minute par utilisateur
async def ask_question(
    request: Request,
    conversation_data: ConversationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Pose une question au RAG et retourne la réponse avec les sources (non-streaming, pour compatibilité).
    Sauvegarde automatiquement les messages dans la base de données.
    """
    try:
        # Créer ou récupérer la conversation
        if conversation_data.conversation_id:
            conversation = get_conversation(db, conversation_data.conversation_id, current_user.id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation non trouvée")
        else:
            conversation = create_conversation(db, current_user.id, conversation_data.question[:50])

        # Ajouter le message utilisateur
        add_message(db, conversation.id, "user", conversation_data.question)

        # Obtenir la réponse du RAG
        result = answer_question(
            question=conversation_data.question,
            show_sources=True,
            force_rebuild=conversation_data.force_rebuild,
        )

        # Ajouter la réponse de l'assistant
        add_message(db, conversation.id, "assistant", result.get("answer", ""))

        # Convertir les sources en modèles Pydantic
        sources = [
            SourceInfo(
                document=source["document"],
                path=source.get("path", ""),
                page=source.get("page"),
                preview=source.get("preview", ""),
            )
            for source in result.get("sources", [])
        ]

        return AnswerResponse(
            answer=result.get("answer", ""),
            sources=sources,
            num_sources=result.get("num_sources", 0),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")


# ========== Export de conversations ==========


@app.get("/conversations/{conversation_id}/export")
async def export_conversation(
    conversation_id: int,
    format: str = "json",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Exporte une conversation dans différents formats."""
    conversation = get_conversation(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation non trouvée")

    messages = get_conversation_messages(db, conversation_id, current_user.id)

    if format == "json":
        content = export_conversation_json(conversation, messages)
        media_type = "application/json"
        filename = f"conversation_{conversation_id}.json"
    elif format == "csv":
        content = export_conversation_csv(conversation, messages)
        media_type = "text/csv"
        filename = f"conversation_{conversation_id}.csv"
    elif format == "markdown":
        content = export_conversation_markdown(conversation, messages)
        media_type = "text/markdown"
        filename = f"conversation_{conversation_id}.md"
    elif format == "txt":
        content = export_conversation_txt(conversation, messages)
        media_type = "text/plain"
        filename = f"conversation_{conversation_id}.txt"
    else:
        raise HTTPException(status_code=400, detail=f"Format non supporté: {format}")

    from fastapi.responses import Response

    return Response(
        content=content, media_type=media_type, headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.post("/conversations/export/bulk")
async def export_conversations_bulk_endpoint(
    conversation_ids: List[int],
    format: str = "json",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Exporte plusieurs conversations dans un seul fichier."""
    conversations = []
    for conv_id in conversation_ids:
        conv = get_conversation(db, conv_id, current_user.id)
        if conv:
            conversations.append(conv)

    if not conversations:
        raise HTTPException(status_code=404, detail="Aucune conversation trouvée")

    content = export_conversations_bulk(conversations, format, db)

    if format == "json":
        media_type = "application/json"
        filename = "conversations_export.json"
    elif format == "csv":
        media_type = "text/csv"
        filename = "conversations_export.csv"
    else:
        raise HTTPException(status_code=400, detail=f"Format non supporté pour bulk: {format}")

    from fastapi.responses import Response

    return Response(
        content=content, media_type=media_type, headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


# ========== Recherche dans l'historique ==========


@app.get("/search/messages")
async def search_messages(
    query: str = Query(..., min_length=1),
    conversation_id: Optional[int] = None,
    role: Optional[str] = Query(None, regex="^(user|assistant)$"),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Recherche dans les messages des conversations."""
    results = search_in_conversations(db, current_user.id, query, conversation_id, role, limit)
    return {"query": query, "count": len(results), "results": results}


@app.get("/search/conversations")
async def search_conversations(
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Recherche des conversations par titre."""
    results = search_conversations_by_title(db, current_user.id, query, limit)
    return {"query": query, "count": len(results), "results": results}


@app.get("/conversations/{conversation_id}/statistics")
async def get_statistics(
    conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Récupère les statistiques d'une conversation."""
    conversation = get_conversation(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation non trouvée")

    stats = get_conversation_statistics(db, current_user.id, conversation_id)
    return stats


# ========== Partage de conversations ==========


@app.post("/conversations/{conversation_id}/share")
async def share_conversation(
    conversation_id: int,
    expires_in_days: Optional[int] = Query(None, ge=1, le=365),
    max_views: Optional[int] = Query(None, ge=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Crée un lien de partage pour une conversation."""
    try:
        shared = create_shared_conversation(db, conversation_id, current_user.id, expires_in_days, max_views)

        # Construire l'URL de partage
        base_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        share_url = f"{base_url}/shared/{shared.share_token}"

        return {
            "share_token": shared.share_token,
            "share_url": share_url,
            "expires_at": shared.expires_at.isoformat() if shared.expires_at else None,
            "max_views": shared.max_views,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/shared/{share_token}")
async def get_shared_conversation_endpoint(share_token: str, db: Session = Depends(get_db)):
    """Récupère une conversation partagée (publique, pas d'authentification requise)."""
    result = get_shared_conversation(db, share_token)
    if not result:
        raise HTTPException(status_code=404, detail="Lien de partage invalide ou expiré")
    return result


@app.delete("/conversations/{conversation_id}/share")
async def revoke_share(
    conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Révoque un partage de conversation."""
    success = revoke_shared_conversation(db, conversation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Partage non trouvé")
    return {"message": "Partage révoqué avec succès"}


@app.get("/conversations/shared")
async def list_shared_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Liste toutes les conversations partagées par l'utilisateur."""
    shared = get_user_shared_conversations(db, current_user.id)
    return {"count": len(shared), "shared_conversations": shared}


# ========== Multi-LLM support ==========


@app.get("/llms")
async def list_llms(current_user: User = Depends(get_current_user)):
    """Liste tous les LLM disponibles."""
    manager = get_llm_manager()
    return {"llms": manager.list_llms()}


@app.get("/llms/{llm_name}")
async def get_llm_info(llm_name: str, current_user: User = Depends(get_current_user)):
    """Récupère les informations sur un LLM spécifique."""
    manager = get_llm_manager()
    try:
        return manager.get_llm_info(llm_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
