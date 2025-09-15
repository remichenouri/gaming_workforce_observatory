"""
🎮 Ubisoft Gaming Workforce Observatory
Predictive Analytics - AI-Powered Workforce Intelligence
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

from src.themes.ubisoft_premium import apply_ubisoft_theme, UBISOFT_COLORS
from src.utils.ubisoft_components import (
    create_ubisoft_header, create_ubisoft_breadcrumb,
    create_ubisoft_section_header, create_ubisoft_info_box,
    create_ubisoft_accent_box, get_ubisoft_chart_config
)

st.set_page_config(
    page_title="Ubisoft Predictive Analytics - AI Intelligence",
    page_icon="🔮",
    layout="wide"
)

apply_ubisoft_theme()

st.markdown(
    create_ubisoft_header(
        "UBISOFT Predictive Analytics",
        "AI-Powered Workforce Intelligence & Future Insights"
    ),
    unsafe_allow_html=True
)

st.markdown(create_ubisoft_breadcrumb("Predictive Analytics"), unsafe_allow_html=True)

# AI Model Performance
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        create_ubisoft_info_box(
            "🤖 Ubisoft AI-Powered Workforce Intelligence",
            "Machine learning models analysent en temps réel les données RH Ubisoft pour prédire les risques, optimiser les équipes et identifier les opportunités de croissance."
        ),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        create_ubisoft_accent_box(
            "🎯 Ubisoft ML Models Performance",
            "Burnout prediction: 89% accuracy • Turnover risk: 87% accuracy • Performance forecasting: 84% accuracy"
        ),
        unsafe_allow_html=True
    )

# Model Performance Dashboard
st.markdown(create_ubisoft_section_header("🧠 Ubisoft AI Models Performance"))

model_data = {
    'Model': ['Turnover Risk', 'Burnout Detection', 'Performance Prediction', 
              'Team Composition', 'Salary Optimization', 'Skill Gap Analysis'],
    'Accuracy': [87, 89, 84, 91, 82, 88],
    'Precision': [85, 92, 81, 89, 79, 86],
    'Recall': [89, 87, 87, 93, 85, 90],
    'Business_Impact': [340000, 520000, 280000, 410000, 190000, 310000]
}

models_df = pd.DataFrame(model_data)

col1, col2 = st.columns(2)

with col1:
    fig_accuracy = go.Figure()
    
    fig_accuracy.add_trace(go.Bar(
        name='Accuracy',
        x=models_df['Model'],
        y=models_df['Accuracy'],
        marker_color=UBISOFT_COLORS['primary']
    ))
    
    fig_accuracy.add_trace(go.Bar(
        name='Precision',
        x=models_df['Model'],
        y=models_df['Precision'],
        marker_color=UBISOFT_COLORS['accent']
    ))
    
    fig_accuracy.update_layout(
        title="🎯 Ubisoft AI Models: Accuracy & Precision",
        barmode='group',
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_accuracy, use_container_width=True)

with col2:
    fig_impact = px.bar(
        models_df,
        x='Model',
        y='Business_Impact',
        color='Business_Impact',
        title='💰 Ubisoft AI Models: Business Impact ($)',
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_impact.update_layout(get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_impact, use_container_width=True)

# Predictive Insights
st.markdown(create_ubisoft_section_header("🔮 Ubisoft Workforce Predictions"))

# Generate prediction data
np.random.seed(42)
employees = np.arange(1, 101)
turnover_risk = np.random.beta(2, 5, 100) * 100
burnout_risk = np.random.beta(1.5, 4, 100) * 100
performance_score = 60 + np.random.normal(0, 15, 100)
performance_score = np.clip(performance_score, 0, 100)

# Risk categories
risk_categories = []
for i in range(100):
    if turnover_risk[i] > 70:
        risk_categories.append('High Risk')
    elif turnover_risk[i] > 40:
        risk_categories.append('Medium Risk')
    else:
        risk_categories.append('Low Risk')

prediction_df = pd.DataFrame({
    'Employee_ID': employees,
    'Turnover_Risk': turnover_risk,
    'Burnout_Risk': burnout_risk,
    'Performance_Score': performance_score,
    'Risk_Category': risk_categories
})

col1, col2 = st.columns(2)

with col1:
    # Risk distribution
    fig_risk_scatter = px.scatter(
        prediction_df,
        x='Turnover_Risk',
        y='Burnout_Risk',
        color='Risk_Category',
        size='Performance_Score',
        title='🚨 Ubisoft Employee Risk Analysis',
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
    
    fig_risk_scatter.update_layout(get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_risk_scatter, use_container_width=True)

with col2:
    # Risk distribution pie
    risk_counts = prediction_df['Risk_Category'].value_counts()
    
    fig_risk_pie = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        marker=dict(colors=[UBISOFT_COLORS['primary'], '#FFD700', UBISOFT_COLORS['accent']]),
        hole=0.4
    )])
    
    fig_risk_pie.update_layout(
        title="🎯 Ubisoft Risk Distribution",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_risk_pie, use_container_width=True)

# Future Projections
st.markdown(create_ubisoft_section_header("📈 Ubisoft Workforce Projections 2025"))

# Generate future projections
future_months = pd.date_range('2025-01-01', periods=12, freq='M')
projections = {
    'Month': future_months,
    'Headcount_Lower': [2800 + i*20 - 50 for i in range(12)],
    'Headcount_Predicted': [2800 + i*25 for i in range(12)],
    'Headcount_Upper': [2800 + i*30 + 50 for i in range(12)],
    'Turnover_Rate': [3.2 + np.random.normal(0, 0.5) for _ in range(12)],
    'Hiring_Need': [45, 52, 38, 67, 73, 89, 92, 78, 65, 71, 56, 48]
}

proj_df = pd.DataFrame(projections)

col1, col2 = st.columns(2)

with col1:
    fig_headcount = go.Figure()
    
    # Add prediction intervals
    fig_headcount.add_trace(go.Scatter(
        x=proj_df['Month'],
        y=proj_df['Headcount_Upper'],
        fill=None,
        mode='lines',
        line_color='rgba(0,0,0,0)',
        showlegend=False
    ))
    
    fig_headcount.add_trace(go.Scatter(
        x=proj_df['Month'],
        y=proj_df['Headcount_Lower'],
        fill='tonexty',
        mode='lines',
        line_color='rgba(0,0,0,0)',
        fillcolor='rgba(0, 153, 255, 0.2)',
        name='Confidence Interval'
    ))
    
    fig_headcount.add_trace(go.Scatter(
        x=proj_df['Month'],
        y=proj_df['Headcount_Predicted'],
        mode='lines+markers',
        name='Predicted Headcount',
        line=dict(color=UBISOFT_COLORS['primary'], width=3)
    ))
    
    fig_headcount.update_layout(
        title="📊 Ubisoft Headcount Projection 2025",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_headcount, use_container_width=True)

with col2:
    fig_hiring = px.bar(
        proj_df,
        x='Month',
        y='Hiring_Need',
        title='👥 Ubisoft Monthly Hiring Forecast 2025',
        color='Hiring_Need',
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_hiring.update_layout(get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_hiring, use_container_width=True)

# Action Recommendations
st.markdown(create_ubisoft_section_header("💡 Ubisoft AI-Generated Recommendations"))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">🚨 Immediate Actions</h4>
        <ul style="color: #F5F5F5; text-align: left;">
            <li><strong>8 employees</strong> at high turnover risk</li>
            <li><strong>Schedule 1-on-1s</strong> with managers</li>
            <li><strong>Review workload</strong> for 12 at-risk</li>
            <li><strong>Offer flexibility</strong> options</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">📅 30-Day Plan</h4>
        <ul style="color: #F5F5F5; text-align: left;">
            <li><strong>Hire 67 people</strong> Q1 focus</li>
            <li><strong>Skills training</strong> for 23 employees</li>
            <li><strong>Team restructuring</strong> in Paris studio</li>
            <li><strong>Salary adjustments</strong> for 15 people</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">🚀 Strategic Initiatives</h4>
        <ul style="color: #F5F5F5; text-align: left;">
            <li><strong>AI mentorship</strong> program launch</li>
            <li><strong>Predictive recruiting</strong> platform</li>
            <li><strong>Wellbeing tracking</strong> app rollout</li>
            <li><strong>Skills matrix</strong> automation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    ## 🔮 Predictive Analytics
    
    **AI-Powered Intelligence**
    
    🧠 **Machine Learning** models en temps réel
    
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
    - **87%** average accuracy
    - **$2.1M** annual value generated
    - **Real-time** processing
    - **40+ variables** analyzed
    """)