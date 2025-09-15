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
    subtitle_html = f"<p style='font-size:1.2rem; color:#555; margin-top:0.5rem;'>{subtitle}</p>" if subtitle else ""
    return f"""
    <div style='background: linear-gradient(90deg, #E60012, #FF4444); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='font-family: Arial, sans-serif; font-weight: bold; font-size: 3.5rem; color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{title}</h1>
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title):
    return f"<h2 style='color: #2C3E50; font-family: Arial, sans-serif; font-weight: bold; border-left: 4px solid #E60012; padding-left: 1rem; margin: 2rem 0 1rem 0;'>{title}</h2>"

def create_ubisoft_info_box(title, content):
    return f"""
    <div style='background: #f8f9fa; border-left: 4px solid #E60012; padding: 1.5rem; margin: 1rem 0; border-radius: 5px;'>
        <h4 style='color: #2C3E50; margin: 0 0 0.5rem 0;'>{title}</h4>
        <p style='color: #555; margin: 0; font-size: 1rem; line-height: 1.5;'>{content}</p>
    </div>
    """

def create_ubisoft_accent_box(title, content):
    return f"""
    <div style='background: linear-gradient(135deg, #E6001215, #fff); border-left: 4px solid #E60012; padding: 1.5rem; margin: 1rem 0; border-radius: 5px;'>
        <h4 style='color: #E60012; margin: 0 0 0.5rem 0;'>{title}</h4>
        <p style='color: #555; margin: 0; font-size: 1rem; line-height: 1.5;'>{content}</p>
    </div>
    """

def get_ubisoft_chart_config():
    return {
        'layout': {
            'font': {'family': 'Arial, sans-serif', 'size': 12, 'color': '#2C3E50'},
            'paper_bgcolor': 'white',
            'plot_bgcolor': '#fafafa'
        }
    }

# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Ubisoft Admin Panel - System Management",
    page_icon="⚙️",
    layout="wide"
)

# SIDEBAR ÉPURÉE - MENU SEULEMENT
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #E60012; font-family: Arial, sans-serif; margin: 0;'>⚙️ Ubisoft</h2>
        <p style='color: #666; font-size: 0.9rem; margin: 0.5rem 0;'>Workforce Observatory</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu de navigation épuré
    menu_items = [
        ("🏠", "Executive Dashboard"),
        ("⚔️", "Talent Wars"), 
        ("🧠", "Neurodiversity ROI"),
        ("🎯", "Predictive Analytics"),
        ("🌍", "Global Studios"),
        ("💰", "Compensation Intel"),
        ("🚀", "Future Insights"),
        ("⚙️", "Admin Panel")
    ]
    
    st.markdown("<h4 style='color: #2C3E50; margin-bottom: 1rem;'>Navigation</h4>", unsafe_allow_html=True)
    
    for icon, name in menu_items:
        if name == "Admin Panel":
            st.markdown(f"""
            <div style='background: #E60012; color: white; padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0;'>
                <strong>{icon} {name}</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0; color: #555;'>
                {icon} {name}
            </div>
            """, unsafe_allow_html=True)

# Check for admin access (in real implementation, this would be proper authentication)
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    # HEADER D'AUTHENTIFICATION
    st.markdown(create_ubisoft_header("Admin Panel", "System Management & Configuration Controls"), unsafe_allow_html=True)
    
    st.markdown(create_ubisoft_accent_box(
        "🔐 Ubisoft Admin Access Required",
        "Please authenticate to access the Ubisoft Gaming Workforce Observatory administrative controls. This secure area is restricted to authorized IT and HR administrators only."
    ), unsafe_allow_html=True)
    
    with st.form("admin_login"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                <h3 style='text-align: center; color: #E60012; margin-bottom: 2rem;'>🎮 Ubisoft Admin Authentication</h3>
            """, unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="ubisoft.admin")
            password = st.text_input("Password", type="password", placeholder="Enter admin password")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.form_submit_button("🔓 Access Admin Panel", type="primary", use_container_width=True):
                # Simple demo authentication (in reality, use proper auth)
                if username == "ubisoft.admin" and password == "demo123":
                    st.session_state.admin_authenticated = True
                    st.success("✅ Authentication successful! Welcome to Ubisoft Admin Panel.")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please contact Ubisoft IT support.")
    
    st.stop()

# HEADER PRINCIPAL PROFESSIONNEL (après authentification)
last_updated = datetime.now().strftime('%Y-%m-%d %H:%M')
st.markdown(f"""
<div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; border-left: 4px solid #E60012;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: #2C3E50;'>⚙️ Admin Panel - System Management</strong>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>System Health • Data Sources • User Management • Security Controls</p>
        </div>
        <div style='text-align: right;'>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Last Updated</p>
            <strong style='color: #E60012;'>{last_updated}</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL AVEC MISE EN VALEUR
st.markdown(create_ubisoft_header("Admin Panel", "System Management & Configuration Controls"), unsafe_allow_html=True)

# INTRODUCTION ADMIN
st.markdown(create_ubisoft_info_box(
    "⚙️ Ubisoft Gaming Workforce Observatory",
    "Administrative controls for Ubisoft HR and IT teams. Monitor system health (99.8% uptime), manage data sources (8 connected), configure dashboards, and oversee user access (847 active users) across all Ubisoft studios worldwide with enterprise-grade security."
), unsafe_allow_html=True)

# SYSTEM HEALTH DASHBOARD
st.markdown(create_ubisoft_section_header("🔧 System Health Monitor"), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #28A745; margin-bottom: 0.5rem;'>✅</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>99.8%</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>System Uptime</p>
        <small style='color: #28A745;'>Excellent</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #0099FF; margin-bottom: 0.5rem;'>⚡</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>1.2s</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Avg Response</p>
        <small style='color: #28A745;'>Fast</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #FFD700; margin-bottom: 0.5rem;'>👥</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>847</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Active Users</p>
        <small style='color: #666;'>Online now</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #E60012; margin-bottom: 0.5rem;'>🔄</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>15min</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Data Refresh</p>
        <small style='color: #666;'>Auto sync</small>
    </div>
    """, unsafe_allow_html=True)

