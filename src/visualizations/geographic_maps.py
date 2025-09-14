"""
Gaming Workforce Observatory - Geographic Maps Enterprise
Cartes interactives des studios gaming mondiaux avec données géospatiales
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st
import geopandas as gpd
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class GamingGeographicMaps:
    """Cartes géographiques avancées pour studios gaming mondiaux"""
    
    def __init__(self):
        # Coordonnées des principaux hubs gaming mondiaux
        self.gaming_hubs = {
            'North America': {
                'San Francisco': {'lat': 37.7749, 'lon': -122.4194, 'tier': 'Tier 1'},
                'Los Angeles': {'lat': 34.0522, 'lon': -118.2437, 'tier': 'Tier 1'},
                'Seattle': {'lat': 47.6062, 'lon': -122.3321, 'tier': 'Tier 1'},
                'Montreal': {'lat': 45.5017, 'lon': -73.5673, 'tier': 'Tier 1'},
                'Austin': {'lat': 30.2672, 'lon': -97.7431, 'tier': 'Tier 2'},
                'Boston': {'lat': 42.3601, 'lon': -71.0589, 'tier': 'Tier 2'}
            },
            'Europe': {
                'London': {'lat': 51.5074, 'lon': -0.1278, 'tier': 'Tier 1'},
                'Paris': {'lat': 48.8566, 'lon': 2.3522, 'tier': 'Tier 1'},
                'Berlin': {'lat': 52.5200, 'lon': 13.4050, 'tier': 'Tier 1'},
                'Stockholm': {'lat': 59.3293, 'lon': 18.0686, 'tier': 'Tier 1'},
                'Amsterdam': {'lat': 52.3676, 'lon': 4.9041, 'tier': 'Tier 2'},
                'Barcelona': {'lat': 41.3851, 'lon': 2.1734, 'tier': 'Tier 2'},
                'Warsaw': {'lat': 52.2297, 'lon': 21.0122, 'tier': 'Tier 2'}
            },
            'Asia-Pacific': {
                'Tokyo': {'lat': 35.6762, 'lon': 139.6503, 'tier': 'Tier 1'},
                'Seoul': {'lat': 37.5665, 'lon': 126.9780, 'tier': 'Tier 1'},
                'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'tier': 'Tier 1'},
                'Shanghai': {'lat': 31.2304, 'lon': 121.4737, 'tier': 'Tier 1'},
                'Sydney': {'lat': -33.8688, 'lon': 151.2093, 'tier': 'Tier 2'},
                'Bangalore': {'lat': 12.9716, 'lon': 77.5946, 'tier': 'Tier 2'}
            }
        }
        
        # Couleurs par région
        self.region_colors = {
            'North America': '#3498db',
            'Europe': '#e74c3c', 
            'Asia-Pacific': '#2ecc71',
            'Latin America': '#f39c12',
            'Africa': '#9b59b6'
        }
        
        # Tailles par tier
        self.tier_sizes = {
            'Tier 1': 25,
            'Tier 2': 15,
            'Tier 3': 10
        }
    
    def create_global_studios_map(self, studios_data: pd.DataFrame) -> go.Figure:
        """Carte mondiale des studios gaming avec données interactives"""
        
        if studios_data.empty:
            return self._create_empty_world_map()
        
        # Préparation des données géographiques
        studios_geo = self._prepare_geographic_data(studios_data)
        
        # Création de la carte base
        fig = go.Figure()
        
        # Ajout des studios par région
        for region, color in self.region_colors.items():
            region_data = studios_geo[studios_geo['region'] == region]
            
            if not region_data.empty:
                fig.add_trace(go.Scattergeo(
                    lon=region_data['longitude'],
                    lat=region_data['latitude'],
                    text=region_data['hover_text'],
                    mode='markers',
                    marker=dict(
                        size=region_data['marker_size'],
                        color=color,
                        opacity=0.8,
                        sizemode='area',
                        sizeref=2.*max(region_data['marker_size'])/(40.**2),
                        sizemin=4,
                        line=dict(width=1, color='white')
                    ),
                    name=region,
                    hovertemplate='<b>%{text}</b><extra></extra>'
                ))
        
        # Configuration de la carte
        fig.update_layout(
            title={
                'text': '🌍 Global Gaming Studios Distribution',
                'x': 0.5,
                'font': {'size': 20}
            },
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showlakes=True,
                lakecolor='rgb(255, 255, 255)',
                showocean=True,
                oceancolor='rgb(230, 245, 255)',
                showcountries=True,
                countrycolor='rgb(204, 204, 204)',
                bgcolor='rgba(0,0,0,0)'
            ),
            height=600,
            showlegend=True,
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='rgba(0, 0, 0, 0.2)',
                borderwidth=1
            )
        )
        
        return fig
    
    def _prepare_geographic_data(self, studios_data: pd.DataFrame) -> pd.DataFrame:
        """Prépare les données géographiques des studios"""
        
        studios_geo = studios_data.copy()
        
        # Ajout de coordonnées si manquantes
        if 'latitude' not in studios_geo.columns or 'longitude' not in studios_geo.columns:
            studios_geo = self._add_coordinates(studios_geo)
        
        # Calcul de la taille des marqueurs
        if 'employees' in studios_geo.columns:
            studios_geo['marker_size'] = studios_geo['employees'].apply(
                lambda x: min(50, max(8, np.sqrt(x) * 2))
            )
        else:
            studios_geo['marker_size'] = 15
        
        # Création du texte hover
        studios_geo['hover_text'] = studios_geo.apply(
            lambda row: self._create_hover_text(row), axis=1
        )
        
        return studios_geo
    
    def _add_coordinates(self, studios_data: pd.DataFrame) -> pd.DataFrame:
        """Ajoute les coordonnées géographiques basées sur la ville/pays"""
        
        studios_with_coords = studios_data.copy()
        
        # Initialisation des colonnes
        studios_with_coords['latitude'] = np.nan
        studios_with_coords['longitude'] = np.nan
        
        # Mapping des coordonnées depuis les hubs connus
        for _, row in studios_with_coords.iterrows():
            city = row.get('city', '')
            country = row.get('country', '')
            location = row.get('location', '')
            
            # Recherche dans les hubs gaming
            coords = self._find_coordinates(city, country, location)
            
            if coords:
                studios_with_coords.loc[_, 'latitude'] = coords['lat']
                studios_with_coords.loc[_, 'longitude'] = coords['lon']
        
        return studios_with_coords.dropna(subset=['latitude', 'longitude'])
    
    def _find_coordinates(self, city: str, country: str, location: str) -> Optional[Dict[str, float]]:
        """Trouve les coordonnées d'une ville dans les hubs gaming"""
        
        search_terms = [city, country, location]
        
        for region_hubs in self.gaming_hubs.values():
            for hub_name, coords in region_hubs.items():
                for term in search_terms:
                    if term and hub_name.lower() in term.lower():
                        return coords
        
        # Coordonnées par défaut pour pays connus
        country_defaults = {
            'United States': {'lat': 39.8283, 'lon': -98.5795},
            'Canada': {'lat': 56.1304, 'lon': -106.3468},
            'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
            'France': {'lat': 46.2276, 'lon': 2.2137},
            'Germany': {'lat': 51.1657, 'lon': 10.4515},
            'Japan': {'lat': 36.2048, 'lon': 138.2529},
            'South Korea': {'lat': 35.9078, 'lon': 127.7669},
            'China': {'lat': 35.8617, 'lon': 104.1954}
        }
        
        return country_defaults.get(country)
    
    def _create_hover_text(self, studio_row: pd.Series) -> str:
        """Crée le texte d'information hover pour un studio"""
        
        name = studio_row.get('studio_name', studio_row.get('name', 'Unknown Studio'))
        city = studio_row.get('city', studio_row.get('location', 'Unknown'))
        employees = studio_row.get('employees', 'N/A')
        revenue = studio_row.get('revenue_usd', 0)
        
        hover_text = f"{name}<br>{city}"
        
        if employees != 'N/A':
            hover_text += f"<br>👥 {employees:,} employees"
        
        if revenue > 0:
            hover_text += f"<br>💰 ${revenue:,.0f} revenue"
        
        return hover_text
    
    def create_regional_heatmap(self, studios_data: pd.DataFrame) -> go.Figure:
        """Heatmap des concentrations de studios par région"""
        
        if studios_data.empty:
            return go.Figure()
        
        # Agrégation par région et pays
        regional_data = studios_data.groupby(['region', 'country']).agg({
            'employees': 'sum',
            'studio_name': 'count'
        }).reset_index()
        
        regional_data.columns = ['region', 'country', 'total_employees', 'studio_count']
        
        # Création de la heatmap
        fig = go.Figure(data=go.Choropleth(
            locations=regional_data['country'],
            z=regional_data['total_employees'],
            locationmode='country names',
            colorscale='Viridis',
            text=regional_data['country'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Studios: %{customdata[0]}<br>' +
                         'Total Employees: %{z:,}<br>' +
                         '<extra></extra>',
            customdata=regional_data[['studio_count']].values,
            colorbar=dict(
                title="Total Employees",
                titleside="right"
            )
        ))
        
        fig.update_layout(
            title={
                'text': '🔥 Gaming Workforce Concentration by Country',
                'x': 0.5,
                'font': {'size': 18}
            },
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            height=500
        )
        
        return fig
    
    def create_talent_migration_flow(self, migration_data: pd.DataFrame) -> go.Figure:
        """Carte des flux de migration des talents gaming"""
        
        if migration_data.empty or 'origin_country' not in migration_data.columns:
            return go.Figure()
        
        # Préparation des données de flux
        flow_data = migration_data.groupby(['origin_country', 'destination_country']).agg({
            'talent_count': 'sum'
        }).reset_index()
        
        # Ajout des coordonnées pour origine et destination
        flow_with_coords = self._add_flow_coordinates(flow_data)
        
        fig = go.Figure()
        
        # Ajout des lignes de flux
        for _, flow in flow_with_coords.iterrows():
            if pd.notna(flow['origin_lat']) and pd.notna(flow['dest_lat']):
                
                # Calcul de l'épaisseur de ligne
                line_width = min(10, max(1, flow['talent_count'] / 10))
                
                fig.add_trace(go.Scattergeo(
                    lon=[flow['origin_lon'], flow['dest_lon']],
                    lat=[flow['origin_lat'], flow['dest_lat']],
                    mode='lines',
                    line=dict(
                        width=line_width,
                        color=f'rgba(255, 107, 53, {min(1, flow["talent_count"]/100)})'
                    ),
                    hovertemplate=f'<b>{flow["origin_country"]} → {flow["destination_country"]}</b><br>' +
                                 f'Talent Flow: {flow["talent_count"]} people<br>' +
                                 '<extra></extra>',
                    showlegend=False
                ))
        
        fig.update_layout(
            title={
                'text': '🌐 Global Gaming Talent Migration Flow',
                'x': 0.5,
                'font': {'size': 18}
            },
            geo=dict(
                projection_type='orthographic',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                oceancolor='rgb(230, 245, 255)',
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            ),
            height=600
        )
        
        return fig
    
    def _add_flow_coordinates(self, flow_data: pd.DataFrame) -> pd.DataFrame:
        """Ajoute les coordonnées pour les flux de migration"""
        
        # Coordonnées centrales des pays principaux
        country_coords = {
            'United States': {'lat': 39.8283, 'lon': -98.5795},
            'Canada': {'lat': 56.1304, 'lon': -106.3468},
            'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
            'France': {'lat': 46.2276, 'lon': 2.2137},
            'Germany': {'lat': 51.1657, 'lon': 10.4515},
            'Sweden': {'lat': 60.1282, 'lon': 18.6435},
            'Japan': {'lat': 36.2048, 'lon': 138.2529},
            'South Korea': {'lat': 35.9078, 'lon': 127.7669},
            'China': {'lat': 35.8617, 'lon': 104.1954},
            'Australia': {'lat': -25.2744, 'lon': 133.7751}
        }
        
        flow_with_coords = flow_data.copy()
        
        # Ajout coordonnées origine
        flow_with_coords['origin_lat'] = flow_with_coords['origin_country'].map(
            lambda x: country_coords.get(x, {}).get('lat')
        )
        flow_with_coords['origin_lon'] = flow_with_coords['origin_country'].map(
            lambda x: country_coords.get(x, {}).get('lon')
        )
        
        # Ajout coordonnées destination
        flow_with_coords['dest_lat'] = flow_with_coords['destination_country'].map(
            lambda x: country_coords.get(x, {}).get('lat')
        )
        flow_with_coords['dest_lon'] = flow_with_coords['destination_country'].map(
            lambda x: country_coords.get(x, {}).get('lon')
        )
        
        return flow_with_coords
    
    def create_salary_geographic_distribution(self, salary_data: pd.DataFrame) -> go.Figure:
        """Distribution géographique des salaires gaming"""
        
        if salary_data.empty:
            return go.Figure()
        
        # Agrégation des salaires par location
        location_salaries = salary_data.groupby(['country', 'city']).agg({
            'salary_usd': ['mean', 'count', 'std']
        }).reset_index()
        
        location_salaries.columns = ['country', 'city', 'avg_salary', 'employee_count', 'salary_std']
        
        # Ajout des coordonnées
        salary_geo = self._add_coordinates(location_salaries)
        
        # Classification des niveaux de salaire
        salary_geo['salary_tier'] = pd.cut(
            salary_geo['avg_salary'],
            bins=[0, 60000, 90000, 120000, float('inf')],
            labels=['Low', 'Medium', 'High', 'Premium'],
            include_lowest=True
        )
        
        # Couleurs par tier de salaire
        tier_colors = {
            'Low': '#3498db',
            'Medium': '#f39c12',
            'High': '#e74c3c',
            'Premium': '#8e44ad'
        }
        
        fig = go.Figure()
        
        # Ajout des points par tier de salaire
        for tier in ['Low', 'Medium', 'High', 'Premium']:
            tier_data = salary_geo[salary_geo['salary_tier'] == tier]
            
            if not tier_data.empty:
                fig.add_trace(go.Scattergeo(
                    lon=tier_data['longitude'],
                    lat=tier_data['latitude'],
                    mode='markers',
                    marker=dict(
                        size=np.sqrt(tier_data['employee_count']) * 3,
                        color=tier_colors[tier],
                        opacity=0.7,
                        sizemode='area',
                        line=dict(width=1, color='white')
                    ),
                    name=f'{tier} Salary',
                    hovertemplate='<b>%{text}</b><br>' +
                                 'Avg Salary: $%{customdata[0]:,.0f}<br>' +
                                 'Employees: %{customdata[1]}<br>' +
                                 '<extra></extra>',
                    text=[f"{row['city']}, {row['country']}" for _, row in tier_data.iterrows()],
                    customdata=tier_data[['avg_salary', 'employee_count']].values
                ))
        
        fig.update_layout(
            title={
                'text': '💰 Global Gaming Salary Distribution by Location',
                'x': 0.5,
                'font': {'size': 18}
            },
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showocean=True,
                oceancolor='rgb(230, 245, 255)'
            ),
            height=600,
            showlegend=True
        )
        
        return fig
    
    def _create_empty_world_map(self) -> go.Figure:
        """Crée une carte mondiale vide en cas d'absence de données"""
        
        fig = go.Figure()
        
        fig.update_layout(
            title={
                'text': '🌍 Global Gaming Studios Map - No Data Available',
                'x': 0.5,
                'font': {'size': 18}
            },
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showocean=True,
                oceancolor='rgb(230, 245, 255)'
            ),
            height=600
        )
        
        fig.add_annotation(
            text="No studio data available for mapping",
            xref="paper", yref="paper",
            x=0.5, y=0.5, 
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        
        return fig
    
    def render_geographic_dashboard(self, studios_data: pd.DataFrame,
                                  migration_data: Optional[pd.DataFrame] = None,
                                  salary_data: Optional[pd.DataFrame] = None):
        """Dashboard complet des cartes géographiques"""
        
        st.markdown("## 🌍 Global Gaming Workforce Geography")
        st.markdown("*Interactive maps showing worldwide distribution of gaming talent and studios*")
        
        # Sélecteur de type de carte
        map_type = st.selectbox(
            "Choose Map Visualization:",
            ["Studios Distribution", "Regional Heatmap", "Talent Migration", "Salary Distribution"],
            index=0
        )
        
        # Affichage selon le type sélectionné
        if map_type == "Studios Distribution":
            fig = self.create_global_studios_map(studios_data)
            st.plotly_chart(fig, use_container_width=True)
            
            if not studios_data.empty:
                # Statistiques géographiques
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    unique_countries = studios_data['country'].nunique()
                    st.metric("🌍 Countries", unique_countries)
                
                with col2:
                    total_studios = len(studios_data)
                    st.metric("🏢 Total Studios", total_studios)
                
                with col3:
                    total_employees = studios_data['employees'].sum() if 'employees' in studios_data.columns else 0
                    st.metric("👥 Total Employees", f"{total_employees:,}")
                
                with col4:
                    avg_studio_size = studios_data['employees'].mean() if 'employees' in studios_data.columns else 0
                    st.metric("📊 Avg Studio Size", f"{avg_studio_size:.0f}")
        
        elif map_type == "Regional Heatmap":
            fig = self.create_regional_heatmap(studios_data)
            st.plotly_chart(fig, use_container_width=True)
        
        elif map_type == "Talent Migration" and migration_data is not None:
            fig = self.create_talent_migration_flow(migration_data)
            st.plotly_chart(fig, use_container_width=True)
        
        elif map_type == "Salary Distribution" and salary_data is not None:
            fig = self.create_salary_geographic_distribution(salary_data)
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info(f"Map type '{map_type}' requires additional data that is not currently available.")
