"""
🎮 Ubisoft Gaming Workforce Observatory
Admin Panel - System Management & Configuration
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ─────────────────────────────────────────────
# STUBS POUR THEME & COMPOSANTS UBISOFT
# Appliquer ABSOLUMENT dans chaque page à remplacer
def apply_ubisoft_theme():
    pass

UBISOFT_COLORS = {
    'primary': '#0099FF',
    'accent': '#E60012',
    'success': '#28A745',
    'warning': '#FFB020',
    'text': '#2C3E50'
}

def create_ubisoft_header(title, subtitle=None):
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    return f"<h1>{title}</h1>{subtitle_html}"

def create_ubisoft_breadcrumb(page):
    return f"<p>🎮 Ubisoft Observatory → {page}</p>"

def create_ubisoft_section_header(title):
    return f"<h3>{title}</h3>"

def create_ubisoft_info_box(title, content):
    return f"<div><strong>{title}</strong><p>{content}</p></div>"

def create_ubisoft_accent_box(title, content):
    return f"<div style='border-left:4px solid #E60012'><strong>{title}</strong><p>{content}</p></div>"

def get_ubisoft_chart_config():
    return {'layout': {}}

def create_ubisoft_metric_cols(metrics, cols=4):
    for metric in metrics:
        st.markdown(f"**{metric['title']}**: {metric['value']}")

def display_ubisoft_logo_section():
    return "<p>© 2024 Ubisoft</p>"

st.set_page_config(
    page_title="Ubisoft Admin Panel - System Management",
    page_icon="⚙️",
    layout="wide"
)

apply_ubisoft_theme()

st.markdown(
    create_ubisoft_header(
        "UBISOFT Admin Panel",
        "System Management & Configuration Controls"
    ),
    unsafe_allow_html=True
)

st.markdown(create_ubisoft_breadcrumb("Admin Panel"), unsafe_allow_html=True)

# Check for admin access (in real implementation, this would be proper authentication)
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.markdown(
        create_ubisoft_accent_box(
            "🔐 Ubisoft Admin Access Required",
            "Please authenticate to access the Ubisoft Gaming Workforce Observatory administrative controls."
        ),
        unsafe_allow_html=True
    )
    
    with st.form("admin_login"):
        st.markdown("### 🎮 Ubisoft Admin Authentication")
        username = st.text_input("Username", placeholder="ubisoft.admin")
        password = st.text_input("Password", type="password", placeholder="Enter admin password")
        
        if st.form_submit_button("🔓 Access Admin Panel", type="primary"):
            # Simple demo authentication (in reality, use proper auth)
            if username == "ubisoft.admin" and password == "demo123":
                st.session_state.admin_authenticated = True
                st.success("✅ Authentication successful! Welcome to Ubisoft Admin Panel.")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please contact Ubisoft IT support.")
    
    st.stop()

# Admin dashboard content
st.markdown(
    create_ubisoft_info_box(
        "⚙️ Ubisoft Gaming Workforce Observatory",
        "Administrative controls for Ubisoft HR and IT teams. Monitor system health, manage data sources, configure dashboards, and oversee user access across all Ubisoft studios worldwide."
    ),
    unsafe_allow_html=True
)

# System Health Dashboard
st.markdown(create_ubisoft_section_header("🔧 Ubisoft System Health Monitor"))

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <div style="text-align: center;">
            <div style="font-size: 3rem; color: #28A745;">✅</div>
            <div style="font-size: 2rem; font-weight: 700; color: #28A745;">99.8%</div>
            <div style="color: #F5F5F5; font-weight: 500;">System Uptime</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <div style="text-align: center;">
            <div style="font-size: 3rem; color: #0099FF;">⚡</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0099FF;">1.2s</div>
            <div style="color: #F5F5F5; font-weight: 500;">Avg Response</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <div style="text-align: center;">
            <div style="font-size: 3rem; color: #FFD700;">👥</div>
            <div style="font-size: 2rem; font-weight: 700; color: #FFD700;">847</div>
            <div style="color: #F5F5F5; font-weight: 500;">Active Users</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <div style="text-align: center;">
            <div style="font-size: 3rem; color: #E60012;">🔄</div>
            <div style="font-size: 2rem; font-weight: 700; color: #E60012;">15min</div>
            <div style="color: #F5F5F5; font-weight: 500;">Data Refresh</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Data Sources Management
st.markdown(create_ubisoft_section_header("📊 Ubisoft Data Sources Management"))

data_sources = {
    'Source': ['Workday HRIS', 'Active Directory', 'Jira Tickets', 'Confluence', 
               'GitLab Analytics', 'Slack Metrics', 'Azure DevOps', 'ServiceNow'],
    'Status': ['Active', 'Active', 'Active', 'Warning', 'Active', 'Active', 'Maintenance', 'Active'],
    'Last_Sync': ['2 min ago', '1 min ago', '5 min ago', '2 hours ago', '3 min ago', '1 min ago', '1 hour ago', '4 min ago'],
    'Records': [15847, 12450, 8934, 5623, 11287, 9876, 7234, 3456],
    'Health_Score': [98, 99, 97, 75, 96, 98, 60, 94]
}

sources_df = pd.DataFrame(data_sources)

col1, col2 = st.columns([2, 1])

with col1:
    # Create status indicators
    status_colors = {'Active': '#28A745', 'Warning': '#FFD700', 'Maintenance': '#E60012'}
    
    for _, source in sources_df.iterrows():
        status_color = status_colors.get(source['Status'], '#CCCCCC')
        st.markdown(f"""
        <div style="background: rgba(26, 26, 26, 0.95); border-left: 4px solid {status_color}; 
                    padding: 15px; margin: 10px 0; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #F5F5F5;">{source['Source']}</strong>
                    <div style="color: #CCCCCC; font-size: 0.9rem;">
                        📊 {source['Records']:,} records • Last sync: {source['Last_Sync']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <span style="color: {status_color}; font-weight: bold;">{source['Status']}</span>
                    <div style="color: #0099FF; font-size: 0.9rem;">Health: {source['Health_Score']}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Data health pie chart
    status_counts = sources_df['Status'].value_counts()
    
    fig_status = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        marker=dict(colors=['#28A745', '#E60012', '#FFD700']),
        hole=0.4
    )])
    
    fig_status.update_layout(
        title="🔍 Ubisoft Data Sources Status",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_status, use_container_width=True)

