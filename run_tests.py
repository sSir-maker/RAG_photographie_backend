"""
Script pour exécuter tous les tests du projet.
"""
import subprocess
import sys

def main():
    """Exécute tous les tests avec pytest."""
    print("🧪 Exécution des tests...")
    print("=" * 60)
    
    # Exécuter pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=False
    )
    
    if result.returncode == 0:
        print("\n✅ Tous les tests sont passés !")
    else:
        print("\n❌ Certains tests ont échoué.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()

