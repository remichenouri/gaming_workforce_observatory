"""
🎮 CORRECTIONS PAGES STREAMLIT - SANS ERREURS

Corrections pour pages/01_⚔️_Talent_Wars.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ─────────────────────────────────────────────
# STUBS POUR ÉVITER IMPORT ERRORS
def apply_ubisoft_theme(): pass
UBISOFT_COLORS = {'primary': '#0099FF', 'accent': '#E60012', 'success': '#28A745', 'warning': '#FFB020', 'text': '#2C3E50'}
def create_ubisoft_header(title, subtitle=None): 
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    return f"<h1>{title}</h1>{subtitle_html}"
def create_ubisoft_breadcrumb(page): return f"<p>🎮 Ubisoft Observatory → {page}</p>"
def create_ubisoft_section_header(title): return f"<h3>{title}</h3>"
def create_ubisoft_info_box(title, content): return f"<div><strong>{title}</strong><p>{content}</p></div>"
def create_ubisoft_accent_box(title, content): return f"<div style='border-left:4px solid #E60012'><strong>{title}</strong><p>{content}</p></div>"
def get_ubisoft_chart_config(): return {'layout': {}}
def create_ubisoft_metric_cols(metrics, cols=4):
    for metric in metrics:
        st.markdown(f"**{metric['title']}**: {metric['value']}")
def display_ubisoft_logo_section(): return "<p>© 2024 Ubisoft</p>"
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Gaming Workforce Observatory - Talent Wars",
    page_icon="⚔️",
    layout="wide"
)

apply_ubisoft_theme()

st.markdown(create_ubisoft_header("Gaming Talent Wars", "Competitive Intelligence & Strategic Talent Acquisition"), unsafe_allow_html=True)
st.markdown(create_ubisoft_breadcrumb("Talent Wars"), unsafe_allow_html=True)

# Introduction CORRIGÉE
st.markdown(create_ubisoft_info_box(
    "⚔️ Battle for Gaming Talent",
    "Analyse stratégique de la compétition pour les meilleurs talents gaming. Gaming vs principales companies du secteur."
), unsafe_allow_html=True)

# Données comparative CORRIGÉES
companies = ['Gaming Studio A', 'EA', 'Activision', 'Epic Games', 'Riot Games', 'Valve', 'Blizzard', 'Take-Two']
avg_salaries = [95000, 98000, 102000, 115000, 108000, 125000, 99000, 94000]
retention_rates = [87.3, 82.1, 79.5, 91.2, 88.7, 93.1, 81.3, 83.9]
employee_satisfaction = [7.8, 7.2, 6.9, 8.4, 8.1, 8.7, 7.0, 7.4]

competitive_df = pd.DataFrame({
    'Company': companies,
    'Avg_Salary': avg_salaries,
    'Retention_Rate': retention_rates,
    'Satisfaction': employee_satisfaction
})

col1, col2 = st.columns([3, 1])

with col1:
    fig_competitive = px.scatter(
        competitive_df,
        x='Avg_Salary',
        y='Retention_Rate',
        size='Satisfaction',
        color='Satisfaction',
        hover_name='Company',
        title='🎮 Gaming Industry: Salary vs Retention Battle',
        labels={
            'Avg_Salary': 'Average Salary (USD)',
            'Retention_Rate': 'Retention Rate (%)',
            'Satisfaction': 'Employee Satisfaction'
        },
        color_continuous_scale=['#FF6B6B', '#FFD700', '#0099FF']
    )
    
    st.plotly_chart(fig_competitive, use_container_width=True)

with col2:
    st.markdown(create_ubisoft_accent_box(
        "🎯 Gaming Strategy",
        "Positioning stratégique: Excellent retention avec salaire compétitif. Focus sur culture et projets innovants."
    ), unsafe_allow_html=True)
    
    st.markdown("### 🏅 Gaming Advantages")
    st.markdown("""
    - **🌍 Global Presence:** 25+ studios worldwide
    - **🎮 AAA Portfolio:** Iconic franchises  
    - **🏢 Work Culture:** Creative freedom
    - **📈 Career Growth:** Clear progression paths
    - **🎯 Innovation:** Cutting-edge technology
    """)

# Talent Acquisition Funnel CORRIGÉ
st.markdown(create_ubisoft_section_header("🎯 Gaming Talent Acquisition Performance"))

col1, col2 = st.columns(2)

with col1:
    funnel_stages = ['Applications', 'Phone Screen', 'Technical Test', 'On-site', 'Offers', 'Accepted']
    gaming_funnel = [10000, 3200, 1800, 650, 420, 340]
    
    fig_funnel = go.Figure()
    
    fig_funnel.add_trace(go.Funnel(
        y=funnel_stages,
        x=gaming_funnel,
        name='Gaming Performance',
        marker=dict(color=UBISOFT_COLORS['primary']),
        connector=dict(line=dict(color=UBISOFT_COLORS['primary'], dash='solid', width=2))
    ))
    
    fig_funnel.update_layout(title="🎮 Gaming Talent Acquisition Funnel")
    st.plotly_chart(fig_funnel, use_container_width=True)

with col2:
    conversion_data = {
        'Stage': ['Application → Phone', 'Phone → Technical', 'Technical → On-site', 'On-site → Offer', 'Offer → Accept'],
        'Gaming': [32, 56, 36, 65, 81],
        'Industry Avg': [28, 50, 36, 60, 70]
    }
    
    conv_df = pd.DataFrame(conversion_data)
    
    fig_conversion = go.Figure()
    
    fig_conversion.add_trace(go.Bar(
        name='Gaming',
        x=conv_df['Stage'],
        y=conv_df['Gaming'],
        marker_color=UBISOFT_COLORS['primary']
    ))
    
    fig_conversion.add_trace(go.Bar(
        name='Industry Average',
        x=conv_df['Stage'],
        y=conv_df['Industry Avg'],
        marker_color='rgba(100, 100, 100, 0.6)'
    ))
    
    fig_conversion.update_layout(
        title="📊 Gaming Conversion Rates vs Industry",
        barmode='group'
    )
    
    st.plotly_chart(fig_conversion, use_container_width=True)

# Actionable Insights CORRIGÉES
st.markdown(create_ubisoft_section_header("💡 Strategic Gaming Recommendations"))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0099FF15, #fff); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #0099FF;">
        <h4 style="color: #0099FF;">🎯 Focus Areas</h4>
        <ul style="color: #2C3E50; text-align: left;">
            <li>Renforcer employee referral program</li>
            <li>Investir dans Game Jams & events</li>
            <li>Développer partnerships universités</li>
            <li>Améliorer GitHub/portfolio sourcing</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFB02015, #fff); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #FFB020;">
        <h4 style="color: #FFB020;">⚡ Quick Wins</h4>
        <ul style="color: #2C3E50; text-align: left;">
            <li>+15% referral bonus pour VR/AR skills</li>
            <li>Fast-track pour Unity/Unreal experts</li>
            <li>Gaming hackathons mensuels</li>
            <li>LinkedIn premium sourcing tools</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #28A74515, #fff); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #28A745;">
        <h4 style="color: #28A745;">📈 Long-term Strategy</h4>
        <ul style="color: #2C3E50; text-align: left;">
            <li>Gaming Academy program</li>
            <li>Global talent pipeline</li>
            <li>AI-powered candidate matching</li>
            <li>Employer branding campaigns</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Sidebar CORRIGÉ
with st.sidebar:
    st.markdown("""
    ## ⚔️ Talent Wars Dashboard
    
    **Competitive Intelligence**
    
    🏆 **Benchmarking** vs industry leaders
    
    🎯 **Acquisition** funnel analysis  
    
    🌟 **Source** optimization
    
    💡 **Strategic** recommendations
    
    ---
    
    ### 🎮 Key Gaming Competitors
    - EA Sports & Games
    - Activision Blizzard  
    - Epic Games
    - Riot Games
    - Valve Corporation
    - Take-Two Interactive
    
    ---
    
    **📊 Data Sources:**
    - Glassdoor salary data
    - LinkedIn talent insights  
    - Gaming industry reports
    - Internal gaming metrics
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #6C757D;">
    🎮 <strong>Gaming Workforce Observatory</strong> - Talent Wars • 
    Strategic Talent Intelligence • © 2024 Gaming Excellence
</div>
""", unsafe_allow_html=True)
