"""
🎮 Gaming Workforce Observatory - Predictive Analytics CORRIGÉ
Page Predictive Analytics sans erreurs d'import
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Configuration page
st.set_page_config(
    page_title="Gaming Workforce Observatory - Predictive Analytics",
    page_icon="🎯",
    layout="wide"
)

# THEME INTÉGRÉ (sans imports externes)
GAMING_COLORS = {
    'primary': '#0099FF',
    'accent': '#E60012',
    'success': '#28A745',
    'warning': '#FFB020',
    'text': '#2C3E50'
}

def apply_gaming_theme():
    """Application du thème gaming intégré"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #0099FF15, #E6001210);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border-left: 4px solid #0099FF;
    }
    .gaming-kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 4px solid #0099FF;
        margin: 0.5rem 0;
    }
    .gaming-info-box {
        background: linear-gradient(135deg, #28A74515, #0099FF10);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #28A74530;
    }
    </style>
    """, unsafe_allow_html=True)

def get_gaming_chart_config():
    """Configuration charts gaming"""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': '#FFFFFF',
        'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': '#2C3E50'},
        'colorway': ['#0099FF', '#E60012', '#28A745', '#FFB020'],
        'margin': {'t': 60, 'b': 40, 'l': 60, 'r': 40},
        'xaxis': {'gridcolor': '#E9ECEF', 'showgrid': True},
        'yaxis': {'gridcolor': '#E9ECEF', 'showgrid': True}
    }

# Application du thème
apply_gaming_theme()

# Header principal
st.markdown("""
<div class="main-header">
    <h1 style="color: #0099FF; margin: 0;">🎯 Gaming Workforce Predictive Analytics</h1>
    <p style="color: #6C757D; margin-top: 0.5rem;">AI-Powered Workforce Intelligence & Future Insights</p>
</div>
""", unsafe_allow_html=True)

# Breadcrumb
st.markdown("""
<div style="background: #F8F9FA; padding: 0.75rem 1rem; border-radius: 6px; margin: 1rem 0; color: #6C757D;">
    🎮 <strong>Gaming Workforce Observatory</strong> → Predictive Analytics
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="gaming-info-box">
    <h4 style="color: #0099FF;">🤖 Gaming AI-Powered Workforce Intelligence</h4>
    <p style="color: #2C3E50;">Machine learning models analysent en temps réel les données gaming workforce pour prédire les risques, optimiser les équipes et identifier les opportunités de croissance.</p>
</div>
""", unsafe_allow_html=True)

# Génération données de démonstration
@st.cache_data(ttl=300)
def generate_ml_model_data():
    """Génère des données ML pour démonstration"""
    np.random.seed(42)
    
    # Données modèles ML
    models = ['Turnover Predictor', 'Burnout Detection', 'Performance Forecaster', 
              'Team Optimizer', 'Salary Benchmarker', 'Skill Gap Analyzer']
    
    return pd.DataFrame({
        'Model': models,
        'Accuracy': [89.3, 87.8, 84.2, 91.5, 86.7, 88.1],
        'Precision': [85.2, 92.1, 81.3, 89.7, 79.4, 86.8],
        'Recall': [89.1, 87.3, 87.2, 93.2, 85.1, 90.3],
        'Business_Impact': [520000, 340000, 280000, 410000, 190000, 310000]
    })

@st.cache_data(ttl=300)
def generate_prediction_data():
    """Génère des données de prédiction gaming"""
    np.random.seed(42)
    
    # Données employés avec risques
    employees = np.arange(1, 101)
    turnover_risk = np.random.beta(2, 5, 100) * 100
    burnout_risk = np.random.beta(1.5, 4, 100) * 100
    performance_score = 60 + np.random.normal(0, 15, 100)
    performance_score = np.clip(performance_score, 0, 100)
    
    # Catégories de risque
    risk_categories = []
    for risk in turnover_risk:
        if risk > 70:
            risk_categories.append('High Risk')
        elif risk > 40:
            risk_categories.append('Medium Risk')
        else:
            risk_categories.append('Low Risk')
    
    return pd.DataFrame({
        'Employee_ID': employees,
        'Turnover_Risk': turnover_risk,
        'Burnout_Risk': burnout_risk,
        'Performance_Score': performance_score,
        'Risk_Category': risk_categories
    })

@st.cache_data(ttl=300)
def generate_projection_data():
    """Génère des projections gaming workforce"""
    future_months = pd.date_range('2025-01-01', periods=12, freq='M')
    
    return pd.DataFrame({
        'Month': future_months,
        'Headcount_Lower': [2800 + i*20 - 50 for i in range(12)],
        'Headcount_Predicted': [2800 + i*25 for i in range(12)],
        'Headcount_Upper': [2800 + i*30 + 50 for i in range(12)],
        'Turnover_Rate': [3.2 + np.random.normal(0, 0.5) for _ in range(12)],
        'Hiring_Need': [45, 52, 38, 67, 73, 89, 92, 78, 65, 71, 56, 48]
    })

# Chargement des données
models_df = generate_ml_model_data()
prediction_df = generate_prediction_data()
projection_df = generate_projection_data()

# Section Performance des Modèles ML
st.markdown("""
<div style="background: linear-gradient(135deg, #0099FF15, transparent); padding: 1rem; border-radius: 8px; margin: 2rem 0 1rem 0; border-left: 4px solid #0099FF;">
    <h3 style="margin: 0; color: #2C3E50;">🧠 Gaming AI Models Performance</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Chart accuracy modèles
    fig_accuracy = go.Figure()
    
    fig_accuracy.add_trace(go.Bar(
        name='Accuracy',
        x=models_df['Model'],
        y=models_df['Accuracy'],
        marker_color=GAMING_COLORS['primary']
    ))
    
    fig_accuracy.add_trace(go.Bar(
        name='Precision',
        x=models_df['Model'],
        y=models_df['Precision'],
        marker_color=GAMING_COLORS['accent']
    ))
    
    fig_accuracy.update_layout(
        title="🎯 Gaming AI Models: Accuracy & Precision",
        barmode='group',
        **get_gaming_chart_config()
    )
    
    st.plotly_chart(fig_accuracy, use_container_width=True)

with col2:
    # Impact business
    fig_impact = px.bar(
        models_df,
        x='Model',
        y='Business_Impact',
        color='Business_Impact',
        title='💰 Gaming AI Models: Business Impact ($)',
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_impact.update_layout(**get_gaming_chart_config())
    st.plotly_chart(fig_impact, use_container_width=True)

# Table performance modèles
st.markdown("### 📊 Gaming ML Models Performance Table")
st.dataframe(
    models_df.style.background_gradient(subset=['Accuracy', 'Precision', 'Recall'], cmap='RdYlGn').format({
        'Accuracy': '{:.1f}%',
        'Precision': '{:.1f}%', 
        'Recall': '{:.1f}%',
        'Business_Impact': '${:,.0f}'
    }),
    use_container_width=True
)

# Section Analyses Prédictives
st.markdown("""
<div style="background: linear-gradient(135deg, #0099FF15, transparent); padding: 1rem; border-radius: 8px; margin: 2rem 0 1rem 0; border-left: 4px solid #0099FF;">
    <h3 style="margin: 0; color: #2C3E50;">🔮 Gaming Workforce Risk Predictions</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Scatter plot risques
    fig_risk_scatter = px.scatter(
        prediction_df,
        x='Turnover_Risk',
        y='Burnout_Risk',
        color='Risk_Category',
        size='Performance_Score',
        title='🚨 Gaming Employee Risk Analysis',
        labels={
            'Turnover_Risk': 'Turnover Risk (%)',
            'Burnout_Risk': 'Burnout Risk (%)'
        },
        color_discrete_map={
            'High Risk': '#E60012',
            'Medium Risk': '#FFD700',
            'Low Risk': '#0099FF'
        }
    )
    
    fig_risk_scatter.update_layout(**get_gaming_chart_config())
    st.plotly_chart(fig_risk_scatter, use_container_width=True)

with col2:
    # Distribution des risques
    risk_counts = prediction_df['Risk_Category'].value_counts()
    
    fig_risk_pie = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        marker=dict(colors=[GAMING_COLORS['primary'], '#FFD700', GAMING_COLORS['accent']]),
        hole=0.4
    )])
    
    fig_risk_pie.update_layout(
        title="🎯 Gaming Risk Distribution",
        **get_gaming_chart_config()
    )
    
    st.plotly_chart(fig_risk_pie, use_container_width=True)

# Section Projections Futur
st.markdown("""
<div style="background: linear-gradient(135deg, #0099FF15, transparent); padding: 1rem; border-radius: 8px; margin: 2rem 0 1rem 0; border-left: 4px solid #0099FF;">
    <h3 style="margin: 0; color: #2C3E50;">📈 Gaming Workforce Projections 2025</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Prédictions headcount
    fig_headcount = go.Figure()
    
    # Intervalle de confiance
    fig_headcount.add_trace(go.Scatter(
        x=projection_df['Month'],
        y=projection_df['Headcount_Upper'],
        fill=None,
        mode='lines',
        line_color='rgba(0,0,0,0)',
        showlegend=False
    ))
    
    fig_headcount.add_trace(go.Scatter(
        x=projection_df['Month'],
        y=projection_df['Headcount_Lower'],
        fill='tonexty',
        mode='lines',
        line_color='rgba(0,0,0,0)',
        fillcolor='rgba(0, 153, 255, 0.2)',
        name='Confidence Interval'
    ))
    
    fig_headcount.add_trace(go.Scatter(
        x=projection_df['Month'],
        y=projection_df['Headcount_Predicted'],
        mode='lines+markers',
        name='Predicted Headcount',
        line=dict(color=GAMING_COLORS['primary'], width=3)
    ))
    
    fig_headcount.update_layout(
        title="📊 Gaming Headcount Projection 2025",
        **get_gaming_chart_config()
    )
    
    st.plotly_chart(fig_headcount, use_container_width=True)

with col2:
    # Besoins recrutement
    fig_hiring = px.bar(
        projection_df,
        x='Month',
        y='Hiring_Need',
        title='👥 Gaming Monthly Hiring Forecast 2025',
        color='Hiring_Need',
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_hiring.update_layout(**get_gaming_chart_config())
    st.plotly_chart(fig_hiring, use_container_width=True)

# Métriques clés prédictives
st.markdown("### 🎯 Gaming Predictive Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    high_risk_count = len(prediction_df[prediction_df['Risk_Category'] == 'High Risk'])
    st.metric("🚨 High Risk Employees", high_risk_count, "-3 vs last month")

with col2:
    avg_turnover_risk = prediction_df['Turnover_Risk'].mean()
    st.metric("📊 Avg Turnover Risk", f"{avg_turnover_risk:.1f}%", "-2.3%")

with col3:
    total_hiring_2025 = projection_df['Hiring_Need'].sum()
    st.metric("📈 Hiring Forecast 2025", total_hiring_2025, "+15% vs 2024")

with col4:
    model_accuracy = models_df['Accuracy'].mean()
    st.metric("🎯 Model Accuracy", f"{model_accuracy:.1f}%", "+1.2%")

# Recommandations IA
st.markdown("""
<div style="background: linear-gradient(135deg, #0099FF15, transparent); padding: 1rem; border-radius: 8px; margin: 2rem 0 1rem 0; border-left: 4px solid #0099FF;">
    <h3 style="margin: 0; color: #2C3E50;">💡 Gaming AI-Generated Recommendations</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="gaming-kpi-card">
        <h4 style="color: #E60012;">🚨 Immediate Actions</h4>
        <ul style="color: #2C3E50;">
            <li><strong>8 employees</strong> at high turnover risk</li>
            <li><strong>Schedule 1-on-1s</strong> with managers</li>
            <li><strong>Review workload</strong> for 12 at-risk</li>
            <li><strong>Offer flexibility</strong> options</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="gaming-kpi-card">
        <h4 style="color: #FFB020;">📅 30-Day Plan</h4>
        <ul style="color: #2C3E50;">
            <li><strong>Hire 67 people</strong> Q1 focus</li>
            <li><strong>Skills training</strong> for 23 employees</li>
            <li><strong>Team restructuring</strong> optimization</li>
            <li><strong>Salary adjustments</strong> for 15 people</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="gaming-kpi-card">
        <h4 style="color: #28A745;">🚀 Strategic Initiatives</h4>
        <ul style="color: #2C3E50;">
            <li><strong>AI mentorship</strong> program launch</li>
            <li><strong>Predictive recruiting</strong> platform</li>
            <li><strong>Wellbeing tracking</strong> app rollout</li>
            <li><strong>Skills matrix</strong> automation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Sidebar informative
with st.sidebar:
    st.markdown("""
    ## 🔮 Predictive Analytics
    
    **AI-Powered Intelligence**
    
    🧠 **Machine Learning** models temps réel
    
    📊 **Predictive Insights** workforce planning
    
    🚨 **Risk Detection** early warning system
    
    💡 **Automated Recommendations** actionables
    
    ---
    
    ### 🤖 Active Models
    - Turnover Risk Predictor
    - Burnout Detection System
    - Performance Forecasting 
    - Team Optimization Engine
    - Salary Benchmarking AI
    - Skill Gap Analyzer
    
    ---
    
    ### 📈 Model Performance
    - **87.8%** average accuracy
    - **$2.1M** annual value generated
    - **Real-time** processing
    - **40+ variables** analyzed
    
    ---
    
    **🔄 Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """.format(datetime=datetime))

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #6C757D;">
    🎮 <strong>Gaming Workforce Observatory</strong> - Predictive Analytics • 
    Powered by Advanced AI • © 2024 Gaming Industry Excellence
</div>
""", unsafe_allow_html=True)
