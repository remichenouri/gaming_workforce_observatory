"""
Gaming Workforce Observatory - Studio Processor Enterprise
Analyse avancée des données des studios gaming globaux
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

class GamingStudioProcessor:
    """Processeur avancé pour analyse des studios gaming mondiaux"""
    
    def __init__(self):
        self.studio_categories = {
            'AAA_Studio': {'min_employees': 500, 'min_revenue': 100000000},
            'AA_Studio': {'min_employees': 100, 'min_revenue': 10000000},
            'Indie_Studio': {'min_employees': 5, 'min_revenue': 1000000},
            'Startup_Studio': {'min_employees': 1, 'min_revenue': 0}
        }
        
        self.regional_multipliers = {
            'North America': {'cost_of_living': 1.0, 'talent_availability': 0.9},
            'Europe': {'cost_of_living': 0.85, 'talent_availability': 0.95},
            'Asia-Pacific': {'cost_of_living': 0.65, 'talent_availability': 0.8},
            'Latin America': {'cost_of_living': 0.4, 'talent_availability': 0.7}
        }
        
        self.genre_specializations = [
            'Action', 'RPG', 'Strategy', 'Simulation', 'Sports', 'Racing',
            'Adventure', 'Puzzle', 'Fighting', 'Shooter', 'Platform', 'MMO',
            'Mobile', 'VR/AR', 'Indie', 'Casual'
        ]
    
    @st.cache_data(ttl=7200)
    def analyze_global_studios(_self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse complète des studios gaming globaux"""
        
        if studios_df.empty:
            return {'status': 'no_data', 'analysis': {}}
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'total_studios_analyzed': len(studios_df),
            'geographic_analysis': _self._analyze_geographic_distribution(studios_df),
            'size_categorization': _self._categorize_studios_by_size(studios_df),
            'financial_analysis': _self._analyze_financial_metrics(studios_df),
            'talent_analysis': _self._analyze_talent_patterns(studios_df),
            'competitive_landscape': _self._analyze_competitive_positioning(studios_df),
            'market_opportunities': _self._identify_market_opportunities(studios_df),
            'risk_assessment': _self._assess_studio_risks(studios_df),
            'benchmarking': _self._generate_benchmarking_data(studios_df)
        }
        
        logger.info(f"Global studio analysis completed for {len(studios_df)} studios")
        return analysis_results
    
    def _analyze_geographic_distribution(self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse la distribution géographique des studios"""
        
        geo_analysis = {
            'by_country': {},
            'by_region': {},
            'concentration_metrics': {},
            'expansion_patterns': {}
        }
        
        if 'country' not in studios_df.columns:
            return geo_analysis
        
        # Analyse par pays
        country_stats = studios_df.groupby('country').agg({
            'employees': ['count', 'sum', 'mean', 'median'],
            'avg_salary': 'mean',
            'retention_rate': 'mean',
            'founded_year': 'mean'
        }).round(2)
        
        country_stats.columns = ['_'.join(col).strip() for col in country_stats.columns]
        geo_analysis['by_country'] = country_stats.to_dict('index')
        
        # Analyse par région
        if 'region' in studios_df.columns:
            region_stats = studios_df.groupby('region').agg({
                'employees': ['count', 'sum', 'mean'],
                'avg_salary': 'mean',
                'retention_rate': 'mean'
            }).round(2)
            
            region_stats.columns = ['_'.join(col).strip() for col in region_stats.columns]
            geo_analysis['by_region'] = region_stats.to_dict('index')
        
        # Métriques de concentration
        total_employees = studios_df['employees'].sum()
        top_5_countries = studios_df.groupby('country')['employees'].sum().nlargest(5)
        
        geo_analysis['concentration_metrics'] = {
            'top_5_countries_share': (top_5_countries.sum() / total_employees * 100).round(2),
            'herfindahl_index': self._calculate_herfindahl_index(studios_df, 'country'),
            'geographic_diversity_score': len(studios_df['country'].unique())
        }
        
        return geo_analysis
    
    def _categorize_studios_by_size(self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Catégorise les studios par taille et type"""
        
        size_analysis = {
            'categories': {},
            'size_distribution': {},
            'growth_patterns': {},
            'efficiency_metrics': {}
        }
        
        if 'employees' not in studios_df.columns:
            return size_analysis
        
        # Classification par catégorie
        studios_df['studio_category'] = studios_df.apply(
            lambda row: self._classify_studio_category(row), axis=1
        )
        
        category_stats = studios_df.groupby('studio_category').agg({
            'employees': ['count', 'mean', 'median', 'sum'],
            'avg_salary': 'mean',
            'retention_rate': 'mean',
            'revenue_usd': 'mean' if 'revenue_usd' in studios_df.columns else lambda x: None
        }).round(2)
        
        category_stats.columns = ['_'.join(col).strip() for col in category_stats.columns]
        size_analysis['categories'] = category_stats.to_dict('index')
        
        # Distribution de taille
        size_ranges = [
            (1, 10, 'Micro (1-10)'),
            (11, 50, 'Small (11-50)'), 
            (51, 200, 'Medium (51-200)'),
            (201, 1000, 'Large (201-1000)'),
            (1001, float('inf'), 'Enterprise (1000+)')
        ]
        
        size_distribution = {}
        for min_size, max_size, label in size_ranges:
            if max_size == float('inf'):
                mask = studios_df['employees'] >= min_size
            else:
                mask = (studios_df['employees'] >= min_size) & (studios_df['employees'] <= max_size)
            
            studios_in_range = studios_df[mask]
            
            size_distribution[label] = {
                'count': len(studios_in_range),
                'percentage': (len(studios_in_range) / len(studios_df) * 100).round(2),
                'avg_salary': studios_in_range['avg_salary'].mean() if 'avg_salary' in studios_in_range.columns else None,
                'avg_retention': studios_in_range['retention_rate'].mean() if 'retention_rate' in studios_in_range.columns else None
            }
        
        size_analysis['size_distribution'] = size_distribution
        
        return size_analysis
    
    def _classify_studio_category(self, studio_row: pd.Series) -> str:
        """Classifie un studio selon sa catégorie"""
        employees = studio_row.get('employees', 0)
        revenue = studio_row.get('revenue_usd', 0)
        
        for category, criteria in self.studio_categories.items():
            if (employees >= criteria['min_employees'] and 
                revenue >= criteria['min_revenue']):
                return category
        
        return 'Startup_Studio'
    
    def _analyze_financial_metrics(self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse les métriques financières des studios"""
        
        financial_analysis = {
            'revenue_analysis': {},
            'profitability_metrics': {},
            'efficiency_ratios': {},
            'cost_structure': {}
        }
        
        # Analyse des revenus
        if 'revenue_usd' in studios_df.columns:
            revenue_stats = {
                'total_revenue': studios_df['revenue_usd'].sum(),
                'avg_revenue': studios_df['revenue_usd'].mean(),
                'median_revenue': studios_df['revenue_usd'].median(),
                'revenue_std': studios_df['revenue_usd'].std(),
                'top_10_percent_share': self._calculate_top_percentile_share(studios_df, 'revenue_usd', 0.1)
            }
            financial_analysis['revenue_analysis'] = revenue_stats
        
        # Ratios d'efficacité
        if 'revenue_usd' in studios_df.columns and 'employees' in studios_df.columns:
            studios_df['revenue_per_employee'] = studios_df['revenue_usd'] / studios_df['employees']
            
            efficiency_metrics = {
                'avg_revenue_per_employee': studios_df['revenue_per_employee'].mean(),
                'median_revenue_per_employee': studios_df['revenue_per_employee'].median(),
                'top_quartile_efficiency': studios_df['revenue_per_employee'].quantile(0.75)
            }
            financial_analysis['efficiency_ratios'] = efficiency_metrics
        
        # Structure des coûts
        if 'avg_salary' in studios_df.columns and 'employees' in studios_df.columns:
            studios_df['total_salary_cost'] = studios_df['avg_salary'] * studios_df['employees']
            
            if 'revenue_usd' in studios_df.columns:
                studios_df['salary_cost_ratio'] = studios_df['total_salary_cost'] / studios_df['revenue_usd']
                
                cost_structure = {
                    'avg_salary_cost_ratio': studios_df['salary_cost_ratio'].mean(),
                    'median_salary_cost_ratio': studios_df['salary_cost_ratio'].median(),
                    'efficient_studios_ratio': (studios_df['salary_cost_ratio'] < 0.6).sum() / len(studios_df)
                }
                financial_analysis['cost_structure'] = cost_structure
        
        return financial_analysis
    
    def _analyze_talent_patterns(self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse les patterns de talents et RH"""
        
        talent_analysis = {
            'retention_patterns': {},
            'salary_benchmarks': {},
            'hiring_trends': {},
            'diversity_metrics': {}
        }
        
        # Patterns de rétention
        if 'retention_rate' in studios_df.columns:
            retention_stats = {
                'avg_retention_rate': studios_df['retention_rate'].mean(),
                'median_retention_rate': studios_df['retention_rate'].median(),
                'high_retention_studios': (studios_df['retention_rate'] > 90).sum(),
                'low_retention_studios': (studios_df['retention_rate'] < 70).sum(),
                'retention_by_size': studios_df.groupby('studio_category')['retention_rate'].mean().to_dict() if 'studio_category' in studios_df.columns else {}
            }
            talent_analysis['retention_patterns'] = retention_stats
        
        # Benchmarks salariaux
        if 'avg_salary' in studios_df.columns:
            salary_benchmarks = {
                'global_avg_salary': studios_df['avg_salary'].mean(),
                'salary_p25': studios_df['avg_salary'].quantile(0.25),
                'salary_p50': studios_df['avg_salary'].quantile(0.50),
                'salary_p75': studios_df['avg_salary'].quantile(0.75),
                'salary_p90': studios_df['avg_salary'].quantile(0.90),
                'salary_by_region': studios_df.groupby('region')['avg_salary'].mean().to_dict() if 'region' in studios_df.columns else {}
            }
            talent_analysis['salary_benchmarks'] = salary_benchmarks
        
        # Métriques de diversité
        if 'neurodiversity_programs' in studios_df.columns:
            diversity_stats = {
                'studios_with_programs': studios_df['neurodiversity_programs'].sum(),
                'program_adoption_rate': (studios_df['neurodiversity_programs'] > 0).sum() / len(studios_df) * 100,
                'correlation_with_retention': studios_df[['neurodiversity_programs', 'retention_rate']].corr().iloc[0, 1] if 'retention_rate' in studios_df.columns else None
            }
            talent_analysis['diversity_metrics'] = diversity_stats
        
        return talent_analysis
    
    def _analyze_competitive_positioning(self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse le positionnement concurrentiel"""
        
        competitive_analysis = {
            'market_leaders': {},
            'competitive_clusters': {},
            'positioning_matrix': {},
            'growth_leaders': {}
        }
        
        # Identification des leaders du marché
        if 'revenue_usd' in studios_df.columns and 'employees' in studios_df.columns:
            # Top studios par revenus
            top_revenue = studios_df.nlargest(10, 'revenue_usd')[['name', 'revenue_usd', 'employees', 'country']].to_dict('records') if 'name' in studios_df.columns else []
            
            # Top studios par employés
            top_employees = studios_df.nlargest(10, 'employees')[['name', 'employees', 'revenue_usd', 'country']].to_dict('records') if 'name' in studios_df.columns else []
            
            # Top studios par efficacité
            if 'revenue_per_employee' in studios_df.columns:
                top_efficiency = studios_df.nlargest(10, 'revenue_per_employee')[['name', 'revenue_per_employee', 'employees', 'country']].to_dict('records') if 'name' in studios_df.columns else []
            else:
                top_efficiency = []
            
            competitive_analysis['market_leaders'] = {
                'by_revenue': top_revenue,
                'by_size': top_employees,
                'by_efficiency': top_efficiency
            }
        
        # Clustering concurrentiel
        if len(studios_df) > 10:
            competitive_analysis['competitive_clusters'] = self._perform_competitive_clustering(studios_df)
        
        return competitive_analysis
    
    def _perform_competitive_clustering(self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Effectue un clustering des studios pour analyse concurrentielle"""
        
        # Sélection des features pour clustering
        clustering_features = []
        feature_names = []
        
        if 'employees' in studios_df.columns:
            clustering_features.append(studios_df['employees'].values.reshape(-1, 1))
            feature_names.append('employees')
        
        if 'revenue_usd' in studios_df.columns:
            clustering_features.append(studios_df['revenue_usd'].fillna(0).values.reshape(-1, 1))
            feature_names.append('revenue_usd')
        
        if 'avg_salary' in studios_df.columns:
            clustering_features.append(studios_df['avg_salary'].fillna(0).values.reshape(-1, 1))
            feature_names.append('avg_salary')
        
        if 'retention_rate' in studios_df.columns:
            clustering_features.append(studios_df['retention_rate'].fillna(75).values.reshape(-1, 1))
            feature_names.append('retention_rate')
        
        if len(clustering_features) < 2:
            return {'status': 'insufficient_features'}
        
        # Préparation des données
        X = np.hstack(clustering_features)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Clustering K-means
        n_clusters = min(5, len(studios_df) // 3)  # Max 5 clusters, min 3 studios par cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X_scaled)
        
        # Analyse des clusters
        studios_df_temp = studios_df.copy()
        studios_df_temp['cluster'] = cluster_labels
        
        cluster_analysis = {}
        for cluster_id in range(n_clusters):
            cluster_studios = studios_df_temp[studios_df_temp['cluster'] == cluster_id]
            
            cluster_stats = {
                'count': len(cluster_studios),
                'avg_employees': cluster_studios['employees'].mean() if 'employees' in cluster_studios.columns else None,
                'avg_revenue': cluster_studios['revenue_usd'].mean() if 'revenue_usd' in cluster_studios.columns else None,
                'avg_salary': cluster_studios['avg_salary'].mean() if 'avg_salary' in cluster_studios.columns else None,
                'avg_retention': cluster_studios['retention_rate'].mean() if 'retention_rate' in cluster_studios.columns else None,
                'dominant_countries': cluster_studios['country'].value_counts().head(3).to_dict() if 'country' in cluster_studios.columns else {}
            }
            
            cluster_analysis[f'Cluster_{cluster_id}'] = cluster_stats
        
        return {
            'cluster_analysis': cluster_analysis,
            'feature_names': feature_names,
            'n_clusters': n_clusters
        }
    
    def _identify_market_opportunities(self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Identifie les opportunités de marché"""
        
        opportunities = {
            'underserved_regions': [],
            'talent_arbitrage': [],
            'efficiency_gaps': [],
            'growth_segments': []
        }
        
        # Régions sous-servies (peu de studios mais bon marché)
        if 'country' in studios_df.columns and 'avg_salary' in studios_df.columns:
            country_stats = studios_df.groupby('country').agg({
                'employees': 'count',
                'avg_salary': 'mean'
            }).reset_index()
            
            # Pays avec peu de studios mais salaires bas
            underserved = country_stats[
                (country_stats['employees'] < 5) & 
                (country_stats['avg_salary'] < country_stats['avg_salary'].median())
            ]
            
            opportunities['underserved_regions'] = underserved.to_dict('records')
        
        # Opportunités d'arbitrage talent
        if 'retention_rate' in studios_df.columns and 'avg_salary' in studios_df.columns:
            # Studios avec haute rétention mais salaires relativement bas
            talent_arbitrage = studios_df[
                (studios_df['retention_rate'] > studios_df['retention_rate'].quantile(0.75)) &
                (studios_df['avg_salary'] < studios_df['avg_salary'].median())
            ]
            
            if not talent_arbitrage.empty:
                opportunities['talent_arbitrage'] = talent_arbitrage[['name', 'country', 'retention_rate', 'avg_salary']].to_dict('records') if 'name' in talent_arbitrage.columns else []
        
        return opportunities
    
    def _assess_studio_risks(self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Évalue les risques des studios"""
        
        risk_assessment = {
            'high_risk_studios': [],
            'risk_factors': {},
            'industry_risks': {},
            'mitigation_strategies': []
        }
        
        # Identification studios à haut risque
        risk_criteria = []
        
        if 'retention_rate' in studios_df.columns:
            risk_criteria.append(studios_df['retention_rate'] < 70)
        
        if 'avg_salary' in studios_df.columns:
            low_salary_threshold = studios_df['avg_salary'].quantile(0.25)
            risk_criteria.append(studios_df['avg_salary'] < low_salary_threshold)
        
        if 'revenue_per_employee' in studios_df.columns:
            low_efficiency_threshold = studios_df['revenue_per_employee'].quantile(0.25)
            risk_criteria.append(studios_df['revenue_per_employee'] < low_efficiency_threshold)
        
        if risk_criteria:
            # Studios avec au moins 2 facteurs de risque
            high_risk_mask = sum(risk_criteria) >= 2
            high_risk_studios = studios_df[high_risk_mask]
            
            if not high_risk_studios.empty:
                risk_assessment['high_risk_studios'] = high_risk_studios[['name', 'country', 'employees']].to_dict('records') if 'name' in high_risk_studios.columns else []
        
        # Facteurs de risque industrie
        risk_assessment['industry_risks'] = {
            'talent_shortage_risk': 'High',
            'market_saturation_risk': 'Medium',
            'technology_disruption_risk': 'High',
            'economic_sensitivity_risk': 'Medium'
        }
        
        return risk_assessment
    
    def _generate_benchmarking_data(self, studios_df: pd.DataFrame) -> Dict[str, Any]:
        """Génère des données de benchmarking"""
        
        benchmarks = {
            'percentiles': {},
            'industry_standards': {},
            'best_practices': {},
            'performance_targets': {}
        }
        
        # Percentiles pour métriques clés
        metrics_to_benchmark = ['employees', 'avg_salary', 'retention_rate', 'revenue_usd']
        
        for metric in metrics_to_benchmark:
            if metric in studios_df.columns:
                benchmarks['percentiles'][metric] = {
                    'p10': studios_df[metric].quantile(0.10),
                    'p25': studios_df[metric].quantile(0.25),
                    'p50': studios_df[metric].quantile(0.50),
                    'p75': studios_df[metric].quantile(0.75),
                    'p90': studios_df[metric].quantile(0.90)
                }
        
        # Standards industrie
        benchmarks['industry_standards'] = {
            'minimum_retention_rate': 75,
            'target_retention_rate': 85,
            'excellent_retention_rate': 90,
            'competitive_salary_percentile': 75,
            'high_growth_revenue_threshold': 10000000
        }
        
        return benchmarks
    
    def _calculate_herfindahl_index(self, df: pd.DataFrame, column: str) -> float:
        """Calcule l'indice Herfindahl pour mesurer la concentration"""
        if column not in df.columns:
            return 0
        
        # Calcul des parts de marché
        total = df['employees'].sum() if 'employees' in df.columns else len(df)
        market_shares = df.groupby(column)['employees'].sum() / total if 'employees' in df.columns else df.groupby(column).size() / len(df)
        
        # Indice Herfindahl = somme des carrés des parts de marché
        hhi = (market_shares ** 2).sum()
        return round(hhi, 4)
    
    def _calculate_top_percentile_share(self, df: pd.DataFrame, column: str, percentile: float) -> float:
        """Calcule la part du top percentile"""
        if column not in df.columns:
            return 0
        
        threshold = df[column].quantile(1 - percentile)
        top_percentile_sum = df[df[column] >= threshold][column].sum()
        total_sum = df[column].sum()
        
        return round((top_percentile_sum / total_sum * 100), 2) if total_sum > 0 else 0
    
    def _calculate_top_percentile_share(self, df: pd.DataFrame, column: str, percentile: float) -> float:
        """Calcule la part détenue par le top percentile"""
        if column not in df.columns or df[column].sum() == 0:
            return 0
        
        threshold = df[column].quantile(1 - percentile)
        top_percentile_sum = df[df[column] >= threshold][column].sum()
        total_sum = df[column].sum()
        
        return round((top_percentile_sum / total_sum * 100), 2)
    
    def export_studio_analysis(self, analysis_results: Dict[str, Any]) -> pd.DataFrame:
        """Exporte l'analyse des studios en DataFrame"""
        
        if not analysis_results or analysis_results.get('status') == 'no_data':
            return pd.DataFrame()
        
        # Extraction des données principales pour export
        export_data = []
        
        # Données géographiques
        geo_data = analysis_results.get('geographic_analysis', {})
        for country, stats in geo_data.get('by_country', {}).items():
            export_data.append({
                'metric_type': 'geographic',
                'category': country,
                'studios_count': stats.get('employees_count', 0),
                'total_employees': stats.get('employees_sum', 0),
                'avg_salary': stats.get('avg_salary_mean', 0),
                'avg_retention': stats.get('retention_rate_mean', 0)
            })
        
        # Données par taille
        size_data = analysis_results.get('size_categorization', {})
        for category, stats in size_data.get('categories', {}).items():
            export_data.append({
                'metric_type': 'size_category', 
                'category': category,
                'studios_count': stats.get('employees_count', 0),
                'avg_employees': stats.get('employees_mean', 0),
                'avg_salary': stats.get('avg_salary_mean', 0),
                'avg_retention': stats.get('retention_rate_mean', 0)
            })
        
        df_export = pd.DataFrame(export_data)
        df_export['analysis_timestamp'] = analysis_results.get('timestamp')
        
        return df_export
