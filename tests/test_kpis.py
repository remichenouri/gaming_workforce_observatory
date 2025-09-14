"""
Gaming Workforce Observatory - KPIs Tests
Tests complets pour les KPIs spécifiques à l'industrie gaming
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestGamingKPICalculator:
    """Tests pour le calculateur de KPIs gaming"""
    
    @pytest.fixture
    def sample_gaming_workforce_data(self):
        """Données d'exemple pour les tests KPI gaming"""
        return pd.DataFrame({
            'employee_id': range(1, 21),
            'name': [f'GameDev_{i}' for i in range(1, 21)],
            'department': ['Programming', 'Art', 'Game Design', 'QA', 'Marketing'] * 4,
            'level': ['Junior', 'Mid', 'Senior', 'Lead'] * 5,
            'salary': [45000, 65000, 95000, 120000] * 5,
            'satisfaction_score': [8.5, 7.2, 9.1, 6.8, 8.0, 7.5, 8.8, 6.5, 9.2, 7.8] * 2,
            'performance_score': [4.2, 3.8, 4.5, 4.0, 4.1, 3.9, 4.3, 3.7, 4.6, 4.0] * 2,
            'years_experience': [2, 4, 7, 10, 6, 3, 8, 1, 9, 5] * 2,
            'hire_date': pd.date_range('2020-01-01', periods=20, freq='ME'),
            'sprint_velocity': [35, 0, 42, 0, 0, 38, 0, 41, 0, 0] * 2,
            'bug_fix_rate': [0, 0, 0, 88, 0, 0, 0, 0, 92, 0] * 2,
            'innovation_index': [82, 75, 90, 68, 71, 85, 78, 88, 65, 73] * 2,
            'burnout_risk': [0.2, 0.3, 0.1, 0.6, 0.25, 0.15, 0.4, 0.1, 0.55, 0.3] * 2,
            'crunch_hours_last_month': [45, 30, 25, 65, 40, 35, 70, 20, 60, 50] * 2,
            'team_collaboration_score': [8.5, 7.0, 9.0, 6.5, 8.2, 7.8, 8.9, 6.2, 9.1, 7.5] * 2,
            'last_promotion': pd.date_range('2022-01-01', periods=20, freq='ME')
        })
    
    @pytest.fixture
    def kpi_calculator(self, sample_gaming_workforce_data):
        """Instance du calculateur KPI gaming"""
        from src.data.kpis import GameKPICalculator
        return GameKPICalculator(sample_gaming_workforce_data)
    
    def test_calculate_gaming_satisfaction(self, kpi_calculator, sample_gaming_workforce_data):
        """Test du calcul de satisfaction gaming"""
        satisfaction = kpi_calculator.calculate_gaming_satisfaction()
        
        # Vérifications gaming-spécifiques
        assert isinstance(satisfaction, float)
        assert 1 <= satisfaction <= 10, "Gaming satisfaction doit être entre 1 et 10"
        
        expected_satisfaction = sample_gaming_workforce_data['satisfaction_score'].mean()
        assert abs(satisfaction - expected_satisfaction) < 0.1
    
    def test_calculate_sprint_velocity(self, kpi_calculator):
        """Test du calcul de vélocité de sprint gaming"""
        velocity = kpi_calculator.calculate_sprint_velocity()
        
        # Vérifications gaming development
        assert isinstance(velocity, float)
        assert velocity >= 0, "Sprint velocity ne peut pas être négative"
        
        # Seuls Programming et Game Design ont sprint velocity
        expected_velocity = kpi_calculator.data[
            kpi_calculator.data['sprint_velocity'] > 0
        ]['sprint_velocity'].mean()
        
        assert abs(velocity - expected_velocity) < 0.1
    
    def test_calculate_bug_fix_rate(self, kpi_calculator):
        """Test du calcul du taux de correction de bugs gaming"""
        bug_rate = kpi_calculator.calculate_bug_fix_rate()
        
        # Vérifications gaming QA
        assert isinstance(bug_rate, float)
        assert 0 <= bug_rate <= 100, "Bug fix rate doit être entre 0 et 100%"
        
        # Seule l'équipe QA a bug fix rate
        qa_data = kpi_calculator.data[kpi_calculator.data['bug_fix_rate'] > 0]
        if not qa_data.empty:
            expected_rate = qa_data['bug_fix_rate'].mean()
            assert abs(bug_rate - expected_rate) < 0.1
    
    def test_calculate_innovation_index(self, kpi_calculator):
        """Test du calcul de l'index d'innovation gaming"""
        innovation = kpi_calculator.calculate_innovation_index()
        
        # Vérifications gaming creativity
        assert isinstance(innovation, float)
        assert 0 <= innovation <= 100, "Innovation index doit être entre 0 et 100"
        
        expected_innovation = kpi_calculator.data['innovation_index'].mean()
        assert abs(innovation - expected_innovation) < 0.1
    
    def test_calculate_crunch_impact_score(self, kpi_calculator):
        """Test du calcul de l'impact des périodes de crunch gaming"""
        crunch_impact = kpi_calculator.calculate_crunch_impact_score()
        
        # Vérifications gaming work-life balance
        assert isinstance(crunch_impact, float)
        assert 0 <= crunch_impact <= 10, "Crunch impact score doit être entre 0 et 10"
        
        # Score plus élevé = impact plus important (négatif)
        high_crunch_employees = kpi_calculator.data[
            kpi_calculator.data['crunch_hours_last_month'] > 60
        ]
        if not high_crunch_employees.empty:
            assert crunch_impact > 3.0, "High crunch hours should result in high impact score"
    
    def test_calculate_team_synergy_score(self, kpi_calculator):
        """Test du calcul du score de synergie d'équipe gaming"""
        synergy = kpi_calculator.calculate_team_synergy_score()
        
        # Vérifications gaming collaboration
        assert isinstance(synergy, float)
        assert 1 <= synergy <= 10, "Team synergy score doit être entre 1 et 10"
        
        expected_synergy = kpi_calculator.data['team_collaboration_score'].mean()
        assert abs(synergy - expected_synergy) < 0.1
    
    def test_calculate_retention_risk(self, kpi_calculator):
        """Test du calcul du risque de rétention gaming"""
        retention_risk = kpi_calculator.calculate_retention_risk()
        
        # Vérifications gaming talent retention
        assert isinstance(retention_risk, float)
        assert 0 <= retention_risk <= 1, "Retention risk doit être entre 0 et 1"
        
        # Basé sur burnout_risk dans les données
        expected_risk = kpi_calculator.data['burnout_risk'].mean()
        assert abs(retention_risk - expected_risk) < 0.1
    
    def test_calculate_performance_distribution(self, kpi_calculator):
        """Test du calcul de distribution des performances gaming"""
        distribution = kpi_calculator.calculate_performance_distribution()
        
        # Vérifications gaming performance analytics
        assert isinstance(distribution, dict)
        
        gaming_levels = ['Junior', 'Mid', 'Senior', 'Lead']
        for level in gaming_levels:
            if level in distribution:
                level_data = distribution[level]
                assert 'count' in level_data
                assert 'avg_performance' in level_data
                assert 'avg_salary' in level_data
                assert 1 <= level_data['avg_performance'] <= 5
    
    def test_calculate_department_kpis(self, kpi_calculator):
        """Test du calcul des KPIs par département gaming"""
        dept_kpis = kpi_calculator.calculate_department_kpis()
        
        # Vérifications gaming departments
        assert isinstance(dept_kpis, dict)
        
        gaming_departments = ['Programming', 'Art', 'Game Design', 'QA', 'Marketing']
        for dept in gaming_departments:
            if dept in dept_kpis:
                dept_data = dept_kpis[dept]
                
                # KPIs communs
                assert 'avg_satisfaction' in dept_data
                assert 'avg_performance' in dept_data
                assert 'employee_count' in dept_data
                
                # KPIs spécifiques gaming
                if dept == 'Programming':
                    assert 'avg_sprint_velocity' in dept_data
                elif dept == 'QA':
                    assert 'avg_bug_fix_rate' in dept_data
    
    def test_gaming_industry_benchmarks(self, kpi_calculator):
        """Test des benchmarks de l'industrie gaming"""
        benchmarks = kpi_calculator.get_gaming_industry_benchmarks()
        
        # Vérifications gaming industry standards
        assert isinstance(benchmarks, dict)
        
        expected_benchmarks = [
            'industry_avg_satisfaction',
            'industry_sprint_velocity',
            'industry_bug_fix_rate',
            'industry_retention_rate',
            'industry_innovation_index'
        ]
        
        for benchmark in expected_benchmarks:
            assert benchmark in benchmarks
            assert isinstance(benchmarks[benchmark], (int, float))
    
    def test_calculate_all_kpis(self, kpi_calculator):
        """Test du calcul de tous les KPIs gaming"""
        all_kpis = kpi_calculator.calculate_all_kpis()
        
        # Vérifications gaming comprehensive analytics
        assert isinstance(all_kpis, dict)
        
        # KPIs gaming essentiels
        essential_kpis = [
            'avg_satisfaction',
            'avg_performance',
            'sprint_velocity',
            'bug_fix_rate',
            'innovation_index',
            'crunch_impact_score',
            'team_synergy_score',
            'retention_risk',
            'total_employees'
        ]
        
        for kpi in essential_kpis:
            assert kpi in all_kpis, f"Missing essential gaming KPI: {kpi}"
    
    def test_kpi_thresholds_gaming(self, kpi_calculator):
        """Test des seuils KPI spécifiques au gaming"""
        kpis = kpi_calculator.calculate_all_kpis()
        thresholds = kpi_calculator.get_gaming_thresholds()
        
        # Vérifications gaming thresholds
        gaming_thresholds = {
            'satisfaction_critical': 6.0,
            'satisfaction_good': 8.0,
            'sprint_velocity_target': 40.0,
            'bug_fix_rate_target': 85.0,
            'innovation_index_target': 75.0,
            'crunch_impact_warning': 5.0,
            'team_synergy_target': 8.0,
            'retention_risk_critical': 0.7
        }
        
        for threshold_name, threshold_value in gaming_thresholds.items():
            assert threshold_name in thresholds
            assert isinstance(thresholds[threshold_name], (int, float))
    
    def test_gaming_alerts_generation(self, kpi_calculator):
        """Test de génération d'alertes gaming"""
        alerts = kpi_calculator.generate_gaming_alerts()
        
        # Vérifications gaming alerts
        assert isinstance(alerts, list)
        
        for alert in alerts:
            assert 'type' in alert
            assert 'severity' in alert
            assert 'message' in alert
            assert 'gaming_context' in alert
            
            # Types d'alertes gaming
            gaming_alert_types = [
                'low_satisfaction',
                'high_turnover_risk', 
                'excessive_crunch',
                'low_sprint_velocity',
                'poor_bug_fix_rate',
                'low_innovation',
                'poor_team_synergy'
            ]
            
            assert alert['type'] in gaming_alert_types
    
    def test_gaming_trends_analysis(self, kpi_calculator, sample_gaming_workforce_data):
        """Test de l'analyse des tendances gaming"""
        # Ajouter des données historiques simulées
        historical_data = sample_gaming_workforce_data.copy()
        historical_data['month'] = pd.date_range('2024-01-01', periods=len(historical_data), freq='ME')
        
        trends = kpi_calculator.analyze_gaming_trends(historical_data)
        
        # Vérifications gaming trends
        assert isinstance(trends, dict)
        
        gaming_trend_metrics = [
            'satisfaction_trend',
            'velocity_trend',
            'innovation_trend',
            'turnover_risk_trend'
        ]
        
        for trend_metric in gaming_trend_metrics:
            if trend_metric in trends:
                trend_data = trends[trend_metric]
                assert 'direction' in trend_data  # 'up', 'down', 'stable'
                assert 'change_rate' in trend_data
                assert 'gaming_significance' in trend_data
    
    def test_gaming_recommendations_engine(self, kpi_calculator):
        """Test du moteur de recommandations gaming"""
        recommendations = kpi_calculator.generate_gaming_recommendations()
        
        # Vérifications gaming recommendations
        assert isinstance(recommendations, list)
        
        for recommendation in recommendations:
            assert 'category' in recommendation
            assert 'priority' in recommendation
            assert 'action' in recommendation
            assert 'gaming_impact' in recommendation
            
            # Catégories de recommandations gaming
            gaming_categories = [
                'talent_retention',
                'performance_optimization',
                'crunch_management',
                'team_collaboration',
                'innovation_enhancement',
                'quality_improvement'
            ]
            
            assert recommendation['category'] in gaming_categories
    
    def test_gaming_kpi_validation(self, kpi_calculator):
        """Test de validation des KPIs gaming"""
        validation_result = kpi_calculator.validate_gaming_kpis()
        
        # Vérifications gaming validation
        assert isinstance(validation_result, dict)
        assert 'is_valid' in validation_result
        assert 'issues' in validation_result
        assert 'gaming_compliance' in validation_result
        
        # Vérifier les problèmes de validation gaming
        if validation_result['issues']:
            for issue in validation_result['issues']:
                assert 'type' in issue
                assert 'severity' in issue
                assert 'gaming_context' in issue

