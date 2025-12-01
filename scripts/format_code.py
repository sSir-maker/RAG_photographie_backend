"""
Script pour formater automatiquement le code Python.
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Formate le code avec black et isort."""
    project_root = Path(__file__).resolve().parent.parent
    
    print("🎨 Formatage du code...")
    print("=" * 60)
    
    # Black
    print("\n📝 Formatage avec Black...")
    result = subprocess.run(
        [sys.executable, "-m", "black", "app/", "tests/", "scripts/"],
        cwd=project_root
    )
    
    if result.returncode != 0:
        print("❌ Erreur lors du formatage avec Black")
        return result.returncode
    
    # isort
    print("\n📦 Tri des imports avec isort...")
    result = subprocess.run(
        [sys.executable, "-m", "isort", "app/", "tests/", "scripts/"],
        cwd=project_root
    )
    
    if result.returncode != 0:
        print("❌ Erreur lors du tri des imports")
        return result.returncode
    
    print("\n✅ Formatage terminé avec succès !")
    return 0

if __name__ == "__main__":
    sys.exit(main())

