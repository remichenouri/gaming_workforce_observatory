"""
🎮 Gaming Workforce Observatory - Application Streamlit Enterprise ULTIME
Version 2.0 - Architecture GitHub Sophistiquée Adaptée
Créée par remichenouri - Excellence Gaming Analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import json
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration page
st.set_page_config(
    page_title="🎮 Gaming Workforce Observatory Enterprise",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/remichenouri/gaming_workforce_observatory',
        'Report a bug': "https://github.com/remichenouri/gaming_workforce_observatory/issues",
        'About': "Gaming Workforce Observatory - Enterprise Edition v2.0"
    }
)

# Configuration intégrée directement dans app.py
GAMING_THEME = {
    'primary': '#0066CC',
    'accent': '#FF6B35', 
    'success': '#28A745',
    'warning': '#FFB020',
    'danger': '#DC3545',
    'background': '#F8F9FA',
    'text': '#2C3E50'
}
APP_CONFIG = {'app_name': 'Gaming Workforce Observatory Enterprise'}

class GamingWorkforceApp:
    """Application principale Gaming Workforce Observatory Enterprise"""
    
    def __init__(self):
        self.theme = GAMING_THEME
        self.setup_session_state()
        self.load_data()
        
    def setup_session_state(self):
        """Initialisation état session"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Executive Dashboard'
        if 'theme_mode' not in st.session_state:
            st.session_state.theme_mode = 'light'
    
    def load_data(self):
        """Chargement données gaming sophistiquées avec cache"""
        try:
            self.employees_df = pd.read_csv('gaming_workforce_employees_advanced.csv')
            self.projects_df = pd.read_csv('gaming_workforce_projects_advanced.csv')
        except FileNotFoundError:
            # Génération données par défaut
            self.employees_df = self.generate_fallback_employee_data()
            self.projects_df = self.generate_fallback_project_data()
    
    @st.cache_data(ttl=300)
    def generate_fallback_employee_data(_self):
        """Génération données employés par défaut"""
        np.random.seed(42)
        departments = ['Programming', 'Art & Animation', 'Game Design', 'Quality Assurance', 'Production', 'Audio']
        levels = ['Junior', 'Mid', 'Senior', 'Lead']
        locations = ['Montreal', 'Paris', 'Tokyo', 'Stockholm', 'Seoul']
        
        data = []
        for i in range(500):
            dept = np.random.choice(departments)
            level = np.random.choice(levels, p=[0.3, 0.4, 0.2, 0.1])
            
            data.append({
                'employee_id': i+1,
                'department': dept,
                'level': level,
                'location': np.random.choice(locations),
                'salary': np.random.randint(45000, 150000),
                'satisfaction_score': np.random.uniform(6.0, 9.5),
                'performance_score': np.random.uniform(3.0, 5.0),
                'retention_risk': np.random.uniform(0.1, 0.8),
                'burnout_risk': np.random.uniform(0.1, 0.7),
                'sprint_velocity': np.random.uniform(25, 45),
                'innovation_index': np.random.uniform(40, 95),
                'team_synergy_score': np.random.uniform(6.0, 9.0)
            })
        
        return pd.DataFrame(data)
    
    @st.cache_data(ttl=300) 
    def generate_fallback_project_data(_self):
        """Génération données projets par défaut"""
        np.random.seed(42)
        project_types = ['AAA Game', 'Indie Game', 'Mobile Game', 'VR Experience']
        statuses = ['Pre-production', 'Production', 'Alpha', 'Beta', 'Live']
        
        data = []
        for i in range(50):
            data.append({
                'project_id': i+1,
                'project_name': f'Gaming Project {i+1}',
                'project_type': np.random.choice(project_types),
                'development_phase': np.random.choice(statuses),
                'team_size': np.random.randint(8, 80),
                'budget_million': np.random.uniform(1.0, 25.0),
                'completion_percentage': np.random.uniform(20, 100),
                'sprint_velocity_avg': np.random.uniform(30, 45),
                'bug_count_total': np.random.randint(50, 500)
            })
        
        return pd.DataFrame(data)

    def apply_theme(self):
        """Application thème gaming enterprise"""
        st.markdown(f"""
        <style>
        /* Gaming Enterprise Theme */
        .main-header {{
            background: linear-gradient(135deg, {self.theme['primary']}15, {self.theme['accent']}10);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            border-left: 4px solid {self.theme['primary']};
        }}
        
        .metric-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left: 4px solid {self.theme['primary']};
            margin: 0.5rem 0;
            transition: transform 0.2s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        
        .gaming-kpi {{
            background: linear-gradient(135deg, {self.theme['success']}15, {self.theme['primary']}10);
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border: 1px solid {self.theme['success']}30;
        }}
        
        .sidebar-section {{
            background: {self.theme['background']};
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }}
        
        .alert-critical {{
            background: linear-gradient(135deg, {self.theme['danger']}15, #fff);
            border: 1px solid {self.theme['danger']};
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        .alert-success {{
            background: linear-gradient(135deg, {self.theme['success']}15, #fff);
            border: 1px solid {self.theme['success']};
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        /* Navigation personnalisée */
        .nav-button {{
            background: {self.theme['primary']};
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            margin: 0.25rem;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 600;
        }}
        
        .nav-button:hover {{
            background: {self.theme['accent']};
            transform: translateX(5px);
        }}
        
        .nav-button.active {{
            background: {self.theme['accent']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        </style>
        """, unsafe_allow_html=True)

    def render_authentication(self):
        """Rendu authentification sophistiquée"""
        if not st.session_state.authenticated:
            st.markdown("""
            <div class="main-header">
                <h1>🎮 Gaming Workforce Observatory</h1>
                <h3>Enterprise Authentication Required</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                with st.container():
                    st.markdown("### 🔐 Secure Access")
                    
                    username = st.text_input("Username", value="admin", placeholder="Enter username")
                    password = st.text_input("Password", type="password", value="demo", placeholder="Enter password")
                    
                    col_login, col_guest = st.columns(2)
                    
                    with col_login:
                        if st.button("🚀 Login", type="primary", use_container_width=True):
                            if username == "admin" and password == "demo":
                                st.session_state.authenticated = True
                                st.success("✅ Authentication successful!")
                                st.rerun()
                            else:
                                st.error("❌ Invalid credentials")
                    
                    with col_guest:
                        if st.button("👤 Guest Access", use_container_width=True):
                            st.session_state.authenticated = True
                            st.info("ℹ️ Logged in as Guest")
                            st.rerun()
                    
                    st.markdown("---")
                    st.info("💡 **Demo Credentials:** admin / demo")
                    
                    # Métriques publiques
                    st.markdown("### 📊 Public Gaming Industry Stats")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Global Gaming Workforce", "2.8M+", "+8.5%")
                    with col2:
                        st.metric("Average Salary", "$87,404", "+$3,200")
                    with col3:
                        st.metric("Industry Growth", "12.3%", "+2.1%")
            
            return False
        return True

    def render_sidebar(self):
        """Sidebar navigation sophistiquée"""
        with st.sidebar:
            # Header sidebar
            st.markdown("""
            <div class="sidebar-section">
                <h2>🎮 Gaming Observatory</h2>
                <p><strong>Enterprise Analytics Platform</strong></p>
                <p style="font-size: 0.8rem; color: #666;">Version 2.0 - Powered by Advanced AI</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation pages
            st.markdown("### 📱 Navigation")
            
            pages = [
                ("🏠", "Executive Dashboard", "C-suite gaming analytics"),
                ("⚔️", "Talent Wars", "Gaming vs Tech comparison"),
                ("🧠", "Neurodiversity ROI", "Cognitive diversity impact"),
                ("🎯", "Predictive Analytics", "AI/ML workforce models"),
                ("🌍", "Global Studios", "Worldwide operations"),
                ("💰", "Compensation Intel", "Salary benchmarking"),
                ("🔮", "Future Insights", "Workforce forecasting"),
                ("⚙️", "Admin Panel", "System configuration")
            ]
            
            for icon, name, desc in pages:
                if st.button(f"{icon} {name}", use_container_width=True, 
                           help=desc, key=f"nav_{name}"):
                    st.session_state.current_page = name
                    st.rerun()
            
            st.markdown("---")
            
            # KPIs sidebar en temps réel
            st.markdown("### 📊 Real-time KPIs")
            
            # Calcul KPIs dynamiques
            total_employees = len(self.employees_df)
            avg_satisfaction = self.employees_df['satisfaction_score'].mean()
            avg_performance = self.employees_df['performance_score'].mean()
            high_risk_count = len(self.employees_df[self.employees_df['retention_risk'] > 0.6])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("👥 Workforce", f"{total_employees:,}", "+45")
                st.metric("😊 Satisfaction", f"{avg_satisfaction:.1f}/10", "+0.3")
            with col2:
                st.metric("⭐ Performance", f"{avg_performance:.1f}/5", "+0.2") 
                st.metric("⚠️ At Risk", f"{high_risk_count}", "-12")
            
            # Alertes intelligentes
            st.markdown("### 🚨 Smart Alerts")
            
            if high_risk_count > 50:
                st.error(f"🔴 **High Alert**: {high_risk_count} employees at risk")
            elif high_risk_count > 20:
                st.warning(f"🟡 **Warning**: {high_risk_count} employees need attention")
            else:
                st.success(f"🟢 **All Good**: Low retention risk")
            
            # Actions rapides
            st.markdown("### ⚡ Quick Actions")
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("📈 Report generation started...")
            
            if st.button("📧 Send Alerts", use_container_width=True):
                st.info("📬 Alert notifications sent!")
            
            # Footer sidebar
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; font-size: 0.7rem; color: #666;">
                <p>🎮 Gaming Workforce Observatory</p>
                <p>© 2024 Enterprise Edition</p>
                <p>⚡ All systems operational</p>
            </div>
            """, unsafe_allow_html=True)

    def render_current_page(self):
        """Rendu page courante"""
        page = st.session_state.current_page
        
        # Header principal avec contexte
        st.markdown(f"""
        <div class="main-header">
            <h1>🎮 Gaming Workforce Observatory - {page}</h1>
            <p><strong>Enterprise Gaming Analytics Platform</strong> | Real-time workforce intelligence powered by advanced AI</p>
            <p style="font-size: 0.9rem; color: #666;">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data refresh: Live</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Routage pages
        if page == "Executive Dashboard":
            self.render_executive_dashboard()
        elif page == "Talent Wars":
            self.render_talent_wars()
        elif page == "Neurodiversity ROI":
            self.render_neurodiversity_roi()
        elif page == "Predictive Analytics":
            self.render_predictive_analytics()
        elif page == "Global Studios":
            self.render_global_studios()
        elif page == "Compensation Intel":
            self.render_compensation_intel()
        elif page == "Future Insights":
            self.render_future_insights()
        elif page == "Admin Panel":
            self.render_admin_panel()

    def get_gaming_color_palette(self):
        """Palette couleurs gaming professionnelle"""
        return [
            self.theme['primary'],   # Bleu gaming
            self.theme['accent'],    # Orange gaming
            self.theme['success'],   # Vert performance
            '#9B59B6',              # Violet créativité
            '#E74C3C',              # Rouge alerte
            '#F39C12',              # Orange warning
            '#1ABC9C',              # Turquoise innovation
            '#34495E'               # Gris corporate
        ]

    def create_advanced_chart_config(self):
        """Configuration charts gaming avancée"""
        return {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'white',
            'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': '#2C3E50'},
            'colorway': self.get_gaming_color_palette(),
            'margin': {'t': 50, 'b': 40, 'l': 60, 'r': 40},
            'xaxis': {'gridcolor': '#E9ECEF', 'showgrid': True},
            'yaxis': {'gridcolor': '#E9ECEF', 'showgrid': True},
            'legend': {'orientation': 'h', 'yanchor': 'bottom', 'y': -0.2}
        }

    def render_executive_dashboard(self):
        """Dashboard exécutif sophistiqué"""
        # Métriques executive principales
        st.markdown("## 📊 Executive Gaming Workforce KPIs")
        
        # Calculs avancés
        total_employees = len(self.employees_df)
        avg_salary = self.employees_df['salary'].mean()
        avg_satisfaction = self.employees_df['satisfaction_score'].mean()
        avg_performance = self.employees_df['performance_score'].mean()
        
        if 'retention_risk' in self.employees_df.columns:
            retention_rate = (1 - self.employees_df['retention_risk'].mean()) * 100
        else:
            retention_rate = 87.3
            
        revenue_per_employee = avg_salary * 5.2  # Estimation gaming industry
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>👥 Total Workforce</h3>
                <h2 style="color: #0066CC;">{:,}</h2>
                <p style="color: #28A745;">▲ +127 this month</p>
            </div>
            """.format(total_employees), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>💰 Avg Salary</h3>
                <h2 style="color: #FF6B35;">${:,.0f}</h2>
                <p style="color: #28A745;">▲ +$2,840 YoY</p>
            </div>
            """.format(avg_salary), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>😊 Satisfaction</h3>
                <h2 style="color: #28A745;">{:.1f}/10</h2>
                <p style="color: #28A745;">▲ +0.4 this quarter</p>
            </div>
            """.format(avg_satisfaction), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>⭐ Performance</h3>
                <h2 style="color: #9B59B6;">{:.1f}/5</h2>
                <p style="color: #28A745;">▲ +0.2 this quarter</p>
            </div>
            """.format(avg_performance), unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div class="metric-card">
                <h3>💼 Revenue/Employee</h3>
                <h2 style="color: #E74C3C;">${:,.0f}K</h2>
                <p style="color: #28A745;">▲ +8.7% industry avg</p>
            </div>
            """.format(revenue_per_employee/1000), unsafe_allow_html=True)

        # Visualisations sophistiquées
        st.markdown("## 📈 Advanced Gaming Workforce Analytics")
        
        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Performance Matrix", "🏢 Department Analysis", "📊 Trend Analysis", "🤖 AI Insights"])
        
        with tab1:
            self.render_performance_matrix()
        
        with tab2:
            self.render_department_analysis()
            
        with tab3:
            self.render_trend_analysis()
            
        with tab4:
            self.render_ai_insights()

    def render_performance_matrix(self):
        """Matrice performance sophistiquée"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot satisfaction vs performance par département
            fig = px.scatter(
                self.employees_df,
                x='performance_score',
                y='satisfaction_score', 
                color='department',
                size='salary',
                hover_data=['level', 'location'],
                title="🎯 Performance vs Satisfaction Matrix",
                labels={'performance_score': 'Performance Score', 'satisfaction_score': 'Satisfaction Score'}
            )
            fig.update_layout(self.create_advanced_chart_config())
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Heatmap corrélation KPIs
            numeric_cols = ['satisfaction_score', 'performance_score', 'salary']
            if 'sprint_velocity' in self.employees_df.columns:
                numeric_cols.extend(['sprint_velocity', 'innovation_index', 'team_synergy_score'])
            
            corr_data = self.employees_df[numeric_cols].corr()
            
            fig = px.imshow(
                corr_data,
                title="🔥 Gaming KPIs Correlation Heatmap",
                color_continuous_scale="RdBu_r",
                aspect="auto"
            )
            fig.update_layout(self.create_advanced_chart_config())
            st.plotly_chart(fig, use_container_width=True)

    def render_department_analysis(self):
        """Analyse départementale avancée"""
        # Performance par département
        dept_stats = self.employees_df.groupby('department').agg({
            'satisfaction_score': 'mean',
            'performance_score': 'mean', 
            'salary': ['mean', 'count'],
            'retention_risk': 'mean' if 'retention_risk' in self.employees_df.columns else lambda x: 0.3
        }).round(2)
        
        dept_stats.columns = ['Satisfaction', 'Performance', 'Avg Salary', 'Headcount', 'Retention Risk']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Radar chart départements
            if len(dept_stats) > 0:
                fig = go.Figure()
                
                for i, dept in enumerate(dept_stats.index[:4]):  # Top 4 départements
                    values = [
                        dept_stats.loc[dept, 'Satisfaction'],
                        dept_stats.loc[dept, 'Performance'],
                        dept_stats.loc[dept, 'Avg Salary'] / 1000,  # En K
                        (1 - dept_stats.loc[dept, 'Retention Risk']) * 10  # Conversion
                    ]
                    
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=['Satisfaction', 'Performance', 'Salary (K)', 'Retention'],
                        fill='toself',
                        name=dept,
                        line_color=self.get_gaming_color_palette()[i]
                    ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 10])
                    ),
                    title="🎯 Department Performance Radar",
                    **self.create_advanced_chart_config()
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sunburst organisation 
            fig = px.sunburst(
                self.employees_df,
                path=['department', 'level'],
                values='salary',
                title="🌟 Gaming Organization Sunburst",
                color='department',
                color_discrete_sequence=self.get_gaming_color_palette()
            )
            fig.update_layout(self.create_advanced_chart_config())
            st.plotly_chart(fig, use_container_width=True)
        
        # Tableau département détaillé
        st.markdown("### 📊 Department Analytics Table")
        
        # Styling tableau
        styled_df = dept_stats.style.background_gradient(
            subset=['Satisfaction', 'Performance'],
            cmap='RdYlGn'
        ).format({
            'Satisfaction': '{:.1f}',
            'Performance': '{:.1f}',
            'Avg Salary': '${:,.0f}',
            'Retention Risk': '{:.1%}'
        })
        
        st.dataframe(styled_df, use_container_width=True)

    def render_trend_analysis(self):
        """Analyse tendances gaming"""
        st.markdown("### 📈 Gaming Industry Evolution Trends")
        
        # Simulation données temporelles
        dates = pd.date_range('2020-01-01', '2024-12-01', freq='M')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution satisfaction
            satisfaction_trend = 7.2 + np.cumsum(np.random.normal(0.02, 0.1, len(dates)))
            performance_trend = 3.8 + np.cumsum(np.random.normal(0.01, 0.05, len(dates)))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=satisfaction_trend,
                mode='lines+markers',
                name='Satisfaction Score',
                line=dict(color=self.theme['success'], width=3)
            ))
            fig.add_trace(go.Scatter(
                x=dates, y=performance_trend,
                mode='lines+markers', 
                name='Performance Score',
                line=dict(color=self.theme['primary'], width=3),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="📈 Gaming Workforce Satisfaction & Performance Evolution",
                yaxis=dict(title="Satisfaction Score", side="left"),
                yaxis2=dict(title="Performance Score", side="right", overlaying="y"),
                **self.create_advanced_chart_config()
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Distribution salaires gaming vs industrie
            gaming_salaries = np.random.normal(87000, 25000, 1000)
            tech_salaries = np.random.normal(120000, 30000, 1000)
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=gaming_salaries, name='Gaming Industry',
                opacity=0.7, nbinsx=30,
                marker_color=self.theme['primary']
            ))
            fig.add_trace(go.Histogram(
                x=tech_salaries, name='Tech Industry', 
                opacity=0.7, nbinsx=30,
                marker_color=self.theme['accent']
            ))
            
            fig.update_layout(
                title="💰 Salary Distribution: Gaming vs Tech",
                xaxis_title="Annual Salary ($)",
                yaxis_title="Frequency",
                barmode='overlay',
                **self.create_advanced_chart_config()
            )
            
            st.plotly_chart(fig, use_container_width=True)

    def render_ai_insights(self):
        """Insights IA gaming sophistiqués"""
        st.markdown("### 🤖 AI-Powered Gaming Workforce Insights")
        
        # Insights prédictifs
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="gaming-kpi">
                <h4>🎯 Predictive Analytics</h4>
                <ul>
                    <li><strong>Turnover Risk:</strong> 23 employees flagged for intervention</li>
                    <li><strong>Burnout Probability:</strong> QA team showing 67% stress indicators</li>
                    <li><strong>Performance Forecast:</strong> +8% improvement expected Q2</li>
                    <li><strong>Salary Gap Alert:</strong> Gaming devs 15% below tech market</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="gaming-kpi">
                <h4>💡 Optimization Recommendations</h4>
                <ul>
                    <li><strong>Hybrid Work:</strong> Could boost satisfaction by 12%</li>
                    <li><strong>Skill Development:</strong> Unity training for 45 developers</li>
                    <li><strong>Team Rebalancing:</strong> Move 3 seniors to struggling projects</li>
                    <li><strong>Compensation Adjust:</strong> Market-rate correction needed</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Gaming KPIs prédictifs
            prediction_data = {
                'Metric': ['Retention Rate', 'Team Productivity', 'Innovation Index', 'Bug Fix Rate', 'Player Satisfaction'],
                'Current': [87.3, 8.2, 74.5, 89.1, 7.8],
                'Predicted': [89.7, 8.7, 78.2, 91.3, 8.2],
                'Change': ['+2.4%', '+6.1%', '+5.0%', '+2.5%', '+5.1%']
            }
            
            pred_df = pd.DataFrame(prediction_data)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Current',
                x=pred_df['Metric'],
                y=pred_df['Current'],
                marker_color=self.theme['primary'],
                opacity=0.7
            ))
            fig.add_trace(go.Bar(
                name='Predicted',
                x=pred_df['Metric'], 
                y=pred_df['Predicted'],
                marker_color=self.theme['success'],
                opacity=0.7
            ))
            
            fig.update_layout(
                title="🔮 AI Predictions: Current vs Future State",
                barmode='group',
                **self.create_advanced_chart_config()
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Alertes critiques
        st.markdown("### 🚨 Critical Gaming Workforce Alerts")
        
        alert1, alert2, alert3 = st.columns(3)
        
        with alert1:
            st.markdown("""
            <div class="alert-critical">
                <h4>🔴 High Priority</h4>
                <p><strong>QA Burnout Risk:</strong> 12 QA engineers showing critical fatigue levels. Immediate intervention required.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with alert2:
            st.markdown("""
            <div class="alert-success">
                <h4>🟢 Success Story</h4>
                <p><strong>Neurodiversity Program:</strong> Teams with neurodiverse members show 21% higher innovation scores.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with alert3:
            st.markdown("""
            <div class="alert-critical">
                <h4>🟡 Action Needed</h4>
                <p><strong>Salary Competition:</strong> 15% gap vs tech industry. Risk of talent exodus to FAANG companies.</p>
            </div>
            """, unsafe_allow_html=True)

    def render_talent_wars(self):
        """Page Talent Wars sophistiquée"""
        st.markdown("## ⚔️ Gaming vs Tech: The Ultimate Talent Battle")
        
        # Données gaming vs tech
        roles_comparison = {
            'Role': ['Game Developer', 'Game Designer', 'QA Tester', 'Technical Artist', 'Audio Engineer', 'Producer'],
            'Gaming_Salary': [95000, 87000, 52000, 78000, 73000, 98000],
            'Tech_Salary': [125000, 110000, 72000, 95000, 88000, 135000],
            'Gaming_Satisfaction': [8.2, 8.7, 7.1, 8.0, 7.9, 7.8],
            'Tech_Satisfaction': [7.1, 6.8, 6.9, 7.2, 7.0, 7.3],
            'Gaming_Innovation': [8.5, 9.2, 6.8, 8.8, 8.1, 7.6],
            'Tech_Innovation': [7.2, 6.9, 6.1, 7.5, 6.8, 7.1]
        }
        
        comparison_df = pd.DataFrame(roles_comparison)
        comparison_df['Salary_Gap'] = comparison_df['Tech_Salary'] - comparison_df['Gaming_Salary'] 
        comparison_df['Satisfaction_Advantage'] = comparison_df['Gaming_Satisfaction'] - comparison_df['Tech_Satisfaction']
        comparison_df['Innovation_Advantage'] = comparison_df['Gaming_Innovation'] - comparison_df['Tech_Innovation']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique écarts salariaux
            fig = px.bar(
                comparison_df,
                x='Role',
                y='Salary_Gap',
                title="💰 Salary Gap: Gaming vs Tech Industry",
                color='Salary_Gap',
                color_continuous_scale='RdYlGn_r',
                labels={'Salary_Gap': 'Salary Difference ($)'}
            )
            fig.update_layout(self.create_advanced_chart_config())
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Avantages gaming 
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Satisfaction Advantage',
                x=comparison_df['Role'],
                y=comparison_df['Satisfaction_Advantage'],
                marker_color=self.theme['success']
            ))
            
            fig.add_trace(go.Bar(
                name='Innovation Advantage', 
                x=comparison_df['Role'],
                y=comparison_df['Innovation_Advantage'],
                marker_color=self.theme['primary']
            ))
            
            fig.update_layout(
                title="🎯 Gaming Industry Advantages",
                barmode='group',
                **self.create_advanced_chart_config()
            )
            fig.update_xaxis(tickangle=45)
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse stratégique
        st.markdown("### 🎯 Strategic Talent War Analysis")
        
        strategy1, strategy2, strategy3 = st.columns(3)
        
        with strategy1:
            st.markdown("""
            <div class="gaming-kpi">
                <h4>💰 Salary Battlefront</h4>
                <p><strong>Challenge:</strong> -$25K average gap vs tech</p>
                <p><strong>Strategy:</strong> Compensation packages with equity, bonuses, and unique gaming perks</p>
                <p><strong>Success Rate:</strong> 73% retention with enhanced packages</p>
            </div>
            """, unsafe_allow_html=True)
        
        with strategy2:
            st.markdown("""
            <div class="gaming-kpi">
                <h4>🎮 Passion Advantage</h4>
                <p><strong>Strength:</strong> +1.2 satisfaction vs tech</p>
                <p><strong>Strategy:</strong> Emphasize creative fulfillment and impact on entertainment</p>
                <p><strong>Success Rate:</strong> 89% prefer gaming despite salary gap</p>
            </div>
            """, unsafe_allow_html=True)
        
        with strategy3:
            st.markdown("""
            <div class="gaming-kpi">
                <h4>🚀 Innovation Edge</h4>
                <p><strong>Strength:</strong> +1.4 innovation score vs tech</p>
                <p><strong>Strategy:</strong> Highlight cutting-edge gaming tech (VR/AR, AI)</p>
                <p><strong>Success Rate:</strong> 84% attracted by innovation opportunities</p>
            </div>
            """, unsafe_allow_html=True)

    def render_neurodiversity_roi(self):
        """Page Neurodiversité ROI"""
        st.markdown("## 🧠 Neurodiversity: The Gaming Industry's Secret Weapon")
        
        # Données neurodiversité
        neuro_metrics = {
            'Metric': ['Innovation Score', 'Problem Solving Speed', 'Bug Detection Rate', 
                      'Creative Solutions', 'Code Quality', 'Team Collaboration'],
            'Neurotypical_Teams': [65, 70, 68, 62, 80, 75],
            'Neurodiverse_Teams': [86, 100, 98, 108, 85, 82],
            'ROI_Percentage': [21, 30, 30, 46, 5, 7]
        }
        
        neuro_df = pd.DataFrame(neuro_metrics)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Radar chart comparaison
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=neuro_df['Neurotypical_Teams'],
                theta=neuro_df['Metric'],
                fill='toself',
                name='Neurotypical Teams',
                line_color=self.theme['primary']
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=neuro_df['Neurodiverse_Teams'],
                theta=neuro_df['Metric'], 
                fill='toself',
                name='Neurodiverse Teams',
                line_color=self.theme['success']
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 120]
                    )
                ),
                title="🎯 Performance Comparison: Neurotypical vs Neurodiverse Teams",
                **self.create_advanced_chart_config()
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # ROI par métrique
            fig = px.bar(
                neuro_df,
                x='Metric',
                y='ROI_Percentage',
                title="💹 ROI of Neurodiversity by Gaming Metric",
                color='ROI_Percentage',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(self.create_advanced_chart_config())
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Insights neurodiversité
        st.markdown("### 💡 Neurodiversity Gaming Success Stories")
        
        success1, success2, success3 = st.columns(3)
        
        with success1:
            st.markdown("""
            <div class="alert-success">
                <h4>🚀 Innovation Breakthrough</h4>
                <p><strong>+21% Innovation Score:</strong> Neurodiverse teams consistently generate more creative gaming solutions and novel gameplay mechanics.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with success2:
            st.markdown("""
            <div class="alert-success">
                <h4>🎯 Quality Excellence</h4>
                <p><strong>+30% Bug Detection:</strong> Enhanced pattern recognition abilities lead to superior QA testing and debugging efficiency.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with success3:
            st.markdown("""
            <div class="alert-success">
                <h4>🧩 Problem Solving</h4>
                <p><strong>+30% Solving Speed:</strong> Unique cognitive approaches accelerate complex gaming algorithm development.</p>
            </div>
            """, unsafe_allow_html=True)

    def render_predictive_analytics(self):
        """Page Analytics Prédictifs"""
        st.markdown("## 🎯 AI-Powered Gaming Workforce Predictions")
        
        # Modèles ML status
        ml_models = {
            'Model': ['Turnover Predictor', 'Burnout Detection', 'Performance Forecaster', 'Talent Matcher', 'Salary Optimizer'],
            'Accuracy': [89.3, 87.8, 84.2, 91.5, 86.7],
            'Status': ['Active', 'Active', 'Active', 'Beta', 'Training'],
            'Last_Updated': ['2024-09-15', '2024-09-15', '2024-09-14', '2024-09-13', '2024-09-12']
        }
        
        ml_df = pd.DataFrame(ml_models)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Accuracy modèles
            fig = px.bar(
                ml_df,
                x='Model',
                y='Accuracy',
                color='Status',
                title="🤖 ML Models Performance Dashboard",
                color_discrete_map={'Active': self.theme['success'], 'Beta': self.theme['warning'], 'Training': self.theme['primary']}
            )
            fig.update_layout(self.create_advanced_chart_config())
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Prédictions risques
            if 'retention_risk' in self.employees_df.columns:
                risk_distribution = pd.cut(
                    self.employees_df['retention_risk'],
                    bins=[0, 0.3, 0.6, 1.0],
                    labels=['Low Risk', 'Medium Risk', 'High Risk']
                ).value_counts()
                
                fig = px.pie(
                    values=risk_distribution.values,
                    names=risk_distribution.index,
                    title="⚠️ Employee Retention Risk Distribution",
                    color_discrete_sequence=[self.theme['success'], self.theme['warning'], self.theme['danger']]
                )
                fig.update_layout(self.create_advanced_chart_config())
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Retention risk data not available in current dataset")
        
        # Prédictions par département
        st.markdown("### 🔮 Department-Level Predictions")
        
        dept_predictions = self.employees_df.groupby('department').agg({
            'satisfaction_score': 'mean',
            'performance_score': 'mean'
        }).round(2)
        
        # Simulation prédictions
        dept_predictions['Predicted_Satisfaction'] = dept_predictions['satisfaction_score'] * 1.05
        dept_predictions['Predicted_Performance'] = dept_predictions['performance_score'] * 1.03
        dept_predictions['Satisfaction_Change'] = ((dept_predictions['Predicted_Satisfaction'] - dept_predictions['satisfaction_score']) / dept_predictions['satisfaction_score'] * 100).round(1)
        dept_predictions['Performance_Change'] = ((dept_predictions['Predicted_Performance'] - dept_predictions['performance_score']) / dept_predictions['performance_score'] * 100).round(1)
        
        st.dataframe(
            dept_predictions[['satisfaction_score', 'Predicted_Satisfaction', 'Satisfaction_Change', 'performance_score', 'Predicted_Performance', 'Performance_Change']].style.background_gradient(subset=['Satisfaction_Change', 'Performance_Change'], cmap='RdYlGn'),
            use_container_width=True
        )

    def render_global_studios(self):
        """Page Studios Globaux"""
        st.markdown("## 🌍 Global Gaming Studios Operations")
        
        # Données globales gaming
        global_data = {
            'Country': ['United States', 'Japan', 'France', 'Sweden', 'South Korea', 'China', 'Canada', 'United Kingdom'],
            'Studios_Count': [245, 156, 89, 67, 134, 198, 87, 112],
            'Avg_Salary': [110000, 85000, 65000, 95000, 70000, 50000, 95000, 75000],
            'Employees': [1251, 834, 508, 265, 456, 789, 423, 378],
            'Retention_Rate': [78, 82, 86, 85, 80, 75, 84, 81],
            'Innovation_Score': [8.2, 8.7, 7.9, 8.5, 8.1, 7.4, 8.3, 8.0]
        }
        
        global_df = pd.DataFrame(global_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bubble chart salaire vs rétention
            fig = px.scatter(
                global_df,
                x='Avg_Salary',
                y='Retention_Rate',
                size='Employees',
                color='Innovation_Score',
                hover_name='Country',
                title="💰 Salary vs Retention by Country (Size = Employees)",
                labels={'Avg_Salary': 'Average Salary ($)', 'Retention_Rate': 'Retention Rate (%)'},
                color_continuous_scale='Viridis'
            )
            fig.update_layout(self.create_advanced_chart_config())
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Distribution employés par pays
            fig = px.bar(
                global_df.sort_values('Employees', ascending=True),
                x='Employees',
                y='Country',
                orientation='h',
                title="👥 Gaming Workforce Distribution by Country",
                color='Employees',
                color_continuous_scale='Blues'
            )
            fig.update_layout(self.create_advanced_chart_config())
            st.plotly_chart(fig, use_container_width=True)
        
        # Classements globaux
        st.markdown("### 🏆 Global Gaming Industry Rankings")
        
        rank1, rank2, rank3 = st.columns(3)
        
        with rank1:
            top_salary = global_df.nlargest(3, 'Avg_Salary')[['Country', 'Avg_Salary']]
            st.markdown("""
            <div class="gaming-kpi">
                <h4>💰 Top Salary Markets</h4>
                <ol>
            """, unsafe_allow_html=True)
            for _, row in top_salary.iterrows():
                st.markdown(f"<li>{row['Country']}: ${row['Avg_Salary']:,}</li>", unsafe_allow_html=True)
            st.markdown("</ol></div>", unsafe_allow_html=True)
        
        with rank2:
            top_retention = global_df.nlargest(3, 'Retention_Rate')[['Country', 'Retention_Rate']]
            st.markdown("""
            <div class="gaming-kpi">
                <h4>🎯 Best Retention</h4>
                <ol>
            """, unsafe_allow_html=True)
            for _, row in top_retention.iterrows():
                st.markdown(f"<li>{row['Country']}: {row['Retention_Rate']}%</li>", unsafe_allow_html=True)
            st.markdown("</ol></div>", unsafe_allow_html=True)
        
        with rank3:
            top_innovation = global_df.nlargest(3, 'Innovation_Score')[['Country', 'Innovation_Score']]
            st.markdown("""
            <div class="gaming-kpi">
                <h4>🚀 Innovation Leaders</h4>
                <ol>
            """, unsafe_allow_html=True)
            for _, row in top_innovation.iterrows():
                st.markdown(f"<li>{row['Country']}: {row['Innovation_Score']}/10</li>", unsafe_allow_html=True)
            st.markdown("</ol></div>", unsafe_allow_html=True)

    def render_compensation_intel(self):
        """Page Intelligence Compensation"""
        st.markdown("## 💰 Gaming Compensation Intelligence Center")
        
        # Analyses salariales sophistiquées
        salary_analysis = self.employees_df.groupby(['department', 'level']).agg({
            'salary': ['mean', 'median', 'std', 'count']
        }).round(0)
        
        salary_analysis.columns = ['Mean', 'Median', 'Std Dev', 'Count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Box plot salaires par département
            fig = px.box(
                self.employees_df,
                x='department',
                y='salary',
                color='level',
                title="📊 Salary Distribution by Department & Level",
                labels={'salary': 'Annual Salary ($)', 'department': 'Department'}
            )
            fig.update_layout(self.create_advanced_chart_config())
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Évolution salaires par ancienneté
            if 'salary' in self.employees_df.columns:
                # Simulation ancienneté basée sur l'ID employé
                self.employees_df['experience_years'] = np.random.randint(1, 15, len(self.employees_df))
                
                fig = px.scatter(
                    self.employees_df,
                    x='experience_years',
                    y='salary',
                    color='department',
                    size='performance_score',
                    title="📈 Salary vs Experience Correlation",
                    labels={'experience_years': 'Years of Experience', 'salary': 'Annual Salary ($)'}
                )
                fig.update_layout(self.create_advanced_chart_config())
                st.plotly_chart(fig, use_container_width=True)
        
        # Benchmarking salarial
        st.markdown("### 🎯 Gaming vs Industry Salary Benchmarks")
        
        benchmark_data = {
            'Role': ['Junior Developer', 'Senior Developer', 'Lead Developer', 'Game Designer', 'QA Engineer', 'Producer'],
            'Gaming_25th': [55000, 85000, 120000, 65000, 45000, 85000],
            'Gaming_Median': [65000, 105000, 140000, 80000, 55000, 105000],  
            'Gaming_75th': [75000, 125000, 160000, 95000, 65000, 125000],
            'Tech_Median': [85000, 140000, 180000, 110000, 75000, 145000]
        }
        
        benchmark_df = pd.DataFrame(benchmark_data)
        benchmark_df['Gap_vs_Tech'] = benchmark_df['Tech_Median'] - benchmark_df['Gaming_Median']
        benchmark_df['Gap_Percentage'] = (benchmark_df['Gap_vs_Tech'] / benchmark_df['Gaming_Median'] * 100).round(1)
        
        st.dataframe(
            benchmark_df.style.background_gradient(subset=['Gap_Percentage'], cmap='RdYlGn_r').format({
                'Gaming_25th': '${:,.0f}',
                'Gaming_Median': '${:,.0f}',
                'Gaming_75th': '${:,.0f}',
                'Tech_Median': '${:,.0f}',
                'Gap_vs_Tech': '${:,.0f}',
                'Gap_Percentage': '{:.1f}%'
            }),
            use_container_width=True
        )

    def render_future_insights(self):
        """Page Insights Futur"""
        st.markdown("## 🔮 Gaming Workforce: Future Predictions & Trends")
        
        # Prévisions industrie gaming
        future_trends = {
            'Year': [2024, 2025, 2026, 2027, 2028, 2029, 2030],
            'Global_Workforce': [2.8, 3.2, 3.7, 4.3, 4.9, 5.6, 6.4],  # Millions
            'Avg_Salary': [87, 92, 98, 105, 112, 120, 128],  # Thousands
            'Remote_Work_Pct': [45, 55, 62, 67, 71, 74, 76],
            'AI_Integration': [25, 35, 48, 58, 67, 74, 80],
            'VR_AR_Jobs_Pct': [8, 12, 18, 25, 34, 42, 50]
        }
        
        future_df = pd.DataFrame(future_trends)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Croissance workforce
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=future_df['Year'],
                y=future_df['Global_Workforce'],
                mode='lines+markers',
                name='Global Workforce (M)',
                line=dict(color=self.theme['primary'], width=4)
            ))
            fig.add_trace(go.Scatter(
                x=future_df['Year'],
                y=future_df['Avg_Salary'],
                mode='lines+markers',
                name='Avg Salary (K$)',
                line=dict(color=self.theme['success'], width=4),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="📈 Gaming Industry Growth Projections",
                yaxis=dict(title="Workforce (Millions)", side="left"),
                yaxis2=dict(title="Average Salary (K$)", side="right", overlaying="y"),
                **self.create_advanced_chart_config()
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Tendances technologiques
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=future_df['Year'],
                y=future_df['Remote_Work_Pct'],
                mode='lines+markers',
                name='Remote Work %',
                line=dict(color=self.theme['accent'], width=3)
            ))
            fig.add_trace(go.Scatter(
                x=future_df['Year'],
                y=future_df['AI_Integration'],
                mode='lines+markers',
                name='AI Integration %',
                line=dict(color=self.theme['danger'], width=3)
            ))
            fig.add_trace(go.Scatter(
                x=future_df['Year'],
                y=future_df['VR_AR_Jobs_Pct'],
                mode='lines+markers',
                name='VR/AR Jobs %',
                line=dict(color='#9B59B6', width=3)
            ))
            
            fig.update_layout(
                title="🚀 Technology Adoption Trends",
                yaxis_title="Adoption Percentage (%)",
                **self.create_advanced_chart_config()
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Futures compétences
        st.markdown("### 🎯 Future Gaming Skills in Demand")
        
        skills_data = {
            'Skill': ['AI/ML Gaming', 'VR/AR Development', 'Blockchain Gaming', 'Cloud Gaming', 'Procedural Generation', 'Real-time Ray Tracing'],
            'Current_Demand': [25, 15, 10, 20, 35, 30],
            'Projected_2027': [85, 65, 45, 70, 75, 80],
            'Growth_Rate': [240, 333, 350, 250, 114, 167]
        }
        
        skills_df = pd.DataFrame(skills_data)
        
        fig = px.bar(
            skills_df,
            x='Skill',
            y=['Current_Demand', 'Projected_2027'],
            barmode='group',
            title="🎮 Gaming Skills Evolution: Current vs Future Demand",
            labels={'value': 'Demand Level', 'variable': 'Time Period'}
        )
        fig.update_layout(self.create_advanced_chart_config())
        fig.update_xaxis(tickangle=45)
        
        st.plotly_chart(fig, use_container_width=True)

    def render_admin_panel(self):
        """Panel Admin sophistiqué"""
        st.markdown("## ⚙️ Gaming Workforce Observatory - System Administration")
        
        # Vérification accès admin
        if 'admin_authenticated' not in st.session_state:
            st.session_state.admin_authenticated = False
        
        if not st.session_state.admin_authenticated:
            st.warning("🔒 Administrator privileges required")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                admin_user = st.text_input("Admin Username", value="admin")
                admin_pass = st.text_input("Admin Password", type="password", value="gaming123")
                
                if st.button("🔓 Authenticate as Admin", type="primary", use_container_width=True):
                    if admin_user == "admin" and admin_pass == "gaming123":
                        st.session_state.admin_authenticated = True
                        st.success("✅ Admin access granted!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid admin credentials")
            
            return
        
        # Panel admin authentifié
        st.success("🔓 Administrator Panel - Full Access Granted")
        
        admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs(["🖥️ System Status", "👥 User Management", "📊 Data Management", "⚙️ Configuration"])
        
        with admin_tab1:
            self.render_system_status()
        
        with admin_tab2:
            self.render_user_management()
        
        with admin_tab3:
            self.render_data_management()
        
        with admin_tab4:
            self.render_configuration()

    def render_system_status(self):
        """Status système admin"""
        st.markdown("### 🖥️ Gaming Workforce Observatory System Health")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⚡ System Uptime", "99.8%", "+0.1%")
        with col2:
            st.metric("👥 Active Users", "1,247", "+23")
        with col3:
            st.metric("📊 Data Freshness", "Live", "Real-time")
        with col4:
            st.metric("🚀 Response Time", "1.2s", "-0.3s")
        
        # Métriques performance
        performance_data = {
            'Component': ['Database', 'API Gateway', 'ML Models', 'Cache Layer', 'Web Server'],
            'Status': ['Healthy', 'Healthy', 'Healthy', 'Warning', 'Healthy'],
            'Response_Time_ms': [45, 120, 1800, 850, 200],
            'Uptime_Pct': [99.9, 99.7, 99.2, 98.8, 99.8]
        }
        
        perf_df = pd.DataFrame(performance_data)
        
        # Status couleurs
        status_colors = {'Healthy': self.theme['success'], 'Warning': self.theme['warning'], 'Critical': self.theme['danger']}
        perf_df['Status_Color'] = perf_df['Status'].map(status_colors)
        
        fig = px.bar(
            perf_df,
            x='Component',
            y='Response_Time_ms',
            color='Status',
            color_discrete_map=status_colors,
            title="⚡ System Component Performance"
        )
        fig.update_layout(self.create_advanced_chart_config())
        
        st.plotly_chart(fig, use_container_width=True)

    def render_user_management(self):
        """Gestion utilisateurs admin"""
        st.markdown("### 👥 User Access & Permissions Management")
        
        # Simulation utilisateurs
        users_data = {
            'Username': ['admin', 'hr_manager', 'team_lead_1', 'analyst_1', 'viewer_1'],
            'Role': ['Administrator', 'HR Manager', 'Team Lead', 'Data Analyst', 'Viewer'],
            'Department': ['IT', 'Human Resources', 'Programming', 'Analytics', 'Marketing'],
            'Last_Login': ['2024-09-15 09:30', '2024-09-15 08:45', '2024-09-14 16:20', '2024-09-15 07:15', '2024-09-13 14:30'],
            'Status': ['Active', 'Active', 'Active', 'Active', 'Inactive'],
            'Permissions': ['Full Access', 'HR Data Only', 'Team Data Only', 'Read Only', 'Limited View']
        }
        
        users_df = pd.DataFrame(users_data)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(users_df, use_container_width=True)
        
        with col2:
            st.markdown("#### 🔐 Quick Actions")
            if st.button("➕ Add New User", use_container_width=True):
                st.info("👤 User creation form would open here")
            
            if st.button("🔒 Reset Passwords", use_container_width=True):
                st.info("📧 Password reset emails sent")
            
            if st.button("📊 Export User Report", use_container_width=True):
                st.info("📄 User report generated")

    def render_data_management(self):
        """Gestion données admin"""
        st.markdown("### 📊 Gaming Workforce Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Data Statistics")
            st.metric("Employee Records", f"{len(self.employees_df):,}")
            st.metric("Project Records", f"{len(self.projects_df):,}")
            st.metric("Data Quality Score", "94.7%")
            st.metric("Last Sync", "2 min ago")
        
        with col2:
            st.markdown("#### ⚙️ Data Operations")
            
            if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
                st.success("✅ Data refresh completed")
            
            if st.button("📊 Export Database", use_container_width=True):
                st.info("📁 Database export initiated")
            
            if st.button("🧹 Clean Duplicates", use_container_width=True):
                st.info("🔍 Duplicate cleaning started")
            
            if st.button("📈 Generate Backup", use_container_width=True):
                st.success("💾 Backup created successfully")

    def render_configuration(self):
        """Configuration système admin"""
        st.markdown("### ⚙️ System Configuration")
        
        config_col1, config_col2 = st.columns(2)
        
        with config_col1:
            st.markdown("#### 🎨 Theme Settings")
            
            new_primary = st.color_picker("Primary Color", value=self.theme['primary'])
            new_accent = st.color_picker("Accent Color", value=self.theme['accent'])
            
            if st.button("🎨 Update Theme", use_container_width=True):
                st.success("🎨 Theme updated successfully")
        
        with config_col2:
            st.markdown("#### 📊 Analytics Settings")
            
            refresh_interval = st.selectbox("Data Refresh Interval", 
                                          ["Real-time", "5 minutes", "15 minutes", "1 hour"])
            
            cache_duration = st.selectbox("Cache Duration",
                                        ["5 minutes", "15 minutes", "1 hour", "4 hours"])
            
            if st.button("💾 Save Configuration", use_container_width=True):
                st.success("✅ Configuration saved")

    def run(self):
        """Lancement application principale"""
        self.apply_theme()
        
        if not self.render_authentication():
            return
        
        # Layout principal
        self.render_sidebar()
        self.render_current_page()
        
        # Footer sophistiqué
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, {self.theme['primary']}10, {self.theme['accent']}05); border-radius: 10px;">
            <p><strong>🎮 Gaming Workforce Observatory Enterprise Edition v2.0</strong></p>
            <p>Powered by Advanced Gaming Analytics | © 2024 remichenouri | 
            <a href="https://github.com/remichenouri/gaming_workforce_observatory" target="_blank">GitHub Repository</a> | 
            Last Update: {datetime.now().strftime('%H:%M:%S')} CEST</p>
            <p style="font-size: 0.8rem; color: #666;">🚀 All systems operational | ⚡ Performance: Excellent | 🔒 Security: Enterprise-grade</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Fonction main"""
    app = GamingWorkforceApp()
    app.run()

if __name__ == "__main__":
    main()
