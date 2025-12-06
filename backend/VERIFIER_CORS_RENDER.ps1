# Script PowerShell pour vérifier la configuration CORS sur Render
# Usage: .\backend\VERIFIER_CORS_RENDER.ps1

param (
    [string]$BackendUrl = "https://rag-photographie-backend.onrender.com",
    [string]$FrontendOrigin = "https://rag-photographie-frontend.onrender.com"
)

Write-Host "`n═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   🔍 VÉRIFICATION CORS RENDER" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════`n" -ForegroundColor Cyan

# Test 1: Vérifier que le backend répond
Write-Host "📡 Test 1: Vérifier que le backend répond..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "$BackendUrl/health" -Method GET -TimeoutSec 10 -ErrorAction Stop
    Write-Host "   ✅ Backend répond correctement" -ForegroundColor Green
    Write-Host "   Status: $($healthResponse.status)" -ForegroundColor Cyan
} catch {
    Write-Host "   ❌ Backend ne répond pas ou erreur:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`n⚠️  ACTION REQUISE: Vérifiez le dashboard Render pour voir si le service est démarré.`n" -ForegroundColor Yellow
    exit 1
}

# Test 2: Vérifier les headers CORS sur une requête OPTIONS (preflight)
Write-Host "`n📋 Test 2: Vérifier les headers CORS (OPTIONS preflight)..." -ForegroundColor Yellow
try {
    $optionsResponse = Invoke-WebRequest -Uri "$BackendUrl/health" -Method OPTIONS -Headers @{
        "Origin" = $FrontendOrigin
        "Access-Control-Request-Method" = "POST"
        "Access-Control-Request-Headers" = "Content-Type,Authorization"
    } -TimeoutSec 10 -ErrorAction Stop
    
    Write-Host "   ✅ Réponse OPTIONS reçue (Status: $($optionsResponse.StatusCode))" -ForegroundColor Green
    
    # Vérifier les headers CORS
    $allowOrigin = $optionsResponse.Headers["Access-Control-Allow-Origin"]
    $allowMethods = $optionsResponse.Headers["Access-Control-Allow-Methods"]
    $allowHeaders = $optionsResponse.Headers["Access-Control-Allow-Headers"]
    $allowCredentials = $optionsResponse.Headers["Access-Control-Allow-Credentials"]
    
    Write-Host "`n   Headers CORS reçus:" -ForegroundColor Cyan
    Write-Host "   - Access-Control-Allow-Origin: $allowOrigin"
    Write-Host "   - Access-Control-Allow-Methods: $allowMethods"
    Write-Host "   - Access-Control-Allow-Headers: $allowHeaders"
    Write-Host "   - Access-Control-Allow-Credentials: $allowCredentials"
    
    # Vérification
    Write-Host "`n   Vérification:" -ForegroundColor Yellow
    if ($allowOrigin -eq $FrontendOrigin -or $allowOrigin -eq "*") {
        Write-Host "   ✅ Access-Control-Allow-Origin: OK" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Access-Control-Allow-Origin: MANQUANT ou INCORRECT" -ForegroundColor Red
        Write-Host "      Attendu: $FrontendOrigin" -ForegroundColor Yellow
        Write-Host "      Reçu: $allowOrigin" -ForegroundColor Yellow
    }
    
    if ($allowMethods) {
        Write-Host "   ✅ Access-Control-Allow-Methods: Présent" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Access-Control-Allow-Methods: MANQUANT" -ForegroundColor Red
    }
    
    if ($allowHeaders) {
        Write-Host "   ✅ Access-Control-Allow-Headers: Présent" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Access-Control-Allow-Headers: MANQUANT" -ForegroundColor Red
    }
    
    if ($allowCredentials -eq "true") {
        Write-Host "   ✅ Access-Control-Allow-Credentials: OK" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Access-Control-Allow-Credentials: $allowCredentials" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "   ❌ Erreur lors du test OPTIONS:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode
        Write-Host "   Status Code: $statusCode" -ForegroundColor Yellow
        
        if ($statusCode -eq 400) {
            Write-Host "`n   ⚠️  Le backend retourne 400 pour OPTIONS !" -ForegroundColor Red
            Write-Host "   Cela signifie que le middleware CORS ne gère pas correctement les requêtes preflight.`n" -ForegroundColor Yellow
        }
    }
}

# Test 3: Vérifier les headers CORS sur une requête GET normale
Write-Host "`n📋 Test 3: Vérifier les headers CORS sur une requête GET..." -ForegroundColor Yellow
try {
    $getResponse = Invoke-WebRequest -Uri "$BackendUrl/health" -Method GET -Headers @{
        "Origin" = $FrontendOrigin
    } -TimeoutSec 10 -ErrorAction Stop
    
    $allowOrigin = $getResponse.Headers["Access-Control-Allow-Origin"]
    
    if ($allowOrigin -eq $FrontendOrigin -or $allowOrigin -eq "*") {
        Write-Host "   ✅ Headers CORS présents sur GET: OK" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Headers CORS manquants ou incorrects sur GET" -ForegroundColor Red
    }
    
} catch {
    Write-Host "   ❌ Erreur lors du test GET:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
}

# Résumé
Write-Host "`n═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   📊 RÉSUMÉ" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "Si les headers CORS sont manquants :" -ForegroundColor Yellow
Write-Host "   1. Vérifiez le dashboard Render: https://dashboard.render.com" -ForegroundColor White
Write-Host "   2. Assurez-vous que le backend est 'Live' et récemment redéployé" -ForegroundColor White
Write-Host "   3. Vérifiez les logs Render pour les erreurs" -ForegroundColor White
Write-Host "   4. Consultez: backend/CONFIGURATION_RENDER_CORS.md`n" -ForegroundColor White

