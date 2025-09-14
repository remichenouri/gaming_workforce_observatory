"""
Gaming Workforce Observatory - Alert System
Advanced alerting for gaming industry workforce metrics
"""

import logging
import smtplib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import pandas as pd
import requests
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels for gaming workforce metrics"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertCategory(Enum):
    """Gaming industry specific alert categories"""
    PERFORMANCE = "performance"
    RETENTION = "retention"
    WELLBEING = "wellbeing"
    QUALITY = "quality"
    DEVELOPMENT = "development"
    CRUNCH = "crunch"

@dataclass
class GamingAlert:
    """Gaming industry workforce alert data structure"""
    alert_id: str
    title: str
    description: str
    severity: AlertSeverity
    category: AlertCategory
    department: str
    affected_employees: List[str]
    gaming_context: Dict[str, Union[str, float]]
    recommendations: List[str]
    created_at: datetime
    requires_action: bool = True
    gaming_phase_context: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert alert to dictionary for serialization"""
        data = asdict(self)
        data['severity'] = self.severity.value
        data['category'] = self.category.value
        data['created_at'] = self.created_at.isoformat()
        return data

class GamingAlertEngine:
    """Main alerting engine for gaming workforce analytics"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._load_default_config()
        self.alert_thresholds = self._load_gaming_thresholds()
        self.alert_channels = self._initialize_channels()
        self.active_alerts: List[GamingAlert] = []
        
    def _load_default_config(self) -> Dict:
        """Load default gaming industry alert configuration"""
        return {
            'email': {
                'enabled': True,
                'smtp_server': 'localhost',
                'smtp_port': 587,
                'from_address': 'alerts@gaming-workforce-observatory.com'
            },
            'slack': {
                'enabled': True,
                'webhook_url': None,
                'channel': '#gaming-workforce-alerts'
            },
            'gaming_contexts': {
                'crunch_season': {'multiplier': 1.5, 'priority_boost': True},
                'pre_launch': {'multiplier': 1.3, 'priority_boost': True},
                'post_launch': {'multiplier': 0.8, 'priority_boost': False}
            }
        }
    
    def _load_gaming_thresholds(self) -> Dict:
        """Load gaming industry specific alert thresholds"""
        return {
            'satisfaction': {
                'critical': 6.0,
                'high': 6.5,
                'medium': 7.0,
                'gaming_adjustment': 0.5  # Gaming industry tends to be more demanding
            },
            'turnover_risk': {
                'critical': 0.8,
                'high': 0.7,
                'medium': 0.5,
                'gaming_context_weight': 1.2
            },
            'sprint_velocity': {
                'critical_drop': 0.3,  # 30% drop from baseline
                'high_drop': 0.2,
                'medium_drop': 0.1,
                'gaming_baseline': 40  # Gaming industry average
            },
            'bug_fix_rate': {
                'critical': 70,
                'high': 75,
                'medium': 80,
                'gaming_quality_standard': 85
            },
            'crunch_hours': {
                'critical': 70,  # hours per month
                'high': 60,
                'medium': 50,
                'gaming_baseline': 40
            },
            'team_synergy': {
                'critical': 5.0,
                'high': 6.0,
                'medium': 7.0,
                'gaming_collaboration_target': 8.0
            }
        }
    
    def _initialize_channels(self) -> Dict:
        """Initialize alert delivery channels"""
        channels = {}
        
        if self.config.get('email', {}).get('enabled'):
            channels['email'] = EmailAlertChannel(self.config['email'])
        
        if self.config.get('slack', {}).get('enabled'):
            channels['slack'] = SlackAlertChannel(self.config['slack'])
            
        return channels
    
    def check_gaming_workforce_alerts(self, df: pd.DataFrame) -> List[GamingAlert]:
        """Main method to check for gaming workforce alerts"""
        alerts = []
        
        # Check different gaming-specific alert categories
        alerts.extend(self._check_satisfaction_alerts(df))
        alerts.extend(self._check_turnover_alerts(df))
        alerts.extend(self._check_performance_alerts(df))
        alerts.extend(self._check_crunch_alerts(df))
        alerts.extend(self._check_quality_alerts(df))
        alerts.extend(self._check_team_synergy_alerts(df))
        
        # Apply gaming context adjustments
        alerts = self._apply_gaming_context_adjustments(alerts)
        
        # Store active alerts
        self.active_alerts.extend(alerts)
        
        return alerts
    
    def _check_satisfaction_alerts(self, df: pd.DataFrame) -> List[GamingAlert]:
        """Check for gaming employee satisfaction alerts"""
        alerts = []
        thresholds = self.alert_thresholds['satisfaction']
        
        # Overall satisfaction check
        avg_satisfaction = df['satisfaction_score'].mean()
        
        if avg_satisfaction < thresholds['critical']:
            alerts.append(GamingAlert(
                alert_id=f"satisfaction_critical_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title="Critical: Gaming Workforce Satisfaction Crisis",
                description=f"Average satisfaction ({avg_satisfaction:.1f}/10) below critical threshold",
                severity=AlertSeverity.CRITICAL,
                category=AlertCategory.WELLBEING,
                department="All",
                affected_employees=df[df['satisfaction_score'] < thresholds['critical']]['name'].tolist(),
                gaming_context={
                    'satisfaction_score': avg_satisfaction,
                    'gaming_industry_average': 7.2,
                    'departments_affected': df.groupby('department')['satisfaction_score'].mean().to_dict(),
                    'potential_impact': "High turnover risk, reduced productivity, poor game quality"
                },
                recommendations=[
                    "Immediate all-hands meeting to address concerns",
                    "Review current crunch periods and workload distribution", 
                    "Implement emergency wellness programs",
                    "Consider hiring additional resources to reduce pressure",
                    "Gaming industry survey: compare to industry standards"
                ],
                created_at=datetime.now(),
                gaming_phase_context=self._determine_gaming_phase()
            ))
        
        # Department-specific satisfaction alerts
        dept_satisfaction = df.groupby('department')['satisfaction_score'].mean()
        for dept, satisfaction in dept_satisfaction.items():
            if satisfaction < thresholds['high']:
                severity = AlertSeverity.CRITICAL if satisfaction < thresholds['critical'] else AlertSeverity.HIGH
                
                alerts.append(GamingAlert(
                    alert_id=f"dept_satisfaction_{dept}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    title=f"Gaming {dept} Department Satisfaction Alert",
                    description=f"{dept} team satisfaction ({satisfaction:.1f}) needs attention",
                    severity=severity,
                    category=AlertCategory.WELLBEING,
                    department=dept,
                    affected_employees=df[(df['department'] == dept) & 
                                        (df['satisfaction_score'] < thresholds['medium'])]['name'].tolist(),
                    gaming_context={
                        'department_satisfaction': satisfaction,
                        'company_average': avg_satisfaction,
                        'gaming_role_specific': self._get_gaming_role_context(dept),
                        'workload_factor': self._calculate_workload_impact(df, dept)
                    },
                    recommendations=self._get_department_specific_recommendations(dept, satisfaction),
                    created_at=datetime.now(),
                    gaming_phase_context=self._determine_gaming_phase()
                ))
        
        return alerts
    
    def _check_turnover_alerts(self, df: pd.DataFrame) -> List[GamingAlert]:
        """Check for gaming industry turnover risk alerts"""
        alerts = []
        
        if 'flight_risk' not in df.columns:
            return alerts
        
        thresholds = self.alert_thresholds['turnover_risk']
        high_risk_employees = df[df['flight_risk'] > thresholds['high']]
        
        if not high_risk_employees.empty:
            gaming_talent_risk = self._assess_gaming_talent_risk(high_risk_employees)
            
            alerts.append(GamingAlert(
                alert_id=f"turnover_risk_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title="High Gaming Talent Flight Risk Detected",
                description=f"{len(high_risk_employees)} employees at high risk of leaving",
                severity=AlertSeverity.HIGH if len(high_risk_employees) < 5 else AlertSeverity.CRITICAL,
                category=AlertCategory.RETENTION,
                department="Multiple" if high_risk_employees['department'].nunique() > 1 else high_risk_employees['department'].iloc[0],
                affected_employees=high_risk_employees['name'].tolist(),
                gaming_context={
                    'high_risk_count': len(high_risk_employees),
                    'gaming_talent_categories': gaming_talent_risk,
                    'average_risk_score': high_risk_employees['flight_risk'].mean(),
                    'departments_impacted': high_risk_employees['department'].value_counts().to_dict(),
                    'gaming_experience_at_risk': high_risk_employees['years_experience'].sum()
                },
                recommendations=[
                    "Schedule immediate 1:1 meetings with at-risk employees",
                    "Review compensation against gaming industry standards",
                    "Assess workload and crunch period impact",
                    "Consider retention bonuses or gaming-specific perks",
                    "Implement gaming career development discussions",
                    "Evaluate team dynamics and gaming culture fit"
                ],
                created_at=datetime.now()
            ))
        
        return alerts
    
    def _check_crunch_alerts(self, df: pd.DataFrame) -> List[GamingAlert]:
        """Check for gaming industry crunch period alerts"""
        alerts = []
        
        if 'crunch_hours_last_month' not in df.columns:
            return alerts
        
        thresholds = self.alert_thresholds['crunch_hours']
        
        # Identify employees in excessive crunch
        crunch_employees = df[df['crunch_hours_last_month'] > thresholds['high']]
        
        if not crunch_employees.empty:
            crunch_analysis = self._analyze_crunch_impact(crunch_employees)
            
            alerts.append(GamingAlert(
                alert_id=f"crunch_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title="Gaming Crunch Period Alert",
                description=f"{len(crunch_employees)} employees in excessive crunch",
                severity=AlertSeverity.HIGH,
                category=AlertCategory.CRUNCH,
                department="Multiple" if crunch_employees['department'].nunique() > 1 else crunch_employees['department'].iloc[0],
                affected_employees=crunch_employees['name'].tolist(),
                gaming_context={
                    'employees_in_crunch': len(crunch_employees),
                    'average_crunch_hours': crunch_employees['crunch_hours_last_month'].mean(),
                    'max_crunch_hours': crunch_employees['crunch_hours_last_month'].max(),
                    'crunch_by_department': crunch_employees.groupby('department')['crunch_hours_last_month'].mean().to_dict(),
