"""
Gaming Workforce Observatory - Salary Processor
Traitement et analyse avancée des données de salaires gaming
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import streamlit as st

logger = logging.getLogger(__name__)

class SalaryProcessor:
    """Processeur de données salaires gaming avec normalisation et détection d'anomalies"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(contamination=0.05, random_state=42)
        
        # Mapping des régions pour normalisation géographique
        self.region_mapping = {
            'San Francisco': 'San Francisco Bay Area',
            'SF': 'San Francisco Bay Area',
            'Silicon Valley': 'San Francisco Bay Area',
            'Los Angeles': 'Los Angeles',
            'LA': 'Los Angeles',
            'New York': 'New York',
            'NYC': 'New York',
            'Seattle': 'Seattle',
            'London': 'London',
            'Paris': 'Paris',
            'Berlin': 'Berlin',
            'Toronto': 'Toronto',
            'Montreal': 'Montreal',
            'Tokyo': 'Tokyo',
            'Seoul': 'Seoul'
        }
        
        # Coefficients d'ajustement géographique (base: San Francisco = 1.0)
        self.cost_of_living_adjustments = {
            'San Francisco Bay Area': 1.00,
            'New York': 0.95,
            'Los Angeles': 0.88,
            'Seattle': 0.85,
            'London': 0.82,
            'Toronto': 0.75,
            'Berlin': 0.68,
            'Paris': 0.78,
            'Montreal': 0.70,
            'Tokyo': 0.80,
            'Seoul': 0.65
        }
    
    @st.cache_data(ttl=7200)  # Cache 2 heures
    def process_salary_data(_self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Traite et nettoie les données de salaires brutes"""
        if raw_data.empty:
            return pd.DataFrame()
        
        df = raw_data.copy()
        
        # Étapes de nettoyage
        df = _self._clean_salary_values(df)
        df = _self._normalize_locations(df)
        df = _self._normalize_job_titles(df)
        df = _self._calculate_total_compensation(df)
        df = _self._adjust_for_cost_of_living(df)
        df = _self._detect_salary_anomalies(df)
        df = _self._enrich_with_experience_metrics(df)
        
        logger.info(f"Processed {len(df)} salary records")
        return df
    
    def _clean_salary_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie et valide les valeurs de salaires"""
        # Conversion en numérique
        salary_columns = ['salary_usd', 'bonus_usd', 'equity_value_usd']
        
        for col in salary_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Filtrage des valeurs aberrantes
        if 'salary_usd' in df.columns:
            # Salaires gaming raisonnables: 30K - 500K USD
            df = df[
                (df['salary_usd'] >= 30000) & 
                (df['salary_usd'] <= 500000)
            ]
        
        # Suppression des doublons
        duplicate_cols = ['company_name', 'role', 'experience_level', 'location']
        available_cols = [col for col in duplicate_cols if col in df.columns]
        if available_cols:
            df = df.drop_duplicates(subset=available_cols, keep='last')
        
        return df
    
    def _normalize_locations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalise les noms de lieux"""
        if 'location' not in df.columns:
            return df
        
        # Nettoyage basique
        df['location'] = df['location'].str.strip().str.title()
        
        # Application du mapping
        df['normalized_location'] = df['location'].map(
            lambda x: self.region_mapping.get(x, x) if pd.notna(x) else 'Remote'
        )
        
        return df
    
    def _normalize_job_titles(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalise les titres de postes gaming"""
        if 'role' not in df.columns and 'title' not in df.columns:
            return df
        
        role_col = 'role' if 'role' in df.columns else 'title'
        
        # Mapping des titres vers départements gaming
        title_to_department = {
            # Programming
            'software engineer': 'Programming',
            'game programmer': 'Programming', 
            'gameplay programmer': 'Programming',
            'engine programmer': 'Programming',
            'technical lead': 'Programming',
            'senior developer': 'Programming',
            
            # Art & Animation
            '3d artist': 'Art & Animation',
            'character artist': 'Art & Animation',
            'environment artist': 'Art & Animation',
            'animator': 'Art & Animation',
            'technical artist': 'Art & Animation',
            'concept artist': 'Art & Animation',
            
            # Game Design
            'game designer': 'Game Design',
            'level designer': 'Game Design',
            'gameplay designer': 'Game Design',
            'narrative designer': 'Game Design',
            'systems designer': 'Game Design',
            
            # QA
            'qa tester': 'Quality Assurance',
            'quality assurance': 'Quality Assurance',
            'test engineer': 'Quality Assurance',
            'qa analyst': 'Quality Assurance',
            
            # Production
            'producer': 'Production',
            'project manager': 'Production',
            'product manager': 'Production',
            'program manager': 'Production'
        }
        
        # Classification automatique
        df['normalized_role'] = df[role_col].str.lower()
        df['department'] = df['normalized_role'].map(
            lambda x: self._classify_role_to_department(x, title_to_department)
        )
        
        return df
    
    def _classify_role_to_department(self, role: str, mapping: Dict[str, str]) -> str:
        """Classifie un rôle dans un département gaming"""
        if pd.isna(role):
            return 'Other'
        
        role_lower = role.lower()
        
        # Recherche exacte d'abord
        if role_lower in mapping:
            return mapping[role_lower]
        
        # Recherche par mots-clés
        for key_phrase, department in mapping.items():
            if key_phrase in role_lower:
                return department
        
        # Classification par mots-clés génériques
        if any(word in role_lower for word in ['develop', 'program', 'code', 'engineer']):
            return 'Programming'
        elif any(word in role_lower for word in ['artist', 'art', 'visual', 'animator']):
            return 'Art & Animation'
        elif any(word in role_lower for word in ['design', 'game design']):
            return 'Game Design'
        elif any(word in role_lower for word in ['qa', 'test', 'quality']):
            return 'Quality Assurance'
        elif any(word in role_lower for word in ['producer', 'manager', 'lead']):
            return 'Production'
        else:
            return 'Other'
    
    def _calculate_total_compensation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule la compensation totale"""
        compensation_components = []
        
        if 'salary_usd' in df.columns:
            compensation_components.append(df['salary_usd'].fillna(0))
        
        if 'bonus_usd' in df.columns:
            compensation_components.append(df['bonus_usd'].fillna(0))
        
        if 'equity_value_usd' in df.columns:
            # Equity valorisée sur 4 ans (standard Silicon Valley)
            equity_annual = df['equity_value_usd'].fillna(0) / 4
            compensation_components.append(equity_annual)
        
        if compensation_components:
            df['total_compensation_usd'] = sum(compensation_components)
        
        return df
    
    def _adjust_for_cost_of_living(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ajuste les salaires selon le coût de la vie"""
        if 'normalized_location' not in df.columns or 'salary_usd' not in df.columns:
            return df
        
        df['cola_multiplier'] = df['normalized_location'].map(
            lambda x: self.cost_of_living_adjustments.get(x, 0.75)  # Default pour locations inconnues
        )
        
        df['salary_cola_adjusted'] = df['salary_usd'] / df['cola_multiplier']
        
        if 'total_compensation_usd' in df.columns:
            df['total_comp_cola_adjusted'] = df['total_compensation_usd'] / df['cola_multiplier']
        
        return df
    
    def _detect_salary_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Détecte les anomalies dans les salaires"""
        if 'salary_usd' not in df.columns or len(df) < 10:
            df['salary_anomaly'] = False
            return df
        
        # Features pour détection d'anomalies
        features = []
        feature_columns = []
        
        if 'salary_usd' in df.columns:
            features.append(df['salary_usd'].values.reshape(-1, 1))
            feature_columns.append('salary_usd')
        
        if 'total_compensation_usd' in df.columns:
            features.append(df['total_compensation_usd'].values.reshape(-1, 1))
            feature_columns.append('total_compensation_usd')
        
        if len(features) == 0:
            df['salary_anomaly'] = False
            return df
        
        # Préparation des données
        feature_matrix = np.hstack(features)
        feature_matrix = np.nan_to_num(feature_matrix, nan=0)
        
        # Détection d'anomalies
        try:
            anomaly_scores = self.anomaly_detector.fit_predict(feature_matrix)
            df['salary_anomaly'] = anomaly_scores == -1
            df['anomaly_score'] = self.anomaly_detector.decision_function(feature_matrix)
        except Exception as e:
            logger.warning(f"Anomaly detection failed: {e}")
            df['salary_anomaly'] = False
            df['anomaly_score'] = 0
        
        return df
    
    def _enrich_with_experience_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrichit avec des métriques d'expérience"""
        if 'experience_level' not in df.columns:
            return df
        
        # Mapping années d'expérience
        experience_to_years = {
            'Intern': 0,
            'Junior': 1.5,
            'Mid': 4,
            'Senior': 8,
            'Lead': 12,
            'Principal': 15,
            'Director': 18
        }
        
        df['estimated_years_experience'] = df['experience_level'].map(
            lambda x: experience_to_years.get(x, 4) if pd.notna(x) else 4
        )
        
        # Score de progression salariale
        if 'salary_usd' in df.columns:
            df['salary_per_experience_year'] = df['salary_usd'] / (df['estimated_years_experience'] + 1)
        
        return df
    
    def calculate_salary_percentiles(self, df: pd.DataFrame, 
                                   group_by: List[str] = None) -> pd.DataFrame:
        """Calcule les percentiles de salaires par groupe"""
        if df.empty or 'salary_usd' not in df.columns:
            return pd.DataFrame()
        
        group_by = group_by or ['department', 'experience_level']
        available_groups = [col for col in group_by if col in df.columns]
        
        if not available_groups:
            return df
        
        percentiles = [10, 25, 50, 75, 90]
        
        result = df.groupby(available_groups)['salary_usd'].agg([
            ('count', 'count'),
            ('mean', 'mean'),
            ('std', 'std'),
            *[(f'p{p}', lambda x, p=p: np.percentile(x.dropna(), p)) for p in percentiles]
        ]).reset_index()
        
        # Ajout de métriques dérivées
        result['cv'] = result['std'] / result['mean']  # Coefficient de variation
        result['iqr'] = result['p75'] - result['p25']  # Interquartile range
        
        return result
    
    def generate_salary_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Génère des insights sur les données de salaires"""
        if df.empty:
            return {'status': 'no_data'}
        
        insights = {
            'total_records': len(df),
            'date_range': {
                'from': df['created_at'].min() if 'created_at' in df.columns else None,
                'to': df['created_at'].max() if 'created_at' in df.columns else None
            }
        }
        
        if 'salary_usd' in df.columns:
            salary_data = df['salary_usd'].dropna()
            insights['salary_stats'] = {
                'median': salary_data.median(),
                'mean': salary_data.mean(),
                'std': salary_data.std(),
                'min': salary_data.min(),
                'max': salary_data.max(),
                'q1': salary_data.quantile(0.25),
                'q3': salary_data.quantile(0.75)
            }
        
        # Insights par département
        if 'department' in df.columns and 'salary_usd' in df.columns:
            dept_stats = df.groupby('department')['salary_usd'].agg([
                'count', 'mean', 'median', 'std'
            ]).round(0)
            insights['department_breakdown'] = dept_stats.to_dict('index')
        
        # Insights par niveau d'expérience
        if 'experience_level' in df.columns and 'salary_usd' in df.columns:
            exp_stats = df.groupby('experience_level')['salary_usd'].agg([
                'count', 'mean', 'median'
            ]).round(0)
            insights['experience_breakdown'] = exp_stats.to_dict('index')
        
        # Détection des anomalies
        if 'salary_anomaly' in df.columns:
            anomaly_count = df['salary_anomaly'].sum()
            insights['anomalies'] = {
                'count': int(anomaly_count),
                'percentage': float(anomaly_count / len(df) * 100)
            }
        
        # Top paying companies
        if 'company_name' in df.columns and 'salary_usd' in df.columns:
            top_companies = df.groupby('company_name')['salary_usd'].mean().sort_values(ascending=False).head(10)
            insights['top_paying_companies'] = top_companies.round(0).to_dict()
        
        return insights
    
    def export_processed_data(self, df: pd.DataFrame, format: str = 'csv') -> str:
        """Exporte les données traitées"""
        if df.empty:
            return ""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'csv':
            filename = f"gaming_salaries_processed_{timestamp}.csv"
            csv_data = df.to_csv(index=False)
            return csv_data
        elif format == 'json':
            filename = f"gaming_salaries_processed_{timestamp}.json"
            json_data = df.to_json(orient='records', indent=2)
            return json_data
        else:
            raise ValueError(f"Unsupported format: {format}")
