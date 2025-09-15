"""
🎮 Ubisoft Gaming Workforce Observatory
Future Insights - Innovation Lab Analytics & Emerging Trends
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
    <div style='background: linear-gradient(90deg, #667eea, #764ba2); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='font-family: Arial, sans-serif; font-weight: bold; font-size: 3.5rem; color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{title}</h1>
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title):
    return f"<h2 style='color: #2C3E50; font-family: Arial, sans-serif; font-weight: bold; border-left: 4px solid #667eea; padding-left: 1rem; margin: 2rem 0 1rem 0;'>{title}</h2>"

def create_ubisoft_info_box(title, content):
    return f"""
    <div style='background: #f8f9fa; border-left: 4px solid #667eea; padding: 1.5rem; margin: 1rem 0; border-radius: 5px;'>
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

st.set_page_config(
    page_title="Ubisoft Future Insights - Innovation Lab",
    page_icon="🚀",
    layout="wide"
)

# SIDEBAR ÉPURÉE - MENU SEULEMENT
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #667eea; font-family: Arial, sans-serif; margin: 0;'>🚀 Ubisoft</h2>
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
        if name == "Future Insights":
            st.markdown(f"""
            <div style='background: #667eea; color: white; padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0;'>
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
<div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; border-left: 4px solid #667eea;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: #2C3E50;'>🚀 Future Insights - Innovation Lab Analytics</strong>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Emerging Technologies • Skills Evolution • Innovation Pipeline • 12 Labs Globally</p>
        </div>
        <div style='text-align: right;'>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Last Updated</p>
            <strong style='color: #667eea;'>{last_updated}</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL AVEC MISE EN VALEUR
st.markdown(create_ubisoft_header("Future Insights", "Innovation Lab Analytics & Emerging Workforce Trends"), unsafe_allow_html=True)

# INTRODUCTION AVEC CONTEXTE INNOVATION
st.markdown(create_ubisoft_info_box(
    "🚀 Ubisoft Innovation Lab Excellence",
    "Exploring the future of gaming workforce through cutting-edge analytics, emerging technologies impact, and next-generation talent strategies. Our 12 innovation labs globally with $127M R&D investment and 94/100 innovation index prepare Ubisoft for the evolving gaming landscape with 47 patents filed in 2024."
), unsafe_allow_html=True)

# MÉTRIQUES INNOVATION AVEC STYLE PROFESSIONNEL
st.markdown(create_ubisoft_section_header("🎯 Innovation Excellence Metrics"), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #667eea; margin-bottom: 0.5rem;'>🧪</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>94/100</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Innovation Index</p>
        <small style='color: #28A745;'>Industry-leading</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #667eea; margin-bottom: 0.5rem;'>🎮</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>$127M</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>R&D Investment</p>
        <small style='color: #28A745;'>Annual budget</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #667eea; margin-bottom: 0.5rem;'>🔬</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>47</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Patents Filed</p>
        <small style='color: #28A745;'>Gaming tech 2024</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #667eea; margin-bottom: 0.5rem;'>💡</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>12</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Innovation Labs</p>
        <small style='color: #666;'>Global network</small>
    </div>
    """, unsafe_allow_html=True)

# EMERGING TECHNOLOGIES IMPACT
st.markdown(create_ubisoft_section_header("🔮 Emerging Technologies Impact"), unsafe_allow_html=True)

# Technology adoption data
tech_data = {
    'Technology': ['AI/Machine Learning', 'Virtual Reality', 'Augmented Reality', 'Blockchain/NFTs',
                   'Cloud Computing', 'Real-time Ray Tracing', 'Procedural Generation', '5G Gaming'],
    'Current_Adoption': [78, 45, 32, 25, 85, 67, 58, 28],
    'Future_Potential': [95, 82, 75, 48, 98, 89, 84, 72],
    'Workforce_Impact': [87, 65, 58, 35, 76, 43, 52, 39],
    'Investment_Priority': [9.2, 7.8, 7.1, 4.2, 8.9, 6.8, 7.5, 5.9]
}

