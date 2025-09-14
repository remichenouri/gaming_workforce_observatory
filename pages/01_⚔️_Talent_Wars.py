"""
Gaming Workforce Observatory - Talent Wars Dashboard
Bataille des talents gaming vs tech avec analyse concurrentielle
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
from src.visualizations.interactive_charts import GamingInteractiveCharts

def initialize_talent_wars_dashboard():
    """Initialise le dashboard Talent Wars"""
    st.set_page_config(
        page_title="⚔️ Gaming Workforce Observatory - Talent Wars",
        page_icon="⚔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Application du thème gaming
    themes = GamingThemes()
    themes.apply_gaming_theme()

def generate_talent_wars_data():
    """Génère les données de bataille des talents"""
    
    # Comparaison secteurs gaming vs tech
    sector_comparison = pd.DataFrame({
        'sector': ['Gaming', 'Big Tech', 'Fintech', 'E-commerce', 'AI/ML', 'Crypto'],
        'avg_salary': [95000, 135000, 120000, 105000, 140000, 125000],
        'growth_rate': [0.23, 0.12, 0.18, 0.15, 0.35, 0.28],
        'job_satisfaction': [8.2, 7.1, 6.9, 7.3, 8.0, 7.5],
        'work_life_balance': [7.8, 6.2, 6.1, 6.8, 7.2, 6.9],
        'career_growth': [8.4, 7.8, 7.5, 7.2, 8.6, 7.9],
        'innovation_score': [9.1, 8.3, 7.8, 7.5, 9.3, 8.7],
        'market_competition': [0.85, 0.95, 0.78, 0.72, 0.92, 0.88]
    })
    
    # Données de talents par rôle
    role_competition = pd.DataFrame({
        'role': ['Senior Game Programmer', 'Game Designer', '3D Artist', 'QA Engineer', 
                'Technical Artist', 'Producer', 'Audio Engineer', 'UI/UX Designer'],
        'gaming_salary': [110000, 95000, 78000, 65000, 88000, 105000, 82000, 90000],
        'tech_salary': [145000, 125000, 95000, 85000, 115000, 135000, 98000, 120000],
        'gaming_demand': [95, 88, 72, 65, 78, 85, 55, 82],
        'tech_demand': [98, 75, 85, 92, 88, 95, 68, 96],
        'skills_overlap': [0.78, 0.45, 0.62, 0.85, 0.71, 0.68, 0.35, 0.89],
        'retention_gaming': [89, 91, 87, 82, 85, 88, 92, 86],
        'retention_tech': [84, 79, 81, 78, 82, 81, 85, 83]
    })
    
    # Tendances de recrutement
    recruitment_trends = pd.DataFrame({
        'month': pd.date_range('2024-01-01', periods=12, freq='M'),
        'gaming_hires': np.random.poisson(45, 12),
        'tech_poaches': np.random.poisson(12, 12),
        'gaming_to_tech': np.random.poisson(8, 12),
        'tech_to_gaming': np.random.poisson(15, 12),
        'salary_premium_needed': np.random.uniform(1.05, 1.25, 12)
    })
    
    # Analyse géographique
    geographic_competition = pd.DataFrame({
        'city': ['San Francisco', 'Seattle', 'Los Angeles', 'Austin', 'Montreal', 
                'London', 'Berlin', 'Tokyo', 'Singapore', 'Sydney'],
        'gaming_companies': [45, 28, 67, 23, 89, 34, 42, 78, 19, 25],
        'tech_companies': [234, 156, 89, 67, 34, 123, 78, 145, 89, 56],
        'talent_pool': [15000, 12000, 18000, 8500, 9500, 14000, 11000, 22000, 7500, 6800],
        'cost_of_living_index': [100, 85, 88, 72, 68, 82, 75, 91, 89, 83],
        'gaming_market_share': [0.15, 0.22, 0.28, 0.18, 0.65, 0.21, 0.28, 0.35, 0.17, 0.31]
    })
    
    # Compétences en tension
    hot_skills = pd.DataFrame({
        'skill': ['Unity', 'Unreal Engine', 'C++', 'Python', 'Machine Learning', 'Cloud Architecture',
                 'DevOps', 'Mobile Development', 'VR/AR', 'Blockchain', 'Data Science', 'Cybersecurity'],
        'gaming_demand': [95, 92, 88, 75, 68, 72, 70, 82, 89, 45, 65, 71],
        'tech_demand': [25, 15, 85, 95, 98, 96, 94, 91, 78, 88, 97, 95],
        'salary_premium': [1.15, 1.22, 1.08, 1.12, 1.35, 1.28, 1.25, 1.18, 1.45, 1.55, 1.32, 1.29],
        'scarcity_index': [0.72, 0.78, 0.65, 0.58, 0.89, 0.85, 0.82, 0.68, 0.92, 0.95, 0.88, 0.86]
    })
    
    return sector_comparison, role_competition, recruitment_trends, geographic_competition, hot_skills

def render_battle_overview(sector_comparison):
    """Vue d'ensemble de la bataille des talents"""
    
    themes = GamingThemes()
    
    # Header Talent Wars
    st.markdown("""
    <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;'>
        <h1 style='color: white; font-family: "Orbitron", monospace; font-size: 3rem; margin: 0;'>⚔️ TALENT WARS</h1>
        <h2 style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'>Gaming vs Tech Industry Battle</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 0;'>Real-time intelligence on the war for gaming talent</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Battle Stats
    st.markdown("### ⚡ Battle Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_html = themes.create_metric_card(
            "Gaming Avg Salary", 
            f"${sector_comparison.loc[0, 'avg_salary']:,}",
            "vs $135k Big Tech",
            "warning",
            "💰"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col2:
        metric_html = themes.create_metric_card(
            "Innovation Score", 
            f"{sector_comparison.loc[0, 'innovation_score']}/10",
            "#1 vs all sectors",
            "success",
            "🚀"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col3:
        metric_html = themes.create_metric_card(
            "Job Satisfaction", 
            f"{sector_comparison.loc[0, 'job_satisfaction']}/10",
            "+1.1 vs Big Tech",
            "success",
            "😊"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col4:
        metric_html = themes.create_metric_card(
            "Market Competition", 
            f"{sector_comparison.loc[0, 'market_competition']:.0%}",
            "High intensity",
            "danger",
            "🔥"
        )
        st.markdown(metric_html, unsafe_allow_html=True)

def render_sector_analysis(sector_comparison):
    """Analyse comparative des secteurs"""
    
    st.markdown("### 🎯 Sector Battlefield Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart comparaison multi-dimensionnelle
        categories = ['Salary (scaled)', 'Job Satisfaction', 'Work Life Balance', 
                     'Career Growth', 'Innovation Score']
        
        fig = go.Figure()
        
        # Gaming
        gaming_values = [
            sector_comparison.loc[0, 'avg_salary'] / 15000,  # Scaled
            sector_comparison.loc[0, 'job_satisfaction'],
            sector_comparison.loc[0, 'work_life_balance'],
            sector_comparison.loc[0, 'career_growth'],
            sector_comparison.loc[0, 'innovation_score']
        ]
        
        # Big Tech
        tech_values = [
            sector_comparison.loc[1, 'avg_salary'] / 15000,  # Scaled
            sector_comparison.loc[1, 'job_satisfaction'],
            sector_comparison.loc[1, 'work_life_balance'],
            sector_comparison.loc[1, 'career_growth'],
            sector_comparison.loc[1, 'innovation_score']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=gaming_values,
            theta=categories,
            fill='toself',
            name='Gaming Industry',
            line_color='#e74c3c',
            fillcolor='rgba(231, 76, 60, 0.3)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=tech_values,
            theta=categories,
            fill='toself',
            name='Big Tech',
            line_color='#3498db',
            fillcolor='rgba(52, 152, 219, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            title="🎪 Gaming vs Big Tech: Multi-Dimensional Comparison",
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Salary vs Satisfaction scatter
        fig_scatter = px.scatter(
            sector_comparison,
            x='avg_salary',
            y='job_satisfaction',
            size='growth_rate',
            color='innovation_score',
            hover_name='sector',
            title='💰 Salary vs Satisfaction Battle Map',
            labels={
                'avg_salary': 'Average Salary (USD)',
                'job_satisfaction': 'Job Satisfaction (1-10)',
                'growth_rate': 'Growth Rate',
                'innovation_score': 'Innovation Score'
            },
            color_continuous_scale='RdYlGn'
        )
        
        # Highlighting gaming
        fig_scatter.add_annotation(
            x=sector_comparison.loc[0, 'avg_salary'],
            y=sector_comparison.loc[0, 'job_satisfaction'],
            text="🎮 GAMING",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#e74c3c",
            font=dict(color="#e74c3c", size=14, family="Orbitron")
        )
        
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

def render_role_competition(role_competition):
    """Analyse de la compétition par rôle"""
    
    st.markdown("### 🏆 Role-by-Role Battle Analysis")
    
    # Salary gap analysis
    role_competition['salary_gap'] = role_competition['tech_salary'] - role_competition['gaming_salary']
    role_competition['salary_gap_pct'] = (role_competition['salary_gap'] / role_competition['gaming_salary']) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary comparison
        fig_salary = go.Figure()
        
        fig_salary.add_trace(go.Bar(
            name='Gaming Salary',
            x=role_competition['role'],
            y=role_competition['gaming_salary'],
            marker_color='#e74c3c'
        ))
        
        fig_salary.add_trace(go.Bar(
            name='Tech Salary',
            x=role_competition['role'],
            y=role_competition['tech_salary'],
            marker_color='#3498db'
        ))
        
        fig_salary.update_layout(
            title='💸 Salary Battle by Role',
            barmode='group',
            xaxis_tickangle=-45,
            height=400,
            yaxis_title='Annual Salary (USD)'
        )
        
        st.plotly_chart(fig_salary, use_container_width=True)
    
    with col2:
        # Demand vs Skills Overlap
        fig_demand = px.scatter(
            role_competition,
            x='skills_overlap',
            y='gaming_demand',
            size='salary_gap_pct',
            color='retention_gaming',
            hover_name='role',
            title='🎯 Talent Poaching Risk Matrix',
            labels={
                'skills_overlap': 'Skills Transferability (0-1)',
                'gaming_demand': 'Gaming Industry Demand',
                'salary_gap_pct': 'Salary Gap %',
                'retention_gaming': 'Gaming Retention %'
            },
            color_continuous_scale='RdYlGn'
        )
        
        # Risk zones
        fig_demand.add_hline(y=80, line_dash="dash", line_color="orange", 
                           annotation_text="High Demand Threshold")
        fig_demand.add_vline(x=0.7, line_dash="dash", line_color="red", 
                           annotation_text="High Transferability Risk")
        
        fig_demand.update_layout(height=400)
        st.plotly_chart(fig_demand, use_container_width=True)
    
    # Detailed role analysis table
    st.markdown("#### 📊 Detailed Role Intelligence")
    
    # Risk assessment
    def calculate_poaching_risk(row):
        risk_score = (
            (row['skills_overlap'] * 0.3) +
            (row['salary_gap_pct'] / 100 * 0.4) +
            ((row['tech_demand'] - row['gaming_demand']) / 100 * 0.3)
        )
        
        if risk_score > 0.6:
            return "🔴 CRITICAL"
        elif risk_score > 0.4:
            return "🟡 HIGH"
        elif risk_score > 0.2:
            return "🟠 MEDIUM"
        else:
            return "🟢 LOW"
    
    role_competition['poaching_risk'] = role_competition.apply(calculate_poaching_risk, axis=1)
    
    display_df = role_competition[['role', 'gaming_salary', 'tech_salary', 'salary_gap_pct', 
                                 'skills_overlap', 'poaching_risk']].copy()
    
    display_df['gaming_salary'] = display_df['gaming_salary'].apply(lambda x: f"${x:,}")
    display_df['tech_salary'] = display_df['tech_salary'].apply(lambda x: f"${x:,}")
    display_df['salary_gap_pct'] = display_df['salary_gap_pct'].apply(lambda x: f"+{x:.1f}%")
    display_df['skills_overlap'] = display_df['skills_overlap'].apply(lambda x: f"{x:.0%}")
    
    display_df.columns = ['Role', 'Gaming Salary', 'Tech Salary', 'Salary Gap', 
                         'Skills Overlap', 'Poaching Risk']
    
    st.dataframe(display_df, use_container_width=True)

def render_recruitment_battle(recruitment_trends):
    """Bataille du recrutement en temps réel"""
    
    st.markdown("### ⚔️ Recruitment Battlefield")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Flux de talents
        fig_flows = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_flows.add_trace(
            go.Scatter(
                x=recruitment_trends['month'],
                y=recruitment_trends['gaming_hires'],
                mode='lines+markers',
                name='Gaming Hires',
                line=dict(color='#27ae60', width=3),
                fill='tonexty'
            ),
            secondary_y=False
        )
        
        fig_flows.add_trace(
            go.Scatter(
                x=recruitment_trends['month'],
                y=recruitment_trends['tech_poaches'],
                mode='lines+markers',
                name='Tech Poaches Our Talent',
                line=dict(color='#e74c3c', width=3)
            ),
            secondary_y=False
        )
        
        fig_flows.add_trace(
            go.Scatter(
                x=recruitment_trends['month'],
                y=recruitment_trends['tech_to_gaming'],
                mode='lines+markers',
                name='Tech → Gaming',
                line=dict(color='#3498db', width=3, dash='dash')
            ),
            secondary_y=False
        )
        
        fig_flows.update_layout(
            title='🔄 Talent Flow Battle Trends',
            height=400
        )
        
        st.plotly_chart(fig_flows, use_container_width=True)
    
    with col2:
        # Salary premium needed
        fig_premium = px.line(
            recruitment_trends,
            x='month',
            y='salary_premium_needed',
            title='💰 Salary Premium Arms Race',
            labels={
                'salary_premium_needed': 'Premium Multiplier',
                'month': 'Month'
            }
        )
        
        fig_premium.add_hline(
            y=1.15, line_dash="dash", line_color="orange",
            annotation_text="Critical Premium Threshold"
        )
        
        fig_premium.update_traces(
            line_color='#f39c12',
            line_width=4
        )
        
        fig_premium.update_layout(height=400)
        st.plotly_chart(fig_premium, use_container_width=True)
    
    # Battle metrics
    st.markdown("#### ⚡ Real-time Battle Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_gaming_hires = recruitment_trends['gaming_hires'].sum()
    total_poached = recruitment_trends['tech_poaches'].sum()
    net_gain_from_tech = recruitment_trends['tech_to_gaming'].sum() - recruitment_trends['gaming_to_tech'].sum()
    avg_premium = recruitment_trends['salary_premium_needed'].mean()
    
    with col1:
        st.metric("Gaming Hires (YTD)", total_gaming_hires, delta=f"+{total_gaming_hires-400}")
    with col2:
        st.metric("Talent Poached by Tech", total_poached, delta_color="inverse")
    with col3:
        st.metric("Net Gain from Tech", net_gain_from_tech, delta="+12 vs last year")
    with col4:
        st.metric("Avg Salary Premium", f"{avg_premium:.1%}", delta="+3.2%")

def render_geographic_warfare(geographic_competition):
    """Guerre géographique des talents"""
    
    st.markdown("### 🌍 Geographic Talent Warfare")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gaming market share by city
        fig_geo = px.scatter(
            geographic_competition,
            x='cost_of_living_index',
            y='gaming_market_share',
            size='talent_pool',
            color='gaming_companies',
            hover_name='city',
            title='🏙️ Strategic City Analysis',
            labels={
                'cost_of_living_index': 'Cost of Living Index',
                'gaming_market_share': 'Gaming Market Share',
                'talent_pool': 'Available Talent Pool',
                'gaming_companies': 'Gaming Companies'
            },
            color_continuous_scale='Viridis'
        )
        
        fig_geo.update_layout(height=400)
        st.plotly_chart(fig_geo, use_container_width=True)
    
    with col2:
        # Competition intensity
        geographic_competition['competition_ratio'] = (
            geographic_competition['tech_companies'] / geographic_competition['gaming_companies']
        )
        
        fig_competition = px.bar(
            geographic_competition.sort_values('competition_ratio'),
            x='competition_ratio',
            y='city',
            orientation='h',
            title='⚔️ Competition Intensity by City',
            labels={'competition_ratio': 'Tech vs Gaming Companies Ratio'},
            color='competition_ratio',
            color_continuous_scale='Reds'
        )
        
        fig_competition.update_layout(height=400)
        st.plotly_chart(fig_competition, use_container_width=True)

def render_skills_warfare(hot_skills):
    """Guerre des compétences chaudes"""
    
    st.markdown("### 🔥 Hot Skills Warfare")
    
    # Skills battle matrix
    hot_skills['battle_intensity'] = (
        (hot_skills['gaming_demand'] + hot_skills['tech_demand']) / 2 * 
        hot_skills['scarcity_index']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Skills demand comparison
        skills_melted = hot_skills.melt(
            id_vars=['skill'],
            value_vars=['gaming_demand', 'tech_demand'],
            var_name='sector',
            value_name='demand'
        )
        
        fig_skills = px.bar(
            skills_melted,
            x='skill',
            y='demand',
            color='sector',
            title='🎯 Skills Demand Battle',
            barmode='group',
            color_discrete_map={
                'gaming_demand': '#e74c3c',
                'tech_demand': '#3498db'
            }
        )
        
        fig_skills.update_xaxes(tickangle=45)
        fig_skills.update_layout(height=400)
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with col2:
        # Salary premium vs scarcity
        fig_premium = px.scatter(
            hot_skills,
            x='scarcity_index',
            y='salary_premium',
            size='battle_intensity',
            color='gaming_demand',
            hover_name='skill',
            title='💎 Premium vs Scarcity Matrix',
            labels={
                'scarcity_index': 'Talent Scarcity Index',
                'salary_premium': 'Salary Premium Multiplier',
                'battle_intensity': 'Battle Intensity',
                'gaming_demand': 'Gaming Demand'
            },
            color_continuous_scale='RdYlGn'
        )
        
        fig_premium.update_layout(height=400)
        st.plotly_chart(fig_premium, use_container_width=True)
    
    # Top battle skills
    st.markdown("#### 🏅 Top Battlefield Skills")
    
    top_skills = hot_skills.sort_values('battle_intensity', ascending=False).head(6)
    
    cols = st.columns(3)
    
    for i, (_, skill) in enumerate(top_skills.iterrows()):
        col_idx = i % 3
        
        with cols[col_idx]:
            # Battle card pour chaque skill
            battle_card = f"""
            <div style='background: linear-gradient(135deg, #667eea, #764ba2); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;'>
                <h4 style='margin: 0; color: white;'>🔥 {skill['skill']}</h4>
                <p style='margin: 0.5rem 0; font-size: 0.9rem;'>
                    Gaming Demand: {skill['gaming_demand']}<br>
                    Tech Demand: {skill['tech_demand']}<br>
                    Premium: +{(skill['salary_premium']-1)*100:.0f}%<br>
                    Scarcity: {skill['scarcity_index']:.0%}
                </p>
            </div>
            """
            st.markdown(battle_card, unsafe_allow_html=True)

def render_battle_strategies():
    """Stratégies de bataille"""
    
    st.markdown("### 🛡️ Counter-Attack Strategies")
    
    strategies = [
        {
            'title': '💰 Compensation Warfare',
            'description': 'Implement dynamic salary bands that auto-adjust to market premiums',
            'tactics': [
                'Real-time market salary tracking',
                'Performance-based equity programs', 
                'Signing bonuses for critical roles',
                'Counter-offer protocol optimization'
            ],
            'impact': 'High',
            'effort': 'Medium',
            'timeline': '3-6 months'
        },
        {
            'title': '🎮 Gaming-Unique Perks',
            'description': 'Leverage unique gaming industry advantages',
            'tactics': [
                'Game development passion projects',
                'Industry conference sponsorships',
                'Creative freedom and autonomy',
                'Gaming hardware and software perks'
            ],
            'impact': 'High',
            'effort': 'Low',
            'timeline': '1-3 months'
        },
        {
            'title': '🚀 Accelerated Growth Paths',
            'description': 'Create faster career progression than tech giants',
            'tactics': [
                'Compressed promotion timelines',
                'Cross-functional project exposure',
                'Technical leadership opportunities',
                'Startup-style ownership culture'
            ],
            'impact': 'Medium',
            'effort': 'High',
            'timeline': '6-12 months'
        },
        {
            'title': '🌟 Talent Pipeline Dominance',
            'description': 'Control talent sources before tech companies',
            'tactics': [
                'University partnership programs',
                'Gaming bootcamp sponsorships',
                'Internship-to-hire pipelines',
                'Gaming community engagement'
            ],
            'impact': 'High',
            'effort': 'High',
            'timeline': '12-24 months'
        }
    ]
    
    for strategy in strategies:
        with st.expander(f"{strategy['title']} - {strategy['impact']} Impact"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {strategy['description']}")
                st.markdown("**Key Tactics:**")
                for tactic in strategy['tactics']:
                    st.markdown(f"• {tactic}")
            
            with col2:
                st.metric("Impact Level", strategy['impact'])
                st.metric("Effort Required", strategy['effort'])  
                st.metric("Timeline", strategy['timeline'])

def main():
    """Fonction principale Talent Wars"""
    
    initialize_talent_wars_dashboard()
    
    # Génération des données
    (sector_comparison, role_competition, recruitment_trends, 
     geographic_competition, hot_skills) = generate_talent_wars_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚔️ Battle Command Center")
        
        battle_sections = [
            "⚡ Battle Overview",
            "📊 Sector Analysis", 
            "🏆 Role Competition",
            "🔄 Recruitment Battle",
            "🌍 Geographic Warfare",
            "🔥 Skills Warfare",
            "🛡️ Battle Strategies"
        ]
        
        selected_section = st.selectbox(
            "Choose battlefield:",
            battle_sections,
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 🎯 Battle Intelligence")
        
        # Real-time metrics
        st.metric("Active Recruiters", "156", delta="+12")
        st.metric("Open Positions", "847", delta="+23")
        st.metric("Avg Time to Hire", "38 days", delta="-5 days")
        
        # Threat level
        st.markdown("---")
        themes = GamingThemes()
        threat_level = themes.create_status_indicator('critical', pulse=True)
        st.markdown(f"**Threat Level:** {threat_level}", unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🚨 Emergency Retention"):
            st.success("Emergency retention protocol activated!")
        
        if st.button("💰 Salary Benchmark Update"):
            st.success("Salary benchmarks updated!")
        
        if st.button("📧 Alert Leadership"):
            st.success("Leadership team alerted!")
    
    # Contenu principal
    if selected_section == "⚡ Battle Overview":
        render_battle_overview(sector_comparison)
    elif selected_section == "📊 Sector Analysis":
        render_sector_analysis(sector_comparison)
    elif selected_section == "🏆 Role Competition":
        render_role_competition(role_competition)
    elif selected_section == "🔄 Recruitment Battle":
        render_recruitment_battle(recruitment_trends)
    elif selected_section == "🌍 Geographic Warfare":
        render_geographic_warfare(geographic_competition)
    elif selected_section == "🔥 Skills Warfare":
        render_skills_warfare(hot_skills)
    elif selected_section == "🛡️ Battle Strategies":
        render_battle_strategies()
    
    # War room footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #e74c3c; font-weight: bold;'>"
        "⚔️ TALENT WARS COMMAND CENTER | CLASSIFIED | "
        f"Last Intelligence Update: {datetime.now().strftime('%H:%M:%S')}"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
