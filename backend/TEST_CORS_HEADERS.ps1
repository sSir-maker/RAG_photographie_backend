# Script PowerShell pour tester si les headers CORS sont présents
# Utilisez ce script pour vérifier que le backend renvoie bien les headers CORS

param(
    [Parameter(Mandatory=$false)]
    [string]$BackendUrl = "https://rag-photographie-backend.onrender.com",
    
    [Parameter(Mandatory=$false)]
    [string]$Origin = "https://rag-photographie-frontend.onrender.com"
)

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   🧪 TEST DES HEADERS CORS" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Backend: $BackendUrl" -ForegroundColor Yellow
Write-Host "📍 Origin:  $Origin" -ForegroundColor Yellow
Write-Host ""

# Test 1: Requête OPTIONS (preflight)
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "TEST 1: Requête OPTIONS (preflight)" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

try {
    $headers = @{
        "Origin" = $Origin
        "Access-Control-Request-Method" = "GET"
        "Access-Control-Request-Headers" = "Content-Type"
    }
    
    $response = Invoke-WebRequest -Uri "$BackendUrl/health" -Method OPTIONS -Headers $headers -UseBasicParsing -ErrorAction Stop
    
    Write-Host "✅ Requête OPTIONS réussie (Code: $($response.StatusCode))" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Headers de la réponse :" -ForegroundColor Cyan
    Write-Host ""
    
    $corsHeaders = @(
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Credentials",
        "Access-Control-Max-Age"
    )
    
    $foundHeaders = 0
    foreach ($headerName in $corsHeaders) {
        if ($response.Headers.ContainsKey($headerName)) {
            $headerValue = $response.Headers[$headerName]
            Write-Host "   ✅ $headerName : $headerValue" -ForegroundColor Green
            $foundHeaders++
        } else {
            Write-Host "   ❌ $headerName : MANQUANT" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    if ($foundHeaders -eq $corsHeaders.Count) {
        Write-Host "✅ Tous les headers CORS sont présents !" -ForegroundColor Green
    } else {
        Write-Host "❌ Certains headers CORS sont manquants ($foundHeaders/$($corsHeaders.Count))" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Erreur lors de la requête OPTIONS:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        Write-Host ""
        Write-Host "   Code HTTP: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "TEST 2: Requête GET normale" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

try {
    $headers = @{
        "Origin" = $Origin
    }
    
    $response = Invoke-WebRequest -Uri "$BackendUrl/health" -Method GET -Headers $headers -UseBasicParsing -ErrorAction Stop
    
    Write-Host "✅ Requête GET réussie (Code: $($response.StatusCode))" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Headers CORS de la réponse :" -ForegroundColor Cyan
    Write-Host ""
    
    $corsHeaders = @(
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Credentials"
    )
    
    $foundHeaders = 0
    foreach ($headerName in $corsHeaders) {
        if ($response.Headers.ContainsKey($headerName)) {
            $headerValue = $response.Headers[$headerName]
            Write-Host "   ✅ $headerName : $headerValue" -ForegroundColor Green
            $foundHeaders++
        } else {
            Write-Host "   ❌ $headerName : MANQUANT" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "📄 Contenu de la réponse (premiers 200 caractères) :" -ForegroundColor Cyan
    $content = $response.Content
    if ($content.Length -gt 200) {
        Write-Host "   $($content.Substring(0, 200))..." -ForegroundColor Gray
    } else {
        Write-Host "   $content" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "❌ Erreur lors de la requête GET:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        Write-Host ""
        Write-Host "   Code HTTP: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   📊 RÉSUMÉ" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Si les headers CORS sont manquants :" -ForegroundColor Yellow
Write-Host "   → Le backend n'a pas été redéployé avec les changements CORS" -ForegroundColor Gray
Write-Host "   → OU il y a une erreur dans la configuration CORS" -ForegroundColor Gray
Write-Host ""
Write-Host "Si les headers CORS sont présents :" -ForegroundColor Yellow
Write-Host "   → Le problème CORS devrait être résolu !" -ForegroundColor Green
Write-Host "   → Vérifiez que le frontend peut maintenant se connecter" -ForegroundColor Gray
Write-Host ""

