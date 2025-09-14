"""
Gaming Workforce Observatory - Application Hybride Enterprise
Combine design minimaliste + fonctionnalités sophistiquées - VERSION CORRIGÉE
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
    UBISOFT_THEME = {'primary_color': '#6366f1'}
    APP_CONFIG = {'app_name': 'Gaming Workforce Observatory'}

try:
    from src.visualizations.interactive_charts import GamingInteractiveCharts
except ImportError:
    GamingInteractiveCharts = None

class GamingWorkforceApp:
    """Application principale hybride - Design + Sophistication"""
    
    def __init__(self):
        self.charts_lib = GamingInteractiveCharts() if GamingInteractiveCharts else None
        self.current_page = "🏠 Executive Dashboard"
        
        # Gaming colors et configuration
        self.gaming_colors = {
            'primary': '#6366f1',
            'secondary': '#764ba2',
            'accent': '#ff6b35',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#3498db'
        }
        
        self.department_colors = {
            'Programming': '#3498db',
            'Art & Animation': '#e74c3c',
            'Game Design': '#2ecc71',
            'Quality Assurance': '#f39c12',
            'Production': '#9b59b6',
            'Audio': '#1abc9c',
            'Marketing': '#34495e'
        }
    
    def apply_sophisticated_theme(self):
        """Thème sophistiqué avec sidebar VISIBLE"""
        
        st.markdown("""
        <style>
        /* Import Professional Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        /* CSS Variables - Gaming Theme */
        :root {
            --primary-color: #6366f1;
            --primary-dark: #4f46e5;
            --secondary-color: #f8fafc;
            --text-color: #1e293b;
            --text-light: #64748b;
            --border-color: #e2e8f0;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --sidebar-width: 300px;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        /* Hide Default Streamlit Elements */
        #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
        
        /* Main App Container */
        .main {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        }
        
        /* SIDEBAR VISIBLE - Sophisticated Design */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border-right: 2px solid var(--border-color);
            box-shadow: var(--shadow-lg);
        }
        
        /* KEEP Hamburger Menu VISIBLE */
        div[aria-label="Toggle sidebar"] {
            display: block !important;
            color: var(--primary-color);
        }
        
        /* Typography System */
        h1 {
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            font-size: 2.5rem;
            color: var(--text-color);
            letter-spacing: -0.05em;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }
        
        h2 {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            font-size: 1.875rem;
            color: var(--text-color);
            letter-spacing: -0.03em;
            margin-bottom: 1rem;
        }
        
        h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1.5rem;
            color: var(--text-color);
            letter-spacing: -0.02em;
            margin-bottom: 0.75rem;
        }
        
        /* Advanced Metrics Cards */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
        }
        
        div[data-testid="metric-container"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--primary-dark));
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px) scale(1.02);
            border-color: var(--primary-color);
        }
        
        div[data-testid="metric-container"]:hover::before {
            opacity: 1;
        }
        
        /* Sophisticated Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            font-size: 0.875rem;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        /* Advanced Navigation */
        .stRadio > div > label {
            background: transparent;
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            transition: all 0.3s ease;
            font-size: 0.875rem;
            font-weight: 500;
            cursor: pointer;
            position: relative;
        }
        
        .stRadio > div > label:hover {
            background: rgba(99, 102, 241, 0.1);
            transform: translateX(4px);
        }
        
        /* Sophisticated Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: var(--secondary-color);
            border-radius: 12px;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: white;
            box-shadow: var(--shadow-sm);
            color: var(--primary-color);
        }
        
        /* Enhanced Expanders */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            font-weight: 600;
            padding: 1rem 1.5rem;
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: var(--primary-color);
            box-shadow: var(--shadow-md);
        }
        
        .streamlit-expanderContent {
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 12px 12px;
            background: white;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--secondary-color);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--primary-color);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-dark);
        }
        </style>
        """, unsafe_allow_html=True)
    
    def create_enterprise_sidebar(self):
        """Sidebar enterprise sophistiquée - RESTAURÉE ET FONCTIONNELLE"""
        
        with st.sidebar:
            # Enterprise Header
            st.markdown("""
            <div style="text-align: center; padding: 1.5rem 0; border-bottom: 2px solid #e2e8f0; margin-bottom: 1.5rem;">
                <div style="font-size: 32px; margin-bottom: 0.75rem;">🎮</div>
                <div style="font-size: 14px; font-weight: 700; color: #6366f1; letter-spacing: 0.5px;">
                    GAMING OBSERVATORY
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 0.25rem;">
                    Enterprise Analytics
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation sophistiquée
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
                index=0,
                key="main_nav"
            )
            
            st.markdown("---")
            
            # KPIs Enterprise
            st.markdown("**📊 Enterprise Metrics**")
            
            # Métriques temps réel
            col1, col2 = st.columns(2)
            with col1:
                st.metric("👥 Workforce", "2,850", "+85")
                st.metric("📊 Data Points", "2.3M", "+5.2%")
            with col2:
                st.metric("📈 Retention", "87.5%", "+2.1%")
                st.metric("👥 Active Users", "1,247", "+12%")
            
            # Métriques additionnelles
            st.metric("⚡ System Uptime", "99.8%", "+0.1%")
            st.metric("🌍 Global Studios", "18")
            
            # Alerts section
            st.markdown("---")
            st.markdown("**🚨 Smart Alerts**")
            
            # Alert indicators
            alert_html = """
            <div style="margin: 0.5rem 0;">
                <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; background: #fef3c7; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <span style="font-size: 12px;">⚠️</span>
                    <span style="font-size: 11px; color: #975a16;">QA Satisfaction Alert</span>
                </div>
            </div>
            <div style="margin: 0.5rem 0;">
                <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; background: #dcfce7; border-radius: 8px; border-left: 4px solid #16a34a;">
                    <span style="font-size: 12px;">✅</span>
                    <span style="font-size: 11px; color: #166534;">All Models Online</span>
                </div>
            </div>
            """
            st.markdown(alert_html, unsafe_allow_html=True)
            
            # Quick Actions
            st.markdown("---")
            st.markdown("**⚡ Quick Actions**")
            
            if st.button("📊 Generate Report", use_container_width=True):
                st.success("Executive report queued for generation...")
            
            if st.button("🚀 Run ML Pipeline", use_container_width=True):
                st.info("ML models updating predictions...")
            
            return selected

    def render_sophisticated_content(self, page_selection):
        """Rendu sophistiqué du contenu selon la page sélectionnée"""
        
        page_name = page_selection.split(" ", 1)[1]  # Extraire le nom après l'icône
        page_icon = page_selection.split(" ", 1)[0]  # Extraire l'icône
        
        # Header sophistiqué avec animations
        st.markdown(f"""
        <div style="margin-bottom: 3rem; position: relative;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; position: relative; overflow: hidden;">
                <div style="position: relative; z-index: 1;">
                    <h1 style="color: white; font-size: 2.5rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 1rem;">
                        <span style="font-size: 3rem;">{page_icon}</span> {page_name}
                    </h1>
                    <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin: 0; font-weight: 400;">
                        Advanced workforce intelligence powered by AI and machine learning
                    </p>
                    <div style="margin-top: 1rem; display: flex; gap: 1rem; flex-wrap: wrap;">
                        <div style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.875rem; backdrop-filter: blur(10px);">
                            🤖 AI-Powered
                        </div>
                        <div style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.875rem; backdrop-filter: blur(10px);">
                            📊 Real-time Data
                        </div>
                        <div style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.875rem; backdrop-filter: blur(10px);">
                            🌍 Global Scale
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Contenu sophistiqué par page
        if "Executive" in page_name:
            self.render_executive_sophisticated()
        elif "Talent Wars" in page_name:
            self.render_talent_wars_sophisticated()
        elif "Neurodiversity" in page_name:
            self.render_neurodiversity_sophisticated()
        elif "Predictive" in page_name:
            self.render_predictive_sophisticated()
        elif "Global" in page_name:
            self.render_global_sophisticated()
        elif "Compensation" in page_name:
            self.render_compensation_sophisticated()
        elif "Future" in page_name:
            self.render_future_sophisticated()
        elif "Admin" in page_name:
            self.render_admin_sophisticated()
        else:
            self.render_default_page()
    
    def render_executive_sophisticated(self):
        """Executive Dashboard sophistiqué"""
        
        # KPIs Enterprise avec animations
        st.markdown("### 📊 Executive KPIs")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Workforce", "2,850", delta="85 this quarter", help="Total active employees across all studios")
        with col2:
            st.metric("Satisfaction Score", "7.3/10", delta="0.3 points", help="Employee satisfaction index")
        with col3:
            st.metric("Retention Rate", "87.5%", delta="2.1%", help="12-month rolling retention rate")
        with col4:
            st.metric("Performance Index", "8.2/10", delta="0.4 points", help="Overall team performance score")
        with col5:
            st.metric("Revenue/Employee", "$425K", delta="$18K", help="Annual revenue per employee")
        
        # Analytics sophistiquées
        st.markdown("### 🎯 Advanced Workforce Analytics")
        
        # Tabs sophistiqués
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends & Forecasting", "🎯 Performance Matrix", "💡 AI Insights", "⚙️ Operations"])
        
        with tab1:
            # Graphique des tendances
            dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
            trend_data = pd.DataFrame({
                'Date': dates,
                'Headcount': np.random.randint(2800, 2900, len(dates)),
                'Satisfaction': np.random.uniform(7.0, 7.8, len(dates)),
                'Retention': np.random.uniform(85, 90, len(dates)),
            })
            
            fig = px.line(trend_data, x='Date', y='Headcount', 
                         title='Workforce Evolution 2024',
                         height=400)
            fig.update_layout(template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Performance par département
            dept_data = pd.DataFrame({
                'Department': ['Programming', 'Art & Animation', 'Game Design', 'QA', 'Production', 'Audio'],
                'Performance': [8.4, 7.9, 8.1, 7.6, 8.2, 8.0],
                'Satisfaction': [8.2, 7.8, 8.0, 7.2, 7.9, 8.1],
                'Size': [450, 320, 180, 150, 80, 60],
            })
            
            fig_matrix = px.scatter(
                dept_data, 
                x='Performance', 
                y='Satisfaction',
                size='Size',
                color='Department',
                title='Department Performance Matrix',
                height=500,
                color_discrete_map=self.department_colors
            )
            
            st.plotly_chart(fig_matrix, use_container_width=True)
            st.dataframe(dept_data, use_container_width=True)
        
        with tab3:
            st.markdown("#### 🤖 AI-Powered Insights")
            
            insights = [
                {"title": "Attrition Risk Alert", "content": "23 employees at high risk", "confidence": 87},
                {"title": "Productivity Optimization", "content": "Flexible schedules could increase productivity 12%", "confidence": 72},
                {"title": "Skill Gap Detection", "content": "AI/ML skills demand growing", "confidence": 91}
            ]
            
            for insight in insights:
                with st.expander(f"🤖 {insight['title']}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Analysis:** {insight['content']}")
                    with col2:
                        st.metric("AI Confidence", f"{insight['confidence']}%")
        
        with tab4:
            st.markdown("#### ⚙️ Operations Dashboard")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("System Uptime", "99.97%", "+0.02%")
            with col2:
                st.metric("Data Freshness", "< 5 min")
            with col3:
                st.metric("Active Sessions", "247", "+12")
            with col4:
                st.metric("API Requests/min", "1,247", "+156")
    
    def render_talent_wars_sophisticated(self):
        """Talent Wars page sophistiquée"""
        
        st.markdown("### ⚔️ Talent Wars: Gaming vs Tech Industry")
        
        # Données sophistiquées
        comparison_data = pd.DataFrame({
            'Role': ['Senior Game Programmer', 'Game Designer', '3D Artist', 'QA Lead', 'Producer'],
            'Gaming_Industry': [125000, 105000, 85000, 75000, 115000],
            'Big_Tech': [180000, 140000, 120000, 110000, 155000],
            'Gap': [55000, 35000, 35000, 35000, 40000]
        })
        
        # Graphique de comparaison
        fig_comp = go.Figure()
        
        fig_comp.add_trace(go.Bar(
            name='Gaming Industry',
            x=comparison_data['Role'],
            y=comparison_data['Gaming_Industry'],
            marker_color=self.gaming_colors['primary']
        ))
        
        fig_comp.add_trace(go.Bar(
            name='Big Tech',
            x=comparison_data['Role'],
            y=comparison_data['Big_Tech'],
            marker_color=self.gaming_colors['danger']
        ))
        
        fig_comp.update_layout(
            title='Salary Comparison: Gaming vs Big Tech',
            barmode='group',
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
        st.dataframe(comparison_data, use_container_width=True)
    
    def render_neurodiversity_sophisticated(self):
        """Neurodiversity ROI sophistiqué"""
        
        st.markdown("### 🧠 Neurodiversity ROI Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("ROI on Accommodations", "363%", "+45%")
        with col2:
            st.metric("Innovation Index", "127", "+27")
        with col3:
            st.metric("Neurodiverse Talent", "12.5%", "+3.2%")
        
        st.info("🚧 Advanced neurodiversity analytics loading...")
    
    def render_predictive_sophisticated(self):
        """Predictive Analytics sophistiqué"""
        
        st.markdown("### 🎯 Predictive Analytics Suite")
        
        # Modèles ML
        st.markdown("#### 🤖 Active ML Models")
        
        models = [
            ("Attrition Predictor", "87.3%", "🟢 Active"),
            ("Performance Forecaster", "82.1%", "🟢 Active"),
            ("Salary Optimizer", "79.8%", "🟡 Training"),
            ("Skill Gap Analyzer", "91.2%", "🟢 Active")
        ]
        
        cols = st.columns(len(models))
        for i, (name, accuracy, status) in enumerate(models):
            with cols[i]:
                st.metric(name, accuracy, status)
    
    def render_global_sophisticated(self):
        """Global Studios sophistiqué"""
        
        st.markdown("### 🌍 Global Studios Intelligence")
        
        # Données globales simulées
        global_data = pd.DataFrame({
            'Studio': ['Paris', 'Montreal', 'Singapore', 'Los Angeles', 'Tokyo'],
            'Employees': [450, 380, 220, 510, 180],
            'Revenue_M': [125, 98, 67, 142, 78],
            'Satisfaction': [8.2, 8.5, 7.9, 7.8, 8.1]
        })
        
        fig_global = px.scatter(
            global_data,
            x='Employees',
            y='Revenue_M',
            size='Satisfaction',
            color='Studio',
            title='Global Studios Performance Matrix'
        )
        
        st.plotly_chart(fig_global, use_container_width=True)
    
    def render_compensation_sophisticated(self):
        """Compensation Intel sophistiqué"""
        
        st.markdown("### 💰 Compensation Intelligence")
        
        # Benchmark data
        benchmark_data = pd.DataFrame({
            'Company': ['Our Company', 'Ubisoft', 'EA Games', 'Riot Games', 'Epic Games'],
            'Avg_Salary': [95000, 125000, 135000, 145000, 140000]
        })
        
        fig_bench = px.bar(
            benchmark_data,
            x='Company',
            y='Avg_Salary',
            title='Industry Salary Benchmark',
            color='Avg_Salary',
            color_continuous_scale='Blues'
        )
        
        st.plotly_chart(fig_bench, use_container_width=True)
    
    def render_future_sophisticated(self):
        """Future Insights sophistiqué"""
        
        st.markdown("### 🔮 Future Workforce Insights")
        
        # Future predictions
        predictions = {
            "2025": {"Revenue": "$285B", "Workforce": "3.8M", "Remote": "65%"},
            "2027": {"Revenue": "$365B", "Workforce": "4.6M", "Remote": "75%"},
            "2030": {"Revenue": "$476B", "Workforce": "5.9M", "Remote": "85%"}
        }
        
        cols = st.columns(3)
        for i, (year, data) in enumerate(predictions.items()):
            with cols[i]:
                st.markdown(f"#### {year} Forecast")
                for metric, value in data.items():
                    st.metric(metric, value)
    
    def render_admin_sophisticated(self):
        """Admin Panel sophistiqué"""
        
        st.markdown("### ⚙️ Enterprise Administration")
        
        # Authentification simplifiée pour démo
        if "admin_authenticated" not in st.session_state:
            st.session_state.admin_authenticated = False
        
        if not st.session_state.admin_authenticated:
            with st.form("admin_login"):
                st.markdown("#### 🔐 Administrator Access")
                
                col1, col2 = st.columns(2)
                with col1:
                    username = st.text_input("Username")
                with col2:
                    password = st.text_input("Password", type="password")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.form_submit_button("🔑 Login", use_container_width=True):
                        if username == "admin" and password == "admin123":
                            st.session_state.admin_authenticated = True
                            st.success("Authentication successful!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                
                with col_b:
                    if st.form_submit_button("👤 Demo Access", use_container_width=True):
                        st.session_state.admin_authenticated = True
                        st.success("Demo access granted!")
                        st.rerun()
        else:
            st.success("🔓 Authenticated as Administrator")
            
            if st.button("🚪 Logout"):
                st.session_state.admin_authenticated = False
                st.rerun()
            
            # Admin dashboard
            st.markdown("#### 🛠️ System Management")
            
            admin_tabs = st.tabs(["Users", "System", "Config"])
            
            with admin_tabs[0]:
                st.markdown("**User Management**")
                st.dataframe({
                    'User': ['admin', 'hr_manager', 'analyst1', 'analyst2'],
                    'Role': ['Administrator', 'HR Manager', 'Data Analyst', 'Data Analyst'],
                    'Status': ['🟢 Active', '🟢 Active', '🟡 Away', '🔴 Inactive']
                })
            
            with admin_tabs[1]:
                st.markdown("**System Status**")
                system_metrics = [
                    ("Database", "🟢 Online", "99.97%"),
                    ("API Services", "🟢 Online", "99.95%"),
                    ("ML Pipeline", "🟢 Online", "98.23%"),
                    ("Data Sync", "🟢 Online", "99.87%")
                ]
                
                for service, status, uptime in system_metrics:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**{service}**")
                    with col2:
                        st.markdown(status)
                    with col3:
                        st.markdown(f"Uptime: {uptime}")
    
    def render_default_page(self):
        """Page par défaut"""
        
        st.markdown("### 🎮 Welcome to Gaming Workforce Observatory")
        st.markdown("Select a page from the sidebar to explore our enterprise analytics platform.")
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Features", "8", "Dashboards")
        with col2:
            st.metric("AI Models", "4", "Active")
        with col3:
            st.metric("Data Sources", "12", "Connected")
    
    def run(self):
        """Lance l'application hybride"""
        
        # Configuration Streamlit - SIDEBAR VISIBLE
        st.set_page_config(
            page_title="🎮 Gaming Workforce Observatory Enterprise",
            page_icon="🎮",
            layout="wide",
            initial_sidebar_state="expanded"  # CHANGÉ: auto ou expanded au lieu de collapsed
        )
        
        # Application du thème sophistiqué
        self.apply_sophisticated_theme()
        
        # Sidebar et navigation
        selected_page = self.create_enterprise_sidebar()
        
        # Contenu principal
        self.render_sophisticated_content(selected_page)
        
        # Footer enterprise
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%); border-radius: 12px; margin-top: 2rem;">
            <div style="color: #64748b; font-size: 0.875rem; margin-bottom: 0.5rem;">
                © 2025 Gaming Workforce Observatory Enterprise • All rights reserved
            </div>
            <div style="display: flex; justify-content: center; gap: 2rem; font-size: 0.75rem; color: #94a3b8;">
                <span>Last updated: {datetime.now().strftime('%H:%M:%S')}</span>
                <span>Version: 1.0.0</span>
                <span>Status: 🟢 All systems operational</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Point d'entrée principal
def main():
    """Lance l'application Gaming Workforce Observatory"""
    app = GamingWorkforceApp()
    app.run()

if __name__ == "__main__":
    main()
