"""
🎮 Ubisoft Gaming Workforce Observatory
Compensation Intelligence - Strategic Salary Analytics
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

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

# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Ubisoft Compensation Intelligence",
    page_icon="💰",
    layout="wide"
)

apply_ubisoft_theme()

st.markdown(
    create_ubisoft_header(
        "UBISOFT Compensation Intelligence",
        "Strategic Salary Analytics & Market Positioning"
    ),
    unsafe_allow_html=True
)

st.markdown(create_ubisoft_breadcrumb("Compensation Intelligence"), unsafe_allow_html=True)

st.markdown(
    create_ubisoft_info_box(
        "💰 Ubisoft Compensation Philosophy",
        "Competitive salaries aligned with Ubisoft's commitment to attracting and retaining top gaming industry talent worldwide. Our data-driven approach ensures fair, market-competitive compensation across all studios and roles."
    ),
    unsafe_allow_html=True
)

# Compensation Overview
comp_metrics = [
    {"title": "Global Payroll", "value": "$847M", "delta": "+8.2% vs 2023", "icon": "💰"},
    {"title": "Avg Gaming Salary", "value": "$95,400", "delta": "Above market +12%", "icon": "📊"},
    {"title": "Pay Equity Score", "value": "96.7%", "delta": "Industry leading", "icon": "⚖️"},
    {"title": "Bonus Pool", "value": "$89M", "delta": "15% of base salaries", "icon": "🎯"}
]

create_ubisoft_metric_cols(comp_metrics)

# Salary by Role Analysis
st.markdown(create_ubisoft_section_header("🎮 Ubisoft Salary Analysis by Gaming Roles"))

# Gaming roles salary data
salary_data = {
    'Role': ['Senior Game Designer', 'Lead Programmer', 'Art Director', 'Technical Director',
             'Game Producer', 'Senior Animator', 'Level Designer', 'QA Lead',
             'UI/UX Designer', 'Audio Designer', 'DevOps Engineer', 'Data Scientist'],
    'Ubisoft_Min': [85000, 95000, 90000, 120000, 88000, 75000, 70000, 65000, 72000, 68000, 85000, 90000],
    'Ubisoft_Median': [105000, 125000, 115000, 150000, 110000, 95000, 88000, 80000, 90000, 85000, 110000, 115000],
    'Ubisoft_Max': [130000, 160000, 145000, 185000, 140000, 120000, 110000, 100000, 115000, 105000, 140000, 145000],
    'Market_Median': [98000, 118000, 108000, 142000, 103000, 88000, 82000, 75000, 85000, 78000, 105000, 108000],
    'Employees': [240, 450, 180, 85, 320, 380, 290, 420, 190, 120, 150, 75]
}

salary_df = pd.DataFrame(salary_data)
salary_df['Ubisoft_Premium'] = ((salary_df['Ubisoft_Median'] - salary_df['Market_Median']) / salary_df['Market_Median'] * 100).round(1)

col1, col2 = st.columns([2, 1])

with col1:
    # Salary ranges visualization
    fig_salary = go.Figure()
    
    # Add Ubisoft ranges
    for i, row in salary_df.iterrows():
        fig_salary.add_trace(go.Scatter(
            x=[row['Ubisoft_Min'], row['Ubisoft_Median'], row['Ubisoft_Max']],
            y=[row['Role']] * 3,
            mode='markers+lines',
            name=row['Role'] if i == 0 else "",
            showlegend=i == 0,
            line=dict(color=UBISOFT_COLORS['primary'], width=4),
            marker=dict(size=[8, 12, 8], color=UBISOFT_COLORS['primary'])
        ))
        
        # Add market median
        fig_salary.add_trace(go.Scatter(
            x=[row['Market_Median']],
            y=[row['Role']],
            mode='markers',
            name='Market Median' if i == 0 else "",
            showlegend=i == 0,
            marker=dict(size=10, color=UBISOFT_COLORS['accent'], symbol='diamond')
        ))
    
    fig_salary.update_layout(
        title="💰 Ubisoft Salary Ranges vs Market (USD)",
        xaxis_title="Salary (USD)",
        yaxis_title="Gaming Roles",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_salary, width='stretch')

with col2:
    # Top premium roles
    st.markdown("### 🏆 Ubisoft Premium vs Market")
    top_premium = salary_df.nlargest(6, 'Ubisoft_Premium')
    
    for _, row in top_premium.iterrows():
        premium_color = UBISOFT_COLORS['primary'] if row['Ubisoft_Premium'] > 0 else UBISOFT_COLORS['accent']
        st.markdown(f"""
        **{row['Role']}**  
        <span style="color: {premium_color}; font-weight: bold;">+{row['Ubisoft_Premium']}% vs market</span>  
        👥 {row['Employees']} employees
        """, unsafe_allow_html=True)

# Geographic Compensation Analysis
st.markdown(create_ubisoft_section_header("🌍 Ubisoft Global Compensation Analysis"))

# Geographic salary data
geo_salary_data = {
    'Studio': ['Montreal', 'Paris', 'San Francisco', 'Toronto', 'Milan', 'Shanghai', 
               'Barcelona', 'Malmö', 'Berlin', 'Kiev', 'Pune', 'Singapore'],
    'Country': ['Canada', 'France', 'USA', 'Canada', 'Italy', 'China',
                'Spain', 'Sweden', 'Germany', 'Ukraine', 'India', 'Singapore'],
    'Avg_Salary_USD': [95000, 87000, 135000, 89000, 78000, 65000, 72000, 92000, 85000, 45000, 35000, 98000],
    'Cost_of_Living': [75, 85, 95, 72, 78, 60, 70, 80, 82, 45, 35, 88],
    'Adjusted_Salary': [95000*75/75, 87000*75/85, 135000*75/95, 89000*75/72, 78000*75/78, 65000*75/60,
                       72000*75/70, 92000*75/80, 85000*75/82, 45000*75/45, 35000*75/35, 98000*75/88],
    'Employees': [3200, 2800, 650, 850, 1200, 980, 400, 250, 330, 320, 220, 180]
}

geo_df = pd.DataFrame(geo_salary_data)

col1, col2 = st.columns(2)

with col1:
    fig_geo_salary = px.scatter(
        geo_df,
        x='Avg_Salary_USD',
        y='Cost_of_Living',
        size='Employees',
        color='Adjusted_Salary',
        hover_name='Studio',
        title='🌍 Ubisoft: Salary vs Cost of Living by Studio',
        labels={
            'Avg_Salary_USD': 'Average Salary (USD)',
            'Cost_of_Living': 'Cost of Living Index',
            'Adjusted_Salary': 'Cost-Adjusted Salary'
        },
        color_continuous_scale=['#E60012', '#FFD700', '#0099FF']
    )
    
    fig_geo_salary.update_layout(get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_geo_salary, width='stretch')

with col2:
    # Best value studios
    geo_df['Value_Score'] = (geo_df['Adjusted_Salary'] / geo_df['Avg_Salary_USD'] * 100).round(1)
    best_value = geo_df.nlargest(6, 'Value_Score')
    
    st.markdown("### 💡 Best Value Ubisoft Studios")
    for _, studio in best_value.iterrows():
        st.markdown(f"""
        **{studio['Studio']}** ({studio['Country']})  
        💰 ${studio['Avg_Salary_USD']:,} • 📈 Value: {studio['Value_Score']}%  
        👥 {studio['Employees']:,} employees
        """)

# Compensation Trends
st.markdown(create_ubisoft_section_header("📈 Ubisoft Compensation Trends & Predictions"))

# Generate trend data
years = list(range(2020, 2026))
trend_data = {
    'Year': years,
    'Avg_Salary': [78000, 82000, 87000, 92000, 95400, 99500],  # 2025-2026 projected
    'Gaming_Market': [75000, 79000, 83000, 87500, 91200, 95000],
    'Tech_Industry': [85000, 90000, 95000, 102000, 108000, 113000],
    'Bonus_Pool_M': [45, 52, 61, 74, 89, 98]
}

trend_df = pd.DataFrame(trend_data)

col1, col2 = st.columns(2)

with col1:
    fig_trends = go.Figure()
    
    fig_trends.add_trace(go.Scatter(
        x=trend_df['Year'],
        y=trend_df['Avg_Salary'],
        mode='lines+markers',
        name='Ubisoft Average',
        line=dict(color=UBISOFT_COLORS['primary'], width=3)
    ))
    
    fig_trends.add_trace(go.Scatter(
        x=trend_df['Year'],
        y=trend_df['Gaming_Market'],
        mode='lines+markers',
        name='Gaming Market',
        line=dict(color='#FFD700', width=2)
    ))
    
    fig_trends.add_trace(go.Scatter(
        x=trend_df['Year'],
        y=trend_df['Tech_Industry'],
        mode='lines+markers',
        name='Tech Industry',
        line=dict(color=UBISOFT_COLORS['accent'], width=2)
    ))
    
    fig_trends.update_layout(
        title="📊 Ubisoft Salary Trends vs Market (2020-2026)",
        **get_ubisoft_chart_config()['layout']
    )
    
    st.plotly_chart(fig_trends, width='stretch')

with col2:
    fig_bonus = px.bar(
        trend_df,
        x='Year',
        y='Bonus_Pool_M',
        title='🎯 Ubisoft Bonus Pool Evolution ($M)',
        color='Bonus_Pool_M',
        color_continuous_scale=['#0066CC', '#0099FF', '#E60012']
    )
    
    fig_bonus.update_layout(get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_bonus, width='stretch')

# Pay Equity Analysis
st.markdown(create_ubisoft_section_header("⚖️ Ubisoft Pay Equity & Fairness Analysis"))

# Pay equity data
equity_data = {
    'Category': ['Gender Pay Gap', 'Ethnicity Pay Gap', 'Experience Level Gap', 'Geographic Disparity'],
    'Ubisoft_Score': [98.2, 96.8, 94.5, 91.3],
    'Industry_Average': [89.5, 85.2, 88.7, 82.1],
    'Target': [98.0, 95.0, 95.0, 90.0]
}

equity_df = pd.DataFrame(equity_data)

fig_equity = go.Figure()

fig_equity.add_trace(go.Bar(
    name='Ubisoft Score',
    x=equity_df['Category'],
    y=equity_df['Ubisoft_Score'],
    marker_color=UBISOFT_COLORS['primary']
))

fig_equity.add_trace(go.Bar(
    name='Industry Average',
    x=equity_df['Category'],
    y=equity_df['Industry_Average'],
    marker_color='rgba(100, 100, 100, 0.6)'
))

fig_equity.add_trace(go.Scatter(
    name='Ubisoft Target',
    x=equity_df['Category'],
    y=equity_df['Target'],
    mode='markers',
    marker=dict(color=UBISOFT_COLORS['accent'], size=12, symbol='diamond')
))

fig_equity.update_layout(
    title="⚖️ Ubisoft Pay Equity Excellence vs Industry",
    barmode='group',
    **get_ubisoft_chart_config()['layout']
)

st.plotly_chart(fig_equity, width='stretch')

# Recommendations
st.markdown(create_ubisoft_section_header("💡 Ubisoft Compensation Strategy Recommendations"))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">🎯 Market Positioning</h4>
        <ul style="color: #F5F5F5; text-align: left;">
            <li>Maintain +12% premium for key roles</li>
            <li>Expand equity compensation program</li>
            <li>Review SF & Toronto salary bands</li>
            <li>Benchmark emerging markets quarterly</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">⚖️ Pay Equity</h4>
        <ul style="color: #F5F5F5; text-align: left;">
            <li>Close geographic disparity gaps</li>
            <li>Enhance transparency programs</li>
            <li>Implement bias-free salary tools</li>
            <li>Quarterly equity audits</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="ubisoft-ultra-card">
        <h4 style="color: #0099FF;">🚀 Future Strategy</h4>
        <ul style="color: #F5F5F5; text-align: left;">
            <li>Skills-based compensation model</li>
            <li>Performance bonus optimization</li>
            <li>Global mobility salary framework</li>
            <li>AI-powered salary recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(display_ubisoft_logo_section(), unsafe_allow_html=True)

# Sidebar CORRIGÉ avec datetime
last = datetime.now().strftime('%Y-%m-%d %H:%M')

with st.sidebar:
    st.markdown(f"""
    ## 💰 Compensation Intel
    
    **Strategic Salary Analytics**
    
    📊 **Market Benchmarking** analysis temps réel
    
    🌍 **Global** compensation insights
    
    ⚖️ **Pay Equity** monitoring system
    
    🎯 **Strategic** recommendations
    
    ---
    
    ### 💡 Key Insights
    - **+12%** above gaming market average  
    - **96.7%** pay equity score
    - **$95,400** global average salary
    - **15%** bonus as % of base
    
    ---
    
    ### 🎮 Top Paying Roles
    1. Technical Director - $150K
    2. Lead Programmer - $125K  
    3. Art Director - $115K
    4. Data Scientist - $115K
    5. Game Producer - $110K
    
    ---
    
    **🔄 Last Updated:** {last}
    """)
