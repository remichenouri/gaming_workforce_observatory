
import streamlit as st

def apply_gaming_theme():
    """Applique le thème gaming professionnel à l'application Streamlit"""

    st.markdown("""
    <style>
        /* === VARIABLES CSS GAMING === */
        :root {
            --gaming-blue: #667eea;
            --gaming-purple: #764ba2;
            --gaming-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --success-color: #28a745;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
            --dark-bg: #1a1a1a;
            --light-bg: #f8f9fa;
            --text-primary: #2c3e50;
            --text-secondary: #6c757d;
        }

        /* === LAYOUT PRINCIPAL === */
        .main > div {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* === HEADER PRINCIPAL === */
        .main-header {
            background: var(--gaming-gradient);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        }

        .main-header h1 {
            margin: 0;
            font-family: 'Arial Black', Arial, sans-serif;
            font-size: 2.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .main-header .subtitle {
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 300;
        }

        /* === BREADCRUMB NAVIGATION === */
        .breadcrumb {
            background: rgba(102, 126, 234, 0.1);
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            border-left: 4px solid var(--gaming-blue);
        }

        /* === MÉTRIQUES ST.METRIC === */
        [data-testid="metric-container"] {
            background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
            border: 2px solid var(--gaming-blue);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
            transition: all 0.3s ease;
        }

        [data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
        }

        [data-testid="metric-container"] > div {
            gap: 0.5rem;
        }

        [data-testid="metric-container"] label {
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            font-size: 0.9rem !important;
        }

        [data-testid="metric-container"] [data-testid="metric-value"] {
            color: var(--gaming-blue) !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }

        /* === SIDEBAR GAMING === */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        }

        .sidebar .sidebar-content .element-container {
            color: white;
        }

        /* === SELECTBOX ET INPUTS === */
        .stSelectbox > div > div {
            background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
            border: 2px solid var(--gaming-blue);
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        .stSelectbox > div > div:hover {
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        }

        /* === BOUTONS === */
        .stButton > button {
            background: var(--gaming-gradient);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }

        /* === ALERTES PERSONNALISÉES === */
        .alert-gaming {
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            font-weight: 500;
        }

        .alert-success-gaming {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-left: 5px solid var(--success-color);
            color: #155724;
        }

        .alert-warning-gaming {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border-left: 5px solid var(--warning-color);
            color: #856404;
        }

        .alert-danger-gaming {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            border-left: 5px solid var(--danger-color);
            color: #721c24;
        }

        /* === GRAPHIQUES PLOTLY === */
        .js-plotly-plot {
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        /* === DATAFRAMES === */
        .stDataFrame {
            border: 2px solid var(--gaming-blue);
            border-radius: 10px;
            overflow: hidden;
        }

        /* === SPINNER PERSONNALISÉ === */
        .stSpinner > div {
            border-top-color: var(--gaming-blue) !important;
        }

        /* === PROGRESS BAR === */
        .stProgress .st-bo {
            background: var(--gaming-gradient);
        }

        /* === TITRES ET TEXTE === */
        h1, h2, h3 {
            color: var(--text-primary);
            font-family: 'Arial Black', Arial, sans-serif;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        h2 {
            font-size: 1.8rem;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--gaming-blue);
        }

        h3 {
            font-size: 1.3rem;
            color: var(--gaming-purple);
        }

        /* === RESPONSIVE MOBILE === */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2rem;
            }

            [data-testid="metric-container"] {
                margin-bottom: 1rem;
            }

            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }

        /* === ANIMATIONS === */
        @keyframes pulse-gaming {
            0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
            100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
        }

        .pulse-animation {
            animation: pulse-gaming 2s infinite;
        }
    </style>
    """, unsafe_allow_html=True)

def create_gaming_alert(message: str, alert_type: str = "success") -> str:
    """Crée une alerte avec le style gaming

    Args:
        message: Le message à afficher
        alert_type: Type d'alerte ("success", "warning", "danger")

    Returns:
        HTML de l'alerte stylée
    """
    return f"""
    <div class="alert-gaming alert-{alert_type}-gaming">
        {message}
    </div>
    """

def create_kpi_card(title: str, value: str, delta: str = None, help_text: str = None) -> str:
    """Crée une carte KPI stylée gaming

    Args:
        title: Titre de la métrique
        value: Valeur principale
        delta: Variation (optionnel)
        help_text: Texte d'aide (optionnel)

    Returns:
        HTML de la carte KPI
    """
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ''
    help_html = f'<div class="kpi-help">{help_text}</div>' if help_text else ''

    return f"""
    <div class="kpi-card-gaming">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
        {help_html}
    </div>
    """
