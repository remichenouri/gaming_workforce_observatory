"""
Gaming Workforce Observatory - Global Studios Dashboard
Analyse mondiale des studios gaming et distribution géographique
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
from pathlib import Path

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
    <div style='background: linear-gradient(90deg, #28A745, #34CE57); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='font-family: Arial, sans-serif; font-weight: bold; font-size: 3.5rem; color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{title}</h1>
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title):
    return f"<h2 style='color: #2C3E50; font-family: Arial, sans-serif; font-weight: bold; border-left: 4px solid #28A745; padding-left: 1rem; margin: 2rem 0 1rem 0;'>{title}</h2>"

def create_ubisoft_info_box(title, content):
    return f"""
    <div style='background: #f8f9fa; border-left: 4px solid #28A745; padding: 1.5rem; margin: 1rem 0; border-radius: 5px;'>
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

def create_metric_card(title, value, subtitle, card_type, icon):
    colors = {
        'info': '#0099FF',
        'success': '#28A745', 
        'warning': '#FFB020',
        'danger': '#E60012'
    }
    color = colors.get(card_type, '#0099FF')
    return f"""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
        <div style="font-size: 2rem; color: {color}; margin-bottom: 0.5rem;">{icon}</div>
        <h3 style="color: #2C3E50; margin: 0; font-size: 2rem;">{value}</h3>
        <p style="color: #666; margin: 0.5rem 0 0 0;">{title}</p>
        <small style="color: #666;">{subtitle}</small>
    </div>
    """

# ─────────────────────────────────────────────

