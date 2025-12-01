.PHONY: help install test lint format clean docker-build docker-up docker-down deploy

help:
	@echo "Commandes disponibles:"
	@echo "  make install      - Installer les dépendances"
	@echo "  make test         - Exécuter les tests"
	@echo "  make lint         - Vérifier le code (sans modification)"
	@echo "  make format       - Formater le code"
	@echo "  make clean        - Nettoyer les fichiers temporaires"
	@echo "  make docker-build - Construire les images Docker"
	@echo "  make docker-up    - Démarrer les services Docker"
	@echo "  make docker-down  - Arrêter les services Docker"
	@echo "  make deploy       - Déployer en production"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=app --cov-report=html

lint:
	python scripts/lint_code.py

format:
	python scripts/format_code.py

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	rm -rf htmlcov/ .coverage coverage.xml

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

deploy:
	@echo "Déploiement via GitHub Actions..."
	@echo "Push sur main pour déclencher le déploiement automatique"

