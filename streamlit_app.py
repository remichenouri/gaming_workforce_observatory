"""
Gaming Workforce Observatory - Application Minimaliste
Design épuré avec sidebar auto-hide inspiré de votre référence
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def apply_clean_theme():
    """Applique le thème minimaliste moderne"""
    
    st.markdown("""
    <style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #f8fafc;
        --text-color: #1e293b;
        --border-color: #e2e8f0;
        --sidebar-width: 280px;
        --sidebar-collapsed: 60px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar minimaliste */
    section[data-testid="stSidebar"] {
        width: var(--sidebar-collapsed) !important;
        min-width: var(--sidebar-collapsed) !important;
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid var(--border-color);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        overflow-x: hidden;
        z-index: 999;
    }
    
    /* Sidebar expand on hover */
    section[data-testid="stSidebar"]:hover {
        width: var(--sidebar-width) !important;
        min-width: var(--sidebar-width) !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide hamburger */
    div[aria-label="Toggle sidebar"] {
        display: none !important;
    }
    
    /* Main content adjustment */
    .main .block-container {
        margin-left: calc(var(--sidebar-collapsed) + 1rem) !important;
        padding: 1rem 2rem !important;
        max-width: none !important;
        transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Typography */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--text-color);
        letter-spacing: -0.025em;
        line-height: 1.25;
    }
    
    /* Clean metrics */
    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    .stButton > button:hover {
        background: #4f46e5;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Radio buttons in sidebar */
    .stRadio > div {
        flex-direction: column;
        gap: 0;
    }
    
    .stRadio > div > label {
        background: transparent;
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.1rem 0;
        transition: all 0.2s ease;
        font-size: 14px;
        font-weight: 500;
    }
    
    .stRadio > div > label:hover {
        background: rgba(99, 102, 241, 0.1);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        border: 1px solid var(--border-color);
        border-top: none;
        border-radius: 0 0 8px 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def create_minimal_sidebar():
    """Sidebar minimaliste avec icônes et navigation"""
    
    with st.sidebar:
        # Logo/Header minimaliste
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <div style="font-size: 28px; margin-bottom: 0.5rem;">🎮</div>
            <div style="font-size: 12px; font-weight: 600; color: #6366f1; opacity: 0; transition: opacity 0.3s;">
                Gaming Observatory
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation avec icônes
        pages = [
            ("🏠", "Executive Dashboard"),
            ("⚔️", "Talent Wars"), 
            ("🧠", "Neurodiversity ROI"),
            ("🎯", "Predictive Analytics"),
            ("🌍", "Global Studios"),
            ("💰", "Compensation Intel"),
            ("🔮", "Future Insights"),
            ("⚙️", "Admin Panel")
        ]
        
        # Radio avec formatage spécial
        selected = st.radio(
            "",
            options=[f"{icon} {name}" for icon, name in pages],
            index=0,
            label_visibility="collapsed",
            key="main_nav"
        )
        
        st.markdown("---")
        
        # KPIs compacts
        st.markdown("**📊 Quick Stats**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("👥", "2,850", "Workforce")
        with col2:
            st.metric("📈", "87.5%", "Retention")
        
        st.metric("⚡", "99.8%", "Uptime")
        
        # Status indicator
        st.markdown("""
        <div style="margin-top: 1rem; padding: 0.5rem; background: #f0fdf4; border-radius: 6px; text-align: center;">
            <div style="color: #16a34a; font-size: 12px; font-weight: 500;">🟢 All Systems Online</div>
        </div>
        """, unsafe_allow_html=True)
        
        return selected

def render_page_content(page_selection):
    """Rendu du contenu selon la page sélectionnée"""
    
    page_name = page_selection.split(" ", 1)[1]  # Extraire le nom après l'icône
    page_icon = page_selection.split(" ", 1)[0]  # Extraire l'icône
    
    # Header épuré
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem; color: #1e293b; display: flex; align-items: center; gap: 0.5rem;">
            {page_icon} {page_name}
        </h1>
        <p style="color: #64748b; font-size: 1.1rem; margin: 0; font-weight: 400;">
            Real-time workforce intelligence and strategic analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contenu spécifique par page
    if "Executive" in page_name:
        render_executive_content()
    elif "Talent Wars" in page_name:
        render_talent_wars_content()
    elif "Neurodiversity" in page_name:
        render_neurodiversity_content()
    elif "Predictive" in page_name:
        render_predictive_content()
    elif "Global" in page_name:
        render_global_content()
    elif "Compensation" in page_name:
        render_compensation_content()
    elif "Future" in page_name:
        render_future_content()
    elif "Admin" in page_name:
        render_admin_content()

def render_executive_content():
    """Contenu Executive Dashboard"""
    
    # KPIs principaux
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Workforce", "2,850", delta="85 this quarter")
    with col2:
        st.metric("Satisfaction Score", "7.3/10", delta="0.3 points")
    with col3:
        st.metric("Retention Rate", "87.5%", delta="2.1%")
    with col4:
        st.metric("Performance Index", "8.2/10", delta="0.4 points")
    
    # Zone principale interactive
    st.markdown("### 📊 Workforce Analytics")
    
    # Tabs pour organiser le contenu
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🎯 Performance", "💡 Insights"])
    
    with tab1:
        # Graphique des tendances
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Headcount': np.random.randint(2800, 2900, len(dates)),
            'Satisfaction': np.random.uniform(7.0, 7.8, len(dates)),
            'Retention': np.random.uniform(85, 90, len(dates))
        })
        
        fig = px.line(trend_data, x='Date', y='Headcount', 
                     title='Workforce Evolution 2024',
                     height=400)
        fig.update_layout(
            template='plotly_white',
            title_font_size=16,
            title_x=0.1
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Performance par département
        dept_data = pd.DataFrame({
            'Department': ['Programming', 'Art & Animation', 'Game Design', 'QA', 'Production'],
            'Performance': [8.4, 7.9, 8.1, 7.6, 8.2],
            'Satisfaction': [8.2, 7.8, 8.0, 7.2, 7.9],
            'Size': [450, 320, 180, 150, 80]
        })
        
        fig_perf = px.scatter(dept_data, x='Performance', y='Satisfaction', 
                             size='Size', color='Department',
                             title='Department Performance Matrix',
                             height=400)
        fig_perf.update_layout(template='plotly_white')
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with tab3:
        st.markdown("#### 🧠 Key Insights")
        
        insights = [
            "Programming team shows highest performance but watch satisfaction trends",
            "QA department needs attention - lowest satisfaction score at 7.2/10", 
            "Art & Animation team stable with good work-life balance",
            "Overall retention above industry average (85%)"
        ]
        
        for insight in insights:
            st.markdown(f"• {insight}")
        
        # Controls avancés
        with st.expander("⚙️ Advanced Controls", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                time_range = st.selectbox("Time Range", ["Last 30 days", "Last quarter", "Last year"])
            with col2:
                department = st.selectbox("Focus Department", ["All", "Programming", "Art", "Design", "QA"])

def render_talent_wars_content():
    """Contenu Talent Wars simplifié"""
    st.info("🚧 Talent Wars analytics are being enhanced with the new design system...")
    
    # Demo chart
    companies = ['Our Company', 'Ubisoft', 'EA', 'Riot', 'Epic']
    salaries = [95000, 125000, 135000, 145000, 140000]
    
    fig = px.bar(x=companies, y=salaries, title="Salary Benchmark")
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

def render_neurodiversity_content():
    """Contenu Neurodiversity ROI"""
    st.info("🚧 Neurodiversity ROI dashboard loading...")

def render_predictive_content():
    """Contenu Predictive Analytics"""
    st.info("🚧 Predictive Analytics models loading...")

def render_global_content():
    """Contenu Global Studios"""
    st.info("🚧 Global Studios map loading...")

def render_compensation_content():
    """Contenu Compensation Intel"""
    st.info("🚧 Compensation Intelligence updating...")

def render_future_content():
    """Contenu Future Insights"""
    st.info("🚧 Future Insights forecasting...")

def render_admin_content():
    """Contenu Admin Panel"""
    st.info("🚧 Admin Panel secure access loading...")

def main():
    """Application principale"""
    
    # Configuration
    st.set_page_config(
        page_title="🎮 Gaming Workforce Observatory",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Applique le thème propre
    apply_clean_theme()
    
    # Sidebar et navigation
    selected_page = create_minimal_sidebar()
    
    # Contenu principal
    render_page_content(selected_page)
    
    # Footer minimaliste
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #64748b; font-size: 0.875rem; padding: 1rem 0;'>"
        f"© 2025 Gaming Workforce Observatory • Last updated: {datetime.now().strftime('%H:%M')} • "
        "All systems operational"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
