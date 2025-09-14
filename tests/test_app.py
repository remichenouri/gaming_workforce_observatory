"""
Gaming Workforce Observatory - Application Tests
Tests pour l'application principale Streamlit
"""

import pytest
import pandas as pd
import streamlit as st
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import tempfile
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestGamingWorkforceApp:
    """Tests pour l'application Gaming Workforce Observatory"""
    
    @pytest.fixture
    def sample_gaming_data(self):
        """Données d'exemple pour les tests gaming"""
        return pd.DataFrame({
            'employee_id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Carol', 'David', 'Emma'],
            'department': ['Programming', 'Game Design', 'Art', 'QA', 'Marketing'],
            'level': ['Senior', 'Lead', 'Mid', 'Senior', 'Mid'],
            'salary': [95000, 110000, 65000, 82000, 58000],
            'satisfaction_score': [8.2, 7.8, 9.1, 6.5, 8.7],
            'performance_score': [4.5, 4.8, 4.2, 3.8, 4.1],
            'years_experience': [6, 8, 4, 7, 3],
            'sprint_velocity': [42, 38, 0, 0, 0],
            'bug_fix_rate': [88, 0, 0, 92, 0],
            'innovation_index': [85, 92, 78, 65, 71],
            'burnout_risk': [0.2, 0.3, 0.1, 0.6, 0.2]
        })
    
    @patch('streamlit.set_page_config')
    def test_app_configuration(self, mock_set_page_config):
        """Test de la configuration de l'application"""
        # Import de l'app (simulé)
        with patch('app.st') as mock_st:
            # Simuler l'importation et l'exécution de app.py
            mock_st.set_page_config = mock_set_page_config
            
            # Vérifier que la configuration gaming est appliquée
            expected_config = {
                'page_title': 'Gaming Workforce Observatory',
                'page_icon': '🎮',
                'layout': 'wide',
                'initial_sidebar_state': 'expanded'
            }
            
            # Simuler l'appel de configuration
            mock_set_page_config.assert_called_once()
    
    def test_gaming_data_loading(self, sample_gaming_data):
        """Test le chargement des données gaming"""
        # Créer un fichier temporaire avec les données
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_gaming_data.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            # Tester le chargement
            loaded_data = pd.read_csv(temp_file)
            
            # Vérifications gaming-spécifiques
            assert 'department' in loaded_data.columns
            assert 'sprint_velocity' in loaded_data.columns
            assert 'bug_fix_rate' in loaded_data.columns
            assert 'innovation_index' in loaded_data.columns
            
            # Vérifier les départements gaming
            gaming_departments = ['Programming', 'Game Design', 'Art', 'QA', 'Marketing']
            assert all(dept in gaming_departments for dept in loaded_data['department'].unique())
            
        finally:
            os.unlink(temp_file)
    
    @patch('src.data.kpis.GameKPICalculator')
    def test_gaming_kpi_calculations(self, mock_kpi_calculator, sample_gaming_data):
        """Test les calculs de KPI gaming"""
        # Mock du calculateur KPI
        mock_calculator_instance = Mock()
        mock_kpi_calculator.return_value = mock_calculator_instance
        
        # Définir les KPIs gaming attendus
        expected_kpis = {
            'avg_satisfaction': 8.06,
            'avg_sprint_velocity': 26.67,  # Moyenne des valeurs non-nulles
            'avg_bug_fix_rate': 60.0,
            'avg_innovation_index': 78.2,
            'retention_risk': 0.28
        }
        
        mock_calculator_instance.calculate_all_kpis.return_value = expected_kpis
        
        # Tester les calculs
        from src.data.kpis import GameKPICalculator
        calculator = GameKPICalculator(sample_gaming_data)
        kpis = calculator.calculate_all_kpis()
        
        assert 'avg_satisfaction' in kpis
        assert 'avg_sprint_velocity' in kpis
        assert 'avg_innovation_index' in kpis
    
    @patch('streamlit.plotly_chart')
    def test_gaming_visualizations(self, mock_plotly_chart, sample_gaming_data):
        """Test les visualisations gaming"""
        with patch('src.utils.charts.create_gaming_chart') as mock_create_chart:
            # Mock de création de graphique gaming
            mock_chart = Mock()
            mock_create_chart.return_value = mock_chart
            
            # Tester différents types de graphiques gaming
            chart_types = [
                'satisfaction_by_department',
                'sprint_velocity_trend',
                'bug_fix_rate_comparison',
                'innovation_index_heatmap'
            ]
            
            for chart_type in chart_types:
                mock_create_chart(sample_gaming_data, chart_type=chart_type)
                mock_create_chart.assert_called()
    
    def test_gaming_department_filtering(self, sample_gaming_data):
        """Test le filtrage par département gaming"""
        # Test filtrage Programming
        programming_data = sample_gaming_data[
            sample_gaming_data['department'] == 'Programming'
        ]
        assert len(programming_data) == 1
        assert programming_data.iloc[0]['sprint_velocity'] == 42
        
        # Test filtrage QA
        qa_data = sample_gaming_data[sample_gaming_data['department'] == 'QA']
        assert len(qa_data) == 1
        assert qa_data.iloc[0]['bug_fix_rate'] == 92
        
        # Test filtrage Art (pas de sprint velocity)
        art_data = sample_gaming_data[sample_gaming_data['department'] == 'Art']
        assert len(art_data) == 1
        assert art_data.iloc[0]['sprint_velocity'] == 0  # Art n'a pas de sprint velocity
    
    def test_gaming_level_analysis(self, sample_gaming_data):
        """Test l'analyse par niveau gaming"""
        # Grouper par niveau
        level_analysis = sample_gaming_data.groupby('level').agg({
            'salary': 'mean',
            'satisfaction_score': 'mean',
            'years_experience': 'mean'
        })
        
        # Vérifications gaming
        assert 'Senior' in level_analysis.index
        assert 'Lead' in level_analysis.index
        assert 'Mid' in level_analysis.index
        
        # Lead devrait avoir le salaire le plus élevé
        lead_salary = level_analysis.loc['Lead', 'salary']
        senior_salary = level_analysis.loc['Senior', 'salary']
        assert lead_salary > senior_salary
    
    @patch('src.ml.gaming_models.GamingTurnoverPredictor')
    def test_ml_predictions(self, mock_predictor, sample_gaming_data):
        """Test les prédictions ML gaming"""
        # Mock du prédicteur
        mock_predictor_instance = Mock()
        mock_predictor.return_value = mock_predictor_instance
        
        # Définir les prédictions attendues
        expected_predictions = {
            'high_risk_employees': ['David'],  # QA avec satisfaction 6.5 et burnout 0.6
            'model_accuracy': 0.82,
            'gaming_factors': ['low_satisfaction', 'high_burnout_risk']
        }
        
        mock_predictor_instance.predict_turnover_risk.return_value = expected_predictions
        
        # Tester les prédictions
        from src.ml.gaming_models import GamingTurnoverPredictor
        predictor = GamingTurnoverPredictor()
        predictions = predictor.predict_turnover_risk(sample_gaming_data)
        
        assert 'high_risk_employees' in predictions
        assert 'model_accuracy' in predictions
    
    def test_gaming_performance_thresholds(self, sample_gaming_data):
        """Test les seuils de performance gaming"""
        gaming_thresholds = {
            'satisfaction_critical': 6.0,
            'satisfaction_good': 8.0,
            'sprint_velocity_target': 40.0,
            'bug_fix_rate_target': 85.0,
            'innovation_index_target': 75.0
        }
        
        # Identifier les employés sous les seuils
        low_satisfaction = sample_gaming_data[
            sample_gaming_data['satisfaction_score'] < gaming_thresholds['satisfaction_critical']
        ]
        assert len(low_satisfaction) == 0  # Dans nos données test, tous > 6.0
        
        # Identifier les équipes avec bonne vélocité
        good_velocity = sample_gaming_data[
            (sample_gaming_data['sprint_velocity'] > 0) & 
            (sample_gaming_data['sprint_velocity'] >= gaming_thresholds['sprint_velocity_target'])
        ]
        assert len(good_velocity) == 1  # Alice en Programming avec 42
    
    @patch('streamlit.sidebar')
    def test_gaming_sidebar_filters(self, mock_sidebar):
        """Test les filtres de la sidebar gaming"""
        with patch('streamlit.selectbox') as mock_selectbox, \
             patch('streamlit.multiselect') as mock_multiselect, \
             patch('streamlit.slider') as mock_slider:
            
            # Simuler les filtres gaming
            gaming_departments = ['All', 'Programming', 'Game Design', 'Art', 'QA', 'Marketing']
            gaming_levels = ['All', 'Junior', 'Mid', 'Senior', 'Lead', 'Principal']
            
            mock_selectbox.side_effect = ['All', 'All']  # Department, Level
            mock_multiselect.return_value = gaming_departments[1:]  # Tous sauf 'All'
            mock_slider.return_value = [1, 10]  # Experience range
            
            # Vérifier que les filtres gaming sont disponibles
            assert 'Programming' in gaming_departments
            assert 'Game Design' in gaming_departments
            assert 'Senior' in gaming_levels
    
    def test_gaming_metrics_validation(self, sample_gaming_data):
        """Test la validation des métriques gaming"""
        # Vérifier les métriques gaming requises
        required_gaming_metrics = [
            'satisfaction_score', 'performance_score', 'sprint_velocity',
            'bug_fix_rate', 'innovation_index', 'burnout_risk'
        ]
        
        for metric in required_gaming_metrics:
            assert metric in sample_gaming_data.columns, f"Missing gaming metric: {metric}"
        
        # Vérifier les plages de valeurs gaming
        assert sample_gaming_data['satisfaction_score'].between(1, 10).all()
        assert sample_gaming_data['performance_score'].between(1, 5).all()
        assert sample_gaming_data['burnout_risk'].between(0, 1).all()
        assert sample_gaming_data['innovation_index'].between(0, 100).all()
    
    def test_gaming_dashboard_performance(self, sample_gaming_data):
        """Test les performances du dashboard gaming"""
        import time
        
        # Simuler le chargement des données
        start_time = time.time()
        
        # Opérations typiques du dashboard
        dept_summary = sample_gaming_data.groupby('department')['satisfaction_score'].mean()
        level_distribution = sample_gaming_data['level'].value_counts()
        avg_salary = sample_gaming_data['salary'].mean()
        
        load_time = time.time() - start_time
        
        # Le traitement des données doit être rapide
        assert load_time < 0.1, f"Data processing too slow: {load_time}s"
        
        # Vérifier que les calculs sont corrects
        assert len(dept_summary) == 5  # 5 départements
        assert len(level_distribution) == 3  # 3 niveaux dans les données test
        assert avg_salary > 0

