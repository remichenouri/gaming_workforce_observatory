"""
Gaming Workforce Observatory - Anomaly Detector Enterprise
Détection d'anomalies sophistiquée avec Isolation Forest et analyses contextuelles
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class GamingAnomalyDetector:
    """Détecteur d'anomalies enterprise pour données RH gaming"""
    
    def __init__(self, contamination: float = 0.05):
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination, 
            random_state=42,
            n_estimators=200,
            max_samples='auto',
            max_features=1.0
        )
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Garde 95% variance
        
        # Features spécifiques gaming pour anomalies
        self.gaming_features = [
            'weekly_hours', 'satisfaction_score', 'performance_score',
            'salary_usd', 'years_experience', 'team_size',
            'project_completion_rate', 'peer_feedback_score',
            'manager_rating', 'overtime_frequency', 'crunch_exposure'
        ]
        
        self.anomaly_profiles = {
            'overworked_burnout': {
                'description': 'Employé en surcharge chronique',
                'indicators': ['high_hours', 'low_satisfaction', 'declining_performance']
            },
            'underperformer': {
                'description': 'Performance inhabituelle',
                'indicators': ['low_performance', 'low_peer_feedback']
            },
            'compensation_outlier': {
                'description': 'Anomalie salariale',
                'indicators': ['salary_mismatch', 'experience_compensation_gap']
            },
            'engagement_drop': {
                'description': 'Baisse engagement soudaine',
                'indicators': ['satisfaction_drop', 'participation_decline']
            }
        }
    
    @st.cache_data(ttl=3600)
    def detect_anomalies(_self, df: pd.DataFrame) -> Dict[str, Any]:
        """Détecte les anomalies dans les données employés gaming"""
        
        detection_results = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'total_records': len(df),
            'anomalies_detected': 0,
            'anomaly_breakdown': {},
            'detailed_anomalies': [],
            'risk_assessment': {},
            'recommendations': []
        }
        
        try:
            # Préparation des données
            X, feature_names = _self._prepare_anomaly_features(df)
            
            if X is None:
                detection_results['status'] = 'error'
                detection_results['message'] = 'Feature preparation failed'
                return detection_results
            
            # Détection d'anomalies
            anomaly_scores = _self.model.fit_predict(X)
            anomaly_probabilities = _self.model.decision_function(X)
            
            # Identification des anomalies
            anomalies_mask = anomaly_scores == -1
            anomalies_count = anomalies_mask.sum()
            
            detection_results['anomalies_detected'] = int(anomalies_count)
            detection_results['anomaly_percentage'] = (anomalies_count / len(df)) * 100
            
            if anomalies_count > 0:
                # Analyse détaillée des anomalies
                anomaly_analysis = _self._analyze_anomalies_detail(
                    df, anomalies_mask, anomaly_probabilities, feature_names
                )
                
                detection_results['detailed_anomalies'] = anomaly_analysis['anomalies']
                detection_results['anomaly_breakdown'] = anomaly_analysis['breakdown']
                detection_results['risk_assessment'] = anomaly_analysis['risk_assessment']
                detection_results['recommendations'] = _self._generate_anomaly_recommendations(
                    anomaly_analysis
                )
            
            detection_results['status'] = 'success'
            logger.info(f"Anomaly detection completed: {anomalies_count} anomalies found in {len(df)} records")
            
        except Exception as e:
            detection_results['status'] = 'error'
            detection_results['message'] = str(e)
            logger.error(f"Anomaly detection failed: {e}")
        
        return detection_results
    
    def _prepare_anomaly_features(self, df: pd.DataFrame) -> Tuple[Optional[np.ndarray], List[str]]:
        """Prépare les features pour la détection d'anomalies"""
        
        # Sélection des features disponibles
        available_features = [col for col in self.gaming_features if col in df.columns]
        
        if len(available_features) < 3:
            logger.error(f"Insufficient features for anomaly detection: {available_features}")
            return None, []
        
        # Engineering de features spécifiques aux anomalies
        df_enhanced = self._engineer_anomaly_features(df)
        
        # Mise à jour des features disponibles après engineering
        all_possible_features = available_features + [
            'hours_satisfaction_ratio', 'performance_experience_ratio',
            'salary_market_deviation', 'engagement_decline_score'
        ]
        
        final_features = [col for col in all_possible_features if col in df_enhanced.columns]
        
        # Extraction et nettoyage
        X = df_enhanced[final_features].fillna(df_enhanced[final_features].median())
        
        # Normalisation
        X_scaled = self.scaler.fit_transform(X)
        
        # Réduction dimensionnelle si trop de features
        if X_scaled.shape[1] > 15:
            X_scaled = self.pca.fit_transform(X_scaled)
            final_features = [f'PC{i+1}' for i in range(X_scaled.shape[1])]
        
        logger.info(f"Anomaly features prepared: {len(final_features)} features")
        return X_scaled, final_features
    
    def _engineer_anomaly_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineering de features spécifiques aux anomalies gaming"""
        
        df_enhanced = df.copy()
        
        # Ratio heures/satisfaction (indicateur burnout)
        if 'weekly_hours' in df.columns and 'satisfaction_score' in df.columns:
            df_enhanced['hours_satisfaction_ratio'] = (
                df['weekly_hours'] / (df['satisfaction_score'] + 1)
            )
        
        # Ratio performance/expérience (indicateur sous-performance)
        if 'performance_score' in df.columns and 'years_experience' in df.columns:
            expected_performance = 2 + (df['years_experience'] / 5)  # Performance attendue
            df_enhanced['performance_experience_ratio'] = (
                df['performance_score'] / expected_performance.clip(lower=1)
            )
        
        # Déviation salariale du marché
        if 'salary_usd' in df.columns and 'years_experience' in df.columns:
            expected_salary = 50000 + (df['years_experience'] * 8000)  # Modèle simple
            df_enhanced['salary_market_deviation'] = (
                (df['salary_usd'] - expected_salary) / expected_salary
            )
        
        # Score de déclin d'engagement
        engagement_factors = []
        for factor in ['satisfaction_score', 'peer_feedback_score', 'manager_rating']:
            if factor in df.columns:
                # Simulation d'une tendance (en réalité, comparaison historique)
                baseline = df[factor].median()
                engagement_factors.append((df[factor] - baseline) / baseline)
        
        if engagement_factors:
            df_enhanced['engagement_decline_score'] = np.mean(engagement_factors, axis=0)
        
        return df_enhanced
    
    def _analyze_anomalies_detail(self, df: pd.DataFrame, anomalies_mask: np.ndarray,
                                 anomaly_scores: np.ndarray, feature_names: List[str]) -> Dict[str, Any]:
        """Analyse détaillée des anomalies détectées"""
        
        anomalies_df = df[anomalies_mask].copy()
        anomalies_df['anomaly_score'] = anomaly_scores[anomalies_mask]
        
        # Classement par sévérité
        anomalies_df['severity'] = pd.cut(
            -anomalies_df['anomaly_score'],  # Scores négatifs = plus anormal
            bins=3,
            labels=['Low', 'Medium', 'High']
        )
        
        detailed_anomalies = []
        
        for idx, anomaly in anomalies_df.iterrows():
            anomaly_profile = self._classify_anomaly_type(anomaly)
            
            detailed_anomalies.append({
                'employee_id': anomaly.get('employee_id', f'Employee_{idx}'),
                'employee_name': anomaly.get('name', 'Anonymous'),
                'department': anomaly.get('department', 'Unknown'),
                'anomaly_score': float(anomaly['anomaly_score']),
                'severity': anomaly['severity'],
                'anomaly_type': anomaly_profile['type'],
                'description': anomaly_profile['description'],
                'key_indicators': anomaly_profile['indicators'],
                'risk_level': anomaly_profile['risk_level'],
                'recommended_actions': anomaly_profile['actions']
            })
        
        # Breakdown par type et département
        anomaly_breakdown = {
            'by_severity': anomalies_df['severity'].value_counts().to_dict(),
            'by_department': anomalies_df.get('department', pd.Series(dtype='object')).value_counts().to_dict(),
            'by_type': {}
        }
        
        for anomaly in detailed_anomalies:
            anomaly_type = anomaly['anomaly_type']
            anomaly_breakdown['by_type'][anomaly_type] = anomaly_breakdown['by_type'].get(anomaly_type, 0) + 1
        
        # Assessment de risque global
        risk_assessment = {
            'high_risk_count': (anomalies_df['severity'] == 'High').sum(),
            'departments_affected': len(anomalies_df.get('department', pd.Series()).unique()),
            'avg_anomaly_score': float(anomalies_df['anomaly_score'].mean()),
            'most_common_type': max(anomaly_breakdown['by_type'], key=anomaly_breakdown['by_type'].get) if anomaly_breakdown['by_type'] else 'None'
        }
        
        return {
            'anomalies': detailed_anomalies,
            'breakdown': anomaly_breakdown,
            'risk_assessment': risk_assessment
        }
    
    def _classify_anomaly_type(self, anomaly_record: pd.Series) -> Dict[str, Any]:
        """Classifie le type d'anomalie et génère des recommandations"""
        
        # Extraction des indicateurs
        weekly_hours = anomaly_record.get('weekly_hours', 40)
        satisfaction = anomaly_record.get('satisfaction_score', 7)
        performance = anomaly_record.get('performance_score', 3)
        salary = anomaly_record.get('salary_usd', 80000)
        experience = anomaly_record.get('years_experience', 3)
        
        # Classification basée sur patterns
        if weekly_hours > 55 and satisfaction < 6:
            return {
                'type': 'overworked_burnout',
                'description': 'Employé en surcharge avec risque de burnout',
                'indicators': [f'Heures: {weekly_hours}/semaine', f'Satisfaction: {satisfaction}/10'],
                'risk_level': 'High',
                'actions': [
                    'Réduire charge de travail immédiatement',
                    'Entretien one-on-one urgent',
                    'Évaluer redistribution tâches'
                ]
            }
        
        elif performance < 2.5 and satisfaction < 5:
            return {
                'type': 'underperformer',
                'description': 'Performance et engagement faibles',
                'indicators': [f'Performance: {performance}/5', f'Satisfaction: {satisfaction}/10'],
                'risk_level': 'High',
                'actions': [
                    'Plan d\'amélioration performance',
                    'Formation et coaching',
                    'Révision des objectifs'
                ]
            }
        
        elif abs(salary - (50000 + experience * 8000)) > 30000:
            return {
                'type': 'compensation_outlier',
                'description': 'Anomalie dans la compensation',
                'indicators': [f'Salaire: ${salary:,.0f}', f'Expérience: {experience} ans'],
                'risk_level': 'Medium',
                'actions': [
                    'Révision équité salariale',
                    'Comparaison benchmarks marché',
                    'Discussion ajustement potentiel'
                ]
            }
        
        else:
            return {
                'type': 'general_outlier',
                'description': 'Pattern atypique nécessitant investigation',
                'indicators': ['Combinaison de facteurs inhabituels'],
                'risk_level': 'Medium',
                'actions': [
                    'Investigation approfondie',
                    'Entretien avec manager',
                    'Suivi personnalisé'
                ]
            }
    
    def _generate_anomaly_recommendations(self, anomaly_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Génère des recommandations basées sur l'analyse des anomalies"""
        
        recommendations = []
        risk_assessment = anomaly_analysis['risk_assessment']
        anomalies = anomaly_analysis['anomalies']
        
        # Recommandations urgentes pour anomalies critiques
        high_risk_count = risk_assessment['high_risk_count']
        if high_risk_count > 0:
            recommendations.append({
                'priority': 'CRITICAL',
                'category': 'Intervention Urgente',
                'title': 'Traiter anomalies à haut risque',
                'description': f'{high_risk_count} employés nécessitent intervention immédiate',
                'action': 'Planifier entretiens dans les 48h',
                'timeline': 'Immédiat'
            })
        
        # Recommandations par type d'anomalie
        type_counts = anomaly_analysis['breakdown']['by_type']
        
        if type_counts.get('overworked_burnout', 0) >= 3:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Gestion Workload',
                'title': 'Prévention burnout collectif',
                'description': 'Plusieurs employés en surcharge détectés',
                'action': 'Révision globale allocation ressources',
                'timeline': '1-2 semaines'
            })
        
        if type_counts.get('compensation_outlier', 0) >= 2:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Équité Salariale',
                'title': 'Audit compensation',
                'description': 'Anomalies salariales multiples détectées',
                'action': 'Révision grilles salariales',
                'timeline': '1 mois'
            })
        
        # Recommandations préventives
        if len(anomalies) > len(anomaly_analysis['breakdown']['by_severity']) * 0.1:  # >10% anomalies
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Monitoring',
                'title': 'Système alerte précoce',
                'description': 'Taux d\'anomalies élevé nécessite monitoring',
                'action': 'Mise en place alertes automatiques',
                'timeline': '2-3 semaines'
            })
        
        return recommendations
    
    def render_anomaly_dashboard(self, detection_results: Dict[str, Any], df: pd.DataFrame):
        """Dashboard de visualisation des anomalies"""
        
        st.markdown("## 🔍 Anomaly Detection Dashboard")
        st.markdown("*Real-time detection of unusual patterns in HR data*")
        
        if detection_results.get('status') != 'success':
            st.error("Anomaly detection failed or no data available")
            return
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            anomalies_count = detection_results.get('anomalies_detected', 0)
            st.metric(
                "🚨 Anomalies Detected",
                anomalies_count,
                delta=f"{detection_results.get('anomaly_percentage', 0):.1f}% of total"
            )
        
        with col2:
            high_risk = detection_results.get('risk_assessment', {}).get('high_risk_count', 0)
            st.metric(
                "⚠️ High Risk",
                high_risk,
                delta_color="inverse"
            )
        
        with col3:
            depts_affected = detection_results.get('risk_assessment', {}).get('departments_affected', 0)
            st.metric(
                "🏢 Departments Affected",
                depts_affected
            )
        
        with col4:
            avg_score = detection_results.get('risk_assessment', {}).get('avg_anomaly_score', 0)
            st.metric(
                "📊 Avg Anomaly Score",
                f"{avg_score:.3f}"
            )
        
        # Répartition des anomalies
        if detection_results.get('anomaly_breakdown'):
            st.markdown("### 📊 Anomaly Breakdown")
            
            breakdown = detection_results['anomaly_breakdown']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Par sévérité
                if breakdown.get('by_severity'):
                    severity_data = breakdown['by_severity']
                    fig1 = px.pie(
                        values=list(severity_data.values()),
                        names=list(severity_data.keys()),
                        title="Anomalies by Severity",
                        color_discrete_map={
                            'High': '#e74c3c',
                            'Medium': '#f39c12',
                            'Low': '#27ae60'
                        }
                    )
                    st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Par type
                if breakdown.get('by_type'):
                    type_data = breakdown['by_type']
                    fig2 = px.bar(
                        x=list(type_data.keys()),
                        y=list(type_data.values()),
                        title="Anomalies by Type",
                        color=list(type_data.values()),
                        color_continuous_scale='Reds'
                    )
                    fig2.update_xaxes(tickangle=45)
                    st.plotly_chart(fig2, use_container_width=True)
        
        # Liste des anomalies détaillées
        detailed_anomalies = detection_results.get('detailed_anomalies', [])
        if detailed_anomalies:
            st.markdown("### 📋 Detailed Anomalies")
            
            # Filtres
            col1, col2, col3 = st.columns(3)
            
            with col1:
                severity_filter = st.selectbox(
                    "Filter by Severity",
                    ['All'] + [a['severity'] for a in detailed_anomalies]
                )
            
            with col2:
                type_filter = st.selectbox(
                    "Filter by Type",
                    ['All'] + list(set([a['anomaly_type'] for a in detailed_anomalies]))
                )
            
            with col3:
                risk_filter = st.selectbox(
                    "Filter by Risk Level",
                    ['All'] + list(set([a['risk_level'] for a in detailed_anomalies]))
                )
            
            # Application des filtres
            filtered_anomalies = detailed_anomalies
            
            if severity_filter != 'All':
                filtered_anomalies = [a for a in filtered_anomalies if a['severity'] == severity_filter]
            if type_filter != 'All':
                filtered_anomalies = [a for a in filtered_anomalies if a['anomaly_type'] == type_filter]
            if risk_filter != 'All':
                filtered_anomalies = [a for a in filtered_anomalies if a['risk_level'] == risk_filter]
            
            # Affichage des anomalies
            for anomaly in filtered_anomalies[:10]:  # Limite à 10 pour performance
                severity_color = {
                    'High': '#e74c3c',
                    'Medium': '#f39c12', 
                    'Low': '#27ae60'
                }.get(anomaly['severity'], '#95a5a6')
                
                with st.expander(
                    f"🚨 {anomaly['employee_name']} - {anomaly['department']} ({anomaly['severity']} Risk)",
                    expanded=(anomaly['severity'] == 'High')
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Type:** {anomaly['anomaly_type']}")
                        st.markdown(f"**Description:** {anomaly['description']}")
                        st.markdown(f"**Risk Level:** {anomaly['risk_level']}")
                        st.markdown(f"**Anomaly Score:** {anomaly['anomaly_score']:.3f}")
                    
                    with col2:
                        st.markdown("**Key Indicators:**")
                        for indicator in anomaly['key_indicators']:
                            st.write(f"• {indicator}")
                        
                        st.markdown("**Recommended Actions:**")
                        for action in anomaly['recommended_actions']:
                            st.write(f"• {action}")
        
        # Recommandations
        recommendations = detection_results.get('recommendations', [])
        if recommendations:
            st.markdown("### 💡 Action Recommendations")
            
            for rec in recommendations:
                priority_colors = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟡',
                    'MEDIUM': '🟠',
                    'LOW': '🟢'
                }
                
                priority_icon = priority_colors.get(rec['priority'], '📋')
                
                with st.expander(f"{priority_icon} {rec['title']} - {rec['category']}"):
                    st.markdown(f"**Priority:** {rec['priority']}")
                    st.markdown(f"**Description:** {rec['description']}")
                    st.markdown(f"**Recommended Action:** {rec['action']}")
                    st.markdown(f"**Timeline:** {rec['timeline']}")
