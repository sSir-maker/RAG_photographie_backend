# ⚡ COMMANDE RAPIDE - Copiez-collez cette commande directement !

$body = @{email="adedayoade993@gmail.com";password="Nassir"} | ConvertTo-Json
Invoke-RestMethod -Uri "https://rag-photographie-backend.onrender.com/auth/login" -Method POST -Body $body -ContentType "application/json"

