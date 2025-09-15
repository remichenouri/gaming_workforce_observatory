"""
🎮 Ubisoft Gaming Workforce Observatory
Executive Dashboard - C-Suite Strategic Workforce Intelligence
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Ubisoft Gaming Workforce Observatory - Executive Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 📊 KPI METRICS UBISOFT - Section Executive
st.markdown("## 🎯 Ubisoft Global Workforce Metrics")

# Génération de données exemple pour Ubisoft
ubisoft_metrics = [
    {"title": "Ubisoft Talent Pool", "value": "2,847", "delta": "+12% vs Q3", "icon": "👥"},
    {"title": "Studios Worldwide", "value": "25", "delta": "Global Presence", "icon": "🌍"},
    {"title": "Retention Rate", "value": "87.3%", "delta": "+5.2% YoY", "icon": "🎯"},
    {"title": "Innovation Index", "value": "94/100", "delta": "Industry Leading", "icon": "🚀"}
]

create_ubisoft_metric_cols(ubisoft_metrics)

# 🌍 Section Studios Ubisoft Worldwide
st.markdown("## 🌍 Ubisoft Global Studios Performance")

col1, col2 = st.columns([2, 1])

with col1:
    # Chart performance studios
    studios_data = {
        'Studio': ['Montreal', 'Paris', 'Milan', 'Shanghai', 'Toronto', 'San Francisco', 'Barcelona', 'Kiev'],
        'Employees': [3200, 2800, 1200, 980, 850, 650, 400, 320],
        'Performance': [94, 91, 88, 85, 89, 87, 84, 82],
        'Projects': [8, 6, 4, 3, 4, 3, 2, 2]
    }
    
    df_studios = pd.DataFrame(studios_data)
    
    fig_studios = px.scatter(
        df_studios, 
        x='Employees', 
        y='Performance',
        size='Projects',
        color='Performance',
        hover_name='Studio',
        title="🎮 Ubisoft Studios: Workforce vs Performance",
        color_continuous_scale=['#0066CC', '#0099FF', '#00CCFF']
    )
    
    fig_studios.update_layout(get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_studios, use_container_width=True)

with col2:
    st.markdown(
        create_ubisoft_info_box(
            "Ubisoft's Global Excellence",
            "Les studios Ubisoft maintiennent des standards d'excellence mondiaux avec une performance moyenne de 87.3% across all locations."
        ),
        unsafe_allow_html=True
    )
    
    # Top performers
    st.markdown("### 🏆 Top Performing Studios")
    for i, row in df_studios.nlargest(3, 'Performance').iterrows():
        st.markdown(f"""
        **{row['Studio']}** - {row['Performance']}%  
        👥 {row['Employees']:,} talents • 🎮 {row['Projects']} projets
        """)

# 📈 Section Trends et Predictive Analytics
st.markdown("## 📈 Ubisoft Workforce Trends & Predictions")

col1, col2 = st.columns(2)

with col1:
    # Trend analysis
    months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    trend_data = {
        'Month': months,
        'Headcount': [2650 + i*15 + np.random.randint(-20, 30) for i in range(len(months))],
        'Satisfaction': [85 + np.random.randint(-3, 5) for _ in range(len(months))],
        'Productivity': [88 + np.random.randint(-4, 6) for _ in range(len(months))]
    }
    
    df_trends = pd.DataFrame(trend_data)
    
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(
        x=df_trends['Month'], 
        y=df_trends['Headcount'],
        mode='lines+markers',
        name='Total Headcount Ubisoft',
        line=dict(color=UBISOFT_COLORS['primary'], width=3)
    ))
    
    fig_trends.update_layout(
        title="🎮 Ubisoft Headcount Evolution 2024",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)

with col2:
    # Satisfaction & Productivity
    fig_satisfaction = go.Figure()
    
    fig_satisfaction.add_trace(go.Scatter(
        x=df_trends['Month'],
        y=df_trends['Satisfaction'],
        mode='lines+markers',
        name='Satisfaction Score',
        line=dict(color=UBISOFT_COLORS['accent'], width=2)
    ))
    
    fig_satisfaction.add_trace(go.Scatter(
        x=df_trends['Month'],
        y=df_trends['Productivity'],
        mode='lines+markers',
        name='Productivity Index',
        line=dict(color=UBISOFT_COLORS['primary'], width=2)
    ))
    
    fig_satisfaction.update_layout(
        title="🎯 Ubisoft Employee Satisfaction & Productivity",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_satisfaction, use_container_width=True)

# 🎮 Section Gaming Industry Benchmarks
st.markdown("## 🎮 Ubisoft vs Gaming Industry Benchmarks")

benchmark_data = {
    'Metric': ['Retention Rate', 'Sprint Velocity', 'Bug Fix Rate', 'Employee NPS', 'Innovation Index'],
    'Gaming Industry Avg': [68, 35, 78, 6.8, 65],
    'Ubisoft Performance': [87, 42, 85, 7.8, 94],
    'Target': [85, 40, 85, 7.5, 75]
}

df_benchmark = pd.DataFrame(benchmark_data)

fig_benchmark = go.Figure()

fig_benchmark.add_trace(go.Bar(
    name='Gaming Industry Average',
    x=df_benchmark['Metric'],
    y=df_benchmark['Gaming Industry Avg'],
    marker_color='rgba(100, 100, 100, 0.6)'
))

fig_benchmark.add_trace(go.Bar(
    name='Ubisoft Performance',
    x=df_benchmark['Metric'],
    y=df_benchmark['Ubisoft Performance'],
    marker_color=UBISOFT_COLORS['primary']
))

fig_benchmark.add_trace(go.Scatter(
    name='Ubisoft Target',
    x=df_benchmark['Metric'],
    y=df_benchmark['Target'],
    mode='markers',
    marker=dict(color=UBISOFT_COLORS['accent'], size=12, symbol='diamond')
))

fig_benchmark.update_layout(
    title="🏆 Ubisoft Excellence vs Industry Standards",
    barmode='group',
    **get_ubisoft_chart_config()['layout']
)

st.plotly_chart(fig_benchmark, use_container_width=True)

# 🚀 AI Predictions Section
st.markdown("## 🤖 Ubisoft AI-Powered Workforce Predictions")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">🔮 Turnover Risk</h4>
        <div style="font-size: 2.5rem; color: #E60012; font-weight: 700;">3.2%</div>
        <p style="color: #F5F5F5; margin: 15px 0 0 0;">
            Low risk identified across Ubisoft studios. ML model accuracy: 89%
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">⚡ Burnout Prevention</h4>
        <div style="font-size: 2.5rem; color: #28A745; font-weight: 700;">92%</div>
        <p style="color: #F5F5F5; margin: 15px 0 0 0;">
            Proactive intervention success rate in Ubisoft development teams
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">🎯 Hiring Forecast</h4>
        <div style="font-size: 2.5rem; color: #0099FF; font-weight: 700;">+340</div>
        <p style="color: #F5F5F5; margin: 15px 0 0 0;">
            Projected new hires Q1 2025 across Ubisoft worldwide studios
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer Ubisoft
st.markdown(display_ubisoft_logo_section(), unsafe_allow_html=True)

# Sidebar avec informations Ubisoft
with st.sidebar:
    st.markdown("""
    ## 🎮 Ubisoft Gaming Workforce Observatory
    
    **Executive Dashboard**
    
    📊 **Real-time KPIs** pour les dirigeants Ubisoft
    
    🌍 **Global Studios** performance tracking
    
    🤖 **AI-Powered** predictions et insights
    
    ---
    
    ### 🏢 Ubisoft Worldwide
    - 🇨🇦 Montreal (HQ)
    - 🇫🇷 Paris
    - 🇮🇹 Milan  
    - 🇨🇳 Shanghai
    - 🇺🇸 San Francisco
    - 🇪🇸 Barcelona
    
    ---
    
    **🔄 Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """.format(datetime=datetime))
