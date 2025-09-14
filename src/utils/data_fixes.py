import pandas as pd

def standardize_gaming_dataframe(df):
    """Standardise les DataFrames pour compatibilité Gaming Observatory"""
    
    # Nettoyer les noms de colonnes
    df.columns = df.columns.str.strip().str.lower()
    
    # Mapping des colonnes courantes
    column_mapping = {
        'level': 'experience_level',
        'dept': 'department',
        'satisfaction': 'satisfaction_score',
        'performance': 'performance_score'
    }
    
    # Appliquer le mapping
    for old_name, new_name in column_mapping.items():
        if old_name in df.columns and new_name not in df.columns:
            df[new_name] = df[old_name]
    
    # Colonnes obligatoires avec valeurs par défaut
    required_columns = {
        'is_active': True,
        'experience_level': 'Unknown',
        'department': 'Unknown',
        'satisfaction_score': 7.0,
        'performance_score': 4.0
    }
    
    for col, default_value in required_columns.items():
        if col not in df.columns:
            df[col] = default_value
    
    return df
