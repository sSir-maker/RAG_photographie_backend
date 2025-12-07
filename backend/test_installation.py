"""
Script pour tester que toutes les dépendances essentielles sont installées.
"""
import sys

def test_imports():
    """Teste les imports essentiels."""
    errors = []
    
    print("🔍 Vérification des dépendances...\n")
    
    # Dépendances essentielles
    essential = {
        "langchain": "LangChain",
        "langchain_community": "LangChain Community",
        "langchain_text_splitters": "LangChain Text Splitters",
        "langchain_core": "LangChain Core",
        "sentence_transformers": "Sentence Transformers",
        "faiss": "FAISS",
        "pdfplumber": "pdfplumber",
        "pytesseract": "pytesseract",
        "PIL": "Pillow",
    }
    
    for module, name in essential.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name} - MANQUANT")
            errors.append(f"{name}: {e}")
    
    # Dépendances optionnelles
    print("\n📦 Dépendances optionnelles (non obligatoires) :\n")
    
    optional = {
        "fitz": "PyMuPDF (extraction images PDF)",
        "pypdfium2": "pypdfium2 (alternative extraction images)",
    }
    
    for module, name in optional.items():
        try:
            __import__(module)
            print(f"✅ {name} - Installé")
        except ImportError:
            print(f"⚠️  {name} - Non installé (le système fonctionne quand même)")
    
    print("\n" + "="*50)
    
    if errors:
        print("\n❌ ERREURS DÉTECTÉES :")
        for error in errors:
            print(f"  - {error}")
        print("\n💡 Solution :")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("\n✅ Toutes les dépendances essentielles sont installées !")
        print("\n💡 Tu peux maintenant lancer :")
        print("  python run_example.py")
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)

