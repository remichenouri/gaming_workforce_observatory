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
import geopandas as gpd
import folium
from folium import plugins
import streamlit_folium as st_folium
from shapely.geometry import Point

# Ajoutez ces imports au début de votre fichier

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
    
    # Info box explicatif
    st.markdown(create_ubisoft_info_box(
        "🌍 Global Gaming Studios Mapping",
        "Cartographie interactive des studios gaming mondiaux avec visualisation en temps réel de la distribution géographique, densité de workforce et patterns régionaux."
    ), unsafe_allow_html=True)
    
    # Sélecteur de moteur cartographique
    col1, col2 = st.columns([3, 1])
    
    with col1:
        map_engine = st.selectbox(
            "🗺️ Moteur cartographique",
            ["Folium Interactive", "Plotly Geographic", "Simple Fallback"],
            index=0,
            help="Choisissez le moteur de rendu de carte"
        )
    
    with col2:
        data_limit = st.selectbox(
            "📊 Nombre de studios",
            [30, 50, 100, "Tous"],
            index=1
        )
    
    # Préparation des données
    display_data = studios_data.head(int(data_limit)) if data_limit != "Tous" else studios_data
    
    # === FOLIUM INTERACTIVE (Option 1) ===
    if map_engine == "Folium Interactive":
        try:
            import folium
            import streamlit_folium as st_folium
            from folium.plugins import MarkerCluster, HeatMap
            
            st.info("🗺️ Chargement de la carte Folium interactive...")
            
            # Centre intelligent
            center_lat = display_data['latitude'].median()
            center_lon = display_data['longitude'].median()
            
            # Création carte
            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=3,
                tiles='CartoDB positron'
            )
            
            # Ajout des markers avec clustering
            marker_cluster = MarkerCluster().add_to(m)
            
            for idx, row in display_data.iterrows():
                # Couleur par région
                region_colors = {
                    'North America': '#0099FF',
                    'Europe': '#28A745', 
                    'Asia-Pacific': '#FFB020',
                    'Latin America': '#E60012'
                }
                color = region_colors.get(row.get('region', ''), '#666666')
                
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=max(8, min(20, row['employees'] / 50)),
                    popup=f"""
                    <b>{row['studio_name']}</b><br>
                    📍 {row['city']}<br>
                    👥 {row['employees']:,} employés<br>
                    💰 ${row.get('annual_revenue_usd', 0):,.0f}<br>
                    ⭐ {row.get('glassdoor_rating', 0):.1f}/5.0
                    """,
                    color='white',
                    weight=2,
                    fillColor=color,
                    fillOpacity=0.8
                ).add_to(marker_cluster)
            
            # Affichage
            map_data = st_folium.st_folium(
                m, 
                width=1200, 
                height=600,
                returned_data=["last_clicked"],
                key="folium_map"
            )
            
            if map_data and map_data.get('last_clicked'):
                st.success(f"🎯 Coordonnées cliquées: {map_data['last_clicked']}")
            
        except ImportError:
            st.error("❌ Folium non disponible - Basculement vers Plotly")
            map_engine = "Plotly Geographic"
        except Exception as e:
            st.error(f"❌ Erreur Folium: {str(e)} - Basculement vers Plotly")
            map_engine = "Plotly Geographic"
    
    # === PLOTLY GEOGRAPHIC (Option 2) ===
    if map_engine == "Plotly Geographic":
        st.info("🌍 Génération de la carte Plotly...")
        
        fig_world = px.scatter_geo(
            display_data,
            lat='latitude',
            lon='longitude',
            size='employees',
            color='region',
            hover_name='studio_name',
            hover_data={
                'city': True,
                'employees': ':,',
                'annual_revenue_usd': ':,.0f',
                'glassdoor_rating': ':.1f'
            },
            title='🌍 Global Gaming Studios Distribution',
            projection='natural earth',
            size_max=25,
            color_discrete_map={
                'North America': '#0099FF',
                'Europe': '#28A745',
                'Asia-Pacific': '#FFB020', 
                'Latin America': '#E60012'
            }
        )
        
        fig_world.update_layout(
            height=600,
            geo=dict(
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showocean=True,
                oceancolor='rgb(230, 245, 255)',
                projection_type='natural earth'
            ),
            **get_ubisoft_chart_config()['layout']
        )
        
        st.plotly_chart(fig_world, use_container_width=True)
    
    # === SIMPLE FALLBACK (Option 3) ===
    if map_engine == "Simple Fallback":
        st.info("🗺️ Carte simple avec coordonnées...")
        
        # Affichage simple en tableau avec coordonnées
        map_data = display_data[['studio_name', 'city', 'country', 'latitude', 'longitude', 'employees']].head(20)
        
        st.dataframe(
            map_data,
            use_container_width=True,
            height=400
        )
        
        # Mini visualisation avec matplotlib si disponible
        try:
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(12, 6))
            scatter = ax.scatter(
                display_data['longitude'], 
                display_data['latitude'],
                s=display_data['employees']/10,
                alpha=0.6,
                c=display_data['region'].astype('category').cat.codes,
                cmap='viridis'
            )
            
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude') 
            ax.set_title('Gaming Studios - Global Distribution')
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
        except ImportError:
            st.warning("Matplotlib non disponible pour la visualisation simple")
    
    # === STATISTIQUES COMMUNES ===
    st.markdown("---")
    st.markdown("### 📊 Analytics Géographiques")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_html = create_metric_card(
            "Studios Affichés", 
            f"{len(display_data):,}",
            f"Total disponible: {len(studios_data)}",
            "info",
            "🏢"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col2:
        metric_html = create_metric_card(
            "Villes", 
            f"{display_data['city'].nunique()}",
            "Hubs gaming globaux",
            "success",
            "🏙️"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col3:
        metric_html = create_metric_card(
            "Pays", 
            f"{display_data['country'].nunique()}", 
            "Marchés représentés",
            "warning",
            "🌍"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col4:
        avg_employees = display_data['employees'].mean()
        metric_html = create_metric_card(
            "Taille Moyenne", 
            f"{avg_employees:.0f}",
            "Employés par studio", 
            "info",
            "👥"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    # Top villes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏆 Top 5 Villes par Workforce**")
        top_cities = display_data.groupby('city')['employees'].sum().nlargest(5)
        for i, (city, employees) in enumerate(top_cities.items(), 1):
            st.write(f"{i}. **{city}**: {employees:,} employés")
    
    with col2:
        st.markdown("**🌎 Distribution Régionale**")
        regional_dist = display_data.groupby('region')['employees'].sum()
        total = regional_dist.sum()
        for region, employees in regional_dist.items():
            pct = (employees / total) * 100
            st.write(f"• **{region}**: {pct:.1f}% ({employees:,})")


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

