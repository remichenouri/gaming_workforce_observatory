"""
Gaming Workforce Observatory - Neurodiversity Processor Enterprise
Traitement avancé des données neurodiversité avec analytics ROI
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import streamlit as st
import logging

logger = logging.getLogger(__name__)

class NeurodiversityProcessor:
    """Processeur enterprise pour données neurodiversité gaming"""
    
    def __init__(self):
        self.condition_mappings = {
            'ADHD': {
                'productivity_multiplier': 1.15,
                'innovation_boost': 1.25,
                'accommodation_cost': 2000
            },
            'Autism Spectrum': {
                'productivity_multiplier': 1.30,
                'innovation_boost': 1.20,
                'accommodation_cost': 2500
            },
            'Dyslexia': {
                'productivity_multiplier': 1.05,
                'innovation_boost': 1.30,
                'accommodation_cost': 1500
            },
            'Dyspraxia': {
                'productivity_multiplier': 1.08,
                'innovation_boost': 1.15,
                'accommodation_cost': 1800
            }
        }
    
    @st.cache_data(ttl=3600)
    def process_neurodiversity_data(_self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """Traite et enrichit les données neurodiversité"""
        
        if raw_df.empty:
            return pd.DataFrame()
        
        df = raw_df.copy()
        
        # Nettoyage des données
        df = _self._clean_neurodiversity_data(df)
        
        # Enrichissement avec métriques calculées
        df = _self._enrich_with_metrics(df)
        
        # Calcul ROI par employé
        df = _self._calculate_individual_roi(df)
        
        logger.info(f"Processed {len(df)} neurodiversity records")
        return df
    
    def _clean_neurodiversity_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données neurodiversité"""
        
        # Valeurs par défaut
        df.fillna({
            'condition_type': 'Unknown',
            'accommodations_provided': [],
            'performance_impact': 1.0,
            'satisfaction_with_support': 7.0,
            'support_cost_annual': 0
        }, inplace=True)
        
        # Normalisation des types de conditions
        condition_standardization = {
            'adhd': 'ADHD',
            'autism': 'Autism Spectrum',
            'asperger': 'Autism Spectrum',
            'dyslexic': 'Dyslexia',
            'dyspraxic': 'Dyspraxia'
        }
        
        df['condition_type'] = df['condition_type'].str.lower().replace(condition_standardization)
        df['condition_type'] = df['condition_type'].str.title()
        
        # Validation des scores
        df['performance_impact'] = df['performance_impact'].clip(0.5, 2.0)
        df['satisfaction_with_support'] = df['satisfaction_with_support'].clip(1, 10)
        
        return df
    
    def _enrich_with_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrichit avec des métriques calculées"""
        
        # Encodage des conditions
        condition_mapping = {condition: i+1 for i, condition in enumerate(self.condition_mappings.keys())}
        condition_mapping['Unknown'] = 0
        condition_mapping['Other'] = len(condition_mapping)
        
        df['condition_encoded'] = df['condition_type'].map(condition_mapping).fillna(0)
        
        # Score d'accommodation
        df['accommodation_score'] = df['accommodations_provided'].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        )
        
        # Multiplicateur de performance théorique
        df['theoretical_multiplier'] = df['condition_type'].map(
            lambda x: self.condition_mappings.get(x, {}).get('productivity_multiplier', 1.0)
        )
        
        # Écart performance réelle vs théorique
        df['performance_gap'] = df['performance_impact'] - df['theoretical_multiplier']
        
        # Score de support qualité
        df['support_quality_score'] = (
            df['satisfaction_with_support'] * df['accommodation_score'] / 10
        ).clip(0, 10)
        
        return df
    
    def _calculate_individual_roi(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule le ROI individuel pour chaque employé neurodivergent"""
        
        # Valeur de productivité baseline (salaire moyen gaming)
        baseline_productivity_value = 95000
        
        # Calcul valeur créée
        df['productivity_value_created'] = (
            baseline_productivity_value * (df['performance_impact'] - 1)
        )
        
        # Calcul coût total support
        df['total_support_cost'] = df['support_cost_annual'].fillna(0)
        
        # ROI individuel
        df['individual_roi'] = np.where(
            df['total_support_cost'] > 0,
            (df['productivity_value_created'] - df['total_support_cost']) / df['total_support_cost'] * 100,
            np.where(df['productivity_value_created'] > 0, 100, 0)
        )
        
        return df
    
    def analyze_department_neurodiversity(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse neurodiversité par département"""
        
        if 'department' not in df.columns:
            return {}
        
        dept_analysis = {}
        
        for dept in df['department'].unique():
            dept_data = df[df['department'] == dept]
            
            if len(dept_data) == 0:
                continue
            
            # Statistiques de base
            total_employees = len(dept_data)
            neurodiverse_count = len(dept_data[dept_data['condition_type'] != 'Unknown'])
            
            dept_analysis[dept] = {
                'total_employees': total_employees,
                'neurodiverse_count': neurodiverse_count,
                'neurodiversity_percentage': (neurodiverse_count / total_employees * 100) if total_employees > 0 else 0,
                'avg_performance_impact': dept_data['performance_impact'].mean(),
                'avg_satisfaction': dept_data['satisfaction_with_support'].mean(),
                'total_roi': dept_data['individual_roi'].sum(),
                'avg_roi_per_employee': dept_data['individual_roi'].mean(),
                'conditions_breakdown': dept_data['condition_type'].value_counts().to_dict()
            }
        
        return dept_analysis
    
    def calculate_organization_roi(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcule le ROI organisationnel global"""
        
        org_roi = {
            'total_neurodiverse_employees': len(df[df['condition_type'] != 'Unknown']),
            'total_productivity_value': df['productivity_value_created'].sum(),
            'total_support_costs': df['total_support_cost'].sum(),
            'net_benefit': df['productivity_value_created'].sum() - df['total_support_cost'].sum(),
            'overall_roi_percentage': 0,
            'average_individual_roi': df['individual_roi'].mean(),
            'conditions_distribution': df['condition_type'].value_counts().to_dict(),
            'high_performing_percentage': 0
        }
        
        # ROI global
        if org_roi['total_support_costs'] > 0:
            org_roi['overall_roi_percentage'] = (
                org_roi['net_benefit'] / org_roi['total_support_costs'] * 100
            )
        
        # Pourcentage haute performance
        high_performers = df[df['performance_impact'] > 1.2]
        org_roi['high_performing_percentage'] = (
            len(high_performers) / len(df) * 100 if len(df) > 0 else 0
        )
        
        return org_roi
    
    def generate_recommendations(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """Génère des recommandations basées sur l'analyse"""
        
        recommendations = []
        
        # Analyse des employés sous-performants
        underperforming = df[df['performance_impact'] < 0.9]
        if len(underperforming) > 0:
            recommendations.append({
                'category': 'Support Enhancement',
                'priority': 'High',
                'title': 'Améliorer support employés sous-performants',
                'description': f'{len(underperforming)} employés neurodivergents sous-performent. Réviser accommodations.',
                'action': 'Audit des accommodations et formation managers'
            })
        
        # Analyse satisfaction faible
        low_satisfaction = df[df['satisfaction_with_support'] < 6]
        if len(low_satisfaction) > 0:
            recommendations.append({
                'category': 'Employee Experience',
                'priority': 'Medium',
                'title': 'Améliorer satisfaction support',
                'description': f'{len(low_satisfaction)} employés peu satisfaits du support reçu.',
                'action': 'Sondage détaillé et amélioration processus'
            })
        
        # Conditions sans accommodation
        no_accommodation = df[(df['condition_type'] != 'Unknown') & (df['accommodation_score'] == 0)]
        if len(no_accommodation) > 0:
            recommendations.append({
                'category': 'Accommodation Gap',
                'priority': 'High',
                'title': 'Combler lacunes accommodations',
                'description': f'{len(no_accommodation)} employés neurodivergents sans accommodations.',
                'action': 'Évaluation besoins et mise en place accommodations'
            })
        
        return recommendations
    
    def export_neurodiversity_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Exporte un rapport complet neurodiversité"""
        
        report = {
            'summary': {
                'total_records': len(df),
                'generation_date': pd.Timestamp.now().isoformat(),
                'data_quality_score': self._calculate_data_quality_score(df)
            },
            'department_analysis': self.analyze_department_neurodiversity(df),
            'organization_roi': self.calculate_organization_roi(df),
            'recommendations': self.generate_recommendations(df),
            'detailed_metrics': {
                'condition_breakdown': df['condition_type'].value_counts().to_dict(),
                'performance_distribution': df['performance_impact'].describe().to_dict(),
                'roi_distribution': df['individual_roi'].describe().to_dict(),
                'satisfaction_scores': df['satisfaction_with_support'].describe().to_dict()
            }
        }
        
        return report
    
    def _calculate_data_quality_score(self, df: pd.DataFrame) -> float:
        """Calcule un score de qualité des données"""
        
        if df.empty:
            return 0.0
        
        quality_factors = []
        
        # Complétude des données essentielles
        essential_columns = ['condition_type', 'performance_impact', 'satisfaction_with_support']
        for col in essential_columns:
            if col in df.columns:
                completeness = 1 - (df[col].isnull().sum() / len(df))
                quality_factors.append(completeness)
        
        # Cohérence des valeurs
        valid_performance = df[
            (df['performance_impact'] >= 0.5) & (df['performance_impact'] <= 2.0)
        ].shape[0] / len(df)
        quality_factors.append(valid_performance)
        
        # Score global
        return np.mean(quality_factors) * 100 if quality_factors else 0.0
