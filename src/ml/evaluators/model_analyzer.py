"""
Gaming Workforce Observatory - Model Analyzer Enterprise
Analyse avancée des modèles ML avec métriques gaming-spécifiques
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, roc_curve,
    mean_squared_error, mean_absolute_error, r2_score,
    precision_recall_curve, average_precision_score
)
from sklearn.inspection import permutation_importance
import shap
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class GamingModelAnalyzer:
    """Analyseur de modèles ML enterprise pour Gaming Workforce Observatory"""
    
    def __init__(self, model, X_test: pd.DataFrame, y_test: pd.Series, 
                 problem_type: str = 'classification',
                 feature_names: List[str] = None,
                 model_name: str = "GamingML_Model"):
        """
        Initialize Gaming Model Analyzer
        
        Args:
            model: Trained ML model (scikit-learn compatible)
            X_test: Test features
            y_test: Test targets
            problem_type: 'classification' or 'regression'
            feature_names: Names of features
            model_name: Human-readable model name
        """
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.problem_type = problem_type
        self.feature_names = feature_names or [f'feat_{i}' for i in range(X_test.shape[1])]
        self.model_name = model_name
        
        # Predictions
        self.y_pred = None
        self.y_pred_proba = None
        
        # Analysis results
        self.metrics = {}
        self.feature_importance = None
        self.shap_values = None
        self.analysis_timestamp = datetime.now()
        
        # Gaming-specific thresholds
        self.gaming_thresholds = {
            'attrition_critical': 0.8,
            'performance_excellent': 4.5,
            'satisfaction_good': 7.0,
            'retention_acceptable': 85.0
        }
    
    def predict(self) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Generate predictions and probabilities"""
        
        logger.info(f"Generating predictions for {self.model_name}")
        
        self.y_pred = self.model.predict(self.X_test)
        
        # Get probabilities for classification
        if self.problem_type == 'classification' and hasattr(self.model, 'predict_proba'):
            self.y_pred_proba = self.model.predict_proba(self.X_test)
        
        return self.y_pred, self.y_pred_proba
    
    def evaluate_model(self) -> Dict[str, Any]:
        """Comprehensive model evaluation"""
        
        if self.y_pred is None:
            self.predict()
        
        logger.info(f"Evaluating {self.problem_type} model: {self.model_name}")
        
        if self.problem_type == 'classification':
            self.metrics = self._evaluate_classification()
        elif self.problem_type == 'regression':
            self.metrics = self._evaluate_regression()
        
        # Add gaming-specific insights
        self.metrics['gaming_insights'] = self._generate_gaming_insights()
        
        # Model complexity metrics
        self.metrics['model_complexity'] = self._analyze_model_complexity()
        
        # Performance summary
        self.metrics['performance_summary'] = self._create_performance_summary()
        
        logger.info(f"Model evaluation completed. Overall score: {self.metrics.get('overall_score', 'N/A')}")
        
        return self.metrics
    
    def _evaluate_classification(self) -> Dict[str, Any]:
        """Evaluate classification model"""
        
        metrics = {}
        
        # Basic metrics
        metrics['classification_report'] = classification_report(
            self.y_test, self.y_pred, output_dict=True
        )
        
        # Confusion matrix
        metrics['confusion_matrix'] = confusion_matrix(self.y_test, self.y_pred).tolist()
        
        # ROC AUC
        if self.y_pred_proba is not None:
            if len(np.unique(self.y_test)) == 2:  # Binary classification
                metrics['roc_auc'] = roc_auc_score(self.y_test, self.y_pred_proba[:, 1])
                metrics['average_precision'] = average_precision_score(self.y_test, self.y_pred_proba[:, 1])
            else:  # Multi-class
                metrics['roc_auc'] = roc_auc_score(self.y_test, self.y_pred_proba, multi_class='ovr')
        
        # Gaming-specific classification metrics
        if hasattr(self, '_is_attrition_model'):
            metrics['attrition_metrics'] = self._calculate_attrition_metrics()
        
        # Overall score for classification
        accuracy = metrics['classification_report']['accuracy']
        roc_auc = metrics.get('roc_auc', accuracy)
        metrics['overall_score'] = (accuracy + roc_auc) / 2
        
        return metrics
    
    def _evaluate_regression(self) -> Dict[str, Any]:
        """Evaluate regression model"""
        
        metrics = {}
        
        # Basic regression metrics
        metrics['mse'] = mean_squared_error(self.y_test, self.y_pred)
        metrics['rmse'] = np.sqrt(metrics['mse'])
        metrics['mae'] = mean_absolute_error(self.y_test, self.y_pred)
        metrics['r2_score'] = r2_score(self.y_test, self.y_pred)
        
        # Mean Absolute Percentage Error
        metrics['mape'] = np.mean(np.abs((self.y_test - self.y_pred) / self.y_test)) * 100
        
        # Gaming-specific regression metrics
        if 'salary' in str(self.model_name).lower():
            metrics['salary_metrics'] = self._calculate_salary_prediction_metrics()
        elif 'performance' in str(self.model_name).lower():
            metrics['performance_metrics'] = self._calculate_performance_metrics()
        
        # Overall score for regression
        metrics['overall_score'] = max(0, metrics['r2_score'])
        
        return metrics
    
    def _calculate_attrition_metrics(self) -> Dict[str, Any]:
        """Gaming-specific attrition prediction metrics"""
        
        attrition_metrics = {}
        
        # High-risk employee identification accuracy
        high_risk_threshold = self.gaming_thresholds['attrition_critical']
        
        if self.y_pred_proba is not None:
            high_risk_predictions = self.y_pred_proba[:, 1] > high_risk_threshold
            actual_attrition = self.y_test == 1
            
            # True positive rate for high-risk employees
            high_risk_recall = np.sum(high_risk_predictions & actual_attrition) / np.sum(actual_attrition)
            attrition_metrics['high_risk_recall'] = high_risk_recall
            
            # Precision for high-risk predictions
            if np.sum(high_risk_predictions) > 0:
                high_risk_precision = np.sum(high_risk_predictions & actual_attrition) / np.sum(high_risk_predictions)
                attrition_metrics['high_risk_precision'] = high_risk_precision
            
            # Cost-benefit analysis
            attrition_metrics['cost_benefit'] = self._calculate_attrition_cost_benefit()
        
        return attrition_metrics
    
    def _calculate_salary_prediction_metrics(self) -> Dict[str, Any]:
        """Gaming-specific salary prediction metrics"""
        
        salary_metrics = {}
        
        # Percentage of predictions within acceptable range (±10%)
        acceptable_range = 0.10
        within_range = np.abs((self.y_pred - self.y_test) / self.y_test) <= acceptable_range
        salary_metrics['predictions_within_10pct'] = np.mean(within_range)
        
        # Under/over prediction bias
        prediction_bias = np.mean(self.y_pred - self.y_test)
        salary_metrics['prediction_bias'] = prediction_bias
        salary_metrics['bias_percentage'] = (prediction_bias / np.mean(self.y_test)) * 100
        
        # Role-specific accuracy (if available)
        if hasattr(self.X_test, 'columns') and 'role' in str(self.X_test.columns):
            # This would need role information in the test set
            pass
        
        return salary_metrics
    
    def analyze_feature_importance(self, method: str = 'auto') -> Dict[str, np.ndarray]:
        """Analyze feature importance using multiple methods"""
        
        logger.info(f"Analyzing feature importance for {self.model_name}")
        
        importance_results = {}
        
        # Method 1: Built-in feature importance
        if hasattr(self.model, 'feature_importances_'):
            importance_results['builtin'] = self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            importance_results['coefficients'] = np.abs(self.model.coef_.flatten())
        
        # Method 2: Permutation importance
        try:
            perm_importance = permutation_importance(
                self.model, self.X_test, self.y_test, 
                n_repeats=5, random_state=42
            )
            importance_results['permutation'] = perm_importance.importances_mean
        except Exception as e:
            logger.warning(f"Could not calculate permutation importance: {e}")
        
        # Method 3: SHAP values (global importance)
        try:
            explainer = shap.Explainer(self.model, self.X_test.sample(100))
            shap_values = explainer(self.X_test.sample(200))
            importance_results['shap'] = np.abs(shap_values.values).mean(0)
            self.shap_values = shap_values
        except Exception as e:
            logger.warning(f"Could not calculate SHAP importance: {e}")
        
        # Combine methods if multiple available
        if len(importance_results) > 1:
            importance_results['combined'] = self._combine_importance_scores(importance_results)
        
        self.feature_importance = importance_results
        
        return importance_results
    
    def _combine_importance_scores(self, importance_dict: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine multiple importance scores using ensemble approach"""
        
        # Normalize all importance scores
        normalized_scores = {}
        for method, scores in importance_dict.items():
            if method != 'combined':
                normalized_scores[method] = scores / np.sum(scores)
        
        # Weighted average (prioritize SHAP if available)
        weights = {
            'shap': 0.4,
            'permutation': 0.3,
            'builtin': 0.2,
            'coefficients': 0.1
        }
        
        combined_scores = np.zeros(len(self.feature_names))
        total_weight = 0
        
        for method, scores in normalized_scores.items():
            weight = weights.get(method, 0.1)
            combined_scores += scores * weight
            total_weight += weight
        
        return combined_scores / total_weight
    
    def _generate_gaming_insights(self) -> Dict[str, Any]:
        """Generate gaming-specific model insights"""
        
        insights = {}
        
        # Model reliability for gaming decisions
        overall_score = self.metrics.get('overall_score', 0)
        
        if overall_score > 0.9:
            insights['reliability'] = 'Excellent - Ready for production deployment'
        elif overall_score > 0.8:
            insights['reliability'] = 'Good - Suitable for most gaming HR decisions'
        elif overall_score > 0.7:
            insights['reliability'] = 'Fair - Use with caution, consider improvements'
        else:
            insights['reliability'] = 'Poor - Requires significant improvement'
        
        # Gaming-specific recommendations
        insights['recommendations'] = []
        
        if self.problem_type == 'classification' and 'attrition' in self.model_name.lower():
            insights['recommendations'].extend([
                "Focus on high-risk predictions for retention interventions",
                "Consider cost-benefit analysis for intervention strategies",
                "Monitor model drift with changing gaming industry trends"
            ])
        
        if hasattr(self, 'feature_importance') and self.feature_importance:
            top_features = self._get_top_features(n=3)
            insights['key_drivers'] = [f"{feat}: {imp:.3f}" for feat, imp in top_features]
        
        # Industry context
        insights['gaming_context'] = {
            'model_type': self.problem_type,
            'gaming_domain': self._infer_gaming_domain(),
            'business_impact': self._assess_business_impact()
        }
        
        return insights
    
    def _get_top_features(self, n: int = 10) -> List[Tuple[str, float]]:
        """Get top N features by importance"""
        
        if not self.feature_importance:
            return []
        
        # Use combined importance if available, otherwise use the first available method
        importance_scores = (self.feature_importance.get('combined') or 
                           self.feature_importance.get('shap') or
                           self.feature_importance.get('permutation') or
                           self.feature_importance.get('builtin') or
                           self.feature_importance.get('coefficients'))
        
        if importance_scores is None:
            return []
        
        # Create feature-importance pairs and sort
        feature_importance_pairs = list(zip(self.feature_names, importance_scores))
        feature_importance_pairs.sort(key=lambda x: x[1], reverse=True)
        
        return feature_importance_pairs[:n]
    
    def create_analysis_report(self) -> Dict[str, Any]:
        """Create comprehensive analysis report"""
        
        if not self.metrics:
            self.evaluate_model()
        
        if not self.feature_importance:
            self.analyze_feature_importance()
        
        report = {
            'model_info': {
                'name': self.model_name,
                'type': str(type(self.model).__name__),
                'problem_type': self.problem_type,
                'analysis_timestamp': self.analysis_timestamp.isoformat(),
                'test_set_size': len(self.y_test)
            },
            'performance_metrics': self.metrics,
            'feature_analysis': {
                'top_features': self._get_top_features(10),
                'feature_count': len(self.feature_names),
                'importance_methods': list(self.feature_importance.keys()) if self.feature_importance else []
            },
            'gaming_insights': self.metrics.get('gaming_insights', {}),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        overall_score = self.metrics.get('overall_score', 0)
        
        # Performance-based recommendations
        if overall_score < 0.8:
            recommendations.extend([
                "Consider feature engineering to improve model performance",
                "Evaluate different algorithms or ensemble methods",
                "Increase training data size if possible"
            ])
        
        # Feature-based recommendations
        if self.feature_importance:
            top_features = self._get_top_features(3)
            if top_features:
                recommendations.append(
                    f"Focus data collection on key features: {', '.join([f[0] for f in top_features])}"
                )
        
        # Problem-specific recommendations
        if 'attrition' in self.model_name.lower():
            recommendations.extend([
                "Implement early warning system for high-risk employees",
                "Design retention strategies based on key risk factors",
                "Regular model retraining with new attrition data"
            ])
        
        return recommendations
    
    def _infer_gaming_domain(self) -> str:
        """Infer gaming domain from model name and features"""
        
        model_lower = self.model_name.lower()
        
        if 'attrition' in model_lower or 'retention' in model_lower:
            return 'talent_retention'
        elif 'salary' in model_lower or 'compensation' in model_lower:
            return 'compensation_analysis'
        elif 'performance' in model_lower:
            return 'performance_management'
        elif 'skill' in model_lower:
            return 'skills_analytics'
        else:
            return 'general_workforce'
    
    def _assess_business_impact(self) -> str:
        """Assess potential business impact"""
        
        overall_score = self.metrics.get('overall_score', 0)
        
        if overall_score > 0.9:
            return 'High - Model ready for critical business decisions'
        elif overall_score > 0.8:
            return 'Medium-High - Suitable for most business applications'
        elif overall_score > 0.7:
            return 'Medium - Use for preliminary analysis and insights'
        else:
            return 'Low - Requires improvement before business deployment'
    
    def _analyze_model_complexity(self) -> Dict[str, Any]:
        """Analyze model complexity and interpretability"""
        
        complexity = {}
        
        model_type = type(self.model).__name__
        
        # Interpretability score
        interpretable_models = ['LinearRegression', 'LogisticRegression', 'DecisionTreeClassifier', 'DecisionTreeRegressor']
        complex_models = ['RandomForestClassifier', 'GradientBoostingClassifier', 'XGBClassifier', 'MLPClassifier']
        
        if model_type in interpretable_models:
            complexity['interpretability'] = 'High'
        elif model_type in complex_models:
            complexity['interpretability'] = 'Medium'
        else:
            complexity['interpretability'] = 'Low'
        
        # Feature complexity
        complexity['feature_count'] = len(self.feature_names)
        
        if len(self.feature_names) < 10:
            complexity['feature_complexity'] = 'Low'
        elif len(self.feature_names) < 50:
            complexity['feature_complexity'] = 'Medium'
        else:
            complexity['feature_complexity'] = 'High'
        
        return complexity
    
    def _create_performance_summary(self) -> Dict[str, Any]:
        """Create executive performance summary"""
        
        summary = {}
        
        overall_score = self.metrics.get('overall_score', 0)
        
        # Executive grade
        if overall_score > 0.9:
            summary['grade'] = 'A+'
            summary['status'] = 'Excellent'
        elif overall_score > 0.8:
            summary['grade'] = 'A'
            summary['status'] = 'Good'
        elif overall_score > 0.7:
            summary['grade'] = 'B'
            summary['status'] = 'Acceptable'
        elif overall_score > 0.6:
            summary['grade'] = 'C'
            summary['status'] = 'Needs Improvement'
        else:
            summary['grade'] = 'F'
            summary['status'] = 'Poor'
        
        summary['overall_score'] = overall_score
        summary['confidence_level'] = self._calculate_confidence_level()
        
        return summary
    
    def _calculate_confidence_level(self) -> str:
        """Calculate confidence level in model predictions"""
        
        # This is a simplified confidence calculation
        # In practice, you might use more sophisticated methods like prediction intervals
        
        overall_score = self.metrics.get('overall_score', 0)
        test_size = len(self.y_test)
        
        # Adjust confidence based on test set size and performance
        if test_size > 1000 and overall_score > 0.85:
            return 'Very High'
        elif test_size > 500 and overall_score > 0.8:
            return 'High'
        elif test_size > 200 and overall_score > 0.7:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_attrition_cost_benefit(self) -> Dict[str, float]:
        """Calculate cost-benefit analysis for attrition model"""
        
        # Simplified cost-benefit calculation
        # In practice, these values would be customized based on company data
        
        cost_benefit = {}
        
        # Assumptions (these should be configurable)
        cost_per_hire = 25000  # Average cost to hire a gaming professional
        retention_program_cost = 5000  # Cost of retention intervention per employee
        
        if self.y_pred_proba is not None:
            high_risk_threshold = self.gaming_thresholds['attrition_critical']
            high_risk_count = np.sum(self.y_pred_proba[:, 1] > high_risk_threshold)
            
            # Potential savings from preventing attrition
            potential_savings = high_risk_count * cost_per_hire * 0.3  # Assume 30% success rate
            intervention_cost = high_risk_count * retention_program_cost
            
            cost_benefit['potential_savings'] = potential_savings
            cost_benefit['intervention_cost'] = intervention_cost
            cost_benefit['net_benefit'] = potential_savings - intervention_cost
            cost_benefit['roi'] = (cost_benefit['net_benefit'] / intervention_cost) if intervention_cost > 0 else 0
        
        return cost_benefit

    def save_analysis(self, filepath: str) -> None:
        """Save analysis results to file"""
        
        report = self.create_analysis_report()
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Analysis report saved to {filepath}")

    def plot_performance_metrics(self) -> go.Figure:
        """Create interactive performance visualization"""
        
        if not self.metrics:
            self.evaluate_model()
        
        fig = go.Figure()
        
        # Add performance visualization logic here
        # This would create charts specific to the problem type
        
        return fig
