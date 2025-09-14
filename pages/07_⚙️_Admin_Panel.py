"""
Gaming Workforce Observatory - Admin Panel
Panel d'administration système pour gestion enterprise
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path
import hashlib
import json
import sqlite3
import logging

# Ajout du chemin pour imports
sys.path.append(str(Path(__file__).parent.parent))

from src.themes.gaming_themes import GamingThemes
from src.utils.audit_logger import GamingAuditLogger
from src.utils.notification_manager import GamingNotificationManager
from src.utils.export_manager import GamingExportManager

def initialize_admin_panel():
    """Initialise le panel d'administration"""
    st.set_page_config(
        page_title="⚙️ Gaming Workforce Observatory - Admin Panel",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Application du thème gaming
    themes = GamingThemes()
    themes.apply_gaming_theme()

def hash_password(password: str) -> str:
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_admin():
    """Authentification administrateur"""
    
    # Base d'utilisateurs admin (en production: base de données sécurisée)
    ADMIN_USERS = {
        "admin": {
            "password_hash": hash_password("gaming_admin_2025"),
            "role": "super_admin",
            "email": "admin@gaming-workforce.com",
            "permissions": ["read", "write", "delete", "manage_users", "view_audit"]
        },
        "hr_admin": {
            "password_hash": hash_password("hr_secure_2025"),
            "role": "hr_admin", 
            "email": "hr@gaming-workforce.com",
            "permissions": ["read", "write", "view_audit"]
        },
        "analyst": {
            "password_hash": hash_password("analyst_2025"),
            "role": "analyst",
            "email": "analyst@gaming-workforce.com", 
            "permissions": ["read", "view_audit"]
        }
    }
    
    # Vérification de session
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
        st.session_state.admin_user = None
        st.session_state.admin_role = None
        st.session_state.admin_permissions = []
    
    if not st.session_state.admin_authenticated:
        
        # Interface de login
        st.markdown("""
        <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;'>
            <h1 style='color: white; font-family: "Orbitron", monospace; font-size: 3rem; margin: 0;'>⚙️ ADMIN ACCESS</h1>
            <h2 style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'>Gaming Workforce Observatory</h2>
            <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 0;'>Enterprise Administration Panel</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            with st.form("admin_login"):
                st.markdown("### 🔐 Administrator Login")
                
                username = st.text_input("Username", placeholder="Enter admin username")
                password = st.text_input("Password", type="password", placeholder="Enter admin password")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    login_btn = st.form_submit_button("🔑 Login", use_container_width=True)
                with col_b:
                    demo_btn = st.form_submit_button("👤 Demo Access", use_container_width=True)
                
                if login_btn:
                    user = ADMIN_USERS.get(username)
                    if user and user["password_hash"] == hash_password(password):
                        st.session_state.admin_authenticated = True
                        st.session_state.admin_user = username
                        st.session_state.admin_role = user["role"]
                        st.session_state.admin_permissions = user["permissions"]
                        
                        # Log de connexion admin
                        audit_logger = GamingAuditLogger()
                        audit_logger.log_event(
                            event_type=audit_logger.AuditEventType.LOGIN,
                            action="Admin panel login",
                            user_context={"user_id": username, "user_email": user["email"]},
                            severity=audit_logger.AuditSeverity.MEDIUM
                        )
                        
                        st.success(f"✅ Welcome {username}! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                
                if demo_btn:
                    # Accès démo avec permissions limitées
                    st.session_state.admin_authenticated = True
                    st.session_state.admin_user = "demo_admin"
                    st.session_state.admin_role = "demo"
                    st.session_state.admin_permissions = ["read"]
                    st.success("✅ Demo access granted! Redirecting...")
                    st.rerun()
            
            # Aide de connexion
            with st.expander("🆘 Need Help?"):
                st.markdown("""
                **Demo Credentials:**
                - Username: `admin` / Password: `gaming_admin_2025`
                - Username: `hr_admin` / Password: `hr_secure_2025`
                - Username: `analyst` / Password: `analyst_2025`
                
                **Or use Demo Access** for read-only access.
                
                **Contact:** admin@gaming-workforce.com
                """)
        
        return False
    
    return True

def render_admin_header():
    """Header admin avec infos utilisateur"""
    
    themes = GamingThemes()
    
    # Status indicator
    status_html = themes.create_status_indicator('online', pulse=False)
    
    header_info = f"""
    <div style='background: linear-gradient(135deg, #2c3e50, #3498db); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; color: white;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h3 style='margin: 0; color: white;'>⚙️ Admin Panel - {st.session_state.admin_role.title()}</h3>
                <p style='margin: 0; opacity: 0.8;'>User: {st.session_state.admin_user} | Last Login: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            <div>
                {status_html}
            </div>
        </div>
    </div>
    """
    
    st.markdown(header_info, unsafe_allow_html=True)

def render_user_management():
    """Gestion des utilisateurs"""
    
    st.markdown("### 👥 User Management")
    
    # Simulation d'utilisateurs système
    users_data = pd.DataFrame({
        'user_id': range(1, 26),
        'username': [f'user_{i}' for i in range(1, 26)],
        'email': [f'user{i}@company.com' for i in range(1, 26)],
        'role': np.random.choice(['employee', 'manager', 'admin', 'analyst'], 25, p=[0.6, 0.2, 0.1, 0.1]),
        'status': np.random.choice(['active', 'inactive', 'suspended'], 25, p=[0.8, 0.15, 0.05]),
        'last_login': pd.date_range(end=datetime.now(), periods=25, freq='-1D'),
        'department': np.random.choice(['Programming', 'Art & Animation', 'Game Design', 'QA', 'Production'], 25),
        'created_at': pd.date_range(end=datetime.now(), periods=25, freq='-30D')
    })
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Filtres
        st.markdown("#### 🔍 User Filters")
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            role_filter = st.multiselect("Filter by Role", users_data['role'].unique(), default=users_data['role'].unique())
        with filter_col2:
            status_filter = st.multiselect("Filter by Status", users_data['status'].unique(), default=users_data['status'].unique())  
        with filter_col3:
            dept_filter = st.multiselect("Filter by Department", users_data['department'].unique(), default=users_data['department'].unique())
        
        # Application des filtres
        filtered_users = users_data[
            (users_data['role'].isin(role_filter)) &
            (users_data['status'].isin(status_filter)) &
            (users_data['department'].isin(dept_filter))
        ]
        
        # Affichage des utilisateurs
        st.markdown("#### 📋 Users List")
        
        # Configuration des colonnes
        display_df = filtered_users[['username', 'email', 'role', 'status', 'department', 'last_login']].copy()
        display_df['last_login'] = display_df['last_login'].dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(display_df, use_container_width=True, height=400)
    
    with col2:
        # Actions utilisateur
        st.markdown("#### ⚡ User Actions")
        
        if "manage_users" in st.session_state.admin_permissions:
            
            # Nouveau utilisateur
            with st.expander("➕ Add New User"):
                new_username = st.text_input("Username")
                new_email = st.text_input("Email")
                new_role = st.selectbox("Role", ['employee', 'manager', 'admin', 'analyst'])
                new_department = st.selectbox("Department", users_data['department'].unique())
                
                if st.button("Create User"):
                    st.success(f"User '{new_username}' created successfully!")
            
            # Actions en lot
            with st.expander("📦 Bulk Actions"):
                bulk_action = st.selectbox("Select Action", ["Activate", "Deactivate", "Reset Password", "Delete"])
                
                if st.button(f"Execute {bulk_action}"):
                    st.info(f"Bulk {bulk_action.lower()} executed on selected users")
            
        else:
            st.warning("⚠️ Insufficient permissions for user management")
        
        # Statistiques utilisateurs
        st.markdown("#### 📊 User Statistics")
        st.metric("Total Users", len(users_data))
        st.metric("Active Users", len(users_data[users_data['status'] == 'active']))
        st.metric("Admins", len(users_data[users_data['role'] == 'admin']))

def render_system_monitoring():
    """Monitoring système"""
    
    st.markdown("### 📊 System Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Métriques système
        st.markdown("#### ⚡ System Performance")
        
        # Simulation métriques système
        cpu_usage = np.random.uniform(45, 85)
        memory_usage = np.random.uniform(55, 75)
        disk_usage = np.random.uniform(35, 60)
        network_io = np.random.uniform(20, 40)
        
        themes = GamingThemes()
        
        # Métriques avec couleurs conditionnelles
        cpu_color = "danger" if cpu_usage > 80 else "warning" if cpu_usage > 60 else "success"
        memory_color = "danger" if memory_usage > 80 else "warning" if memory_usage > 60 else "success"
        
        cpu_html = themes.create_metric_card("CPU Usage", f"{cpu_usage:.1f}%", "", cpu_color, "💻")
        st.markdown(cpu_html, unsafe_allow_html=True)
        
        memory_html = themes.create_metric_card("Memory Usage", f"{memory_usage:.1f}%", "", memory_color, "🧠")
        st.markdown(memory_html, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Disk Usage", f"{disk_usage:.1f}%")
        with col_b:
            st.metric("Network I/O", f"{network_io:.1f} MB/s")
    
    with col2:
        # Activité système
        st.markdown("#### 📈 System Activity (Last 24h)")
        
        # Génération données activité
        hours = pd.date_range(start=datetime.now() - timedelta(hours=24), end=datetime.now(), freq='H')
        activity_data = pd.DataFrame({
            'hour': hours,
            'requests': np.random.poisson(50, len(hours)),
            'users_active': np.random.poisson(25, len(hours)),
            'errors': np.random.poisson(2, len(hours))
        })
        
        fig_activity = px.line(
            activity_data,
            x='hour',
            y=['requests', 'users_active'],
            title='System Activity Trends',
            labels={'value': 'Count', 'hour': 'Time'}
        )
        
        st.plotly_chart(fig_activity, use_container_width=True)
    
    # Alertes système
    st.markdown("#### 🚨 System Alerts")
    
    alerts = [
        {"level": "warning", "message": "High CPU usage on server-02 (78%)", "time": "5 minutes ago"},
        {"level": "info", "message": "Database backup completed successfully", "time": "1 hour ago"},
        {"level": "critical", "message": "Failed login attempts from IP 192.168.1.100", "time": "2 hours ago"},
    ]
    
    for alert in alerts:
        alert_color = {"critical": "#e74c3c", "warning": "#f39c12", "info": "#3498db"}[alert["level"]]
        alert_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}[alert["level"]]
        
        st.markdown(f"""
        <div style='border-left: 4px solid {alert_color}; padding: 0.5rem; margin: 0.5rem 0; background: rgba(0,0,0,0.1);'>
            {alert_icon} <strong>{alert["message"]}</strong> <small>({alert["time"]})</small>
        </div>
        """, unsafe_allow_html=True)

def render_audit_logs():
    """Gestion des logs d'audit"""
    
    st.markdown("### 🔍 Audit Logs & Security")
    
    audit_logger = GamingAuditLogger()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Récupération des logs d'audit
        try:
            logs_df = audit_logger.get_audit_trail(limit=50)
            
            if not logs_df.empty:
                # Filtres pour les logs
                st.markdown("#### 🎛️ Log Filters")
                filter_col1, filter_col2 = st.columns(2)
                
                with filter_col1:
                    event_types = st.multiselect(
                        "Event Types",
                        logs_df['event_type'].unique() if 'event_type' in logs_df.columns else [],
                        default=logs_df['event_type'].unique()[:3] if 'event_type' in logs_df.columns else []
                    )
                
                with filter_col2:
                    severity_levels = st.multiselect(
                        "Severity Levels", 
                        logs_df['severity'].unique() if 'severity' in logs_df.columns else [],
                        default=logs_df['severity'].unique() if 'severity' in logs_df.columns else []
                    )
                
                # Application des filtres
                if event_types and severity_levels:
                    filtered_logs = logs_df[
                        (logs_df['event_type'].isin(event_types)) &
                        (logs_df['severity'].isin(severity_levels))
                    ]
                else:
                    filtered_logs = logs_df
                
                # Affichage des logs
                st.markdown("#### 📋 Recent Audit Events")
                
                display_cols = ['timestamp', 'event_type', 'user_email', 'action_performed', 'severity']
                available_cols = [col for col in display_cols if col in filtered_logs.columns]
                
                if available_cols:
                    st.dataframe(filtered_logs[available_cols].head(20), use_container_width=True)
                else:
                    st.warning("No audit data columns available for display")
            
            else:
                st.info("No audit logs available. Start using the application to generate audit events.")
        
        except Exception as e:
            st.error(f"Error loading audit logs: {str(e)}")
            
            # Logs simulés pour la démo
            st.markdown("#### 📋 Simulated Audit Events (Demo)")
            
            demo_logs = pd.DataFrame({
                'timestamp': pd.date_range(end=datetime.now(), periods=10, freq='-1H'),
                'event_type': np.random.choice(['login', 'data_access', 'report_generation'], 10),
                'user_email': np.random.choice(['admin@company.com', 'user@company.com'], 10),
                'action': np.random.choice(['Login successful', 'Dashboard accessed', 'Report exported'], 10),
                'severity': np.random.choice(['low', 'medium', 'high'], 10, p=[0.6, 0.3, 0.1])
            })
            
            st.dataframe(demo_logs, use_container_width=True)
    
    with col2:
        # Statistiques d'audit
        st.markdown("#### 📊 Audit Statistics")
        
        # Métriques d'audit
        st.metric("Events Today", 47)
        st.metric("Critical Events", 3, delta_color="inverse")
        st.metric("Active Users", 12)
        
        # Actions d'audit
        if "view_audit" in st.session_state.admin_permissions:
            
            st.markdown("#### ⚙️ Audit Actions")
            
            if st.button("📥 Export Audit Log"):
                st.success("Audit log export initiated")
            
            if st.button("🧹 Clean Old Logs"):
                st.info("Old logs cleanup scheduled")
            
            if st.button("🔄 Refresh Logs"):
                st.rerun()
        
        else:
            st.warning("⚠️ Insufficient permissions")

def render_configuration():
    """Configuration système"""
    
    st.markdown("### ⚙️ System Configuration")
    
    if "write" not in st.session_state.admin_permissions:
        st.warning("⚠️ Read-only access - Configuration changes not permitted")
        return
    
    # Onglets de configuration
    config_tabs = st.tabs(["General", "Security", "Notifications", "Database", "Integrations"])
    
    with config_tabs[0]:
        st.markdown("#### 🌐 General Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            app_name = st.text_input("Application Name", value="Gaming Workforce Observatory")
            app_version = st.text_input("Version", value="1.0.0", disabled=True)
            timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "CET"], index=3)
            
        with col2:
            max_users = st.number_input("Max Concurrent Users", value=100, min_value=1)
            session_timeout = st.number_input("Session Timeout (minutes)", value=60, min_value=5)
            debug_mode = st.checkbox("Debug Mode", value=False)
        
        if st.button("💾 Save General Settings"):
            st.success("General settings saved successfully!")
    
    with config_tabs[1]:
        st.markdown("#### 🔒 Security Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            password_policy = st.selectbox("Password Policy", ["Standard", "Strong", "Enterprise"])
            mfa_required = st.checkbox("Require MFA", value=True)
            ip_whitelist = st.text_area("IP Whitelist", "192.168.1.0/24\n10.0.0.0/8")
        
        with col2:
            max_login_attempts = st.number_input("Max Login Attempts", value=3, min_value=1)
            lockout_duration = st.number_input("Lockout Duration (minutes)", value=15)
            audit_retention = st.number_input("Audit Log Retention (days)", value=90)
        
        if st.button("🔐 Save Security Settings"):
            st.success("Security settings updated!")
    
    with config_tabs[2]:
        st.markdown("#### 📧 Notification Settings")
        
        notification_manager = GamingNotificationManager()
        
        # Email settings
        st.markdown("##### 📨 Email Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            smtp_server = st.text_input("SMTP Server", value="smtp.company.com")
            smtp_port = st.number_input("SMTP Port", value=587)
            
        with col2:
            email_username = st.text_input("Email Username")
            use_tls = st.checkbox("Use TLS", value=True)
        
        # Slack settings
        st.markdown("##### 💬 Slack Configuration")
        slack_webhook = st.text_input("Slack Webhook URL", type="password")
        slack_channel = st.text_input("Default Channel", value="#workforce-alerts")
        
        if st.button("📬 Save Notification Settings"):
            st.success("Notification settings configured!")
    
    with config_tabs[3]:
        st.markdown("#### 🗄️ Database Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            db_host = st.text_input("Database Host", value="localhost")
            db_port = st.number_input("Database Port", value=5432)
            db_name = st.text_input("Database Name", value="gaming_workforce")
        
        with col2:
            backup_enabled = st.checkbox("Auto Backup", value=True)
            backup_frequency = st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
            
            if st.button("🔄 Test Connection"):
                st.success("Database connection successful!")
        
        if st.button("💾 Save Database Settings"):
            st.success("Database settings updated!")
    
    with config_tabs[4]:
        st.markdown("#### 🔗 External Integrations")
        
        # API integrations
        st.markdown("##### 🌐 API Integrations")
        
        integrations = {
            "Slack": {"enabled": True, "status": "connected"},
            "Microsoft Teams": {"enabled": False, "status": "disconnected"},
            "JIRA": {"enabled": True, "status": "connected"},
            "GitHub": {"enabled": False, "status": "disconnected"}
        }
        
        for integration, config in integrations.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{integration}**")
            with col2:
                enabled = st.checkbox("Enabled", value=config["enabled"], key=f"{integration}_enabled")
            with col3:
                status_color = "🟢" if config["status"] == "connected" else "🔴"
                st.markdown(f"{status_color} {config['status'].title()}")

def main():
    """Fonction principale Admin Panel"""
    
    initialize_admin_panel()
    
    # Authentification admin
    if not authenticate_admin():
        return
    
    # Header admin
    render_admin_header()
    
    # Sidebar avec logout
    with st.sidebar:
        st.markdown(f"## ⚙️ Admin Console")
        
        admin_sections = [
            "👥 User Management",
            "📊 System Monitoring", 
            "🔍 Audit Logs",
            "⚙️ Configuration",
            "📈 Analytics",
            "🔧 Maintenance"
        ]
        
        selected_section = st.selectbox(
            "Select admin section:",
            admin_sections,
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📊 System Status")
        
        themes = GamingThemes()
        
        system_status = themes.create_status_indicator('online')
        database_status = themes.create_status_indicator('online')
        api_status = themes.create_status_indicator('warning')
        
        st.markdown(f"**System:** {system_status}", unsafe_allow_html=True)
        st.markdown(f"**Database:** {database_status}", unsafe_allow_html=True)
        st.markdown(f"**APIs:** {api_status}", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Quick Stats")
        
        st.metric("Active Sessions", "47")
        st.metric("System Uptime", "99.8%")
        st.metric("Last Backup", "2h ago")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            
            # Log de déconnexion
            audit_logger = GamingAuditLogger()
            audit_logger.log_event(
                event_type=audit_logger.AuditEventType.LOGOUT,
                action="Admin panel logout",
                user_context={"user_id": st.session_state.admin_user},
                severity=audit_logger.AuditSeverity.LOW
            )
            
            st.session_state.admin_authenticated = False
            st.session_state.admin_user = None
            st.session_state.admin_role = None
            st.session_state.admin_permissions = []
            st.success("Logged out successfully!")
            st.rerun()
    
    # Contenu principal selon la section
    if selected_section == "👥 User Management":
        render_user_management()
    elif selected_section == "📊 System Monitoring":
        render_system_monitoring()
    elif selected_section == "🔍 Audit Logs":
        render_audit_logs()
    elif selected_section == "⚙️ Configuration":
        render_configuration()
    elif selected_section == "📈 Analytics":
        st.markdown("### 📈 System Analytics")
        st.info("Advanced analytics dashboard coming soon...")
    elif selected_section == "🔧 Maintenance":
        st.markdown("### 🔧 System Maintenance")
        st.info("Maintenance tools coming soon...")
    
    # Footer admin
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #7f8c8d; font-size: 12px;'>"
        f"⚙️ Gaming Workforce Observatory Admin Panel | "
        f"User: {st.session_state.admin_user} ({st.session_state.admin_role}) | "
        f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        "Enterprise Administration Console"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
