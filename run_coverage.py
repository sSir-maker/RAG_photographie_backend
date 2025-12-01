"""
Script pour générer un rapport de couverture de code.
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Génère un rapport de couverture."""
    print("📊 Génération du rapport de couverture...")
    print("=" * 60)
    
    # Créer le répertoire htmlcov s'il n'existe pas
    htmlcov_dir = Path("htmlcov")
    htmlcov_dir.mkdir(exist_ok=True)
    
    # Exécuter pytest avec couverture
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "--cov=app",
            "--cov-report=term-missing",
            "--cov-report=html",
            "-v"
        ],
        capture_output=False
    )
    
    if result.returncode == 0:
        print("\n✅ Rapport de couverture généré !")
        print(f"📄 Rapport HTML : {htmlcov_dir.absolute() / 'index.html'}")
        print("\nPour voir le rapport HTML, ouvre :")
        print(f"   {htmlcov_dir.absolute() / 'index.html'}")
    else:
        print("\n⚠️ Certains tests ont échoué, mais le rapport a été généré.")
        print(f"📄 Rapport HTML : {htmlcov_dir.absolute() / 'index.html'}")

if __name__ == "__main__":
    main()

