"""
🎮 Ubisoft UI Components Library - CORRIGÉ ET COMPLET
Composants réutilisables pour Gaming Workforce Observatory Ubisoft
"""

import streamlit as st
import plotly.graph_objects as go

# Import sécurisé avec fallback
try:
    from src.themes.ubisoft_premium import UBISOFT_COLORS, UBISOFT_CHART_THEME
except ImportError:
    # Fallback si import échoue
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
    
    UBISOFT_CHART_THEME = {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': '#FFFFFF',
            'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': '#2C3E50'},
            'colorway': ['#0099FF', '#E60012', '#28A745', '#FFB020'],
            'margin': {'t': 60, 'b': 40, 'l': 60, 'r': 40}
        }
    }

def create_ubisoft_kpi_card(title: str, value: str, delta: str = None, icon: str = "📊"):
    """Crée une KPI card stylée Ubisoft"""
    delta_html = f'<p style="font-size: 0.9rem; color: #28A745; margin: 0;">{delta}</p>' if delta else ''
    
    return f"""
    <div class="ubisoft-kpi-card">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
            <h3 style="margin: 0; color: #2C3E50; font-size: 1rem;">{title}</h3>
        </div>
        <h2 style="margin: 0.5rem 0; color: #0099FF; font-size: 1.8rem;">{value}</h2>
        {delta_html}
    </div>
    """

def create_ubisoft_breadcrumb(current_page: str):
    """Crée la navigation breadcrumb Ubisoft"""
    return f"""
    <div class="ubisoft-breadcrumb">
        🎮 <strong>Ubisoft Gaming Workforce Observatory</strong> → {current_page}
    </div>
    """

def create_ubisoft_header(title: str, subtitle: str = None):
    """Crée un header de page Ubisoft"""
    subtitle_html = f'<p style="font-size: 1.1rem; color: #6C757D; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ''
    
    return f"""
    <div class="main-header">
        <h1 style="color: #0099FF; margin: 0; font-size: 2.2rem;">{title}</h1>
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title: str):
    """Crée un header de section Ubisoft"""
    return f"""
    <div class="ubisoft-section-header">
        <h3 style="margin: 0; color: #2C3E50;">{title}</h3>
    </div>
    """

def create_ubisoft_info_box(title: str, content: str):
    """Crée une info box Ubisoft"""
    return f"""
    <div class="ubisoft-info-box">
        <h4 style="color: #0099FF; margin-bottom: 0.5rem;">{title}</h4>
        <p style="margin: 0; color: #2C3E50;">{content}</p>
    </div>
    """

def create_ubisoft_accent_box(title: str, content: str):
    """Crée une accent box Ubisoft rouge"""
    return f"""
    <div class="ubisoft-accent-box">
        <h5 style="color: #E60012; margin-bottom: 0.5rem;">{title}</h5>
        <p style="margin: 0; color: #2C3E50;">{content}</p>
    </div>
    """

def create_ubisoft_stats_grid(stats_list):
    """Crée une grille de statistiques Ubisoft"""
    cards_html = ""
    for stat in stats_list:
        cards_html += f"""
        <div class="ubisoft-kpi-card">
            <h5 style="color: #0099FF; margin-bottom: 0.5rem;">{stat['title']}</h5>
            <h2 style="color: #2C3E50; margin: 0.5rem 0; font-size: 1.8rem;">{stat['value']}</h2>
            <p style="margin: 0; color: #6C757D; font-size: 0.9rem;">{stat.get('description', '')}</p>
        </div>
        """
    
    return f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 1rem 0;">
        {cards_html}
    </div>
    """

def get_ubisoft_chart_config():
    """Retourne la configuration des charts Ubisoft"""
    return UBISOFT_CHART_THEME

def create_ubisoft_metric_cols(metrics_data, cols=4):
    """Crée des colonnes de métriques Ubisoft"""
    if not metrics_data:
        return
        
    cols_st = st.columns(cols)
    
    for i, metric in enumerate(metrics_data):
        with cols_st[i % cols]:
            st.markdown(
                create_ubisoft_kpi_card(
                    metric.get('title', 'Metric'),
                    metric.get('value', '0'),
                    metric.get('delta'),
                    metric.get('icon', '📊')
                ),
                unsafe_allow_html=True
            )

def display_ubisoft_logo_section():
    """Affiche la section logo Ubisoft subtile"""
    return f"""
    <div style="text-align: center; padding: 2rem; margin-top: 3rem; background: linear-gradient(135deg, {UBISOFT_COLORS['light']}, {UBISOFT_COLORS['white']}); border-radius: 8px;">
        <h4 style="color: {UBISOFT_COLORS['primary']}; margin-bottom: 0.5rem;">🎮 Powered by Ubisoft Gaming Excellence</h4>
        <p style="color: {UBISOFT_COLORS['text']}; margin: 0; font-size: 0.9rem;">
            Advanced Workforce Analytics • Gaming Industry Leadership • © 2024 Ubisoft Entertainment
        </p>
    </div>
    """

def apply_ubisoft_theme():
    """Application du thème Ubisoft - fonction de compatibilité"""
    st.markdown("""
    <style>
    /* Ubisoft Gaming Theme Enterprise */
    .main-header {
        background: linear-gradient(135deg, #0099FF15, #E6001210);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border-left: 4px solid #0099FF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .ubisoft-kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 4px solid #0099FF;
        margin: 0.5rem 0;
        transition: transform 0.2s ease;
    }
    
    .ubisoft-kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .ubisoft-info-box {
        background: linear-gradient(135deg, #28A74515, #0099FF10);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #28A74530;
    }
    
    .ubisoft-accent-box {
        background: linear-gradient(135deg, #E6001215, #fff);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #E60012;
    }
    
    .ubisoft-breadcrumb {
        background: #F8F9FA;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #6C757D;
    }
    
    .ubisoft-section-header {
        background: linear-gradient(135deg, #0099FF15, transparent);
        padding: 1rem;
        border-radius: 8px;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #0099FF;
    }
    </style>
    """, unsafe_allow_html=True)

# Classes pour compatibilité étendue
class GamingThemes:
    """Classe themes gaming pour compatibilité"""
    
    @staticmethod
    def get_colors():
        return UBISOFT_COLORS
    
    @staticmethod
    def get_chart_config():
        return UBISOFT_CHART_THEME

# Export pour compatibilité
__all__ = [
    'create_ubisoft_kpi_card',
    'create_ubisoft_breadcrumb', 
    'create_ubisoft_header',
    'create_ubisoft_section_header',
    'create_ubisoft_info_box',
    'create_ubisoft_accent_box',
    'create_ubisoft_stats_grid',
    'get_ubisoft_chart_config',
    'create_ubisoft_metric_cols',
    'display_ubisoft_logo_section',
    'apply_ubisoft_theme',
    'UBISOFT_COLORS',
    'UBISOFT_CHART_THEME',
    'GamingThemes'
]
