# config/app_config.py
"""
🎮 Gaming Workforce Observatory Enterprise - Configuration Centralisée
Version 2.0 - Configuration application sophistiquée
"""

import streamlit as st
from datetime import datetime

# ===============================
# 🎯 CONFIGURATION GAMING THEME
# ===============================

GAMING_THEME = {
    'primary': '#0066CC',       # Bleu gaming corporate
    'accent': '#FF6B35',        # Orange gaming dynamique
    'success': '#28A745',       # Vert performance
    'warning': '#FFB020',       # Orange attention
    'danger': '#DC3545',        # Rouge critique
    'background': '#F8F9FA',    # Fond clair professionnel
    'text': '#2C3E50',         # Texte sombre lisible
    'secondary': '#6C757D',     # Gris secondaire
    'light': '#F8F9FA',        # Gris clair
    'dark': '#343A40'           # Gris foncé
}

GAMING_COLOR_PALETTE = [
    GAMING_THEME['primary'],    # Bleu gaming
    GAMING_THEME['accent'],     # Orange gaming
    GAMING_THEME['success'],    # Vert performance
    '#9B59B6',                  # Violet créativité
    '#E74C3C',                  # Rouge alerte
    '#F39C12',                  # Orange warning
    '#1ABC9C',                  # Turquoise innovation
    '#34495E'                   # Gris corporate
]

# ===============================
# 🚀 CONFIGURATION APPLICATION
# ===============================

APP_CONFIG = {
    'app_name': 'Gaming Workforce Observatory Enterprise',
    'app_version': '2.0',
    'app_description': 'Advanced gaming analytics powered by AI',
    'page_title': '🎮 Gaming Workforce Observatory Enterprise',
    'page_icon': '🎮',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'author': 'remichenouri',
    'github_url': 'https://github.com/remichenouri/gaming_workforce_observatory',
    'contact_email': 'remi.chenouri@gaming-workforce-observatory.com',
    'company': 'Gaming Workforce Analytics Inc.',
    'copyright_year': '2024'
}

# ===============================
# 🎮 CONFIGURATION GAMING SPECIFIQUE
# ===============================

GAMING_DEPARTMENTS = [
    'Programming', 'Art & Animation', 'Game Design', 'Quality Assurance', 
    'Production', 'Audio', 'Marketing', 'Business Development'
]

GAMING_LEVELS = ['Junior', 'Mid', 'Senior', 'Lead', 'Director']

GAMING_LOCATIONS = [
    'Montreal', 'Paris', 'Tokyo', 'Stockholm', 'Seoul', 
    'San Francisco', 'London', 'Berlin', 'Vancouver', 'Austin'
]

GAMING_PROJECT_TYPES = [
    'AAA Game', 'Indie Game', 'Mobile Game', 'VR Experience', 
    'AR Game', 'Game Engine', 'Gaming Tools', 'Esports Platform'
]

GAMING_DEVELOPMENT_PHASES = [
    'Pre-production', 'Production', 'Alpha', 'Beta', 'Gold Master', 'Live Operations'
]

# ===============================
# 📊 CONFIGURATION KPIs GAMING
# ===============================

GAMING_KPI_CATEGORIES = {
    'performance': {
        'name': '⭐ Performance Gaming',
        'icon': '⭐',
        'color': GAMING_THEME['success']
    },
    'satisfaction': {
        'name': '😊 Satisfaction Gaming',
        'icon': '😊',
        'color': GAMING_THEME['primary']
    },
    'retention': {
        'name': '🎯 Retention Gaming',
        'icon': '🎯',
        'color': GAMING_THEME['accent']
    },
    'innovation': {
        'name': '🚀 Innovation Gaming',
        'icon': '🚀',
        'color': '#9B59B6'
    },
    'collaboration': {
        'name': '🤝 Collaboration Gaming',
        'icon': '🤝',
        'color': '#1ABC9C'
    }
}

GAMING_KPI_TARGETS = {
    'satisfaction_score': {'min': 7.5, 'target': 8.5, 'max': 10.0},
    'performance_score': {'min': 3.5, 'target': 4.2, 'max': 5.0},
    'retention_rate': {'min': 80, 'target': 87, 'max': 95},
    'innovation_index': {'min': 70, 'target': 80, 'max': 100},
    'sprint_velocity': {'min': 30, 'target': 38, 'max': 50},
    'burnout_risk': {'min': 0.0, 'target': 0.2, 'max': 0.4}
}

# ===============================
# 🤖 CONFIGURATION ML/AI
# ===============================

ML_MODELS_CONFIG = {
    'turnover_predictor': {
        'name': 'Turnover Predictor',
        'accuracy': 89.3,
        'model_type': 'RandomForest',
        'features': ['satisfaction_score', 'performance_score', 'salary', 'retention_risk']
    },
    'burnout_detector': {
        'name': 'Burnout Detection',
        'accuracy': 87.8,
        'model_type': 'GradientBoosting',
        'features': ['sprint_velocity', 'overtime_hours', 'project_pressure']
    },
    'performance_forecaster': {
        'name': 'Performance Forecaster',
        'accuracy': 84.2,
        'model_type': 'LSTM',
        'features': ['historical_performance', 'team_synergy', 'project_complexity']
    },
    'talent_matcher': {
        'name': 'Talent Matcher',
        'accuracy': 91.5,
        'model_type': 'NeuralNetwork',
        'features': ['skills', 'experience', 'personality', 'gaming_preferences']
    }
}

