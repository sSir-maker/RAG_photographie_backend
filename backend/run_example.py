"""
Script principal pour tester le RAG photographie.
Lance ce script depuis la racine du projet.
"""
from app.config import settings
from app.rag_pipeline import answer_question
from pathlib import Path


def main() -> None:
    # S'assurer que le dossier data existe
    data_dir = settings.data_dir
    data_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 Dossier documents photo : {data_dir}")
    if not any(data_dir.iterdir()):
        print(
            "⚠️  Le dossier 'data/' est vide.\n"
            "Ajoute par exemple un fichier 'bases_photographie.txt' ou un PDF de tuto photo."
        )

    # Forcer la reconstruction du vector store pour inclure tous les PDFs
    print("\n🔄 Reconstruction du vector store avec tous les documents...")
    print("   (Cela peut prendre quelques minutes pour traiter les PDFs avec OCR)\n")
    
    question = "Quels réglages de base pour photographier un portrait en lumière naturelle ?"
    print(f"❓ Question : {question}\n")
    result = answer_question(question, show_sources=True, force_rebuild=True)
    
    print("💬 Réponse du RAG :\n")
    print(result["answer"])
    
    print(f"\n📚 Sources utilisées ({result['num_sources']} documents) :\n")
    for i, source in enumerate(result["sources"], 1):
        print(f"{i}. 📄 {source['document']}")
        if source.get("path"):
            print(f"   Chemin : {source['path']}")
        print(f"   Extrait : {source['preview']}\n")


if __name__ == "__main__":
    main()

