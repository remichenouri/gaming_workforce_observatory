"""
Gaming Workforce Observatory - Performance Tracker Enterprise
Suivi des performances ML dans le temps avec alertes gaming-spécifiques
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
import json
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types de métriques supportées"""
    ACCURACY = "accuracy"
    ROC_AUC = "roc_auc"
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1_score"
    MSE = "mse"
    RMSE = "rmse"
    MAE = "mae"
    R2_SCORE = "r2_score"
    ATTRITION_PRECISION = "attrition_precision"
    SALARY_MAPE = "salary_mape"
    CUSTOM = "custom"

class AlertLevel(Enum):
    """Niveaux d'alerte"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class PerformanceAlert:
    """Structure d'alerte de performance"""
    timestamp: datetime
    model_name: str
    metric_name: str
    current_value: float
    threshold_value: float
    alert_level: AlertLevel
    message: str

class GamingPerformanceTracker:
    """Tracker de performance pour modèles ML gaming workforce"""
    
    def __init__(self, db_path: str = "model_performance.db"):
        """
        Initialize Performance Tracker
        
        Args:
            db_path: Path to SQLite database for storing metrics
        """
        self.db_path = db_path
        self.performance_log = pd.DataFrame()
        self.alerts_log = []
        
        # Gaming-specific performance thresholds
        self.thresholds = {
            'attrition_model': {
                'roc_auc': {'warning': 0.75, 'critical': 0.70},
                'precision': {'warning': 0.80, 'critical': 0.75}
            },
            'salary_model': {
                'r2_score': {'warning': 0.75, 'critical': 0.70},
                'mape': {'warning': 15.0, 'critical': 20.0}  # Higher is worse
            },
            'performance_model': {
                'r2_score': {'warning': 0.70, 'critical': 0.65},
                'mae': {'warning': 0.5, 'critical': 0.7}  # Higher is worse
            }
        }
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for performance tracking"""
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS model_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    model_name TEXT NOT NULL,
                    model_version TEXT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    dataset_size INTEGER,
                    data_quality_score REAL,
                    drift_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    model_name TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    current_value REAL NOT NULL,
                    threshold_value REAL NOT NULL,
                    alert_level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    resolved BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for better performance
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_model_performance_timestamp 
                ON model_performance(timestamp)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_model_performance_model_name 
                ON model_performance(model_name)
            """)
    
    def log_metric(self, model_name: str, metric_name: str, metric_value: float,
                   model_version: str = None, dataset_size: int = None,
                   data_quality_score: float = None, drift_score: float = None,
                   timestamp: datetime = None) -> None:
        """
        Log a performance metric
        
        Args:
            model_name: Name of the model
            metric_name: Name of the metric (accuracy, roc_auc, etc.)
            metric_value: Value of the metric
            model_version: Version of the model
            dataset_size: Size of the evaluation dataset
            data_quality_score: Quality score of the data (0-1)
            drift_score: Data drift score (0-1)
            timestamp: Timestamp of the metric (defaults to now)
        """
        
        if timestamp is None:
            timestamp = datetime.now()
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO model_performance 
                (timestamp, model_name, model_version, metric_name, metric_value, 
                 dataset_size, data_quality_score, drift_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp.isoformat(), model_name, model_version, metric_name,
                metric_value, dataset_size, data_quality_score, drift_score
            ))
        
        # Check for alerts
        self._check_performance_alert(model_name, metric_name, metric_value, timestamp)
        
        logger.info(f"Logged metric: {model_name}.{metric_name} = {metric_value}")
    
    def _check_performance_alert(self, model_name: str, metric_name: str, 
                                metric_value: float, timestamp: datetime) -> None:
        """Check if metric triggers performance alert"""
        
        # Determine model type from name
        model_type = self._get_model_type(model_name)
        
        if model_type not in self.thresholds:
            return
        
        if metric_name not in self.thresholds[model_type]:
            return
        
        thresholds = self.thresholds[model_type][metric_name]
        
        # Check for critical alert
        if self._is_metric_below_threshold(metric_name, metric_value, thresholds['critical']):
            self._create_alert(
                timestamp, model_name, metric_name, metric_value, 
                thresholds['critical'], AlertLevel.CRITICAL,
                f"Critical performance degradation: {metric_name} = {metric_value:.4f}"
            )
        
        # Check for warning alert
        elif self._is_metric_below_threshold(metric_name, metric_value, thresholds['warning']):
            self._create_alert(
                timestamp, model_name, metric_name, metric_value,
                thresholds['warning'], AlertLevel.WARNING,
                f"Performance warning: {metric_name} = {metric_value:.4f}"
            )
    
    def _is_metric_below_threshold(self, metric_name: str, value: float, threshold: float) -> bool:
        """Check if metric is below threshold (considering if lower is worse)"""
        
        # Metrics where lower values are worse
        higher_is_better = ['accuracy', 'roc_auc', 'precision', 'recall', 'f1_score', 'r2_score']
        # Metrics where higher values are worse  
        lower_is_better = ['mse', 'rmse', 'mae', 'mape']
        
        if any(metric in metric_name.lower() for metric in higher_is_better):
            return value < threshold
        elif any(metric in metric_name.lower() for metric in lower_is_better):
            return value > threshold
        else:
            # Default: assume higher is better
            return value < threshold
    
    def _get_model_type(self, model_name: str) -> str:
        """Infer model type from model name"""
        
        name_lower = model_name.lower()
        
        if 'attrition' in name_lower or 'retention' in name_lower:
            return 'attrition_model'
        elif 'salary' in name_lower or 'compensation' in name_lower:
            return 'salary_model'
        elif 'performance' in name_lower:
            return 'performance_model'
        else:
            return 'generic_model'
    
    def _create_alert(self, timestamp: datetime, model_name: str, metric_name: str,
                     current_value: float, threshold_value: float, alert_level: AlertLevel,
                     message: str) -> None:
        """Create and store performance alert"""
        
        alert = PerformanceAlert(
            timestamp=timestamp,
            model_name=model_name,
            metric_name=metric_name,
            current_value=current_value,
            threshold_value=threshold_value,
            alert_level=alert_level,
            message=message
        )
        
        self.alerts_log.append(alert)
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO performance_alerts 
                (timestamp, model_name, metric_name, current_value, 
                 threshold_value, alert_level, message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp.isoformat(), model_name, metric_name, current_value,
                threshold_value, alert_level.value, message
            ))
        
        logger.warning(f"Performance alert: {alert_level.value} - {message}")
    
    def get_performance_history(self, model_name: str = None, metric_name: str = None,
                              start_date: datetime = None, end_date: datetime = None,
                              limit: int = 1000) -> pd.DataFrame:
        """
        Retrieve performance history from database
        
        Args:
            model_name: Filter by model name
            metric_name: Filter by metric name
            start_date: Start date for filtering
            end_date: End date for filtering
            limit: Maximum number of records to return
        
        Returns:
            DataFrame with performance history
        """
        
        query = "SELECT * FROM model_performance WHERE 1=1"
        params = []
        
        if model_name:
            query += " AND model_name = ?"
            params.append(model_name)
        
        if metric_name:
            query += " AND metric_name = ?"
            params.append(metric_name)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def plot_metric_trend(self, model_name: str, metric_name: str,
                         days: int = 30) -> go.Figure:
        """
        Plot metric trend over time
        
        Args:
            model_name: Name of the model
            metric_name: Name of the metric
            days: Number of days to plot
        
        Returns:
            Plotly figure
        """
        
        start_date = datetime.now() - timedelta(days=days)
        df = self.get_performance_history(
            model_name=model_name,
            metric_name=metric_name,
            start_date=start_date
        )
        
        if df.empty:
            # Return empty figure with message
            fig = go.Figure()
            fig.add_annotation(
                text=f"No data available for {model_name}.{metric_name}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Create trend plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['metric_value'],
            mode='lines+markers',
            name=f'{metric_name}',
            line=dict(color='#0082c4', width=3),
            marker=dict(size=8)
        ))
        
        # Add threshold lines if available
        model_type = self._get_model_type(model_name)
        if model_type in self.thresholds and metric_name in self.thresholds[model_type]:
            thresholds = self.thresholds[model_type][metric_name]
            
            # Warning threshold
            fig.add_hline(
                y=thresholds['warning'],
                line_dash="dash",
                line_color="orange",
                annotation_text="Warning Threshold"
            )
            
            # Critical threshold
            fig.add_hline(
                y=thresholds['critical'],
                line_dash="dash",
                line_color="red",
                annotation_text="Critical Threshold"
            )
        
        fig.update_layout(
            title=f'{model_name} - {metric_name} Performance Trend',
            xaxis_title='Date',
            yaxis_title=metric_name,
            height=400
        )
        
        return fig
    
    def get_model_summary(self, model_name: str, days: int = 30) -> Dict[str, Any]:
        """
        Get performance summary for a model
        
        Args:
            model_name: Name of the model
            days: Number of days to analyze
        
        Returns:
            Dictionary with model performance summary
        """
        
        start_date = datetime.now() - timedelta(days=days)
        df = self.get_performance_history(
            model_name=model_name,
            start_date=start_date
        )
        
        if df.empty:
            return {'error': 'No performance data available'}
        
        summary = {}
        
        # Overall metrics
        summary['total_evaluations'] = len(df)
        summary['date_range'] = {
            'start': df['timestamp'].min().isoformat(),
            'end': df['timestamp'].max().isoformat()
        }
        
        # Metric-wise summary
        metrics_summary = {}
        for metric in df['metric_name'].unique():
            metric_data = df[df['metric_name'] == metric]
            
            metrics_summary[metric] = {
                'current_value': float(metric_data.iloc[0]['metric_value']),
                'average_value': float(metric_data['metric_value'].mean()),
                'min_value': float(metric_data['metric_value'].min()),
                'max_value': float(metric_data['metric_value'].max()),
                'trend': self._calculate_trend(metric_data['metric_value'])
            }
        
        summary['metrics'] = metrics_summary
        
        # Recent alerts
        recent_alerts = [
            {
                'timestamp': alert.timestamp.isoformat(),
                'metric_name': alert.metric_name,
                'alert_level': alert.alert_level.value,
                'message': alert.message
            }
            for alert in self.alerts_log
            if alert.model_name == model_name and 
               alert.timestamp >= start_date
        ]
        
        summary['recent_alerts'] = recent_alerts
        summary['alert_count'] = len(recent_alerts)
        
        return summary
    
    def _calculate_trend(self, values: pd.Series) -> str:
        """Calculate trend direction for metric values"""
        
        if len(values) < 2:
            return 'insufficient_data'
        
        # Simple linear regression to determine trend
        x = np.arange(len(values))
        y = values.values
        
        # Calculate slope
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0.001:
            return 'improving'
        elif slope < -0.001:
            return 'degrading'
        else:
            return 'stable'
    
    def export_performance_report(self, model_name: str = None, 
                                days: int = 30) -> Dict[str, Any]:
        """
        Export comprehensive performance report
        
        Args:
            model_name: Model to analyze (if None, analyzes all models)
            days: Number of days to analyze
        
        Returns:
            Dictionary with comprehensive performance report
        """
        
        start_date = datetime.now() - timedelta(days=days)
        
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'period_days': days,
                'start_date': start_date.isoformat(),
                'model_filter': model_name
            },
            'models_summary': {}
        }
        
        # Get all models or specific model
        df = self.get_performance_history(
            model_name=model_name,
            start_date=start_date,
            limit=10000
        )
        
        if df.empty:
            report['error'] = 'No performance data available for the specified period'
            return report
        
        # Analyze each model
        for model in df['model_name'].unique():
            report['models_summary'][model] = self.get_model_summary(model, days)
        
        # Overall statistics
        report['overall_statistics'] = {
            'total_models': len(df['model_name'].unique()),
            'total_evaluations': len(df),
            'total_alerts': len([a for a in self.alerts_log if a.timestamp >= start_date]),
            'models_with_alerts': len(set([a.model_name for a in self.alerts_log if a.timestamp >= start_date]))
        }
        
        return report