# ===============================
# 🏢 CONFIGURATION UI/UX
# ===============================

UI_SETTINGS = {
    'chart_height': 400,
    'chart_width': 800,
    'sidebar_width': 300,
    'animation_duration': 500,
    'refresh_interval': 30,  # secondes
    'items_per_page': 25,
    'max_file_size': 200,    # MB
    'supported_formats': ['.csv', '.xlsx', '.json'],
    'date_format': '%Y-%m-%d',
    'time_format': '%H:%M:%S',
    'datetime_format': '%Y-%m-%d %H:%M:%S'
}

RESPONSIVE_BREAKPOINTS = {
    'mobile': 768,
    'tablet': 1024,
    'desktop': 1440,
    'large_desktop': 1920
}

# ===============================
# 🔐 CONFIGURATION SECURITY
# ===============================

SECURITY_CONFIG = {
    'session_timeout': 3600,           # 1 heure
    'max_login_attempts': 3,
    'password_min_length': 8,
    'require_2fa': False,
    'allowed_domains': ['company.com', 'gaming-company.com'],
    'encryption_key_length': 256,
    'audit_log_retention': 90          # jours
}

USER_ROLES = {
    'viewer': {
        'name': 'Viewer',
        'permissions': ['read'],
        'pages': ['Executive Dashboard', 'Global Studios', 'Future Insights']
    },
    'analyst': {
        'name': 'Analyst',
        'permissions': ['read', 'analyze'],
        'pages': ['Executive Dashboard', 'Talent Wars', 'Neurodiversity ROI', 
                 'Predictive Analytics', 'Global Studios', 'Compensation Intel', 'Future Insights']
    },
    'admin': {
        'name': 'Administrator',
        'permissions': ['read', 'write', 'admin'],
        'pages': 'all'
    }
}

# ===============================
# 📱 CONFIGURATION PAGES
# ===============================

PAGES_CONFIG = {
    'Executive Dashboard': {
        'title': '🏠 Executive Dashboard',
        'icon': '🏠',
        'description': 'C-suite gaming analytics overview',
        'file': '01_🏠_Executive_Dashboard.py',
        'order': 1,
        'default': True
    },
    'Talent Wars': {
        'title': '⚔️ Talent Wars',
        'icon': '⚔️',
        'description': 'Gaming vs Tech talent battle analysis',
        'file': '02_⚔️_Talent_Wars.py',
        'order': 2
    },
    'Neurodiversity ROI': {
        'title': '🧠 Neurodiversity ROI',
        'icon': '🧠',
        'description': 'Cognitive diversity impact measurement',
        'file': '03_🧠_Neurodiversity_ROI.py',
        'order': 3
    },
    'Predictive Analytics': {
        'title': '🎯 Predictive Analytics',
        'icon': '🎯',
        'description': 'AI/ML workforce predictions',
        'file': '04_🎯_Predictive_Analytics.py',
        'order': 4
    },
    'Global Studios': {
        'title': '🌍 Global Studios',
        'icon': '🌍',
        'description': 'Worldwide gaming operations',
        'file': '05_🌍_Global_Studios.py',
        'order': 5
    },
    'Compensation Intel': {
        'title': '💰 Compensation Intel',
        'icon': '💰',
        'description': 'Gaming salary benchmarking',
        'file': '06_💰_Compensation_Intel.py',
        'order': 6
    },
    'Future Insights': {
        'title': '🔮 Future Insights',
        'icon': '🔮',
        'description': 'Gaming workforce forecasting',
        'file': '07_🔮_Future_Insights.py',
        'order': 7
    },
    'Admin Panel': {
        'title': '⚙️ Admin Panel',
        'icon': '⚙️',
        'description': 'System administration center',
        'file': '08_⚙️_Admin_Panel.py',
        'order': 8
    }
}

# ===============================
# 📊 CONFIGURATION DASHBOARD
# ===============================

DASHBOARD_METRICS = {
    'workforce_total': {
        'label': '👥 Total Workforce',
        'icon': '👥',
        'format': '{:,}',
        'delta_format': '▲ +{} this month'
    },
    'avg_salary': {
        'label': '💰 Average Salary',
        'icon': '💰',
        'format': '${:,.0f}',
        'delta_format': '▲ +${:,} YoY'
    },
    'satisfaction': {
        'label': '😊 Satisfaction',
        'icon': '😊',
        'format': '{:.1f}/10',
        'delta_format': '▲ +{:.1f} this quarter'
    },
    'performance': {
        'label': '⭐ Performance',
        'icon': '⭐',
        'format': '{:.1f}/5',
        'delta_format': '▲ +{:.1f} this quarter'
    },
    'revenue_per_employee': {
        'label': '💼 Revenue/Employee',
        'icon': '💼',
        'format': '${:.0f}K',
        'delta_format': '▲ +{:.1f}% industry avg'
    }
}

