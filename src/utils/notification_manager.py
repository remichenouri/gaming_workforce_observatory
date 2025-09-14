"""
Gaming Workforce Observatory - Notification Manager Enterprise
Système de notifications multi-canal (email, Slack, Teams, Discord)
"""
import smtplib
import json
import requests
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Any, Optional, Union
import streamlit as st
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from enum import Enum
import schedule
import time
import threading

logger = logging.getLogger(__name__)

class NotificationLevel(Enum):
    """Niveaux de priorité des notifications"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"

class NotificationChannel(Enum):
    """Canaux de notification supportés"""
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"
    DISCORD = "discord"
    WEBHOOK = "webhook"

@dataclass
class NotificationTemplate:
    """Template de notification gaming"""
    title: str
    message: str
    level: NotificationLevel
    channels: List[NotificationChannel]
    metadata: Dict[str, Any]

class GamingNotificationManager:
    """Gestionnaire de notifications enterprise pour gaming workforce"""
    
    def __init__(self):
        # Configuration des canaux
        self.email_config = {
            'smtp_server': st.secrets.get('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': st.secrets.get('SMTP_PORT', 587),
            'username': st.secrets.get('EMAIL_USERNAME'),
            'password': st.secrets.get('EMAIL_PASSWORD'),
            'from_address': st.secrets.get('FROM_EMAIL')
        }
        
        self.slack_config = {
            'webhook_url': st.secrets.get('SLACK_WEBHOOK_URL'),
            'bot_token': st.secrets.get('SLACK_BOT_TOKEN'),
            'channel': st.secrets.get('SLACK_CHANNEL', '#workforce-alerts')
        }
        
        self.teams_config = {
            'webhook_url': st.secrets.get('TEAMS_WEBHOOK_URL')
        }
        
        self.discord_config = {
            'webhook_url': st.secrets.get('DISCORD_WEBHOOK_URL')
        }
        
        # Templates de notifications gaming
        self.templates = {
            'employee_high_risk': NotificationTemplate(
                title="🚨 High Attrition Risk Alert",
                message="Employee {employee_name} in {department} shows high attrition risk ({risk_score}%)",
                level=NotificationLevel.CRITICAL,
                channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK],
                metadata={'icon': '⚠️', 'color': '#e74c3c'}
            ),
            'team_satisfaction_drop': NotificationTemplate(
                title="📉 Team Satisfaction Drop",
                message="{department} team satisfaction dropped to {satisfaction_score}/10",
                level=NotificationLevel.WARNING,
                channels=[NotificationChannel.SLACK, NotificationChannel.TEAMS],
                metadata={'icon': '😟', 'color': '#f39c12'}
            ),
            'project_milestone': NotificationTemplate(
                title="🎯 Project Milestone Achieved",
                message="Project {project_name} reached milestone: {milestone_name}",
                level=NotificationLevel.SUCCESS,
                channels=[NotificationChannel.SLACK, NotificationChannel.DISCORD],
                metadata={'icon': '🎉', 'color': '#27ae60'}
            ),
            'skills_gap_critical': NotificationTemplate(
                title="🎪 Critical Skills Gap Detected",
                message="Critical skills gap in {department}: {skill_name} (gap: {gap_severity})",
                level=NotificationLevel.CRITICAL,
                channels=[NotificationChannel.EMAIL, NotificationChannel.TEAMS],
                metadata={'icon': '🔧', 'color': '#e74c3c'}
            ),
            'performance_review_due': NotificationTemplate(
                title="📝 Performance Review Due",
                message="Performance review due for {employee_count} employees in {department}",
                level=NotificationLevel.INFO,
                channels=[NotificationChannel.EMAIL],
                metadata={'icon': '📋', 'color': '#3498db'}
            ),
            'hiring_milestone': NotificationTemplate(
                title="👥 Hiring Milestone Reached",
                message="Successfully hired {hire_count} new {department} team members this quarter",
                level=NotificationLevel.SUCCESS,
                channels=[NotificationChannel.SLACK, NotificationChannel.TEAMS],
                metadata={'icon': '🎯', 'color': '#2ecc71'}
            )
        }
        
        # Queue des notifications
        self.notification_queue = []
        self.notification_history = []
        
        # Configuration des seuils d'alerte
        self.alert_thresholds = {
            'attrition_risk_critical': 0.8,
            'satisfaction_warning': 6.0,
            'performance_critical': 2.5,
            'retention_warning': 75.0
        }
        
        # Démarrage du scheduler
        self._start_scheduler()
    
    def send_notification(self, template_name: str, recipients: List[str],
                         data: Dict[str, Any], channels: Optional[List[NotificationChannel]] = None) -> Dict[str, bool]:
        """Envoie une notification multi-canal"""
        
        if template_name not in self.templates:
            logger.error(f"Template '{template_name}' not found")
            return {'error': 'Template not found'}
        
        template = self.templates[template_name]
        
        # Utilisation des canaux spécifiés ou ceux du template
        target_channels = channels or template.channels
        
        # Formatage du message
        formatted_title = template.title.format(**data)
        formatted_message = template.message.format(**data)
        
        # Résultats d'envoi par canal
        results = {}
        
        # Envoi par canal
        for channel in target_channels:
            try:
                if channel == NotificationChannel.EMAIL:
                    results['email'] = self._send_email(
                        recipients, formatted_title, formatted_message, template
                    )
                elif channel == NotificationChannel.SLACK:
                    results['slack'] = self._send_slack(
                        formatted_title, formatted_message, template
                    )
                elif channel == NotificationChannel.TEAMS:
                    results['teams'] = self._send_teams(
                        formatted_title, formatted_message, template
                    )
                elif channel == NotificationChannel.DISCORD:
                    results['discord'] = self._send_discord(
                        formatted_title, formatted_message, template
                    )
                
            except Exception as e:
                logger.error(f"Failed to send notification via {channel.value}: {e}")
                results[channel.value] = False
        
        # Enregistrement dans l'historique
        self.notification_history.append({
            'timestamp': datetime.now().isoformat(),
            'template': template_name,
            'recipients': recipients,
            'channels': [c.value for c in target_channels],
            'data': data,
            'results': results
        })
        
        return results
    
    def _send_email(self, recipients: List[str], title: str, message: str,
                   template: NotificationTemplate) -> bool:
        """Envoie une notification par email"""
        
        if not self.email_config['username'] or not self.email_config['password']:
            logger.warning("Email configuration incomplete")
            return False
        
        try:
            # Création du message HTML gaming
            html_content = self._create_email_html(title, message, template)
            
            # Configuration SMTP
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            
            # Envoi à chaque destinataire
            for recipient in recipients:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = f"[Gaming Workforce] {title}"
                msg['From'] = self.email_config['from_address']
                msg['To'] = recipient
                
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
                
                server.sendmail(self.email_config['from_address'], recipient, msg.as_string())
            
            server.quit()
            logger.info(f"Email sent successfully to {len(recipients)} recipients")
            return True
            
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return False
    
    def _create_email_html(self, title: str, message: str, template: NotificationTemplate) -> str:
        """Crée le contenu HTML de l'email avec thème gaming"""
        
        color = template.metadata.get('color', '#3498db')
        icon = template.metadata.get('icon', '🎮')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Exo+2:wght@400;600&display=swap');
                body {{
                    font-family: 'Exo 2', Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
                    color: #ecf0f1;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px;
                    overflow: hidden;
                    box-shadow: 0 8px 32px rgba(0, 130, 196, 0.3);
                }}
                .header {{
                    background: linear-gradient(135deg, {color}, {color}CC);
                    padding: 30px 20px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    font-family: 'Orbitron', monospace;
                    font-size: 24px;
                    margin: 0;
                    text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
                }}
                .icon {{
                    font-size: 48px;
                    margin-bottom: 10px;
                    display: block;
                }}
                .content {{
                    padding: 30px 20px;
                    background: rgba(255, 255, 255, 0.95);
                    color: #2c3e50;
                }}
                .message {{
                    font-size: 16px;
                    line-height: 1.8;
                    margin-bottom: 20px;
                }}
                .footer {{
                    background: #34495e;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #bdc3c7;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(45deg, #0082c4, #00d4ff);
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin: 10px 0;
                }}
                .alert-info {{ border-left: 4px solid #3498db; }}
                .alert-warning {{ border-left: 4px solid #f39c12; }}
                .alert-critical {{ border-left: 4px solid #e74c3c; }}
                .alert-success {{ border-left: 4px solid #27ae60; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <span class="icon">{icon}</span>
                    <h1>🎮 Gaming Workforce Observatory</h1>
                    <h2>{title}</h2>
                </div>
                <div class="content alert-{template.level.value}">
                    <div class="message">
                        {message}
                    </div>
                    <div style="margin-top: 20px;">
                        <strong>Timestamp:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
                        <strong>Priority:</strong> {template.level.value.title()}<br>
                        <strong>System:</strong> Gaming Workforce Observatory Enterprise
                    </div>
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="https://gaming-workforce-observatory.streamlit.app" class="button">
                            View Dashboard
                        </a>
                    </div>
                </div>
                <div class="footer">
                    <p>🎮 Gaming Workforce Observatory Enterprise | Confidential</p>
                    <p>This notification was sent automatically based on your alert preferences.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _send_slack(self, title: str, message: str, template: NotificationTemplate) -> bool:
        """Envoie une notification Slack"""
        
        if not self.slack_config['webhook_url']:
            logger.warning("Slack webhook URL not configured")
            return False
        
        try:
            color = template.metadata.get('color', '#3498db')
            icon = template.metadata.get('icon', '🎮')
            
            slack_payload = {
                "channel": self.slack_config['channel'],
                "username": "Gaming Workforce Bot",
                "icon_emoji": ":video_game:",
                "attachments": [
                    {
                        "color": color,
                        "title": f"{icon} {title}",
                        "text": message,
                        "fields": [
                            {
                                "title": "Priority",
                                "value": template.level.value.title(),
                                "short": True
                            },
                            {
                                "title": "Timestamp",
                                "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "short": True
                            }
                        ],
                        "footer": "Gaming Workforce Observatory",
                        "footer_icon": "https://streamlit.io/favicon.ico",
                        "ts": int(datetime.now().timestamp())
                    }
                ]
            }
            
            response = requests.post(
                self.slack_config['webhook_url'],
                json=slack_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Slack notification sent successfully")
                return True
            else:
                logger.error(f"Slack notification failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Slack notification error: {e}")
            return False
    
    def _send_teams(self, title: str, message: str, template: NotificationTemplate) -> bool:
        """Envoie une notification Microsoft Teams"""
        
        if not self.teams_config['webhook_url']:
            logger.warning("Teams webhook URL not configured")
            return False
        
        try:
            color = template.metadata.get('color', '3498db').replace('#', '')
            icon = template.metadata.get('icon', '🎮')
            
            teams_payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": color,
                "summary": title,
                "sections": [
                    {
                        "activityTitle": f"{icon} Gaming Workforce Observatory",
                        "activitySubtitle": title,
                        "activityImage": "https://streamlit.io/favicon.ico",
                        "facts": [
                            {
                                "name": "Message",
                                "value": message
                            },
                            {
                                "name": "Priority",
                                "value": template.level.value.title()
                            },
                            {
                                "name": "Timestamp",
                                "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                        ]
                    }
                ],
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": "View Dashboard",
                        "targets": [
                            {
                                "os": "default",
                                "uri": "https://gaming-workforce-observatory.streamlit.app"
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.teams_config['webhook_url'],
                json=teams_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Teams notification sent successfully")
                return True
            else:
                logger.error(f"Teams notification failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Teams notification error: {e}")
            return False
    
    def _send_discord(self, title: str, message: str, template: NotificationTemplate) -> bool:
        """Envoie une notification Discord"""
        
        if not self.discord_config['webhook_url']:
            logger.warning("Discord webhook URL not configured")
            return False
        
        try:
            color_hex = template.metadata.get('color', '#3498db').replace('#', '')
            color_int = int(color_hex, 16)
            icon = template.metadata.get('icon', '🎮')
            
            discord_payload = {
                "username": "Gaming Workforce Bot",
                "avatar_url": "https://streamlit.io/favicon.ico",
                "embeds": [
                    {
                        "title": f"{icon} {title}",
                        "description": message,
                        "color": color_int,
                        "fields": [
                            {
                                "name": "Priority",
                                "value": template.level.value.title(),
                                "inline": True
                            },
                            {
                                "name": "System",
                                "value": "Gaming Workforce Observatory",
                                "inline": True
                            }
                        ],
                        "timestamp": datetime.now().isoformat(),
                        "footer": {
                            "text": "Gaming Workforce Observatory Enterprise"
                        }
                    }
                ]
            }
            
            response = requests.post(
                self.discord_config['webhook_url'],
                json=discord_payload,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                logger.info("Discord notification sent successfully")
                return True
            else:
                logger.error(f"Discord notification failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Discord notification error: {e}")
            return False
    
    def monitor_workforce_metrics(self, metrics_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Monitore les métriques et déclenche des alertes automatiques"""
        
        triggered_alerts = []
        
        # Vérification des seuils d'alerte
        for employee_id, employee_data in metrics_data.get('employees', {}).items():
            
            # Risque d'attrition élevé
            attrition_risk = employee_data.get('attrition_risk', 0)
            if attrition_risk >= self.alert_thresholds['attrition_risk_critical']:
                
                alert_data = {
                    'employee_name': employee_data.get('name', 'Unknown'),
                    'employee_id': employee_id,
                    'department': employee_data.get('department', 'Unknown'),
                    'risk_score': f"{attrition_risk*100:.1f}"
                }
                
                # Destinataires selon le département
                recipients = self._get_department_managers(employee_data.get('department'))
                
                self.send_notification(
                    'employee_high_risk',
                    recipients,
                    alert_data
                )
                
                triggered_alerts.append({
                    'type': 'high_attrition_risk',
                    'employee_id': employee_id,
                    'data': alert_data
                })
        
        # Vérification satisfaction d'équipe
        for dept, dept_data in metrics_data.get('departments', {}).items():
            satisfaction = dept_data.get('avg_satisfaction', 10)
            
            if satisfaction <= self.alert_thresholds['satisfaction_warning']:
                
                alert_data = {
                    'department': dept,
                    'satisfaction_score': f"{satisfaction:.1f}"
                }
                
                recipients = self._get_department_managers(dept)
                
                self.send_notification(
                    'team_satisfaction_drop',
                    recipients,
                    alert_data
                )
                
                triggered_alerts.append({
                    'type': 'low_satisfaction',
                    'department': dept,
                    'data': alert_data
                })
        
        return triggered_alerts
    
    def _get_department_managers(self, department: str) -> List[str]:
        """Retourne la liste des managers d'un département"""
        
        # Configuration des managers par département
        department_managers = {
            'Programming': ['tech-lead@company.com', 'cto@company.com'],
            'Art & Animation': ['art-director@company.com', 'creative-director@company.com'],
            'Game Design': ['design-lead@company.com', 'product-manager@company.com'],
            'Quality Assurance': ['qa-manager@company.com', 'product-manager@company.com'],
            'Production': ['producer@company.com', 'project-manager@company.com']
        }
        
        return department_managers.get(department, ['hr@company.com', 'manager@company.com'])
    
    def schedule_recurring_reports(self, report_config: Dict[str, Any]):
        """Programme des rapports récurrents"""
        
        # Rapport hebdomadaire
        if report_config.get('weekly_summary', False):
            schedule.every().monday.at("09:00").do(
                self._send_weekly_summary
            )
        
        # Rapport mensuel
        if report_config.get('monthly_report', False):
            schedule.every().month.do(
                self._send_monthly_report
            )
        
        # Alertes quotidiennes
        if report_config.get('daily_alerts', True):
            schedule.every().day.at("08:00").do(
                self._check_daily_alerts
            )
    
    def _send_weekly_summary(self):
        """Envoie le résumé hebdomadaire"""
        
        # Données simulées du résumé
        summary_data = {
            'week_start': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'week_end': datetime.now().strftime('%Y-%m-%d'),
            'total_employees': 850,
            'new_hires': 12,
            'departures': 5,
            'avg_satisfaction': 7.2,
            'projects_completed': 3
        }
        
        self.send_notification(
            'weekly_summary',
            ['management@company.com', 'hr@company.com'],
            summary_data,
            [NotificationChannel.EMAIL]
        )
    
    def _send_monthly_report(self):
        """Envoie le rapport mensuel"""
        # Implémentation du rapport mensuel
        pass
    
    def _check_daily_alerts(self):
        """Vérifie les alertes quotidiennes"""
        # Implémentation des vérifications quotidiennes
        pass
    
    def _start_scheduler(self):
        """Démarre le scheduler en arrière-plan"""
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Vérification chaque minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
    
    def render_notification_interface(self):
        """Interface Streamlit pour la gestion des notifications"""
        
        st.markdown("## 📢 Notification Management Center")
        st.markdown("*Configure and monitor multi-channel notifications for gaming workforce*")
        
        # Onglets
        tab1, tab2, tab3, tab4 = st.tabs(["Send Notification", "Templates", "Settings", "History"])
        
        with tab1:
            st.markdown("### 🚀 Send Custom Notification")
            
            col1, col2 = st.columns(2)
            
            with col1:
                template_name = st.selectbox(
                    "Notification Template:",
                    list(self.templates.keys())
                )
                
                recipients = st.text_area(
                    "Recipients (one email per line):",
                    "manager@company.com\nhr@company.com"
                )
                
                channels = st.multiselect(
                    "Notification Channels:",
                    [channel.value for channel in NotificationChannel],
                    default=['email', 'slack']
                )
            
            with col2:
                st.markdown("**Template Preview:**")
                if template_name:
                    template = self.templates[template_name]
                    st.info(f"**Title:** {template.title}")
                    st.info(f"**Message:** {template.message}")
                    st.info(f"**Level:** {template.level.value}")
            
            # Données pour le template
            st.markdown("### 📝 Template Data")
            template_data = {}
            
            if template_name == 'employee_high_risk':
                col1, col2, col3 = st.columns(3)
                with col1:
                    template_data['employee_name'] = st.text_input("Employee Name", "John Doe")
                with col2:
                    template_data['department'] = st.text_input("Department", "Programming")
                with col3:
                    template_data['risk_score'] = st.text_input("Risk Score (%)", "85.5")
            
            elif template_name == 'team_satisfaction_drop':
                col1, col2 = st.columns(2)
                with col1:
                    template_data['department'] = st.text_input("Department", "Quality Assurance")
                with col2:
                    template_data['satisfaction_score'] = st.text_input("Satisfaction Score", "6.2")
            
            # Envoi
            if st.button("📤 Send Notification"):
                recipient_list = [email.strip() for email in recipients.split('\n') if email.strip()]
                selected_channels = [NotificationChannel(ch) for ch in channels]
                
                with st.spinner("Sending notification..."):
                    results = self.send_notification(
                        template_name,
                        recipient_list,
                        template_data,
                        selected_channels
                    )
                
                # Affichage des résultats
                success_channels = [ch for ch, success in results.items() if success]
                failed_channels = [ch for ch, success in results.items() if not success]
                
                if success_channels:
                    st.success(f"✅ Notification sent successfully via: {', '.join(success_channels)}")
                
                if failed_channels:
                    st.error(f"❌ Failed to send via: {', '.join(failed_channels)}")
        
        with tab2:
            st.markdown("### 📋 Notification Templates")
            
            for template_name, template in self.templates.items():
                with st.expander(f"{template.metadata.get('icon', '📢')} {template_name.replace('_', ' ').title()}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Title:** {template.title}")
                        st.markdown(f"**Message:** {template.message}")
                        st.markdown(f"**Level:** {template.level.value}")
                    
                    with col2:
                        st.markdown(f"**Channels:** {', '.join([ch.value for ch in template.channels])}")
                        st.markdown(f"**Color:** {template.metadata.get('color', 'Default')}")
                        st.markdown(f"**Icon:** {template.metadata.get('icon', 'Default')}")
        
        with tab3:
            st.markdown("### ⚙️ Notification Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📧 Email Configuration")
                email_enabled = st.checkbox("Enable Email Notifications", value=True)
                if email_enabled:
                    st.text_input("SMTP Server", value=self.email_config.get('smtp_server', ''))
                    st.number_input("SMTP Port", value=self.email_config.get('smtp_port', 587))
                
                st.markdown("#### 💬 Slack Configuration")
                slack_enabled = st.checkbox("Enable Slack Notifications", value=True)
                if slack_enabled:
                    st.text_input("Webhook URL", value="[Configured]" if self.slack_config.get('webhook_url') else "")
                    st.text_input("Channel", value=self.slack_config.get('channel', ''))
            
            with col2:
                st.markdown("#### 🎯 Alert Thresholds")
                
                new_attrition_threshold = st.slider(
                    "Attrition Risk Critical (%)",
                    0, 100,
                    int(self.alert_thresholds['attrition_risk_critical'] * 100)
                ) / 100
                
                new_satisfaction_threshold = st.slider(
                    "Satisfaction Warning (1-10)",
                    1.0, 10.0,
                    self.alert_thresholds['satisfaction_warning']
                )
                
                if st.button("💾 Save Settings"):
                    self.alert_thresholds['attrition_risk_critical'] = new_attrition_threshold
                    self.alert_thresholds['satisfaction_warning'] = new_satisfaction_threshold
                    st.success("Settings saved successfully!")
        
        with tab4:
            st.markdown("### 📊 Notification History")
            
            if self.notification_history:
                history_df = pd.DataFrame(self.notification_history)
                
                # Métriques d'historique
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Sent", len(history_df))
                with col2:
                    success_rate = history_df['results'].apply(
                        lambda x: any(x.values()) if isinstance(x, dict) else False
                    ).mean() * 100
                    st.metric("Success Rate", f"{success_rate:.1f}%")
                with col3:
                    most_used_template = history_df['template'].mode().iloc[0] if len(history_df) > 0 else "N/A"
                    st.metric("Most Used Template", most_used_template.replace('_', ' ').title())
                with col4:
                    recent_count = len(history_df[
                        pd.to_datetime(history_df['timestamp']) > datetime.now() - timedelta(days=1)
                    ])
                    st.metric("Last 24h", recent_count)
                
                # Historique détaillé
                st.markdown("#### Recent Notifications")
                
                display_df = history_df[['timestamp', 'template', 'channels', 'results']].copy()
                display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
                display_df['template'] = display_df['template'].str.replace('_', ' ').str.title()
                display_df['success'] = display_df['results'].apply(
                    lambda x: "✅" if (any(x.values()) if isinstance(x, dict) else False) else "❌"
                )
                
                st.dataframe(
                    display_df[['timestamp', 'template', 'channels', 'success']].head(10),
                    use_container_width=True
                )
            
            else:
                st.info("No notification history available yet.")
