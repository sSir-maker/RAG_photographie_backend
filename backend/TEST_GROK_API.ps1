# Script de test pour vérifier la connexion à l'API Grok (X.AI)
# Utilisez ce script pour tester votre clé API Grok

param(
    [Parameter(Mandatory=$false)]
    [string]$ApiKey = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Model = "grok-4-latest"
)

# Si la clé API n'est pas fournie en paramètre, essayer depuis les variables d'environnement
if ([string]::IsNullOrEmpty($ApiKey)) {
    $ApiKey = $env:GROK_API_KEY
    if ([string]::IsNullOrEmpty($ApiKey)) {
        $ApiKey = $env:XAI_API_KEY
    }
}

if ([string]::IsNullOrEmpty($ApiKey)) {
    Write-Host "❌ Erreur: Clé API non trouvée" -ForegroundColor Red
    Write-Host ""
    Write-Host "Configurez votre clé API avec l'une des options suivantes:" -ForegroundColor Yellow
    Write-Host "  - Passer en paramètre: .\TEST_GROK_API.ps1 -ApiKey 'xai-votre-cle-ici'" -ForegroundColor Cyan
    Write-Host "  - Variable d'environnement: `$env:GROK_API_KEY='xai-votre-cle-ici'" -ForegroundColor Cyan
    exit 1
}

$BaseUrl = "https://api.x.ai/v1"
$Endpoint = "$BaseUrl/chat/completions"

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   🧪 TEST CONNEXION API GROK (X.AI)" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Base URL: $BaseUrl" -ForegroundColor Yellow
Write-Host "📍 Endpoint: $Endpoint" -ForegroundColor Yellow
Write-Host "🤖 Modèle: $Model" -ForegroundColor Yellow
Write-Host ""

$body = @{
    messages = @(
        @{
            role = "system"
            content = "You are a helpful assistant."
        },
        @{
            role = "user"
            content = "Say 'Hello from Grok!' and nothing else."
        }
    )
    model = $Model
    stream = $false
    temperature = 0
} | ConvertTo-Json -Depth 10

try {
    Write-Host "🔄 Envoi de la requête..." -ForegroundColor Yellow
    
    $response = Invoke-RestMethod -Uri $Endpoint -Method POST -Body $body -ContentType "application/json" -Headers @{
        "Authorization" = "Bearer $ApiKey"
    }
    
    Write-Host ""
    Write-Host "✅ SUCCÈS ! Connexion à Grok établie." -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Réponse de Grok:" -ForegroundColor Cyan
    Write-Host "   $($response.choices[0].message.content)" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Informations de la réponse:" -ForegroundColor Cyan
    Write-Host "   Modèle utilisé: $($response.model)" -ForegroundColor White
    Write-Host "   Tokens utilisés: $($response.usage.total_tokens)" -ForegroundColor White
    Write-Host ""
    
    # Afficher aussi le base_url à utiliser
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Green
    Write-Host "   ✅ CONFIGURATION RECOMMANDÉE" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ajoutez ces variables dans votre fichier .env :" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "GROK_API_KEY=$ApiKey" -ForegroundColor Cyan
    Write-Host "GROK_MODEL=$Model" -ForegroundColor Cyan
    Write-Host "GROK_BASE_URL=$BaseUrl" -ForegroundColor Cyan
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ ERREUR lors de la connexion à Grok" -ForegroundColor Red
    Write-Host ""
    Write-Host "Détails de l'erreur:" -ForegroundColor Yellow
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $reader.DiscardBufferedData()
        $responseBody = $reader.ReadToEnd()
        
        Write-Host "   Code HTTP: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host "   Message: $responseBody" -ForegroundColor Red
        
        if ($_.Exception.Response.StatusCode.value__ -eq 401) {
            Write-Host ""
            Write-Host "💡 Vérifiez que votre clé API est valide." -ForegroundColor Yellow
        }
    } else {
        Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    exit 1
}

