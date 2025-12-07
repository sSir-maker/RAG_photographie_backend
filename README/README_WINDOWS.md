# 🪟 Guide Windows - Commandes Rapides

## ⚡ Commandes Essentielles

### Installation

```powershell
# Installer les outils de développement
.\scripts\install-dev.ps1

# Ou manuellement
pip install -r requirements-dev.txt
```

### Formatage

```powershell
.\scripts\format.ps1
```

### Vérification

```powershell
.\scripts\lint.ps1
```

### Tests

```powershell
.\scripts\test.ps1
```

### Nettoyage

```powershell
.\scripts\clean.ps1
```

## ⚠️ Si tu as une erreur de politique d'exécution

```powershell
# Autoriser les scripts pour la session actuelle
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Puis réessayer
.\scripts\format.ps1
```

## 📚 Documentation Complète

Voir `WINDOWS_SCRIPTS.md` pour plus de détails.

---

**✅ Utilise les scripts PowerShell au lieu de `make` sur Windows !**

