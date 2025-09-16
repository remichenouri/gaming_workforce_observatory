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

# Imports centralisés et templates
from config.app_config import setup_page_config, GAMING_THEME, get_chart_config
from components.page_template import create_page_header, create_metrics_row, create_sidebar_filters

# ─────────────────────────────────────────────
# 🚀 Configuration de la page
# ─────────────────────────────────────────────
setup_page_config()

# ─────────────────────────────────────────────
# ◀️ Sidebar (filtres ou simple nav)
# ─────────────────────────────────────────────
filters = create_sidebar_filters()

# ─────────────────────────────────────────────
# 🎮 Header principal
# ─────────────────────────────────────────────
create_page_header(
    "🏠 Executive Dashboard",
    "C-Suite Strategic Workforce Intelligence"
)

# ─────────────────────────────────────────────
# 🎯 Key Performance Indicators
# ─────────────────────────────────────────────
metrics = [
    ("👥 Talent Pool", "2,847", "+12% vs Q3", GAMING_THEME['primary']),
    ("🌍 Studios Worldwide", "25", "Global Presence", GAMING_THEME['accent']),
    ("🎯 Retention Rate", "87.3%", "+5.2% YoY", GAMING_THEME['success']),
    ("🚀 Innovation Index", "94/100", "Industry Leading", GAMING_THEME['warning'])
]
create_metrics_row(metrics)

# ─────────────────────────────────────────────
# 🌍 Global Studios Performance
# ─────────────────────────────────────────────
st.subheader("🌍 Global Studios Performance")
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
    title=None,
    color_continuous_scale=['#0066CC', '#0099FF', '#00CCFF']
)
fig_studios.update_layout(**get_chart_config())
st.plotly_chart(fig_studios, use_container_width=True)

# ─────────────────────────────────────────────
# 📈 Workforce Trends & Predictions
# ─────────────────────────────────────────────
st.subheader("📈 Workforce Trends & Predictions")
months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
trend_data = {
    'Month': months,
    'Headcount': [2650 + i*15 + np.random.randint(-20, 30) for i in range(len(months))],
}
df_trends = pd.DataFrame(trend_data)

fig_trends = go.Figure()
fig_trends.add_trace(go.Scatter(
    x=df_trends['Month'],
    y=df_trends['Headcount'],
    mode='lines+markers',
    name='Total Headcount Ubisoft',
    line=dict(color=GAMING_THEME['primary'], width=3)
))
fig_trends.update_layout(title=None, **get_chart_config())
st.plotly_chart(fig_trends, use_container_width=True)

# ─────────────────────────────────────────────
# 🏆 Industry Benchmarks
# ─────────────────────────────────────────────
st.subheader("🏆 Industry Benchmarks")
benchmark_data = {
    'Metric': ['Retention Rate', 'Sprint Velocity', 'Bug Fix Rate', 'Employee NPS', 'Innovation Index'],
    'Gaming Avg': [68, 35, 78, 6.8, 65],
    'Ubisoft': [87, 42, 85, 7.8, 94],
    'Target': [85, 40, 85, 7.5, 75]
}
df_benchmark = pd.DataFrame(benchmark_data)

fig_benchmark = go.Figure()
fig_benchmark.add_trace(go.Bar(
    name='Gaming Avg',
    x=df_benchmark['Metric'],
    y=df_benchmark['Gaming Avg'],
    marker_color='rgba(100,100,100,0.6)'
))
fig_benchmark.add_trace(go.Bar(
    name='Ubisoft',
    x=df_benchmark['Metric'],
    y=df_benchmark['Ubisoft'],
    marker_color=GAMING_THEME['primary']
))
fig_benchmark.add_trace(go.Scatter(
    name='Target',
    x=df_benchmark['Metric'],
    y=df_benchmark['Target'],
    mode='markers',
    marker=dict(color=GAMING_THEME['accent'], size=10, symbol='diamond')
))
fig_benchmark.update_layout(barmode='group', title=None, **get_chart_config())
st.plotly_chart(fig_benchmark, use_container_width=True)
