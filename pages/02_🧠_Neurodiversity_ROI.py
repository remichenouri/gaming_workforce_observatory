"""
🎮 Ubisoft Gaming Workforce Observatory
Neurodiversity ROI - Inclusion Excellence & Business Impact
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─────────────────────────────────────────────
# STUBS POUR THEME & COMPOSANTS UBISOFT
# Appliquer ABSOLUMENT dans chaque page à remplacer
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
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    return f"<h1>{title}</h1>{subtitle_html}"

def create_ubisoft_breadcrumb(page):
    return f"<p>🎮 Ubisoft Observatory → {page}</p>"

def create_ubisoft_section_header(title):
    return f"<h3>{title}</h3>"

def create_ubisoft_info_box(title, content):
    return f"<div><strong>{title}</strong><p>{content}</p></div>"

def create_ubisoft_accent_box(title, content):
    return f"<div style='border-left:4px solid #E60012'><strong>{title}</strong><p>{content}</p></div>"

def get_ubisoft_chart_config():
    return {'layout': {}}

def create_ubisoft_metric_cols(metrics, cols=4):
    for metric in metrics:
        st.markdown(f"**{metric['title']}**: {metric['value']}")

def display_ubisoft_logo_section():
    return "<p>© 2024 Ubisoft</p>"
# ─────────────────────────────────────────────


st.set_page_config(
    page_title="Ubisoft Neurodiversity ROI - Inclusion Excellence",
    page_icon="🧠",
    layout="wide"
)

neurodiversity_metrics = [
    {"title": "Neurodiverse Talent Pool", "value": "18.3%", "delta": "+4.2% vs 2023", "icon": "🧠"},
    {"title": "Innovation Score Increase", "value": "+23%", "delta": "Teams with ND members", "icon": "💡"},
    {"title": "Bug Detection Rate", "value": "+31%", "delta": "QA teams advantage", "icon": "🔍"},
    {"title": "ROI per ND Hire", "value": "$47K", "delta": "Annual value add", "icon": "💰"}
]

create_ubisoft_metric_cols(neurodiversity_metrics)

# Performance Analysis
st.markdown(create_ubisoft_section_header("📈 Ubisoft Neurodiverse Teams Performance"))

col1, col2 = st.columns(2)

with col1:
    # Team performance comparison
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
        title="🎮 Ubisoft Team Performance by Neurodiversity Composition",
        barmode='group',
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_performance, use_container_width=True)

with col2:
    # ROI over time
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
        title="💰 Ubisoft Neurodiversity Program ROI 2024",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_roi, use_container_width=True)

# Skills Analysis
st.markdown(create_ubisoft_section_header("🎯 Ubisoft Neurodivergent Excellence Areas"))

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
    title='🧠 Ubisoft: Neurodivergent Talent Advantages by Skill Area',
    labels={'Advantage': 'Performance Advantage (%)', 'Ubisoft_Value': 'Business Value ($K)'},
    color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
)

fig_skills.update_layout(get_ubisoft_chart_config()['layout'])
st.plotly_chart(fig_skills, use_container_width=True)

# Success Stories
st.markdown(create_ubisoft_section_header("🌟 Ubisoft Neurodiversity Success Stories"))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">🎮 QA Excellence</h4>
        <p style="color: #F5F5F5;">
            <strong>Team Lead with Autism</strong><br/>
            • 47% faster bug detection<br/>
            • 89% accuracy improvement<br/>
            • Mentored 12 junior testers<br/>
            • Saved $340K in post-launch fixes
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">🎨 Creative Innovation</h4>
        <p style="color: #F5F5F5;">
            <strong>Game Designer with ADHD</strong><br/>
            • Led 3 award-winning features<br/>
            • 156% faster ideation process<br/>
            • Cross-team collaboration champion<br/>
            • Generated $2.3M in new revenue
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">⚙️ Technical Mastery</h4>
        <p style="color: #F5F5F5;">
            <strong>Senior Developer with Dyslexia</strong><br/>
            • Optimized core engine (+34% perf)<br/>
            • Reduced load times by 52%<br/>
            • Mentored 8 junior developers<br/>
            • Patent holder (3 innovations)
        </p>
    </div>
    """, unsafe_allow_html=True)

# Accommodation ROI
st.markdown(create_ubisoft_section_header("🛠️ Ubisoft Accommodation Investment & Returns"))

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
    title='💡 Ubisoft: Accommodation Cost vs Productivity Impact',
    labels={
        'Cost_Per_Employee': 'Cost per Employee (USD)',
        'Productivity_Gain': 'Productivity Gain (%)',
        'Satisfaction_Increase': 'Satisfaction Increase'
    },
    color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
)

fig_accommodations.update_layout(get_ubisoft_chart_config()['layout'])
st.plotly_chart(fig_accommodations, use_container_width=True)

with st.sidebar:
    st.markdown("""
    ## 🧠 Neurodiversity ROI
    
    **Inclusion Excellence**
    
    📊 **Measurable Impact** on business outcomes
    
    🎯 **Performance Analytics** by team composition
    
    💰 **ROI Tracking** accommodation investments
    
    🌟 **Success Stories** from Ubisoft teams
    
    ---
    
    ### 🎮 Key Focus Areas
    - Quality Assurance Excellence
    - Pattern Recognition
    - Creative Problem Solving  
    - Technical Innovation
    - Data Analysis
    - System Architecture
    
    ---
    
    ### 📈 2024 Achievements
    - **18.3%** neurodiverse workforce
    - **$3.2M** total ROI generated
    - **94%** retention rate
    - **23%** innovation boost
    """)
