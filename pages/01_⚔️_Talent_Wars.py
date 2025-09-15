"""
🎮 Ubisoft Gaming Workforce Observatory
Talent Wars - Competitive Intelligence & Strategic Talent Acquisition
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ─────────────────────────────────────────────
# STUBS POUR ÉVITER IMPORT ERRORS
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
    <div style='background: linear-gradient(90deg, #E60012, #FF4444); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='font-family: Arial, sans-serif; font-weight: bold; font-size: 3.5rem; color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{title}</h1>
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title):
    return f"<h2 style='color: #2C3E50; font-family: Arial, sans-serif; font-weight: bold; border-left: 4px solid #E60012; padding-left: 1rem; margin: 2rem 0 1rem 0;'>{title}</h2>"

def create_ubisoft_info_box(title, content):
    return f"""
    <div style='background: #f8f9fa; border-left: 4px solid #E60012; padding: 1.5rem; margin: 1rem 0; border-radius: 5px;'>
        <h4 style='color: #2C3E50; margin: 0 0 0.5rem 0;'>{title}</h4>
        <p style='color: #555; margin: 0; font-size: 1rem; line-height: 1.5;'>{content}</p>
    </div>
    """

def create_ubisoft_accent_box(title, content):
    return f"""
    <div style='background: linear-gradient(135deg, #E6001215, #fff); border-left: 4px solid #E60012; padding: 1.5rem; margin: 1rem 0; border-radius: 5px;'>
        <h4 style='color: #E60012; margin: 0 0 0.5rem 0;'>{title}</h4>
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

st.set_page_config(
    page_title="Gaming Workforce Observatory - Talent Wars",
    page_icon="⚔️",
    layout="wide"
)

