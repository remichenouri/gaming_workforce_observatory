# Gaming Workforce Observatory - Production Dockerfile

FROM python:3.11-slim

# Métadonnées
LABEL maintainer="remi.chenouri@example.com"
LABEL description="Gaming Workforce Observatory - Streamlit Dashboard"
LABEL version="2.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Créer utilisateur non-root pour sécurité
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser

# Répertoire de travail
WORKDIR /app

# Copier requirements et installer dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code application
COPY . .

# Créer dossiers nécessaires
RUN mkdir -p data/processed && \
    mkdir -p assets && \
    mkdir -p .streamlit

# Permissions pour utilisateur app
RUN chown -R appuser:appuser /app
USER appuser

# Port Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Commande de démarrage
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
