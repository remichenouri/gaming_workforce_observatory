"""
Gaming Workforce Observatory Enterprise - Configuration centralisée
Optimisé pour entretien Ubisoft HR Data Analyst
"""
import os
from pathlib import Path

# Application Configuration
APP_NAME = "Gaming Workforce Observatory Enterprise"
VERSION = "2.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "gaming-workforce-secret-key-2025")

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
EXPORTS_DIR = BASE_DIR / "exports"

# Database Configuration
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "gaming_workforce"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "sslmode": os.getenv("DB_SSLMODE", "prefer")
}

# API Configuration
API_CONFIG = {
    "linkedin": {
        "client_id": os.getenv("LINKEDIN_CLIENT_ID"),
        "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET"),
        "base_url": "https://api.linkedin.com/v2",
        "rate_limit": 500  # requests per hour
    },
    "glassdoor": {
        "api_key": os.getenv("GLASSDOOR_API_KEY"),
        "base_url": "https://api.glassdoor.com/api/api.htm",
        "rate_limit": 1000  # requests per day
    },
    "indeed": {
        "publisher_id": os.getenv("INDEED_PUBLISHER_ID"),
        "base_url": "https://api.indeed.com/ads/apisearch",
        "rate_limit": 3600  # requests per hour
    }
}

# Cache Configuration
CACHE_CONFIG = {
    "default_ttl": 3600,  # 1 hour
    "ml_models_ttl": 86400,  # 24 hours
    "api_data_ttl": 1800,  # 30 minutes
    "user_session_ttl": 28800  # 8 hours
}

# ML Configuration
ML_CONFIG = {
    "model_versions": {
        "attrition_predictor": "v2.1.0",
        "salary_recommender": "v1.8.0",
        "team_clusterer": "v1.5.0",
        "sentiment_analyzer": "v2.0.0"
    },
    "performance_thresholds": {
        "accuracy_min": 0.85,
        "precision_min": 0.80,
        "recall_min": 0.75,
        "f1_score_min": 0.80
    },
    "training_schedule": "0 2 * * 0",  # Weekly Sunday 2 AM
    "batch_size": 1000,
    "max_training_time": 7200  # 2 hours
}

# Gaming Industry Constants
GAMING_CONFIG = {
    "major_studios": [
        "Microsoft Gaming", "Ubisoft", "Electronic Arts", "Sony Interactive",
        "Take-Two Interactive", "Embracer Group", "Nintendo", "Nexon",
        "NetEase Games", "Epic Games", "Activision Blizzard"
    ],
    "departments": [
        "Programming", "Art & Animation", "Game Design", "Quality Assurance",
        "Marketing", "Management", "Audio", "Technical Art", "Production"
    ],
    "experience_levels": ["Intern", "Junior", "Mid", "Senior", "Lead", "Principal"],
    "regions": ["North America", "Europe", "Asia-Pacific", "Latin America"],
    "salary_currencies": ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"]
}

# Notification Configuration
NOTIFICATION_CONFIG = {
    "email": {
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", 587)),
        "username": os.getenv("EMAIL_USERNAME"),
        "password": os.getenv("EMAIL_PASSWORD"),
        "from_address": os.getenv("FROM_EMAIL", "noreply@gaming-workforce.com")
    },
    "slack": {
        "webhook_url": os.getenv("SLACK_WEBHOOK_URL"),
        "channel": "#hr-analytics",
        "username": "Gaming Workforce Bot"
    }
}

# Security Configuration
SECURITY_CONFIG = {
    "session_timeout": 28800,  # 8 hours
    "max_login_attempts": 5,
    "password_min_length": 12,
    "require_2fa": True,
    "allowed_domains": ["ubisoft.com", "gaming-workforce.com"],
    "audit_retention_days": 365
}
UBISOFT_THEME = {
    'primary_color': '#6366f1',
    'background_color': '#ffffff',
    'secondary_background_color': '#f8fafc',
    'text_color': '#1e293b',
    'accent_color': '#ff6b35'
}

APP_CONFIG = {
    'app_name': 'Gaming Workforce Observatory',
    'version': '1.0.0',
    'debug': False,
    'max_upload_size': 200
}