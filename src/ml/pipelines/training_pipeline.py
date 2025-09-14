"""
Gaming Workforce Observatory - Training Pipeline Enterprise
Pipeline automatisé d'entraînement avec MLOps et versioning des modèles
"""
import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import joblib
import json
import hashlib

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
import mlflow
import mlflow.sklearn

logger = logging.getLogger(__name__)

class EnterpriseTrainingPipeline:
    """Pipeline d'entraînement enterprise avec MLOps et monitoring"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_path = config.get('data_path')
        self.model_save_path = Path(config.get('model_save_path', 'models/'))
        self.experiment_name = config.get('experiment_name', 'gaming_workforce_models')
        
        # Initialisation MLflow
        mlflow.set_experiment(self.experiment_name)
        
        # Modèles supportés
        self.supported_models = {
            'random_forest': RandomForestClassifier,
            'gradient_boosting': GradientBoostingClassifier,
            'logistic_regression': LogisticRegression
        }
        
        # Paramètres de grid search
        self.param_grids = {
            'random_forest': {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 15, 20, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 6, 9],
                'subsample': [0.8, 1.0]
            },
            'logistic_regression': {
                'C': [0.1, 1.0, 10.0],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear', 'saga']
            }
        }
        
        self.training_results = {}
        self.best_model = None
        self.best_model_name = None
        
    def run_full_pipeline(self) -> Dict[str, Any]:
        """Exécute le pipeline complet d'entraînement"""
        
        pipeline_results = {
            'pipeline_id': self._generate_pipeline_id(),
            'timestamp': datetime.now().isoformat(),
            'status': 'started',
            'stages_completed': [],
            'model_performances': {},
            'best_model_info': {},
            'data_quality_report': {},
            'deployment_artifacts': {}
        }
        
        try:
            with mlflow.start_run(run_name=f"training_pipeline_{pipeline_results['pipeline_id']}"):
                
                # Étape 1: Chargement et validation des données
                logger.info("Stage 1: Data loading and validation")
                data_validation = self._validate_and_load_data()
                pipeline_results['data_quality_report'] = data_validation
                pipeline_results['stages_completed'].append('data_validation')
                
                if not data_validation['is_valid']:
                    pipeline_results['status'] = 'failed'
                    pipeline_results['error'] = 'Data validation failed'
                    return pipeline_results
                
                # Étape 2: Préparation des données
                logger.info("Stage 2: Data preparation")
                X_train, X_test, y_train, y_test, feature_names = self._prepare_training_data(
                    data_validation['data']
                )
                pipeline_results['stages_completed'].append('data_preparation')
                
                # Étape 3: Entraînement des modèles
                logger.info("Stage 3: Model training and selection")
                model_results = self._train_and_evaluate_models(
                    X_train, X_test, y_train, y_test, feature_names
                )
                pipeline_results['model_performances'] = model_results
                pipeline_results['stages_completed'].append('model_training')
                
                # Étape 4: Sélection du meilleur modèle
                best_model_info = self._select_best_model(model_results)
                pipeline_results['best_model_info'] = best_model_info
                pipeline_results['stages_completed'].append('model_selection')
                
                # Étape 5: Validation finale et sauvegarde
                logger.info("Stage 5: Final validation and artifact creation")
                deployment_artifacts = self._create_deployment_artifacts(
                    best_model_info, feature_names, pipeline_results['pipeline_id']
                )
                pipeline_results['deployment_artifacts'] = deployment_artifacts
                pipeline_results['stages_completed'].append('artifact_creation')
                
                # Logging MLflow
                mlflow.log_params(self.config)
                mlflow.log_metrics({
                    'best_model_auc': best_model_info['performance']['test_auc'],
                    'best_model_accuracy': best_model_info['performance']['accuracy'],
                    'training_samples': len(X_train),
                    'test_samples': len(X_test)
                })
                mlflow.sklearn.log_model(self.best_model, "best_model")
                
                pipeline_results['status'] = 'completed'
                logger.info(f"Training pipeline completed successfully: {pipeline_results['pipeline_id']}")
                
        except Exception as e:
            pipeline_results['status'] = 'failed'
            pipeline_results['error'] = str(e)
            logger.error(f"Training pipeline failed: {e}")
        
        return pipeline_results
    
    def _generate_pipeline_id(self) -> str:
        """Génère un ID unique pour le pipeline"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config_hash = hashlib.md5(str(self.config).encode()).hexdigest()[:8]
        return f"pipeline_{timestamp}_{config_hash}"
    
    def _validate_and_load_data(self) -> Dict[str, Any]:
        """Valide et charge les données d'entraînement"""
        
        validation_result = {
            'is_valid': False,
            'data': None,
            'quality_metrics': {},
            'warnings': [],
            'errors': []
        }
        
        try:
            # Chargement des données
            if not os.path.exists(self.data_path):
                validation_result['errors'].append(f"Data file not found: {self.data_path}")
                return validation_result
            
            data = pd.read_csv(self.data_path)
            
            # Vérifications de qualité
            quality_checks = [
                ('min_samples', len(data) >= 100, f"Insufficient samples: {len(data)}"),
                ('target_column', 'will_leave_6months' in data.columns, "Target column missing"),
                ('missing_data', data.isnull().sum().sum() / data.size < 0.5, "Too much missing data"),
                ('target_balance', data['will_leave_6months'].value_counts().min() >= 10, "Imbalanced target")
            ]
            
            passed_checks = 0
            for check_name, condition, error_msg in quality_checks:
                if condition:
                    passed_checks += 1
                else:
                    validation_result['errors'].append(error_msg)
            
            validation_result['quality_metrics'] = {
                'total_samples': len(data),
                'total_features': len(data.columns),
                'missing_percentage': (data.isnull().sum().sum() / data.size) * 100,
                'target_distribution': data['will_leave_6months'].value_counts().to_dict(),
                'checks_passed': f"{passed_checks}/{len(quality_checks)}"
            }
            
            if passed_checks == len(quality_checks):
                validation_result['is_valid'] = True
                validation_result['data'] = data
                logger.info(f"Data validation passed: {len(data)} samples loaded")
            
        except Exception as e:
            validation_result['errors'].append(f"Data loading error: {str(e)}")
        
        return validation_result
    
    def _prepare_training_data(self, data: pd.DataFrame) -> tuple:
        """Prépare les données pour l'entraînement"""
        
        # Nettoyage et engineering des features
        data_clean = data.dropna(subset=['will_leave_6months'])
        
        # Sélection des features prédictives
        feature_columns = [
            'satisfaction_score', 'performance_score', 'weekly_hours',
            'years_experience', 'salary_usd', 'team_size', 'age'
        ]
        
        # Features disponibles
        available_features = [col for col in feature_columns if col in data_clean.columns]
        
        # Engineering de features avancées
        data_enhanced = self._engineer_features(data_clean)
        
        # Features finales (disponibles + engineered)
        engineered_features = [
            'salary_percentile', 'hours_satisfaction_ratio', 'experience_performance_ratio'
        ]
        
        all_features = available_features + [
            feat for feat in engineered_features if feat in data_enhanced.columns
        ]
        
        # Préparation X et y
        X = data_enhanced[all_features].fillna(data_enhanced[all_features].median())
        y = data_enhanced['will_leave_6months']
        
        # Normalisation
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(
            scaler.fit_transform(X), 
            columns=X.columns, 
            index=X.index
        )
        
        # Division train/test stratifiée
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, 
            test_size=0.2, 
            random_state=42, 
            stratify=y
        )
        
        logger.info(f"Training data prepared: {len(all_features)} features, {len(X_train)} train samples")
        
        return X_train, X_test, y_train, y_test, all_features
    
    def _engineer_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Engineering de features avancées"""
        
        data_enhanced = data.copy()
        
        # Percentile de salaire
        if 'salary_usd' in data.columns:
            data_enhanced['salary_percentile'] = data['salary_usd'].rank(pct=True)
        
        # Ratio heures/satisfaction (indicateur burnout)
        if 'weekly_hours' in data.columns and 'satisfaction_score' in data.columns:
            data_enhanced['hours_satisfaction_ratio'] = (
                data['weekly_hours'] / (data['satisfaction_score'] + 1)
            )
        
        # Ratio expérience/performance
        if 'years_experience' in data.columns and 'performance_score' in data.columns:
            expected_perf = 2 + (data['years_experience'] / 10)  # Performance attendue
            data_enhanced['experience_performance_ratio'] = (
                data['performance_score'] / expected_perf.clip(lower=1)
            )
        
        return data_enhanced
    
    def _train_and_evaluate_models(self, X_train, X_test, y_train, y_test, feature_names) -> Dict[str, Any]:
        """Entraîne et évalue multiple modèles avec grid search"""
        
        model_results = {}
        
        for model_name, ModelClass in self.supported_models.items():
            logger.info(f"Training {model_name}...")
            
            try:
                # Grid search avec validation croisée
                param_grid = self.param_grids.get(model_name, {})
                
                if param_grid:
                    grid_search = GridSearchCV(
                        ModelClass(random_state=42),
                        param_grid,
                        cv=5,
                        scoring='roc_auc',
                        n_jobs=-1,
                        verbose=0
                    )
                    
                    grid_search.fit(X_train, y_train)
                    best_model = grid_search.best_estimator_
                    best_params = grid_search.best_params_
                else:
                    best_model = ModelClass(random_state=42)
                    best_model.fit(X_train, y_train)
                    best_params = {}
                
                # Prédictions et métriques
                y_pred = best_model.predict(X_test)
                y_proba = best_model.predict_proba(X_test)[:, 1] if hasattr(best_model, 'predict_proba') else None
                
                # Métriques de performance
                performance_metrics = {
                    'accuracy': float(np.mean(y_pred == y_test)),
                    'test_auc': float(roc_auc_score(y_test, y_proba)) if y_proba is not None else 0.0
                }
                
                # Cross-validation score
                cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='roc_auc')
                performance_metrics['cv_auc_mean'] = float(cv_scores.mean())
                performance_metrics['cv_auc_std'] = float(cv_scores.std())
                
                # Classification report
                clf_report = classification_report(y_test, y_pred, output_dict=True)
                
                # Feature importance si disponible
                feature_importance = {}
                if hasattr(best_model, 'feature_importances_'):
                    feature_importance = dict(zip(
                        feature_names, 
                        best_model.feature_importances_
                    ))
                
                model_results[model_name] = {
                    'model': best_model,
                    'best_params': best_params,
                    'performance': performance_metrics,
                    'classification_report': clf_report,
                    'feature_importance': feature_importance,
                    'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
                }
                
                logger.info(f"{model_name} - AUC: {performance_metrics['test_auc']:.4f}")
                
            except Exception as e:
                logger.error(f"Error training {model_name}: {e}")
                model_results[model_name] = {'error': str(e)}
        
        return model_results
    
    def _select_best_model(self, model_results: Dict[str, Any]) -> Dict[str, Any]:
        """Sélectionne le meilleur modèle basé sur les performances"""
        
        valid_models = {
            name: results for name, results in model_results.items()
            if 'error' not in results
        }
        
        if not valid_models:
            raise ValueError("No valid models found")
        
        # Sélection basée sur AUC test
        best_model_name = max(
            valid_models.keys(),
            key=lambda x: valid_models[x]['performance']['test_auc']
        )
        
        best_model_info = valid_models[best_model_name]
        self.best_model = best_model_info['model']
        self.best_model_name = best_model_name
        
        logger.info(f"Best model selected: {best_model_name} (AUC: {best_model_info['performance']['test_auc']:.4f})")
        
        return {
            'model_name': best_model_name,
            'model': self.best_model,
            'performance': best_model_info['performance'],
            'best_params': best_model_info['best_params'],
            'feature_importance': best_model_info['feature_importance']
        }
    
    def _create_deployment_artifacts(self, best_model_info: Dict[str, Any], 
                                   feature_names: List[str], pipeline_id: str) -> Dict[str, Any]:
        """Crée les artefacts de déploiement"""
        
        # Répertoire de sauvegarde
        save_dir = self.model_save_path / pipeline_id
        save_dir.mkdir(parents=True, exist_ok=True)
        
        artifacts = {}
        
        # Sauvegarde du modèle
        model_path = save_dir / 'model.joblib'
        joblib.dump(best_model_info['model'], model_path)
        artifacts['model_path'] = str(model_path)
        
        # Métadonnées du modèle
        metadata = {
            'pipeline_id': pipeline_id,
            'model_name': best_model_info['model_name'],
            'training_timestamp': datetime.now().isoformat(),
            'performance_metrics': best_model_info['performance'],
            'feature_names': feature_names,
            'best_parameters': best_model_info['best_params'],
            'feature_importance': best_model_info['feature_importance']
        }
        
        metadata_path = save_dir / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        artifacts['metadata_path'] = str(metadata_path)
        
        # Configuration de déploiement
        deployment_config = {
            'model_version': pipeline_id,
            'input_features': feature_names,
            'prediction_threshold': 0.5,
            'monitoring_enabled': True
        }
        
        config_path = save_dir / 'deployment_config.json'
        with open(config_path, 'w') as f:
            json.dump(deployment_config, f, indent=2)
        artifacts['config_path'] = str(config_path)
        
        logger.info(f"Deployment artifacts created in: {save_dir}")
        
        return artifacts
    
    def get_model_performance_report(self, model_results: Dict[str, Any]) -> str:
        """Génère un rapport de performance des modèles"""
        
        report = "# Gaming Workforce Models - Training Report\n\n"
        report += f"**Training Timestamp:** {datetime.now().isoformat()}\n"
        report += f"**Pipeline ID:** {getattr(self, 'pipeline_id', 'N/A')}\n\n"
        
        report += "## Model Performance Comparison\n\n"
        report += "| Model | Test AUC | CV AUC (±std) | Accuracy | Best Parameters |\n"
        report += "|-------|----------|---------------|----------|----------------|\n"
        
        for model_name, results in model_results.items():
            if 'error' not in results:
                perf = results['performance']
                params_str = str(results['best_params'])[:50] + "..." if len(str(results['best_params'])) > 50 else str(results['best_params'])
                
                report += f"| {model_name} | {perf['test_auc']:.4f} | "
                report += f"{perf['cv_auc_mean']:.4f} (±{perf['cv_auc_std']:.4f}) | "
                report += f"{perf['accuracy']:.4f} | {params_str} |\n"
        
        if hasattr(self, 'best_model_name') and self.best_model_name:
            report += f"\n**Best Model:** {self.best_model_name}\n"
        
        return report
