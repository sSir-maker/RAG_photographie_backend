# Script pour tester avec curl.exe correctement dans PowerShell
# Ce script montre comment utiliser curl dans PowerShell sans erreurs

Write-Host "`n═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   TEST CURL DANS POWERSHELL" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════`n" -ForegroundColor Cyan

$email = "adedayoade993@gmail.com"
$password = "Nassir"

# Méthode 1 : Utiliser des guillemets simples pour le JSON
Write-Host "📝 Méthode 1 : Avec guillemets simples`n" -ForegroundColor Yellow

$jsonBody = @"
{"email":"$email","password":"$password"}
"@

# Sauvegarder dans un fichier temporaire (méthode la plus fiable)
$tempFile = [System.IO.Path]::GetTempFileName() + ".json"
$jsonBody | Out-File -FilePath $tempFile -Encoding utf8 -NoNewline

Write-Host "Commande curl avec fichier JSON :" -ForegroundColor Cyan
Write-Host "curl.exe -X POST `"https://rag-photographie-backend.onrender.com/auth/login`" -H `"Content-Type: application/json`" -d `"@$tempFile`"`n" -ForegroundColor White

$result = curl.exe -X POST "https://rag-photographie-backend.onrender.com/auth/login" -H "Content-Type: application/json" -d "@$tempFile" 2>&1

# Nettoyer le fichier temporaire
Remove-Item $tempFile -ErrorAction SilentlyContinue

Write-Host "Résultat :" -ForegroundColor Cyan
Write-Host $result`n

# Méthode 2 : Utiliser Invoke-RestMethod (RECOMMANDÉ)
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "`n📝 Méthode 2 : PowerShell natif (RECOMMANDÉ)`n" -ForegroundColor Yellow

$body = @{
    email = $email
    password = $password
} | ConvertTo-Json

Write-Host "Commande PowerShell :" -ForegroundColor Cyan
Write-Host 'Invoke-RestMethod -Uri "https://rag-photographie-backend.onrender.com/auth/login" -Method POST -Body $body -ContentType "application/json"`n' -ForegroundColor White

try {
    $response = Invoke-RestMethod `
        -Uri "https://rag-photographie-backend.onrender.com/auth/login" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" `
        -ErrorAction Stop
    
    Write-Host "✅ SUCCÈS !" -ForegroundColor Green
    Write-Host "Réponse :" -ForegroundColor Cyan
    $response | ConvertTo-Json
    
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "❌ Erreur $statusCode" -ForegroundColor Red
    
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $reader.BaseStream.Position = 0
    $responseBody = $reader.ReadToEnd()
    $reader.Close()
    
    Write-Host "Réponse : $responseBody" -ForegroundColor Yellow
    
    if ($responseBody -match '^\s*\{') {
        Write-Host "`n✅ JSON détecté (pas de HTML) !" -ForegroundColor Green
    } else {
        Write-Host "`n❌ HTML détecté !" -ForegroundColor Red
    }
}

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

