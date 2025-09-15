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
    subtitle_html = f"<p style='font-size:1.2rem; color:#555; margin-top:0.5rem;'>{subtitle}</p>" if subtitle else ""
    return f"""
    <div style='background: linear-gradient(90deg, #FFB020, #FFC533); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='font-family: Arial, sans-serif; font-weight: bold; font-size: 3.5rem; color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{title}</h1>
        {subtitle_html}
    </div>
    """

def create_ubisoft_section_header(title):
    return f"<h2 style='color: #2C3E50; font-family: Arial, sans-serif; font-weight: bold; border-left: 4px solid #FFB020; padding-left: 1rem; margin: 2rem 0 1rem 0;'>{title}</h2>"

def create_ubisoft_info_box(title, content):
    return f"""
    <div style='background: #f8f9fa; border-left: 4px solid #FFB020; padding: 1.5rem; margin: 1rem 0; border-radius: 5px;'>
        <h4 style='color: #2C3E50; margin: 0 0 0.5rem 0;'>{title}</h4>
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
    page_title="Ubisoft Compensation Intelligence",
    page_icon="💰",
    layout="wide"
)

# SIDEBAR ÉPURÉE - MENU SEULEMENT
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #FFB020; font-family: Arial, sans-serif; margin: 0;'>💰 Ubisoft</h2>
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
        if name == "Compensation Intel":
            st.markdown(f"""
            <div style='background: #FFB020; color: white; padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0;'>
                <strong>{icon} {name}</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='padding: 0.75rem; border-radius: 5px; margin: 0.25rem 0; color: #555;'>
                {icon} {name}
            </div>
            """, unsafe_allow_html=True)

# HEADER PRINCIPAL PROFESSIONNEL
last_updated = datetime.now().strftime('%Y-%m-%d %H:%M')
st.markdown(f"""
<div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; border-left: 4px solid #FFB020;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <strong style='color: #2C3E50;'>💰 Compensation Intelligence - Strategic Salary Analytics</strong>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Market Benchmarking • Global Compensation • Pay Equity • $847M Global Payroll</p>
        </div>
        <div style='text-align: right;'>
            <p style='margin: 0; color: #666; font-size: 0.9rem;'>Last Updated</p>
            <strong style='color: #FFB020;'>{last_updated}</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL AVEC MISE EN VALEUR
st.markdown(create_ubisoft_header("Compensation Intelligence", "Strategic Salary Analytics & Market Positioning"), unsafe_allow_html=True)

# INTRODUCTION AVEC CONTEXTE BUSINESS
st.markdown(create_ubisoft_info_box(
    "💰 Ubisoft Compensation Philosophy",
    "Competitive salaries aligned with Ubisoft's commitment to attracting and retaining top gaming industry talent worldwide. Our data-driven approach ensures fair, market-competitive compensation across all studios and roles with a +12% premium above gaming market average and industry-leading 96.7% pay equity score."
), unsafe_allow_html=True)

# MÉTRIQUES CLÉS AVEC STYLE PROFESSIONNEL
st.markdown(create_ubisoft_section_header("🎯 Key Compensation Metrics"), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #FFB020; margin-bottom: 0.5rem;'>💰</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>$847M</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Global Payroll</p>
        <small style='color: #28A745;'>+8.2% vs 2023</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #FFB020; margin-bottom: 0.5rem;'>📊</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>$95,400</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Avg Gaming Salary</p>
        <small style='color: #28A745;'>Above market +12%</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #FFB020; margin-bottom: 0.5rem;'>⚖️</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>96.7%</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Pay Equity Score</p>
        <small style='color: #28A745;'>Industry leading</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; color: #FFB020; margin-bottom: 0.5rem;'>🎯</div>
        <h3 style='color: #2C3E50; margin: 0; font-size: 2rem;'>$89M</h3>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Bonus Pool</p>
        <small style='color: #666;'>15% of base salaries</small>
    </div>
    """, unsafe_allow_html=True)

# SALARY BY ROLE ANALYSIS
st.markdown(create_ubisoft_section_header("🎮 Salary Analysis by Gaming Roles"), unsafe_allow_html=True)

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
        <div style='background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 5px; border-left: 4px solid {premium_color};'>
            <strong style='color: #2C3E50;'>{row['Role']}</strong><br>
            <span style='color: {premium_color}; font-weight: bold;'>+{row['Ubisoft_Premium']}% vs market</span><br>
            <span style='color: #666; font-size: 0.9rem;'>👥 {row['Employees']} employees</span>
        </div>
        """, unsafe_allow_html=True)

