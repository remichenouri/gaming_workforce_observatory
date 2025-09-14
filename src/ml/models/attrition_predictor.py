"""
Gaming Workforce Observatory - Attrition Predictor Enterprise
Prédiction avancée du turnover gaming avec ensemble methods et SHAP explicability
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
import xgboost as xgb
import shap
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)

class GamingAttritionPredictor:
    """Prédicteur de turnover gaming enterprise avec ML explicable"""
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.feature_columns = [
            'satisfaction_score', 'performance_score', 'salary_percentile',
            'years_experience', 'crunch_exposure_hours', 'team_size',
            'manager_rating', 'career_progression_score', 'work_life_balance',
            'training_opportunities', 'project_completion_rate', 'peer_feedback',
            'commute_time', 'remote_flexibility', 'bonus_percentage',
            'equity_value', 'benefits_score', 'department_encoded',
            'level_encoded', 'location_encoded', 'neurodiversity_support'
        ]
        
        self.scaler = StandardScaler()
        self.encoders = {}
        self.explainer = None
        self.feature_importance = None
        self.model_metadata = {}
        
        # Seuils de risque gaming-specific
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
    
    @st.cache_data(ttl=86400)  # Cache 24h
    def train_ensemble_model(_self, data: pd.DataFrame, target_column: str = 'will_leave_6months') -> Dict[str, Any]:
        """Entraîne un ensemble de modèles avec validation croisée"""
        
        training_results = {
            'timestamp': datetime.now().isoformat(),
            'data_shape': data.shape,
            'model_performances': {},
            'best_model_info': {},
            'feature_importance': {},
            'training_metrics': {}
        }
        
        try:
            # Préparation des données
            X, y = _self._prepare_features(data, target_column)
            
            if X is None or y is None:
                training_results['status'] = 'error'
                training_results['message'] = 'Feature preparation failed'
                return training_results
            
            # Division train/test stratifiée
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Définition des modèles
            _self.models = {
                'random_forest': RandomForestClassifier(
                    n_estimators=200, max_depth=15, min_samples_split=5,
                    min_samples_leaf=2, random_state=42, n_jobs=-1
                ),
                'xgboost': xgb.XGBClassifier(
                    n_estimators=150, max_depth=8, learning_rate=0.1,
                    subsample=0.8, colsample_bytree=0.8, random_state=42
                ),
                'gradient_boosting': GradientBoostingClassifier(
                    n_estimators=150, max_depth=6, learning_rate=0.1,
                    random_state=42
                ),
                'logistic_regression': LogisticRegression(
                    random_state=42, max_iter=1000, C=1.0
                )
            }
            
            # Entraînement et évaluation de chaque modèle
            for model_name, model in _self.models.items():
                logger.info(f"Training {model_name}...")
                
                # Entraînement
                model.fit(X_train, y_train)
                
                # Prédictions
                y_pred = model.predict(X_test)
                y_proba = model.predict_proba(X_test)[:, 1]
                
                # Métriques
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
                test_auc = roc_auc_score(y_test, y_proba)
                
                # Classification report
                clf_report = classification_report(y_test, y_pred, output_dict=True)
                
                training_results['model_performances'][model_name] = {
                    'cv_mean_auc': cv_scores.mean(),
                    'cv_std_auc': cv_scores.std(),
                    'test_auc': test_auc,
                    'precision': clf_report['weighted avg']['precision'],
                    'recall': clf_report['weighted avg']['recall'],
                    'f1_score': clf_report['weighted avg']['f1-score'],
                    'accuracy': clf_report['accuracy']
                }
                
                logger.info(f"{model_name} - Test AUC: {test_auc:.4f}, CV AUC: {cv_scores.mean():.4f}")
            
            # Sélection du meilleur modèle
            best_model_name = max(
                training_results['model_performances'].keys(),
                key=lambda x: training_results['model_performances'][x]['test_auc']
            )
            
            _self.best_model = _self.models[best_model_name]
            _self.best_model_name = best_model_name
            
            # Métadonnées du meilleur modèle
            training_results['best_model_info'] = {
                'model_name': best_model_name,
                'performance': training_results['model_performances'][best_model_name],
                'feature_count': len(_self.feature_columns),
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            # Feature importance
            if hasattr(_self.best_model, 'feature_importances_'):
                feature_importance = dict(zip(
                    _self.feature_columns, 
                    _self.best_model.feature_importances_
                ))
                _self.feature_importance = feature_importance
                training_results['feature_importance'] = feature_importance
            
            # SHAP explicabilité
            if best_model_name in ['random_forest', 'xgboost', 'gradient_boosting']:
                _self.explainer = shap.TreeExplainer(_self.best_model)
                shap_values = _self.explainer.shap_values(X_test[:100])  # Sample pour performance
                
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]  # Classe positive
                
                training_results['shap_summary'] = {
                    'mean_shap_values': dict(zip(_self.feature_columns, np.mean(np.abs(shap_values), axis=0))),
                    'sample_size': min(100, len(X_test))
                }
            
            training_results['status'] = 'success'
            _self.model_metadata = training_results
            
            logger.info(f"Training completed. Best model: {best_model_name} (AUC: {training_results['best_model_info']['performance']['test_auc']:.4f})")
            
        except Exception as e:
            training_results['status'] = 'error'
            training_results['message'] = str(e)
            logger.error(f"Training failed: {e}")
        
        return training_results
    
    def _prepare_features(self, data: pd.DataFrame, target_column: str) -> Tuple[Optional[pd.DataFrame], Optional[pd.Series]]:
        """Prépare les features pour l'entraînement"""
        
        if target_column not in data.columns:
            logger.error(f"Target column '{target_column}' not found")
            return None, None
        
        # Nettoyage des données
        data_clean = data.dropna(subset=[target_column])
        
        # Création des features dérivées
        data_clean = self._engineer_features(data_clean)
        
        # Encodage des variables catégorielles
        data_encoded = self._encode_categorical_features(data_clean)
        
        # Sélection des features disponibles
        available_features = [col for col in self.feature_columns if col in data_encoded.columns]
        
        if len(available_features) < 5:
            logger.error(f"Insufficient features available: {len(available_features)}")
            return None, None
        
        X = data_encoded[available_features]
        y = data_encoded[target_column]
        
        # Mise à jour de la liste des features utilisées
        self.feature_columns = available_features
        
        # Normalisation des features numériques
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        X[numeric_columns] = self.scaler.fit_transform(X[numeric_columns])
        
        logger.info(f"Features prepared: {len(available_features)} features, {len(X)} samples")
        return X, y
    
    def _engineer_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Ingénierie de features gaming-specific"""
        
        data_enhanced = data.copy()
        
        # Feature: Percentile de salaire
        if 'salary_usd' in data.columns:
            data_enhanced['salary_percentile'] = data['salary_usd'].rank(pct=True) * 100
        
        # Feature: Exposition au crunch
        if 'weekly_hours' in data.columns:
            data_enhanced['crunch_exposure_hours'] = np.maximum(0, data['weekly_hours'] - 40)
        
        # Feature: Score de progression de carrière
        if 'years_experience' in data.columns and 'experience_level' in data.columns:
            level_mapping = {'Intern': 0, 'Junior': 1, 'Mid': 2, 'Senior': 3, 'Lead': 4, 'Principal': 5}
            expected_level = data['years_experience'].apply(lambda x: min(4, x // 2))
            actual_level = data['experience_level'].map(level_mapping).fillna(2)
            data_enhanced['career_progression_score'] = (actual_level - expected_level + 2) / 4
        
        # Feature: Work-life balance score
        if 'satisfaction_score' in data.columns and 'weekly_hours' in data.columns:
            data_enhanced['work_life_balance'] = (
                data['satisfaction_score'] * (50 - np.minimum(50, data['weekly_hours'])) / 50
            )
        
        # Feature: Support neurodiversité
        if 'neurodivergent_condition' in data.columns:
            data_enhanced['neurodiversity_support'] = (~data['neurodivergent_condition'].isnull()).astype(int)
        
        # Feature: Flexibilité remote
        if 'is_remote' in data.columns:
            data_enhanced['remote_flexibility'] = data['is_remote'].astype(int)
        elif 'location' in data.columns:
            data_enhanced['remote_flexibility'] = data['location'].str.contains('remote', case=False, na=False).astype(int)
        
        # Features par défaut si manquantes
        default_features = {
            'manager_rating': 3.5,
            'training_opportunities': 0.6,
            'project_completion_rate': 0.85,
            'peer_feedback': 3.8,
            'commute_time': 30,
            'bonus_percentage': 10,
            'equity_value': 0,
            'benefits_score': 7.0,
            'team_size': 8
        }
        
        for feature, default_value in default_features.items():
            if feature not in data_enhanced.columns:
                data_enhanced[feature] = default_value
        
        return data_enhanced
    
    def _encode_categorical_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Encode les features catégorielles"""
        
        data_encoded = data.copy()
        
        # Mapping des départements
        if 'department' in data.columns:
            dept_mapping = {
                'Programming': 4, 'Game Design': 3, 'Art & Animation': 2,
                'Quality Assurance': 1, 'Production': 3, 'Audio': 2,
                'Marketing': 1, 'Management': 4
            }
            data_encoded['department_encoded'] = data['department'].map(dept_mapping).fillna(2)
        
        # Mapping des niveaux d'expérience
        if 'experience_level' in data.columns:
            level_mapping = {
                'Intern': 0, 'Junior': 1, 'Mid': 2, 'Senior': 3, 
                'Lead': 4, 'Principal': 5, 'Director': 6
            }
            data_encoded['level_encoded'] = data['experience_level'].map(level_mapping).fillna(2)
        
        # Encodage des locations (par région)
        if 'location' in data.columns:
            location_mapping = self._create_location_mapping(data['location'])
            data_encoded['location_encoded'] = data['location'].map(location_mapping).fillna(2)
        
        return data_encoded
    
    def _create_location_mapping(self, locations: pd.Series) -> Dict[str, int]:
        """Crée un mapping pour les locations basé sur le coût de la vie"""
        
        high_cost_areas = ['san francisco', 'new york', 'london', 'zurich', 'singapore']
        medium_cost_areas = ['seattle', 'boston', 'toronto', 'berlin', 'amsterdam']
        
        mapping = {}
        for location in locations.dropna().unique():
            location_lower = str(location).lower()
            
            if any(area in location_lower for area in high_cost_areas):
                mapping[location] = 3  # High cost
            elif any(area in location_lower for area in medium_cost_areas):
                mapping[location] = 2  # Medium cost
            elif 'remote' in location_lower:
                mapping[location] = 1  # Remote
            else:
                mapping[location] = 1  # Low cost / other
        
        return mapping
    
    def predict_attrition_risk(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prédit le risque d'attrition pour un employé"""
        
        if not self.best_model:
            return {'error': 'Model not trained yet'}
        
        try:
            # Préparation des données employé
            employee_df = pd.DataFrame([employee_data])
            employee_df = self._engineer_features(employee_df)
            employee_df = self._encode_categorical_features(employee_df)
            
            # Sélection des features
            available_features = [col for col in self.feature_columns if col in employee_df.columns]
            X_employee = employee_df[available_features]
            
            # Normalisation
            numeric_columns = X_employee.select_dtypes(include=[np.number]).columns
            X_employee[numeric_columns] = self.scaler.transform(X_employee[numeric_columns])
            
            # Prédiction
            attrition_prob = self.best_model.predict_proba(X_employee)[0, 1]
            
            # Classification du risque
            if attrition_prob >= self.risk_thresholds['high']:
                risk_level = "🔴 HIGH RISK"
                risk_color = "#e74c3c"
                priority = "CRITICAL"
            elif attrition_prob >= self.risk_thresholds['medium']:
                risk_level = "🟡 MEDIUM RISK"
                risk_color = "#f39c12"
                priority = "HIGH"
            elif attrition_prob >= self.risk_thresholds['low']:
                risk_level = "🟠 LOW-MEDIUM RISK"
                risk_color = "#ff9500"
                priority = "MEDIUM"
            else:
                risk_level = "🟢 LOW RISK"
                risk_color = "#27ae60"
                priority = "LOW"
            
            # Explications SHAP
            explanations = {}
            if self.explainer:
                shap_values = self.explainer.shap_values(X_employee)
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]  # Classe positive
                
                feature_contributions = dict(zip(available_features, shap_values[0]))
                
                # Top facteurs de risque
                top_risk_factors = sorted(
                    feature_contributions.items(), 
                    key=lambda x: abs(x[1]), 
                    reverse=True
                )[:5]
                
                explanations = {
                    'top_risk_factors': top_risk_factors,
                    'shap_base_value': self.explainer.expected_value[1] if isinstance(self.explainer.expected_value, list) else self.explainer.expected_value
                }
            
            # Recommandations personnalisées
            recommendations = self._generate_retention_recommendations(
                employee_data, attrition_prob, explanations.get('top_risk_factors', [])
            )
            
            # Résultat complet
            result = {
                'timestamp': datetime.now().isoformat(),
                'employee_id': employee_data.get('employee_id', 'Unknown'),
                'attrition_probability': round(attrition_prob, 4),
                'risk_level': risk_level,
                'risk_color': risk_color,
                'priority': priority,
                'confidence_score': self._calculate_confidence_score(X_employee),
                'explanations': explanations,
                'recommendations': recommendations,
                'model_used': self.best_model_name,
                'features_analyzed': len(available_features)
            }
            
            logger.info(f"Attrition prediction completed for employee {employee_data.get('employee_id', 'Unknown')}: {attrition_prob:.2%} risk")
            
            return result
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _calculate_confidence_score(self, X: pd.DataFrame) -> float:
        """Calcule un score de confiance pour la prédiction"""
        
        if not self.best_model or len(X) == 0:
            return 0.0
        
        # Score basé sur la probabilité de classe
        probabilities = self.best_model.predict_proba(X)[0]
        confidence = max(probabilities)  # Confiance = probabilité de la classe prédite
        
        return round(confidence, 3)
    
    def _generate_retention_recommendations(self, employee_data: Dict, risk_prob: float, 
                                          risk_factors: List[Tuple[str, float]]) -> List[Dict]:
        """Génère des recommandations personnalisées de rétention"""
        
        recommendations = []
        
        # Analyse des facteurs de risque principaux
        factor_names = [factor[0] for factor in risk_factors[:3]] if risk_factors else []
        
        # Recommandations basées sur les facteurs de risque
        if 'satisfaction_score' in factor_names:
            recommendations.append({
                'category': 'Satisfaction',
                'action': '🎯 Améliorer satisfaction employé',
                'description': 'Organiser un entretien one-on-one pour identifier les sources d\'insatisfaction',
                'timeline': '1-2 semaines',
                'priority': 'HIGH',
                'estimated_impact': 'Réduction risque: 15-25%'
            })
        
        if 'crunch_exposure_hours' in factor_names:
            recommendations.append({
                'category': 'Work-Life Balance',
                'action': '⚖️ Réduire exposition crunch',
                'description': 'Redistribuer la charge de travail, embaucher du support temporaire',
                'timeline': '1 semaine',
                'priority': 'CRITICAL',
                'estimated_impact': 'Réduction risque: 20-30%'
            })
        
        if 'salary_percentile' in factor_names:
            recommendations.append({
                'category': 'Compensation',
                'action': '💰 Révision salariale',
                'description': 'Analyser la compétitivité salariale et proposer ajustement',
                'timeline': '2-4 semaines',
                'priority': 'HIGH',
                'estimated_impact': 'Réduction risque: 10-20%'
            })
        
        if 'career_progression_score' in factor_names:
            recommendations.append({
                'category': 'Career Development',
                'action': '📈 Plan de développement carrière',
                'description': 'Définir objectifs de promotion et plan de formation',
                'timeline': '1 mois',
                'priority': 'MEDIUM',
                'estimated_impact': 'Réduction risque: 12-18%'
            })
        
        if 'manager_rating' in factor_names:
            recommendations.append({
                'category': 'Management',
                'action': '👥 Améliorer relation manager',
                'description': 'Formation management, feedback 360°, coaching leadership',
                'timeline': '3-4 semaines',
                'priority': 'HIGH',
                'estimated_impact': 'Réduction risque: 15-22%'
            })
        
        # Recommandations générales selon le niveau de risque
        if risk_prob >= 0.7:
            recommendations.append({
                'category': 'Immediate Action',
                'action': '🚨 Plan de rétention d\'urgence',
                'description': 'Activer protocole de rétention: rencontre RH, proposition contre-offre',
                'timeline': 'Immédiat',
                'priority': 'CRITICAL',
                'estimated_impact': 'Réduction risque: 25-40%'
            })
        
        elif risk_prob >= 0.4:
            recommendations.append({
                'category': 'Proactive Engagement',
                'action': '🤝 Engagement proactif',
                'description': 'Augmenter fréquence des check-ins, proposer projets intéressants',
                'timeline': '2 semaines',
                'priority': 'MEDIUM',
                'estimated_impact': 'Réduction risque: 10-15%'
            })
        
        # Limitation à 5 recommandations max
        return recommendations[:5]
    
    def batch_predict(self, employees_df: pd.DataFrame) -> pd.DataFrame:
        """Prédictions en lot pour multiple employés"""
        
        if not self.best_model:
            raise ValueError("Model not trained yet")
        
        results = []
        
        for _, employee in employees_df.iterrows():
            employee_dict = employee.to_dict()
            prediction = self.predict_attrition_risk(employee_dict)
            
            if 'error' not in prediction:
                results.append({
                    'employee_id': employee_dict.get('employee_id', ''),
                    'attrition_probability': prediction['attrition_probability'],
                    'risk_level': prediction['risk_level'],
                    'priority': prediction['priority'],
                    'confidence_score': prediction['confidence_score']
                })
        
        return pd.DataFrame(results)
    
    def save_model(self, filepath: str) -> bool:
        """Sauvegarde le modèle entraîné"""
        
        if not self.best_model:
            logger.error("No trained model to save")
            return False
        
        try:
            model_data = {
                'model': self.best_model,
                'model_name': self.best_model_name,
                'feature_columns': self.feature_columns,
                'scaler': self.scaler,
                'encoders': self.encoders,
                'risk_thresholds': self.risk_thresholds,
                'metadata': self.model_metadata
            }
            
            joblib.dump(model_data, filepath)
            logger.info(f"Model saved successfully to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def load_model(self, filepath: str) -> bool:
        """Charge un modèle sauvegardé"""
        
        try:
            model_data = joblib.load(filepath)
            
            self.best_model = model_data['model']
            self.best_model_name = model_data['model_name']
            self.feature_columns = model_data['feature_columns']
            self.scaler = model_data['scaler']
            self.encoders = model_data['encoders']
            self.risk_thresholds = model_data['risk_thresholds']
            self.model_metadata = model_data['metadata']
            
            # Recréer l'explainer si nécessaire
            if self.best_model_name in ['random_forest', 'xgboost', 'gradient_boosting']:
                self.explainer = shap.TreeExplainer(self.best_model)
            
            logger.info(f"Model loaded successfully from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Retourne les informations du modèle"""
        
        if not self.best_model:
            return {'status': 'No model trained'}
        
        return {
            'model_name': self.best_model_name,
            'features_count': len(self.feature_columns),
            'metadata': self.model_metadata,
            'risk_thresholds': self.risk_thresholds,
            'training_timestamp': self.model_metadata.get('timestamp', 'Unknown')
        }
    
    def render_model_performance_dashboard(self):
        """Dashboard de performance du modèle"""
        
        if not self.model_metadata:
            st.warning("No model performance data available")
            return
        
        st.markdown("## 🎯 Model Performance Dashboard")
        
        # Métriques de performance
        best_perf = self.model_metadata.get('best_model_info', {}).get('performance', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Test AUC", f"{best_perf.get('test_auc', 0):.3f}")
        with col2:
            st.metric("📊 Precision", f"{best_perf.get('precision', 0):.3f}")
        with col3:
            st.metric("🔍 Recall", f"{best_perf.get('recall', 0):.3f}")
        with col4:
            st.metric("⚡ F1-Score", f"{best_perf.get('f1_score', 0):.3f}")
        
        # Comparaison des modèles
        model_performances = self.model_metadata.get('model_performances', {})
        
        if model_performances:
            st.markdown("### 📈 Model Comparison")
            
            perf_df = pd.DataFrame(model_performances).T
            perf_df = perf_df.round(4)
            
            fig = px.bar(
                perf_df.reset_index(), 
                x='index', 
                y='test_auc',
                title='Model Performance Comparison (Test AUC)',
                color='test_auc',
                color_continuous_scale='Viridis'
            )
            fig.update_xaxes(title='Model')
            fig.update_yaxes(title='AUC Score')
            st.plotly_chart(fig, use_container_width=True)
        
        # Feature importance
        feature_importance = self.model_metadata.get('feature_importance', {})
        if feature_importance:
            st.markdown("### 🔍 Feature Importance")
            
            importance_df = pd.DataFrame([
                {'Feature': k, 'Importance': v} 
                for k, v in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:15]
            ])
            
            fig = px.bar(
                importance_df,
                x='Importance',
                y='Feature',
                orientation='h',
                title='Top 15 Most Important Features',
                color='Importance',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
