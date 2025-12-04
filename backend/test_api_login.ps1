# Script PowerShell pour tester l'API de login
# Usage: .\test_api_login.ps1

param(
    [string]$Email = "test@test.com",
    [string]$Password = "test123"
)

Write-Host "`n═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   TEST API LOGIN" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "📧 Email: $Email" -ForegroundColor Yellow
Write-Host "🔒 Password: $Password`n" -ForegroundColor Yellow

# Créer le body JSON
$body = @{
    email = $Email
    password = $Password
} | ConvertTo-Json

Write-Host "📤 Envoi de la requête..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

try {
    $response = Invoke-RestMethod `
        -Uri "https://rag-photographie-backend.onrender.com/auth/login" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" `
        -ErrorAction Stop
    
    Write-Host "✅ SUCCÈS !`n" -ForegroundColor Green
    Write-Host "Réponse:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10
    Write-Host "`n✅ Le backend retourne bien du JSON !" -ForegroundColor Green
    
} catch {
    Write-Host "❌ ERREUR !`n" -ForegroundColor Red
    
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "Status Code: $statusCode" -ForegroundColor Yellow
    
    if ($_.Exception.Response) {
        # Lire la réponse d'erreur
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        
        Write-Host "`nRéponse complète:" -ForegroundColor Cyan
        Write-Host $responseBody -ForegroundColor Yellow
        
        # Vérifier si c'est du JSON
        if ($responseBody -match '^\s*\{') {
            Write-Host "`n✅ Le backend retourne du JSON (pas de HTML) !" -ForegroundColor Green
            
            try {
                $parsed = $responseBody | ConvertFrom-Json
                if ($parsed.detail) {
                    Write-Host "`n📝 Message d'erreur:" -ForegroundColor Cyan
                    Write-Host $parsed.detail -ForegroundColor Yellow
                }
            } catch {
                Write-Host "`n⚠️  Impossible de parser le JSON" -ForegroundColor Yellow
            }
        } else {
            Write-Host "`n❌ Le backend retourne du HTML au lieu de JSON !" -ForegroundColor Red
            Write-Host "Les premiers caractères: $($responseBody.Substring(0, [Math]::Min(100, $responseBody.Length)))" -ForegroundColor Red
        }
        
        $reader.Close()
    } else {
        Write-Host "`n❌ Erreur de connexion:" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

