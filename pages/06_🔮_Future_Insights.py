"""
Gaming Workforce Observatory - Future Insights Dashboard
Prédictions et insights futuristes pour l'industrie gaming
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

def initialize_future_insights_dashboard():
    """Initialise le dashboard future insights"""
    st.set_page_config(
        page_title="🔮 Gaming Workforce Observatory - Future Insights",
        page_icon="🔮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Application du thème gaming
    themes = GamingThemes()
    themes.apply_gaming_theme()

def generate_future_data():
    """Génère les données futuristes de l'industrie gaming"""
    
    # Tendances technologiques émergentes
    tech_trends = pd.DataFrame({
        'technology': [
            'AI/ML in Game Development', 'Cloud Gaming', 'VR/AR Gaming', 
            'Blockchain Gaming', 'Metaverse Platforms', 'Neural Interfaces',
            'Quantum Computing', 'Procedural Generation AI', 'Real-time Ray Tracing',
            'Cross-platform Gaming', 'Edge Computing', '5G Gaming'
        ],
        'adoption_2024': [25, 15, 12, 8, 18, 2, 1, 30, 45, 75, 20, 35],
        'predicted_2027': [75, 60, 45, 35, 55, 15, 8, 80, 90, 95, 70, 85],
        'predicted_2030': [95, 85, 75, 60, 80, 40, 25, 95, 98, 99, 90, 95],
        'impact_score': [95, 85, 80, 70, 90, 60, 45, 88, 82, 92, 78, 83],
        'talent_demand': [90, 70, 75, 65, 85, 80, 95, 85, 78, 60, 72, 68],
        'investment_required': [8.5, 12.2, 15.8, 6.3, 20.5, 35.0, 50.0, 5.2, 8.9, 3.2, 12.8, 8.5]
    })
    
    # Évolution des rôles gaming
    role_evolution = pd.DataFrame({
        'role': [
            'AI Game Designer', 'Metaverse Architect', 'Blockchain Game Developer',
            'VR Experience Designer', 'Cloud Gaming Engineer', 'Neural Interface Programmer',
            'Procedural Content Creator', 'Data-Driven Game Analyst', 'Community Experience Manager',
            'Gaming Ethicist', 'Virtual Economy Designer', 'Cross-Reality Developer'
        ],
        'emergence_year': [2023, 2024, 2022, 2021, 2023, 2026, 2024, 2022, 2023, 2025, 2023, 2025],
        'demand_2027': [85, 90, 70, 75, 80, 60, 88, 82, 78, 65, 72, 85],
        'salary_projection_2027': [145000, 165000, 135000, 125000, 140000, 185000, 120000, 115000, 95000, 110000, 130000, 150000],
        'skill_rarity': [78, 85, 65, 60, 70, 95, 72, 55, 45, 80, 68, 82],
        'automation_risk': [25, 15, 35, 20, 40, 10, 45, 60, 30, 5, 25, 30]
    })
    
    # Prédictions industrie gaming
    industry_predictions = {
        '2025': {
            'global_revenue': 285.5,  # Billions USD
            'mobile_gaming_share': 0.58,
            'cloud_gaming_revenue': 8.2,
            'vr_ar_market': 15.8,
            'workforce_size': 3.8,  # Millions
            'avg_salary_growth': 0.078,
            'remote_work_adoption': 0.65
        },
        '2027': {
            'global_revenue': 365.2,
            'mobile_gaming_share': 0.62,
            'cloud_gaming_revenue': 28.5,
            'vr_ar_market': 45.2,
            'workforce_size': 4.6,
            'avg_salary_growth': 0.065,
            'remote_work_adoption': 0.75
        },
        '2030': {
            'global_revenue': 475.8,
            'mobile_gaming_share': 0.68,
            'cloud_gaming_revenue': 85.3,
            'vr_ar_market': 125.8,
            'workforce_size': 5.9,
            'avg_salary_growth': 0.055,
            'remote_work_adoption': 0.85
        }
    }
    
    # Disruptions potentielles
    disruptions = [
        {
            'name': 'Full AI-Generated Games',
            'probability': 0.35,
            'timeline': '2028-2030',
            'impact': 'High',
            'workforce_effect': 'Displacement of 30% junior developers',
            'preparation': 'Upskilling in AI tool management and creative direction'
        },
        {
            'name': 'Neural Gaming Interfaces',
            'probability': 0.25,
            'timeline': '2030-2032',
            'impact': 'Revolutionary',
            'workforce_effect': 'New specialized roles in neurogaming',
            'preparation': 'Early investment in neurotechnology expertise'
        },
        {
            'name': 'Metaverse Consolidation',
            'probability': 0.65,
            'timeline': '2025-2027',
            'impact': 'Medium',
            'workforce_effect': 'Platform specialization required',
            'preparation': 'Multi-platform development skills'
        },
        {
            'name': 'Quantum Gaming Breakthrough',
            'probability': 0.15,
            'timeline': '2032-2035',
            'impact': 'Revolutionary',
            'workforce_effect': 'Entirely new computing paradigm',
            'preparation': 'Quantum computing fundamentals'
        },
        {
            'name': 'Gaming Industry Regulation',
            'probability': 0.80,
            'timeline': '2025-2026',
            'impact': 'Medium',
            'workforce_effect': 'Increased compliance roles',
            'preparation': 'Legal and ethics training'
        }
    ]
    
    # Skills futures
    skills_future = pd.DataFrame({
        'skill': [
            'Prompt Engineering', 'Ethical AI Design', 'Quantum Programming',
            'Neural Interface Development', 'Metaverse Architecture', 'Blockchain Integration',
            'Cloud-Native Development', 'Data Privacy Engineering', 'Sustainable Gaming Design',
            'Cross-Reality UX', 'AI Model Training', 'Virtual Economy Design'
        ],
        'current_demand': [40, 25, 5, 10, 60, 45, 70, 55, 30, 35, 65, 50],
        'predicted_2027': [85, 75, 25, 45, 90, 70, 95, 85, 65, 80, 90, 85],
        'predicted_2030': [95, 90, 60, 75, 95, 85, 98, 95, 85, 95, 95, 95],
        'learning_difficulty': [6, 8, 9, 9, 7, 7, 6, 7, 5, 8, 8, 6],
        'salary_premium': [1.25, 1.35, 2.10, 1.85, 1.45, 1.30, 1.20, 1.40, 1.15, 1.55, 1.50, 1.35]
    })
    
    return tech_trends, role_evolution, industry_predictions, disruptions, skills_future