# User Management
st.markdown(create_ubisoft_section_header("👥 Ubisoft User Access Management"))

user_data = {
    'Role': ['HR Directors', 'Studio Managers', 'Team Leads', 'Analysts', 'Executives', 'IT Admins'],
    'Active_Users': [45, 128, 234, 89, 18, 12],
    'Last_7_Days': [42, 98, 187, 76, 16, 11],
    'Permissions': ['Full Access', 'Studio View', 'Team View', 'Read Only', 'Executive View', 'Admin'],
    'Avg_Session': ['24 min', '18 min', '12 min', '31 min', '8 min', '45 min']
}

users_df = pd.DataFrame(user_data)

col1, col2 = st.columns(2)

with col1:
    fig_users = px.bar(
        users_df,
        x='Role',
        y='Active_Users',
        color='Active_Users',
        title='👥 Ubisoft Active Users by Role',
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_users.update_layout(get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_users, use_container_width=True)

with col2:
    # User activity
    st.markdown("### 📊 User Activity Summary")
    for _, user in users_df.iterrows():
        activity_rate = (user['Last_7_Days'] / user['Active_Users'] * 100) if user['Active_Users'] > 0 else 0
        activity_color = '#28A745' if activity_rate > 80 else '#FFD700' if activity_rate > 60 else '#E60012'
        
        st.markdown(f"""
        **{user['Role']}**  
        👥 {user['Active_Users']} active • 🔄 {user['Last_7_Days']} weekly  
        <span style="color: {activity_color};">📈 {activity_rate:.1f}% engagement</span>  
        ⏱️ Avg session: {user['Avg_Session']}
        """, unsafe_allow_html=True)

# System Configuration
st.markdown(create_ubisoft_section_header("⚙️ Ubisoft System Configuration"))

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔧 Dashboard Settings")
    
    with st.form("dashboard_config"):
        refresh_interval = st.selectbox(
            "Data Refresh Interval",
            options=[5, 10, 15, 30, 60],
            index=2,
            help="Minutes between automatic data refreshes"
        )
        
        cache_duration = st.selectbox(
            "Cache Duration",
            options=[10, 30, 60, 120],
            index=1,
            help="Minutes to cache dashboard data"
        )
        
        enable_notifications = st.checkbox("Enable System Notifications", value=True)
        enable_audit_logs = st.checkbox("Enable Audit Logging", value=True)
        
        if st.form_submit_button("💾 Save Configuration"):
            st.success("✅ Configuration saved successfully!")

with col2:
    st.markdown("### 📈 Performance Tuning")
    
    with st.form("performance_config"):
        max_concurrent_users = st.number_input(
            "Max Concurrent Users",
            min_value=100,
            max_value=2000,
            value=1000,
            step=100
        )
        
        query_timeout = st.number_input(
            "Query Timeout (seconds)",
            min_value=30,
            max_value=300,
            value=120,
            step=30
        )
        
        enable_compression = st.checkbox("Enable Data Compression", value=True)
        enable_ssl = st.checkbox("Force SSL/HTTPS", value=True)
        
        if st.form_submit_button("🚀 Apply Performance Settings"):
            st.success("✅ Performance settings applied!")

# Audit Logs
st.markdown(create_ubisoft_section_header("📋 Ubisoft System Audit Logs"))

# Generate sample audit data
audit_data = {
    'Timestamp': [datetime.now() - timedelta(minutes=x*15) for x in range(10)],
    'User': ['admin.john', 'hr.sarah', 'manager.mike', 'analyst.emma', 'exec.david',
             'admin.lisa', 'hr.paul', 'manager.anna', 'analyst.tom', 'exec.jane'],
    'Action': ['Config Change', 'Data Export', 'Dashboard Access', 'Report Generation', 'Executive View',
               'User Creation', 'Data Import', 'Dashboard Access', 'Analysis Run', 'Strategic Review'],
    'Resource': ['System Settings', 'Employee Data', 'Executive Dashboard', 'Talent Analytics', 'KPI Dashboard',
                 'User Management', 'HR Systems', 'Team Dashboard', 'Predictive Models', 'Future Insights'],
    'Status': ['Success', 'Success', 'Success', 'Success', 'Success',
               'Success', 'Warning', 'Success', 'Success', 'Success']
}

audit_df = pd.DataFrame(audit_data)

st.dataframe(
    audit_df.style.apply(
        lambda x: ['background-color: rgba(40, 167, 69, 0.1)' if v == 'Success' 
                  else 'background-color: rgba(255, 215, 0, 0.1)' if v == 'Warning'
                  else 'background-color: rgba(230, 0, 18, 0.1)' for v in x], 
        subset=['Status']
    ),
    use_container_width=True
)

# Admin Actions
st.markdown(create_ubisoft_section_header("🛠️ Ubisoft Administrative Actions"))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">🔄 Data Management</h4>
        <button style="background: #0099FF; color: white; border: none; padding: 10px 20px; 
                       border-radius: 5px; margin: 5px; cursor: pointer;">Force Data Sync</button><br/>
        <button style="background: #FFD700; color: black; border: none; padding: 10px 20px; 
                       border-radius: 5px; margin: 5px; cursor: pointer;">Clear Cache</button><br/>
        <button style="background: #28A745; color: white; border: none; padding: 10px 20px; 
                       border-radius: 5px; margin: 5px; cursor: pointer;">Export Logs</button>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">👥 User Actions</h4>
        <button style="background: #0099FF; color: white; border: none; padding: 10px 20px; 
                       border-radius: 5px; margin: 5px; cursor: pointer;">Add User</button><br/>
        <button style="background: #FFD700; color: black; border: none; padding: 10px 20px; 
                       border-radius: 5px; margin: 5px; cursor: pointer;">Reset Password</button><br/>
        <button style="background: #E60012; color: white; border: none; padding: 10px 20px; 
                       border-radius: 5px; margin: 5px; cursor: pointer;">Revoke Access</button>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">⚙️ System Control</h4>
        <button style="background: #28A745; color: white; border: none; padding: 10px 20px; 
                       border-radius: 5px; margin: 5px; cursor: pointer;">Restart Services</button><br/>
        <button style="background: #FFD700; color: black; border: none; padding: 10px 20px; 
                       border-radius: 5px; margin: 5px; cursor: pointer;">Maintenance Mode</button><br/>
        <button style="background: #E60012; color: white; border: none; padding: 10px 20px; 
                       border-radius: 5px; margin: 5px; cursor: pointer;">Emergency Stop</button>
    </div>
    """, unsafe_allow_html=True)

# Logout option
st.markdown("---")
if st.button("🔐 Logout from Admin Panel"):
    st.session_state.admin_authenticated = False
    st.success("✅ Successfully logged out from Ubisoft Admin Panel")
    st.rerun()

with st.sidebar:
    st.markdown("""
    ## ⚙️ Admin Panel
    
    **System Management**
    
    🔧 **System Health** monitoring real-time
    
    📊 **Data Sources** configuration
    
    👥 **User Management** access control
    
    📋 **Audit Logs** security tracking
    
    ---
    
    ### 🎮 Ubisoft Infrastructure
    - **99.8%** System uptime
    - **847** Active users
    - **8** Data sources connected
    - **15min** Refresh intervals
    
    ---
    
    ### 🔐 Security Status
    - SSL/HTTPS: ✅ Enabled
    - Authentication: ✅ Active
    - Audit Logging: ✅ Running
    - Data Encryption: ✅ AES-256
    """)
