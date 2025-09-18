"""
🎮 Ubisoft Gaming Workforce Observatory
Neurodiversity ROI - Inclusion Excellence & Business Impact
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

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

st.set_page_config(
    page_title="Ubisoft Neurodiversity ROI - Inclusion Excellence",
    page_icon="🧠",
    layout="wide"
)

# SIDEBAR ÉPURÉE - MENU SEULEMENT
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #0099FF; font-family: Arial, sans-serif; margin: 0;'>🧠 Ubisoft</h2>
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
        if name == "Neurodiversity ROI":
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
<div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; border-left: 4px solid #0099FF;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: #2C3E50;'>🧠 Neurodiversity ROI - Inclusion Excellence</strong>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Business Impact Analysis • Performance Metrics • Accommodation ROI</p>
        </div>
        <div style='text-align: right;'>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Last Updated</p>
            <strong style='color: #0099FF;'>{last_updated}</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL AVEC MISE EN VALEUR
st.markdown(create_ubisoft_header("Neurodiversity ROI", "Inclusion Excellence & Measurable Business Impact"), unsafe_allow_html=True)

# INTRODUCTION AVEC CONTEXTE BUSINESS
st.markdown(create_ubisoft_info_box(
    "🧠 Ubisoft Neurodiversity Excellence Program",
    "Notre programme d'inclusion de la neurodiversité génère un impact business mesurable de $3.2M annuellement. Avec 18.3% de talents neurodivergents, Ubisoft démontre que l'inclusion améliore l'innovation (+23%), la qualité (+31% détection bugs) et la performance globale des équipes de développement gaming."
), unsafe_allow_html=True)

# MÉTRIQUES CLÉS AVEC STYLE PROFESSIONNEL
st.markdown(create_ubisoft_section_header("🎯 Key Performance Indicators"), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>🧠</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>18.3%</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Neurodiverse Talent Pool</p>
        <small style='color: #28A745;'>+4.2% vs 2023</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>💡</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>+23%</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Innovation Score</p>
        <small style='color: #28A745;'>Teams with ND members</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>🔍</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>+31%</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Bug Detection Rate</p>
        <small style='color: #28A745;'>QA teams advantage</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>💰</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>$47K</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>ROI per ND Hire</p>
        <small style='color: #28A745;'>Annual value add</small>
    </div>
    """, unsafe_allow_html=True)

