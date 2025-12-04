# 🔐 Fix : Mot de passe trop court

## ❌ **Problème identifié**

Le mot de passe **"Nassir"** fait seulement **6 caractères**, alors que le backend requiert **au moins 8 caractères**.

```
Erreur 422 : Le mot de passe doit contenir au moins 8 caractères
```

## 📋 **Règles de validation actuelles**

Le backend valide les mots de passe selon ces règles :

1. ✅ **Minimum 8 caractères**
2. ✅ **Maximum 72 caractères** (limite bcrypt)
3. ✅ **Au moins une lettre**
4. ✅ **Au moins un chiffre ou caractère spécial**

## ✅ **Solutions**

### **Solution 1 : Utiliser un mot de passe plus long (RECOMMANDÉ)**

Utilisez un mot de passe d'au moins 8 caractères, par exemple :

- `Nassir123` (9 caractères)
- `Nassir2024` (10 caractères)
- `NassirPhoto!` (12 caractères)

### **Solution 2 : Réduire la validation à 6 caractères**

Si vous voulez vraiment utiliser "Nassir", vous pouvez modifier la validation backend :

**Fichier :** `backend/app/security.py`

```python
# Ligne 212 - Modifier de 8 à 6
if len(password) < 6:  # Au lieu de 8
    return False, "Le mot de passe doit contenir au moins 6 caractères"
```

⚠️ **Note :** Réduire la longueur minimale réduit la sécurité. Non recommandé pour la production.

## 🔧 **Test de création de compte**

Une fois que vous avez un mot de passe de 8+ caractères :

```powershell
$body = @{
    name = "Adedayo"
    email = "adedayoade993@gmail.com"
    password = "Nassir123"  # 8+ caractères
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "https://rag-photographie-backend.onrender.com/auth/signup" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

## 📝 **Modifier la validation (si nécessaire)**

Si vous voulez vraiment accepter 6 caractères minimum :

1. Modifiez `backend/app/security.py` ligne 212
2. Commitez et poussez les modifications
3. Render redéploiera automatiquement

**Mais je recommande fortement d'utiliser un mot de passe plus long pour la sécurité !**

