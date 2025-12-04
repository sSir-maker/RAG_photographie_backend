# 🔧 Fix : Erreur curl dans PowerShell

## ❌ **Votre erreur**

```powershell
curl.exe -X POST https://rag-photographie-backend.onrender.com/auth/login `
  -H "Content-Type: application/json" `
  -d "{\"email\":\"adedayoade993@gmail.com\",\"password\":\"Nassir\"}"
```

**Résultat :**
```
{"detail":[{"type":"json_invalid","loc":["body",1],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting property name enclosed in double quotes"}}]}
curl: (3) URL rejected: Port number was not a decimal number between 0 and 65535
```

## 🔍 **Pourquoi ça ne fonctionne pas ?**

PowerShell interprète les guillemets doubles échappés (`\"`) de manière spéciale. Quand vous écrivez :

```powershell
-d "{\"email\":\"test@test.com\",\"password\":\"test\"}"
```

PowerShell peut :
1. Mal interpréter les guillemets échappés
2. Créer un JSON invalide
3. Provoquer des erreurs d'URL

## ✅ **Solutions**

### **Solution 1 : PowerShell natif (RECOMMANDÉ)**

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

**✅ Avantages :**
- Pas de problème d'échappement
- Gestion native des objets JSON
- Meilleure gestion des erreurs

### **Solution 2 : curl avec fichier JSON**

```powershell
# Créer le JSON dans un fichier
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

### **Solution 3 : curl avec guillemets simples (délicat)**

```powershell
# Utiliser des guillemets simples ET des backticks pour échapper
curl.exe -X POST "https://rag-photographie-backend.onrender.com/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"adedayoade993@gmail.com\",\"password\":\"Nassir\"}'
```

⚠️ **Note :** Cette méthode peut ne pas fonctionner selon votre version de PowerShell.

## 🚀 **Commandes prêtes à l'emploi**

### **Commande rapide (1 ligne)**

```powershell
$body = @{email="adedayoade993@gmail.com";password="Nassir"} | ConvertTo-Json; Invoke-RestMethod -Uri "https://rag-photographie-backend.onrender.com/auth/login" -Method POST -Body $body -ContentType "application/json"
```

### **Avec gestion d'erreurs**

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
    
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $reader.BaseStream.Position = 0
    $responseBody = $reader.ReadToEnd()
    $reader.Close()
    
    Write-Host "Réponse: $responseBody" -ForegroundColor Yellow
}
```

## 📝 **Scripts disponibles**

1. **`COMMANDE_TEST_RAPIDE.ps1`** - Commande simple en 2 lignes
2. **`test_api_login.ps1`** - Script complet avec gestion d'erreurs
3. **`test_curl_correct.ps1`** - Exemples avec curl (si vous devez l'utiliser)

## ✅ **Résultat attendu**

Avec la bonne commande, vous devriez voir :

**Succès (200) :**
```json
{
  "access_token": "eyJhbGciOiJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "adedayoade993@gmail.com",
    "name": "..."
  }
}
```

**Erreur (401) :**
```json
{
  "detail": "Email ou mot de passe incorrect"
}
```

**Important :** Les deux réponses sont en **JSON** (pas de HTML) ✅

## 💡 **Recommandation finale**

**Utilisez `Invoke-RestMethod`** plutôt que `curl.exe` dans PowerShell. C'est :
- ✅ Plus simple
- ✅ Plus fiable
- ✅ Mieux intégré à PowerShell
- ✅ Pas de problème d'échappement

