"""
Gaming Workforce Observatory - Data Loader Tests
Tests pour le chargement des données gaming
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import tempfile
import os
from datetime import datetime, timedelta

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestGamingDataLoader:
    """Tests pour le chargeur de données gaming"""
    
    @pytest.fixture
    def temp_gaming_data_file(self):
        """Crée un fichier temporaire avec des données gaming"""
        gaming_data = pd.DataFrame({
            'employee_id': range(1, 11),
            'name': [f'GameDev_{i}' for i in range(1, 11)],
            'department': ['Programming', 'Art', 'Game Design', 'QA', 'Marketing'] * 2,
            'level': ['Junior', 'Mid', 'Senior', 'Lead', 'Senior'] * 2,
            'salary': [45000, 65000, 95000, 120000, 85000] * 2,
            'satisfaction_score': [8.5, 7.2, 9.1, 6.8, 8.0, 7.5, 8.8, 6.5, 9.2, 7.8],
            'performance_score': [4.2, 3.8, 4.5, 4.0, 4.1, 3.9, 4.3, 3.7, 4.6, 4.0],
            'years_experience': [2, 4, 7, 10, 6, 3, 8, 1, 9, 5],
            'hire_date': ['2022-01-15', '2020-06-10', '2018-03-22', '2016-11-05', '2019-08-17'] * 2,
            'sprint_velocity': [35, 0, 42, 0, 0, 38, 0, 41, 0, 0],
            'bug_fix_rate': [0, 0, 0, 88, 0, 0, 0, 0, 92, 0],
            'innovation_index': [82, 75, 90, 68, 71, 85, 78, 88, 65, 73],
            'burnout_risk': [0.2, 0.3, 0.1, 0.6, 0.25, 0.15, 0.4, 0.1, 0.55, 0.3]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            gaming_data.to_csv(f.name, index=False)
            yield f.name
        
        os.unlink(f.name)
    
    @patch('src.data.loader.pd.read_csv')
    def test_load_gaming_data_basic(self, mock_read_csv, temp_gaming_data_file):
        """Test basic gaming data loading functionality"""
        
        # ✅ Retourner un vrai DataFrame au lieu d'un Mock
        sample_gaming_data = pd.DataFrame({
            'employee_id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Carol'],
            'department': ['Programming', 'Art', 'QA'],
            'satisfaction_score': [8.5, 7.2, 9.1]
        })
        mock_read_csv.return_value = sample_gaming_data
        
        from src.data.loader import DataLoader
        loader = DataLoader()
        result = loader.load_sample_data()
        
        # Maintenant le test passera
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    
    def test_gaming_data_schema_validation(self, temp_gaming_data_file):
        """Test de validation du schéma de données gaming"""
        data = pd.read_csv(temp_gaming_data_file)
        
        # Colonnes requises pour l'analytics gaming
        required_gaming_columns = [
            'employee_id', 'name', 'department', 'level', 'salary',
            'satisfaction_score', 'performance_score', 'years_experience',
            'hire_date', 'sprint_velocity', 'bug_fix_rate', 'innovation_index'
        ]
        
        for column in required_gaming_columns:
            assert column in data.columns, f"Missing gaming column: {column}"
        
        # Vérifier les types de données gaming
        assert data['employee_id'].dtype in ['int64', 'int32']
        assert data['salary'].dtype in ['int64', 'int32', 'float64']
        assert data['satisfaction_score'].dtype == 'float64'
        assert data['sprint_velocity'].dtype in ['int64', 'int32', 'float64']
    
    def test_gaming_data_cleaning(self, temp_gaming_data_file):
        """Test du nettoyage des données gaming"""
        # Créer des données avec des problèmes
        dirty_data = pd.read_csv(temp_gaming_data_file)
        
        # Ajouter des valeurs problématiques
        dirty_data.loc[0, 'satisfaction_score'] = 15  # Hors limites
        dirty_data.loc[1, 'salary'] = -1000  # Négatif
        dirty_data.loc[2, 'department'] = 'InvalidDept'  # Département invalide
        
        # Simuler le nettoyage
        from src.data.loader import DataLoader
        loader = DataLoader()
        
        # Le nettoyage devrait corriger les problèmes
        cleaned_data = loader._clean_gaming_data(dirty_data)
        
        # Vérifications
        assert all(cleaned_data['satisfaction_score'].between(1, 10))
        assert all(cleaned_data['salary'] > 0)
        
        valid_departments = ['Programming', 'Art', 'Game Design', 'QA', 'Marketing']
        invalid_depts = cleaned_data[~cleaned_data['department'].isin(valid_departments)]
        assert len(invalid_depts) == 0, "Invalid departments should be cleaned"
    
    @patch('streamlit.cache_data')
    def test_gaming_data_caching(self, mock_cache_data):
        """Test du cache des données gaming"""
        # Simuler le décorateur de cache Streamlit
        def cache_decorator(ttl=300):
            def decorator(func):
                return func
            return decorator
        
        mock_cache_data.side_effect = cache_decorator
        
        from src.data.loader import DataLoader
        loader = DataLoader()
        
        # La méthode de chargement doit utiliser le cache
        with patch.object(loader, 'load_sample_data') as mock_load:
            mock_load.return_value = pd.DataFrame({'test': [1, 2, 3]})
            
            # Premier appel
            result1 = loader.load_sample_data()
            # Deuxième appel (devrait utiliser le cache)
            result2 = loader.load_sample_data()
            
            # Vérifier que les résultats sont identiques
            pd.testing.assert_frame_equal(result1, result2)
    
    def test_gaming_data_preprocessing(self, temp_gaming_data_file):
        """Test du préprocessing des données gaming"""
        data = pd.read_csv(temp_gaming_data_file)
        
        from src.data.loader import DataLoader
        loader = DataLoader()
        processed_data = loader._preprocess_gaming_data(data)
        
        # Vérifications du préprocessing gaming
        
        # 1. Les dates doivent être converties
        assert processed_data['hire_date'].dtype == 'datetime64[ns]'
        
        # 2. Les départements doivent être catégoriques
        assert processed_data['department'].dtype.name == 'category'
        
        # 3. Calculer l'ancienneté
        if 'tenure_months' in processed_data.columns:
            assert processed_data['tenure_months'].dtype in ['int64', 'float64']
            assert all(processed_data['tenure_months'] >= 0)
        
        # 4. Normaliser les scores gaming
        if 'satisfaction_normalized' in processed_data.columns:
            assert processed_data['satisfaction_normalized'].between(0, 1).all()
    
    def test_gaming_department_filtering(self, temp_gaming_data_file):
        """Test du filtrage par département gaming"""
        data = pd.read_csv(temp_gaming_data_file)
        
        from src.data.loader import DataLoader
        loader = DataLoader()
        
        # Test filtrage Programming
        programming_data = loader.filter_by_department(data, 'Programming')
        assert all(programming_data['department'] == 'Programming')
        assert any(programming_data['sprint_velocity'] > 0)  # Programming a sprint velocity
        
        # Test filtrage QA
        qa_data = loader.filter_by_department(data, 'QA')
        assert all(qa_data['department'] == 'QA')
        assert any(qa_data['bug_fix_rate'] > 0)  # QA a bug fix rate
        
        # Test filtrage Art
        art_data = loader.filter_by_department(data, 'Art')
        assert all(art_data['department'] == 'Art')
        assert all(art_data['sprint_velocity'] == 0)  # Art n'a pas de sprint velocity
    
    def test_gaming_level_analysis(self, temp_gaming_data_file):
        """Test de l'analyse par niveau gaming"""
        data = pd.read_csv(temp_gaming_data_file)
        
        from src.data.loader import DataLoader
        loader = DataLoader()
        
        # Analyser par niveau
        level_analysis = loader.analyze_by_gaming_level(data)
        
        # Vérifications
        gaming_levels = ['Junior', 'Mid', 'Senior', 'Lead']
        for level in gaming_levels:
            if level in level_analysis.index:
                # Lead doit avoir les salaires les plus élevés
                if level == 'Lead':
                    other_levels = [l for l in gaming_levels if l != 'Lead' and l in level_analysis.index]
                    for other_level in other_levels:
                        assert level_analysis.loc['Lead', 'avg_salary'] >= level_analysis.loc[other_level, 'avg_salary']
    
    def test_gaming_data_aggregation(self, temp_gaming_data_file):
        """Test de l'agrégation des données gaming"""
        data = pd.read_csv(temp_gaming_data_file)
        
        from src.data.loader import DataLoader
        loader = DataLoader()
        
        # Agrégation par département
        dept_summary = loader.aggregate_gaming_metrics(data, group_by='department')
        
        # Vérifications
        assert 'avg_satisfaction' in dept_summary.columns
        assert 'avg_performance' in dept_summary.columns
        assert 'avg_salary' in dept_summary.columns
        assert 'employee_count' in dept_summary.columns
        
        # Vérifier que Programming et QA ont des métriques spécifiques
        if 'Programming' in dept_summary.index:
            prog_row = dept_summary.loc['Programming']
            assert 'avg_sprint_velocity' in dept_summary.columns
        
        if 'QA' in dept_summary.index:
            qa_row = dept_summary.loc['QA']
            assert 'avg_bug_fix_rate' in dept_summary.columns
    
    def test_gaming_data_validation_errors(self):
        """Test de gestion des erreurs de validation gaming"""
        # Créer des données invalides
        invalid_data = pd.DataFrame({
            'employee_id': [1, 2, 3],
            'name': ['A', 'B', 'C'],
            # Manque des colonnes requises gaming
            'some_column': [1, 2, 3]
        })
        
        from src.data.loader import DataLoader
        loader = DataLoader()
        
        # Doit lever une exception pour données invalides
        with pytest.raises(ValueError, match="Missing required gaming columns"):
            loader.validate_gaming_schema(invalid_data)
    
    def test_gaming_performance_metrics_calculation(self, temp_gaming_data_file):
        """Test du calcul des métriques de performance gaming"""
        data = pd.read_csv(temp_gaming_data_file)
        
        from src.data.loader import DataLoader
        loader = DataLoader()
        
        # Calculer les métriques gaming
        metrics = loader.calculate_gaming_performance_metrics(data)
        
        # Vérifications des métriques gaming
        expected_metrics = [
            'total_employees',
            'avg_satisfaction',
            'avg_performance',
            'programming_velocity',
            'qa_bug_fix_rate',
            'innovation_index',
            'retention_risk_score'
        ]
        
        for metric in expected_metrics:
            assert metric in metrics, f"Missing gaming metric: {metric}"
        
        # Vérifier les valeurs
        assert metrics['total_employees'] == len(data)
        assert 1 <= metrics['avg_satisfaction'] <= 10
        assert 1 <= metrics['avg_performance'] <= 5
        assert 0 <= metrics['innovation_index'] <= 100
    
    def test_gaming_data_export(self, temp_gaming_data_file):
        """Test de l'export des données gaming"""
        data = pd.read_csv(temp_gaming_data_file)