def render_future_overview(industry_predictions):
    """Vue d'ensemble des insights futurs"""
    
    themes = GamingThemes()
    
    # Header Future Insights
    st.markdown("""
    <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;'>
        <h1 style='color: white; font-family: "Orbitron", monospace; font-size: 3rem; margin: 0;'>🔮 FUTURE INSIGHTS</h1>
        <h2 style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'>Gaming Industry Crystal Ball</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 0;'>Strategic foresight for tomorrow's gaming workforce</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prédictions clés
    st.markdown("### 🌟 Key Industry Predictions")
    
    col1, col2, col3 = st.columns(3)
    
    # 2025 Predictions
    with col1:
        st.markdown("#### 🎯 2025 Horizon")
        pred_2025 = industry_predictions['2025']
        
        metrics_2025 = [
            ("Global Revenue", f"${pred_2025['global_revenue']:.1f}B"),
            ("Workforce Size", f"{pred_2025['workforce_size']:.1f}M people"),
            ("Cloud Gaming", f"${pred_2025['cloud_gaming_revenue']:.1f}B"),
            ("Remote Work", f"{pred_2025['remote_work_adoption']:.0%}"),
            ("VR/AR Market", f"${pred_2025['vr_ar_market']:.1f}B")
        ]
        
        for metric, value in metrics_2025:
            st.markdown(f"**{metric}:** {value}")
    
    # 2027 Predictions  
    with col2:
        st.markdown("#### 🚀 2027 Vision")
        pred_2027 = industry_predictions['2027']
        
        metrics_2027 = [
            ("Global Revenue", f"${pred_2027['global_revenue']:.1f}B"),
            ("Workforce Size", f"{pred_2027['workforce_size']:.1f}M people"),
            ("Cloud Gaming", f"${pred_2027['cloud_gaming_revenue']:.1f}B"),
            ("Remote Work", f"{pred_2027['remote_work_adoption']:.0%}"),
            ("VR/AR Market", f"${pred_2027['vr_ar_market']:.1f}B")
        ]
        
        for metric, value in metrics_2027:
            st.markdown(f"**{metric}:** {value}")
    
    # 2030 Predictions
    with col3:
        st.markdown("#### 🌌 2030 Transformation")
        pred_2030 = industry_predictions['2030']
        
        metrics_2030 = [
            ("Global Revenue", f"${pred_2030['global_revenue']:.1f}B"),
            ("Workforce Size", f"{pred_2030['workforce_size']:.1f}M people"),
            ("Cloud Gaming", f"${pred_2030['cloud_gaming_revenue']:.1f}B"),
            ("Remote Work", f"{pred_2030['remote_work_adoption']:.0%}"),
            ("VR/AR Market", f"${pred_2030['vr_ar_market']:.1f}B")
        ]
        
        for metric, value in metrics_2030:
            st.markdown(f"**{metric}:** {value}")
    
    # Growth trajectories
    st.markdown("### 📈 Industry Growth Trajectories")
    
    # Préparer les données pour le graphique
    years = [2024, 2025, 2027, 2030]
    
    # Extrapolation 2024 (current)
    current_estimates = {
        'global_revenue': 220.5,
        'cloud_gaming_revenue': 4.8,
        'vr_ar_market': 8.2,
        'workforce_size': 3.2
    }
    
    trajectory_data = pd.DataFrame({
        'Year': years,
        'Global_Revenue': [
            current_estimates['global_revenue'],
            industry_predictions['2025']['global_revenue'],
            industry_predictions['2027']['global_revenue'],
            industry_predictions['2030']['global_revenue']
        ],
        'Cloud_Gaming': [
            current_estimates['cloud_gaming_revenue'],
            industry_predictions['2025']['cloud_gaming_revenue'],
            industry_predictions['2027']['cloud_gaming_revenue'],
            industry_predictions['2030']['cloud_gaming_revenue']
        ],
        'VR_AR_Market': [
            current_estimates['vr_ar_market'],
            industry_predictions['2025']['vr_ar_market'],
            industry_predictions['2027']['vr_ar_market'],
            industry_predictions['2030']['vr_ar_market']
        ]
    })
    
    fig_trajectories = go.Figure()
    
    fig_trajectories.add_trace(go.Scatter(
        x=trajectory_data['Year'],
        y=trajectory_data['Global_Revenue'],
        mode='lines+markers',
        name='Global Gaming Revenue ($B)',
        line=dict(color='#3498db', width=3)
    ))
    
    fig_trajectories.add_trace(go.Scatter(
        x=trajectory_data['Year'],
        y=trajectory_data['Cloud_Gaming'],
        mode='lines+markers',
        name='Cloud Gaming Revenue ($B)',
        line=dict(color='#e74c3c', width=3),
        yaxis='y2'
    ))
    
    fig_trajectories.add_trace(go.Scatter(
        x=trajectory_data['Year'],
        y=trajectory_data['VR_AR_Market'],
        mode='lines+markers',
        name='VR/AR Market ($B)',
        line=dict(color='#2ecc71', width=3),
        yaxis='y2'
    ))
    
    fig_trajectories.update_layout(
        title='🚀 Gaming Industry Growth Trajectories',
        xaxis_title='Year',
        yaxis=dict(title='Global Revenue ($B)', side='left'),
        yaxis2=dict(title='Cloud Gaming & VR/AR ($B)', side='right', overlaying='y'),
        height=400
    )
    
    st.plotly_chart(fig_trajectories, use_container_width=True)

def render_technology_trends(tech_trends):
    """Analyse des tendances technologiques"""
    
    st.markdown("### 🔬 Emerging Technology Adoption")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Technology adoption timeline
        fig_adoption = go.Figure()
        
        fig_adoption.add_trace(go.Scatter(
            x=[2024, 2027, 2030],
            y=[tech_trends['adoption_2024'].mean(), 
               tech_trends['predicted_2027'].mean(), 
               tech_trends['predicted_2030'].mean()],
            mode='lines+markers',
            name='Average Adoption',
            line=dict(color='#3498db', width=4),
            marker=dict(size=10)
        ))
        
        # Individual technology trajectories (top 5)
        top_5_tech = tech_trends.nlargest(5, 'impact_score')
        
        for _, tech in top_5_tech.iterrows():
            fig_adoption.add_trace(go.Scatter(
                x=[2024, 2027, 2030],
                y=[tech['adoption_2024'], tech['predicted_2027'], tech['predicted_2030']],
                mode='lines+markers',
                name=tech['technology'][:15] + '...' if len(tech['technology']) > 15 else tech['technology'],
                opacity=0.7
            ))
        
        fig_adoption.update_layout(
            title='📊 Technology Adoption Timeline',
            xaxis_title='Year',
            yaxis_title='Adoption Rate (%)',
            height=400
        )
        
        st.plotly_chart(fig_adoption, use_container_width=True)
    
    with col2:
        # Impact vs Investment matrix
        fig_matrix = px.scatter(
            tech_trends,
            x='investment_required',
            y='impact_score',
            size='talent_demand',
            color='predicted_2030',
            hover_name='technology',
            title='💎 Impact vs Investment Matrix',
            labels={
                'investment_required': 'Investment Required ($B)',
                'impact_score': 'Industry Impact Score',
                'talent_demand': 'Talent Demand Score',
                'predicted_2030': '2030 Adoption %'
            },
            color_continuous_scale='Viridis'
        )
        
        fig_matrix.update_layout(height=400)
        st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Technology readiness matrix
    st.markdown("#### 🎪 Technology Readiness Assessment")
    
    # Classification des technologies
    tech_trends['readiness_category'] = tech_trends.apply(
        lambda row: 'Ready to Scale' if row['adoption_2024'] > 30 else
                   'Early Adoption' if row['adoption_2024'] > 15 else
                   'Experimental' if row['adoption_2024'] > 5 else
                   'Emerging', axis=1
    )
    
    readiness_counts = tech_trends['readiness_category'].value_counts()
    
    cols = st.columns(len(readiness_counts))
    
    categories = ['Ready to Scale', 'Early Adoption', 'Experimental', 'Emerging']
    colors = ['#27ae60', '#3498db', '#f39c12', '#e74c3c']
    
    for i, category in enumerate(categories):
        if category in readiness_counts.index:
            with cols[i]:
                count = readiness_counts[category]
                techs = tech_trends[tech_trends['readiness_category'] == category]['technology'].tolist()
                
                category_card = f"""
                <div style='background: {colors[i]}; padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;'>
                    <h4 style='margin: 0; color: white;'>{category}</h4>
                    <p style='margin: 0.5rem 0; font-size: 1.2rem; font-weight: bold;'>{count} Technologies</p>
                    <div style='font-size: 0.8rem;'>
                        {', '.join(techs[:2])}{'...' if len(techs) > 2 else ''}
                    </div>
                </div>
                """
                st.markdown(category_card, unsafe_allow_html=True)

def render_role_evolution(role_evolution):
    """Évolution des rôles gaming"""
    
    st.markdown("### 👨‍💻 Future Gaming Roles Evolution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary projections for new roles
        fig_salary = px.bar(
            role_evolution.sort_values('salary_projection_2027', ascending=True),
            x='salary_projection_2027',
            y='role',
            orientation='h',
            title='💰 2027 Salary Projections for Emerging Roles',
            color='skill_rarity',
            color_continuous_scale='Plasma'
        )
        
        fig_salary.update_layout(height=500)
        st.plotly_chart(fig_salary, use_container_width=True)
    
    with col2:
        # Demand vs Automation Risk
        fig_risk = px.scatter(
            role_evolution,
            x='automation_risk',
            y='demand_2027',
            size='salary_projection_2027',
            color='skill_rarity',
            hover_name='role',
            title='🤖 Demand vs Automation Risk',
            labels={
                'automation_risk': 'Automation Risk (%)',
                'demand_2027': 'Market Demand 2027',
                'skill_rarity': 'Skill Rarity Score'
            },
            color_continuous_scale='RdYlGn_r'
        )
        
        # Risk quadrants
        fig_risk.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="High Demand Threshold")
        fig_risk.add_vline(x=40, line_dash="dash", line_color="red", annotation_text="High Automation Risk")
        
        fig_risk.update_layout(height=500)
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Role categories analysis
    st.markdown("#### 🎯 Strategic Role Categories")
    
    # Catégorisation des rôles
    role_evolution['strategic_priority'] = role_evolution.apply(
        lambda row: 'Critical Investment' if row['demand_2027'] > 80 and row['automation_risk'] < 30 else
                   'High Potential' if row['demand_2027'] > 70 and row['skill_rarity'] > 70 else
                   'Monitor & Develop' if row['demand_2027'] > 60 else
                   'Evaluate', axis=1
    )
    
    priority_groups = role_evolution.groupby('strategic_priority')
    
    for priority, group in priority_groups:
        priority_colors = {
            'Critical Investment': '#e74c3c',
            'High Potential': '#f39c12',
            'Monitor & Develop': '#3498db',
            'Evaluate': '#95a5a6'
        }
        
        color = priority_colors.get(priority, '#95a5a6')
        
        with st.expander(f"🎪 {priority} ({len(group)} roles)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Roles in this category:**")
                for _, role in group.iterrows():
                    st.markdown(f"• {role['role']}")
            
            with col2:
                avg_salary = group['salary_projection_2027'].mean()
                avg_demand = group['demand_2027'].mean()
                avg_rarity = group['skill_rarity'].mean()
                
                st.metric("Avg 2027 Salary", f"${avg_salary:,.0f}")
                st.metric("Avg Market Demand", f"{avg_demand:.0f}/100")
                st.metric("Avg Skill Rarity", f"{avg_rarity:.0f}/100")

def render_disruption_scenarios(disruptions):
    """Scénarios de disruption"""
    
    st.markdown("### ⚡ Industry Disruption Scenarios")
    
    # Analyse de probabilité et impact
    disruption_df = pd.DataFrame(disruptions)
    
    # Matrice probabilité vs impact
    impact_mapping = {'Low': 25, 'Medium': 50, 'High': 75, 'Revolutionary': 100}
    disruption_df['impact_numeric'] = disruption_df['impact'].map(impact_mapping)
    disruption_df['probability_numeric'] = disruption_df['probability'] * 100
    
    fig_disruption = px.scatter(
        disruption_df,
        x='probability_numeric',
        y='impact_numeric',
        size=[50] * len(disruption_df),  # Taille uniforme
        hover_name='name',
        title='🌪️ Disruption Probability vs Impact Matrix',
        labels={
            'probability_numeric': 'Probability (%)',
            'impact_numeric': 'Industry Impact Score'
        }
    )
    
    # Quadrants
    fig_disruption.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Medium Impact")
    fig_disruption.add_vline(x=50, line_dash="dash", line_color="gray", annotation_text="50% Probability")
    
    # Annotations pour chaque point
    for _, disruption in disruption_df.iterrows():
        fig_disruption.add_annotation(
            x=disruption['probability_numeric'],
            y=disruption['impact_numeric'],
            text=disruption['name'][:15] + '...' if len(disruption['name']) > 15 else disruption['name'],
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="rgba(0,0,0,0.5)",
            font=dict(size=10)
        )
    
    fig_disruption.update_layout(height=500)
    st.plotly_chart(fig_disruption, use_container_width=True)
    
    # Détail des scénarios de disruption
    st.markdown("#### 🎪 Disruption Scenario Deep Dive")
    
    # Tri par probabilité décroissante
    sorted_disruptions = sorted(disruptions, key=lambda x: x['probability'], reverse=True)
    
    for disruption in sorted_disruptions:
        prob_color = '#e74c3c' if disruption['probability'] > 0.6 else '#f39c12' if disruption['probability'] > 0.3 else '#3498db'
        
        with st.expander(f"⚡ {disruption['name']} - {disruption['probability']:.0%} probability"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Timeline:** {disruption['timeline']}")
                st.markdown(f"**Workforce Effect:** {disruption['workforce_effect']}")
                st.markdown(f"**Preparation Strategy:** {disruption['preparation']}")
            
            with col2:
                st.metric("Probability", f"{disruption['probability']:.0%}")
                st.metric("Impact Level", disruption['impact'])

def render_skills_future(skills_future):
    """Futur des compétences gaming"""
    
    st.markdown("### 🎪 Future Skills Landscape")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Skills demand evolution
        fig_skills_evolution = go.Figure()
        
        # Top 6 skills par demande future
        top_skills = skills_future.nlargest(6, 'predicted_2030')
        
        years = ['Current (2024)', '2027', '2030']
        
        for _, skill in top_skills.iterrows():
            fig_skills_evolution.add_trace(go.Scatter(
                x=years,
                y=[skill['current_demand'], skill['predicted_2027'], skill['predicted_2030']],
                mode='lines+markers',
                name=skill['skill'][:20] + '...' if len(skill['skill']) > 20 else skill['skill']
            ))
        
        fig_skills_evolution.update_layout(
            title='📈 Skills Demand Evolution',
            xaxis_title='Timeline',
            yaxis_title='Demand Score (0-100)',
            height=400
        )
        
        st.plotly_chart(fig_skills_evolution, use_container_width=True)
    
    with col2:
        # Learning difficulty vs salary premium
        fig_learning = px.scatter(
            skills_future,
            x='learning_difficulty',
            y='salary_premium',
            size='predicted_2030',
            color='current_demand',
            hover_name='skill',
            title='🎓 Learning Difficulty vs Salary Premium',
            labels={
                'learning_difficulty': 'Learning Difficulty (1-10)',
                'salary_premium': 'Salary Premium Multiplier',
                'predicted_2030': '2030 Demand',
                'current_demand': 'Current Demand'
            },
            color_continuous_scale='Viridis'
        )
        
        fig_learning.update_layout(height=400)
        st.plotly_chart(fig_learning, use_container_width=True)
    
    # Skills investment priorities
    st.markdown("#### 🎯 Skills Investment Priorities")
    
    # Calcul du score d'investissement
    skills_future['investment_score'] = (
        (skills_future['predicted_2030'] - skills_future['current_demand']) * 0.4 +  # Growth potential
        skills_future['salary_premium'] * 20 +  # Financial return
        (10 - skills_future['learning_difficulty']) * 5  # Ease of learning
    ).round(1)
    
    top_investments = skills_future.nlargest(8, 'investment_score')
    
    # Affichage en cartes
    cols = st.columns(4)
    
    for i, (_, skill) in enumerate(top_investments.iterrows()):
        col_idx = i % 4
        
        with cols[col_idx]:
            growth = skill['predicted_2030'] - skill['current_demand']
            
            skill_card = f"""
            <div style='background: linear-gradient(135deg, #667eea, #764ba2); 
                        padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0; height: 180px;'>
                <h4 style='margin: 0; color: white; font-size: 0.9rem;'>{skill['skill']}</h4>
                <div style='margin: 0.5rem 0; font-size: 0.8rem;'>
                    <strong>Growth:</strong> +{growth:.0f} points<br>
                    <strong>Premium:</strong> {skill['salary_premium']:.1f}x<br>
                    <strong>Difficulty:</strong> {skill['learning_difficulty']:.0f}/10<br>
                    <strong>Score:</strong> {skill['investment_score']:.1f}
                </div>
            </div>
            """
            st.markdown(skill_card, unsafe_allow_html=True)

def render_strategic_recommendations():
    """Recommandations stratégiques futuristes"""
    
    st.markdown("### 🚀 Strategic Future-Proofing Recommendations")
    
    # Recommandations par horizon temporel
    recommendations = {
        'Immediate (2025)': [
            {
                'title': 'AI/ML Upskilling Program',
                'description': 'Launch comprehensive AI integration training for all developers',
                'investment': '$2.5M',
                'roi_timeframe': '12-18 months',
                'risk_mitigation': 'Prevents skill obsolescence in 75% of programming roles'
            },
            {
                'title': 'Cloud Gaming Infrastructure',
                'description': 'Begin transition to cloud-native game development practices',
                'investment': '$5.8M',
                'roi_timeframe': '18-24 months',
                'risk_mitigation': 'Positions for 60% growth in cloud gaming market'
            },
            {
                'title': 'Metaverse Competency Center',
                'description': 'Establish dedicated metaverse development team',
                'investment': '$3.2M',
                'roi_timeframe': '24-36 months',
                'risk_mitigation': 'Captures early-mover advantage in $55B market by 2027'
            }
        ],
        'Medium-term (2025-2027)': [
            {
                'title': 'Neural Interface R&D Lab',
                'description': 'Invest in neural gaming interface research and talent',
                'investment': '$8.5M',
                'roi_timeframe': '3-5 years',
                'risk_mitigation': 'Prepares for revolutionary 2030+ gaming paradigm'
            },
            {
                'title': 'Quantum Computing Partnership',
                'description': 'Partner with quantum computing companies for future algorithms',
                'investment': '$4.2M',
                'roi_timeframe': '5-7 years',
                'risk_mitigation': 'Early access to game-changing computing power'
            },
            {
                'title': 'Ethical AI Framework',
                'description': 'Develop comprehensive ethical AI guidelines for game development',
                'investment': '$1.8M',
                'roi_timeframe': '2-3 years',
                'risk_mitigation': 'Prevents regulatory issues and builds trust'
            }
        ],
        'Long-term (2027-2030)': [
            {
                'title': 'Cross-Reality Platform',
                'description': 'Build unified platform spanning AR/VR/traditional gaming',
                'investment': '$15.5M',
                'roi_timeframe': '5-8 years',
                'risk_mitigation': 'Dominates convergent gaming experience market'
            },
            {
                'title': 'AI Game Generation Suite',
                'description': 'Develop AI tools that can generate complete game experiences',
                'investment': '$22.0M',
                'roi_timeframe': '7-10 years',
                'risk_mitigation': 'Transforms industry cost structure and speed'
            }
        ]
    }
    
    for timeframe, recs in recommendations.items():
        st.markdown(f"#### {timeframe}")
        
        for rec in recs:
            with st.expander(f"🎯 {rec['title']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Strategy:** {rec['description']}")
                    st.markdown(f"**Risk Mitigation:** {rec['risk_mitigation']}")
                    st.markdown(f"**ROI Timeframe:** {rec['roi_timeframe']}")
                
                with col2:
                    st.metric("Investment", rec['investment'])
    
    # Future readiness scorecard
    st.markdown("#### 📊 Future Readiness Scorecard")
    
    readiness_categories = {
        'AI/ML Integration': {'score': 68, 'target': 85, 'gap': -17},
        'Cloud Gaming': {'score': 45, 'target': 80, 'gap': -35},
        'VR/AR Capabilities': {'score': 52, 'target': 75, 'gap': -23},
        'Metaverse Readiness': {'score': 38, 'target': 70, 'gap': -32},
        'Blockchain Gaming': {'score': 28, 'target': 60, 'gap': -32},
        'Neural Interfaces': {'score': 5, 'target': 40, 'gap': -35}
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scorecard radar
        categories = list(readiness_categories.keys())
        scores = [readiness_categories[cat]['score'] for cat in categories]
        targets = [readiness_categories[cat]['target'] for cat in categories]
        
        fig_scorecard = go.Figure()
        
        fig_scorecard.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Current Readiness',
            line_color='#3498db'
        ))
        
        fig_scorecard.add_trace(go.Scatterpolar(
            r=targets,
            theta=categories,
            fill='toself',
            name='Target Readiness',
            line_color='#e74c3c',
            opacity=0.6
        ))
        
        fig_scorecard.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title='🎪 Future Readiness Assessment',
            height=400
        )
        
        st.plotly_chart(fig_scorecard, use_container_width=True)
    
    with col2:
        st.markdown("**Readiness Gap Analysis:**")
        
        for category, data in readiness_categories.items():
            gap_percentage = abs(data['gap'])
            
            if gap_percentage > 30:
                status = "🔴 Critical Gap"
                color = "#e74c3c"
            elif gap_percentage > 20:
                status = "🟡 Significant Gap"
                color = "#f39c12"
            elif gap_percentage > 10:
                status = "🟠 Moderate Gap"
                color = "#e67e22"
            else:
                status = "🟢 On Track"
                color = "#27ae60"
            
            st.markdown(f"**{category}:** {status}")
            st.markdown(f"Current: {data['score']}% | Target: {data['target']}% | Gap: {data['gap']}")
            st.markdown("---")

def main():
    """Fonction principale Future Insights"""
    
    initialize_future_insights_dashboard()
    
    # Génération des données
    tech_trends, role_evolution, industry_predictions, disruptions, skills_future = generate_future_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔮 Future Intelligence")
        
        future_sections = [
            "🌟 Future Overview",
            "🔬 Technology Trends",
            "👨‍💻 Role Evolution", 
            "⚡ Disruption Scenarios",
            "🎪 Skills Future",
            "🚀 Strategic Recommendations"
        ]
        
        selected_section = st.selectbox(
            "Explore future insights:",
            future_sections,
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📊 Future Metrics")
        
        # Métriques futures
        themes = GamingThemes()
        
        # Probabilité de disruption moyenne
        avg_disruption_prob = np.mean([d['probability'] for d in disruptions]) * 100
        
        st.metric("Industry Growth", "+115% by 2030")
        st.metric("Workforce Growth", "+84% by 2030")
        st.metric("Disruption Risk", f"{avg_disruption_prob:.0f}%")
        
        # Indicateurs de préparation
        st.markdown("---")
        st.markdown("### 🎯 Readiness Status")
        
        ai_status = themes.create_status_indicator('warning')
        st.markdown(f"**AI Readiness:** {ai_status}", unsafe_allow_html=True)
        
        cloud_status = themes.create_status_indicator('critical')
        st.markdown(f"**Cloud Gaming:** {cloud_status}", unsafe_allow_html=True)
        
        metaverse_status = themes.create_status_indicator('warning')
        st.markdown(f"**Metaverse:** {metaverse_status}", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔮 Future Strategy Report"):
            st.success("Future strategy report generated!")
        
        if st.button("🎯 Readiness Assessment"):
            st.success("Comprehensive readiness assessment initiated!")
        
        if st.button("📧 Share Vision"):
            st.success("Future vision shared with leadership!")
    
    # Contenu principal
    if selected_section == "🌟 Future Overview":
        render_future_overview(industry_predictions)
    elif selected_section == "🔬 Technology Trends":
        render_technology_trends(tech_trends)
    elif selected_section == "👨‍💻 Role Evolution":
        render_role_evolution(role_evolution)
    elif selected_section == "⚡ Disruption Scenarios":
        render_disruption_scenarios(disruptions)
    elif selected_section == "🎪 Skills Future":
        render_skills_future(skills_future)
    elif selected_section == "🚀 Strategic Recommendations":
        render_strategic_recommendations()
    
    # Footer futuriste
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #667eea; font-weight: bold;'>"
        "🔮 THE FUTURE OF GAMING WORKFORCE | "
        f"Predictions Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
        "Strategic Foresight Dashboard"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
