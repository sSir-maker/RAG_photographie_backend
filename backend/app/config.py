from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings:
    data_dir: Path = BASE_DIR / "data"
    vector_store_dir: Path = BASE_DIR / "storage" / "vector_store"

    # Modèle d'embedding HuggingFace (gratuit)
    embedding_model_name: str = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "sentence-transformers/all-MiniLM-L6-v2",
    )

    # LLM : par défaut on utilise Ollama en local, mais peut être remplacé par Grok (X.AI)
    # Pour utiliser Grok, configurez GROK_API_KEY (ou XAI_API_KEY) dans les variables d'environnement
    llm_model_name: str = os.getenv("LLM_MODEL_NAME", "llama3")

    # Vitesse du streaming (délai en secondes entre chaque token)
    # OPTIMISATION: Réduction du délai par défaut de 30ms à 5ms pour plus de rapidité
    streaming_delay: float = float(os.getenv("STREAMING_DELAY", "0.005"))  # 5ms par défaut (optimisé)

    # Nombre de documents à récupérer pour le RAG (défaut optimisé pour vitesse)
    num_retrieval_docs: int = int(os.getenv("NUM_RETRIEVAL_DOCS", "2"))  # 2 au lieu de 3 pour plus de rapidité

    # Taille maximale du contexte (en caractères) pour limiter la latence
    max_context_length: int = int(os.getenv("MAX_CONTEXT_LENGTH", "1500"))  # Limiter le contexte à 1500 caractères


settings = Settings()
