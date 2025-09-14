# tests/test_gaming_functions.py
import pytest
import pandas as pd
import sys
import os

# Ajouter le chemin src pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.kpis import GameKPICalculator
from data.loader import DataLoader

class TestGamingFunctions:
    
    def setup_method(self):
        """Setup données gaming test"""
        self.gaming_data = pd.DataFrame({
            'employee_id': range(1, 11),
            'department': ['Programming', 'Art', 'QA'] * 3 + ['Marketing'],
            'satisfaction_score': [8.2, 7.5, 9.1] * 3 + [7.8],
            'performance_score': [4.1, 4.3, 4.6] * 3 + [4.2],
            'sprint_velocity': [35, 0, 0] * 3 + [0],
            'innovation_index': [82, 75, 68] * 3 + [85]
        })
    
    def test_gaming_kpi_calculator_init(self):
        """Test initialisation GameKPICalculator"""
        calculator = GameKPICalculator(self.gaming_data)
        assert calculator.data.shape == (10, 6)
        assert 'department' in calculator.data.columns
    
    def test_calculate_gaming_satisfaction(self):
        """Test calcul satisfaction gaming"""
        calculator = GameKPICalculator(self.gaming_data)
        satisfaction = calculator.calculate_gaming_satisfaction()
        
        assert isinstance(satisfaction, float)
        assert 0 <= satisfaction <= 10
    
    def test_calculate_all_gaming_kpis(self):
        """Test calcul ensemble KPIs gaming"""
        calculator = GameKPICalculator(self.gaming_data)
        all_kpis = calculator.calculate_all_kpis()
        
        expected_kpis = [
            'total_employees', 'avg_satisfaction', 'avg_performance',
            'sprint_velocity', 'innovation_index', 'crunch_impact_score'  # ← Bon nom
        ]
        
        for kpi in expected_kpis:
            assert kpi in all_kpis
            assert isinstance(all_kpis[kpi], (int, float))

def test_gaming_data_loader():
    """Test DataLoader gaming"""
    loader = DataLoader()
    
    # Test chargement données
    data = loader.load_sample_data()
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0
    
    # Test colonnes gaming obligatoires
    required_columns = ['employee_id', 'department', 'satisfaction_score']
    for col in required_columns:
        assert col in data.columns
