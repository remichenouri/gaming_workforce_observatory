"""
Gaming Workforce Observatory - Model Explainer Enterprise
Pipeline d'explication de modèles ML avec SHAP et visualisations gaming
"""
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
import logging
from datetime import datetime
import io
import base64

logger = logging.getLogger(__name__)

class GamingModelExplainer:
    """
    Enterprise-grade model explainer pour Gaming Workforce Observatory
    Utilise SHAP pour l'explicabilité avec visualisations gaming-spécifiques
    """
    
    def __init__(self, model, X_train: pd.DataFrame, feature_names: List[str] = None,
                 model_name: str = "GamingML_Model", problem_type: str = "classification"):
        """
        Initialize Gaming Model Explainer
        
        Args:
            model: Trained ML model
            X_train: Training data for SHAP explainer
            feature_names: Names of features
            model_name: Human-readable model name
            problem_type: 'classification' or 'regression'
        """
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names or [f'feat_{i}' for i in range(X_train.shape[1])]
        self.model_name = model_name
        self.problem_type = problem_type
        
        # SHAP components
        self.explainer = None
        self.shap_values = None
        self.base_value = None
        
        # Gaming-specific interpretations
        self.gaming_interpretations = {
            'attrition': {
                'satisfaction_score': 'Lower satisfaction strongly predicts higher attrition risk',
                'weekly_hours': 'Excessive working hours increase attrition probability',
                'years_experience': 'Mid-career professionals have highest attrition risk',
                'performance_score': 'Counter-intuitively, high performers often leave for better opportunities'
            },
            'salary': {
                'years_experience': 'Primary driver of salary - exponential relationship',
                'department': 'Programming roles command highest compensation',
                'performance_score': 'Strong correlation with salary adjustments',
                'location': 'Geographic location creates 40%+ salary variance'
            },
            'performance': {
                'training_hours': 'Investment in training shows clear performance returns',
                'manager_rating': 'Manager relationship crucial for performance outcomes',
                'project_complexity': 'Challenging projects develop higher-performing talent'
            }
        }
    
    def fit_explainer(self, sample_size: int = 100) -> None:
        """
        Fit SHAP explainer to the model
        
        Args:
            sample_size: Sample size for background data (for performance)
        """
        
        logger.info(f"Fitting SHAP explainer for {self.model_name}")
        
        try:
            # Try TreeExplainer first (for tree-based models)
            if hasattr(self.model, 'tree_'):
                self.explainer = shap.TreeExplainer(self.model)
                logger.info("Using TreeExplainer")
            
            # Try LinearExplainer for linear models
            elif hasattr(self.model, 'coef_'):
                self.explainer = shap.LinearExplainer(self.model, self.X_train)
                logger.info("Using LinearExplainer")
            
            # General Explainer (works with most models)
            else:
                background_data = shap.sample(self.X_train, sample_size)
                self.explainer = shap.Explainer(self.model, background_data)
                logger.info("Using General Explainer")
                
        except Exception as e:
            logger.warning(f"Standard explainers failed: {e}. Falling back to KernelExplainer")
            
            # Fallback to KernelExplainer (slower but works with any model)
            background_data = shap.sample(self.X_train, min(sample_size, 50))
            
            if self.problem_type == 'classification' and hasattr(self.model, 'predict_proba'):
                self.explainer = shap.KernelExplainer(self.model.predict_proba, background_data)
            else:
                self.explainer = shap.KernelExplainer(self.model.predict, background_data)
    
    def explain_predictions(self, X_explain: pd.DataFrame, 
                          max_samples: int = 100) -> np.ndarray:
        """
        Generate SHAP values for predictions
        
        Args:
            X_explain: Data to explain
            max_samples: Maximum number of samples to explain (for performance)
        
        Returns:
            SHAP values array
        """
        
        if self.explainer is None:
            self.fit_explainer()
        
        # Limit samples for performance
        if len(X_explain) > max_samples:
            X_explain_sample = X_explain.sample(max_samples, random_state=42)
            logger.warning(f"Explaining subset of {max_samples} samples for performance")
        else:
            X_explain_sample = X_explain
        
        logger.info(f"Generating SHAP values for {len(X_explain_sample)} samples")
        
        try:
            self.shap_values = self.explainer(X_explain_sample)
            
            # Extract base value
            if hasattr(self.shap_values, 'base_values'):
                self.base_value = self.shap_values.base_values
            elif hasattr(self.explainer, 'expected_value'):
                self.base_value = self.explainer.expected_value
            
            return self.shap_values
            
        except Exception as e:
            logger.error(f"Error generating SHAP values: {e}")
            raise
    
    def create_summary_plot(self, max_features: int = 20) -> go.Figure:
        """
        Create interactive summary plot using Plotly
        
        Args:
            max_features: Maximum number of features to show
        
        Returns:
            Plotly figure
        """
        
        if self.shap_values is None:
            raise ValueError("Must call explain_predictions() first")
        
        # Calculate feature importance
        if hasattr(self.shap_values, 'values'):
            shap_vals = self.shap_values.values
        else:
            shap_vals = self.shap_values
        
        # Handle multi-output (classification with probabilities)
        if len(shap_vals.shape) == 3:
            shap_vals = shap_vals[:, :, 1]  # Take positive class for binary classification
        
        # Calculate mean absolute SHAP values for feature importance
        importance = np.abs(shap_vals).mean(0)
        
        # Get top features
        top_features_idx = np.argsort(importance)[-max_features:]
        top_features = [self.feature_names[i] for i in top_features_idx]
        top_importance = importance[top_features_idx]
        
        # Create interactive bar plot
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_features,
            x=top_importance,
            orientation='h',
            marker_color='rgb(55, 83, 109)',
            name='Feature Importance'
        ))
        
        fig.update_layout(
            title=f'🎮 {self.model_name} - Feature Importance (SHAP)',
            xaxis_title='Mean |SHAP Value|',
            yaxis_title='Features',
            height=max(400, len(top_features) * 25),
            showlegend=False
        )
        
        return fig
    
    def create_waterfall_plot(self, instance_idx: int = 0) -> go.Figure:
        """
        Create waterfall plot for individual prediction explanation
        
        Args:
            instance_idx: Index of instance to explain
        
        Returns:
            Plotly figure
        """
        
        if self.shap_values is None:
            raise ValueError("Must call explain_predictions() first")
        
        # Get SHAP values for specific instance
        if hasattr(self.shap_values, 'values'):
            instance_shap = self.shap_values.values[instance_idx]
        else:
            instance_shap = self.shap_values[instance_idx]
        
        # Handle multi-output
        if len(instance_shap.shape) > 1:
            instance_shap = instance_shap[:, 1]  # Positive class
        
        # Get base value
        if isinstance(self.base_value, np.ndarray):
            base_val = self.base_value[instance_idx]
        else:
            base_val = self.base_value
        
        # Sort by absolute impact
        feature_impact = list(zip(self.feature_names, instance_shap))
        feature_impact.sort(key=lambda x: abs(x[1]), reverse=True)
        
        # Take top 15 features for readability
        top_features = feature_impact[:15]
        
        # Create waterfall data
        features = ['Base Value'] + [f[0] for f in top_features] + ['Prediction']
        values = [base_val] + [f[1] for f in top_features] + [0]
        
        # Calculate cumulative values
        cumulative = [base_val]
        for val in [f[1] for f in top_features]:
            cumulative.append(cumulative[-1] + val)
        
        final_prediction = cumulative[-1]
        cumulative.append(final_prediction)
        
        # Create waterfall plot
        fig = go.Figure()
        
        colors = ['blue'] + ['green' if v > 0 else 'red' for v in [f[1] for f in top_features]] + ['blue']
        
        for i, (feature, value, cum_val, color) in enumerate(zip(features, values, cumulative, colors)):
            fig.add_trace(go.Bar(
                x=[feature],
                y=[value if i == 0 or i == len(features)-1 else abs(value)],
                base=[0 if i == 0 or i == len(features)-1 else min(cum_val-abs(value), cum_val)],
                marker_color=color,
                name=feature,
                showlegend=False,
                text=[f"{value:.3f}"],
                textposition="outside"
            ))
        
        fig.update_layout(
            title=f'🎯 {self.model_name} - Individual Prediction Explanation',
            xaxis_title='Features',
            yaxis_title='SHAP Value',
            height=500,
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_feature_interaction_plot(self, feature1: str, feature2: str) -> go.Figure:
        """
        Create interaction plot between two features
        
        Args:
            feature1: Name of first feature
            feature2: Name of second feature
        
        Returns:
            Plotly figure
        """
        
        if feature1 not in self.feature_names or feature2 not in self.feature_names:
            raise ValueError("Features not found in feature names")
        
        idx1 = self.feature_names.index(feature1)
        idx2 = self.feature_names.index(feature2)
        
        if self.shap_values is None:
            raise ValueError("Must call explain_predictions() first")
        
        # Get feature values and SHAP values
        if hasattr(self.shap_values, 'values'):
            shap_vals = self.shap_values.values
            feature_vals = self.shap_values.data
        else:
            shap_vals = self.shap_values
            feature_vals = self.X_train.values  # Fallback
        
        # Handle multi-output
        if len(shap_vals.shape) == 3:
            shap_vals = shap_vals[:, :, 1]
        
        # Create scatter plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=feature_vals[:, idx1],
            y=feature_vals[:, idx2],
            mode='markers',
            marker=dict(
                size=8,
                color=shap_vals[:, idx1] + shap_vals[:, idx2],
                colorscale='RdBu',
                colorbar=dict(title="Combined SHAP Value"),
                line=dict(width=1, color='black')
            ),
            text=[f"SHAP {feature1}: {shap_vals[i, idx1]:.3f}<br>"
                  f"SHAP {feature2}: {shap_vals[i, idx2]:.3f}"
                  for i in range(len(shap_vals))],
            hovertemplate="%{text}<extra></extra>"
        ))
        
        fig.update_layout(
            title=f'🔄 {self.model_name} - Feature Interaction: {feature1} vs {feature2}',
            xaxis_title=feature1,
            yaxis_title=feature2,
            height=500
        )
        
        return fig
    
    def generate_gaming_insights(self) -> Dict[str, Any]:
        """
        Generate gaming-specific insights from SHAP values
        
        Returns:
            Dictionary with gaming insights
        """
        
        if self.shap_values is None:
            raise ValueError("Must call explain_predictions() first")
        
        insights = {
            'model_name': self.model_name,
            'analysis_timestamp': datetime.now().isoformat(),
            'top_factors': [],
            'gaming_interpretations': [],
            'recommendations': []
        }
        
        # Calculate global feature importance
        if hasattr(self.shap_values, 'values'):
            shap_vals = self.shap_values.values
        else:
            shap_vals = self.shap_values
        
        if len(shap_vals.shape) == 3:
            shap_vals = shap_vals[:, :, 1]  # Binary classification positive class
        
        importance = np.abs(shap_vals).mean(0)
        
        # Get top 10 features
        top_indices = np.argsort(importance)[-10:][::-1]
        
        for idx in top_indices:
            feature_name = self.feature_names[idx]
            feature_importance = importance[idx]
            
            insights['top_factors'].append({
                'feature': feature_name,
                'importance': float(feature_importance),
                'average_impact': float(shap_vals[:, idx].mean())
            })
        
        # Add gaming-specific interpretations
        model_type = self._infer_model_type()
        
        if model_type in self.gaming_interpretations:
            for feature, interpretation in self.gaming_interpretations[model_type].items():
                if any(feature.lower() in f.lower() for f in self.feature_names):
                    insights['gaming_interpretations'].append({
                        'feature': feature,
                        'interpretation': interpretation
                    })
        
        # Generate recommendations
        insights['recommendations'] = self._generate_recommendations(top_indices, importance)
        
        return insights
    
    def _infer_model_type(self) -> str:
        """Infer model type from model name"""
        
        name_lower = self.model_name.lower()
        
        if 'attrition' in name_lower or 'retention' in name_lower:
            return 'attrition'
        elif 'salary' in name_lower or 'compensation' in name_lower:
            return 'salary'
        elif 'performance' in name_lower:
            return 'performance'
        else:
            return 'general'
    
    def _generate_recommendations(self, top_indices: np.ndarray, 
                                importance: np.ndarray) -> List[str]:
        """Generate actionable recommendations based on feature importance"""
        
        recommendations = []
        
        # Get top 3 features
        top_3_features = [self.feature_names[idx] for idx in top_indices[:3]]
        
        recommendations.append(
            f"Focus data collection and quality improvement on top features: {', '.join(top_3_features)}"
        )
        
        # Model type specific recommendations
        model_type = self._infer_model_type()
        
        if model_type == 'attrition':
            recommendations.extend([
                "Implement early intervention for employees with high predicted attrition risk",
                "Monitor satisfaction scores and working hours as key attrition indicators",
                "Create retention programs targeting high-performing employees"
            ])
        
        elif model_type == 'salary':
            recommendations.extend([
                "Review compensation bands for consistency with model predictions",
                "Address any systematic salary gaps identified by the model",
                "Use model predictions for salary adjustment planning"
            ])
        
        elif model_type == 'performance':
            recommendations.extend([
                "Identify high-potential employees using model predictions",
                "Design development programs based on key performance drivers",
                "Monitor manager relationships and training investments"
            ])
        
        return recommendations
    
    def export_explanation_report(self, X_explain: pd.DataFrame,
                                max_instances: int = 5) -> Dict[str, Any]:
        """
        Export comprehensive explanation report
        
        Args:
            X_explain: Data to explain
            max_instances: Maximum instances to include in report
        
        Returns:
            Comprehensive explanation report
        """
        
        # Generate explanations if not already done
        if self.shap_values is None:
            self.explain_predictions(X_explain)
        
        report = {
            'model_info': {
                'name': self.model_name,
                'problem_type': self.problem_type,
                'features_count': len(self.feature_names),
                'explained_instances': min(len(X_explain), max_instances)
            },
            'global_explanations': self.generate_gaming_insights(),
            'feature_importance': self._get_feature_importance_summary(),
            'individual_explanations': []
        }
        
        # Add individual explanations for top instances
        for i in range(min(max_instances, len(X_explain))):
            instance_explanation = self._explain_single_instance(i, X_explain.iloc[i])
            report['individual_explanations'].append(instance_explanation)
        
        return report
    
    def _get_feature_importance_summary(self) -> Dict[str, Any]:
        """Get feature importance summary"""
        
        if self.shap_values is None:
            return {}
        
        if hasattr(self.shap_values, 'values'):
            shap_vals = self.shap_values.values
        else:
            shap_vals = self.shap_values
        
        if len(shap_vals.shape) == 3:
            shap_vals = shap_vals[:, :, 1]
        
        importance = np.abs(shap_vals).mean(0)
        
        return {
            'features': self.feature_names,
            'importance_scores': importance.tolist(),
            'top_5_features': [
                {
                    'feature': self.feature_names[idx],
                    'importance': float(importance[idx])
                }
                for idx in np.argsort(importance)[-5:][::-1]
            ]
        }
    
    def _explain_single_instance(self, instance_idx: int, 
                                instance_data: pd.Series) -> Dict[str, Any]:
        """Explain single instance"""
        
        if hasattr(self.shap_values, 'values'):
            instance_shap = self.shap_values.values[instance_idx]
        else:
            instance_shap = self.shap_values[instance_idx]
        
        if len(instance_shap.shape) > 1:
            instance_shap = instance_shap[:, 1]
        
        # Get top contributing features
        top_positive = []
        top_negative = []
        
        for i, (feature, shap_val) in enumerate(zip(self.feature_names, instance_shap)):
            contribution = {
                'feature': feature,
                'value': float(instance_data.iloc[i]) if hasattr(instance_data, 'iloc') else float(instance_data[i]),
                'shap_value': float(shap_val)
            }
            
            if shap_val > 0:
                top_positive.append(contribution)
            else:
                top_negative.append(contribution)
        
        top_positive.sort(key=lambda x: x['shap_value'], reverse=True)
        top_negative.sort(key=lambda x: x['shap_value'])
        
        return {
            'instance_index': instance_idx,
            'top_positive_contributions': top_positive[:5],
            'top_negative_contributions': top_negative[:5],
            'prediction_explanation': self._create_prediction_explanation(
                top_positive[:3], top_negative[:3]
            )
        }
    
    def _create_prediction_explanation(self, top_positive: List[Dict], 
                                     top_negative: List[Dict]) -> str:
        """Create human-readable prediction explanation"""
        
        explanation_parts = []
        
        if top_positive:
            pos_features = [f"{contrib['feature']} (impact: {contrib['shap_value']:.3f})" 
                           for contrib in top_positive]
            explanation_parts.append(f"Factors increasing prediction: {', '.join(pos_features)}")
        
        if top_negative:
            neg_features = [f"{contrib['feature']} (impact: {contrib['shap_value']:.3f})" 
                           for contrib in top_negative]
            explanation_parts.append(f"Factors decreasing prediction: {', '.join(neg_features)}")
        
        return ". ".join(explanation_parts)
