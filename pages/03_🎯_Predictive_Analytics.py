"""
🎮 Gaming Workforce Observatory - Predictive Analytics
Page Predictive Analytics sans erreurs d'import
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# STUBS POUR THEME & COMPOSANTS UBISOFT
def apply_ubisoft_theme():
    pass

UBISOFT_COLORS = {
    'primary': '#0099FF',
    'accent': '#E60012',
    'success': '#28A745',
    'warning': '#FFB020',
    'text': '#2C3E50'
}

def create_ubisoft_header(title, subtitle=None):
    subtitle_html = f"<p style='font-size:1.2rem; color:#555; margin-top:0.5rem;'>{subtitle}</p>" if subtitle else ""
    return f"""
    <div style='background: linear-gradient(90deg, #FFB020, #FFC533); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='font-family: Arial, sans-serif; font-weight: bold; font-size: 3.5rem; color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{title}</h1>
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title):
    return f"<h2 style='color: #2C3E50; font-family: Arial, sans-serif; font-weight: bold; border-left: 4px solid #FFB020; padding-left: 1rem; margin: 2rem 0 1rem 0;'>{title}</h2>"

def create_ubisoft_info_box(title, content):
    return f"""
    <div style='background: #f8f9fa; border-left: 4px solid #FFB020; padding: 1.5rem; margin: 1rem 0; border-radius: 5px;'>
        <h4 style='color: #2C3E50; margin: 0 0 0.5rem 0;'>{title}</h4>
        <p style='color: #555; margin: 0; font-size: 1rem; line-height: 1.5;'>{content}</p>
    </div>
    """

def get_ubisoft_chart_config():
    return {
        'layout': {
            'font': {'family': 'Arial, sans-serif', 'size': 12, 'color': '#2C3E50'},
            'paper_bgcolor': 'white',
            'plot_bgcolor': '#fafafa'
        }
    }

# ─────────────────────────────────────────────

# Configuration page
st.set_page_config(
    page_title="Gaming Workforce Observatory - Predictive Analytics",
    page_icon="🎯",
    layout="wide"
)

# SIDEBAR ÉPURÉE - MENU SEULEMENT
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #FFB020; font-family: Arial, sans-serif; margin: 0;'>🎯 Ubisoft</h2>
        <p style='color: #666; font-size: 0.9rem; margin: 0.5rem 0;'>Workforce Observatory</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu de navigation épuré
    menu_items = [
        ("🏠", "Executive Dashboard"),
        ("⚔️", "Talent Wars"), 
        ("🧠", "Neurodiversity ROI"),
        ("🎯", "Predictive Analytics"),
        ("🌍", "Global Studios"),
        ("💰", "Compensation Intel"),
        ("🚀", "Future Insights"),
        ("⚙️", "Admin Panel")
    ]
    
    st.markdown("<h4 style='color: #2C3E50; margin-bottom: 1rem;'>Navigation</h4>", unsafe_allow_html=True)
    
    for icon, name in menu_items:
        if name == "Predictive Analytics":
            st.markdown(f"""
            <div style='background: #FFB020; color: white; padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0;'>
                <strong>{icon} {name}</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0; color: #555;'>
                {icon} {name}
            </div>
            """, unsafe_allow_html=True)

