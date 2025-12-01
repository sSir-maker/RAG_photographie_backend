"""
Script de test pour diagnostiquer les erreurs de streaming.
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.rag_pipeline import answer_question_stream

def test_streaming():
    """Test le streaming pour voir les erreurs."""
    try:
        question = "Qu'est-ce que l'ISO en photographie ?"
        print(f"Test du streaming avec la question: {question}")
        print("-" * 50)
        
        for i, chunk in enumerate(answer_question_stream(question, force_rebuild=False)):
            if isinstance(chunk, dict):
                print(f"Chunk {i} (dict): {chunk.keys()}")
                if "sources" in chunk:
                    print(f"  Sources: {len(chunk.get('sources', []))}")
                    print(f"  Full answer length: {len(chunk.get('full_answer', ''))}")
            elif isinstance(chunk, str):
                print(f"Chunk {i} (str): {chunk[:50]}...")
            else:
                print(f"Chunk {i} (type: {type(chunk)}): {chunk}")
        
        print("-" * 50)
        print("Streaming terminé avec succès!")
        
    except Exception as e:
        import traceback
        print(f"ERREUR: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    test_streaming()

