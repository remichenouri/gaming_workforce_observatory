# Gaming Workforce Observatory - Makefile

.PHONY: help install dev run test lint format clean docker-build docker-run deploy

help: ## Afficher l'aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Installer les dépendances
	pip install -r requirements.txt

dev: ## Installer dépendances développement
	pip install pytest black flake8 mypy

run: ## Lancer l'application Streamlit
	streamlit run app.py

test: ## Lancer les tests
	pytest tests/ -v --cov=src

lint: ## Vérifier la qualité du code
	flake8 src/ tests/
	mypy src/ --ignore-missing-imports

format: ## Formater le code
	black src/ tests/ *.py
	isort src/ tests/ *.py

clean: ## Nettoyer les fichiers temporaires
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/

docker-build: ## Construire l'image Docker
	docker build -t gaming-workforce-observatory:latest .

docker-run: ## Lancer avec Docker
	docker run -p 8501:8501 gaming-workforce-observatory:latest

docker-compose-up: ## Lancer avec Docker Compose
	docker-compose up --build

deploy-streamlit: ## Déployer sur Streamlit Cloud
	@echo "Push vers GitHub et connecter à Streamlit Cloud"
	git add .
	git commit -m "Deploy: $(shell date)"
	git push origin main

setup-dev: install dev ## Setup environnement développement complet
	pre-commit install
	@echo "Environnement de développement prêt !"

check-quality: lint test ## Vérification qualité complète
	@echo "Qualité du code vérifiée !"
