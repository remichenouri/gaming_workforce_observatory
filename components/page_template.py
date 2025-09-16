# components/page_template.py
"""
Page Template Réutilisable pour Gaming Workforce Observatory
"""

import streamlit as st
from datetime import datetime
from config.app_config import get_current_timestamp, GAMING_THEME

# ===============================
# 🎮 Templates de Page
# ===============================

def create_page_header(title: str, subtitle: str = None):
    """
    Crée un header standardisé pour chaque page.

    Args:
        title (str): Titre de la page incluant l'icône.
        subtitle (str, optional): Sous-titre ou description courte.
    """
    current_time = get_current_timestamp()
    
    st.markdown(f"""
    <div class="gaming-header">
        <h1>{title}</h1>
        <p><strong>Gaming Workforce Observatory Enterprise</strong>
        {f"| {subtitle}" if subtitle else ''}</p>
        <p>Dernière mise à jour: {current_time} | Données: Live</p>
    </div>
    """, unsafe_allow_html=True)


def create_sidebar_filters():
    """
    Crée des filtres standardisés dans la sidebar.

    Returns:
        dict: Valeurs sélectionnées pour date_range, departments, locations
    """
    with st.sidebar:
        st.markdown("### 🔍 Filtres")
        
        # Filtre plage de dates
        date_range = st.date_input(
            "Période", 
            value=[datetime.now().date(), datetime.now().date()],
            help="Sélectionnez la période d'analyse"
        )
        
        # Filtre département
        departments = st.multiselect(
            "Départements", 
            options=list(GAMING_THEME.keys()),  # Remplacer par vos listes
            default=[]
        )
        
        # Filtre localisation
        locations = st.multiselect(
            "Localisations", 
            options=[
                'Montreal', 'Paris', 'Tokyo', 'Stockholm', 'Seoul',
                'San Francisco', 'London', 'Berlin', 'Vancouver', 'Austin'
            ],
            default=[]
        )
        
        st.markdown("---")
    
    return {
        'date_range': date_range,
        'departments': departments,
        'locations': locations
    }


def create_metrics_row(metrics: list):
    """
    Affiche une rangée de metrics avec cartes.

    Args:
        metrics (list): Liste de tuples (label, value, delta, color)
    """
    cols = st.columns(len(metrics))
    for idx, (label, value, delta, color) in enumerate(metrics):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid {color};">
                <h3 style="margin:0; font-size:1rem; font-weight:600;">{label}</h3>
                <p style="margin:0; font-size:1.8rem; font-weight:700; color:{color};">{value}</p>
                <p style="margin:0; font-size:0.9rem; color:grey;">{delta}</p>
            </div>
            """, unsafe_allow_html=True)