class TestGamingKPIIntegration:
    """Tests d'intégration pour les KPIs gaming"""
    
    def test_kpi_calculator_with_real_data(self):
        """Test avec des données réelles gaming"""
        # Simuler des données plus réalistes
        real_gaming_data = pd.DataFrame({
            'employee_id': range(1, 101),
            'department': np.random.choice(['Programming', 'Art', 'Game Design', 'QA', 'Marketing'], 100),
            'level': np.random.choice(['Junior', 'Mid', 'Senior', 'Lead'], 100),
            'satisfaction_score': np.random.normal(7.5, 1.2, 100).clip(1, 10),
            'performance_score': np.random.normal(4.0, 0.5, 100).clip(1, 5),
            'sprint_velocity' : np.where(
            pd.Series(np.random.choice(['Programming', 'Game Design', 'Art', 'QA', 'Marketing'], 100)).isin(['Programming', 'Game Design']),  # ← VIRGULE AJOUTÉE
            np.random.normal(40, 8, 100).clip(10, 80),
            0
            ),
            'bug_fix_rate': np.where(
                np.random.choice(['Programming', 'Art', 'Game Design', 'QA', 'Marketing'], 100) == 'QA',
                np.random.normal(85, 10, 100).clip(50, 100),
                0
            ),
            'innovation_index': np.random.normal(75, 15, 100).clip(0, 100),
            'burnout_risk': np.random.beta(2, 5, 100),  # Distribution réaliste
            'crunch_hours_last_month': np.random.gamma(2, 20, 100).clip(0, 120)
        })
        
        from src.data.kpis import GameKPICalculator
        calculator = GameKPICalculator(real_gaming_data)
        
        # Test avec données volumineuses
        kpis = calculator.calculate_all_kpis()
        
        # Vérifications de performance
        assert len(kpis) > 0
        assert kpis['total_employees'] == 100
        assert isinstance(kpis['avg_satisfaction'], float)
    
    @pytest.mark.slow
    def test_kpi_performance_large_dataset(self):
        """Test de performance avec un grand dataset gaming"""
        import time
        
        # Créer un grand dataset gaming
        large_gaming_dataset = pd.DataFrame({
            'employee_id': range(1, 10001),
            'department': np.random.choice(['Programming', 'Art', 'Game Design', 'QA', 'Marketing'], 10000),
            'satisfaction_score': np.random.uniform(6.0, 9.5, 10000),
            'performance_score': np.random.uniform(3.0, 5.0, 10000),
            'innovation_index': np.random.uniform(50, 95, 10000)
        })
        
        from src.data.kpis import GameKPICalculator
        calculator = GameKPICalculator(large_gaming_dataset)
        
        start_time = time.time()
        kpis = calculator.calculate_all_kpis()
        calculation_time = time.time() - start_time
        
        # Les calculs doivent être rapides même avec 10k employés
        assert calculation_time < 5.0, f"KPI calculation too slow: {calculation_time}s"
        assert kpis['total_employees'] == 10000
    
    def test_kpi_edge_cases_gaming(self):
        """Test des cas limites gaming"""
        # Dataset avec des valeurs extrêmes
        edge_case_data = pd.DataFrame({
            'employee_id': [1, 2, 3, 4],
            'department': ['Programming', 'QA', 'Art', 'Game Design'],
            'satisfaction_score': [1.0, 10.0, 5.5, 7.8],  # Min, max, et valeurs normales
            'performance_score': [1.0, 5.0, 3.0, 4.0],
            'sprint_velocity': [100, 0, 0, 80],  # Très haute vélocité
            'bug_fix_rate': [0, 100, 0, 0],  # Taux parfait
            'innovation_index': [0, 100, 50, 75],  # Min, max
            'burnout_risk': [0.0, 1.0, 0.3, 0.5]  # Min, max risk
        })
        
        from src.data.kpis import GameKPICalculator
        calculator = GameKPICalculator(edge_case_data)
        
        # Doit gérer les cas extrêmes sans erreur
        kpis = calculator.calculate_all_kpis()
        
        assert isinstance(kpis, dict)
        assert kpis['total_employees'] == 4
        assert 1 <= kpis['avg_satisfaction'] <= 10
        assert 1 <= kpis['avg_performance'] <= 5

if __name__ == "__main__":
    pytest.main([__file__])
