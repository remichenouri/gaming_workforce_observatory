"""
Gaming Workforce Observatory - Executive Dashboard
Dashboard C-level avec métriques stratégiques gaming workforce
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

# Ajout du chemin pour imports
sys.path.append(str(Path(__file__).parent.parent))

from src.themes.gaming_themes import GamingThemes
from src.visualizations.interactive_charts import GamingInteractiveCharts
from src.ml.models.attrition_predictor import GamingAttritionPredictor
from src.utils.notification_manager import GamingNotificationManager
from src.utils.export_manager import GamingExportManager

def initialize_dashboard():
    """Initialise le dashboard avec thème gaming"""
    st.set_page_config(
        page_title="🎮 Gaming Workforce Observatory - Executive Dashboard",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Application du thème gaming
    themes = GamingThemes()
    themes.apply_gaming_theme()
    themes.apply_ubisoft_branding()

def generate_executive_data():
    """Génère des données exécutives simulées"""
    
    # Métriques clés
    executive_metrics = {
        'total_workforce': 2850,
        'departments': 8,
        'active_projects': 23,
        'avg_tenure_years': 4.2,
        'overall_satisfaction': 7.3,
        'retention_rate': 87.5,
        'diversity_score': 72.8,
        'performance_index': 8.2
    }
    
    # Tendances mensuelles (12 derniers mois)
    months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
    
    monthly_trends = pd.DataFrame({
        'month': months,
        'headcount': np.random.randint(2800, 2900, 12),
        'satisfaction': np.random.uniform(7.0, 7.8, 12),
        'retention': np.random.uniform(85, 90, 12),
        'productivity': np.random.uniform(78, 88, 12),
        'recruitment': np.random.randint(15, 45, 12),
        'attrition': np.random.randint(8, 25, 12)
    })
    
    # Données départementales
    departments_data = pd.DataFrame({
        'department': ['Programming', 'Art & Animation', 'Game Design', 'Quality Assurance', 
                      'Production', 'Audio', 'Marketing', 'Operations'],
        'headcount': [950, 680, 420, 380, 180, 95, 85, 60],
        'avg_salary': [105000, 78000, 92000, 65000, 98000, 73000, 82000, 75000],
        'satisfaction': [7.8, 7.1, 7.5, 6.9, 7.4, 7.7, 7.2, 7.0],
        'retention_rate': [89.2, 85.1, 88.7, 82.3, 87.9, 91.2, 86.5, 83.8],
        'avg_experience': [5.2, 4.8, 4.5, 3.9, 6.1, 5.8, 4.2, 4.7],
        'performance_score': [8.4, 7.9, 8.1, 7.6, 8.2, 8.3, 7.8, 7.5],
        'budget_allocated': [45.2, 28.4, 18.7, 12.8, 8.9, 4.2, 3.5, 2.3]  # Millions USD
    })
    
    # KPIs stratégiques
    strategic_kpis = {
        'talent_acquisition': {
            'time_to_fill': 42,  # jours
            'cost_per_hire': 8500,  # USD
            'quality_of_hire': 8.1,
            'offer_acceptance_rate': 0.89
        },
        'engagement': {
            'employee_net_promoter_score': 68,
            'internal_mobility_rate': 0.23,
            'training_completion_rate': 0.91,
            'innovation_index': 7.8
        },
        'performance': {
            'revenue_per_employee': 285000,
            'project_success_rate': 0.87,
            'client_satisfaction': 8.9,
            'market_competitiveness': 0.78
        },
        'financial': {
            'total_compensation_budget': 298.5,  # Millions USD
            'roi_on_training': 3.2,
            'cost_savings_initiatives': 12.4,  # Millions USD
            'productivity_gains': 0.15  # 15% YoY
        }
    }
    
    return executive_metrics, monthly_trends, departments_data, strategic_kpis

def render_executive_summary(executive_metrics, strategic_kpis):
    """Affiche le résumé exécutif"""
    
    themes = GamingThemes()
    
    # Header exécutif
    header_html = themes.create_dashboard_header(
        "🎮 Gaming Workforce Observatory", 
        "Executive Dashboard - Strategic Workforce Intelligence"
    )
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Métriques principales - Row 1
    st.markdown("### 📊 Key Workforce Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_html = themes.create_metric_card(
            "Total Workforce", 
            f"{executive_metrics['total_workforce']:,}",
            "+85 this quarter",
            "success",
            "👥"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col2:
        metric_html = themes.create_metric_card(
            "Overall Satisfaction", 
            f"{executive_metrics['overall_satisfaction']}/10",
            "+0.3 vs last quarter",
            "info",
            "😊"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col3:
        metric_html = themes.create_metric_card(
            "Retention Rate", 
            f"{executive_metrics['retention_rate']:.1f}%",
            "+2.1% YoY",
            "success",
            "📈"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col4:
        metric_html = themes.create_metric_card(
            "Performance Index", 
            f"{executive_metrics['performance_index']}/10",
            "Above industry avg",
            "success",
            "🎯"
        )
        st.markdown(metric_html, unsafe_allow_html=True)

def render_strategic_kpis(strategic_kpis):
    """Affiche les KPIs stratégiques avec rings de progression"""
    
    themes = GamingThemes()
    
    st.markdown("### 🎯 Strategic Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 🎪 Talent Acquisition")
        
        # Ring de progression pour Quality of Hire
        ring_html = themes.create_progress_ring(
            strategic_kpis['talent_acquisition']['quality_of_hire'] * 10,
            "Quality of Hire",
            "primary"
        )
        st.markdown(ring_html, unsafe_allow_html=True)
        
        st.metric("Time to Fill", f"{strategic_kpis['talent_acquisition']['time_to_fill']} days")
        st.metric("Cost per Hire", f"${strategic_kpis['talent_acquisition']['cost_per_hire']:,}")
    
    with col2:
        st.markdown("#### 💡 Engagement")
        
        ring_html = themes.create_progress_ring(
            strategic_kpis['engagement']['employee_net_promoter_score'],
            "Employee NPS",
            "success"
        )
        st.markdown(ring_html, unsafe_allow_html=True)
        
        st.metric("Internal Mobility", f"{strategic_kpis['engagement']['internal_mobility_rate']:.1%}")
        st.metric("Training Completion", f"{strategic_kpis['engagement']['training_completion_rate']:.1%}")
    
    with col3:
        st.markdown("#### ⚡ Performance")
        
        ring_html = themes.create_progress_ring(
            strategic_kpis['performance']['project_success_rate'] * 100,
            "Project Success",
            "warning"
        )
        st.markdown(ring_html, unsafe_allow_html=True)
        
        st.metric("Revenue/Employee", f"${strategic_kpis['performance']['revenue_per_employee']:,}")
        st.metric("Client Satisfaction", f"{strategic_kpis['performance']['client_satisfaction']}/10")
    
    with col4:
        st.markdown("#### 💰 Financial Impact")
        
        ring_html = themes.create_progress_ring(
            strategic_kpis['financial']['roi_on_training'] * 25,  # Scaled for visual
            "ROI on Training",
            "accent"
        )
        st.markdown(ring_html, unsafe_allow_html=True)
        
        st.metric("Total Comp Budget", f"${strategic_kpis['financial']['total_compensation_budget']:.1f}M")
        st.metric("Productivity Gains", f"+{strategic_kpis['financial']['productivity_gains']:.1%}")

def render_department_overview(departments_data):
    """Vue d'ensemble des départements"""
    
    st.markdown("### 🏢 Department Overview & Performance")
    
    # Graphiques des départements
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition de l'effectif
        fig_headcount = px.treemap(
            departments_data,
            values='headcount',
            names='department',
            title='🌳 Workforce Distribution by Department',
            color='satisfaction',
            color_continuous_scale='RdYlGn',
            hover_data=['avg_salary', 'retention_rate']
        )
        
        fig_headcount.update_layout(
            font=dict(size=12),
            title_font_size=16,
            height=400
        )
        
        st.plotly_chart(fig_headcount, use_container_width=True)
    
    with col2:
        # Budget vs Performance
        fig_budget = px.scatter(
            departments_data,
            x='budget_allocated',
            y='performance_score',
            size='headcount',
            color='retention_rate',
            hover_name='department',
            title='💰 Budget Allocation vs Performance',
            labels={
                'budget_allocated': 'Budget Allocated (M USD)',
                'performance_score': 'Performance Score',
                'retention_rate': 'Retention Rate (%)'
            },
            color_continuous_scale='Viridis'
        )
        
        fig_budget.update_layout(height=400)
        st.plotly_chart(fig_budget, use_container_width=True)
    
    # Tableau détaillé des départements
    st.markdown("#### 📋 Department Details")
    
    # Formatage du tableau
    display_df = departments_data.copy()
    display_df['avg_salary'] = display_df['avg_salary'].apply(lambda x: f"${x:,}")
    display_df['satisfaction'] = display_df['satisfaction'].apply(lambda x: f"{x:.1f}/10")
    display_df['retention_rate'] = display_df['retention_rate'].apply(lambda x: f"{x:.1f}%")
    display_df['budget_allocated'] = display_df['budget_allocated'].apply(lambda x: f"${x:.1f}M")
    
    display_df.columns = [
        'Department', 'Headcount', 'Avg Salary', 'Satisfaction', 
        'Retention Rate', 'Avg Experience', 'Performance', 'Budget'
    ]
    
    st.dataframe(display_df, use_container_width=True, height=300)

