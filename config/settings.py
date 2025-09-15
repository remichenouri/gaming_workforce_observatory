"""
Gaming Workforce Observatory - Configuration Settings
Enterprise Edition - Gaming Industry Specialized Configuration
"""

import os
from typing import Dict, Any

# === GAMING THEME CONFIGURATION ===
GAMING_THEME = {
    # Primary Gaming Colors
    'primary': '#0066CC',        # Professional Gaming Blue
    'primary_dark': '#0052A3',   # Darker shade for hover states
    'accent': '#FF6B35',         # Gaming Orange for highlights
    'accent_light': '#FF8C61',   # Lighter accent for backgrounds
    
    # Status Colors
    'success': '#28A745',        # Green for positive metrics
    'warning': '#FFB020',        # Orange for attention needed
    'danger': '#DC3545',         # Red for critical alerts
    'info': '#17A2B8',          # Cyan for informational
    
    # Background Colors
    'background': '#F8F9FA',     # Light professional background
    'surface': '#FFFFFF',        # Card surfaces
    'surface_dark': '#F1F3F4',   # Darker surface variant
    
    # Text Colors
    'text': '#2C3E50',          # Primary text color
    'text_light': '#6C757D',    # Secondary text color
    'text_muted': '#ADB5BD',    # Muted text color
    
    # Gaming-Specific Colors
    'gaming_blue': '#0066CC',    # Gaming industry standard blue
    'gaming_orange': '#FF6B35',  # Gaming industry accent
    'gaming_purple': '#9B59B6',  # Creative/innovation color
    'gaming_green': '#28A745',   # Performance/success color
    'gaming_red': '#E74C3C',     # Alert/critical color
}

# === APPLICATION CONFIGURATION ===
APP_CONFIG = {
    'app_name': 'Gaming Workforce Observatory Enterprise',
    'version': '2.0.0',
    'description': 'Advanced Gaming Industry Workforce Analytics Platform',
    'author': 'remichenouri',
    'github_url': 'https://github.com/remichenouri/gaming_workforce_observatory',
    'contact_email': 'contact@gaming-workforce-observatory.com',
    
    # Performance Settings
    'cache_ttl': 300,  # 5 minutes cache
    'max_cache_entries': 1000,
    'chart_animation_duration': 500,
    'loading_timeout': 30,
    
    # Gaming Industry Specific
    'supported_gaming_roles': [
        'Game Developer', 'Game Designer', 'Technical Artist',
        'QA Tester', 'Audio Engineer', 'Game Producer',
        'Level Designer', '3D Artist', 'Animator',
        'UI/UX Designer', 'Community Manager', 'Data Analyst'
    ],
    
    'gaming_departments': [
        'Programming', 'Art & Animation', 'Game Design',
        'Quality Assurance', 'Production', 'Audio',
        'Marketing', 'Management', 'Operations'
    ],
    
    'gaming_platforms': [
        'PC', 'PlayStation', 'Xbox', 'Nintendo Switch',
        'Mobile (iOS/Android)', 'VR Headsets', 'Web Browser',
        'Arcade', 'Console (Generic)', 'Steam Deck'
    ],
    
    'project_phases': [
        'Concept', 'Pre-production', 'Production',
        'Alpha', 'Beta', 'Gold Master', 'Launch',
        'Live Operations', 'Post-Launch Support', 'Sunset'
    ]
}

# === DASHBOARD CONFIGURATION ===
DASHBOARD_CONFIG = {
    'pages': [
        {
            'name': 'Executive Dashboard',
            'icon': '🏠',
            'description': 'C-suite gaming analytics and KPIs',
            'access_level': 'executive'
        },
        {
            'name': 'Talent Wars',
            'icon': '⚔️',
            'description': 'Gaming vs Tech industry comparison',
            'access_level': 'manager'
        },
        {
            'name': 'Neurodiversity ROI',
            'icon': '🧠',
            'description': 'Cognitive diversity impact analysis',
            'access_level': 'hr'
        },
        {
            'name': 'Predictive Analytics',
            'icon': '🎯',
            'description': 'AI/ML workforce models and predictions',
            'access_level': 'analyst'
        },
        {
            'name': 'Global Studios',
            'icon': '🌍',
            'description': 'Worldwide gaming operations view',
            'access_level': 'manager'
        },
        {
            'name': 'Compensation Intel',
            'icon': '💰',
            'description': 'Gaming industry salary benchmarking',
            'access_level': 'hr'
        },
        {
            'name': 'Future Insights',
            'icon': '🔮',
            'description': 'Gaming workforce forecasting',
            'access_level': 'executive'
        },
        {
            'name': 'Admin Panel',
            'icon': '⚙️',
            'description': 'System administration and configuration',
            'access_level': 'admin'
        }
    ],
    
    'kpi_refresh_interval': 60,  # seconds
    'chart_default_height': 400,
    'table_page_size': 50,
    'export_formats': ['CSV', 'Excel', 'PDF', 'JSON']
}