# SIDEBAR ÉPURÉE - MENU SEULEMENT
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #E60012; font-family: Arial, sans-serif; margin: 0;'>⚔️ Ubisoft</h2>
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
        if name == "Talent Wars":
            st.markdown(f"""
            <div style='background: #E60012; color: white; padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0;'>
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
<div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; border-left: 4px solid #E60012;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: #2C3E50;'>⚔️ Talent Wars - Competitive Intelligence</strong>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Strategic Talent Acquisition • Gaming Industry Benchmarks • Market Analysis</p>
        </div>
        <div style='text-align: right;'>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Last Updated</p>
            <strong style='color: #E60012;'>{last_updated}</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL AVEC MISE EN VALEUR
st.markdown(create_ubisoft_header("Talent Wars", "Competitive Intelligence & Strategic Talent Acquisition"), unsafe_allow_html=True)

# INTRODUCTION AVEC STYLE PROFESSIONNEL
st.markdown(create_ubisoft_info_box(
    "⚔️ Battle for Gaming Talent",
    "Analyse stratégique de la compétition pour les meilleurs talents gaming. Comparaison des performances Ubisoft versus les principales companies du secteur technologique et gaming. Identification des opportunités d'amélioration et des avantages concurrentiels dans l'acquisition de talents de haut niveau."
), unsafe_allow_html=True)

# DONNÉES COMPARATIVES
companies = ['Ubisoft', 'EA', 'Activision', 'Epic Games', 'Riot Games', 'Valve', 'Blizzard', 'Take-Two']
avg_salaries = [95000, 98000, 102000, 115000, 108000, 125000, 99000, 94000]
retention_rates = [87.3, 82.1, 79.5, 91.2, 88.7, 93.1, 81.3, 83.9]
employee_satisfaction = [7.8, 7.2, 6.9, 8.4, 8.1, 8.7, 7.0, 7.4]

competitive_df = pd.DataFrame({
    'Company': companies,
    'Avg_Salary': avg_salaries,
    'Retention_Rate': retention_rates,
    'Satisfaction': employee_satisfaction
})

# SECTION COMPARATIVE AVEC INFO INTÉGRÉE
st.markdown(create_ubisoft_section_header("🏆 Competitive Market Analysis"), unsafe_allow_html=True)

st.markdown(create_ubisoft_accent_box(
    "🎯 Ubisoft Strategic Positioning",
    "Positioning stratégique: Excellent retention avec salaire compétitif. Focus sur culture créative, projets innovants et développement de carrière. Ubisoft se distingue par son portefeuille AAA mondial et sa présence dans 25 studios internationaux."
), unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

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
    
    fig_competitive.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_competitive, width='stretch')

with col2:
    st.markdown("### 🏅 Ubisoft Competitive Advantages")
    
    advantages = [
        ("🌍", "Global Presence", "25+ studios worldwide"),
        ("🎮", "AAA Portfolio", "Iconic franchises"),
        ("🏢", "Work Culture", "Creative freedom"),
        ("📈", "Career Growth", "Clear progression paths"),
        ("🎯", "Innovation", "Cutting-edge technology")
    ]
    
    for icon, title, desc in advantages:
        st.markdown(f"""
        <div style='background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 5px; border-left: 4px solid #0099FF;'>
            <strong style='color: #2C3E50;'>{icon} {title}</strong><br>
            <span style='color: #666; font-size: 0.9rem;'>{desc}</span>
        </div>
        """, unsafe_allow_html=True)

# TALENT ACQUISITION FUNNEL
st.markdown(create_ubisoft_section_header("🎯 Gaming Talent Acquisition Performance"), unsafe_allow_html=True)

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
    
    fig_funnel.update_layout(
        title="🎮 Gaming Talent Acquisition Funnel",
        **get_ubisoft_chart_config()['layout']
    )
    st.plotly_chart(fig_funnel, width='stretch')

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
        barmode='group',
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_conversion, width='stretch')

# RECOMMANDATIONS STRATÉGIQUES AVEC STYLE AMÉLIORÉ
st.markdown(create_ubisoft_section_header("💡 Strategic Gaming Recommendations"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #0099FF;'>
        <h4 style='color: #0099FF; margin: 0 0 1rem 0;'>🎯 Focus Areas</h4>
        <ul style='color: #2C3E50; margin: 0; padding-left: 1.2rem; line-height: 1.6;'>
            <li><strong>Employee Referral:</strong> Renforcer le programme interne</li>
            <li><strong>Game Jams:</strong> Investir dans les événements créatifs</li>
            <li><strong>Partenariats:</strong> Développer liens universités</li>
            <li><strong>Sourcing:</strong> Améliorer GitHub/portfolio sourcing</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #FFB020;'>
        <h4 style='color: #FFB020; margin: 0 0 1rem 0;'>⚡ Quick Wins</h4>
        <ul style='color: #2C3E50; margin: 0; padding-left: 1.2rem; line-height: 1.6;'>
            <li><strong>Bonus VR/AR:</strong> +15% referral bonus</li>
            <li><strong>Fast-track:</strong> Unity/Unreal experts</li>
            <li><strong>Hackathons:</strong> Gaming events mensuels</li>
            <li><strong>LinkedIn:</strong> Premium sourcing tools</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #28A745;'>
        <h4 style='color: #28A745; margin: 0 0 1rem 0;'>📈 Long-term Strategy</h4>
        <ul style='color: #2C3E50; margin: 0; padding-left: 1.2rem; line-height: 1.6;'>
            <li><strong>Gaming Academy:</strong> Programme formation</li>
            <li><strong>Global Pipeline:</strong> Talent pipeline</li>
            <li><strong>IA Matching:</strong> Candidat matching</li>
            <li><strong>Employer Brand:</strong> Campagnes de marque</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# FOOTER PROFESSIONNEL
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 5px; margin-top: 2rem;'>
    <p style='color: #666; margin: 0; font-size: 0.9rem;'>
        © 2024 Ubisoft Entertainment - Gaming Workforce Observatory<br>
        Talent Wars Dashboard • Strategic Talent Intelligence • Confidential and Proprietary
    </p>
</div>
""", unsafe_allow_html=True)