tech_df = pd.DataFrame(tech_data)

col1, col2 = st.columns(2)

with col1:
    fig_tech_adoption = px.scatter(
        tech_df,
        x='Current_Adoption',
        y='Future_Potential',
        size='Investment_Priority',
        color='Workforce_Impact',
        hover_name='Technology',
        title='🚀 Technology Adoption vs Future Potential',
        labels={
            'Current_Adoption': 'Current Adoption (%)',
            'Future_Potential': 'Future Potential (%)',
            'Workforce_Impact': 'Workforce Impact Score'
        },
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_tech_adoption.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_tech_adoption, width='stretch')

with col2:
    # Technology priorities ranking
    st.markdown("### 🎯 Technology Investment Priorities")
    tech_ranked = tech_df.nlargest(6, 'Investment_Priority')
    
    for i, row in tech_ranked.iterrows():
        priority_color = UBISOFT_COLORS['primary'] if row['Investment_Priority'] > 7 else '#FFD700'
        st.markdown(f"""
        <div style='background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 5px; border-left: 4px solid {priority_color};'>
            <strong style='color: #2C3E50;'>{i+1}. {row['Technology']}</strong><br>
            <span style='color: {priority_color}; font-weight: bold;'>Priority: {row['Investment_Priority']}/10</span><br>
            <span style='color: #666; font-size: 0.9rem;'>📈 Future potential: {row['Future_Potential']}%</span>
        </div>
        """, unsafe_allow_html=True)

# SKILLS EVOLUTION
st.markdown(create_ubisoft_section_header("📚 Skills Evolution & Future Workforce"), unsafe_allow_html=True)

# Skills demand evolution
skills_evolution = {
    'Skill': ['Unity Development', 'Unreal Engine', 'AI/ML Engineering', 'VR Development',
              'UI/UX Design', 'Data Analytics', 'DevOps Engineering', 'Blockchain Dev',
              'Cloud Architecture', 'Game Analytics', 'Procedural Art', 'Mobile Development'],
    '2024_Demand': [95, 88, 68, 45, 82, 74, 78, 25, 71, 63, 52, 69],
    '2026_Projected': [92, 85, 89, 78, 85, 87, 82, 45, 89, 81, 74, 73],
    'Growth_Rate': [0, 0, 31, 73, 4, 18, 5, 80, 25, 29, 42, 6],
    'Talent_Gap': [23, 34, 67, 78, 18, 42, 28, 89, 51, 38, 72, 25]
}

skills_df = pd.DataFrame(skills_evolution)
skills_df['Priority_Score'] = (skills_df['2026_Projected'] * skills_df['Talent_Gap'] / 100).round(1)

fig_skills_evolution = go.Figure()

fig_skills_evolution.add_trace(go.Bar(
    name='2024 Demand',
    x=skills_df['Skill'],
    y=skills_df['2024_Demand'],
    marker_color='rgba(0, 153, 255, 0.6)'
))

fig_skills_evolution.add_trace(go.Bar(
    name='2026 Projected',
    x=skills_df['Skill'],
    y=skills_df['2026_Projected'],
    marker_color=UBISOFT_COLORS['primary']
))

fig_skills_evolution.update_layout(
    title="📈 Skills Demand Evolution (2024 vs 2026)",
    barmode='group',
    **get_ubisoft_chart_config()['layout']
)

st.plotly_chart(fig_skills_evolution, width='stretch')

# FUTURE WORKFORCE SCENARIOS
st.markdown(create_ubisoft_section_header("🎲 Future Workforce Scenarios"), unsafe_allow_html=True)

scenarios_data = {
    'Scenario': ['Conservative Growth', 'Aggressive Expansion', 'AI-Augmented', 'Remote-First'],
    'Headcount_2026': [17500, 22000, 16800, 18200],
    'Remote_Percentage': [35, 28, 42, 85],
    'AI_Adoption': [65, 70, 95, 75],
    'Innovation_Score': [88, 92, 96, 86],
    'Cost_Efficiency': [78, 72, 89, 94]
}

scenarios_df = pd.DataFrame(scenarios_data)

