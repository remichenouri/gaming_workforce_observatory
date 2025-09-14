"""
Gaming Workforce Observatory - Talent Pipeline Analyzer
Prédiction et optimisation du pipeline de talents gaming
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class GamingTalentPipelineAnalyzer:
    """Analyseur de pipeline de talents gaming avec prédictions ML"""
    
    def __init__(self):
        self.hiring_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.success_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        
        # Métriques pipeline gaming
        self.pipeline_stages = {
            'sourcing': {'conversion_rate': 0.25, 'avg_days': 7},
            'screening': {'conversion_rate': 0.40, 'avg_days': 5}, 
            'technical_interview': {'conversion_rate': 0.60, 'avg_days': 10},
            'cultural_fit': {'conversion_rate': 0.80, 'avg_days': 3},
            'offer': {'conversion_rate': 0.85, 'avg_days': 5},
            'onboarding': {'conversion_rate': 0.95, 'avg_days': 14}
        }
        
        # Départements gaming et leurs spécificités
        self.gaming_departments = {
            'Programming': {
                'skills_required': ['C++', 'C#', 'Unity', 'Unreal Engine'],
                'avg_time_to_hire': 45,
                'difficulty_score': 0.8,
                'market_competition': 0.9
            },
            'Game Design': {
                'skills_required': ['Game Mechanics', 'Level Design', 'Balancing'],
                'avg_time_to_hire': 35,
                'difficulty_score': 0.6,
                'market_competition': 0.7
            },
            'Art & Animation': {
                'skills_required': ['Maya', 'Blender', '3D Modeling', 'Animation'],
                'avg_time_to_hire': 40,
                'difficulty_score': 0.7,
                'market_competition': 0.8
            },
            'Quality Assurance': {
                'skills_required': ['Test Planning', 'Bug Tracking', 'Automation'],
                'avg_time_to_hire': 25,
                'difficulty_score': 0.4,
                'market_competition': 0.5
            }
        }
    
    @st.cache_data(ttl=3600)
    def analyze_talent_pipeline(_self, hiring_data: pd.DataFrame, 
                               current_needs: Dict[str, int]) -> Dict[str, Any]:
        """Analyse complète du pipeline de talents gaming"""
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'current_pipeline_health': {},
            'hiring_predictions': {},
            'bottleneck_analysis': {},
            'recommendations': [],
            'talent_forecast': {}
        }
        
        try:
            # Analyse de la santé actuelle du pipeline
            pipeline_health = _self._analyze_pipeline_health(hiring_data)
            analysis_results['current_pipeline_health'] = pipeline_health
            
            # Prédictions de recrutement
            hiring_predictions = _self._predict_hiring_success(hiring_data, current_needs)
            analysis_results['hiring_predictions'] = hiring_predictions
            
            # Analyse des goulots d'étranglement
            bottlenecks = _self._identify_bottlenecks(hiring_data)
            analysis_results['bottleneck_analysis'] = bottlenecks
            
            # Prévisions de talents
            talent_forecast = _self._forecast_talent_needs(current_needs, hiring_data)
            analysis_results['talent_forecast'] = talent_forecast
            
            # Génération de recommandations
            recommendations = _self._generate_pipeline_recommendations(
                pipeline_health, bottlenecks, hiring_predictions
            )
            analysis_results['recommendations'] = recommendations
            
            logger.info("Talent pipeline analysis completed successfully")
            
        except Exception as e:
            analysis_results['status'] = 'error'
            analysis_results['message'] = str(e)
            logger.error(f"Talent pipeline analysis failed: {e}")
        
        return analysis_results
    
    def _analyze_pipeline_health(self, hiring_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyse la santé globale du pipeline de recrutement"""
        
        health_metrics = {
            'overall_health_score': 0,
            'stage_performance': {},
            'conversion_rates': {},
            'time_to_hire': {},
            'department_health': {}
        }
        
        if hiring_data.empty:
            return health_metrics
        
        # Analyse par étape du pipeline
        for stage, benchmarks in self.pipeline_stages.items():
            if f'{stage}_conversion' in hiring_data.columns:
                actual_conversion = hiring_data[f'{stage}_conversion'].mean()
                benchmark_conversion = benchmarks['conversion_rate']
                
                performance_score = min(100, (actual_conversion / benchmark_conversion) * 100)
                
                health_metrics['stage_performance'][stage] = {
                    'actual_conversion': actual_conversion,
                    'benchmark_conversion': benchmark_conversion,
                    'performance_score': performance_score,
                    'status': 'good' if performance_score >= 90 else 'needs_improvement'
                }
        
        # Temps moyen de recrutement
        if 'time_to_hire' in hiring_data.columns:
            avg_time = hiring_data['time_to_hire'].mean()
            health_metrics['time_to_hire'] = {
                'average_days': avg_time,
                'benchmark_days': 35,  # Benchmark industrie gaming
                'performance': 'good' if avg_time <= 40 else 'slow'
            }
        
        # Analyse par département
        if 'department' in hiring_data.columns:
            for dept in hiring_data['department'].unique():
                dept_data = hiring_data[hiring_data['department'] == dept]
                
                if not dept_data.empty:
                    success_rate = dept_data.get('hired', pd.Series([0])).mean()
                    avg_time = dept_data.get('time_to_hire', pd.Series([35])).mean()
                    
                    dept_benchmark = self.gaming_departments.get(dept, {})
                    benchmark_time = dept_benchmark.get('avg_time_to_hire', 35)
                    
                    health_metrics['department_health'][dept] = {
                        'success_rate': success_rate,
                        'avg_time_to_hire': avg_time,
                        'benchmark_time': benchmark_time,
                        'time_performance': 'good' if avg_time <= benchmark_time else 'slow',
                        'candidates_processed': len(dept_data)
                    }
        
        # Score de santé global
        stage_scores = [perf['performance_score'] 
                       for perf in health_metrics['stage_performance'].values()]
        if stage_scores:
            health_metrics['overall_health_score'] = np.mean(stage_scores)
        
        return health_metrics
    
    def _predict_hiring_success(self, hiring_data: pd.DataFrame, 
                               current_needs: Dict[str, int]) -> Dict[str, Any]:
        """Prédit le succès de recrutement basé sur les besoins actuels"""
        
        predictions = {
            'department_predictions': {},
            'timeline_predictions': {},
            'success_probability': {},
            'resource_requirements': {}
        }
        
        # Prédictions par département
        for dept, needed_count in current_needs.items():
            dept_data = hiring_data[hiring_data['department'] == dept] if 'department' in hiring_data.columns else hiring_data
            
            if len(dept_data) > 10:  # Assez de données pour prédiction
                # Calcul du taux de succès historique
                historical_success = dept_data.get('hired', pd.Series([0])).mean()
                
                # Estimation du temps basé sur l'historique
                avg_time_to_hire = dept_data.get('time_to_hire', pd.Series([35])).mean()
                
                # Prédiction du nombre de candidats nécessaires
                candidates_needed = int(needed_count / max(0.1, historical_success)) if historical_success > 0 else needed_count * 5
                
                # Estimation du temps total
                estimated_timeline = avg_time_to_hire * 1.2  # Buffer de 20%
                
                predictions['department_predictions'][dept] = {
                    'positions_needed': needed_count,
                    'candidates_to_source': candidates_needed,
                    'historical_success_rate': historical_success,
                    'estimated_timeline_days': estimated_timeline,
                    'confidence_level': min(100, len(dept_data) / 20 * 100)  # Plus de données = plus de confiance
                }
            
            else:
                # Utiliser benchmarks industrie
                dept_info = self.gaming_departments.get(dept, {})
                difficulty = dept_info.get('difficulty_score', 0.6)
                
                predictions['department_predictions'][dept] = {
                    'positions_needed': needed_count,
                    'candidates_to_source': int(needed_count / (1 - difficulty)),
                    'historical_success_rate': 1 - difficulty,
                    'estimated_timeline_days': dept_info.get('avg_time_to_hire', 35),
                    'confidence_level': 30  # Faible confiance avec peu de données
                }
        
        # Prédiction de timeline globale
        max_timeline = max([pred['estimated_timeline_days'] 
                           for pred in predictions['department_predictions'].values()])
        
        predictions['timeline_predictions'] = {
            'estimated_completion_days': max_timeline,
            'completion_date': (datetime.now() + timedelta(days=max_timeline)).isoformat(),
            'parallel_hiring_benefit': max_timeline * 0.3  # 30% réduction si parallélisation
        }
        
        return predictions
    
    def _identify_bottlenecks(self, hiring_data: pd.DataFrame) -> Dict[str, Any]:
        """Identifie les goulots d'étranglement dans le pipeline"""
        
        bottlenecks = {
            'stage_bottlenecks': {},
            'time_bottlenecks': {},
            'capacity_issues': {},
            'improvement_opportunities': []
        }
        
        # Analyse des goulots par étape
        for stage, benchmarks in self.pipeline_stages.items():
            stage_column = f'{stage}_conversion'
            time_column = f'{stage}_time'
            
            if stage_column in hiring_data.columns:
                actual_conversion = hiring_data[stage_column].mean()
                benchmark_conversion = benchmarks['conversion_rate']
                
                if actual_conversion < benchmark_conversion * 0.8:  # Plus de 20% sous benchmark
                    bottlenecks['stage_bottlenecks'][stage] = {
                        'severity': 'high' if actual_conversion < benchmark_conversion * 0.6 else 'medium',
                        'actual_rate': actual_conversion,
                        'benchmark_rate': benchmark_conversion,
                        'impact': f"Losing {(benchmark_conversion - actual_conversion) * 100:.1f}% more candidates than expected"
                    }
            
            # Analyse du temps par étape
            if time_column in hiring_data.columns:
                actual_time = hiring_data[time_column].mean()
                benchmark_time = benchmarks['avg_days']
                
                if actual_time > benchmark_time * 1.5:  # 50% plus lent que benchmark
                    bottlenecks['time_bottlenecks'][stage] = {
                        'severity': 'high' if actual_time > benchmark_time * 2 else 'medium',
                        'actual_days': actual_time,
                        'benchmark_days': benchmark_time,
                        'delay': actual_time - benchmark_time
                    }
        
        # Opportunités d'amélioration
        if bottlenecks['stage_bottlenecks']:
            most_problematic_stage = max(
                bottlenecks['stage_bottlenecks'].keys(),
                key=lambda x: benchmarks['conversion_rate'] - bottlenecks['stage_bottlenecks'][x]['actual_rate']
            )
            
            bottlenecks['improvement_opportunities'].append({
                'priority': 'high',
                'area': most_problematic_stage,
                'description': f'Focus on improving {most_problematic_stage} conversion rate',
                'expected_impact': 'Could improve overall pipeline by 15-25%'
            })
        
        return bottlenecks
    
    def _forecast_talent_needs(self, current_needs: Dict[str, int], 
                              hiring_data: pd.DataFrame) -> Dict[str, Any]:
        """Prévisions des besoins en talents à court et moyen terme"""
        
        forecast = {
            'next_quarter': {},
            'next_year': {},
            'growth_scenarios': {},
            'skill_demand_forecast': {}
        }
        
        # Croissance historique si disponible
        growth_rate = 0.15  # 15% croissance annuelle par défaut gaming
        
        if 'hire_date' in hiring_data.columns:
            # Calcul croissance basée sur historique
            hiring_data['hire_date'] = pd.to_datetime(hiring_data['hire_date'])
            monthly_hires = hiring_data.groupby(hiring_data['hire_date'].dt.to_period('M')).size()
            
            if len(monthly_hires) > 6:  # Au moins 6 mois de données
                # Tendance linéaire simple
                x = np.arange(len(monthly_hires))
                y = monthly_hires.values
                slope = np.polyfit(x, y, 1)[0]
                growth_rate = max(0, slope / monthly_hires.mean() * 12)  # Annualisé
        
        # Prévisions par département
        for dept, current_need in current_needs.items():
            base_team_size = current_need * 3  # Estimation équipe actuelle
            
            # Prévision Q1
            q1_growth = base_team_size * (growth_rate / 4)
            forecast['next_quarter'][dept] = {
                'additional_hires': max(0, int(q1_growth)),
                'total_team_size_target': base_team_size + q1_growth
            }
            
            # Prévision annuelle
            annual_growth = base_team_size * growth_rate
            forecast['next_year'][dept] = {
                'additional_hires': max(0, int(annual_growth)),
                'total_team_size_target': base_team_size + annual_growth
            }
        
        # Scénarios de croissance
        for scenario, multiplier in [('conservative', 0.5), ('optimistic', 1.5), ('aggressive', 2.0)]:
            forecast['growth_scenarios'][scenario] = {}
            
            for dept, yearly_forecast in forecast['next_year'].items():
                adjusted_hires = int(yearly_forecast['additional_hires'] * multiplier)
                forecast['growth_scenarios'][scenario][dept] = adjusted_hires
        
        return forecast
    
    def _generate_pipeline_recommendations(self, health_data: Dict[str, Any],
                                         bottlenecks: Dict[str, Any],
                                         predictions: Dict[str, Any]) -> List[Dict[str, str]]:
        """Génère des recommandations pour optimiser le pipeline"""
        
        recommendations = []
        
        # Recommandations basées sur la santé du pipeline
        overall_score = health_data.get('overall_health_score', 0)
        
        if overall_score < 70:
            recommendations.append({
                'category': 'Pipeline Health',
                'priority': 'High',
                'title': 'Amélioration générale du pipeline',
                'description': f'Score de santé actuel: {overall_score:.1f}%. Pipeline nécessite optimisation.',
                'action': 'Audit complet des processus de recrutement',
                'expected_impact': 'Amélioration 20-30% efficacité globale',
                'timeline': '6-8 semaines'
            })
        
        # Recommandations basées sur les goulots d'étranglement
        stage_bottlenecks = bottlenecks.get('stage_bottlenecks', {})
        
        for stage, bottleneck_info in stage_bottlenecks.items():
            if bottleneck_info['severity'] == 'high':
                recommendations.append({
                    'category': 'Bottleneck Resolution',
                    'priority': 'Critical',
                    'title': f'Résoudre goulot étape {stage}',
                    'description': f'Taux conversion {bottleneck_info["actual_rate"]:.1%} vs benchmark {bottleneck_info["benchmark_rate"]:.1%}',
                    'action': f'Formation équipes, révision processus {stage}',
                    'expected_impact': 'Gain 15-25% candidats qualifiés',
                    'timeline': '3-4 semaines'
                })
        
        # Recommandations basées sur les prédictions
        low_confidence_depts = [
            dept for dept, pred in predictions.get('department_predictions', {}).items()
            if pred.get('confidence_level', 100) < 50
        ]
        
        if low_confidence_depts:
            recommendations.append({
                'category': 'Data Quality',
                'priority': 'Medium',
                'title': 'Améliorer collecte données recrutement',
                'description': f'Données insuffisantes pour {", ".join(low_confidence_depts)}',
                'action': 'Mettre en place tracking détaillé candidats',
                'expected_impact': 'Prédictions plus précises',
                'timeline': '2-3 semaines'
            })
        
        # Recommandations proactives
        high_difficulty_depts = [
            dept for dept, info in self.gaming_departments.items()
            if info.get('difficulty_score', 0) > 0.7
        ]
        
        if high_difficulty_depts:
            recommendations.append({
                'category': 'Talent Sourcing',
                'priority': 'Medium',
                'title': 'Stratégie sourcing départements difficiles',
                'description': f'Départements {", ".join(high_difficulty_depts)} nécessitent approche spécialisée',
                'action': 'Partenariats écoles spécialisées, head-hunting',
                'expected_impact': 'Réduction 20% temps recrutement',
                'timeline': '4-6 semaines'
            })
        
        return recommendations
    
    def render_talent_pipeline_dashboard(self, analysis_results: Dict[str, Any]):
        """Dashboard Streamlit pour l'analyse du pipeline de talents"""
        
        st.markdown("## 🎯 Talent Pipeline Analytics")
        st.markdown("*Strategic talent acquisition insights for gaming teams*")
        
        if 'status' in analysis_results and analysis_results['status'] == 'error':
            st.error(f"Analysis failed: {analysis_results.get('message', 'Unknown error')}")
            return
        
        # Métriques de santé du pipeline
        health_data = analysis_results.get('current_pipeline_health', {})
        
        if health_data:
            st.markdown("### 📊 Pipeline Health Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                overall_score = health_data.get('overall_health_score', 0)
                status_color = "🟢" if overall_score >= 80 else "🟡" if overall_score >= 60 else "🔴"
                st.metric(
                    f"{status_color} Overall Health",
                    f"{overall_score:.1f}%"
                )
            
            with col2:
                time_data = health_data.get('time_to_hire', {})
                avg_days = time_data.get('average_days', 0)
                st.metric(
                    "⏰ Avg Time to Hire",
                    f"{avg_days:.0f} days",
                    delta=f"{avg_days - 35:.0f} vs benchmark"
                )
            
            with col3:
                stage_perf = health_data.get('stage_performance', {})
                good_stages = sum(1 for s in stage_perf.values() if s.get('status') == 'good')
                total_stages = len(stage_perf)
                st.metric(
                    "✅ Stages Performing Well",
                    f"{good_stages}/{total_stages}"
                )
            
            with col4:
                dept_health = health_data.get('department_health', {})
                total_candidates = sum(d.get('candidates_processed', 0) for d in dept_health.values())
                st.metric(
                    "👥 Candidates Processed",
                    f"{total_candidates:,}"
                )
        
        # Prédictions de recrutement
        predictions = analysis_results.get('hiring_predictions', {})
        
        if predictions.get('department_predictions'):
            st.markdown("### 🔮 Hiring Predictions")
            
            pred_data = []
            for dept, pred in predictions['department_predictions'].items():
                pred_data.append({
                    'Department': dept,
                    'Positions Needed': pred.get('positions_needed', 0),
                    'Candidates to Source': pred.get('candidates_to_source', 0),
                    'Success Rate': f"{pred.get('historical_success_rate', 0):.1%}",
                    'Timeline (Days)': f"{pred.get('estimated_timeline_days', 0):.0f}
