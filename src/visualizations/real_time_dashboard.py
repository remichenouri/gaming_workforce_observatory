"""
Gaming Workforce Observatory - Real-time Dashboard
Dashboard temps réel avec WebSocket et auto-refresh
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import asyncio
import json
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class RealTimeDashboard:
    """Dashboard temps réel pour monitoring gaming workforce"""
    
    def __init__(self):
        self.refresh_interval = 30  # secondes
        self.last_update = datetime.now()
        self.metrics_history = []
        
        # Métriques temps réel
        self.current_metrics = {
            'active_employees': 0,
            'avg_satisfaction': 0,
            'critical_alerts': 0,
            'projects_active': 0,
            'crunch_teams': 0,
            'hiring_pipeline': 0
        }
        
        # Configuration alertes
        self.alert_thresholds = {
            'satisfaction_critical': 5.0,
            'crunch_hours_critical': 60,
            'attrition_risk_high': 0.7,
            'performance_drop': 0.2
        }
    
    def initialize_dashboard(self):
        """Initialise le dashboard avec configuration"""
        
        st.set_page_config(
            page_title="Gaming Workforce Real-time Dashboard",
            page_icon="🎮",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # CSS personnalisé pour le temps réel
        st.markdown("""
        <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
        }
        .alert-critical {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            animation: pulse 2s infinite;
        }
        .alert-warning {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }
        .metric-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-good { background-color: #27ae60; }
        .status-warning { background-color: #f39c12; }
        .status-critical { background-color: #e74c3c; }
        </style>
        """, unsafe_allow_html=True)
    
    def generate_realtime_data(self) -> Dict[str, Any]:
        """Génère des données temps réel simulées"""
        
        current_time = datetime.now()
        
        # Simulation données temps réel
        base_employees = 850
        time_factor = np.sin((current_time.hour + current_time.minute/60) * np.pi / 12)
        
        realtime_data = {
            'timestamp': current_time.isoformat(),
            'active_employees': int(base_employees + time_factor * 50),
            'avg_satisfaction': max(1, min(10, 7.2 + np.random.normal(0, 0.5))),
            'critical_alerts': np.random.poisson(2),
            'projects_active': 23 + np.random.randint(-2, 3),
            'crunch_teams': max(0, int(5 + np.random.normal(0, 2))),
            'hiring_pipeline': 47 + np.random.randint(-5, 8),
            'system_health': np.random.choice(['healthy', 'warning', 'critical'], p=[0.7, 0.25, 0.05]),
            'response_time_ms': max(10, np.random.normal(150, 30)),
            'data_freshness_minutes': np.random.randint(1, 10)
        }
        
        # Ajout à l'historique
        self.metrics_history.append(realtime_data)
        if len(self.metrics_history) > 100:  # Garder 100 derniers points
            self.metrics_history = self.metrics_history[-100:]
        
        return realtime_data
    
    def create_metrics_overview(self, realtime_data: Dict[str, Any]):
        """Crée la vue d'ensemble des métriques temps réel"""
        
        st.markdown("### 📊 Real-time Metrics Overview")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            active_employees = realtime_data['active_employees']
            delta_employees = active_employees - 850  # baseline
            st.metric(
                "👥 Active Employees",
                f"{active_employees:,}",
                delta=f"{delta_employees:+d}" if delta_employees != 0 else None
            )
        
        with col2:
            satisfaction = realtime_data['avg_satisfaction']
            satisfaction_status = "🟢" if satisfaction >= 7 else "🟡" if satisfaction >= 5 else "🔴"
            st.metric(
                f"{satisfaction_status} Avg Satisfaction",
                f"{satisfaction:.1f}/10",
                delta=f"{satisfaction - 7.2:.1f}" if satisfaction != 7.2 else None
            )
        
        with col3:
            alerts = realtime_data['critical_alerts']
            alert_status = "🔴" if alerts > 5 else "🟡" if alerts > 2 else "🟢"
            st.metric(
                f"{alert_status} Critical Alerts",
                alerts,
                delta=f"{alerts - 2:+d}" if alerts != 2 else None,
                delta_color="inverse"
            )
        
        with col4:
            projects = realtime_data['projects_active']
            st.metric(
                "🎮 Active Projects",
                projects,
                delta=f"{projects - 23:+d}" if projects != 23 else None
            )
        
        with col5:
            crunch_teams = realtime_data['crunch_teams']
            crunch_status = "🔴" if crunch_teams > 8 else "🟡" if crunch_teams > 4 else "🟢"
            st.metric(
                f"{crunch_status} Teams in Crunch",
                crunch_teams,
                delta=f"{crunch_teams - 5:+d}" if crunch_teams != 5 else None,
                delta_color="inverse"
            )
        
        with col6:
            pipeline = realtime_data['hiring_pipeline']
            st.metric(
                "🎯 Hiring Pipeline",
                pipeline,
                delta=f"{pipeline - 47:+d}" if pipeline != 47 else None
            )
    
    def create_realtime_alerts_panel(self, realtime_data: Dict[str, Any]):
        """Panneau d'alertes temps réel"""
        
        st.markdown("### 🚨 Real-time Alerts")
        
        alerts = []
        
        # Génération d'alertes basées sur les métriques
        if realtime_data['avg_satisfaction'] < self.alert_thresholds['satisfaction_critical']:
            alerts.append({
                'level': 'critical',
                'title': 'Critical Satisfaction Drop',
                'message': f"Average satisfaction at {realtime_data['avg_satisfaction']:.1f}/10",
                'action': 'Immediate team intervention required',
                'timestamp': realtime_data['timestamp']
            })
        
        if realtime_data['crunch_teams'] > 8:
            alerts.append({
                'level': 'critical',
                'title': 'Excessive Crunch Detected',
                'message': f"{realtime_data['crunch_teams']} teams in crunch mode",
                'action': 'Review resource allocation urgently',
                'timestamp': realtime_data['timestamp']
            })
        
        if realtime_data['critical_alerts'] > 5:
            alerts.append({
                'level': 'warning',
                'title': 'High Alert Volume',
                'message': f"{realtime_data['critical_alerts']} critical alerts active",
                'action': 'Investigate system issues',
                'timestamp': realtime_data['timestamp']
            })
        
        # Simulation d'alertes supplémentaires
        if np.random.random() < 0.3:  # 30% chance
            sample_alerts = [
                {
                    'level': 'warning',
                    'title': 'Performance Degradation',
                    'message': 'Art team showing 15% performance drop',
                    'action': 'Schedule team check-in',
                    'timestamp': realtime_data['timestamp']
                },
                {
                    'level': 'info',
                    'title': 'New Hire Onboarding',
                    'message': '3 new developers starting next week',
                    'action': 'Prepare onboarding materials',
                    'timestamp': realtime_data['timestamp']
                }
            ]
            alerts.extend(np.random.choice(sample_alerts, size=1))
        
        if not alerts:
            st.success("✅ No active alerts - All systems nominal")
        else:
            for alert in alerts:
                alert_color = {
                    'critical': '#e74c3c',
                    'warning': '#f39c12',
                    'info': '#3498db'
                }.get(alert['level'], '#95a5a6')
                
                alert_icon = {
                    'critical': '🔴',
                    'warning': '🟡',
                    'info': '🔵'
                }.get(alert['level'], 'ℹ️')
                
                with st.expander(f"{alert_icon} {alert['title']}", expanded=(alert['level'] == 'critical')):
                    st.markdown(f"**Message:** {alert['message']}")
                    st.markdown(f"**Recommended Action:** {alert['action']}")
                    st.markdown(f"**Time:** {alert['timestamp'][:19]}")
    
    def create_trend_charts(self, history_data: List[Dict[str, Any]]):
        """Graphiques de tendances temps réel"""
        
        if len(history_data) < 2:
            st.info("Accumulating data for trend analysis...")
            return
        
        st.markdown("### 📈 Real-time Trends")
        
        # Conversion en DataFrame
        df_history = pd.DataFrame(history_data)
        df_history['timestamp'] = pd.to_datetime(df_history['timestamp'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Tendance satisfaction
            fig_satisfaction = go.Figure()
            fig_satisfaction.add_trace(go.Scatter(
                x=df_history['timestamp'],
                y=df_history['avg_satisfaction'],
                mode='lines+markers',
                name='Satisfaction',
                line=dict(color='#27ae60', width=3)
            ))
            
            fig_satisfaction.add_hline(
                y=self.alert_thresholds['satisfaction_critical'],
                line_dash="dash",
                line_color="red",
                annotation_text="Critical Threshold"
            )
            
            fig_satisfaction.update_layout(
                title='Team Satisfaction Trend',
                xaxis_title='Time',
                yaxis_title='Satisfaction Score',
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig_satisfaction, use_container_width=True)
        
        with col2:
            # Tendance équipes en crunch
            fig_crunch = go.Figure()
            fig_crunch.add_trace(go.Scatter(
                x=df_history['timestamp'],
                y=df_history['crunch_teams'],
                mode='lines+markers',
                name='Crunch Teams',
                line=dict(color='#e74c3c', width=3),
                fill='tozeroy',
                fillcolor='rgba(231, 76, 60, 0.1)'
            ))
            
            fig_crunch.update_layout(
                title='Teams in Crunch Mode',
                xaxis_title='Time',
                yaxis_title='Number of Teams',
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig_crunch, use_container_width=True)
        
        # Graphique combiné des métriques principales
        st.markdown("#### 📊 Combined Metrics View")
        
        fig_combined = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Active Employees', 'Critical Alerts', 'Active Projects', 'Hiring Pipeline'),
            vertical_spacing=0.1
        )
        
        # Active Employees
        fig_combined.add_trace(
            go.Scatter(x=df_history['timestamp'], y=df_history['active_employees'],
                      mode='lines', name='Active Employees', line=dict(color='#3498db')),
            row=1, col=1
        )
        
        # Critical Alerts
        fig_combined.add_trace(
            go.Scatter(x=df_history['timestamp'], y=df_history['critical_alerts'],
                      mode='lines+markers', name='Critical Alerts', line=dict(color='#e74c3c')),
            row=1, col=2
        )
        
        # Active Projects
        fig_combined.add_trace(
            go.Scatter(x=df_history['timestamp'], y=df_history['projects_active'],
                      mode='lines', name='Active Projects', line=dict(color='#9b59b6')),
            row=2, col=1
        )
        
        # Hiring Pipeline
        fig_combined.add_trace(
            go.Scatter(x=df_history['timestamp'], y=df_history['hiring_pipeline'],
                      mode='lines', name='Hiring Pipeline', line=dict(color='#f39c12')),
            row=2, col=2
        )
        
        fig_combined.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_combined, use_container_width=True)
    
    def create_system_health_panel(self, realtime_data: Dict[str, Any]):
        """Panneau de santé système"""
        
        st.markdown("### 💻 System Health")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            health_status = realtime_data['system_health']
            health_color = {
                'healthy': '🟢',
                'warning': '🟡',
                'critical': '🔴'
            }.get(health_status, '⚪')
            
            st.markdown(f"**Overall Status:** {health_color} {health_status.title()}")
        
        with col2:
            response_time = realtime_data['response_time_ms']
            response_status = "🟢" if response_time < 200 else "🟡" if response_time < 500 else "🔴"
            st.markdown(f"**Response Time:** {response_status} {response_time:.0f}ms")
        
        with col3:
            freshness = realtime_data['data_freshness_minutes']
            freshness_status = "🟢" if freshness < 5 else "🟡" if freshness < 10 else "🔴"
            st.markdown(f"**Data Freshness:** {freshness_status} {freshness}min")
        
        with col4:
            uptime = "99.8%"  # Simulé
            st.markdown(f"**Uptime:** 🟢 {uptime}")
    
    def run_realtime_dashboard(self):
        """Lance le dashboard temps réel principal"""
        
        self.initialize_dashboard()
        
        # Header
        st.markdown("# 🎮 Gaming Workforce Real-time Dashboard")
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown("*Live monitoring of gaming workforce metrics*")
        with col2:
            if st.button("🔄 Refresh Now"):
                st.rerun()
        with col3:
            auto_refresh = st.checkbox("Auto-refresh", value=True)
        
        # Timestamp et statut
        current_time = datetime.now()
        st.markdown(f"**Last Updated:** {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Génération données temps réel
        realtime_data = self.generate_realtime_data()
        
        # Métriques principales
        self.create_metrics_overview(realtime_data)
        
        st.divider()
        
        # Layout en colonnes
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Graphiques de tendances
            self.create_trend_charts(self.metrics_history)
        
        with col2:
            # Alertes
            self.create_realtime_alerts_panel(realtime_data)
            
            st.divider()
            
            # Santé système
            self.create_system_health_panel(realtime_data)
        
        # Auto-refresh
        if auto_refresh:
            time.sleep(self.refresh_interval)
            st.rerun()
    
    def create_team_activity_heatmap(self, activity_data: pd.DataFrame = None):
        """Heatmap d'activité des équipes en temps réel"""
        
        if activity_data is None:
            # Génération de données d'activité simulées
            departments = ['Programming', 'Art & Animation', 'Game Design', 'QA', 'Production']
            hours = list(range(9, 19))  # 9h à 18h
            
            activity_matrix = []
            for dept in departments:
                dept_activity = []
                for hour in hours:
                    # Simulation d'activité basée sur l'heure
                    base_activity = 50
                    hour_factor = np.sin((hour - 9) * np.pi / 10) * 30
                    noise = np.random.normal(0, 10)
                    activity = max(0, min(100, base_activity + hour_factor + noise))
                    dept_activity.append(activity)
                activity_matrix.append(dept_activity)
            
            activity_df = pd.DataFrame(
                activity_matrix,
                index=departments,
                columns=[f"{hour}:00" for hour in hours]
            )
        else:
            activity_df = activity_data
        
        fig = go.Figure(data=go.Heatmap(
            z=activity_df.values,
            x=activity_df.columns,
            y=activity_df.index,
            colorscale='Viridis',
            text=np.round(activity_df.values, 0),
            texttemplate="%{text}%",
            textfont={"size": 10},
            colorbar=dict(title="Activity Level (%)")
        ))
        
        fig.update_layout(
            title='🔥 Real-time Team Activity Heatmap',
            xaxis_title='Time of Day',
            yaxis_title='Department',
            height=300
        )
        
        return fig
    
    def create_live_kpi_gauges(self, kpi_data: Dict[str, float]):
        """Gauges KPI en temps réel"""
        
        fig = make_subplots(
            rows=1, cols=3,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
            subplot_titles=('Productivity', 'Team Health', 'Project Progress')
        )
        
        # Gauge Productivité
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=kpi_data.get('productivity', 75),
                title={'text': "Productivity %"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "#1f77b4"},
                       'steps': [{'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "green"}]},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=1
        )
        
        # Gauge Santé équipe
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=kpi_data.get('team_health', 82),
                title={'text': "Team Health %"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "#ff7f0e"},
                       'steps': [{'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "green"}]},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=2
        )
        
        # Gauge Progrès projet
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=kpi_data.get('project_progress', 68),
                title={'text': "Project Progress %"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "#2ca02c"},
                       'steps': [{'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "green"}]},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=3
        )
        
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        
        return fig
