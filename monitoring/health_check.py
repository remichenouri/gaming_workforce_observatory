"""
Health check endpoint for monitoring Gaming Workforce Observatory
"""
import streamlit as st
import pandas as pd
import time
import psutil
import sys
from datetime import datetime
from src.data.loader import DataLoader
from src.data.kpis import GameKPICalculator

def check_system_health():
    """Check system health metrics"""
    health = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy',
        'checks': {}
    }
    
    try:
        # Memory check
        memory = psutil.virtual_memory()
        health['checks']['memory'] = {
            'used_percent': memory.percent,
            'available_mb': memory.available // 1024 // 1024,
            'status': 'ok' if memory.percent < 80 else 'warning'
        }
        
        # CPU check
        cpu_percent = psutil.cpu_percent(interval=1)
        health['checks']['cpu'] = {
            'usage_percent': cpu_percent,
            'status': 'ok' if cpu_percent < 80 else 'warning'
        }
        
        # Disk check
        disk = psutil.disk_usage('/')
        health['checks']['disk'] = {
            'used_percent': (disk.used / disk.total) * 100,
            'free_gb': disk.free // 1024 // 1024 // 1024,
            'status': 'ok' if (disk.used / disk.total) * 100 < 80 else 'warning'
        }
        
        # Data loading check
        start_time = time.time()
        loader = DataLoader()
        df = loader.load_sample_data()
        load_time = time.time() - start_time
        
        health['checks']['data_loading'] = {
            'load_time_seconds': round(load_time, 2),
            'records_count': len(df),
            'status': 'ok' if load_time < 2.0 else 'warning'
        }
        
        # KPI calculation check
        start_time = time.time()
        calculator = GameKPICalculator(df)
        kpis = calculator.calculate_all_kpis()
        calc_time = time.time() - start_time
        
        health['checks']['kpi_calculation'] = {
            'calculation_time_seconds': round(calc_time, 2),
            'kpis_count': len(kpis),
            'status': 'ok' if calc_time < 1.0 else 'warning'
        }
        
        # Overall status
        if any(check['status'] == 'warning' for check in health['checks'].values()):
            health['status'] = 'warning'
            
    except Exception as e:
        health['status'] = 'error'
        health['error'] = str(e)
    
    return health

def display_health_dashboard():
    """Display health monitoring dashboard"""
    st.title("🏥 Gaming Workforce Observatory - Health Check")
    
    # Auto-refresh every 30 seconds
    if st.button("🔄 Refresh Health Status"):
        st.rerun()
    
    with st.spinner("Checking system health..."):
        health = check_system_health()
    
    # Status indicator
    status_colors = {
        'healthy': '🟢',
        'warning': '🟡', 
        'error': '🔴'
    }
    
    st.header(f"{status_colors[health['status']]} Overall Status: {health['status'].title()}")
    st.write(f"**Last Check:** {health['timestamp']}")
    
    if health['status'] == 'error':
        st.error(f"❌ **Error:** {health.get('error', 'Unknown error')}")
        return
    
    # Detailed checks
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖥️ System Resources")
        
        if 'memory' in health['checks']:
            memory = health['checks']['memory']
            st.metric(
                "Memory Usage",
                f"{memory['used_percent']:.1f}%",
                f"{memory['available_mb']} MB available"
            )
        
        if 'cpu' in health['checks']:
            cpu = health['checks']['cpu']
            st.metric("CPU Usage", f"{cpu['usage_percent']:.1f}%")
        
        if 'disk' in health['checks']:
            disk = health['checks']['disk']
            st.metric(
                "Disk Usage",
                f"{disk['used_percent']:.1f}%",
                f"{disk['free_gb']} GB free"
            )
    
    with col2:
        st.subheader("📊 Application Performance")
        
        if 'data_loading' in health['checks']:
            data = health['checks']['data_loading']
            st.metric(
                "Data Loading",
                f"{data['load_time_seconds']}s",
                f"{data['records_count']} records"
            )
        
        if 'kpi_calculation' in health['checks']:
            kpis = health['checks']['kpi_calculation']
            st.metric(
                "KPI Calculation",
                f"{kpis['calculation_time_seconds']}s",
                f"{kpis['kpis_count']} KPIs"
            )
    
    # Performance recommendations
    st.subheader("💡 Performance Recommendations")
    
    recommendations = []
    
    if health['checks'].get('memory', {}).get('used_percent', 0) > 70:
        recommendations.append("⚠️ High memory usage detected. Consider optimizing data caching.")
    
    if health['checks'].get('data_loading', {}).get('load_time_seconds', 0) > 1.5:
        recommendations.append("⚠️ Slow data loading. Consider data preprocessing or indexing.")
    
    if not recommendations:
        st.success("✅ All systems running optimally!")
    else:
        for rec in recommendations:
            st.warning(rec)

if __name__ == "__main__":
    display_health_dashboard()
