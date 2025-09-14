"""
Gaming Workforce Observatory - Data Loader
"""
import pandas as pd
import streamlit as st
from typing import Optional, Dict, Any

class DataLoader:
    """Chargeur de données gaming"""
    
    def __init__(self):
        pass
    
    @st.cache_resource(ttl=300)
    def load_sample_data(_self) -> pd.DataFrame:
        """Charge les données d'exemple gaming"""
        try:
            return pd.read_csv('data/sample_data.csv')
        except FileNotFoundError:
            # Données par défaut si fichier manquant
            return pd.DataFrame({
                'employee_id': [1, 2, 3],
                'name': ['Alice', 'Bob', 'Carol'],
                'department': ['Programming', 'Art', 'QA'],
                'level': ['Senior', 'Mid', 'Senior'],
                'salary': [95000, 65000, 82000],
                'satisfaction_score': [8.2, 9.1, 6.5],
                'performance_score': [4.5, 4.2, 3.8],
                'years_experience': [6, 4, 7],
                'sprint_velocity': [42, 0, 0],
                'bug_fix_rate': [0, 0, 92],
                'innovation_index': [85, 78, 65],
                'burnout_risk': [0.2, 0.1, 0.6]
            })
    
    def _clean_gaming_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données gaming"""
        # Nettoie les scores de satisfaction (1-10)
        df.loc[df['satisfaction_score'] > 10, 'satisfaction_score'] = 10
        df.loc[df['satisfaction_score'] < 1, 'satisfaction_score'] = 1
        
        # Nettoie les salaires (positifs)
        df.loc[df['salary'] < 0, 'salary'] = df['salary'].median()
        
        # Filtre les départements valides
        valid_departments = ['Programming', 'Art', 'Game Design', 'QA', 'Marketing', 'Management']
        df = df[df['department'].isin(valid_departments)]
        
        return df
    
    def _preprocess_gaming_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Préprocesse les données gaming"""
        # Convertir les dates
        if 'hire_date' in df.columns:
            df['hire_date'] = pd.to_datetime(df['hire_date'])
        
        # Créer des catégories
        if 'department' in df.columns:
            df['department'] = df['department'].astype('category')
        
        return df
    
    def filter_by_department(self, df: pd.DataFrame, department: str) -> pd.DataFrame:
        """Filtre par département gaming"""
        return df[df['department'] == department]
    
    def analyze_by_gaming_level(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyse par niveau gaming"""
        return df.groupby('level').agg({
            'salary': 'mean',
            'satisfaction_score': 'mean',
            'performance_score': 'mean'
        }).rename(columns={
            'salary': 'avg_salary',
            'satisfaction_score': 'avg_satisfaction',
            'performance_score': 'avg_performance'
        })
    
    def aggregate_gaming_metrics(self, df: pd.DataFrame, group_by: str = 'department') -> pd.DataFrame:
        """Agrégation des métriques gaming"""
        base_agg = {
            'satisfaction_score': 'mean',
            'performance_score': 'mean', 
            'salary': 'mean',
            'employee_id': 'count'
        }
        
        # Ajouter métriques spécifiques si disponibles
        if 'sprint_velocity' in df.columns:
            base_agg['sprint_velocity'] = lambda x: x[x > 0].mean() if (x > 0).any() else 0
        
        if 'bug_fix_rate' in df.columns:
            base_agg['bug_fix_rate'] = lambda x: x[x > 0].mean() if (x > 0).any() else 0
        
        result = df.groupby(group_by).agg(base_agg)
        result = result.rename(columns={
            'satisfaction_score': 'avg_satisfaction',
            'performance_score': 'avg_performance',
            'salary': 'avg_salary',
            'employee_id': 'employee_count',
            'sprint_velocity': 'avg_sprint_velocity',
            'bug_fix_rate': 'avg_bug_fix_rate'
        })
        
        return result
    
    def validate_gaming_schema(self, df: pd.DataFrame) -> None:
        """Valide le schéma gaming"""
        required_columns = ['employee_id', 'name', 'department', 'level', 
                          'salary', 'satisfaction_score']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required gaming columns: {missing_columns}")
    
    def calculate_gaming_performance_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calcule les métriques de performance gaming"""
        metrics = {
            'total_employees': len(df),
            'avg_satisfaction': float(df['satisfaction_score'].mean()),
            'avg_performance': float(df['performance_score'].mean())
        }
        
        # Métriques conditionnelles
        prog_data = df[df['department'] == 'Programming']
        if len(prog_data) > 0 and 'sprint_velocity' in df.columns:
            velocity_data = prog_data[prog_data['sprint_velocity'] > 0]
            if len(velocity_data) > 0:
                metrics['programming_velocity'] = float(velocity_data['sprint_velocity'].mean())
        
        qa_data = df[df['department'] == 'QA']
        if len(qa_data) > 0 and 'bug_fix_rate' in df.columns:
            bug_data = qa_data[qa_data['bug_fix_rate'] > 0]
            if len(bug_data) > 0:
                metrics['qa_bug_fix_rate'] = float(bug_data['bug_fix_rate'].mean())
        
        if 'innovation_index' in df.columns:
            metrics['innovation_index'] = float(df['innovation_index'].mean())
        
        if 'burnout_risk' in df.columns:
            metrics['retention_risk_score'] = float(df['burnout_risk'].mean())
        
        return metrics
# === FONCTIONS MANQUANTES ===
def load_employee_data():
    """Charge les données employés gaming"""
    loader = DataLoader()
    return loader.load_sample_data()

def load_monthly_metrics():
    """Charge les métriques mensuelles gaming"""
    import pandas as pd
    return pd.DataFrame({
        'month': pd.date_range('2023-01', periods=12, freq='ME'),
        'satisfaction': [7.2, 7.5, 7.8, 8.1, 7.9, 8.0, 7.7, 7.4, 7.6, 7.8, 8.2, 8.0],
        'performance': [4.1, 4.2, 4.3, 4.4, 4.2, 4.3, 4.0, 3.9, 4.1, 4.2, 4.4, 4.3],
        'velocity': [35, 38, 42, 40, 36, 39, 33, 31, 37, 41, 43, 40]
    })

def load_performance_data():
    """Charge les données de performance gaming"""
    loader = DataLoader()
    data = loader.load_sample_data()
    if 'employee_id' in data.columns and 'performance_score' in data.columns:
        return data[['employee_id', 'performance_score', 'department']]
    else:
        # Données par défaut si colonnes manquantes
        import pandas as pd
        import numpy as np
        return pd.DataFrame({
            'employee_id': range(1, 101),
            'performance_score': np.random.uniform(3.0, 5.0, 100),
            'department': np.random.choice(['Programming', 'Art', 'QA'], 100)
        })
# Ajoutez à la fin du fichier
def initialize_data_cache():
    """Initialise le cache des données"""
    return True
def initialize_data_cache():
    """Initialise le cache des données"""
    return True

def load_employee_data():
    """Charge les données employés gaming"""
    loader = DataLoader()
    return loader.load_sample_data()

def load_monthly_metrics():
    """Charge les métriques mensuelles gaming"""
    import pandas as pd
    return pd.DataFrame({
        'month': pd.date_range('2023-01', periods=12, freq='ME'),
        'satisfaction': [7.2, 7.5, 7.8, 8.1, 7.9, 8.0, 7.7, 7.4, 7.6, 7.8, 8.2, 8.0]
    })

def load_performance_data():
    """Charge les données de performance gaming"""
    loader = DataLoader()
    data = loader.load_sample_data()
    return data[['employee_id', 'performance_score', 'department']]

