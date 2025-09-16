import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

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
# CHARGEMENT DES DONNÉES RÉELLES
@st.cache_data
def load_data():
    # Utiliser les fichiers réels de votre repo GitHub
    try:
        # Charger le fichier principal des employés
        df_employees = pd.read_csv('data/gaming_workforce_employees_advanced.csv')
        df_projects = pd.read_csv('data/gaming_workforce_projects_advanced.csv')
        df_sample = pd.read_csv('data/sample_data.csv')
        
        # Ajouter une source d'identification
        df_employees['Source'] = f'Employees Advanced ({len(df_employees):,} records)'
        df_projects['Source'] = f'Projects Advanced ({len(df_projects):,} records)'
        df_sample['Source'] = f'Sample Data ({len(df_sample):,} records)'
        
        # Convertir les scores si les colonnes existent
        for df in [df_employees, df_projects, df_sample]:
            if 'SatisfactionScore' in df.columns:
                df['SatisfactionPct'] = df['SatisfactionScore'] / df['SatisfactionScore'].max() * 100
            if 'PerformanceScore' in df.columns:
                df['PerformancePct'] = df['PerformanceScore'] / df['PerformanceScore'].max() * 100
        
        # Combiner les datasets qui ont des colonnes compatibles
        combined_dfs = []
        for df in [df_employees, df_projects, df_sample]:
            if not df.empty:
                combined_dfs.append(df)
        
        return pd.concat(combined_dfs, ignore_index=True, sort=False)
        
    except FileNotFoundError as e:
        st.error(f"Fichier non trouvé: {e}")
        # Fallback: générer des données de démonstration
        return generate_demo_data()

def generate_demo_data():
    """Génère des données de démonstration en cas d'absence des fichiers CSV"""
    np.random.seed(42)
    demo_data = pd.DataFrame({
        'EmployeeID': range(1, 1001),
        'Age': np.random.randint(22, 60, 1000),
        'Department': np.random.choice(['Game Design', 'Programming', 'Art', 'QA', 'Production'], 1000),
        'Location': np.random.choice(['Montreal', 'Paris', 'Milan', 'Shanghai'], 1000),
        'Salary': np.random.randint(45000, 120000, 1000),
        'SatisfactionScore': np.random.uniform(3.0, 9.5, 1000),
        'PerformanceScore': np.random.uniform(3.5, 9.8, 1000),
        'TenureYears': np.random.uniform(0.5, 15.0, 1000),
        'Source': 'Demo Data (1,000 records)'
    })
    demo_data['SatisfactionPct'] = demo_data['SatisfactionScore'] / demo_data['SatisfactionScore'].max() * 100
    demo_data['PerformancePct'] = demo_data['PerformanceScore'] / demo_data['PerformanceScore'].max() * 100
    return demo_data

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
    
    # Affichage des sources de données disponibles
    st.markdown("### 📊 Data Sources")
    sources_info = df_all['Source'].value_counts()
    for source, count in sources_info.items():
        st.markdown(f"• **{source}**: {count:,} rows")

# ─────────────────────────────────────────────
# HEADER PRINCIPAL
last_updated = datetime.now().strftime('%Y-%m-%d %H:%M')
st.markdown(f"""
<div style='background: #f8f9fa; padding: 1rem; border-left: 4px solid #28A745;
            border-radius:5px; margin-bottom:1rem;'>
  <div style='display:flex; justify-content:space-between;'>
    <div>
      <strong style='color:#2C3E50;'>🎮 Ubisoft Gaming Workforce Observatory</strong><br>
      <small style='color:#666;'>Real Data Analysis • {len(df_all):,} Total Records</small>
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
    "Real Gaming Workforce Data Intelligence"
), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SÉLECTEUR DE SOURCE
sources = df_all['Source'].unique()
selected = st.multiselect("Sélectionnez les sources de données :", sources, default=list(sources))
df = df_all[df_all['Source'].isin(selected)]

# ─────────────────────────────────────────────
# SECTION KPI
st.markdown(create_ubisoft_section_header("🎯 Key Performance Indicators"), unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    if 'SatisfactionPct' in df.columns:
        sat_avg = df['SatisfactionPct'].mean()
        st.metric("Avg Satisfaction (%)", f"{sat_avg:.1f}")
    else:
        st.metric("Records", f"{len(df):,}")

with k2:
    if 'PerformancePct' in df.columns:
        perf_avg = df['PerformancePct'].mean()
        st.metric("Avg Performance (%)", f"{perf_avg:.1f}")
    else:
        st.metric("Sources", f"{len(selected)}")

with k3:
    if 'Age' in df.columns:
        age_avg = df['Age'].mean()
        st.metric("Avg Age", f"{age_avg:.1f} yrs")
    else:
        st.metric("Columns", f"{len(df.columns)}")

with k4:
    if 'TenureYears' in df.columns:
        tenure_avg = df['TenureYears'].mean()
        st.metric("Avg Tenure", f"{tenure_avg:.1f} yrs")
    else:
        st.metric("Data Quality", "✓ Good")

# ─────────────────────────────────────────────
# VISUALISATIONS CONDITIONNELLES
if 'PerformancePct' in df.columns and 'SatisfactionPct' in df.columns:
    st.markdown(create_ubisoft_section_header("📊 Performance vs Satisfaction"), unsafe_allow_html=True)
    fig1 = px.scatter(
        df, x='PerformancePct', y='SatisfactionPct',
        color='Source', 
        size='TenureYears' if 'TenureYears' in df.columns else None,
        title="Performance vs Satisfaction Analysis"
    )
    fig1.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig1, use_container_width=True)

if 'Department' in df.columns:
    st.markdown(create_ubisoft_section_header("🏢 Department Distribution"), unsafe_allow_html=True)
    fig2 = px.histogram(
        df, x='Department', color='Source',
        title="Workforce Distribution by Department"
    )
    fig2.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig2, use_container_width=True)

if 'Salary' in df.columns:
    st.markdown(create_ubisoft_section_header("💰 Salary Analysis"), unsafe_allow_html=True)
    fig3 = px.box(
        df, x='Source', y='Salary',
        title="Salary Distribution by Source"
    )
    fig3.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────
# APERÇU DES DONNÉES
st.markdown(create_ubisoft_section_header("🔍 Data Preview"), unsafe_allow_html=True)
st.dataframe(df.head(100), use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:2rem; background:#f8f9fa; border-radius:5px;'>
  <small style='color:#666;'>© 2025 Ubisoft Entertainment • Gaming Workforce Observatory • Confidential</small>
</div>
""", unsafe_allow_html=True)