# GEOGRAPHIC COMPENSATION ANALYSIS
st.markdown(create_ubisoft_section_header("🌍 Global Compensation Analysis"), unsafe_allow_html=True)

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
    
    fig_geo_salary.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_geo_salary, width='stretch')

with col2:
    # Best value studios
    geo_df['Value_Score'] = (geo_df['Adjusted_Salary'] / geo_df['Avg_Salary_USD'] * 100).round(1)
    best_value = geo_df.nlargest(6, 'Value_Score')
    
    st.markdown("### 💡 Best Value Ubisoft Studios")
    for _, studio in best_value.iterrows():
        st.markdown(f"""
        <div style='background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 5px; border-left: 4px solid #28A745;'>
            <strong style='color: #2C3E50;'>{studio['Studio']}</strong> ({studio['Country']})<br>
            <span style='color: #666; font-size: 0.9rem;'>💰 ${studio['Avg_Salary_USD']:,} • 📈 Value: {studio['Value_Score']}%</span><br>
            <span style='color: #666; font-size: 0.9rem;'>👥 {studio['Employees']:,} employees</span>
        </div>
        """, unsafe_allow_html=True)

# COMPENSATION TRENDS
st.markdown(create_ubisoft_section_header("📈 Compensation Trends & Predictions"), unsafe_allow_html=True)

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
    
    fig_bonus.update_layout(**get_ubisoft_chart_config()['layout'])
    st.plotly_chart(fig_bonus, width='stretch')

# PAY EQUITY ANALYSIS
st.markdown(create_ubisoft_section_header("⚖️ Pay Equity & Fairness Analysis"), unsafe_allow_html=True)

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

# RECOMMENDATIONS AVEC STYLE AMÉLIORÉ
st.markdown(create_ubisoft_section_header("💡 Compensation Strategy Recommendations"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0099FF, #00CCFF); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🎯</div>
        <h4 style='color: white; margin: 0;'>Market Positioning</h4>
        <div style='margin: 1rem 0; text-align: left;'>
            <strong>• Maintain +12%</strong> premium for key roles<br>
            <strong>• Expand equity</strong> compensation program<br>
            <strong>• Review SF & Toronto</strong> salary bands<br>
            <strong>• Benchmark emerging</strong> markets quarterly
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #28A745, #34CE57); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>⚖️</div>
        <h4 style='color: white; margin: 0;'>Pay Equity</h4>
        <div style='margin: 1rem 0; text-align: left;'>
            <strong>• Close geographic</strong> disparity gaps<br>
            <strong>• Enhance transparency</strong> programs<br>
            <strong>• Implement bias-free</strong> salary tools<br>
            <strong>• Quarterly equity</strong> audits
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #E60012, #FF1744); padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🚀</div>
        <h4 style='color: white; margin: 0;'>Future Strategy</h4>
        <div style='margin: 1rem 0; text-align: left;'>
            <strong>• Skills-based</strong> compensation model<br>
            <strong>• Performance bonus</strong> optimization<br>
            <strong>• Global mobility</strong> salary framework<br>
            <strong>• AI-powered salary</strong> recommendations
        </div>
    </div>
    """, unsafe_allow_html=True)

# FOOTER PROFESSIONNEL
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 5px; margin-top: 2rem;'>
    <p style='color: #666; margin: 0; font-size: 0.9rem;'>
        © 2024 Ubisoft Entertainment - Gaming Workforce Observatory<br>
        Compensation Intelligence Dashboard • Strategic Salary Analytics • Confidential and Proprietary Information
    </p>
</div>
""", unsafe_allow_html=True)
