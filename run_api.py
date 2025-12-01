"""
Script pour lancer l'API FastAPI du RAG photographie.
"""
import uvicorn
import os

if __name__ == "__main__":
    # Configuration pour production
    workers = int(os.getenv("WORKERS", "1"))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    if workers > 1:
        # Multi-workers pour production
        uvicorn.run(
            "app.api:app",
            host="0.0.0.0",
            port=8001,
            workers=workers,
            log_level="info",
            access_log=True,
        )
    else:
        # Single worker avec reload pour développement
        uvicorn.run(
            "app.api:app",
            host="0.0.0.0",
            port=8001,
            reload=reload,
            log_level="info" if not reload else "debug",
        )
