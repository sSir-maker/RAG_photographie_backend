# 🚀 Démarrer Phoenix Dashboard

## Commande principale

```bash
phoenix serve --port 6006
```

## Alternative (si la commande `phoenix` n'est pas reconnue)

```bash
python -m phoenix.server.main serve --port 6006
```

## Vérification

Une fois démarré, le dashboard sera accessible sur :
- **http://localhost:6006**

## Options disponibles

```bash
# Port personnalisé
phoenix serve --port 8000

# Aide
phoenix serve --help
```

## Arrêter Phoenix

Appuyez sur `Ctrl+C` dans le terminal où Phoenix est lancé.

## Note

Phoenix doit être démarré **avant** de lancer l'API pour que le monitoring fonctionne correctement.

