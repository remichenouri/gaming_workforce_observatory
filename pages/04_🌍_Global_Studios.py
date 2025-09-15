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

apply_ubisoft_theme()

# Ajout du chemin pour imports
sys.path.append(str(Path(__file__).parent.parent))

from src.visualizations.geographic_maps import GamingGeographicMaps

def initialize_global_studios_dashboard():
    """Initialise le dashboard studios mondiaux"""
    st.set_page_config(
        page_title="🌍 Gaming Workforce Observatory - Global Studios",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Application du thème gaming
    themes = GamingThemes()
    themes.apply_gaming_theme()

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

def render_global_overview(studios_data, regional_costs):
    """Vue d'ensemble mondiale"""
    
    themes = GamingThemes()
    
    # Header Global Studios
    st.markdown("""
    <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;'>
        <h1 style='color: white; font-family: "Orbitron", monospace; font-size: 3rem; margin: 0;'>🌍 GLOBAL STUDIOS</h1>
        <h2 style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'>Worldwide Gaming Workforce Intelligence</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 0;'>Strategic insights into global gaming talent distribution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métriques globales
    st.markdown("### 🌏 Global Gaming Ecosystem")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_studios = len(studios_data)
    total_workforce = studios_data['employees'].sum()
    total_revenue = studios_data['annual_revenue_usd'].sum()
    avg_studio_size = studios_data['employees'].mean()
    
    with col1:
        metric_html = themes.create_metric_card(
            "Total Studios", 
            f"{total_studios:,}",
            "Across 18 cities",
            "info",
            "🏢"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col2:
        metric_html = themes.create_metric_card(
            "Global Workforce", 
            f"{total_workforce:,}",
            "Gaming professionals",
            "success",
            "👥"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col3:
        metric_html = themes.create_metric_card(
            "Combined Revenue", 
            f"${total_revenue/1e9:.1f}B",
            "Annual industry value",
            "warning",
            "💰"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col4:
        metric_html = themes.create_metric_card(
            "Avg Studio Size", 
            f"{avg_studio_size:.0f}",
            "Employees per studio",
            "info",
            "📊"
        )
        st.markdown(metric_html, unsafe_allow_html=True)

def render_world_map(studios_data):
    """Carte mondiale interactive"""
    
    st.markdown("### 🗺️ Interactive World Map")
    
    # Utilisation du module geographic_maps
    geo_maps = GamingGeographicMaps()
    
    # Préparation des données pour la carte
    map_data = studios_data.copy()
    
    # Carte principale
    fig_world = px.scatter_geo(
        map_data,
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
        height=600
    )
    
    st.plotly_chart(fig_world, width='stretch')

def render_regional_analysis(studios_data, regional_costs):
    """Analyse régionale détaillée"""
    
    st.markdown("### 📊 Regional Market Analysis")
    
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
        # Workforce distribution par région
        fig_workforce = px.pie(
            regional_summary,
            values='total_workforce',
            names='region',
            title='👥 Workforce Distribution by Region',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig_workforce, width='stretch')
    
    with col2:
        # Revenue vs Workforce correlation
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
        
        st.plotly_chart(fig_revenue, width='stretch')
    
    # Tableau comparatif régional
    st.markdown("#### 🌏 Regional Comparison Matrix")
    
    # Merge avec les coûts régionaux
    regional_analysis = regional_summary.merge(regional_costs, on='region', how='left')
    
    # Calcul du ROI par région (simplifié)
    regional_analysis['workforce_roi'] = (
        regional_analysis['total_revenue'] / 
        (regional_analysis['total_workforce'] * regional_analysis['avg_salary_usd'])
    ).round(2)
    
    # Formatage pour affichage
    display_regional = regional_analysis.copy()
    display_regional['total_revenue'] = display_regional['total_revenue'].apply(lambda x: f"${x/1e9:.1f}B")
    display_regional['avg_salary_usd'] = display_regional['avg_salary_usd'].apply(lambda x: f"${x:,}")
    display_regional['office_rent_sqft_year'] = display_regional['office_rent_sqft_year'].apply(lambda x: f"${x}")
    
    columns_display = [
        'region', 'studio_count', 'total_workforce', 'total_revenue', 
        'avg_salary_usd', 'talent_availability', 'workforce_roi'
    ]
    
    st.dataframe(
        display_regional[columns_display].rename(columns={
            'region': 'Region',
            'studio_count': 'Studios',
            'total_workforce': 'Workforce',
            'total_revenue': 'Revenue',
            'avg_salary_usd': 'Avg Salary',
            'talent_availability': 'Talent Pool',
            'workforce_roi': 'ROI'
        }),
        width='stretch'
    )

def render_city_competition(city_competition):
    """Analyse de la concurrence par ville"""
    
    st.markdown("### 🏙️ City-Level Competition Analysis")
    
    # Top villes par différents critères
    col1, col2 = st.columns(2)
    
    with col1:
        # Top villes par workforce
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
        
        fig_workforce_cities.update_layout(height=400)
        st.plotly_chart(fig_workforce_cities, width='stretch')
    
    with col2:
        # Studio density vs quality
        fig_density_quality = px.scatter(
            city_competition,
            x='studio_count',
            y='avg_rating',
            size='total_workforce',
            color='region',
            hover_name='city',
            title='⭐ Studio Density vs Quality (Glassdoor Rating)',
            labels={
                'studio_count': 'Number of Studios',
                'avg_rating': 'Average Glassdoor Rating'
            }
        )
        
        fig_density_quality.update_layout(height=400)
        st.plotly_chart(fig_density_quality, width='stretch')
    
    # Gaming hubs analysis
    st.markdown("#### 🎮 Gaming Hubs Deep Dive")
    
    # Création d'un score composite pour les "gaming hubs"
    city_competition['hub_score'] = (
        (city_competition['total_workforce'] / city_competition['total_workforce'].max()) * 0.4 +
        (city_competition['studio_count'] / city_competition['studio_count'].max()) * 0.3 +
        (city_competition['avg_rating'] / city_competition['avg_rating'].max()) * 0.2 +
        (city_competition['avg_diversity'] / city_competition['avg_diversity'].max()) * 0.1
    ) * 100
    
    top_hubs = city_competition.nlargest(8, 'hub_score')
    
    # Affichage des top gaming hubs
    cols = st.columns(4)
    
    for i, (_, hub) in enumerate(top_hubs.iterrows()):
        col_idx = i % 4
        
        with cols[col_idx]:
            hub_card = f"""
            <div style='background: linear-gradient(135deg, #3498db, #2980b9); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;'>
                <h4 style='margin: 0; color: white;'>🏙️ {hub['city']}</h4>
                <p style='margin: 0.5rem 0; font-size: 0.9rem;'>
                    {hub['region']}<br>
                    Studios: {hub['studio_count']}<br>
                    Workforce: {hub['total_workforce']:,}<br>
                    Hub Score: {hub['hub_score']:.1f}/100
                </p>
            </div>
            """
            st.markdown(hub_card, unsafe_allow_html=True)

def render_talent_migration(talent_migration):
    """Analyse de la migration des talents"""
    
    st.markdown("### 🔄 Global Talent Migration Patterns")
    
    # Migration flows
    migration_flows = talent_migration.groupby(['origin_country', 'destination_country'])['talent_count'].sum().reset_index()
    migration_flows = migration_flows[migration_flows['origin_country'] != migration_flows['destination_country']]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top migration corridors
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
        
        fig_flows.update_layout(height=400)
        st.plotly_chart(fig_flows, width='stretch')
    
    with col2:
        # Migration by skill type
        skill_migration = talent_migration.groupby('skill_type')['talent_count'].sum().reset_index()
        
        fig_skills = px.pie(
            skill_migration,
            values='talent_count',
            names='skill_type',
            title='🎪 Talent Migration by Skill Type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig_skills.update_layout(height=400)
        st.plotly_chart(fig_skills, width='stretch')
    
    # Net migration analysis
    st.markdown("#### 📈 Net Migration Analysis")
    
    # Calculer la migration nette par pays
    outbound = talent_migration.groupby('origin_country')['talent_count'].sum()
    inbound = talent_migration.groupby('destination_country')['talent_count'].sum()
    
    net_migration = pd.DataFrame({
        'country': list(set(outbound.index) | set(inbound.index)),
    })
    
    net_migration['outbound'] = net_migration['country'].map(outbound).fillna(0)
    net_migration['inbound'] = net_migration['country'].map(inbound).fillna(0)
    net_migration['net_migration'] = net_migration['inbound'] - net_migration['outbound']
    net_migration = net_migration.sort_values('net_migration', ascending=False)
    
    # Graphique net migration
    fig_net = px.bar(
        net_migration,
        x='country',
        y='net_migration',
        title='📊 Net Talent Migration by Country',
        color='net_migration',
        color_continuous_scale='RdBu',
        color_continuous_midpoint=0
    )
    
    fig_net.add_hline(y=0, line_dash="dash", line_color="black")
    fig_net.update_xaxes(tickangle=45)
    fig_net.update_layout(height=400)
    
    st.plotly_chart(fig_net, width='stretch')

def render_cost_optimization(regional_costs, studios_data):
    """Analyse d'optimisation des coûts"""
    
    st.markdown("### 💡 Cost Optimization & Strategic Positioning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost vs Talent matrix
        fig_cost_talent = px.scatter(
            regional_costs,
            x='avg_salary_usd',
            y='talent_availability',
            size='cost_of_living_index',
            color='region',
            hover_name='region',
            title='💰 Cost vs Talent Availability Matrix',
            labels={
                'avg_salary_usd': 'Average Salary (USD)',
                'talent_availability': 'Talent Availability Score'
            }
        )
        
        # Quadrants d'optimisation
        fig_cost_talent.add_hline(y=80, line_dash="dash", line_color="gray", annotation_text="High Talent Threshold")
        fig_cost_talent.add_vline(x=70000, line_dash="dash", line_color="gray", annotation_text="Mid-Range Cost")
        
        fig_cost_talent.update_layout(height=400)
        st.plotly_chart(fig_cost_talent, width='stretch')
    
    with col2:
        # ROI analysis
        regional_costs['salary_efficiency'] = regional_costs['talent_availability'] / (regional_costs['avg_salary_usd'] / 1000)
        
        fig_efficiency = px.bar(
            regional_costs,
            x='region',
            y='salary_efficiency',
            title='⚡ Salary Efficiency Score by Region',
            color='salary_efficiency',
            color_continuous_scale='Greens'
        )
        
        fig_efficiency.update_layout(height=400)
        st.plotly_chart(fig_efficiency, width='stretch')
    
    # Recommandations stratégiques
    st.markdown("#### 🎯 Strategic Recommendations by Region")
    
    recommendations = {
        'North America': {
            'strategy': 'Premium Talent Hub',
            'focus': 'High-value projects, senior talent, innovation centers',
            'considerations': 'Highest costs but best talent pool and market access'
        },
        'Europe': {
            'strategy': 'Balanced Excellence',
            'focus': 'Mix of senior and mid-level talent, strong regulatory compliance',
            'considerations': 'Good talent availability with moderate costs'
        },
        'Asia-Pacific': {
            'strategy': 'Scale & Efficiency',
            'focus': 'Large development teams, mobile gaming, rapid scaling',
            'considerations': 'Cost-effective with growing talent pool'
        },
        'Latin America': {
            'strategy': 'Emerging Market',
            'focus': 'Nearshore development, cost-sensitive projects',
            'considerations': 'Lowest costs but limited senior talent'
        }
    }
    
    for region, rec in recommendations.items():
        with st.expander(f"🌍 {region} - {rec['strategy']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Strategic Focus:** {rec['focus']}")
            
            with col2:
                st.markdown(f"**Key Considerations:** {rec['considerations']}")

def render_market_opportunities():
    """Opportunités de marché émergentes"""
    
    st.markdown("### 🚀 Emerging Market Opportunities")
    
    # Marchés émergents simulés
    emerging_markets = pd.DataFrame({
        'market': ['Eastern Europe', 'Southeast Asia', 'India', 'Africa', 'Middle East'],
        'growth_potential': [85, 92, 88, 75, 70],
        'talent_cost_advantage': [60, 70, 80, 85, 65],
        'market_maturity': [65, 58, 72, 35, 45],
        'infrastructure_score': [75, 68, 70, 55, 72],
        'risk_score': [35, 25, 20, 45, 40]  # Lower is better
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Growth potential vs cost advantage
        fig_opportunity = px.scatter(
            emerging_markets,
            x='talent_cost_advantage',
            y='growth_potential',
            size='infrastructure_score',
            color='risk_score',
            hover_name='market',
            title='🌟 Emerging Market Opportunity Matrix',
            labels={
                'talent_cost_advantage': 'Cost Advantage Score',
                'growth_potential': 'Growth Potential Score'
            },
            color_continuous_scale='RdYlGn_r'  # Red for high risk
        )
        
        fig_opportunity.update_layout(height=400)
        st.plotly_chart(fig_opportunity, width='stretch')
    
    with col2:
        # Market readiness radar
        categories = ['Growth Potential', 'Cost Advantage', 'Market Maturity', 'Infrastructure', 'Risk (Inverted)']
        
        fig_radar = go.Figure()
        
        for _, market in emerging_markets.iterrows():
            values = [
                market['growth_potential'],
                market['talent_cost_advantage'],
                market['market_maturity'],
                market['infrastructure_score'],
                100 - market['risk_score']  # Invert risk for radar
            ]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=market['market'],
                opacity=0.6
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title='📡 Market Readiness Comparison',
            height=400
        )
        
        st.plotly_chart(fig_radar, width='stretch')
    
    # Top opportunities
    st.markdown("#### 🏆 Top 3 Market Opportunities")
    
    # Calcul du score composite
    emerging_markets['opportunity_score'] = (
        emerging_markets['growth_potential'] * 0.3 +
        emerging_markets['talent_cost_advantage'] * 0.25 +
        emerging_markets['infrastructure_score'] * 0.2 +
        emerging_markets['market_maturity'] * 0.15 +
        (100 - emerging_markets['risk_score']) * 0.1
    )
    
    top_opportunities = emerging_markets.nlargest(3, 'opportunity_score')
    
    cols = st.columns(3)
    
    for i, (_, opportunity) in enumerate(top_opportunities.iterrows()):
        with cols[i]:
            rank = i + 1
            score = opportunity['opportunity_score']
            
            opportunity_card = f"""
            <div style='background: linear-gradient(135deg, #2ecc71, #27ae60); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;'>
                <h4 style='margin: 0; color: white;'>#{rank} {opportunity['market']}</h4>
                <p style='margin: 0.5rem 0; font-size: 0.9rem;'>
                    Opportunity Score: {score:.1f}/100<br>
                    Growth Potential: {opportunity['growth_potential']}<br>
                    Cost Advantage: {opportunity['talent_cost_advantage']}<br>
                    Risk Level: {opportunity['risk_score']}/100
                </p>
            </div>
            """
            st.markdown(opportunity_card, unsafe_allow_html=True)

def main():
    """Fonction principale Global Studios"""
    
    initialize_global_studios_dashboard()
    
    # Génération des données
    studios_data, talent_migration, regional_costs, city_competition = generate_global_studios_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🌍 Global Intelligence")
        
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
        
        st.markdown("---")
        st.markdown("### 📈 Global Metrics")
        
        total_countries = studios_data['country'].nunique()
        total_cities = studios_data['city'].nunique()
        total_workforce = studios_data['employees'].sum()
        
        st.metric("Countries", total_countries)
        st.metric("Cities", total_cities)
        st.metric("Global Workforce", f"{total_workforce:,}")
        
        # Distribution par région
        st.markdown("---")
        st.markdown("### 🌍 Regional Split")
        
        regional_split = studios_data.groupby('region')['employees'].sum()
        for region, workforce in regional_split.items():
            percentage = (workforce / total_workforce) * 100
            st.markdown(f"**{region}:** {percentage:.1f}%")
        
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📊 Export Global Report"):
            st.success("Global analysis report generated!")
        
        if st.button("🎯 Market Entry Analysis"):
            st.success("Market entry assessment initiated!")
        
        if st.button("📧 Share with Leadership"):
            st.success("Global insights shared!")
    
    # Contenu principal
    if selected_section == "🌏 Global Overview":
        render_global_overview(studios_data, regional_costs)
    elif selected_section == "🗺️ World Map":
        render_world_map(studios_data)
    elif selected_section == "📊 Regional Analysis":
        render_regional_analysis(studios_data, regional_costs)
    elif selected_section == "🏙️ City Competition":
        render_city_competition(city_competition)
    elif selected_section == "🔄 Talent Migration":
        render_talent_migration(talent_migration)
    elif selected_section == "💡 Cost Optimization":
        render_cost_optimization(regional_costs, studios_data)
    elif selected_section == "🚀 Market Opportunities":
        render_market_opportunities()
    
    # Footer global
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #3498db; font-weight: bold;'>"
        "🌍 GLOBAL GAMING WORKFORCE INTELLIGENCE | "
        f"Covering {studios_data['country'].nunique()} Countries | "
        f"Data Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