st.set_page_config(
    page_title="🌍 Gaming Workforce Observatory - Global Studios",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SIDEBAR ÉPURÉE - MENU SEULEMENT
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #28A745; font-family: Arial, sans-serif; margin: 0;'>🌍 Ubisoft</h2>
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
        if name == "Global Studios":
            st.markdown(f"""
            <div style='background: #28A745; color: white; padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0;'>
                <strong>{icon} {name}</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0; color: #555;'>
                {icon} {name}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section selector intégré dans le sidebar
    st.markdown("<h4 style='color: #2C3E50; margin-bottom: 1rem;'>Global Sections</h4>", unsafe_allow_html=True)
    
    global_sections = [
        "🌏 Global Overview",
        "🗺️ World Map",
        "📊 Regional Analysis",
        "🏙️ City Competition",
        "🔄 Talent Migration", 
        "💡 Cost Optimization",
        "🚀 Market Opportunities"
    ]
    
    selected_section = st.selectbox(
        "Explore global insights:",
        global_sections,
        index=0
    )

# HEADER PRINCIPAL PROFESSIONNEL
last_updated = datetime.now().strftime('%Y-%m-%d %H:%M')
st.markdown(f"""
<div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; border-left: 4px solid #28A745;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: #2C3E50;'>🌍 Global Studios - Worldwide Intelligence</strong>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Strategic insights • Talent distribution • Market opportunities • 14 countries analyzed</p>
        </div>
        <div style='text-align: right;'>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Last Updated</p>
            <strong style='color: #28A745;'>{last_updated}</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL AVEC MISE EN VALEUR
st.markdown(create_ubisoft_header("Global Studios", "Worldwide Gaming Workforce Intelligence"), unsafe_allow_html=True)

# GÉNÉRATION DES DONNÉES
@st.cache_data(ttl=300)
def generate_global_studios_data():
    """Génère les données des studios gaming mondiaux"""
    
    # Données des studios par région
    studios_data = pd.DataFrame({
        'studio_id': range(1, 201),
        'studio_name': [f'Gaming Studio {i}' for i in range(1, 201)],
        'city': np.random.choice([
            'Los Angeles', 'San Francisco', 'Seattle', 'Montreal', 'Toronto', 'London', 
            'Paris', 'Berlin', 'Stockholm', 'Helsinki', 'Tokyo', 'Seoul', 'Shanghai',
            'Singapore', 'Sydney', 'Melbourne', 'São Paulo', 'Mexico City'
        ], 200),
        'country': np.random.choice([
            'United States', 'Canada', 'United Kingdom', 'France', 'Germany', 'Sweden',
            'Finland', 'Japan', 'South Korea', 'China', 'Singapore', 'Australia', 'Brazil', 'Mexico'
        ], 200),
        'region': np.random.choice(['North America', 'Europe', 'Asia-Pacific', 'Latin America'], 200),
        'studio_size': np.random.choice(['Indie', 'Small', 'Medium', 'Large', 'AAA'], 200, 
                                       p=[0.3, 0.25, 0.25, 0.15, 0.05]),
        'employees': np.random.lognormal(4, 1.2, 200).astype(int).clip(5, 2000),
        'founded_year': np.random.randint(1990, 2024, 200),
        'primary_platform': np.random.choice(['Mobile', 'PC', 'Console', 'Web', 'VR/AR'], 200),
        'genre_focus': np.random.choice([
            'Action', 'RPG', 'Strategy', 'Puzzle', 'Simulation', 'Sports', 'Racing', 'Adventure'
        ], 200),
        'annual_revenue_usd': np.random.lognormal(15, 1.5, 200).astype(int).clip(100000, 500000000),
        'games_published': np.random.poisson(8, 200).clip(1, 50),
        'avg_metacritic': np.random.normal(72, 12, 200).clip(40, 95),
        'remote_workforce_pct': np.random.beta(2, 3, 200) * 100,
        'diversity_index': np.random.beta(3, 2, 200) * 100,
        'glassdoor_rating': np.random.normal(3.8, 0.6, 200).clip(2.0, 5.0)
    })
    
    # Ajout de coordonnées géographiques simulées
    city_coords = {
        'Los Angeles': (34.0522, -118.2437),
        'San Francisco': (37.7749, -122.4194),
        'Seattle': (47.6062, -122.3321),
        'Montreal': (45.5017, -73.5673),
        'Toronto': (43.6532, -79.3832),
        'London': (51.5074, -0.1278),
        'Paris': (48.8566, 2.3522),
        'Berlin': (52.5200, 13.4050),
        'Stockholm': (59.3293, 18.0686),
        'Helsinki': (60.1699, 24.9384),
        'Tokyo': (35.6762, 139.6503),
        'Seoul': (37.5665, 126.9780),
        'Shanghai': (31.2304, 121.4737),
        'Singapore': (1.3521, 103.8198),
        'Sydney': (-33.8688, 151.2093),
        'Melbourne': (-37.8136, 144.9631),
        'São Paulo': (-23.5558, -46.6396),
        'Mexico City': (19.4326, -99.1332)
    }
    
    studios_data['latitude'] = studios_data['city'].map(lambda x: city_coords.get(x, (0, 0))[0])
    studios_data['longitude'] = studios_data['city'].map(lambda x: city_coords.get(x, (0, 0))[1])
    
    # Données de migration des talents
    talent_migration = pd.DataFrame({
        'origin_country': np.random.choice(['United States', 'Canada', 'United Kingdom', 'Germany', 'France'], 150),
        'destination_country': np.random.choice(['United States', 'Canada', 'United Kingdom', 'Germany', 'France'], 150),
        'talent_count': np.random.poisson(15, 150),
        'year': np.random.choice([2022, 2023, 2024], 150),
        'skill_type': np.random.choice(['Programming', 'Art', 'Design', 'Production'], 150)
    })
    
    # Données de coût par région
    regional_costs = pd.DataFrame({
        'region': ['North America', 'Europe', 'Asia-Pacific', 'Latin America'],
        'avg_salary_usd': [95000, 78000, 52000, 38000],
        'cost_of_living_index': [100, 85, 65, 45],
        'talent_availability': [85, 92, 88, 75],  # Score sur 100
        'time_to_hire_days': [45, 38, 52, 35],
        'office_rent_sqft_year': [48, 35, 25, 18],
        'tax_rate_corporate': [25.5, 22.3, 18.7, 28.2]
    })
    
    # Analyse concurrentielle par ville
    city_competition = studios_data.groupby(['city', 'region']).agg({
        'employees': 'sum',
        'studio_name': 'count',
        'annual_revenue_usd': 'sum',
        'glassdoor_rating': 'mean',
        'diversity_index': 'mean'
    }).reset_index()
    
    city_competition.columns = [
        'city', 'region', 'total_workforce', 'studio_count', 
        'total_revenue', 'avg_rating', 'avg_diversity'
    ]
    
    return studios_data, talent_migration, regional_costs, city_competition

# Chargement des données
studios_data, talent_migration, regional_costs, city_competition = generate_global_studios_data()

# CONTENU BASÉ SUR LA SECTION SÉLECTIONNÉE
if selected_section == "🌏 Global Overview":
    st.markdown(create_ubisoft_info_box(
        "🌍 Global Gaming Ecosystem Intelligence",
        "Vue d'ensemble complète de l'écosystème gaming mondial avec 200 studios analysés across 18 villes majeures. Notre intelligence couvre la distribution des talents, les performances par région et les opportunités stratégiques d'expansion internationale."
    ), unsafe_allow_html=True)
    
    st.markdown(create_ubisoft_section_header("🌏 Key Global Metrics"), unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_studios = len(studios_data)
    total_workforce = studios_data['employees'].sum()
    total_revenue = studios_data['annual_revenue_usd'].sum()
    avg_studio_size = studios_data['employees'].mean()
    
    with col1:
        metric_html = create_metric_card(
            "Total Studios", 
            f"{total_studios:,}",
            "Across 18 cities",
            "info",
            "🏢"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col2:
        metric_html = create_metric_card(
            "Global Workforce", 
            f"{total_workforce:,}",
            "Gaming professionals",
            "success",
            "👥"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col3:
        metric_html = create_metric_card(
            "Combined Revenue", 
            f"${total_revenue/1e9:.1f}B",
            "Annual industry value",
            "warning",
            "💰"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col4:
        metric_html = create_metric_card(
            "Avg Studio Size", 
            f"{avg_studio_size:.0f}",
            "Employees per studio",
            "info",
            "📊"
        )
        st.markdown(metric_html, unsafe_allow_html=True)

elif selected_section == "🗺️ World Map":
    st.markdown(create_ubisoft_section_header("🗺️ Interactive World Map"), unsafe_allow_html=True)
    
    fig_world = px.scatter_geo(
        studios_data,
        lat='latitude',
        lon='longitude',
        size='employees',
        color='region',
        hover_name='studio_name',
        hover_data={
            'city': True,
            'employees': True,
            'annual_revenue_usd': ':,.0f',
            'glassdoor_rating': ':.1f'
        },
        title='🌍 Global Gaming Studios Distribution',
        projection='natural earth',
        size_max=30
    )
    
    fig_world.update_layout(
        geo=dict(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
            projection_type='natural earth'
        ),
        height=600,
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_world, width='stretch')

elif selected_section == "📊 Regional Analysis":
    st.markdown(create_ubisoft_section_header("📊 Regional Market Analysis"), unsafe_allow_html=True)
    
    # Analyse par région
    regional_summary = studios_data.groupby('region').agg({
        'employees': ['sum', 'mean'],
        'studio_name': 'count',
        'annual_revenue_usd': 'sum',
        'glassdoor_rating': 'mean',
        'diversity_index': 'mean',
        'remote_workforce_pct': 'mean'
    }).round(2)
    
    regional_summary.columns = [
        'total_workforce', 'avg_studio_size', 'studio_count', 
        'total_revenue', 'avg_rating', 'avg_diversity', 'avg_remote_pct'
    ]
    
    regional_summary = regional_summary.reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_workforce = px.pie(
            regional_summary,
            values='total_workforce',
            names='region',
            title='👥 Workforce Distribution by Region',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig_workforce.update_layout(**get_ubisoft_chart_config()['layout'])
        st.plotly_chart(fig_workforce, width='stretch')
    
    with col2:
        fig_revenue = px.scatter(
            regional_summary,
            x='total_workforce',
            y='total_revenue',
            size='studio_count',
            color='region',
            hover_name='region',
            title='💰 Revenue vs Workforce by Region',
            labels={
                'total_workforce': 'Total Workforce',
                'total_revenue': 'Total Revenue (USD)'
            }
        )
        
        fig_revenue.update_layout(**get_ubisoft_chart_config()['layout'])
        st.plotly_chart(fig_revenue, width='stretch')

elif selected_section == "🏙️ City Competition":
    st.markdown(create_ubisoft_section_header("🏙️ City-Level Competition Analysis"), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_workforce_cities = city_competition.nlargest(10, 'total_workforce')
        
        fig_workforce_cities = px.bar(
            top_workforce_cities,
            x='total_workforce',
            y='city',
            orientation='h',
            color='region',
            title='👥 Top Cities by Total Workforce',
            labels={'total_workforce': 'Total Gaming Workforce'}
        )
        
        fig_workforce_cities.update_layout(height=400, **get_ubisoft_chart_config()['layout'])
        st.plotly_chart(fig_workforce_cities, width='stretch')
    
    with col2:
        fig_density_quality = px.scatter(
            city_competition,
            x='studio_count',
            y='avg_rating',
            size='total_workforce',
            color='region',
            hover_name='city',
            title='⭐ Studio Density vs Quality',
            labels={
                'studio_count': 'Number of Studios',
                'avg_rating': 'Average Glassdoor Rating'
            }
        )
        
        fig_density_quality.update_layout(height=400, **get_ubisoft_chart_config()['layout'])
        st.plotly_chart(fig_density_quality, width='stretch')

# Ajouter les autres sections...
elif selected_section == "🔄 Talent Migration":
    st.markdown(create_ubisoft_section_header("🔄 Global Talent Migration Patterns"), unsafe_allow_html=True)
    
    migration_flows = talent_migration.groupby(['origin_country', 'destination_country'])['talent_count'].sum().reset_index()
    migration_flows = migration_flows[migration_flows['origin_country'] != migration_flows['destination_country']]
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_flows = migration_flows.nlargest(10, 'talent_count')
        top_flows['corridor'] = top_flows['origin_country'] + ' → ' + top_flows['destination_country']
        
        fig_flows = px.bar(
            top_flows,
            x='talent_count',
            y='corridor',
            orientation='h',
            title='🌉 Top Talent Migration Corridors',
            labels={'talent_count': 'Number of Talents'},
            color='talent_count',
            color_continuous_scale='Blues'
        )
        
        fig_flows.update_layout(height=400, **get_ubisoft_chart_config()['layout'])
        st.plotly_chart(fig_flows, width='stretch')
    
    with col2:
        skill_migration = talent_migration.groupby('skill_type')['talent_count'].sum().reset_index()
        
        fig_skills = px.pie(
            skill_migration,
            values='talent_count',
            names='skill_type',
            title='🎪 Talent Migration by Skill Type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig_skills.update_layout(height=400, **get_ubisoft_chart_config()['layout'])
        st.plotly_chart(fig_skills, width='stretch')

# FOOTER PROFESSIONNEL
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 5px; margin-top: 2rem;'>
    <p style='color: #666; margin: 0; font-size: 0.9rem;'>
        © 2024 Ubisoft Entertainment - Gaming Workforce Observatory<br>
        Global Studios Dashboard • Covering {studios_data['country'].nunique()} Countries • 
        Data Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} • Confidential and Proprietary
    </p>
</div>
""", unsafe_allow_html=True)

