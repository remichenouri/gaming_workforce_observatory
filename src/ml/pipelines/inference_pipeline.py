"""
Gaming Workforce Observatory - Inference Pipeline Enterprise
Pipeline d'inférence en temps réel avec monitoring et A/B testing
"""
import joblib
import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import streamlit as st
from sklearn.preprocessing import StandardScaler
import mlflow
import mlflow.sklearn

logger = logging.getLogger(__name__)

class EnterpriseInferencePipeline:
    """Pipeline d'inférence enterprise avec monitoring et versioning"""
    
    def __init__(self, model_config_path: str):
        self.model_config_path = Path(model_config_path)
        self.model = None
        self.metadata = None
        self.scaler = None
        self.feature_names = []
        self.model_version = None
        
        # Métriques de monitoring
        self.prediction_history = []
        self.performance_metrics = {
            'total_predictions': 0,
            'avg_prediction_time': 0,
            'error_count': 0,
            'confidence_distribution': []
        }
        
        self._load_model_artifacts()
    
    def _load_model_artifacts(self):
        """Charge le modèle et ses artefacts"""
        
        try:
            # Chargement des métadonnées
            metadata_path = self.model_config_path / 'metadata.json'
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                
                self.feature_names = self.metadata.get('feature_names', [])
                self.model_version = self.metadata.get('pipeline_id', 'unknown')
                
                logger.info(f"Model metadata loaded: version {self.model_version}")
            
            # Chargement du modèle
            model_path = self.model_config_path / 'model.joblib'
            if model_path.exists():
                self.model = joblib.load(model_path)
                logger.info("Model loaded successfully")
            else:
                raise FileNotFoundError(f"Model file not found: {model_path}")
                
            # Chargement du scaler si disponible
            scaler_path = self.model_config_path / 'scaler.joblib'
            if scaler_path.exists():
                self.scaler = joblib.load(scaler_path)
                logger.info("Scaler loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model artifacts: {e}")
            raise
    
    def predict_single(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Effectue une prédiction pour un employé unique"""
        
        start_time = datetime.now()
        
        try:
            # Préparation des données
            employee_df = pd.DataFrame([employee_data])
            processed_data = self._preprocess_input(employee_df)
            
            if processed_data is None:
                return {
                    'error': 'Data preprocessing failed',
                    'employee_id': employee_data.get('employee_id', 'unknown'),
                    'timestamp': start_time.isoformat()
                }
            
            # Prédiction
            prediction_proba = self.model.predict_proba(processed_data)[0]
            prediction_class = self.model.predict(processed_data)[0]
            
            # Confidence et risk level
            confidence = max(prediction_proba)
            attrition_probability = prediction_proba[1] if len(prediction_proba) > 1 else prediction_proba[0]
            
            # Classification du risque
            risk_level = self._classify_risk_level(attrition_probability)
            
            # Temps de prédiction
            prediction_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Construction du résultat
            result = {
                'employee_id': employee_data.get('employee_id', 'unknown'),
                'prediction': {
                    'will_leave': bool(prediction_class),
                    'attrition_probability': float(attrition_probability),
                    'confidence': float(confidence),
                    'risk_level': risk_level
                },
                'model_info': {
                    'model_version': self.model_version,
                    'features_used': len(self.feature_names),
                    'prediction_time_ms': prediction_time
                },
                'timestamp': start_time.isoformat()
            }
            
            # Enregistrement pour monitoring
            self._log_prediction(result, prediction_time)
            
            return result
            
        except Exception as e:
            self.performance_metrics['error_count'] += 1
            logger.error(f"Prediction error for employee {employee_data.get('employee_id', 'unknown')}: {e}")
            
            return {
                'error': str(e),
                'employee_id': employee_data.get('employee_id', 'unknown'),
                'timestamp': start_time.isoformat()
            }
    
    def predict_batch(self, employees_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Effectue des prédictions en lot"""
        
        results = []
        start_time = datetime.now()
        
        try:
            # Conversion en DataFrame
            employees_df = pd.DataFrame(employees_data)
            processed_data = self._preprocess_input(employees_df)
            
            if processed_data is None:
                # Retourner erreurs individuelles
                return [
                    {
                        'error': 'Data preprocessing failed',
                        'employee_id': emp.get('employee_id', f'employee_{i}'),
                        'timestamp': start_time.isoformat()
                    }
                    for i, emp in enumerate(employees_data)
                ]
            
            # Prédictions batch
            predictions_proba = self.model.predict_proba(processed_data)
            predictions_class = self.model.predict(processed_data)
            
            # Construction des résultats
            for i, (emp_data, pred_class, pred_proba) in enumerate(
                zip(employees_data, predictions_class, predictions_proba)
            ):
                confidence = max(pred_proba)
                attrition_probability = pred_proba[1] if len(pred_proba) > 1 else pred_proba[0]
                risk_level = self._classify_risk_level(attrition_probability)
                
                result = {
                    'employee_id': emp_data.get('employee_id', f'employee_{i}'),
                    'prediction': {
                        'will_leave': bool(pred_class),
                        'attrition_probability': float(attrition_probability),
                        'confidence': float(confidence),
                        'risk_level': risk_level
                    },
                    'model_info': {
                        'model_version': self.model_version,
                        'features_used': len(self.feature_names)
                    },
                    'timestamp': start_time.isoformat()
                }
                
                results.append(result)
            
            # Logging batch
            batch_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.info(f"Batch prediction completed: {len(results)} predictions in {batch_time:.2f}ms")
            
            # Mise à jour métriques
            self.performance_metrics['total_predictions'] += len(results)
            
        except Exception as e:
            logger.error(f"Batch prediction error: {e}")
            # Retourner erreurs pour tous
            results = [
                {
                    'error': str(e),
                    'employee_id': emp.get('employee_id', f'employee_{i}'),
                    'timestamp': start_time.isoformat()
                }
                for i, emp in enumerate(employees_data)
            ]
        
        return results
    
    def _preprocess_input(self, input_df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Prétraite les données d'entrée"""
        
        try:
            # Engineering des features (cohérent avec training)
            processed_df = self._engineer_features(input_df)
            
            # Sélection des features du modèle
            available_features = [col for col in self.feature_names if col in processed_df.columns]
            
            if len(available_features) < len(self.feature_names) * 0.8:  # Au moins 80% des features
                logger.warning(f"Only {len(available_features)}/{len(self.feature_names)} features available")
            
            # Extraction et imputation
            X = processed_df[available_features].fillna(processed_df[available_features].median())
            
            # Ajout des features manquantes avec valeurs par défaut
            for feature in self.feature_names:
                if feature not in X.columns:
                    X[feature] = 0  # Valeur par défaut
            
            # Réordonnancement selon l'ordre d'entraînement
            X = X[self.feature_names]
            
            # Normalisation si scaler disponible
            if self.scaler:
                X_scaled = pd.DataFrame(
                    self.scaler.transform(X),
                    columns=X.columns,
                    index=X.index
                )
                return X_scaled
            
            return X
            
        except Exception as e:
            logger.error(f"Preprocessing error: {e}")
            return None
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineering de features (cohérent avec training pipeline)"""
        
        df_enhanced = df.copy()
        
        # Percentile de salaire
        if 'salary_usd' in df.columns:
            # Approximation basée sur distribution typique
            df_enhanced['salary_percentile'] = df['salary_usd'].rank(pct=True)
        
        # Ratio heures/satisfaction
        if 'weekly_hours' in df.columns and 'satisfaction_score' in df.columns:
            df_enhanced['hours_satisfaction_ratio'] = (
                df['weekly_hours'] / (df['satisfaction_score'] + 1)
            )
        
        # Ratio expérience/performance
        if 'years_experience' in df.columns and 'performance_score' in df.columns:
            expected_perf = 2 + (df['years_experience'] / 10)
            df_enhanced['experience_performance_ratio'] = (
                df['performance_score'] / expected_perf.clip(lower=1)
            )
        
        return df_enhanced
    
    def _classify_risk_level(self, probability: float) -> str:
        """Classifie le niveau de risque d'attrition"""
        
        if probability >= 0.75:
            return 'Critical'
        elif probability >= 0.50:
            return 'High' 
        elif probability >= 0.30:
            return 'Medium'
        else:
            return 'Low'
    
    def _log_prediction(self, result: Dict[str, Any], prediction_time: float):
        """Enregistre la prédiction pour monitoring"""
        
        # Ajout à l'historique (limité aux 1000 dernières)
        self.prediction_history.append({
            'timestamp': result['timestamp'],
            'employee_id': result['employee_id'],
            'attrition_probability': result['prediction']['attrition_probability'],
            'confidence': result['prediction']['confidence'],
            'risk_level': result['prediction']['risk_level'],
            'prediction_time_ms': prediction_time
        })
        
        # Limitation de l'historique
        if len(self.prediction_history) > 1000:
            self.prediction_history = self.prediction_history[-1000:]
        
        # Mise à jour des métriques
        self.performance_metrics['total_predictions'] += 1
        
        # Moyenne mobile du temps de prédiction
        current_avg = self.performance_metrics['avg_prediction_time']
        total_preds = self.performance_metrics['total_predictions']
        new_avg = ((current_avg * (total_preds - 1)) + prediction_time) / total_preds
        self.performance_metrics['avg_prediction_time'] = new_avg
        
        # Distribution de confiance
        confidence = result['prediction']['confidence']
        self.performance_metrics['confidence_distribution'].append(confidence)
        
        # Garder seulement les 100 dernières confidences
        if len(self.performance_metrics['confidence_distribution']) > 100:
            self.performance_metrics['confidence_distribution'] = \
                self.performance_metrics['confidence_distribution'][-100:]
    
    def get_monitoring_dashboard_data(self) -> Dict[str, Any]:
        """Retourne les données pour le dashboard de monitoring"""
        
        if not self.prediction_history:
            return {'status': 'no_data', 'message': 'No predictions logged yet'}
        
        # Analyse des prédictions récentes
        recent_predictions = self.prediction_history[-100:]  # 100 dernières
        
        # Distribution des niveaux de risque
        risk_distribution = {}
        for pred in recent_predictions:
            risk = pred['risk_level']
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
        
        # Tendances temporelles (par heure)
        hourly_trends = {}
        for pred in recent_predictions:
            hour = pred['timestamp'][:13]  # YYYY-MM-DDTHH
            if hour not in hourly_trends:
                hourly_trends[hour] = {'count': 0, 'avg_probability': 0, 'high_risk_count': 0}
            
            hourly_trends[hour]['count'] += 1
            hourly_trends[hour]['avg_probability'] += pred['attrition_probability']
            if pred['risk_level'] in ['High', 'Critical']:
                hourly_trends[hour]['high_risk_count'] += 1
        
        # Calcul des moyennes
        for hour_data in hourly_trends.values():
            hour_data['avg_probability'] /= hour_data['count']
        
        # Métriques de performance
        performance_summary = {
            'total_predictions': self.performance_metrics['total_predictions'],
            'avg_prediction_time_ms': round(self.performance_metrics['avg_prediction_time'], 2),
            'error_rate': (self.performance_metrics['error_count'] / 
                          max(1, self.performance_metrics['total_predictions'])) * 100,
            'avg_confidence': round(np.mean(self.performance_metrics['confidence_distribution']), 3)
            if self.performance_metrics['confidence_distribution'] else 0
        }
        
        return {
            'status': 'success',
            'model_version': self.model_version,
            'last_updated': datetime.now().isoformat(),
            'risk_distribution': risk_distribution,
            'hourly_trends': hourly_trends,
            'performance_summary': performance_summary,
            'recent_predictions_count': len(recent_predictions)
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Vérifie la santé du pipeline d'inférence"""
        
        health_status = {
            'status': 'healthy',
            'checks': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Vérification du modèle
        health_status['checks']['model_loaded'] = self.model is not None
        
        # Vérification des métadonnées
        health_status['checks']['metadata_available'] = self.metadata is not None
        
        # Vérification des features
        health_status['checks']['features_defined'] = len(self.feature_names) > 0
        
        # Test de prédiction simple
        try:
            test_data = {col: 1.0 for col in self.feature_names}
            test_result = self.predict_single(test_data)
            health_status['checks']['prediction_test'] = 'error' not in test_result
        except:
            health_status['checks']['prediction_test'] = False
        
        # Vérification performance récente
        if self.performance_metrics['total_predictions'] > 0:
            error_rate = (self.performance_metrics['error_count'] / 
                         self.performance_metrics['total_predictions'])
            health_status['checks']['error_rate_acceptable'] = error_rate < 0.05  # <5% erreurs
        else:
            health_status['checks']['error_rate_acceptable'] = True
        
        # Status global
        all_checks_passed = all(health_status['checks'].values())
        health_status['status'] = 'healthy' if all_checks_passed else 'degraded'
        
        return health_status
    
    def render_inference_dashboard(self):
        """Interface Streamlit pour le monitoring des inférences"""
        
        st.markdown("## 🔮 Model Inference Dashboard")
        st.markdown(f"*Model Version: {self.model_version}*")
        
        # Health Check
        health = self.health_check()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### System Health")
        with col2:
            status_color = "🟢" if health['status'] == 'healthy' else "🟡"
            st.markdown(f"**Status:** {status_color} {health['status'].upper()}")
        
        # Checks détaillés
        checks_df = pd.DataFrame([
            {'Check': check.replace('_', ' ').title(), 'Status': '✅' if passed else '❌'}
            for check, passed in health['checks'].items()
        ])
        st.dataframe(checks_df, hide_index=True)
        
        # Données de monitoring
        monitoring_data = self.get_monitoring_dashboard_data()
        
        if monitoring_data['status'] == 'success':
            # Métriques de performance
            st.markdown("### 📊 Performance Metrics")
            
            perf = monitoring_data['performance_summary']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Predictions", perf['total_predictions'])
            with col2:
                st.metric("Avg Response Time", f"{perf['avg_prediction_time_ms']:.1f}ms")
            with col3:
                st.metric("Error Rate", f"{perf['error_rate']:.2f}%")
            with col4:
                st.metric("Avg Confidence", f"{perf['avg_confidence']:.3f}")
            
            # Distribution des risques
            st.markdown("### 🎯 Risk Level Distribution")
            
            risk_dist = monitoring_data['risk_distribution']
            if risk_dist:
                colors = {
                    'Critical': '#e74c3c',
                    'High': '#f39c12', 
                    'Medium': '#f1c40f',
                    'Low': '#27ae60'
                }
                
                fig = px.pie(
                    values=list(risk_dist.values()),
                    names=list(risk_dist.keys()),
                    title="Recent Predictions by Risk Level",
                    color=list(risk_dist.keys()),
                    color_discrete_map=colors
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Test de prédiction en direct
        st.markdown("### 🧪 Live Prediction Test")
        
        with st.expander("Test Single Prediction"):
            col1, col2 = st.columns(2)
            
            with col1:
                test_satisfaction = st.slider("Satisfaction Score", 1, 10, 7)
                test_hours = st.slider("Weekly Hours", 30, 80, 45)
                test_performance = st.slider("Performance Score", 1, 5, 3)
            
            with col2:
                test_experience = st.slider("Years Experience", 0, 20, 3)
                test_salary = st.number_input("Salary (USD)", 30000, 200000, 80000)
                test_team_size = st.slider("Team Size", 1, 20, 8)
            
            if st.button("Run Prediction Test"):
                test_data = {
                    'satisfaction_score': test_satisfaction,
                    'weekly_hours': test_hours,
                    'performance_score': test_performance,
                    'years_experience': test_experience,
                    'salary_usd': test_salary,
                    'team_size': test_team_size,
                    'employee_id': 'test_employee'
                }
                
                with st.spinner("Running prediction..."):
                    result = self.predict_single(test_data)
                
                if 'error' in result:
                    st.error(f"Prediction failed: {result['error']}")
                else:
                    pred = result['prediction']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Attrition Risk", f"{pred['attrition_probability']:.1%}")
                    with col2:
                        st.metric("Risk Level", pred['risk_level'])
                    with col3:
                        st.metric("Confidence", f"{pred['confidence']:.3f}")
                    
                    if pred['risk_level'] in ['High', 'Critical']:
                        st.warning("⚠️ This employee shows high attrition risk!")
                    else:
                        st.success("✅ Low attrition risk detected")