def render_trends_analysis(monthly_trends):
    """Analyse des tendances temporelles"""
    
    st.markdown("### 📈 12-Month Trends Analysis")
    
    # Graphiques de tendances
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution de l'effectif et satisfaction
        fig_trends = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_trends.add_trace(
            go.Scatter(
                x=monthly_trends['month'],
                y=monthly_trends['headcount'],
                mode='lines+markers',
                name='Headcount',
                line=dict(color='#3498db', width=3)
            ),
            secondary_y=False
        )
        
        fig_trends.add_trace(
            go.Scatter(
                x=monthly_trends['month'],
                y=monthly_trends['satisfaction'],
                mode='lines+markers',
                name='Satisfaction',
                line=dict(color='#e74c3c', width=3)
            ),
            secondary_y=True
        )
        
        fig_trends.update_xaxes(title_text="Month")
        fig_trends.update_yaxes(title_text="Headcount", secondary_y=False)
        fig_trends.update_yaxes(title_text="Satisfaction Score", secondary_y=True)
        
        fig_trends.update_layout(
            title_text="👥 Workforce & Satisfaction Trends",
            height=400
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
    
    with col2:
        # Recrutement vs Attrition
        fig_hiring = go.Figure()
        
        fig_hiring.add_trace(go.Bar(
            x=monthly_trends['month'],
            y=monthly_trends['recruitment'],
            name='New Hires',
            marker_color='#27ae60'
        ))
        
        fig_hiring.add_trace(go.Bar(
            x=monthly_trends['month'],
            y=-monthly_trends['attrition'],  # Négatif pour visualisation
            name='Departures',
            marker_color='#e74c3c'
        ))
        
        fig_hiring.update_layout(
            title="🔄 Hiring vs Attrition Flow",
            barmode='relative',
            yaxis_title="Number of Employees",
            height=400
        )
        
        st.plotly_chart(fig_hiring, use_container_width=True)

def render_predictive_insights():
    """Insights prédictifs et alertes"""
    
    st.markdown("### 🔮 Predictive Insights & Alerts")
    
    # Simulated predictive data
    predictive_alerts = [
        {
            'priority': 'HIGH',
            'category': 'Attrition Risk',
            'message': 'QA department showing 23% higher attrition risk next quarter',
            'impact': 'Potential loss of 8-12 key QA engineers',
            'action': 'Immediate retention intervention recommended',
            'confidence': 0.87
        },
        {
            'priority': 'MEDIUM',
            'category': 'Skills Gap',
            'message': 'Unity expertise gap projected for Q2 2025',
            'impact': '3 major projects may face delays',
            'action': 'Accelerate Unity training program or external hiring',
            'confidence': 0.74
        },
        {
            'priority': 'LOW',
            'category': 'Compensation',
            'message': 'Art team salaries 8% below market average',
            'impact': 'Increased recruitment difficulty',
            'action': 'Review compensation bands for artists',
            'confidence': 0.92
        }
    ]
    
    # Affichage des alertes
    for i, alert in enumerate(predictive_alerts):
        
        priority_colors = {
            'HIGH': '#e74c3c',
            'MEDIUM': '#f39c12', 
            'LOW': '#3498db'
        }
        
        priority_icons = {
            'HIGH': '🚨',
            'MEDIUM': '⚠️',
            'LOW': 'ℹ️'
        }
        
        color = priority_colors[alert['priority']]
        icon = priority_icons[alert['priority']]
        
        with st.expander(f"{icon} {alert['category']} - {alert['priority']} Priority", expanded=(alert['priority'] == 'HIGH')):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Message:** {alert['message']}")
                st.markdown(f"**Business Impact:** {alert['impact']}")
                st.markdown(f"**Recommended Action:** {alert['action']}")
            
            with col2:
                st.metric(
                    "Confidence Level",
                    f"{alert['confidence']:.0%}",
                    help="ML model confidence in this prediction"
                )
    
    # Quick actions
    st.markdown("#### ⚡ Quick Executive Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 Send Alert to HR", type="primary"):
            st.success("Alert sent to HR leadership team")
    
    with col2:
        if st.button("📊 Generate Detailed Report"):
            st.success("Detailed analysis report queued for generation")
    
    with col3:
        if st.button("👥 Schedule Leadership Review"):
            st.success("Leadership review meeting scheduled")

def render_export_section():
    """Section d'export pour dirigeants"""
    
    st.markdown("### 📤 Executive Reports & Exports")
    
    export_manager = GamingExportManager()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Available Reports")
        
        report_types = [
            "📊 Executive Summary (PDF)",
            "📈 Monthly Board Report (PDF)", 
            "💰 Financial Impact Analysis (Excel)",
            "🎯 Strategic KPI Dashboard (Excel)",
            "⚠️ Risk Assessment Report (PDF)"
        ]
        
        selected_reports = st.multiselect(
            "Select reports to generate:",
            report_types,
            default=["📊 Executive Summary (PDF)"]
        )
        
        include_predictions = st.checkbox("Include Predictive Analytics", value=True)
        confidential_mode = st.checkbox("Mark as Confidential", value=True)
    
    with col2:
        st.markdown("#### ⚙️ Export Options")
        
        recipients = st.text_area(
            "Email recipients (one per line):",
            "ceo@company.com\ncfo@company.com\nchro@company.com"
        )
        
        schedule_frequency = st.selectbox(
            "Schedule Frequency:",
            ["One-time", "Weekly", "Monthly", "Quarterly"]
        )
        
        if st.button("📬 Generate & Send Reports", type="primary"):
            with st.spinner("Generating executive reports..."):
                # Simulation de génération de rapport
                import time
                time.sleep(2)
                
                st.success("✅ Reports generated and sent successfully!")
                
                # Affichage des liens de téléchargement simulés
                for report in selected_reports:
                    report_name = report.split()[-1].replace("(", "").replace(")", "")
                    filename = f"executive_{report_name.lower()}_{datetime.now().strftime('%Y%m%d')}"
                    st.markdown(f"📎 [{filename}] - Ready for download")

def main():
    """Fonction principale du dashboard exécutif"""
    
    initialize_dashboard()
    
    # Génération des données
    executive_metrics, monthly_trends, departments_data, strategic_kpis = generate_executive_data()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🎮 Executive Navigation")
        
        dashboard_sections = [
            "📊 Executive Summary",
            "🎯 Strategic KPIs", 
            "🏢 Department Overview",
            "📈 Trends Analysis",
            "🔮 Predictive Insights",
            "📤 Reports & Export"
        ]
        
        selected_section = st.selectbox(
            "Navigate to section:",
            dashboard_sections,
            index=0
        )
        
        # Configuration temps réel
        st.markdown("---")
        st.markdown("### ⚙️ Dashboard Settings")
        
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
        show_alerts = st.checkbox("Show Real-time Alerts", value=True)
        executive_view = st.selectbox("View Mode", ["Executive", "Detailed", "Presentation"])
        
        # Métriques de statut
        st.markdown("---")
        st.markdown("### 📊 System Status")
        st.metric("Data Freshness", "2 minutes ago")
        st.metric("Active Users", "47")
        
        # Indicateur de statut système
        themes = GamingThemes()
        status_html = themes.create_status_indicator('online', pulse=False)
        st.markdown(f"**System Status:** {status_html}", unsafe_allow_html=True)
    
    # Contenu principal basé sur la sélection
    if selected_section == "📊 Executive Summary":
        render_executive_summary(executive_metrics, strategic_kpis)
    
    elif selected_section == "🎯 Strategic KPIs":
        render_strategic_kpis(strategic_kpis)
        
        # Graphiques KPI additionnels
        st.markdown("### 📈 KPI Trends & Benchmarks")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # ROI sur formation
            fig_roi = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = strategic_kpis['financial']['roi_on_training'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "ROI on Training Investment"},
                delta = {'reference': 2.5},
                gauge = {
                    'axis': {'range': [None, 5]},
                    'bar': {'color': "#0082c4"},
                    'steps': [
                        {'range': [0, 2], 'color': "lightgray"},
                        {'range': [2, 3.5], 'color': "yellow"},
                        {'range': [3.5, 5], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 4
                    }
                }
            ))
            fig_roi.update_layout(height=300)
            st.plotly_chart(fig_roi, use_container_width=True)
        
        with col2:
            # Satisfaction vs Industrie
            benchmark_data = pd.DataFrame({
                'Metric': ['Our Company', 'Industry Average', 'Top Quartile'],
                'Satisfaction': [7.3, 6.8, 8.1],
                'Retention': [87.5, 84.2, 91.3]
            })
            
            fig_benchmark = px.bar(
                benchmark_data,
                x='Metric',
                y=['Satisfaction', 'Retention'],
                title='📊 Performance vs Industry Benchmarks',
                barmode='group',
                color_discrete_sequence=['#0082c4', '#ff6b35']
            )
            fig_benchmark.update_layout(height=300)
            st.plotly_chart(fig_benchmark, use_container_width=True)
    
    elif selected_section == "🏢 Department Overview":
        render_department_overview(departments_data)
    
    elif selected_section == "📈 Trends Analysis":
        render_trends_analysis(monthly_trends)
    
    elif selected_section == "🔮 Predictive Insights":
        render_predictive_insights()
    
    elif selected_section == "📤 Reports & Export":
        render_export_section()
    
    # Footer exécutif
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #7f8c8d; font-size: 12px;'>"
        "🎮 Gaming Workforce Observatory Enterprise | "
        f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        "Confidential Executive Dashboard"
        "</div>",
        unsafe_allow_html=True
    )
    
    # Auto-refresh si activé
    if auto_refresh:
        import time
        time.sleep(30)
        st.rerun()

if __name__ == "__main__":
    main()
