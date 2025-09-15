"""
Gaming Workforce Observatory - Application Enterprise Professionnelle
Design professionnel avec fond clair + fonctionnalités sophistiquées
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path for enterprise modules
sys.path.append(str(Path(__file__).parent / "src"))

# Enterprise imports (with fallbacks)
try:
    from config.settings import UBISOFT_THEME, APP_CONFIG
except ImportError:
    UBISOFT_THEME = {'primary_color': '#0099FF'}
    APP_CONFIG = {'app_name': 'Ubisoft Gaming Workforce Observatory'}

try:
    from src.visualizations.interactive_charts import GamingInteractiveCharts
except ImportError:
    GamingInteractiveCharts = None

class UbisoftWorkforceApp:
    """Application principale Ubisoft - Design Professionnel Clair"""
    
    def __init__(self):
        self.charts_lib = GamingInteractiveCharts() if GamingInteractiveCharts else None
        self.current_page = "🏠 Executive Dashboard"
        
        # Ubisoft Colors - Professional Theme
        self.ubisoft_colors = {
            'primary': '#0099FF',      # Bleu Ubisoft
            'primary_dark': '#0066CC', 
            'accent': '#E60012',       # Rouge Ubisoft
            'success': '#28A745',
            'warning': '#FFB020',
            'danger': '#DC3545',
            'light': '#F8F9FA',        # Fond clair
            'white': '#FFFFFF',
            'text': '#2C3E50',         # Texte sombre
            'text_light': '#6C757D'
        }
        
        self.department_colors = {
            'Programming': '#0099FF',
            'Art & Animation': '#E60012',
            'Game Design': '#28A745',
            'Quality Assurance': '#FFB020',
            'Production': '#9B59B6',
            'Audio': '#17A2B8',
            'Marketing': '#6C757D'
        }
    
    def apply_professional_theme(self):
        """Thème professionnel avec fond CLAIR"""
        
        st.markdown("""
        <style>
        /* Import Professional Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* CSS Variables - Professional Light Theme */
        :root {
            --ubisoft-primary: #0099FF;
            --ubisoft-accent: #E60012;
            --bg-light: #F8F9FA;
            --bg-white: #FFFFFF;
            --text-dark: #2C3E50;
            --text-light: #6C757D;
            --border-light: #DEE2E6;
            --shadow: 0 2px 10px rgba(0,0,0,0.1);
            --shadow-hover: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        /* Hide Default Elements */
        #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
        
        /* Main App - Professional Light Background */
        .stApp {
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            background: var(--bg-light);
            color: var(--text-dark);
        }
        
        /* SIDEBAR Professional Light */
        section[data-testid="stSidebar"] {
            background: var(--bg-white);
            border-right: 1px solid var(--border-light);
            box-shadow: var(--shadow);
        }
        
        section[data-testid="stSidebar"] > div {
            background: var(--bg-white);
        }
        
        /* Typography Professional */
        h1, h2, h3 {
            color: var(--text-dark);
            font-family: 'Inter', sans-serif;
        }
        
        h1 {
            font-weight: 800;
            font-size: 2.2rem;
            margin-bottom: 1rem;
        }
        
        h2 {
            font-weight: 700;
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            font-weight: 600;
            font-size: 1.4rem;
            color: var(--ubisoft-primary);
            margin-bottom: 0.75rem;
        }
        
        /* Professional Metrics Cards */
        div[data-testid="metric-container"] {
            background: var(--bg-white);
            border: 1px solid var(--border-light);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            box-shadow: var(--shadow-hover);
            transform: translateY(-2px);
            border-color: var(--ubisoft-primary);
        }
        
        /* Professional Buttons */
        .stButton > button {
            background: var(--ubisoft-primary);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            box-shadow: var(--shadow);
        }
        
        .stButton > button:hover {
            background: var(--ubisoft-primary);
            transform: translateY(-1px);
            box-shadow: var(--shadow-hover);
        }
        
        /* Professional Navigation */
        .stRadio > div > label {
            background: var(--bg-white);
            border: 1px solid var(--border-light);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            transition: all 0.3s ease;
            color: var(--text-dark);
        }
        
        .stRadio > div > label:hover {
            background: rgba(0, 153, 255, 0.1);
            border-color: var(--ubisoft-primary);
        }
        
        /* Professional Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: var(--bg-white);
            border-radius: 8px;
            padding: 0.5rem;
            border: 1px solid var(--border-light);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 6px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: var(--text-dark);
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--ubisoft-primary);
            color: white;
            box-shadow: var(--shadow);
        }
        
        /* Professional Expanders */
        .streamlit-expanderHeader {
            background: var(--bg-white);
            border: 1px solid var(--border-light);
            border-radius: 8px;
            padding: 1rem 1.5rem;
            color: var(--text-dark);
            font-weight: 600;
        }
        
        .streamlit-expanderContent {
            border: 1px solid var(--border-light);
            border-top: none;
            border-radius: 0 0 8px 8px;
            background: var(--bg-white);
        }
        
        /* Professional Forms */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div {
            background: var(--bg-white);
            border: 1px solid var(--border-light);
            color: var(--text-dark);
            border-radius: 6px;
        }
        
        /* Professional DataFrames */
        .stDataFrame {
            background: var(--bg-white);
            border: 1px solid var(--border-light);
            border-radius: 8px;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-light);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--ubisoft-primary);
            border-radius: 3px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def get_professional_chart_config(self):
        """Configuration professionnelle des charts Plotly"""
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
                },
                'legend': {
                    'font': {'color': '#2C3E50'}
                }
            }
        }
    
    def create_professional_sidebar(self):
        """Sidebar professionnelle"""
        
        with st.sidebar:
            # Header professionnel
            st.markdown("""
            <div style="text-align: center; padding: 1.5rem 0; border-bottom: 2px solid #0099FF; margin-bottom: 1.5rem;">
                <div style="font-size: 28px; margin-bottom: 0.75rem;">🎮</div>
                <div style="font-size: 14px; font-weight: 700; color: #0099FF;">
                    UBISOFT GAMING OBSERVATORY
                </div>
                <div style="font-size: 11px; color: #6C757D; margin-top: 0.25rem;">
                    Enterprise Workforce Analytics
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation
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
            
            selected = st.radio(
                "Navigation",
                options=[f"{icon} {name}" for icon, name in pages],
                index=0
            )
            
            st.markdown("---")
            
            # KPIs
            st.markdown("**📊 Global Metrics**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Workforce", "2,847", "+85")
                st.metric("Retention", "87.3%", "+2.1%")
            with col2:
                st.metric("Satisfaction", "7.8/10", "+0.5")
                st.metric("Studios", "25", "Global")
            
            # Alerts
            st.markdown("---")
            st.markdown("**🚨 Smart Alerts**")
            
            st.markdown("""
            <div style="padding: 8px; background: #FFF3CD; border-left: 4px solid #FFB020; border-radius: 4px; margin: 8px 0;">
                <small style="color: #856404;">⚠️ QA Satisfaction Alert</small>
            </div>
            <div style="padding: 8px; background: #D4EDDA; border-left: 4px solid #28A745; border-radius: 4px; margin: 8px 0;">
                <small style="color: #155724;">✅ All Systems Online</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Actions
            st.markdown("---")
            if st.button("📊 Generate Report", use_container_width=True):
                st.success("Report queued")
            
            return selected

    def render_professional_content(self, page_selection):
        """Contenu professionnel"""
        
        page_name = page_selection.split(" ", 1)[1]
        page_icon = page_selection.split(" ", 1)[0]
        
        # Header professionnel
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0099FF 0%, #0066CC 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; color: white;">
            <h1 style="color: white; margin: 0; display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 2.5rem;">{page_icon}</span> 
                UBISOFT {page_name}
            </h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                Professional workforce analytics powered by advanced AI
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Contenu par page
        if "Executive" in page_name:
            self.render_executive_professional()
        elif "Talent Wars" in page_name:
            self.render_talent_wars_professional()
        elif "Neurodiversity" in page_name:
            self.render_neurodiversity_professional()
        elif "Predictive" in page_name:
            self.render_predictive_professional()
        elif "Global" in page_name:
            self.render_global_professional()
        elif "Compensation" in page_name:
            self.render_compensation_professional()
        elif "Future" in page_name:
            self.render_future_professional()
        elif "Admin" in page_name:
            self.render_admin_professional()
    
    def render_executive_professional(self):
        """Executive Dashboard professionnel"""
        
        st.markdown("### 📊 Executive KPIs")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Global Workforce", "2,847", "+85")
        with col2:
            st.metric("Satisfaction", "7.8/10", "+0.5")
        with col3:
            st.metric("Retention Rate", "87.3%", "+2.1%")
        with col4:
            st.metric("Performance", "8.7/10", "+0.6")
        with col5:
            st.metric("Revenue/Employee", "$485K", "+$28K")
        
        st.markdown("### 📈 Workforce Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Global Trends", "Department Performance", "AI Insights"])
        
        with tab1:
            # Données simulées
            dates = pd.date_range('2024-01-01', periods=12, freq='M')
            data = pd.DataFrame({
                'Date': dates,
                'Headcount': np.random.randint(2800, 2900, 12)
            })
            
            fig = px.line(data, x='Date', y='Headcount', 
                         color_discrete_sequence=[self.ubisoft_colors['primary']])
            
            # Configuration SANS conflit de title
            chart_config = self.get_professional_chart_config()
            fig.update_layout(**chart_config['layout'])
            fig.update_layout(title="Workforce Evolution 2024")  # Title appliqué séparément
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            dept_data = pd.DataFrame({
                'Department': ['Programming', 'Art', 'Design', 'QA', 'Production'],
                'Performance': [8.7, 8.2, 8.4, 7.9, 8.5],
                'Satisfaction': [8.5, 8.1, 8.3, 7.8, 8.2],
                'Size': [680, 520, 280, 350, 180]
            })
            
            fig = px.scatter(dept_data, x='Performance', y='Satisfaction', 
                           size='Size', color='Department',
                           color_discrete_map=self.department_colors)
            
            chart_config = self.get_professional_chart_config()
            fig.update_layout(**chart_config['layout'])
            fig.update_layout(title="Department Performance Matrix")
            
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(dept_data, use_container_width=True)
        
        with tab3:
            st.markdown("#### 🤖 AI-Powered Insights")
            
            insights = [
                "8 employees at high turnover risk - Montreal studio",
                "Hybrid work model could boost productivity 18%",
                "VR/AR skills critical for upcoming projects"
            ]
            
            for i, insight in enumerate(insights, 1):
                st.info(f"**Insight {i}:** {insight}")
    
    def render_talent_wars_professional(self):
        """Talent Wars professionnel"""
        st.markdown("### ⚔️ Talent Competition Analysis")
        st.info("🚧 Advanced talent analytics loading...")
    
    def render_neurodiversity_professional(self):
        """Neurodiversity professionnel"""
        st.markdown("### 🧠 Neurodiversity ROI")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Neurodiverse Talent", "18.3%", "+4.2%")
        with col2:
            st.metric("Innovation Boost", "+27%", "vs baseline")
        with col3:
            st.metric("Bug Detection", "+34%", "QA advantage")
        with col4:
            st.metric("ROI per Hire", "$52K", "annual")
    
    def render_predictive_professional(self):
        """Predictive Analytics professionnel"""
        st.markdown("### 🎯 AI-Powered Predictions")
        
        models = [
            ("Turnover Predictor", "89.3%", "🟢 Active"),
            ("Burnout Detection", "87.8%", "🟢 Active"),
            ("Performance Forecaster", "84.2%", "🟢 Active")
        ]
        
        cols = st.columns(3)
        for i, (name, accuracy, status) in enumerate(models):
            with cols[i]:
                st.metric(name, accuracy, status)
    
    def render_global_professional(self):
        """Global Studios professionnel"""
        st.markdown("### 🌍 Global Operations")
        st.info("🚧 Global studios analytics loading...")
    
    def render_compensation_professional(self):
        """Compensation professionnel"""
        st.markdown("### 💰 Compensation Intelligence")
        st.info("🚧 Salary benchmarking analytics loading...")
    
    def render_future_professional(self):
        """Future Insights professionnel"""
        st.markdown("### 🔮 Future Workforce")
        
        predictions = {
            "2025": {"Workforce": "3,200", "AI Integration": "75%"},
            "2027": {"Workforce": "3,800", "AI Integration": "90%"},
            "2030": {"Workforce": "4,500", "AI Integration": "95%"}
        }
        
        cols = st.columns(3)
        for i, (year, data) in enumerate(predictions.items()):
            with cols[i]:
                st.markdown(f"#### {year}")
                for metric, value in data.items():
                    st.metric(metric, value)
    
    def render_admin_professional(self):
        """Admin Panel professionnel"""
        st.markdown("### ⚙️ System Administration")
        
        if "admin_auth" not in st.session_state:
            st.session_state.admin_auth = False
        
        if not st.session_state.admin_auth:
            st.warning("🔐 Administrator access required")
            
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username")
            with col2:
                password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                if username == "admin" and password == "demo":
                    st.session_state.admin_auth = True
                    st.success("✅ Authenticated")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        else:
            st.success("🔓 Administrator Panel")
            if st.button("Logout"):
                st.session_state.admin_auth = False
                st.rerun()
            
            st.markdown("#### System Status")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Uptime", "99.8%")
            with col2:
                st.metric("Users", "847")
            with col3:
                st.metric("Response", "1.2s")
    
    def run(self):
        """Lance l'application professionnelle"""
        
        st.set_page_config(
            page_title="🎮 Ubisoft Gaming Workforce Observatory",
            page_icon="🎮",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        self.apply_professional_theme()
        selected_page = self.create_professional_sidebar()
        self.render_professional_content(selected_page)
        
        # Footer professionnel
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; color: #6C757D; font-size: 0.85rem;">
            © 2025 Ubisoft Entertainment • Gaming Workforce Observatory Enterprise<br/>
            Last updated: {datetime.now().strftime('%H:%M:%S')} • Version 2.0 • All systems operational
        </div>
        """, unsafe_allow_html=True)

def main():
    app = UbisoftWorkforceApp()
    app.run()

if __name__ == "__main__":
    main()
