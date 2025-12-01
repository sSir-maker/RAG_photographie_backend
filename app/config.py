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

    # LLM : par défaut on suppose un LLM accessible via Ollama en local
    llm_model_name: str = os.getenv("LLM_MODEL_NAME", "llama3")
    
    # Vitesse du streaming (délai en secondes entre chaque token)
    streaming_delay: float = float(os.getenv("STREAMING_DELAY", "0.03"))  # 30ms par défaut


settings = Settings()


