"""
Script d'exemple pour tester le RAG photographie.
Peut être lancé depuis la racine avec: python -m app.run_example
"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH pour les imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.config import settings
from app.rag_pipeline import answer_question


def main() -> None:
    # S'assurer que le dossier data existe
    data_dir = settings.data_dir
    data_dir.mkdir(parents=True, exist_ok=True)

    print(f"Dossier documents photo : {data_dir}")
    if not any(data_dir.iterdir()):
        print(
            "⚠️  Le dossier 'data/' est vide.\n"
            "Ajoute par exemple un fichier 'bases_photographie.txt' ou un PDF de tuto photo."
        )

    question = "Quels réglages de base pour photographier un portrait en lumière naturelle ?"
    print(f"\nQuestion : {question}\n")
    answer = answer_question(question)
    print("Réponse du RAG :\n")
    print(answer)


if __name__ == "__main__":
    main()


