"""
Gaming Workforce Observatory - Performance Monitor Enterprise
Monitoring temps réel des performances avec métriques détaillées
"""
import time
import psutil
import streamlit as st
from datetime import datetime, timedelta
import threading
import queue
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor de performance enterprise pour optimisation temps réel"""
    
    def __init__(self):
        self.metrics_queue = queue.Queue()
        self.is_monitoring = False
        self.monitoring_thread = None
        self.performance_history = []
        self.alert_thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'response_time_ms': 2000,
            'concurrent_users': 100
        }
        
    def start_monitoring(self):
        """Démarre le monitoring en arrière-plan"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitoring_thread.start()
            logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Arrête le monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Boucle principale de monitoring"""
        while self.is_monitoring:
            try:
                metrics = self._collect_metrics()
                self.metrics_queue.put(metrics)
                
                # Garder historique limité
                self.performance_history.append(metrics)
                if len(self.performance_history) > 1000:
                    self.performance_history = self.performance_history[-500:]
                
                # Vérifier alertes
                self._check_alerts(metrics)
                
                time.sleep(5)  # Collecte toutes les 5 secondes
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)  # Attendre plus longtemps en cas d'erreur
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """Collecte les métriques système et application"""
        try:
            # Métriques système
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Métriques réseau
            network = psutil.net_io_counters()
            
            # Métriques Streamlit (simulées)
            concurrent_users = self._estimate_concurrent_users()
            response_time = self._measure_response_time()
            
            return {
                'timestamp': datetime.now(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': memory.used / (1024**3),
                'memory_total_gb': memory.total / (1024**3),
                'disk_percent': disk.percent,
                'disk_used_gb': disk.used / (1024**3),
                'disk_total_gb': disk.total / (1024**3),
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv,
                'concurrent_users': concurrent_users,
                'response_time_ms': response_time,
                'app_status': 'healthy'
            }
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {
                'timestamp': datetime.now(),
                'app_status': 'error',
                'error_message': str(e)
            }
    
    def _estimate_concurrent_users(self) -> int:
        """Estime le nombre d'utilisateurs concurrents"""
        # Simulation basée sur session Streamlit
        if hasattr(st, 'session_state') and st.session_state:
            return len(st.session_state) if isinstance(st.session_state, dict) else 1
        return 1
    
    def _measure_response_time(self) -> float:
        """Mesure le temps de réponse de l'application"""
        start_time = time.time()
        # Simulation d'une opération typique
        try:
            # Test rapide de base de données ou cache
            _ = datetime.now()
            end_time = time.time()
            return (end_time - start_time) * 1000  # Convertir en ms
        except:
            return 999.0  # Valeur par défaut en cas d'erreur
    
    def _check_alerts(self, metrics: Dict[str, Any]):
        """Vérifie les seuils d'alerte"""
        alerts = []
        
        if metrics.get('cpu_percent', 0) > self.alert_thresholds['cpu_percent']:
            alerts.append({
                'type': 'CPU',
                'level': 'WARNING',
                'message': f"CPU usage high: {metrics['cpu_percent']:.1f}%",
                'timestamp': metrics['timestamp']
            })
        
        if metrics.get('memory_percent', 0) > self.alert_thresholds['memory_percent']:
            alerts.append({
                'type': 'MEMORY',
                'level': 'WARNING', 
                'message': f"Memory usage high: {metrics['memory_percent']:.1f}%",
                'timestamp': metrics['timestamp']
            })
        
        if metrics.get('response_time_ms', 0) > self.alert_thresholds['response_time_ms']:
            alerts.append({
                'type': 'PERFORMANCE',
                'level': 'WARNING',
                'message': f"Response time high: {metrics['response_time_ms']:.0f}ms",
                'timestamp': metrics['timestamp']
            })
        
        # Stocker alertes en session pour affichage
        if alerts:
            if 'performance_alerts' not in st.session_state:
                st.session_state['performance_alerts'] = []
            
            st.session_state['performance_alerts'].extend(alerts)
            
            # Garder seulement les 10 dernières alertes
            st.session_state['performance_alerts'] = st.session_state['performance_alerts'][-10:]
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques actuelles"""
        try:
            return self.metrics_queue.get_nowait()
        except queue.Empty:
            if self.performance_history:
                return self.performance_history[-1]
            return {}
    
    def get_performance_history(self, minutes: int = 60) -> List[Dict[str, Any]]:
        """Retourne l'historique de performance"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        return [
            metric for metric in self.performance_history
            if metric.get('timestamp', datetime.min) > cutoff_time
        ]
    
    def render_performance_dashboard(self):
        """Affiche le dashboard de performance"""
        st.markdown("### 📊 System Performance Monitor")
        
        current_metrics = self.get_current_metrics()
        
        if current_metrics:
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                cpu_color = "🔴" if current_metrics.get('cpu_percent', 0) > 80 else "🟢"
                st.metric(
                    f"{cpu_color} CPU Usage",
                    f"{current_metrics.get('cpu_percent', 0):.1f}%"
                )
            
            with col2:
                memory_color = "🔴" if current_metrics.get('memory_percent', 0) > 85 else "🟢"
                st.metric(
                    f"{memory_color} Memory",
                    f"{current_metrics.get('memory_percent', 0):.1f}%",
                    f"{current_metrics.get('memory_used_gb', 0):.1f}GB used"
                )
            
            with col3:
                response_color = "🔴" if current_metrics.get('response_time_ms', 0) > 2000 else "🟢"
                st.metric(
                    f"{response_color} Response Time",
                    f"{current_metrics.get('response_time_ms', 0):.0f}ms"
                )
            
            with col4:
                st.metric(
                    "👥 Active Users",
                    current_metrics.get('concurrent_users', 0)
                )
            
            # Graphique historique
            history = self.get_performance_history(30)  # 30 dernières minutes
            
            if history:
                import plotly.graph_objects as go
                from plotly.subplots import make_subplots
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('CPU Usage', 'Memory Usage', 'Response Time', 'Disk Usage'),
                    vertical_spacing=0.1
                )
                
                timestamps = [h['timestamp'] for h in history]
                
                # CPU
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=[h.get('cpu_percent', 0) for h in history],
                        name='CPU %',
                        line=dict(color='#ff6b35')
                    ),
                    row=1, col=1
                )
                
                # Memory
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=[h.get('memory_percent', 0) for h in history],
                        name='Memory %',
                        line=dict(color='#667eea')
                    ),
                    row=1, col=2
                )
                
                # Response Time
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=[h.get('response_time_ms', 0) for h in history],
                        name='Response Time (ms)',
                        line=dict(color='#764ba2')
                    ),
                    row=2, col=1
                )
                
                # Disk
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=[h.get('disk_percent', 0) for h in history],
                        name='Disk %',
                        line=dict(color='#27ae60')
                    ),
                    row=2, col=2
                )
                
                fig.update_layout(height=500, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # Alertes actives
        if 'performance_alerts' in st.session_state and st.session_state['performance_alerts']:
            st.markdown("### ⚠️ Active Alerts")
            for alert in st.session_state['performance_alerts'][-5:]:  # 5 dernières
                alert_color = {"WARNING": "🟡", "ERROR": "🔴", "INFO": "🔵"}.get(alert['level'], "ℹ️")
                st.warning(f"{alert_color} {alert['type']}: {alert['message']}")
        
        # Options de configuration
        with st.expander("⚙️ Performance Settings"):
            new_cpu_threshold = st.slider("CPU Alert Threshold (%)", 50, 95, self.alert_thresholds['cpu_percent'])
            new_memory_threshold = st.slider("Memory Alert Threshold (%)", 50, 95, self.alert_thresholds['memory_percent'])
            
            if st.button("Update Thresholds"):
                self.alert_thresholds['cpu_percent'] = new_cpu_threshold
                self.alert_thresholds['memory_percent'] = new_memory_threshold
                st.success("Thresholds updated!")
