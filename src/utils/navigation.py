
import streamlit as st

def setup_navigation():
    """Configure la navigation et l'état global de l'application"""

    # Initialisation des états de session si nécessaire
    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = True
        st.session_state.current_filters = {}
        st.session_state.data_last_updated = None

    # Configuration de la sidebar avec navigation
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; margin-bottom: 1rem; color: white;">
        <h3>🎮 Observatory</h3>
        <p style="margin: 0; opacity: 0.9;">Gaming Workforce Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    # Menu navigation principal
    st.sidebar.markdown("### 🧭 Navigation")

    # Status de l'application
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Status Application")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.sidebar.markdown("**🔄 Données:**")
        st.sidebar.success("✅ Sync")

    with col2:
        st.sidebar.markdown("**⚡ Performance:**")
        st.sidebar.success("✅ Optimal")

    # Liens utiles
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔗 Liens Utiles")

    st.sidebar.markdown("""
    - 📚 [Documentation](https://docs.gaming-workforce.com)
    - 🐛 [Signaler un Bug](https://github.com/remichenouri/gaming-workforce-observatory/issues)
    - 💬 [Support](mailto:support@gaming-workforce.com)
    - ⭐ [GitHub](https://github.com/remichenouri/gaming-workforce-observatory)
    """)

def get_current_page():
    """Retourne la page actuellement active"""
    try:
        # Streamlit utilise le nom du fichier pour identifier la page
        import inspect
        current_file = inspect.getfile(inspect.currentframe())
        if "Dashboard" in current_file:
            return "dashboard"
        elif "Analytics" in current_file:
            return "analytics"
        elif "Teams" in current_file:
            return "teams"
        elif "Predictions" in current_file:
            return "predictions"
        else:
            return "home"
    except:
        return "unknown"

def set_page_config_gaming(page_title: str, page_icon: str = "🎮"):
    """Configuration standardisée pour toutes les pages"""
    st.set_page_config(
        page_title=f"{page_title} - Gaming Workforce Observatory",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/remichenouri/gaming-workforce-observatory/issues',
            'Report a bug': 'https://github.com/remichenouri/gaming-workforce-observatory/issues',
            'About': """
            # 🎮 Gaming Workforce Observatory
            **Tableau de bord RH avancé pour l'industrie gaming**

            Version: 2.0.0 | License: MIT
            Développeur: Rémi Chenouri
            """
        }
    )
