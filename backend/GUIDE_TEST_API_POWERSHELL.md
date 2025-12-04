# 🔧 Guide : Tester l'API avec PowerShell

## ✅ **Solution recommandée : Utiliser le script**

Le script `test_api_login.ps1` est la méthode la plus simple :

```powershell
# Test avec des identifiants personnalisés
.\test_api_login.ps1 -Email "votre@email.com" -Password "votre_mot_de_passe"

# Test avec des identifiants par défaut
.\test_api_login.ps1
```

## 🔧 **Commandes PowerShell natives**

### **Méthode 1 : Invoke-RestMethod (recommandé)**

```powershell
$body = @{
    email = "adedayoade993@gmail.com"
    password = "Nassir"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "https://rag-photographie-backend.onrender.com/auth/login" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

### **Méthode 2 : Invoke-WebRequest (plus de détails)**

```powershell
$body = @{
    email = "adedayoade993@gmail.com"
    password = "Nassir"
} | ConvertTo-Json

$response = Invoke-WebRequest `
    -Uri "https://rag-photographie-backend.onrender.com/auth/login" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Afficher le résultat
$response.Content | ConvertFrom-Json
```

### **Méthode 3 : Gestion des erreurs complète**

```powershell
$body = @{
    email = "adedayoade993@gmail.com"
    password = "Nassir"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod `
        -Uri "https://rag-photographie-backend.onrender.com/auth/login" `
        -Method POST `
        -Body $body `
        -ContentType "application/json"
    
    Write-Host "✅ Succès !" -ForegroundColor Green
    $response | ConvertTo-Json
    
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "❌ Erreur $statusCode" -ForegroundColor Red
    
    # Lire la réponse d'erreur
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $reader.BaseStream.Position = 0
    $responseBody = $reader.ReadToEnd()
    $reader.Close()
    
    Write-Host "Réponse: $responseBody" -ForegroundColor Yellow
    
    # Vérifier si c'est du JSON ou du HTML
    if ($responseBody -match '^\s*\{') {
        Write-Host "✅ JSON détecté" -ForegroundColor Green
        $responseBody | ConvertFrom-Json
    } else {
        Write-Host "❌ HTML détecté !" -ForegroundColor Red
    }
}
```

## ⚠️ **Utiliser curl.exe dans PowerShell (méthodes correctes)**

### **Méthode 1 : Utiliser un fichier JSON (RECOMMANDÉ pour curl)**

```powershell
# Créer un fichier JSON temporaire
$jsonBody = @"
{"email":"adedayoade993@gmail.com","password":"Nassir"}
"@

$tempFile = [System.IO.Path]::GetTempFileName() + ".json"
$jsonBody | Out-File -FilePath $tempFile -Encoding utf8 -NoNewline

# Utiliser curl avec le fichier
curl.exe -X POST "https://rag-photographie-backend.onrender.com/auth/login" `
  -H "Content-Type: application/json" `
  -d "@$tempFile"

# Nettoyer
Remove-Item $tempFile
```

### **Méthode 2 : Utiliser des guillemets simples (délicat)**

```powershell
# ATTENTION : Cette méthode peut être problématique selon la version PowerShell
curl.exe -X POST "https://rag-photographie-backend.onrender.com/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"adedayoade993@gmail.com\",\"password\":\"Nassir\"}'
```

### **❌ Pourquoi votre commande curl a échoué ?**

Votre commande originale :
```powershell
curl.exe -X POST https://rag-photographie-backend.onrender.com/auth/login `
  -H "Content-Type: application/json" `
  -d "{\"email\":\"adedayoade993@gmail.com\",\"password\":\"Nassir\"}"
```

**Problèmes identifiés :**
1. ❌ Les guillemets doubles échappés `\"` ne sont pas correctement interprétés par PowerShell
2. ❌ Le JSON est mal formaté à cause de l'échappement
3. ❌ Erreur : `"Expecting property name enclosed in double quotes"`

**Solution :** Utilisez plutôt `Invoke-RestMethod` (méthode PowerShell native) ou un fichier JSON temporaire avec curl.

## 🔍 **Vérifier que le backend retourne du JSON**

Le script `test_api_login.ps1` vérifie automatiquement si la réponse est du JSON ou du HTML.

**Résultat attendu (JSON) :**
```json
{
  "detail": "Email ou mot de passe incorrect"
}
```

**Si vous voyez du HTML (problème) :**
```html
<!DOCTYPE html>
<html>...
```

## 📝 **Test de l'endpoint de santé**

Pour vérifier que le backend est accessible :

```powershell
Invoke-RestMethod -Uri "https://rag-photographie-backend.onrender.com/health"
```

## 🚀 **Test complet avec tous les endpoints**

```powershell
# Health check
Write-Host "🏥 Health check..." -ForegroundColor Cyan
Invoke-RestMethod -Uri "https://rag-photographie-backend.onrender.com/health"

# Login
Write-Host "`n🔐 Login..." -ForegroundColor Cyan
$body = @{email="test@test.com";password="test"} | ConvertTo-Json
try {
    Invoke-RestMethod -Uri "https://rag-photographie-backend.onrender.com/auth/login" `
        -Method POST -Body $body -ContentType "application/json"
} catch {
    Write-Host "Erreur: $($_.Exception.Message)" -ForegroundColor Red
}
```

## ✅ **Résultat attendu**

Toutes les réponses doivent être en **JSON**, jamais en HTML :

- ✅ `{"detail": "..."}` → JSON
- ✅ `{"access_token": "...", "user": {...}}` → JSON
- ❌ `<!DOCTYPE html>` → HTML (problème à résoudre)

