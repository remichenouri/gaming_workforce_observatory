"""
Gaming Workforce Observatory - Compensation Intelligence Dashboard
Intelligence compensation avancée avec benchmarking marché gaming
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Ajout du chemin pour imports
sys.path.append(str(Path(__file__).parent.parent))

from src.themes.gaming_themes import GamingThemes

def initialize_compensation_dashboard():
    """Initialise le dashboard compensation intelligence"""
    st.set_page_config(
        page_title="💰 Gaming Workforce Observatory - Compensation Intel",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Application du thème gaming
    themes = GamingThemes()
    themes.apply_gaming_theme()

def generate_compensation_data():
    """Génère les données de compensation gaming"""
    
    np.random.seed(42)
    
    # Données de compensation par rôle et expérience
    roles = ['Game Programmer', 'Senior Game Programmer', 'Lead Game Programmer', 
             'Game Designer', 'Senior Game Designer', 'Lead Game Designer',
             '3D Artist', 'Senior 3D Artist', 'Art Director',
             'QA Tester', 'QA Lead', 'QA Manager',
             'Producer', 'Senior Producer', 'Executive Producer']
    
    # Salaires de base par rôle (USD)
    base_salaries = {
        'Game Programmer': 85000, 'Senior Game Programmer': 120000, 'Lead Game Programmer': 155000,
        'Game Designer': 78000, 'Senior Game Designer': 115000, 'Lead Game Designer': 145000,
        '3D Artist': 65000, 'Senior 3D Artist': 95000, 'Art Director': 125000,
        'QA Tester': 50000, 'QA Lead': 75000, 'QA Manager': 95000,
        'Producer': 90000, 'Senior Producer': 125000, 'Executive Producer': 180000
    }
    
    # Génération des données de compensation détaillées
    compensation_data = []
    
    for role in roles:
        for _ in range(np.random.randint(15, 35)):
            base_salary = base_salaries[role]
            
            # Variations selon l'expérience et la performance
            experience_years = np.random.exponential(3) + 1
            if 'Senior' in role:
                experience_years += 3
            elif 'Lead' in role or 'Director' in role:
                experience_years += 6
            
            experience_years = min(experience_years, 20)
            
            # Facteurs d'ajustement
            performance_multiplier = np.random.normal(1.0, 0.15)
            location_multiplier = np.random.choice([0.85, 1.0, 1.25, 1.45], p=[0.3, 0.4, 0.25, 0.05])
            company_size_multiplier = np.random.choice([0.9, 1.0, 1.15, 1.3], p=[0.2, 0.4, 0.3, 0.1])
            
            total_comp = base_salary * performance_multiplier * location_multiplier * company_size_multiplier
            total_comp = max(total_comp, base_salary * 0.7)  # Plancher
            
            # Répartition de la compensation
            base_percentage = np.random.uniform(0.65, 0.85)
            bonus_percentage = np.random.uniform(0.10, 0.25)
            equity_percentage = 1 - base_percentage - bonus_percentage
            
            compensation_data.append({
                'role': role,
                'years_experience': round(experience_years, 1),
                'total_compensation': round(total_comp),
                'base_salary': round(total_comp * base_percentage),
                'bonus': round(total_comp * bonus_percentage),
                'equity_value': round(total_comp * equity_percentage),
                'location_tier': np.random.choice(['Tier 1', 'Tier 2', 'Tier 3'], p=[0.3, 0.5, 0.2]),
                'company_size': np.random.choice(['Startup', 'Mid-size', 'Large', 'AAA'], p=[0.2, 0.3, 0.3, 0.2]),
                'department': role.split()[0] if role.split()[0] in ['Game', '3D', 'QA'] else 
                            'Programming' if 'Programmer' in role else
                            'Design' if 'Designer' in role else
                            'Art' if 'Artist' in role or 'Art' in role else
                            'QA' if 'QA' in role else 'Production',
                'performance_rating': np.random.choice(['Below', 'Meets', 'Exceeds', 'Outstanding'], 
                                                     p=[0.1, 0.5, 0.3, 0.1]),
                'remote_work': np.random.choice([True, False], p=[0.4, 0.6])
            })
    
    comp_df = pd.DataFrame(compensation_data)
    
    # Données de benchmarking marché
    market_data = pd.DataFrame({
        'role': list(base_salaries.keys()),
        'market_p25': [salary * 0.85 for salary in base_salaries.values()],
        'market_p50': [salary * 1.0 for salary in base_salaries.values()],
        'market_p75': [salary * 1.2 for salary in base_salaries.values()],
        'market_p90': [salary * 1.4 for salary in base_salaries.values()],
        'growth_1_year': np.random.uniform(0.03, 0.12, len(base_salaries)),
        'growth_3_year': np.random.uniform(0.15, 0.35, len(base_salaries)),
        'demand_score': np.random.uniform(60, 95, len(base_salaries)),
        'competition_level': np.random.choice(['Low', 'Medium', 'High', 'Very High'], len(base_salaries))
    })
    
    # Analyse d'équité salariale
    equity_analysis = comp_df.groupby(['role', 'performance_rating']).agg({
        'total_compensation': ['mean', 'std', 'count'],
        'years_experience': 'mean'
    }).round(0)
    
    # Pay gaps analysis (simulé)
    pay_gaps = {
        'gender_gap': {
            'overall': 0.078,  # 7.8% gap
            'by_role': {
                'Programming': 0.085,
                'Design': 0.062,
                'Art': 0.045,
                'QA': 0.033,
                'Production': 0.091
            }
        },
        'experience_premium': {
            '0-2_years': 1.0,
            '3-5_years': 1.23,
            '6-10_years': 1.55,
            '11+_years': 1.89
        },
        'location_premium': {
            'Tier 1': 1.45,
            'Tier 2': 1.0,
            'Tier 3': 0.85
        }
    }
    
    # Projections futures
    compensation_projections = {
        'next_year': {
            'salary_inflation': 0.076,
            'bonus_growth': 0.045,
            'equity_growth': 0.12,
            'high_demand_roles': ['Senior Game Programmer', 'Lead Game Designer', 'Art Director']
        },
        'next_3_years': {
            'salary_inflation': 0.235,
            'market_premium_shift': 0.18,
            'emerging_roles': ['ML Engineer', 'VR Specialist', 'Blockchain Developer'],
            'declining_roles': ['QA Tester']  # Automation impact
        }
    }
    
    return comp_df, market_data, equity_analysis, pay_gaps, compensation_projections

def render_compensation_overview(comp_df, market_data):
    """Vue d'ensemble de la compensation"""
    
    themes = GamingThemes()
    
    # Header Compensation Intelligence
    st.markdown("""
    <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;'>
        <h1 style='color: white; font-family: "Orbitron", monospace; font-size: 3rem; margin: 0;'>💰 COMPENSATION INTEL</h1>
        <h2 style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'>Strategic Gaming Workforce Compensation Intelligence</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 0;'>Data-driven insights for competitive compensation strategies</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métriques clés de compensation
    st.markdown("### 💎 Key Compensation Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    avg_total_comp = comp_df['total_compensation'].mean()
    median_base_salary = comp_df['base_salary'].median()
    bonus_percentage = (comp_df['bonus'].sum() / comp_df['total_compensation'].sum()) * 100
    equity_percentage = (comp_df['equity_value'].sum() / comp_df['total_compensation'].sum()) * 100
    
    with col1:
        metric_html = themes.create_metric_card(
            "Avg Total Comp", 
            f"${avg_total_comp:,.0f}",
            "All roles included",
            "success",
            "💰"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col2:
        metric_html = themes.create_metric_card(
            "Median Base Salary", 
            f"${median_base_salary:,.0f}",
            f"+{np.random.uniform(3.5, 8.2):.1f}% YoY",
            "info",
            "📊"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col3:
        metric_html = themes.create_metric_card(
            "Bonus Component", 
            f"{bonus_percentage:.1f}%",
            "Of total compensation",
            "warning",
            "🎯"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col4:
        metric_html = themes.create_metric_card(
            "Equity Component", 
            f"{equity_percentage:.1f}%",
            "Long-term incentives",
            "info",
            "📈"
        )
        st.markdown(metric_html, unsafe_allow_html=True)

def render_salary_benchmarking(comp_df, market_data):
    """Benchmarking salarial détaillé"""
    
    st.markdown("### 📊 Market Salary Benchmarking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary distribution par rôle
        role_salary_stats = comp_df.groupby('role')['total_compensation'].agg(['mean', 'median', 'std']).round(0)
        role_salary_stats = role_salary_stats.reset_index()
        role_salary_stats.columns = ['Role', 'Mean', 'Median', 'Std Dev']
        
        # Top 8 rôles par salaire moyen
        top_roles = role_salary_stats.nlargest(8, 'Mean')
        
        fig_roles = px.bar(
            top_roles,
            x='Mean',
            y='Role',
            orientation='h',
            title='💼 Top Roles by Average Total Compensation',
            color='Mean',
            color_continuous_scale='Viridis'
        )
        
        fig_roles.update_layout(height=400)
        st.plotly_chart(fig_roles, use_container_width=True)
    
    with col2:
        # Compensation vs Experience
        fig_exp = px.scatter(
            comp_df.sample(200),  # Sample pour performance
            x='years_experience',
            y='total_compensation',
            color='department',
            size='bonus',
            hover_data=['role', 'company_size'],
            title='⭐ Compensation vs Experience',
            labels={
                'years_experience': 'Years of Experience',
                'total_compensation': 'Total Compensation (USD)'
            }
        )
        
        fig_exp.update_layout(height=400)
        st.plotly_chart(fig_exp, use_container_width=True)
    
    # Market positioning analysis
    st.markdown("#### 🎯 Our Position vs Market")
    
    # Merge notre data avec market data
    our_averages = comp_df.groupby('role')['total_compensation'].mean().reset_index()
    our_averages.columns = ['role', 'our_average']
    
    market_comparison = market_data.merge(our_averages, on='role', how='left')
    market_comparison['vs_market_p50'] = ((market_comparison['our_average'] - market_comparison['market_p50']) / 
                                         market_comparison['market_p50'] * 100).round(1)
    
    # Graphique de positioning
    fig_positioning = px.scatter(
        market_comparison,
        x='market_p50',
        y='our_average',
        size='demand_score',
        color='vs_market_p50',
        hover_name='role',
        title='🎪 Our Compensation vs Market P50',
        labels={
            'market_p50': 'Market P50 (USD)',
            'our_average': 'Our Average (USD)',
            'vs_market_p50': '% vs Market'
        },
        color_continuous_scale='RdBu',
        color_continuous_midpoint=0
    )
    
    # Ligne de parité
    min_val = min(market_comparison['market_p50'].min(), market_comparison['our_average'].min())
    max_val = max(market_comparison['market_p50'].max(), market_comparison['our_average'].max())
    fig_positioning.add_shape(
        type="line",
        x0=min_val, y0=min_val,
        x1=max_val, y1=max_val,
        line=dict(color="gray", width=2, dash="dash")
    )
    
    st.plotly_chart(fig_positioning, use_container_width=True)

def render_equity_analysis(comp_df, pay_gaps):
    """Analyse d'équité salariale"""
    
    st.markdown("### ⚖️ Pay Equity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pay gaps par département
        dept_gaps = pay_gaps['gender_gap']['by_role']
        gap_df = pd.DataFrame(list(dept_gaps.items()), columns=['Department', 'Gender_Gap_Pct'])
        gap_df['Gender_Gap_Pct'] = gap_df['Gender_Gap_Pct'] * 100
        
        fig_gaps = px.bar(
            gap_df,
            x='Department',
            y='Gender_Gap_Pct',
            title='👥 Gender Pay Gap by Department',
            color='Gender_Gap_Pct',
            color_continuous_scale='Reds'
        )
        
        fig_gaps.add_hline(y=0, line_dash="dash", line_color="green", annotation_text="Pay Parity")
        fig_gaps.update_layout(height=400)
        st.plotly_chart(fig_gaps, use_container_width=True)
    
    with col2:
        # Experience premium analysis
        exp_premium = pay_gaps['experience_premium']
        exp_df = pd.DataFrame(list(exp_premium.items()), columns=['Experience_Band', 'Premium_Multiplier'])
        
        fig_exp_premium = px.bar(
            exp_df,
            x='Experience_Band',
            y='Premium_Multiplier',
            title='📈 Experience Premium Analysis',
            color='Premium_Multiplier',
            color_continuous_scale='Blues'
        )
        
        fig_exp_premium.update_layout(height=400)
        st.plotly_chart(fig_exp_premium, use_container_width=True)
    
    # Equity recommendations
    st.markdown("#### 💡 Pay Equity Recommendations")
    
    recommendations = [
        {
            'priority': 'High',
            'issue': 'Production Department Gap',
            'description': f"9.1% gender pay gap in Production - highest across departments",
            'action': 'Conduct detailed pay audit and implement correction plan',
            'timeline': 'Q1 2025',
            'investment': '$125K'
        },
        {
            'priority': 'Medium',
            'issue': 'Programming Compensation Range',
            'description': f"Programming shows 8.5% gap with high variance",
            'action': 'Standardize level definitions and salary bands',
            'timeline': 'Q2 2025',
            'investment': '$80K'
        },
        {
            'priority': 'Low',
            'issue': 'Location Premium Consistency',
            'description': f"45% premium for Tier 1 locations needs validation",
            'action': 'Review cost-of-living adjustments quarterly',
            'timeline': 'Ongoing',
            'investment': '$25K'
        }
    ]
    
    for rec in recommendations:
        priority_colors = {'High': '#e74c3c', 'Medium': '#f39c12', 'Low': '#3498db'}
        color = priority_colors[rec['priority']]
        
        with st.expander(f"🎯 {rec['issue']} - {rec['priority']} Priority"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Issue:** {rec['description']}")
                st.markdown(f"**Recommended Action:** {rec['action']}")
                st.markdown(f"**Timeline:** {rec['timeline']}")
            
            with col2:
                st.metric("Investment Required", rec['investment'])

def render_compensation_planning(compensation_projections):
    """Planification de compensation future"""
    
    st.markdown("### 🔮 Compensation Planning & Projections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Projections 1 an
        st.markdown("#### 📅 Next Year Projections")
        
        next_year = compensation_projections['next_year']
        
        projections_1y = [
            ("Salary Inflation", f"{next_year['salary_inflation']:.1%}", "Market-driven increase"),
            ("Bonus Growth", f"{next_year['bonus_growth']:.1%}", "Performance-linked"),
            ("Equity Growth", f"{next_year['equity_growth']:.1%}", "Retention-focused"),
        ]
        
        for metric, value, description in projections_1y:
            col_a, col_b, col_c = st.columns([2, 1, 2])
            with col_a:
                st.markdown(f"**{metric}:**")
            with col_b:
                st.markdown(f"**{value}**")
            with col_c:
                st.markdown(f"*{description}*")
        
        st.markdown("**High Demand Roles (Premium Expected):**")
        for role in next_year['high_demand_roles']:
            st.markdown(f"• {role}")
    
    with col2:
        # Projections 3 ans
        st.markdown("#### 🚀 3-Year Strategic Outlook")
        
        three_year = compensation_projections['next_3_years']
        
        projections_3y = [
            ("Cumulative Salary Growth", f"{three_year['salary_inflation']:.1%}", "Inflation + market"),
            ("Market Premium Shift", f"{three_year['market_premium_shift']:.1%}", "Competition increase"),
        ]
        
        for metric, value, description in projections_3y:
            col_a, col_b, col_c = st.columns([2, 1, 2])
            with col_a:
                st.markdown(f"**{metric}:**")
            with col_b:
                st.markdown(f"**{value}**")
            with col_c:
                st.markdown(f"*{description}*")
        
        st.markdown("**Emerging Roles:**")
        for role in three_year['emerging_roles']:
            st.markdown(f"• {role}")
        
        st.markdown("**Roles at Risk:**")
        for role in three_year['declining_roles']:
            st.markdown(f"• {role} (automation impact)")
    
    # Budget impact calculator
    st.markdown("#### 💰 Budget Impact Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_payroll = st.number_input("Current Annual Payroll ($M)", value=125.5, step=0.1)
        employee_count = st.number_input("Employee Count", value=1200, step=10)
        
    with col2:
        salary_increase = st.slider("Planned Salary Increase (%)", 0.0, 15.0, 7.6, 0.1)
        headcount_growth = st.slider("Headcount Growth (%)", 0.0, 25.0, 8.0, 0.5)
        
    with col3:
        # Calculs automatiques
        new_payroll = current_payroll * (1 + salary_increase/100) * (1 + headcount_growth/100)
        budget_increase = new_payroll - current_payroll
        cost_per_employee = (budget_increase * 1000000) / (employee_count * (1 + headcount_growth/100))
        
        st.metric("New Annual Payroll", f"${new_payroll:.1f}M", f"+${budget_increase:.1f}M")
        st.metric("Budget Increase", f"{((new_payroll/current_payroll - 1)*100):.1f}%")
        st.metric("Cost/Employee Impact", f"${cost_per_employee:,.0f}")

def render_competitive_intelligence():
    """Intelligence compétitive marché"""
    
    st.markdown("### 🕵️ Competitive Intelligence")
    
    # Données des compétiteurs (simulées)
    competitors = pd.DataFrame({
        'company': ['Ubisoft', 'EA Games', 'Activision', 'Epic Games', 'Riot Games', 'Unity', 'Our Company'],
        'avg_programmer_salary': [125000, 135000, 130000, 140000, 145000, 120000, 118000],
        'avg_designer_salary': [105000, 115000, 110000, 125000, 130000, 100000, 108000],
        'avg_artist_salary': [85000, 95000, 90000, 100000, 105000, 82000, 87000],
        'bonus_percentage': [15, 18, 20, 25, 22, 12, 16],
        'equity_offering': [True, True, True, True, True, False, True],
        'remote_work_policy': ['Hybrid', 'Flexible', 'Office', 'Remote-First', 'Hybrid', 'Office', 'Hybrid'],
        'glassdoor_rating': [3.8, 3.2, 3.1, 4.2, 4.5, 3.9, 3.7],
        'market_position': ['Established', 'Established', 'Established', 'Growth', 'Growth', 'Established', 'Growth']
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Competitive salary positioning
        salary_cols = ['avg_programmer_salary', 'avg_designer_salary', 'avg_artist_salary']
        
        fig_comp = go.Figure()
        
        for _, company in competitors.iterrows():
            fig_comp.add_trace(go.Scatterpolar(
                r=[company[col]/1000 for col in salary_cols],  # Convert to K
                theta=['Programmers', 'Designers', 'Artists'],
                fill='toself',
                name=company['company'],
                opacity=0.7 if company['company'] != 'Our Company' else 1.0,
                line=dict(width=3 if company['company'] == 'Our Company' else 1)
            ))
        
        fig_comp.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 150]
                )
            ),
            title='💰 Competitive Salary Positioning (K USD)',
            height=400
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
    
    with col2:
        # Company attractiveness matrix
        fig_matrix = px.scatter(
            competitors,
            x='bonus_percentage',
            y='glassdoor_rating',
            size='avg_programmer_salary',
            color='market_position',
            hover_name='company',
            title='🎯 Company Attractiveness Matrix',
            labels={
                'bonus_percentage': 'Bonus Percentage',
                'glassdoor_rating': 'Glassdoor Rating'
            }
        )
        
        # Highlight our company
        our_company = competitors[competitors['company'] == 'Our Company']
        fig_matrix.add_annotation(
            x=our_company['bonus_percentage'].iloc[0],
            y=our_company['glassdoor_rating'].iloc[0],
            text="👈 US",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#e74c3c",
            font=dict(size=14, color="#e74c3c")
        )
        
        fig_matrix.update_layout(height=400)
        st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Competitive insights
    st.markdown("#### 🎪 Key Competitive Insights")
    
    insights = [
        "**Riot Games** leads in both programmer salaries ($145K) and bonus percentages (22%)",
        "**Epic Games** offers highest designer compensation ($125K) with strong Glassdoor ratings (4.2)",
        "We rank **5th/7** in programmer salaries - opportunity for improvement",
        "Our bonus percentage (16%) is **below industry median** (18%)",
        "**Remote-first policies** becoming competitive advantage (Epic Games example)"
    ]
    
    for insight in insights:
        st.markdown(f"• {insight}")

def render_compensation_recommendations():
    """Recommandations stratégiques de compensation"""
    
    st.markdown("### 🎯 Strategic Compensation Recommendations")
    
    # Recommandations par catégorie
    recommendations = {
        'Immediate Actions (Q1 2025)': [
            {
                'title': 'Senior Programmer Salary Adjustment',
                'description': 'Increase senior programmer salaries by 8% to match market P75',
                'investment': '$2.4M annually',
                'impact': 'Retain 95% of senior technical talent',
                'risk': 'High attrition risk if not addressed'
            },
            {
                'title': 'Performance Bonus Restructure',
                'description': 'Increase bonus target from 16% to 20% for all roles',
                'investment': '$1.8M annually',
                'impact': 'Improved motivation and retention',
                'risk': 'Budget overrun if performance exceeds targets'
            }
        ],
        'Medium-term (2025)': [
            {
                'title': 'Equity Program Enhancement',
                'description': 'Implement RSU program for all employees above mid-level',
                'investment': '$5.2M in equity grants',
                'impact': 'Long-term retention and alignment',
                'risk': 'Dilution concerns from shareholders'
            },
            {
                'title': 'Location Premium Review',
                'description': 'Adjust location premiums based on updated cost-of-living data',
                'investment': '$800K annually',
                'impact': 'Improved fairness and talent access',
                'risk': 'Some employee dissatisfaction with changes'
            }
        ],
        'Strategic (2025-2027)': [
            {
                'title': 'AI/ML Talent Premium Strategy',
                'description': 'Create specialized compensation bands for AI/ML engineers',
                'investment': '$3.5M annually by 2027',
                'impact': 'Access to cutting-edge talent',
                'risk': 'Internal equity concerns'
            },
            {
                'title': 'Total Rewards Program',
                'description': 'Comprehensive benefits overhaul including learning stipends, wellness',
                'investment': '$2.1M setup + $4.2M annually',
                'impact': 'Holistic employee value proposition',
                'risk': 'Complex administration'
            }
        ]
    }
    
    for timeframe, recs in recommendations.items():
        st.markdown(f"#### {timeframe}")
        
        for rec in recs:
            with st.expander(f"💡 {rec['title']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Description:** {rec['description']}")
                    st.markdown(f"**Expected Impact:** {rec['impact']}")
                    st.markdown(f"**Risk Consideration:** {rec['risk']}")
                
                with col2:
                    st.metric("Investment", rec['investment'])
    
    # ROI Calculator pour recommandations
    st.markdown("#### 📊 Recommendation ROI Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Input Assumptions**")
        current_attrition_rate = st.slider("Current Attrition Rate (%)", 5.0, 25.0, 12.5)
        cost_to_replace = st.number_input("Cost to Replace Employee ($)", value=85000, step=1000)
        
    with col2:
        st.markdown("**Projected Improvements**")
        attrition_reduction = st.slider("Attrition Reduction (%)", 1.0, 10.0, 3.5)
        productivity_gain = st.slider("Productivity Gain (%)", 1.0, 15.0, 5.0)
        
    with col3:
        st.markdown("**ROI Calculation**")
        
        # Calculs
        current_attrition_cost = (current_attrition_rate/100) * 1200 * cost_to_replace  # 1200 employees
        new_attrition_cost = ((current_attrition_rate - attrition_reduction)/100) * 1200 * cost_to_replace
        attrition_savings = current_attrition_cost - new_attrition_cost
        
        productivity_value = 1200 * 95000 * (productivity_gain/100)  # Avg salary * productivity gain
        
        total_benefits = attrition_savings + productivity_value
        total_investment = 8.4e6  # Total from recommendations
        
        roi = ((total_benefits - total_investment) / total_investment) * 100
        
        st.metric("Annual Benefits", f"${total_benefits/1e6:.1f}M")
        st.metric("Annual Investment", f"${total_investment/1e6:.1f}M") 
        st.metric("ROI", f"{roi:.1f}%")

def main():
    """Fonction principale Compensation Intelligence"""
    
    initialize_compensation_dashboard()
    
    # Génération des données
    comp_df, market_data, equity_analysis, pay_gaps, compensation_projections = generate_compensation_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 💰 Compensation Hub")
        
        comp_sections = [
            "💎 Compensation Overview",
            "📊 Salary Benchmarking", 
            "⚖️ Pay Equity Analysis",
            "🔮 Compensation Planning",
            "🕵️ Competitive Intelligence",
            "🎯 Strategic Recommendations"
        ]
        
        selected_section = st.selectbox(
            "Select compensation module:",
            comp_sections,
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        
        # Statistiques rapides
        total_payroll = (comp_df['total_compensation'].sum() / 1e6)
        avg_comp_growth = np.random.uniform(5.8, 8.4)
        market_position = "P65"  # Notre position vs marché
        
        st.metric("Total Payroll", f"${total_payroll:.1f}M")
        st.metric("YoY Growth", f"{avg_comp_growth:.1f}%")
        st.metric("Market Position", market_position)
        
        # Alertes compensation
        st.markdown("---")
        st.markdown("### ⚠️ Compensation Alerts")
        
        themes = GamingThemes()
        
        alert_html = themes.create_status_indicator('warning')
        st.markdown(f"**Programming Gap:** {alert_html}", unsafe_allow_html=True)
        
        alert_html = themes.create_status_indicator('critical')
        st.markdown(f"**Senior Retention:** {alert_html}", unsafe_allow_html=True)
        
        alert_html = themes.create_status_indicator('online')
        st.markdown(f"**Budget Status:** {alert_html}", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("📊 Generate Comp Report"):
            st.success("Compensation analysis report generated!")
        
        if st.button("💰 Budget Planning"):
            st.success("Budget planning initiated!")
        
        if st.button("📧 Share with Executives"):
            st.success("Compensation insights shared!")
    
    # Contenu principal
    if selected_section == "💎 Compensation Overview":
        render_compensation_overview(comp_df, market_data)
    elif selected_section == "📊 Salary Benchmarking":
        render_salary_benchmarking(comp_df, market_data)
    elif selected_section == "⚖️ Pay Equity Analysis":
        render_equity_analysis(comp_df, pay_gaps)
    elif selected_section == "🔮 Compensation Planning":
        render_compensation_planning(compensation_projections)
    elif selected_section == "🕵️ Competitive Intelligence":
        render_competitive_intelligence()
    elif selected_section == "🎯 Strategic Recommendations":
        render_compensation_recommendations()
    
    # Footer compensation
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #f39c12; font-weight: bold;'>"
        "💰 STRATEGIC COMPENSATION INTELLIGENCE | "
        f"Market Data Updated: {datetime.now().strftime('%Y-%m-%d')} | "
        "Confidential Compensation Analysis"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
