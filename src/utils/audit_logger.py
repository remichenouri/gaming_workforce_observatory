"""
Gaming Workforce Observatory - Audit Logger Enterprise
Système de logging d'audit complet avec traçabilité gaming
"""
import logging
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import streamlit as st
from pathlib import Path
import pandas as pd
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import threading
from contextlib import contextmanager

class AuditEventType(Enum):
    """Types d'événements d'audit"""
    LOGIN = "login"
    LOGOUT = "logout"
    DATA_ACCESS = "data_access"
    DATA_EXPORT = "data_export"
    REPORT_GENERATION = "report_generation"
    NOTIFICATION_SENT = "notification_sent"
    SETTINGS_CHANGE = "settings_change"
    ML_MODEL_TRAINING = "ml_model_training"
    DASHBOARD_VIEW = "dashboard_view"
    EMPLOYEE_SEARCH = "employee_search"
    ALERT_TRIGGERED = "alert_triggered"
    SYSTEM_ERROR = "system_error"

class AuditSeverity(Enum):
    """Niveaux de sévérité des événements"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AuditEvent:
    """Structure d'un événement d'audit"""
    event_id: str
    timestamp: str
    event_type: AuditEventType
    severity: AuditSeverity
    user_id: Optional[str]
    user_email: Optional[str]
    session_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    resource_accessed: Optional[str]
    action_performed: str
    details: Dict[str, Any]
    outcome: str  # SUCCESS, FAILURE, ERROR
    duration_ms: Optional[int]
    data_sensitivity: str  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    compliance_tags: List[str]

class GamingAuditLogger:
    """Logger d'audit enterprise pour Gaming Workforce Observatory"""
    
    def __init__(self, db_path: str = "audit_logs.db"):
        self.db_path = db_path
        self.session_lock = threading.Lock()
        
        # Configuration compliance
        self.compliance_frameworks = {
            'GDPR': ['personal_data', 'employee_data', 'performance_data'],
            'SOX': ['financial_data', 'compensation_data', 'reporting'],
            'ISO27001': ['security_events', 'access_control', 'data_classification'],
            'HIPAA': ['health_data', 'wellness_data'],  # Si données santé employés
            'PCI': ['payment_data', 'compensation_processing']
        }
        
        # Classification des données sensibles
        self.data_sensitivity_rules = {
            'employee_personal': 'CONFIDENTIAL',
            'salary_data': 'RESTRICTED',
            'performance_reviews': 'CONFIDENTIAL',
            'aggregated_metrics': 'INTERNAL',
            'public_reports': 'PUBLIC',
            'ml_models': 'INTERNAL',
            'system_logs': 'INTERNAL'
        }
        
        # Initialisation de la base de données
        self._init_database()
        
        # Configuration logging Python standard
        self._setup_logging()
    
    def _init_database(self):
        """Initialise la base de données d'audit"""
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_events (
                    event_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    user_id TEXT,
                    user_email TEXT,
                    session_id TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    resource_accessed TEXT,
                    action_performed TEXT NOT NULL,
                    details TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    duration_ms INTEGER,
                    data_sensitivity TEXT NOT NULL,
                    compliance_tags TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON audit_events(timestamp);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_event_type ON audit_events(event_type);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_id ON audit_events(user_id);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_severity ON audit_events(severity);
            """)
    
    def _setup_logging(self):
        """Configure le logging Python standard"""
        
        # Logger pour fichiers
        self.file_logger = logging.getLogger('gaming_audit')
        self.file_logger.setLevel(logging.INFO)
        
        # Handler pour fichier avec rotation
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler(
            'logs/gaming_audit.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10
        )
        
        # Format détaillé pour audit
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | AUDIT | %(message)s | '
            'Thread:%(thread)d | Process:%(process)d'
        )
        file_handler.setFormatter(formatter)
        
        self.file_logger.addHandler(file_handler)
    
    def log_event(self, event_type: AuditEventType, action: str,
                  details: Dict[str, Any] = None, severity: AuditSeverity = AuditSeverity.MEDIUM,
                  user_context: Dict[str, Any] = None, outcome: str = "SUCCESS",
                  duration_ms: int = None, resource: str = None) -> str:
        """Log un événement d'audit"""
        
        # Génération ID unique
        event_id = self._generate_event_id()
        
        # Contexte utilisateur depuis Streamlit si disponible
        if user_context is None:
            user_context = self._get_streamlit_user_context()
        
        # Classification de sensibilité
        data_sensitivity = self._classify_data_sensitivity(resource, details)
        
        # Tags de compliance
        compliance_tags = self._determine_compliance_tags(event_type, resource, details)
        
        # Création de l'événement
        audit_event = AuditEvent(
            event_id=event_id,
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            severity=severity,
            user_id=user_context.get('user_id'),
            user_email=user_context.get('user_email'),
            session_id=user_context.get('session_id'),
            ip_address=user_context.get('ip_address'),
            user_agent=user_context.get('user_agent'),
            resource_accessed=resource,
            action_performed=action,
            details=details or {},
            outcome=outcome,
            duration_ms=duration_ms,
            data_sensitivity=data_sensitivity,
            compliance_tags=compliance_tags
        )
        
        # Enregistrement dans la DB
        self._store_event(audit_event)
        
        # Log dans fichier
        self._log_to_file(audit_event)
        
        # Alertes pour événements critiques
        if severity == AuditSeverity.CRITICAL:
            self._trigger_security_alert(audit_event)
        
        return event_id
    
    def _generate_event_id(self) -> str:
        """Génère un ID unique pour l'événement"""
        
        timestamp = datetime.now().isoformat()
        random_data = f"{timestamp}{threading.current_thread().ident}"
        
        return hashlib.sha256(random_data.encode()).hexdigest()[:16]
    
    def _get_streamlit_user_context(self) -> Dict[str, Any]:
        """Récupère le contexte utilisateur depuis Streamlit"""
        
        context = {}
        
        try:
            # Session Streamlit
            if hasattr(st, 'session_state'):
                context['session_id'] = getattr(st.session_state, 'session_id', None)
                context['user_id'] = getattr(st.session_state, 'user_id', None)
                context['user_email'] = getattr(st.session_state, 'user_email', None)
            
            # Informations réseau (limitées dans Streamlit)
            context['ip_address'] = 'streamlit_client'
            context['user_agent'] = 'streamlit_app'
            
        except Exception as e:
            self.file_logger.warning(f"Could not retrieve user context: {e}")
        
        return context
    
    def _classify_data_sensitivity(self, resource: str, details: Dict[str, Any]) -> str:
        """Classifie la sensibilité des données accédées"""
        
        if not resource and not details:
            return 'PUBLIC'
        
        # Vérification par ressource
        for pattern, sensitivity in self.data_sensitivity_rules.items():
            if resource and pattern in resource.lower():
                return sensitivity
        
        # Vérification par contenu des détails
        if details:
            detail_text = json.dumps(details).lower()
            
            if any(term in detail_text for term in ['salary', 'compensation', 'pay']):
                return 'RESTRICTED'
            elif any(term in detail_text for term in ['performance', 'review', 'personal']):
                return 'CONFIDENTIAL'
            elif any(term in detail_text for term in ['employee', 'staff', 'team']):
                return 'INTERNAL'
        
        return 'INTERNAL'
    
    def _determine_compliance_tags(self, event_type: AuditEventType, 
                                 resource: str, details: Dict[str, Any]) -> List[str]:
        """Détermine les tags de compliance applicables"""
        
        tags = []
        
        # Analyse du contenu
        content_text = f"{resource or ''} {json.dumps(details or {})}"
        content_lower = content_text.lower()
        
        # Vérification GDPR
        if any(term in content_lower for term in ['employee', 'personal', 'email', 'name']):
            tags.append('GDPR')
        
        # Vérification SOX
        if any(term in content_lower for term in ['salary', 'compensation', 'financial', 'report']):
            tags.append('SOX')
        
        # Vérification ISO27001
        if event_type in [AuditEventType.LOGIN, AuditEventType.DATA_ACCESS, AuditEventType.SYSTEM_ERROR]:
            tags.append('ISO27001')
        
        # Vérification PCI (si applicable)
        if any(term in content_lower for term in ['payment', 'card', 'billing']):
            tags.append('PCI')
        
        return tags
    
    def _store_event(self, event: AuditEvent):
        """Stocke l'événement dans la base de données"""
        
        with self.session_lock:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT INTO audit_events (
                            event_id, timestamp, event_type, severity, user_id, user_email,
                            session_id, ip_address, user_agent, resource_accessed,
                            action_performed, details, outcome, duration_ms,
                            data_sensitivity, compliance_tags
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        event.event_id,
                        event.timestamp,
                        event.event_type.value,
                        event.severity.value,
                        event.user_id,
                        event.user_email,
                        event.session_id,
                        event.ip_address,
                        event.user_agent,
                        event.resource_accessed,
                        event.action_performed,
                        json.dumps(event.details),
                        event.outcome,
                        event.duration_ms,
                        event.data_sensitivity,
                        json.dumps(event.compliance_tags)
                    ))
                    
            except Exception as e:
                self.file_logger.error(f"Failed to store audit event: {e}")
    
    def _log_to_file(self, event: AuditEvent):
        """Log l'événement dans le fichier"""
        
        log_message = (
            f"EventID:{event.event_id} | Type:{event.event_type.value} | "
            f"User:{event.user_email or event.user_id or 'Anonymous'} | "
            f"Action:{event.action_performed} | Resource:{event.resource_accessed or 'N/A'} | "
            f"Outcome:{event.outcome} | Sensitivity:{event.data_sensitivity} | "
            f"Compliance:{','.join(event.compliance_tags)}"
        )
        
        if event.severity == AuditSeverity.CRITICAL:
            self.file_logger.critical(log_message)
        elif event.severity == AuditSeverity.HIGH:
            self.file_logger.warning(log_message)
        else:
            self.file_logger.info(log_message)
    
    def _trigger_security_alert(self, event: AuditEvent):
        """Déclenche une alerte de sécurité pour événements critiques"""
        
        # Intégration avec le notification manager si disponible
        try:
            from .notification_manager import GamingNotificationManager
            
            notifier = GamingNotificationManager()
            
            alert_data = {
                'event_id': event.event_id,
                'event_type': event.event_type.value,
                'user': event.user_email or event.user_id or 'Unknown',
                'action': event.action_performed,
                'timestamp': event.timestamp
            }
            
            notifier.send_notification(
                'security_alert',
                ['security@company.com', 'admin@company.com'],
                alert_data
            )
            
        except Exception as e:
            self.file_logger.error(f"Failed to send security alert: {e}")
    
    @contextmanager
    def audit_operation(self, event_type: AuditEventType, action: str,
                       resource: str = None, severity: AuditSeverity = AuditSeverity.MEDIUM):
        """Context manager pour audit automatique d'opérations"""
        
        start_time = datetime.now()
        event_details = {}
        outcome = "SUCCESS"
        
        try:
            yield event_details
            
        except Exception as e:
            outcome = "ERROR"
            event_details['error'] = str(e)
            event_details['error_type'] = type(e).__name__
            severity = AuditSeverity.HIGH
            raise
            
        finally:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            self.log_event(
                event_type=event_type,
                action=action,
                details=event_details,
                severity=severity,
                outcome=outcome,
                duration_ms=duration_ms,
                resource=resource
            )
    
    def get_audit_trail(self, start_date: datetime = None, end_date: datetime = None,
                       event_types: List[AuditEventType] = None,
                       user_id: str = None, severity: AuditSeverity = None,
                       limit: int = 1000) -> pd.DataFrame:
        """Récupère l'historique d'audit avec filtres"""
        
        query = "SELECT * FROM audit_events WHERE 1=1"
        params = []
        
        # Filtres
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())
        
        if event_types:
            query += f" AND event_type IN ({','.join(['?' for _ in event_types])})"
            params.extend([et.value for et in event_types])
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if severity:
            query += " AND severity = ?"
            params.append(severity.value)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
        
        # Parsing des colonnes JSON
        if not df.empty:
            df['details'] = df['details'].apply(lambda x: json.loads(x) if x else {})
            df['compliance_tags'] = df['compliance_tags'].apply(lambda x: json.loads(x) if x else [])
        
        return df
    
    def generate_compliance_report(self, framework: str, 
                                 start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Génère un rapport de compliance pour un framework spécifique"""
        
        if framework not in self.compliance_frameworks:
            raise ValueError(f"Framework {framework} not supported")
        
        # Récupération des événements pertinents
        audit_trail = self.get_audit_trail(start_date=start_date, end_date=end_date)
        
        # Filtrage par framework
        framework_events = audit_trail[
            audit_trail['compliance_tags'].apply(
                lambda tags: framework in tags if isinstance(tags, list) else False
            )
        ]
        
        # Analyse par type d'événement
        event_summary = framework_events.groupby('event_type').agg({
            'event_id': 'count',
            'severity': lambda x: x.value_counts().to_dict()
        }).to_dict()
        
        # Analyse par utilisateur
        user_activity = framework_events.groupby('user_email').agg({
            'event_id': 'count',
            'resource_accessed': 'nunique'
        }).to_dict() if 'user_email' in framework_events.columns else {}
        
        # Événements critiques
        critical_events = framework_events[
            framework_events['severity'] == 'critical'
        ].to_dict('records')
        
        return {
            'framework': framework,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'total_events': len(framework_events),
            'event_summary': event_summary,
            'user_activity': user_activity,
            'critical_events': critical_events,
            'compliance_status': 'COMPLIANT' if len(critical_events) == 0 else 'REVIEW_REQUIRED'
        }
    
    def render_audit_dashboard(self):
        """Interface Streamlit pour la gestion d'audit"""
        
        st.markdown("## 🔍 Audit & Compliance Dashboard")
        st.markdown("*Monitor and analyze system access and compliance with gaming workforce data*")
        
        # Onglets
        tab1, tab2, tab3, tab4 = st.tabs(["Audit Trail", "Compliance Reports", "Analytics", "Settings"])
        
        with tab1:
            st.markdown("### 📋 Recent Audit Events")
            
            # Filtres
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                date_range = st.date_input(
                    "Date Range",
                    value=[datetime.now().date() - pd.Timedelta(days=7), datetime.now().date()],
                    key="audit_date_range"
                )
            
            with col2:
                event_types = st.multiselect(
                    "Event Types",
                    [et.value for et in AuditEventType],
                    default=['data_access', 'report_generation']
                )
            
            with col3:
                severity_filter = st.selectbox(
                    "Severity",
                    ['All'] + [s.value for s in AuditSeverity]
                )
            
            with col4:
                limit = st.number_input("Max Records", min_value=10, max_value=10000, value=100)
            
            # Récupération des données
            if len(date_range) == 2:
                start_date = datetime.combine(date_range[0], datetime.min.time())
                end_date = datetime.combine(date_range[1], datetime.max.time())
                
                event_types_enum = [AuditEventType(et) for et in event_types]
                severity_enum = AuditSeverity(severity_filter) if severity_filter != 'All' else None
                
                audit_df = self.get_audit_trail(
                    start_date=start_date,
                    end_date=end_date,
                    event_types=event_types_enum,
                    severity=severity_enum,
                    limit=limit
                )
                
                if not audit_df.empty:
                    # Métriques rapides
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Events", len(audit_df))
                    with col2:
                        unique_users = audit_df['user_email'].nunique()
                        st.metric("Unique Users", unique_users)
                    with col3:
                        critical_count = (audit_df['severity'] == 'critical').sum()
                        st.metric("Critical Events", critical_count, delta_color="inverse")
                    with col4:
                        success_rate = (audit_df['outcome'] == 'SUCCESS').mean() * 100
                        st.metric("Success Rate", f"{success_rate:.1f}%")
                    
                    # Tableau des événements
                    display_df = audit_df[[
                        'timestamp', 'event_type', 'user_email', 'action_performed',
                        'resource_accessed', 'outcome', 'severity', 'data_sensitivity'
                    ]].copy()
                    
                    display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    st.dataframe(display_df, use_container_width=True, height=400)
                    
                    # Export
                    if st.button("📥 Export Audit Trail"):
                        csv = audit_df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
                else:
                    st.info("No audit events found for the selected criteria.")
        
        with tab2:
            st.markdown("### 📊 Compliance Reports")
            
            col1, col2 = st.columns(2)
            
            with col1:
                framework = st.selectbox(
                    "Compliance Framework",
                    list(self.compliance_frameworks.keys())
                )
                
                report_period = st.selectbox(
                    "Report Period",
                    ["Last 7 days", "Last 30 days", "Last 90 days", "Custom"]
                )
                
                if report_period == "Custom":
                    custom_range = st.date_input(
                        "Custom Date Range",
                        value=[datetime.now().date() - pd.Timedelta(days=30), datetime.now().date()]
                    )
                
                if st.button("📋 Generate Compliance Report"):
                    # Calcul des dates
                    if report_period == "Last 7 days":
                        start_date = datetime.now() - pd.Timedelta(days=7)
                        end_date = datetime.now()
                    elif report_period == "Last 30 days":
                        start_date = datetime.now() - pd.Timedelta(days=30)
                        end_date = datetime.now()
                    elif report_period == "Last 90 days":
                        start_date = datetime.now() - pd.Timedelta(days=90)
                        end_date = datetime.now()
                    else:  # Custom
                        start_date = datetime.combine(custom_range[0], datetime.min.time())
                        end_date = datetime.combine(custom_range[1], datetime.max.time())
                    
                    with st.spinner("Generating compliance report..."):
                        compliance_report = self.generate_compliance_report(
                            framework, start_date, end_date
                        )
                    
                    # Affichage du rapport
                    st.success(f"✅ {framework} Compliance Report Generated")
                    
                    with col2:
                        st.markdown("#### Report Summary")
                        st.metric("Total Events", compliance_report['total_events'])
                        st.metric("Compliance Status", compliance_report['compliance_status'])
                        st.metric("Critical Events", len(compliance_report['critical_events']))
                        
                        if compliance_report['critical_events']:
                            st.warning("⚠️ Critical events require review")
                            for event in compliance_report['critical_events'][:3]:
                                st.text(f"• {event['action_performed']} - {event['timestamp']}")
            
            with col2 if 'compliance_report' not in locals() else st.container():
                if 'compliance_report' in locals():
                    st.markdown("#### Event Types Distribution")
                    
                    event_counts = {}
                    for event_type, data in compliance_report['event_summary'].items():
                        if isinstance(data, dict) and 'event_id' in data:
                            event_counts[event_type] = data['event_id']
                    
                    if event_counts:
                        events_df = pd.DataFrame(list(event_counts.items()), 
                                               columns=['Event Type', 'Count'])
                        st.bar_chart(events_df.set_index('Event Type'))
        
        with tab3:
            st.markdown("### 📈 Audit Analytics")
            
            # Analyse des tendances sur 30 jours
            end_date = datetime.now()
            start_date = end_date - pd.Timedelta(days=30)
            
            analytics_df = self.get_audit_trail(start_date=start_date, end_date=end_date, limit=5000)
            
            if not analytics_df.empty:
                # Tendances quotidiennes
                analytics_df['date'] = pd.to_datetime(analytics_df['timestamp']).dt.date
                daily_events = analytics_df.groupby('date').size().reset_index(name='events')
                
                st.markdown("#### Daily Event Trends (Last 30 Days)")
                st.line_chart(daily_events.set_index('date'))
                
                # Top utilisateurs
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Top Users by Activity")
                    user_activity = analytics_df['user_email'].value_counts().head(10)
                    st.bar_chart(user_activity)
                
                with col2:
                    st.markdown("#### Event Types Distribution")
                    event_types = analytics_df['event_type'].value_counts()
                    st.bar_chart(event_types)
            
            else:
                st.info("Insufficient data for analytics. Please adjust the date range.")
        
        with tab4:
            st.markdown("### ⚙️ Audit Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Data Retention")
                retention_days = st.number_input(
                    "Audit Log Retention (days)",
                    min_value=30, max_value=2555, value=365
                )
                
                st.markdown("#### Compliance Frameworks")
                enabled_frameworks = st.multiselect(
                    "Enabled Frameworks",
                    list(self.compliance_frameworks.keys()),
                    default=['GDPR', 'ISO27001']
                )
                
                st.markdown("#### Alert Thresholds")
                failed_login_threshold = st.number_input(
                    "Failed Login Alert Threshold",
                    min_value=1, max_value=100, value=5
                )
            
            with col2:
                st.markdown("#### Database Statistics")
                
                # Statistiques de la DB
                with sqlite3.connect(self.db_path) as conn:
                    stats = conn.execute("SELECT COUNT(*) as total FROM audit_events").fetchone()
                    
                    oldest = conn.execute(
                        "SELECT MIN(timestamp) as oldest FROM audit_events"
                    ).fetchone()
                    
                    size_mb = Path(self.db_path).stat().st_size / (1024 * 1024)
                
                st.metric("Total Events", stats[0] if stats else 0)
                st.metric("Database Size", f"{size_mb:.2f} MB")
                st.metric("Oldest Record", oldest[0] if oldest and oldest[0] else "N/A")
                
                # Actions de maintenance
                st.markdown("#### Maintenance Actions")
                
                if st.button("🧹 Clean Old Records"):
                    cutoff_date = datetime.now() - pd.Timedelta(days=retention_days)
                    
                    with sqlite3.connect(self.db_path) as conn:
                        deleted = conn.execute(
                            "DELETE FROM audit_events WHERE timestamp < ?",
                            (cutoff_date.isoformat(),)
                        ).rowcount
                    
                    st.success(f"Deleted {deleted} old records")
                
                if st.button("💾 Backup Database"):
                    backup_path = f"audit_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                    import shutil
                    shutil.copy2(self.db_path, backup_path)
                    st.success(f"Database backed up to {backup_path}")