# DATA SOURCES MANAGEMENT
st.markdown(create_ubisoft_section_header("📊 Data Sources Management"), unsafe_allow_html=True)

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
    # Create status indicators with improved styling
    status_colors = {'Active': '#28A745', 'Warning': '#FFD700', 'Maintenance': '#E60012'}
    
    for _, source in sources_df.iterrows():
        status_color = status_colors.get(source['Status'], '#CCCCCC')
        st.markdown(f"""
        <div style='background: white; border-left: 4px solid {status_color}; padding: 1.5rem; margin: 1rem 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <strong style='color: #2C3E50;'>{source['Source']}</strong>
                    <div style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>
                        📊 {source['Records']:,} records • Last sync: {source['Last_Sync']}
                    </div>
                </div>
                <div style='text-align: right;'>
                    <span style='color: {status_color}; font-weight: bold;'>{source['Status']}</span>
                    <div style='color: #0099FF; font-size: 0.9rem; margin-top: 0.5rem;'>Health: {source['Health_Score']}%</div>
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
        title="🔍 Data Sources Status",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_status, width='stretch')

# USER MANAGEMENT
st.markdown(create_ubisoft_section_header("👥 User Access Management"), unsafe_allow_html=True)

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
        title='👥 Active Users by Role',
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_users.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_users, width='stretch')

with col2:
    # User activity with improved styling
    st.markdown("### 📊 User Activity Summary")
    for _, user in users_df.iterrows():
        activity_rate = (user['Last_7_Days'] / user['Active_Users'] * 100) if user['Active_Users'] > 0 else 0
        activity_color = '#28A745' if activity_rate > 80 else '#FFD700' if activity_rate > 60 else '#E60012'
        
        st.markdown(f"""
        <div style='background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 5px; border-left: 4px solid {activity_color};'>
            <strong style='color: #2C3E50;'>{user['Role']}</strong><br>
            <span style='color: #666; font-size: 0.9rem;'>👥 {user['Active_Users']} active • 🔄 {user['Last_7_Days']} weekly</span><br>
            <span style='color: {activity_color}; font-weight: bold;'>📈 {activity_rate:.1f}% engagement</span><br>
            <span style='color: #666; font-size: 0.9rem;'>⏱️ Avg session: {user['Avg_Session']}</span>
        </div>
        """, unsafe_allow_html=True)

# SYSTEM CONFIGURATION
st.markdown(create_ubisoft_section_header("⚙️ System Configuration"), unsafe_allow_html=True)

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

# AUDIT LOGS
st.markdown(create_ubisoft_section_header("📋 System Audit Logs"), unsafe_allow_html=True)

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
    width='stretch'
)

# ADMIN ACTIONS AVEC STYLE AMÉLIORÉ
st.markdown(create_ubisoft_section_header("🛠️ Administrative Actions"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0099FF, #00CCFF); padding: 2rem; border-radius: 10px; text-align: center; color: white; margin-bottom: 1rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🔄</div>
        <h4 style='color: white; margin: 0;'>Data Management</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Force Data Sync", use_container_width=True):
        st.success("✅ Data sync initiated!")
    if st.button("🗑️ Clear Cache", use_container_width=True):
        st.success("✅ Cache cleared!")
    if st.button("📤 Export Logs", use_container_width=True):
        st.success("✅ Logs exported!")

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFB020, #FFC533); padding: 2rem; border-radius: 10px; text-align: center; color: white; margin-bottom: 1rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>👥</div>
        <h4 style='color: white; margin: 0;'>User Actions</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👥 Add User", use_container_width=True):
        st.info("🔹 User creation form would open here")
    if st.button("🔑 Reset Password", use_container_width=True):
        st.info("🔹 Password reset interface would appear")
    if st.button("🚫 Revoke Access", use_container_width=True):
        st.warning("⚠️ Access revocation requires confirmation")

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #E60012, #FF1744); padding: 2rem; border-radius: 10px; text-align: center; color: white; margin-bottom: 1rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>⚙️</div>
        <h4 style='color: white; margin: 0;'>System Control</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Restart Services", use_container_width=True):
        st.success("✅ Services restart initiated!")
    if st.button("🔧 Maintenance Mode", use_container_width=True):
        st.warning("⚠️ Maintenance mode activated")
    if st.button("🛑 Emergency Stop", use_container_width=True):
        st.error("❌ Emergency procedures activated")

# LOGOUT OPTION
st.markdown("---")
if st.button("🔐 Logout from Admin Panel", type="secondary", use_container_width=True):
    st.session_state.admin_authenticated = False
    st.success("✅ Successfully logged out from Ubisoft Admin Panel")
    st.rerun()

# FOOTER PROFESSIONNEL
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 5px; margin-top: 2rem;'>
    <p style='color: #666; margin: 0; font-size: 0.9rem;'>
        © 2024 Ubisoft Entertainment - Gaming Workforce Observatory<br>
        Admin Panel • System Management & Configuration • Confidential and Proprietary Information
    </p>
</div>
""", unsafe_allow_html=True)

