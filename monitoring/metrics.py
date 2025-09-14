"""
Gaming Workforce Observatory - Metrics Collection
Advanced metrics collection for gaming industry workforce analytics
"""

import time
import psutil
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import logging
from pathlib import Path
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GamingMetric:
    """Gaming industry specific metric data structure"""
    name: str
    value: Union[float, int, str]
    unit: str
    category: str
    gaming_context: Dict[str, Any]
    timestamp: datetime
    department: Optional[str] = None
    gaming_phase: Optional[str] = None

class GamingMetricsCollector:
    """Comprehensive metrics collection for gaming workforce analytics"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.metrics_history: List[GamingMetric] = []
        self.gaming_thresholds = self._load_gaming_thresholds()
        
    def _load_gaming_thresholds(self) -> Dict:
        """Load gaming industry specific thresholds"""
        return {
            'performance': {
                'page_load_time': 2.0,  # seconds
                'chart_rendering': 0.5,  # seconds
                'filter_response': 0.1,  # seconds
                'ml_prediction': 3.0,    # seconds
            },
            'gaming_kpis': {
                'sprint_velocity': 40.0,
                'bug_fix_rate': 85.0,
                'satisfaction': 7.5,
                'retention_rate': 0.85,
                'innovation_index': 75.0
            },
            'system': {
                'cpu_usage': 80.0,
                'memory_usage': 80.0,
                'disk_usage': 80.0,
                'cache_hit_rate': 85.0
            }
        }
    
    def collect_performance_metrics(self) -> Dict[str, GamingMetric]:
        """Collect application performance metrics"""
        metrics = {}
        
        # Page load time simulation
        start_time = time.time()
        # Simulate dashboard loading
        time.sleep(0.001)  # Minimal delay for simulation
        load_time = time.time() - start_time
        
        metrics['page_load_time'] = GamingMetric(
            name="Dashboard Load Time",
            value=round(load_time * 1000, 2),  # Convert to milliseconds
            unit="milliseconds",
            category="performance",
            gaming_context={
                "target": 2000,  # 2 seconds in ms
                "status": "excellent" if load_time < 1.0 else "good" if load_time < 2.0 else "poor",
                "gaming_impact": "Fast loading critical for real-time gaming analytics"
            },
            timestamp=datetime.now()
        )
        
        # Chart rendering time
        chart_render_time = np.random.uniform(0.2, 0.8)  # Simulated
        metrics['chart_rendering'] = GamingMetric(
            name="Chart Rendering Time",
            value=round(chart_render_time * 1000, 2),
            unit="milliseconds", 
            category="performance",
            gaming_context={
                "target": 500,
                "chart_types": ["plotly_gaming_velocity", "plotly_satisfaction_heatmap"],
                "gaming_optimization": "Gaming-themed charts with performance focus"
            },
            timestamp=datetime.now()
        )
        
        return metrics
    
    def collect_gaming_kpi_metrics(self, df: pd.DataFrame) -> Dict[str, GamingMetric]:
        """Collect gaming industry specific KPI metrics"""
        metrics = {}
        
        if df.empty:
            return metrics
        
        # Sprint Velocity
        if 'sprint_velocity' in df.columns:
            avg_velocity = df['sprint_velocity'].mean()
            metrics['sprint_velocity'] = GamingMetric(
                name="Average Sprint Velocity",
                value=round(avg_velocity, 1),
                unit="story_points",
                category="gaming_development",
                gaming_context={
                    "industry_average": 38.5,
                    "target": 40.0,
                    "departments": df.groupby('department')['sprint_velocity'].mean().to_dict(),
                    "gaming_methodology": "Agile/Scrum adapted for game development"
                },
                timestamp=datetime.now()
            )
        
        # Bug Fix Rate
        if 'bug_fix_rate' in df.columns:
            avg_bug_fix = df['bug_fix_rate'].mean()
            metrics['bug_fix_rate'] = GamingMetric(
                name="Bug Fix Rate",
                value=round(avg_bug_fix, 1),
                unit="percentage",
                category="gaming_quality",
                gaming_context={
                    "industry_standard": 85.0,
                    "qa_teams": df[df['department'] == 'QA']['bug_fix_rate'].mean(),
                    "programming_teams": df[df['department'] == 'Programming']['bug_fix_rate'].mean(),
                    "gaming_quality_impact": "Critical for game stability and user experience"
                },
                timestamp=datetime.now()
            )
        
        # Gaming Satisfaction Score
        if 'satisfaction_score' in df.columns:
            avg_satisfaction = df['satisfaction_score'].mean()
            metrics['gaming_satisfaction'] = GamingMetric(
                name="Gaming Workforce Satisfaction",
                value=round(avg_satisfaction, 1),
                unit="score_10",
                category="gaming_wellbeing",
                gaming_context={
                    "gaming_industry_average": 7.2,
                    "crunch_impact_adjusted": True,
                    "department_breakdown": df.groupby('department')['satisfaction_score'].mean().to_dict(),
                    "gaming_culture_factors": ["work_life_balance", "creative_freedom", "team_collaboration"]
                },
                timestamp=datetime.now()
            )
        
        # Innovation Index
        if 'innovation_index' in df.columns:
            avg_innovation = df['innovation_index'].mean()
            metrics['innovation_index'] = GamingMetric(
                name="Gaming Innovation Index",
                value=round(avg_innovation, 1),
                unit="score_100",
                category="gaming_creativity",
                gaming_context={
                    "creative_departments": ["Game Design", "Art", "Programming"],
                    "innovation_types": ["gameplay_features", "technical_solutions", "artistic_concepts"],
                    "gaming_ip_potential": "New ideas that could become game features or IP"
                },
                timestamp=datetime.now()
            )
        
        return metrics
    
    def collect_system_metrics(self) -> Dict[str, GamingMetric]:
        """Collect system performance metrics"""
        metrics = {}
        
        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics['cpu_usage'] = GamingMetric(
            name="CPU Usage",
            value=cpu_percent,
            unit="percentage",
            category="system",
            gaming_context={
                "threshold": 80.0,
                "status": "good" if cpu_percent < 70 else "warning" if cpu_percent < 80 else "critical",
                "gaming_workload": "Analytics processing for gaming workforce data"
            },
            timestamp=datetime.now()
        )
        
        # Memory Usage
        memory = psutil.virtual_memory()
        metrics['memory_usage'] = GamingMetric(
            name="Memory Usage",
            value=memory.percent,
            unit="percentage",
            category="system",
            gaming_context={
                "available_mb": memory.available // 1024 // 1024,
                "gaming_data_size": "Large gaming workforce datasets in memory",
                "caching_impact": "Streamlit caching for gaming analytics performance"
            },
            timestamp=datetime.now()
        )
        
        # Disk Usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        metrics['disk_usage'] = GamingMetric(
            name="Disk Usage",
            value=round(disk_percent, 1),
            unit="percentage",
            category="system",
            gaming_context={
                "free_gb": disk.free // 1024 // 1024 // 1024,
                "gaming_data_storage": "Employee data, gaming metrics, ML models",
                "backup_space": "Gaming workforce data backups"
            },
            timestamp=datetime.now()
        )
        
        return metrics
    
    def collect_gaming_team_metrics(self, df: pd.DataFrame) -> Dict[str, GamingMetric]:
        """Collect gaming team-specific metrics"""
        metrics = {}
        
        if df.empty:
            return metrics
        
        # Team size distribution
        team_sizes = df.groupby('department').size()
        metrics['team_distribution'] = GamingMetric(
            name="Gaming Team Distribution",
            value=team_sizes.to_dict(),
            unit="employees",
            category="gaming_teams",
            gaming_context={
                "ideal_ratios": {
                    "Programming": 0.35,
                    "Art": 0.25,
                    "Game Design": 0.15,
                    "QA": 0.15,
                    "Management": 0.10
                },
                "studio_size": len(df),
                "studio_type": self._classify_studio_size(len(df))
            },
            timestamp=datetime.now()
        )
        
        # Experience distribution
        if 'years_experience' in df.columns:
            exp_distribution = {
                'Junior (0-2 years)': len(df[df['years_experience'] <= 2]),
                'Mid (3-5 years)': len(df[(df['years_experience'] > 2) & (df['years_experience'] <= 5)]),
                'Senior (6+ years)': len(df[df['years_experience'] > 5])
            }
            
            metrics['experience_distribution'] = GamingMetric(
                name="Gaming Experience Distribution",
                value=exp_distribution,
                unit="employees",
                category="gaming_talent",
                gaming_context={
                    "senior_ratio": exp_distribution['Senior (6+ years)'] / len(df),
                    "mentorship_capacity": "Senior developers available for junior mentoring",
                    "gaming_expertise_depth": "Years of gaming industry specific experience"
                },
                timestamp=datetime.now()
            )
        
        return metrics
    
    def _classify_studio_size(self, employee_count: int) -> str:
        """Classify gaming studio size"""
        if employee_count <= 20:
            return "Indie Studio"
        elif employee_count <= 100:
            return "Mid-size Studio"
        else:
            return "AAA Studio"
    
    def collect_ml_performance_metrics(self) -> Dict[str, GamingMetric]:
        """Collect ML model performance metrics"""
        metrics = {}
        
        # Simulated ML metrics (in real implementation, these would come from actual models)
        turnover_model_accuracy = 0.82
        burnout_model_accuracy = 0.78
        
        metrics['ml_turnover_accuracy'] = GamingMetric(
            name="Turnover Prediction Accuracy",
            value=turnover_model_accuracy,
            unit="accuracy_score",
            category="gaming_ml",
            gaming_context={
                "model_type": "RandomForestClassifier",
                "gaming_features": ["satisfaction", "crunch_hours", "sprint_velocity"],
                "industry_benchmark": 0.75,
                "gaming_specific_training": "Trained on gaming industry workforce data"
            },
            timestamp=datetime.now()
        )
        
        metrics['ml_burnout_accuracy'] = GamingMetric(
            name="Burnout Risk Accuracy",
            value=burnout_model_accuracy,
            unit="accuracy_score",
            category="gaming_ml",
            gaming_context={
                "model_type": "GradientBoostingClassifier",
                "crunch_sensitivity": "High sensitivity to gaming crunch periods",
                "early_warning": "Detects burnout risk 2-4 weeks in advance"
            },
            timestamp=datetime.now()
        )
        
        return metrics
    
    def generate_metrics_report(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Generate comprehensive metrics report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'gaming_context': 'Gaming Workforce Observatory Metrics',
            'categories': {}
        }
        
        # Collect all metrics
        all_metrics = {}
        all_metrics.update(self.collect_performance_metrics())
        all_metrics.update(self.collect_system_metrics())
        all_metrics.update(self.collect_ml_performance_metrics())
        
        if df is not None:
            all_metrics.update(self.collect_gaming_kpi_metrics(df))
            all_metrics.update(self.collect_gaming_team_metrics(df))
        
        # Group metrics by category
        for metric_name, metric in all_metrics.items():
            category = metric.category
            if category not in report['categories']:
                report['categories'][category] = []
            
            report['categories'][category].append({
                'name': metric.name,
                'value': metric.value,
                'unit': metric.unit,
                'gaming_context': metric.gaming_context,
                'timestamp': metric.timestamp.isoformat()
            })
        
        # Add summary
        report['summary'] = {
            'total_metrics': len(all_metrics),
            'categories_count': len(report['categories']),
            'gaming_focus': 'Metrics specifically designed for gaming industry workforce analytics',
            'collection_duration': 'Real-time collection with gaming context'
        }
        
        return report
    
    def export_metrics_to_csv(self, filepath: str) -> None:
        """Export metrics to CSV for analysis"""
        if not self.metrics_history:
            logger.warning("No metrics to export")
            return
        
        metrics_data = []
        for metric in self.metrics_history:
            metrics_data.append({
                'name': metric.name,
                'value': metric.value,
                'unit': metric.unit,
                'category': metric.category,
                'department': metric.department,
                'gaming_phase': metric.gaming_phase,
                'timestamp': metric.timestamp
            })
        
        df = pd.DataFrame(metrics_data)
        df.to_csv(filepath, index=False)
        logger.info(f"Gaming metrics exported to {filepath}")

def main():
    """Example usage of Gaming Metrics Collector"""
    collector = GamingMetricsCollector()
    
    # Create sample gaming workforce data
    sample_data = pd.DataFrame({
        'employee_id': range(1, 101),
        'department': np.random.choice(['Programming', 'Art', 'Game Design', 'QA'], 100),
        'satisfaction_score': np.random.uniform(6.0, 9.0, 100),
        'sprint_velocity': np.random.uniform(25, 55, 100),
        'bug_fix_rate': np.random.uniform(70, 95, 100),
        'innovation_index': np.random.uniform(50, 90, 100),
        'years_experience': np.random.randint(0, 15, 100)
    })
    
    # Generate comprehensive report
    report = collector.generate_metrics_report(sample_data)
    
    # Print gaming-focused summary
    print("🎮 Gaming Workforce Observatory - Metrics Report")
    print("=" * 50)
    print(f"📊 Total Metrics: {report['summary']['total_metrics']}")
    print(f"📋 Categories: {report['summary']['categories_count']}")
    print(f"🎯 Gaming Focus: {report['summary']['gaming_focus']}")
    
    # Show key gaming metrics
    if 'gaming_development' in report['categories']:
        print("\n🚀 Gaming Development Metrics:")
        for metric in report['categories']['gaming_development']:
            print(f"  • {metric['name']}: {metric['value']} {metric['unit']}")
    
    if 'gaming_quality' in report['categories']:
        print("\n🎯 Gaming Quality Metrics:")
        for metric in report['categories']['gaming_quality']:
            print(f"  • {metric['name']}: {metric['value']} {metric['unit']}")

if __name__ == "__main__":
    main()