# HEADER PRINCIPAL PROFESSIONNEL
last_updated = datetime.now().strftime('%Y-%m-%d %H:%M')
st.markdown(f"""
<div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; border-left: 4px solid #FFB020;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: #2C3E50;'>🎯 Predictive Analytics - AI-Powered Intelligence</strong>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Machine Learning Models • Risk Detection • Future Workforce Planning</p>
        </div>
        <div style='text-align: right;'>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Last Updated</p>
            <strong style='color: #FFB020;'>{last_updated}</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL AVEC MISE EN VALEUR
st.markdown(create_ubisoft_header("Predictive Analytics", "AI-Powered Workforce Intelligence & Future Insights"), unsafe_allow_html=True)

# INTRODUCTION AVEC CONTEXTE
st.markdown(create_ubisoft_info_box(
    "🤖 Gaming AI-Powered Workforce Intelligence",
    "Nos modèles de machine learning analysent en temps réel les données workforce gaming pour prédire les risques de turnover, optimiser les équipes et identifier les opportunités de croissance. Avec une précision moyenne de 87.8%, notre système génère $2.1M de valeur annuelle."
), unsafe_allow_html=True)

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

# SECTION PERFORMANCE ML
st.markdown(create_ubisoft_section_header("🧠 AI Models Performance"), unsafe_allow_html=True)

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
        title="🎯 AI Models: Accuracy & Precision",
        barmode='group',
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_accuracy, width='stretch')

with col2:
    fig_impact = px.bar(
        models_df,
        x='Model',
        y='Business_Impact',
        color='Business_Impact',
        title='💰 AI Models: Business Impact ($)',
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_impact.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_impact, width='stretch')

# TABLE PERFORMANCE
st.markdown("### 📊 ML Models Performance Summary")
st.dataframe(
    models_df.style.background_gradient(subset=['Accuracy', 'Precision', 'Recall'], cmap='RdYlGn').format({
        'Accuracy': '{:.1f}%',
        'Precision': '{:.1f}%', 
        'Recall': '{:.1f}%',
        'Business_Impact': '${:,.0f}'
    }),
    width='stretch'
)

# SECTION RISK PREDICTIONS
st.markdown(create_ubisoft_section_header("🔮 Workforce Risk Predictions"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig_risk_scatter = px.scatter(
        prediction_df,
        x='Turnover_Risk',
        y='Burnout_Risk',
        color='Risk_Category',
        size='Performance_Score',
        title='🚨 Employee Risk Analysis',
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
    
    fig_risk_scatter.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_risk_scatter, width='stretch')

with col2:
    risk_counts = prediction_df['Risk_Category'].value_counts()
    
    fig_risk_pie = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        marker=dict(colors=[UBISOFT_COLORS['primary'], '#FFD700', UBISOFT_COLORS['accent']]),
        hole=0.4
    )])
    
    fig_risk_pie.update_layout(
        title="🎯 Risk Distribution",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_risk_pie, width='stretch')

# SECTION PROJECTIONS
st.markdown(create_ubisoft_section_header("📈 Workforce Projections 2025"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
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
        line=dict(color=UBISOFT_COLORS['primary'], width=3)
    ))
    
    fig_headcount.update_layout(
        title="📊 Headcount Projection 2025",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_headcount, width='stretch')

with col2:
    fig_hiring = px.bar(
        projection_df,
        x='Month',
        y='Hiring_Need',
        title='👥 Monthly Hiring Forecast 2025',
        color='Hiring_Need',
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_hiring.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_hiring, width='stretch')

# MÉTRIQUES PRÉDICTIVES
st.markdown("### 🎯 Key Predictive Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    high_risk_count = len(prediction_df[prediction_df['Risk_Category'] == 'High Risk'])
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #E60012; margin-bottom: 0.5rem;'>🚨</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>{high_risk_count}</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>High Risk Employees</p>
        <small style='color: #28A745;'>-3 vs last month</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_turnover_risk = prediction_df['Turnover_Risk'].mean()
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #FFB020; margin-bottom: 0.5rem;'>📊</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>{avg_turnover_risk:.1f}%</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Avg Turnover Risk</p>
        <small style='color: #28A745;'>-2.3%</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_hiring_2025 = projection_df['Hiring_Need'].sum()
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>📈</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>{total_hiring_2025}</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Hiring Forecast 2025</p>
        <small style='color: #28A745;'>+15% vs 2024</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    model_accuracy = models_df['Accuracy'].mean()
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #28A745; margin-bottom: 0.5rem;'>🎯</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>{model_accuracy:.1f}%</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Model Accuracy</p>
        <small style='color: #28A745;'>+1.2%</small>
    </div>
    """, unsafe_allow_html=True)

# AI RECOMMENDATIONS AVEC STYLE AMÉLIORÉ
st.markdown(create_ubisoft_section_header("💡 AI-Generated Recommendations"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #E60012, #FF1744); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🚨</div>
        <h4 style='color: white; margin: 0;'>Immediate Actions</h4>
        <div style='margin: 1rem 0; text-align: left;'>
            <strong>• 8 employees</strong> at high turnover risk<br>
            <strong>• Schedule 1-on-1s</strong> with managers<br>
            <strong>• Review workload</strong> for 12 at-risk<br>
            <strong>• Offer flexibility</strong> options
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFB020, #FFC533); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>📅</div>
        <h4 style='color: white; margin: 0;'>30-Day Plan</h4>
        <div style='margin: 1rem 0; text-align: left;'>
            <strong>• Hire 67 people</strong> Q1 focus<br>
            <strong>• Skills training</strong> for 23 employees<br>
            <strong>• Team restructuring</strong> optimization<br>
            <strong>• Salary adjustments</strong> for 15 people
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #28A745, #34CE57); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🚀</div>
        <h4 style='color: white; margin: 0;'>Strategic Initiatives</h4>
        <div style='margin: 1rem 0; text-align: left;'>
            <strong>• AI mentorship</strong> program launch<br>
            <strong>• Predictive recruiting</strong> platform<br>
            <strong>• Wellbeing tracking</strong> app rollout<br>
            <strong>• Skills matrix</strong> automation
        </div>
    </div>
    """, unsafe_allow_html=True)

# FOOTER PROFESSIONNEL
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 5px; margin-top: 2rem;'>
    <p style='color: #666; margin: 0; font-size: 0.9rem;'>
        © Gaming Workforce Observatory<br>
        Predictive Analytics Dashboard • Powered by Advanced AI • Confidential and Proprietary Information
    </p>
</div>
""", unsafe_allow_html=True)