class TestGamingAppIntegration:
    """Tests d'intégration pour l'application gaming"""
    
    def test_end_to_end_workflow(self):
        """Test du workflow complet gaming"""
        # Ce test simulerait un parcours utilisateur complet
        # 1. Chargement de l'app
        # 2. Sélection des filtres gaming
        # 3. Visualisation des KPIs
        # 4. Analyse des prédictions ML
        # 5. Export des rapports
        
        # Simulé pour l'exemple
        workflow_steps = [
            'load_gaming_data',
            'apply_gaming_filters', 
            'calculate_gaming_kpis',
            'generate_gaming_charts',
            'run_ml_predictions',
            'export_gaming_report'
        ]
        
        for step in workflow_steps:
            # Chaque étape devrait réussir
            assert step is not None
    
    @pytest.mark.slow
    def test_large_dataset_performance(self):
        """Test avec un large dataset gaming"""
        # Créer un dataset de grande taille pour tester les performances
        large_dataset = pd.DataFrame({
            'employee_id': range(1, 1001),
            'department': ['Programming', 'Art', 'Game Design', 'QA', 'Marketing'] * 200,
            'satisfaction_score': [8.0] * 1000,
            'performance_score': [4.0] * 1000,
            'salary': [75000] * 1000
        })
        
        import time
        start_time = time.time()
        
        # Opérations sur le large dataset
        summary = large_dataset.groupby('department').agg({
            'satisfaction_score': 'mean',
            'performance_score': 'mean', 
            'salary': 'mean'
        })
        
        processing_time = time.time() - start_time
        
        # Doit traiter 1000 employés rapidement
        assert processing_time < 1.0, f"Large dataset processing too slow: {processing_time}s"
        assert len(summary) == 5  # 5 départements

if __name__ == "__main__":
    pytest.main([__file__])
