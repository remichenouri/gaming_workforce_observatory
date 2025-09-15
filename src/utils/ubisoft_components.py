"""
🎮 Ubisoft UI Components Library
Composants réutilisables pour le Gaming Workforce Observatory Ubisoft
"""

import streamlit as st
import plotly.graph_objects as go
from src.themes.ubisoft_premium import UBISOFT_COLORS, UBISOFT_CHART_THEME

def create_ubisoft_kpi_card(title: str, value: str, delta: str = None, icon: str = "📊"):
    """Crée une KPI card stylée Ubisoft"""
    delta_html = f'<div class="ubisoft-kpi-delta">{delta}</div>' if delta else ''
    
    return f"""
    <div class="ubisoft-kpi-card">
        <div style="font-size: 3rem; margin-bottom: 20px; color: {UBISOFT_COLORS['primary']};">{icon}</div>
        <div class="ubisoft-kpi-value">{value}</div>
        <div class="ubisoft-kpi-title">{title}</div>
        {delta_html}
    </div>
    """

def create_ubisoft_breadcrumb(current_page: str):
    """Crée la navigation breadcrumb Ubisoft"""
    return f"""
    <div class="ubisoft-breadcrumb">
        <span class="ubisoft-breadcrumb-text">
            🎮 UBISOFT Gaming Workforce Observatory → {current_page}
        </span>
    </div>
    """

def create_ubisoft_header(title: str, subtitle: str = None):
    """Crée un header de page Ubisoft"""
    subtitle_html = f'<div style="font-size: 1.5rem; color: {UBISOFT_COLORS["text_primary"]}; margin-top: 20px; font-weight: 400;">{subtitle}</div>' if subtitle else ''
    
    return f"""
    <div class="ubisoft-mega-title">
        🎮 {title}
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title: str):
    """Crée un header de section Ubisoft"""
    return f"""
    <div class="ubisoft-section-header">
        {title}
    </div>
    """

def create_ubisoft_info_box(title: str, content: str):
    """Crée une info box Ubisoft"""
    return f"""
    <div class="ubisoft-info-box">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """

def create_ubisoft_accent_box(title: str, content: str):
    """Crée une accent box Ubisoft rouge"""
    return f"""
    <div class="ubisoft-accent-box">
        <h5>{title}</h5>
        <p style="color: {UBISOFT_COLORS['text_primary']}; font-size: 0.9rem; margin: 10px 0 0 0;">{content}</p>
    </div>
    """

def create_ubisoft_stats_grid(stats_list):
    """Crée une grille de statistiques Ubisoft"""
    cards_html = ""
    for stat in stats_list:
        cards_html += f"""
        <div class="ubisoft-ultra-card">
            <h5 style="color: {UBISOFT_COLORS['primary']}; margin-bottom: 15px;">{stat['title']}</h5>
            <div style="font-size: 2rem; color: {UBISOFT_COLORS['accent']}; font-weight: 700; margin-bottom: 10px;">
                {stat['value']}
            </div>
            <p style="color: {UBISOFT_COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">
                {stat.get('description', '')}
            </p>
        </div>
        """
    
    return f"""
    <div class="ubisoft-stats-grid">
        {cards_html}
    </div>
    """

def get_ubisoft_chart_config():
    """Retourne la configuration des charts Ubisoft"""
    return UBISOFT_CHART_THEME

def create_ubisoft_metric_cols(metrics_data, cols=4):
    """Crée des colonnes de métriques Ubisoft"""
    cols_st = st.columns(cols)
    
    for i, metric in enumerate(metrics_data):
        with cols_st[i % cols]:
            st.markdown(
                create_ubisoft_kpi_card(
                    metric['title'],
                    metric['value'],
                    metric.get('delta'),
                    metric.get('icon', '📊')
                ),
                unsafe_allow_html=True
            )

def display_ubisoft_logo_section():
    """Affiche la section logo Ubisoft subtile"""
    return f"""
    <div style="text-align: center; margin: 60px 0 40px 0; opacity: 0.7;">
        <div style="font-size: 1.8rem; color: {UBISOFT_COLORS['primary']}; font-weight: 300;">
            🎮 Powered by Ubisoft Gaming Excellence
        </div>
        <div style="font-size: 0.9rem; color: {UBISOFT_COLORS['text_secondary']}; margin-top: 10px;">
            Workforce Analytics • Gaming Industry Leaders
        </div>
    </div>
    """