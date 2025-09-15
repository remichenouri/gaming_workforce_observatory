"""
Ubisoft Premium Theme Configuration - Professional Light Version
"""

# Couleurs Ubisoft Corporate
UBISOFT_COLORS = {
    'primary': '#0099FF',
    'primary_dark': '#0066CC',
    'accent': '#E60012',
    'success': '#28A745',
    'warning': '#FFB020',
    'light': '#F8F9FA',
    'white': '#FFFFFF',
    'text': '#2C3E50'
}

def get_ubisoft_chart_config():
    """Configuration professionnelle des charts - SANS title par défaut"""
    return {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': '#FFFFFF',
            'font': {
                'family': 'Inter, sans-serif',
                'size': 12,
                'color': '#2C3E50'
            },
            'colorway': ['#0099FF', '#E60012', '#28A745', '#FFB020', '#9B59B6', '#17A2B8'],
            'margin': {'t': 60, 'b': 40, 'l': 60, 'r': 40},
            'xaxis': {
                'gridcolor': '#E9ECEF',
                'showgrid': True,
                'color': '#6C757D'
            },
            'yaxis': {
                'gridcolor': '#E9ECEF',
                'showgrid': True,
                'color': '#6C757D'
            }
        }
    }

# Fonction pour corriger les imports manquants
def create_ubisoft_header(title, subtitle=None):
    return f"""
    <h1>{title}</h1>
    {f'<p>{subtitle}</p>' if subtitle else ''}
    """

def create_ubisoft_breadcrumb(page):
    return f"🎮 Ubisoft Gaming Observatory → {page}"

def create_ubisoft_metric_cols(metrics):
    return metrics  # Placeholder

# Export pour compatibilité
__all__ = [
    'UBISOFT_COLORS', 
    'get_ubisoft_chart_config',
    'create_ubisoft_header',
    'create_ubisoft_breadcrumb',
    'create_ubisoft_metric_cols'
]