# PERFORMANCE ANALYSIS
st.markdown(create_ubisoft_section_header("📈 Team Performance Analysis"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    teams_data = {
        'Team_Type': ['Neurotypical Only', 'Mixed Teams (10-30%)', 'Mixed Teams (30%+)', 'ND-Led Teams'],
        'Innovation_Score': [72, 89, 94, 97],
        'Problem_Solving': [75, 87, 92, 95],
        'Code_Quality': [78, 82, 88, 91],
        'Team_Count': [45, 28, 15, 8]
    }
    
    teams_df = pd.DataFrame(teams_data)
    
    fig_performance = go.Figure()
    
    fig_performance.add_trace(go.Bar(
        name='Innovation Score',
        x=teams_df['Team_Type'],
        y=teams_df['Innovation_Score'],
        marker_color=UBISOFT_COLORS['primary']
    ))
    
    fig_performance.add_trace(go.Bar(
        name='Problem Solving',
        x=teams_df['Team_Type'],
        y=teams_df['Problem_Solving'],
        marker_color=UBISOFT_COLORS['accent']
    ))
    
    fig_performance.update_layout(
        title="🎮 Team Performance by Neurodiversity Composition",
        barmode='group',
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_performance, width='stretch')

with col2:
    months = pd.date_range('2024-01-01', periods=12, freq='M')
    roi_data = {
        'Month': months,
        'Cumulative_ROI': [15000, 32000, 51000, 73000, 98000, 127000, 
                          158000, 192000, 230000, 271000, 315000, 362000],
        'Monthly_Impact': [15000, 17000, 19000, 22000, 25000, 29000,
                          31000, 34000, 38000, 41000, 44000, 47000]
    }
    
    roi_df = pd.DataFrame(roi_data)
    
    fig_roi = go.Figure()
    
    fig_roi.add_trace(go.Scatter(
        x=roi_df['Month'],
        y=roi_df['Cumulative_ROI'],
        mode='lines+markers',
        name='Cumulative ROI ($)',
        line=dict(color=UBISOFT_COLORS['primary'], width=3),
        fill='tonexty'
    ))
    
    fig_roi.update_layout(
        title="💰 Neurodiversity Program ROI 2024",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_roi, width='stretch')

# SKILLS ANALYSIS
st.markdown(create_ubisoft_section_header("🎯 Neurodivergent Excellence Areas"), unsafe_allow_html=True)

skills_analysis = {
    'Skill_Area': ['Pattern Recognition', 'Quality Assurance', 'Data Analysis', 
                   'System Architecture', 'Creative Problem Solving', 'Detail Orientation',
                   'Mathematical Modeling', 'Memory & Recall'],
    'ND_Performance': [95, 92, 88, 85, 91, 97, 89, 94],
    'NT_Performance': [73, 76, 78, 82, 84, 79, 75, 71],
    'Ubisoft_Value': [23, 28, 15, 18, 22, 31, 19, 26]
}

skills_df = pd.DataFrame(skills_analysis)
skills_df['Advantage'] = skills_df['ND_Performance'] - skills_df['NT_Performance']

fig_skills = px.bar(
    skills_df,
    x='Skill_Area',
    y='Advantage',
    color='Ubisoft_Value',
    title='🧠 Neurodivergent Talent Advantages by Skill Area',
    labels={'Advantage': 'Performance Advantage (%)', 'Ubisoft_Value': 'Business Value ($K)'},
    color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
)

fig_skills.update_layout(**get_ubisoft_chart_config()['layout'])
st.plotly_chart(fig_skills, width='stretch')

# SUCCESS STORIES AVEC STYLE AMÉLIORÉ
st.markdown(create_ubisoft_section_header("🌟 Success Stories"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0099FF, #00CCFF); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🎮</div>
        <h4 style='color: white; margin: 0;'>QA Excellence</h4>
        <div style='margin: 1rem 0;'>
            <strong>Team Lead with Autism</strong><br/>
            • 47% faster bug detection<br/>
            • 89% accuracy improvement<br/>
            • Mentored 12 junior testers<br/>
            • Saved $340K in post-launch fixes
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #28A745, #34CE57); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🎨</div>
        <h4 style='color: white; margin: 0;'>Creative Innovation</h4>
        <div style='margin: 1rem 0;'>
            <strong>Game Designer with ADHD</strong><br/>
            • Led 3 award-winning features<br/>
            • 156% faster ideation process<br/>
            • Cross-team collaboration champion<br/>
            • Generated $2.3M in new revenue
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #E60012, #FF1744); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>⚙️</div>
        <h4 style='color: white; margin: 0;'>Technical Mastery</h4>
        <div style='margin: 1rem 0;'>
            <strong>Senior Developer with Dyslexia</strong><br/>
            • Optimized core engine (+34% perf)<br/>
            • Reduced load times by 52%<br/>
            • Mentored 8 junior developers<br/>
            • Patent holder (3 innovations)
        </div>
    </div>
    """, unsafe_allow_html=True)

# ACCOMMODATION ROI
st.markdown(create_ubisoft_section_header("🛠️ Accommodation Investment & Returns"), unsafe_allow_html=True)

accommodation_data = {
    'Accommodation': ['Noise-Canceling Headphones', 'Flexible Work Hours', 'Specialized Software',
                     'Quiet Workspaces', 'Task Management Tools', 'Communication Apps',
                     'Ergonomic Equipment', 'Training Programs'],
    'Cost_Per_Employee': [250, 0, 850, 1200, 180, 120, 650, 2400],
    'Productivity_Gain': [15, 28, 35, 42, 22, 18, 12, 67],
    'Satisfaction_Increase': [8.2, 9.1, 7.8, 9.4, 7.2, 6.9, 6.1, 8.8]
}

acc_df = pd.DataFrame(accommodation_data)

fig_accommodations = px.scatter(
    acc_df,
    x='Cost_Per_Employee',
    y='Productivity_Gain',
    size='Satisfaction_Increase',
    color='Satisfaction_Increase',
    hover_name='Accommodation',
    title='💡 Accommodation Cost vs Productivity Impact',
    labels={
        'Cost_Per_Employee': 'Cost per Employee (USD)',
        'Productivity_Gain': 'Productivity Gain (%)',
        'Satisfaction_Increase': 'Satisfaction Increase'
    },
    color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
)

fig_accommodations.update_layout(**get_ubisoft_chart_config()['layout'])
st.plotly_chart(fig_accommodations, width='stretch')

# FOOTER PROFESSIONNEL
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 5px; margin-top: 2rem;'>
    <p style='color: #666; margin: 0; font-size: 0.9rem;'>
        © Gaming Workforce Observatory<br>
        Neurodiversity ROI Dashboard • Inclusion Excellence • Confidential and Proprietary Information
    </p>
</div>
""", unsafe_allow_html=True)
