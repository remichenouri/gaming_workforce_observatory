import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ─────────────────────────────────────────────
# STUBS POUR THÈME & COMPOSANTS UBISOFT
def apply_ubisoft_theme():
    pass

UBISOFT_COLORS = {
    'primary':  '#0099FF',
    'accent':   '#E60012',
    'success':  '#28A745',
    'warning':  '#FFB020',
    'text':     '#2C3E50'
}

def create_ubisoft_header(title, subtitle=None):
    subtitle_html = (
        f"<p style='font-size:1.2rem; color:#555; margin-top:0.5rem;'>{subtitle}</p>"
        if subtitle else ""
    )
    return f"""
    <div style='background: linear-gradient(90deg, #0099FF, #00CCFF);
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
        <h1 style='font-family: Arial, sans-serif; font-weight: bold;
                   font-size: 3rem; color: white; margin: 0;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
            {title}
        </h1>
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title):
    return f"""
    <h2 style='color: #2C3E50; font-family: Arial, sans-serif;
               font-weight: bold; border-left: 4px solid #0099FF;
               padding-left: 1rem; margin: 2rem 0 1rem 0;'>
        {title}
    </h2>
    """

def create_ubisoft_info_box(title, content):
    return f"""
    <div style='background: #f8f9fa; border-left: 4px solid #0099FF;
                padding: 1.5rem; margin: 1rem 0; border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
        <h4 style='color: #2C3E50; margin: 0 0 0.5rem 0;'>{title}</h4>
        <p style='color: #555; margin: 0; font-size: 1rem;
                  line-height: 1.5;'>{content}</p>
    </div>
    """

def get_ubisoft_chart_config():
    return {
        'layout': {
            'font': {'family': 'Arial, sans-serif', 'size': 12, 'color': '#2C3E50'},
            'paper_bgcolor': 'white',
            'plot_bgcolor': '#fafafa',
            'margin': {'l':40,'r':40,'t':50,'b':40}
        }
    }

# ─────────────────────────────────────────────
# CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Ubisoft Gaming Workforce Observatory",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
@st.cache_data
def load_data():
    df_basic    = pd.read_csv('generated_employee_data.csv')
    df_enriched = pd.read_csv('enriched_employee_data.csv')
    # Convertir scores en pourcentage
    for df in (df_basic, df_enriched):
        df['SatisfactionPct'] = df['SatisfactionScore'] / df['SatisfactionScore'].max() * 100
        df['PerformancePct']   = df['PerformanceScore']   / df['PerformanceScore'].max()   * 100
    # Identifier la source
    df_basic['Source']    = f'Basic ({len(df_basic):,} lines)'
    df_enriched['Source'] = f'Enriched ({len(df_enriched):,} lines)'
    return pd.concat([df_basic, df_enriched], ignore_index=True)

df_all = load_data()

# ─────────────────────────────────────────────
# BARRE LATÉRALE
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #0099FF; font-family: Arial, sans-serif; margin: 0;'>🎮 Ubisoft</h2>
        <p style='color: #666; font-size: 0.9rem; margin: 0.5rem 0;'>Workforce Observatory</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h4 style='color: #2C3E50;'>Navigation</h4>", unsafe_allow_html=True)
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
    for icon, name in menu_items:
        if name == "Executive Dashboard":
            st.markdown(f"<div style='background: #0099FF; color: white; padding: 0.75rem; border-radius:5px;'><strong>{icon} {name}</strong></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='padding: 0.75rem; color: #555;'>{icon} {name}</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER PRINCIPAL
last_updated = datetime.now().strftime('%Y-%m-%d %H:%M')
st.markdown(f"""
<div style='background: #f8f9fa; padding: 1rem; border-left: 4px solid #28A745;
            border-radius:5px; margin-bottom:1rem;'>
  <div style='display:flex; justify-content:space-between;'>
    <div>
      <strong style='color:#2C3E50;'>🎮 Ubisoft Gaming Workforce Observatory</strong><br>
      <small style='color:#666;'>Global Studios • 25 Locations • 15,847 Employees</small>
    </div>
    <div style='text-align:right;'>
      <small style='color:#666;'>Last Updated</small><br>
      <strong style='color:#0099FF;'>{last_updated}</strong>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL
st.markdown(create_ubisoft_header(
    "Executive Dashboard",
    "C-Suite Strategic Workforce Intelligence"
), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SÉLECTEUR DE SOURCE
sources = df_all['Source'].unique()
selected = st.multiselect("Sélectionnez la source de données :", sources, default=list(sources))
df = df_all[df_all['Source'].isin(selected)]

# ─────────────────────────────────────────────
# SECTION KPI
st.markdown(create_ubisoft_section_header("🎯 Key Performance Indicators"), unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Avg Satisfaction (%)", f"{df['SatisfactionPct'].mean():.1f}")
with k2:
    st.metric("Avg Performance (%)", f"{df['PerformancePct'].mean():.1f}")
with k3:
    st.metric("Avg Age", f"{df['Age'].mean():.1f} yrs")
with k4:
    st.metric("Avg Tenure (yrs)", f"{df['TenureYears'].mean():.1f} yrs")

# ─────────────────────────────────────────────
# SCATTER: Performance vs Satisfaction
st.markdown(create_ubisoft_section_header("📊 Performance vs Satisfaction"), unsafe_allow_html=True)
fig1 = px.scatter(
    df, x='PerformancePct', y='SatisfactionPct',
    color='Source', size='TenureYears',
    hover_data=['EmployeeID','Department','Location'],
    labels={'PerformancePct':'Perf (%)','SatisfactionPct':'Sat (%)'},
    title="Performance vs Satisfaction Comparison"
)
fig1.update_layout(**get_ubisoft_chart_config()['layout'])
st.plotly_chart(fig1, use_container_width=True)

# ─────────────────────────────────────────────
# HISTOGRAMME: Effectifs par Département
st.markdown(create_ubisoft_section_header("🏢 Distribution par Département"), unsafe_allow_html=True)
fig2 = px.histogram(
    df, x='Department', color='Source',
    barmode='group', title="Headcount by Department"
)
fig2.update_layout(**get_ubisoft_chart_config()['layout'])
st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# BOXPLOT: Salaires
st.markdown(create_ubisoft_section_header("💰 Répartition des Salaires"), unsafe_allow_html=True)
fig3 = px.box(
    df, x='Source', y='Salary',
    title="Salary Distribution by Source",
    color='Source'
)
fig3.update_layout(**get_ubisoft_chart_config()['layout'])
st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:2rem; background:#f8f9fa; border-radius:5px;'>
  <small style='color:#666;'>© 2025 Ubisoft Entertainment • Confidential and Proprietary Information</small>
</div>
""", unsafe_allow_html=True)