# ===============================
# 🎮 FUNCTIONS UTILITAIRES
# ===============================

def setup_page_config():
    """Configuration page Streamlit centralisée"""
    st.set_page_config(
        page_title=APP_CONFIG['page_title'],
        page_icon=APP_CONFIG['page_icon'],
        layout=APP_CONFIG['layout'],
        initial_sidebar_state=APP_CONFIG['initial_sidebar_state'],
        menu_items={
            'Get Help': APP_CONFIG['github_url'],
            'Report a bug': f"{APP_CONFIG['github_url']}/issues",
            'About': f"{APP_CONFIG['app_name']} v{APP_CONFIG['app_version']} - Enterprise Edition"
        }
    )

def get_current_timestamp():
    """Timestamp actuel formaté"""
    return datetime.now().strftime(UI_SETTINGS['datetime_format'])

def get_gaming_theme():
    """Retourne le thème gaming complet"""
    return GAMING_THEME

def get_gaming_color_palette():
    """Retourne la palette de couleurs gaming"""
    return GAMING_COLOR_PALETTE

def format_metric_value(value, metric_type):
    """Formatage valeurs métriques selon le type"""
    if metric_type in DASHBOARD_METRICS:
        format_string = DASHBOARD_METRICS[metric_type]['format']
        if isinstance(value, (int, float)):
            return format_string.format(value)
    return str(value)

def get_kpi_target(kpi_name):
    """Retourne les targets pour un KPI gaming"""
    return GAMING_KPI_TARGETS.get(kpi_name, {'min': 0, 'target': 50, 'max': 100})

def is_user_authorized(user_role, page_name):
    """Vérifie l'autorisation utilisateur pour une page"""
    if user_role not in USER_ROLES:
        return False
    
    user_pages = USER_ROLES[user_role]['pages']
    
    if user_pages == 'all':
        return True
    
    return page_name in user_pages

def get_chart_config():
    """Configuration standard pour les graphiques"""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'white',
        'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': GAMING_THEME['text']},
        'colorway': GAMING_COLOR_PALETTE,
        'margin': {'t': 50, 'b': 40, 'l': 60, 'r': 40},
        'xaxis': {'gridcolor': '#E9ECEF', 'showgrid': True},
        'yaxis': {'gridcolor': '#E9ECEF', 'showgrid': True},
        'legend': {'orientation': 'h', 'yanchor': 'bottom', 'y': -0.2}
    }

# ===============================
# 🚀 CONFIGURATION PERFORMANCE
# ===============================

PERFORMANCE_CONFIG = {
    'cache_ttl': 300,              # 5 minutes
    'max_cache_entries': 100,
    'lazy_loading': True,
    'enable_compression': True,
    'chunk_size': 1000,
    'max_concurrent_requests': 10,
    'timeout_seconds': 30
}

# ===============================
# 📈 CONFIGURATION ANALYTICS
# ===============================

ANALYTICS_CONFIG = {
    'default_date_range': 30,      # jours
    'min_sample_size': 50,
    'confidence_level': 0.95,
    'significance_threshold': 0.05,
    'outlier_detection': True,
    'anomaly_threshold': 2.5,      # écarts-types
    'trend_window': 7,             # jours
    'seasonality_periods': [7, 30, 365]  # jours, semaine, mois, année
}

# ===============================
# 🎯 CONFIGURATION EXPORT
# ===============================

EXPORT_CONFIG = {
    'max_export_rows': 50000,
    'supported_formats': ['csv', 'xlsx', 'json', 'pdf'],
    'compression': True,
    'include_metadata': True,
    'date_in_filename': True,
    'author_watermark': True
}

# ===============================
# 🔄 VERSION & MISE À JOUR
# ===============================

VERSION_INFO = {
    'current_version': APP_CONFIG['app_version'],
    'release_date': '2024-09-16',
    'changelog': {
        '2.0': [
            'Navigation st.navigation() moderne',
            'Architecture modulaire enterprise',
            'Templates réutilisables',
            'CSS externalisé',
            '100+ KPIs gaming sophistiqués',
            'ML/AI models intégrés',
            'Thème gaming professionnel'
        ],
        '1.0': [
            'Version initiale',
            'Dashboard gaming basique',
            'Visualisations Plotly',
            'Authentification simple'
        ]
    }
}

# ===============================
# 🎮 GAMING INDUSTRY BENCHMARKS
# ===============================

INDUSTRY_BENCHMARKS = {
    'gaming_avg_salary': 87404,
    'gaming_satisfaction': 8.2,
    'gaming_retention': 87.3,
    'gaming_innovation': 74.5,
    'tech_avg_salary': 120000,
    'tech_satisfaction': 7.0,
    'tech_retention': 82.1,
    'tech_innovation': 68.2,
    'industry_growth': 12.3,
    'workforce_size': 2800000
}