# === GAMING INDUSTRY BENCHMARKS ===
GAMING_BENCHMARKS = {
    'salary_ranges': {
        'Junior': {'min': 35000, 'max': 65000, 'median': 50000},
        'Mid': {'min': 55000, 'max': 95000, 'median': 75000},
        'Senior': {'min': 80000, 'max': 140000, 'median': 110000},
        'Lead': {'min': 110000, 'max': 180000, 'median': 145000},
        'Director': {'min': 150000, 'max': 250000, 'median': 200000}
    },
    
    'satisfaction_targets': {
        'Gaming': 7.8,
        'Tech': 7.1,
        'Industry_Average': 6.9
    },
    
    'retention_targets': {
        'Gaming': 82.0,
        'Tech': 78.5,
        'Industry_Average': 75.2
    },
    
    'performance_metrics': {
        'sprint_velocity_target': 40,
        'bug_fix_rate_target': 85,
        'innovation_index_target': 75,
        'team_synergy_target': 8.0
    }
}

# === SECURITY CONFIGURATION ===
SECURITY_CONFIG = {
    'authentication_required': True,
    'session_timeout': 3600,  # 1 hour
    'max_login_attempts': 3,
    'password_min_length': 8,
    
    'access_levels': {
        'viewer': ['Executive Dashboard', 'Global Studios'],
        'analyst': ['Executive Dashboard', 'Global Studios', 'Predictive Analytics', 'Compensation Intel'],
        'manager': ['Executive Dashboard', 'Talent Wars', 'Global Studios', 'Predictive Analytics', 'Compensation Intel'],
        'hr': ['Executive Dashboard', 'Talent Wars', 'Neurodiversity ROI', 'Compensation Intel', 'Future Insights'],
        'executive': ['Executive Dashboard', 'Talent Wars', 'Neurodiversity ROI', 'Global Studios', 'Future Insights'],
        'admin': ['all']
    },
    
    'demo_users': {
        'admin': {'password': 'demo', 'level': 'admin'},
        'manager': {'password': 'gaming123', 'level': 'manager'},
        'analyst': {'password': 'data123', 'level': 'analyst'}
    }
}

# === PERFORMANCE CONFIGURATION ===
PERFORMANCE_CONFIG = {
    'targets': {
        'page_load_time': 2.0,      # seconds
        'chart_render_time': 0.5,   # seconds
        'filter_response_time': 0.1, # seconds
        'ml_prediction_time': 3.0,  # seconds
        'cache_hit_rate': 0.85      # 85%
    },
    
    'optimization': {
        'enable_caching': True,
        'cache_compression': True,
        'lazy_loading': True,
        'chart_streaming': False,
        'data_pagination': True
    }
}

# === ENVIRONMENT CONFIGURATION ===
def get_environment_config():
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'development')
    
    if env == 'production':
        return {
            'debug': False,
            'cache_ttl': 600,  # 10 minutes
            'logging_level': 'INFO',
            'enable_telemetry': True
        }
    elif env == 'staging':
        return {
            'debug': True,
            'cache_ttl': 300,  # 5 minutes
            'logging_level': 'DEBUG',
            'enable_telemetry': True
        }
    else:  # development
        return {
            'debug': True,
            'cache_ttl': 60,   # 1 minute
            'logging_level': 'DEBUG',
            'enable_telemetry': False
        }

# === EXPORT CONFIGURATION ===
def get_config() -> Dict[str, Any]:
    """Get complete configuration dictionary"""
    return {
        'theme': GAMING_THEME,
        'app': APP_CONFIG,
        'dashboard': DASHBOARD_CONFIG,
        'benchmarks': GAMING_BENCHMARKS,
        'security': SECURITY_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'environment': get_environment_config()
    }