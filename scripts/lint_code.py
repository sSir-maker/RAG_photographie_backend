"""
Script pour linter le code Python.
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Lint le code avec flake8 et pylint."""
    project_root = Path(__file__).resolve().parent.parent
    
    print("🔍 Vérification du code...")
    print("=" * 60)
    
    errors = []
    
    # Black check
    print("\n📝 Vérification du formatage (Black)...")
    result = subprocess.run(
        [sys.executable, "-m", "black", "--check", "app/", "tests/", "scripts/"],
        cwd=project_root,
        capture_output=True
    )
    if result.returncode != 0:
        errors.append("Black")
        print("❌ Erreurs de formatage détectées")
        print(result.stdout.decode())
    else:
        print("✅ Formatage OK")
    
    # isort check
    print("\n📦 Vérification du tri des imports (isort)...")
    result = subprocess.run(
        [sys.executable, "-m", "isort", "--check-only", "app/", "tests/", "scripts/"],
        cwd=project_root,
        capture_output=True
    )
    if result.returncode != 0:
        errors.append("isort")
        print("❌ Erreurs de tri des imports détectées")
        print(result.stdout.decode())
    else:
        print("✅ Tri des imports OK")
    
    # Flake8
    print("\n🔍 Vérification avec Flake8...")
    result = subprocess.run(
        [sys.executable, "-m", "flake8", "app/", "tests/", "scripts/"],
        cwd=project_root,
        capture_output=True
    )
    if result.returncode != 0:
        errors.append("Flake8")
        print("❌ Erreurs Flake8 détectées")
        print(result.stdout.decode())
    else:
        print("✅ Flake8 OK")
    
    # Pylint
    print("\n🔍 Vérification avec Pylint...")
    result = subprocess.run(
        [sys.executable, "-m", "pylint", "app/"],
        cwd=project_root,
        capture_output=True
    )
    if result.returncode != 0:
        errors.append("Pylint")
        print("⚠️ Avertissements Pylint détectés")
        print(result.stdout.decode())
    else:
        print("✅ Pylint OK")
    
    if errors:
        print(f"\n❌ Erreurs détectées avec: {', '.join(errors)}")
        return 1
    else:
        print("\n✅ Toutes les vérifications sont passées !")
        return 0

if __name__ == "__main__":
    sys.exit(main())

