"""
Gaming Workforce Observatory - Crunch Analyzer
Détection et analyse des périodes de surcharge (crunch) dans le développement gaming
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any, Optional, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

class CrunchAnalyzer:
    """Analyseur de crunch gaming avec détection automatique et alertes"""
    
    def __init__(self):
        self.crunch_thresholds = {
            'hours_per_week': 50,
            'consecutive_weeks': 3,
            'satisfaction_drop': 1.0,
            'performance_impact': 0.15
        }
        
        self.project_phases = {
            'pre_production': {'base_hours': 40, 'crunch_multiplier': 1.1},
            'production': {'base_hours': 42, 'crunch_multiplier': 1.3},
            'alpha': {'base_hours': 45, 'crunch_multiplier': 1.5},
            'beta': {'base_hours': 48, 'crunch_multiplier': 1.7},
            'gold_master': {'base_hours': 52, 'crunch_multiplier': 2.0},
            'post_launch': {'base_hours': 38, 'crunch_multiplier': 1.2}
        }
    
    @st.cache_data(ttl=3600)
    def analyze_crunch_patterns(_self, employee_data: pd.DataFrame, 
                               timesheet_data: pd.DataFrame = None) -> Dict[str, Any]:
        """Analyse complète des patterns de crunch gaming"""
        
        if employee_data.empty:
            return {'status': 'no_data', 'analysis': {}}
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'total_employees_analyzed': len(employee_data),
            'crunch_detection': _self._detect_crunch_periods(employee_data, timesheet_data),
            'department_analysis': _self._analyze_crunch_by_department(employee_data),
            'project_phase_impact': _self._analyze_project_phase_crunch(employee_data),
            'health_metrics': _self._calculate_crunch_health_metrics(employee_data),
            'predictions': _self._predict_crunch_risk(employee_data),
            'recommendations': _self._generate_crunch_recommendations(employee_data)
        }
        
        logger.info(f"Crunch analysis completed for {len(employee_data)} employees")
        return analysis_results
    
    def _detect_crunch_periods(self, employee_data: pd.DataFrame, 
                              timesheet_data: pd.DataFrame = None) -> Dict[str, Any]:
        """Détecte les périodes de crunch actuelles et historiques"""
        
        crunch_detection = {
            'current_crunch_employees': [],
            'at_risk_employees': [],
            'historical_patterns': {},
            'severity_levels': {}
        }
        
        # Analyse des heures travaillées
        if 'weekly_hours' in employee_data.columns:
            # Employés en crunch actuel
            current_crunch = employee_data[
                employee_data['weekly_hours'] > self.crunch_thresholds['hours_per_week']
            ]
            
            crunch_detection['current_crunch_employees'] = [
                {
                    'employee_id': row['employee_id'],
                    'name': row.get('name', f"Employee {row['employee_id']}"),
                    'department': row.get('department', 'Unknown'),
                    'weekly_hours': row['weekly_hours'],
                    'weeks_in_crunch': row.get('consecutive_crunch_weeks', 1),
                    'severity': self._calculate_crunch_severity(row)
                }
                for _, row in current_crunch.iterrows()
            ]
            
            # Employés à risque (proche du seuil)
            at_risk_threshold = self.crunch_thresholds['hours_per_week'] - 5
            at_risk = employee_data[
                (employee_data['weekly_hours'] > at_risk_threshold) &
                (employee_data['weekly_hours'] <= self.crunch_thresholds['hours_per_week'])
            ]
            
            crunch_detection['at_risk_employees'] = [
                {
                    'employee_id': row['employee_id'],
                    'name': row.get('name', f"Employee {row['employee_id']}"),
                    'department': row.get('department', 'Unknown'),
                    'weekly_hours': row['weekly_hours'],
                    'risk_score': self._calculate_risk_score(row)
                }
                for _, row in at_risk.iterrows()
            ]
        
        # Analyse par niveaux de sévérité
        if crunch_detection['current_crunch_employees']:
            severity_counts = {}
            for emp in crunch_detection['current_crunch_employees']:
                severity = emp['severity']
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            crunch_detection['severity_levels'] = severity_counts
        
        return crunch_detection
    
    def _calculate_crunch_severity(self, employee_row: pd.Series) -> str:
        """Calcule la sévérité du crunch pour un employé"""
        hours = employee_row.get('weekly_hours', 40)
        weeks = employee_row.get('consecutive_crunch_weeks', 1)
        satisfaction = employee_row.get('satisfaction_score', 7.0)
        
        # Score de sévérité basé sur plusieurs facteurs
        severity_score = 0
        
        # Impact des heures
        if hours > 60:
            severity_score += 3
        elif hours > 55:
            severity_score += 2
        elif hours > 50:
            severity_score += 1
        
        # Impact de la durée
        if weeks > 8:
            severity_score += 3
        elif weeks > 4:
            severity_score += 2
        elif weeks > 2:
            severity_score += 1
        
        # Impact sur la satisfaction
        if satisfaction < 5:
            severity_score += 2
        elif satisfaction < 6:
            severity_score += 1
        
        # Classification
        if severity_score >= 6:
            return 'Critical'
        elif severity_score >= 4:
            return 'High'
        elif severity_score >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_risk_score(self, employee_row: pd.Series) -> float:
        """Calcule un score de risque de crunch (0-100)"""
        hours = employee_row.get('weekly_hours', 40)
        project_phase = employee_row.get('project_phase', 'production')
        department = employee_row.get('department', 'Programming')
        
        # Score de base selon les heures
        base_score = min(100, (hours / 70) * 100)
        
        # Ajustement selon la phase de projet
        phase_multiplier = self.project_phases.get(project_phase, {}).get('crunch_multiplier', 1.0)
        adjusted_score = base_score * phase_multiplier
        
        # Ajustement selon le département (certains départements plus à risque)
        dept_risk_multipliers = {
            'Programming': 1.2,
            'Quality Assurance': 1.3,
            'Art & Animation': 1.1,
            'Game Design': 1.0,
            'Production': 0.9
        }
        
        dept_multiplier = dept_risk_multipliers.get(department, 1.0)
        final_score = min(100, adjusted_score * dept_multiplier)
        
        return round(final_score, 2)
    
    def _analyze_crunch_by_department(self, employee_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyse du crunch par département gaming"""
        
        if 'department' not in employee_data.columns:
            return {}
        
        dept_analysis = {}
        
        for dept in employee_data['department'].unique():
            dept_data = employee_data[employee_data['department'] == dept]
            
            if 'weekly_hours' in dept_data.columns:
                crunch_employees = dept_data[
                    dept_data['weekly_hours'] > self.crunch_thresholds['hours_per_week']
                ]
                
                dept_analysis[dept] = {
                    'total_employees': len(dept_data),
                    'employees_in_crunch': len(crunch_employees),
                    'crunch_percentage': (len(crunch_employees) / len(dept_data)) * 100,
                    'avg_weekly_hours': dept_data['weekly_hours'].mean(),
                    'max_weekly_hours': dept_data['weekly_hours'].max(),
                    'avg_satisfaction': dept_data.get('satisfaction_score', pd.Series([7.0])).mean(),
                    'productivity_impact': self._calculate_productivity_impact(dept_data)
                }
        
        return dept_analysis
    
    def _analyze_project_phase_crunch(self, employee_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyse l'impact des phases de projet sur le crunch"""
        
        if 'project_phase' not in employee_data.columns:
            return {}
        
        phase_analysis = {}
        
        for phase in employee_data['project_phase'].unique():
            phase_data = employee_data[employee_data['project_phase'] == phase]
            
            if 'weekly_hours' in phase_data.columns:
                expected_hours = self.project_phases.get(phase, {}).get('base_hours', 40)
                
                phase_analysis[phase] = {
                    'employees_count': len(phase_data),
                    'avg_hours': phase_data['weekly_hours'].mean(),
                    'expected_hours': expected_hours,
                    'hours_deviation': phase_data['weekly_hours'].mean() - expected_hours,
                    'crunch_probability': self._calculate_phase_crunch_probability(phase),
                    'burnout_risk': self._calculate_burnout_risk(phase_data)
                }
        
        return phase_analysis
    
    def _calculate_phase_crunch_probability(self, phase: str) -> float:
        """Calcule la probabilité de crunch selon la phase de projet"""
        phase_probabilities = {
            'pre_production': 0.15,
            'production': 0.35,
            'alpha': 0.60,
            'beta': 0.75,
            'gold_master': 0.90,
            'post_launch': 0.25
        }
        
        return phase_probabilities.get(phase, 0.40)
    
    def _calculate_productivity_impact(self, dept_data: pd.DataFrame) -> float:
        """Calcule l'impact du crunch sur la productivité"""
        if 'weekly_hours' not in dept_data.columns:
            return 0.0
        
        # Modèle simplifié : productivité diminue après 45h/semaine
        optimal_hours = 45
        avg_hours = dept_data['weekly_hours'].mean()
        
        if avg_hours <= optimal_hours:
            return 0.0  # Pas d'impact négatif
        
        # Impact négatif croissant après 45h
        impact = min(0.5, (avg_hours - optimal_hours) * 0.02)
        return round(impact, 3)
    
    def _calculate_burnout_risk(self, phase_data: pd.DataFrame) -> str:
        """Évalue le risque de burnout pour une phase"""
        if phase_data.empty:
            return 'Unknown'
        
        avg_hours = phase_data.get('weekly_hours', pd.Series([40])).mean()
        avg_satisfaction = phase_data.get('satisfaction_score', pd.Series([7])).mean()
        
        risk_score = 0
        
        if avg_hours > 55:
            risk_score += 3
        elif avg_hours > 50:
            risk_score += 2
        elif avg_hours > 45:
            risk_score += 1
        
        if avg_satisfaction < 5:
            risk_score += 2
        elif avg_satisfaction < 6:
            risk_score += 1
        
        if risk_score >= 4:
            return 'High'
        elif risk_score >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_crunch_health_metrics(self, employee_data: pd.DataFrame) -> Dict[str, Any]:
        """Calcule les métriques de santé liées au crunch"""
        
        health_metrics = {
            'overall_health_score': 0,
            'stress_indicators': {},
            'retention_risk': 0,
            'performance_trends': {}
        }
        
        if employee_data.empty:
            return health_metrics
        
        # Score de santé global (0-100)
        factors = []
        
        if 'weekly_hours' in employee_data.columns:
            avg_hours = employee_data['weekly_hours'].mean()
            hours_score = max(0, 100 - (avg_hours - 40) * 2)
            factors.append(hours_score)
        
        if 'satisfaction_score' in employee_data.columns:
            avg_satisfaction = employee_data['satisfaction_score'].mean()
            satisfaction_score = (avg_satisfaction / 10) * 100
            factors.append(satisfaction_score)
        
        if 'stress_level' in employee_data.columns:
            avg_stress = employee_data['stress_level'].mean()
            stress_score = max(0, 100 - avg_stress * 10)
            factors.append(stress_score)
        
        if factors:
            health_metrics['overall_health_score'] = round(np.mean(factors), 2)
        
        # Indicateurs de stress
        if 'weekly_hours' in employee_data.columns:
            high_hours_count = (employee_data['weekly_hours'] > 50).sum()
            health_metrics['stress_indicators']['high_hours_employees'] = high_hours_count
            health_metrics['stress_indicators']['percentage_high_hours'] = round(
                (high_hours_count / len(employee_data)) * 100, 2
            )
        
        # Risque de rétention
        if 'satisfaction_score' in employee_data.columns and 'weekly_hours' in employee_data.columns:
            at_risk = employee_data[
                (employee_data['satisfaction_score'] < 6) & 
                (employee_data['weekly_hours'] > 50)
            ]
            health_metrics['retention_risk'] = len(at_risk)
        
        return health_metrics
    
    def _predict_crunch_risk(self, employee_data: pd.DataFrame) -> Dict[str, Any]:
        """Prédit les risques de crunch futurs"""
        
        predictions = {
            'next_month_risk': 'Medium',
            'high_risk_departments': [],
            'recommended_actions': []
        }
        
        if employee_data.empty:
            return predictions
        
        # Analyse par département
        if 'department' in employee_data.columns and 'weekly_hours' in employee_data.columns:
            dept_risks = []
            
            for dept in employee_data['department'].unique():
                dept_data = employee_data[employee_data['department'] == dept]
                avg_hours = dept_data['weekly_hours'].mean()
                
                if avg_hours > 48:
                    dept_risks.append({
                        'department': dept,
                        'risk_level': 'High',
                        'avg_hours': round(avg_hours, 1)
                    })
                elif avg_hours > 45:
                    dept_risks.append({
                        'department': dept,
                        'risk_level': 'Medium',
                        'avg_hours': round(avg_hours, 1)
                    })
            
            predictions['high_risk_departments'] = dept_risks
        
        # Recommandations d'actions
        if predictions['high_risk_departments']:
            predictions['recommended_actions'] = [
                'Implement mandatory rest periods for high-risk departments',
                'Review project timelines and resource allocation',
                'Consider temporary staff augmentation',
                'Monitor employee satisfaction scores weekly',
                'Establish crunch compensation policies'
            ]
        
        return predictions
    
    def _generate_crunch_recommendations(self, employee_data: pd.DataFrame) -> List[Dict[str, str]]:
        """Génère des recommandations pour gérer le crunch"""
        
        recommendations = []
        
        if employee_data.empty:
            return recommendations
        
        # Analyse des heures moyennes
        if 'weekly_hours' in employee_data.columns:
            avg_hours = employee_data['weekly_hours'].mean()
            
            if avg_hours > 50:
                recommendations.append({
                    'priority': 'High',
                    'category': 'Immediate Action',
                    'title': 'Reduce Working Hours',
                    'description': f'Average {avg_hours:.1f}h/week exceeds healthy limits. Implement immediate measures to reduce workload.',
                    'timeline': '1-2 weeks'
                })
            
            if avg_hours > 45:
                recommendations.append({
                    'priority': 'Medium',
                    'category': 'Resource Management',
                    'title': 'Resource Augmentation',
                    'description': 'Consider hiring temporary contractors or redistributing tasks to balance workload.',
                    'timeline': '2-4 weeks'
                })
        
        # Analyse de satisfaction
        if 'satisfaction_score' in employee_data.columns:
            avg_satisfaction = employee_data['satisfaction_score'].mean()
            
            if avg_satisfaction < 6:
                recommendations.append({
                    'priority': 'High',
                    'category': 'Employee Wellbeing',
                    'title': 'Address Satisfaction Issues',
                    'description': f'Low satisfaction score ({avg_satisfaction:.1f}/10) indicates potential burnout risks.',
                    'timeline': 'Immediate'
                })
        
        # Recommandations générales
        recommendations.extend([
            {
                'priority': 'Medium',
                'category': 'Policy',
                'title': 'Establish Crunch Guidelines',
                'description': 'Create clear policies for maximum working hours and mandatory recovery periods.',
                'timeline': '1 month'
            },
            {
                'priority': 'Low',
                'category': 'Monitoring',
                'title': 'Implement Crunch Tracking',
                'description': 'Set up automated monitoring system for working hours and stress indicators.',
                'timeline': '6-8 weeks'
            }
        ])
        
        return recommendations
    
    def render_crunch_dashboard(self, analysis_results: Dict[str, Any]):
        """Affiche le dashboard d'analyse du crunch"""
        
        st.markdown("# 🔥 Gaming Crunch Analysis Dashboard")
        st.markdown("*Real-time monitoring of development crunch periods and team health*")
        
        if not analysis_results or analysis_results.get('status') == 'no_data':
            st.warning("No data available for crunch analysis")
            return
        
        # Métriques principales
        crunch_data = analysis_results.get('crunch_detection', {})
        health_metrics = analysis_results.get('health_metrics', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            crunch_count = len(crunch_data.get('current_crunch_employees', []))
            st.metric(
                "🔥 Employees in Crunch",
                crunch_count,
                delta=f"{crunch_count - 15}" if crunch_count > 15 else None,
                delta_color="inverse"
            )
        
        with col2:
            at_risk_count = len(crunch_data.get('at_risk_employees', []))
            st.metric(
                "⚠️ At Risk",
                at_risk_count,
                delta=f"{at_risk_count - 8}" if at_risk_count > 8 else None,
                delta_color="inverse"
            )
        
        with col3:
            health_score = health_metrics.get('overall_health_score', 0)
            st.metric(
                "💚 Health Score",
                f"{health_score:.0f}%",
                delta=f"{health_score - 75:.0f}%" if health_score != 75 else None
            )
        
        with col4:
            retention_risk = health_metrics.get('retention_risk', 0)
            st.metric(
                "📉 Retention Risk",
                retention_risk,
                delta=f"{retention_risk - 5}" if retention_risk != 5 else None,
                delta_color="inverse"
            )
        
        # Analyse par département
        st.markdown("## 🏢 Crunch Analysis by Department")
        
        dept_analysis = analysis_results.get('department_analysis', {})
        if dept_analysis:
            dept_df = pd.DataFrame(dept_analysis).T.reset_index()
            dept_df.columns = ['Department'] + list(dept_df.columns[1:])
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.bar(
                    dept_df,
                    x='Department',
                    y='crunch_percentage',
                    title='Percentage of Employees in Crunch by Department',
                    color='crunch_percentage',
                    color_continuous_scale='Reds'
                )
                fig1.update_layout(height=400)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.scatter(
                    dept_df,
                    x='avg_weekly_hours',
                    y='avg_satisfaction',
                    size='total_employees',
                    color='Department',
                    title='Hours vs Satisfaction by Department'
                )
                fig2.update_layout(height=400)
                st.plotly_chart(fig2, use_container_width=True)
        
        # Alertes et recommandations
        st.markdown("## 🚨 Alerts & Recommendations")
        
        recommendations = analysis_results.get('recommendations', [])
        
        # Affichage par priorité
        priority_colors = {
            'High': '🔴',
            'Medium': '🟡', 
            'Low': '🟢'
        }
        
        for priority in ['High', 'Medium', 'Low']:
            priority_recs = [r for r in recommendations if r.get('priority') == priority]
            if priority_recs:
                st.markdown(f"### {priority_colors[priority]} {priority} Priority")
                
                for rec in priority_recs:
                    with st.expander(f"{rec['title']} - {rec['category']}"):
                        st.write(f"**Description:** {rec['description']}")
                        st.write(f"**Timeline:** {rec['timeline']}")
        
        # Employés en crunch critique
        critical_employees = [
            emp for emp in crunch_data.get('current_crunch_employees', [])
            if emp.get('severity') in ['Critical', 'High']
        ]
        
        if critical_employees:
            st.markdown("## ⚡ Critical Attention Required")
            
            critical_df = pd.DataFrame(critical_employees)
            st.dataframe(critical_df, use_container_width=True)
