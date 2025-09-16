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
    <div style='background: linear-gradient(90deg, #0099FF, #00CCFF); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='font-family: Arial, sans-serif; font-weight: bold; font-size: 3.5rem; color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{title}</h1>
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title):
    return f"<h2 style='color: #2C3E50; font-family: Arial, sans-serif; font-weight: bold; border-left: 4px solid #0099FF; padding-left: 1rem; margin: 2rem 0 1rem 0;'>{title}</h2>"

def create_ubisoft_info_box(title, content):
    return f"""
    <div style='background: #f8f9fa; border-left: 4px solid #0099FF; padding: 1.5rem; margin: 1rem 0; border-radius: 5px;'>
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

# Configuration de la page
st.set_page_config(
    page_title="Ubisoft Gaming Workforce Observatory - Executive Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SIDEBAR ÉPURÉE - MENU SEULEMENT
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #0099FF; font-family: Arial, sans-serif; margin: 0;'>🎮 Ubisoft</h2>
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
        if name == "Executive Dashboard":
            st.markdown(f"""
            <div style='background: #0099FF; color: white; padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0;'>
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
<div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; border-left: 4px solid #28A745;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: #2C3E50;'>🎮 Ubisoft Gaming Workforce Observatory</strong>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Global Studios • 25 Locations • 15,847 Employees</p>
        </div>
        <div style='text-align: right;'>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Last Updated</p>
            <strong style='color: #0099FF;'>{last_updated}</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL AVEC MISE EN VALEUR
st.markdown(create_ubisoft_header("Executive Dashboard", "C-Suite Strategic Workforce Intelligence"), unsafe_allow_html=True)

# MÉTRIQUES CLÉS AVEC STYLE PROFESSIONNEL
st.markdown(create_ubisoft_section_header("🎯 Key Performance Indicators"), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>👥</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>2,847</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Talent Pool</p>
        <small style='color: #28A745;'>+12% vs Q3</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>🌍</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>25</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Studios Worldwide</p>
        <small style='color: #666;'>Global Presence</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>🎯</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>87.3%</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Retention Rate</p>
        <small style='color: #28A745;'>+5.2% YoY</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>🚀</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>94/100</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Innovation Index</p>
        <small style='color: #28A745;'>Industry Leading</small>
    </div>
    """, unsafe_allow_html=True)

# SECTION STUDIOS AVEC INFO BOX INTÉGRÉE
st.markdown(create_ubisoft_section_header("🌍 Global Studios Performance"), unsafe_allow_html=True)

st.markdown(create_ubisoft_info_box(
    "Ubisoft's Global Excellence",
    "Les studios Ubisoft maintiennent des standards d'excellence mondiaux avec une performance moyenne de 87.3% across all locations. Our global footprint spans 6 continents with major development centers in Montreal, Paris, Milan, Shanghai, Toronto, San Francisco, Barcelona, and Kiev."
), unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
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
    
    fig_studios.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_studios, width='stretch')

with col2:
    st.markdown("### 🏆 Top Performing Studios")
    for i, row in df_studios.nlargest(3, 'Performance').iterrows():
        st.markdown(f"""
        <div style='background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 5px; border-left: 4px solid #0099FF;'>
            <strong style='color: #2C3E50;'>{row['Studio']}</strong> - <span style='color: #0099FF;'>{row['Performance']}%</span><br>
            <span style='color: #666; font-size: 0.9rem;'>👥 {row['Employees']:,} talents • 🎮 {row['Projects']} projets</span>
        </div>
        """, unsafe_allow_html=True)

# SECTION TRENDS
st.markdown(create_ubisoft_section_header("📈 Workforce Trends & Predictions"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
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
    
    st.plotly_chart(fig_trends, width='stretch')

with col2:
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
        title="🎯 Employee Satisfaction & Productivity",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_satisfaction, width='stretch')

# BENCHMARKS
st.markdown(create_ubisoft_section_header("🎮 Industry Benchmarks"), unsafe_allow_html=True)

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

st.plotly_chart(fig_benchmark, width='stretch')

# AI PREDICTIONS AVEC STYLE AMÉLIORÉ
st.markdown(create_ubisoft_section_header("🤖 AI-Powered Workforce Predictions"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0099FF, #00CCFF); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🔮</div>
        <h3 style='color: white; margin: 0;'>Turnover Risk</h3>
        <div style='font-size: 3rem; font-weight: bold; margin: 1rem 0;'>3.2%</div>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;'>
            Low risk identified across Ubisoft studios. ML model accuracy: 89%
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #28A745, #34CE57); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>⚡</div>
        <h3 style='color: white; margin: 0;'>Burnout Prevention</h3>
        <div style='font-size: 3rem; font-weight: bold; margin: 1rem 0;'>92%</div>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;'>
            Proactive intervention success rate in Ubisoft development teams
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #E60012, #FF1744); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🎯</div>
        <h3 style='color: white; margin: 0;'>Hiring Forecast</h3>
        <div style='font-size: 3rem; font-weight: bold; margin: 1rem 0;'>+340</div>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;'>
            Projected new hires Q1 2025 across Ubisoft worldwide studios
        </p>
    </div>
    """, unsafe_allow_html=True)

# FOOTER PROFESSIONNEL
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 5px; margin-top: 2rem;'>
    <p style='color: #666; margin: 0; font-size: 0.9rem;'>
        © 2024 Ubisoft Entertainment - Gaming Workforce Observatory<br>
        Confidential and Proprietary Information
    </p>
</div>
""", unsafe_allow_html=True)