fig_scenarios = go.Figure()

fig_scenarios.add_trace(go.Scatterpolar(
    r=scenarios_df['Innovation_Score'],
    theta=scenarios_df['Scenario'],
    fill='toself',
    name='Scenario Impact'
))

fig_scenarios.update_layout(
    title="🔮 Future Workforce Scenarios",
    polar=dict(radialaxis=dict(visible=True)),
    **get_ubisoft_chart_config()['layout']
)

st.plotly_chart(fig_scenarios, width='stretch')

# INNOVATION PIPELINE AVEC STYLE AMÉLIORÉ
st.markdown(create_ubisoft_section_header("🧪 Innovation Pipeline"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🔬</div>
        <h4 style='color: white; margin: 0;'>Research Phase</h4>
        <div style='margin: 1rem 0; text-align: left;'>
            <strong>• Neural Game AI:</strong> Adaptive NPCs<br>
            <strong>• Quantum Rendering:</strong> Ultra-realistic<br>
            <strong>• Biometric UX:</strong> Emotion-based<br>
            <strong>• Haptic Worlds:</strong> Full-body feedback
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0099FF, #00CCFF); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🚀</div>
        <h4 style='color: white; margin: 0;'>Development Phase</h4>
        <div style='margin: 1rem 0; text-align: left;'>
            <strong>• Voice Synthesis:</strong> Dynamic dialogue<br>
            <strong>• Procedural Worlds:</strong> Infinite content<br>
            <strong>• AR Integration:</strong> Mixed reality<br>
            <strong>• AI Assistants:</strong> Creative co-pilots
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #28A745, #34CE57); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🎮</div>
        <h4 style='color: white; margin: 0;'>Deployment Phase</h4>
        <div style='margin: 1rem 0; text-align: left;'>
            <strong>• Cloud Streaming:</strong> Instant access<br>
            <strong>• Real-time Ray Tracing:</strong> Enhanced<br>
            <strong>• Cross-platform Play:</strong> Universal<br>
            <strong>• Predictive Analytics:</strong> Player insights
        </div>
    </div>
    """, unsafe_allow_html=True)

# CHALLENGES & OPPORTUNITIES
st.markdown(create_ubisoft_section_header("⚡ Future Challenges & Strategic Opportunities"), unsafe_allow_html=True)

challenges_opportunities = {
    'Area': ['Talent Acquisition', 'Skills Development', 'Technology Adoption', 'Market Competition',
             'Remote Collaboration', 'Innovation Speed', 'Cost Management', 'Regulatory Compliance'],
    'Challenge_Level': [78, 82, 65, 89, 58, 75, 67, 45],
    'Opportunity_Score': [85, 92, 88, 76, 94, 89, 73, 62],
    'Strategic_Priority': [9.2, 9.5, 8.8, 8.1, 7.8, 9.1, 7.2, 6.5]
}

challenges_df = pd.DataFrame(challenges_opportunities)

fig_challenges = px.scatter(
    challenges_df,
    x='Challenge_Level',
    y='Opportunity_Score',
    size='Strategic_Priority',
    color='Strategic_Priority',
    hover_name='Area',
    title='⚡ Challenges vs Opportunities Matrix',
    labels={
        'Challenge_Level': 'Challenge Level (1-100)',
        'Opportunity_Score': 'Opportunity Score (1-100)',
        'Strategic_Priority': 'Strategic Priority (1-10)'
    },
    color_continuous_scale=['#E60012', '#FFD700', '#0099FF']
)

fig_challenges.update_layout(**get_ubisoft_chart_config()['layout'])
st.plotly_chart(fig_challenges, width='stretch')

# FOOTER PROFESSIONNEL
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 5px; margin-top: 2rem;'>
    <p style='color: #666; margin: 0; font-size: 0.9rem;'>
        © 2024 Ubisoft Entertainment - Gaming Workforce Observatory<br>
        Future Insights Dashboard • Innovation Lab Analytics • Confidential and Proprietary Information
    </p>
</div>
""", unsafe_allow_html=True)
