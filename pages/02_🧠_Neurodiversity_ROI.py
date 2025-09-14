"""
Gaming Workforce Observatory - Neurodiversity ROI Dashboard  
Analyse ROI et impact de la neurodiversité dans l'industrie gaming
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
from src.data.processors.neurodiversity_processor import NeurodiversityProcessor
from src.analytics.skills_gap_analyzer import GamingSkillsGapAnalyzer

def initialize_neurodiversity_dashboard():
    """Initialise le dashboard neurodiversité"""
    st.set_page_config(
        page_title="🧠 Gaming Workforce Observatory - Neurodiversity ROI",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Application du thème gaming
    themes = GamingThemes()
    themes.apply_gaming_theme()

def generate_neurodiversity_data():
    """Génère les données de neurodiversité gaming"""
    
    # Données démographiques neurodiversité
    neurodiversity_demographics = pd.DataFrame({
        'condition': ['ADHD', 'Autism Spectrum', 'Dyslexia', 'Dyspraxia', 'Other ND', 'Neurotypical'],
        'count': [145, 67, 89, 34, 28, 1487],  # Total = 1850
        'percentage': [7.8, 3.6, 4.8, 1.8, 1.5, 80.4],
        'industry_avg_percentage': [10.0, 4.0, 10.0, 6.0, 3.0, 67.0],  # Benchmarks industrie
        'gaming_representation': [145/1850*100, 67/1850*100, 89/1850*100, 34/1850*100, 28/1850*100, 1487/1850*100]
    })
    
    # Performance par condition neurodivergente
    performance_data = pd.DataFrame({
        'employee_id': range(1, 364),  # 363 employés neurodivergents
        'condition': np.random.choice(['ADHD', 'Autism Spectrum', 'Dyslexia', 'Dyspraxia', 'Other ND'], 363),
        'department': np.random.choice(['Programming', 'Art & Animation', 'Game Design', 'QA', 'Audio'], 363),
        'performance_score': np.random.normal(4.2, 0.8, 363).clip(1, 5),  # Légèrement au-dessus moyenne
        'innovation_score': np.random.normal(4.5, 0.9, 363).clip(1, 5),   # Plus élevé en innovation
        'problem_solving': np.random.normal(4.3, 0.7, 363).clip(1, 5),
        'collaboration_score': np.random.normal(3.8, 1.0, 363).clip(1, 5),
        'satisfaction_score': np.random.uniform(6.5, 9.5, 363),
        'years_experience': np.random.randint(1, 15, 363),
        'salary_usd': np.random.normal(85000, 25000, 363).clip(45000, 180000),
        'accommodations_cost': np.random.gamma(2, 1000, 363).clip(0, 8000),  # Coût accommodations
        'productivity_multiplier': np.random.normal(1.15, 0.25, 363).clip(0.8, 2.0),  # Productivité
        'retention_months': np.random.exponential(48, 363).clip(6, 120)  # Rétention plus longue
    })
    
    # ROI calculations
    baseline_productivity_value = 95000  # Valeur baseline par employé
    performance_data['productivity_value'] = (
        baseline_productivity_value * performance_data['productivity_multiplier']
    )
    performance_data['accommodation_roi'] = np.where(
        performance_data['accommodations_cost'] > 0,
        (performance_data['productivity_value'] - baseline_productivity_value - 
         performance_data['accommodations_cost']) / performance_data['accommodations_cost'] * 100,
        100  # ROI infini si pas de coût
    )
    
    # Données par département
    dept_neurodiversity = performance_data.groupby('department').agg({
        'employee_id': 'count',
        'performance_score': 'mean',
        'innovation_score': 'mean', 
        'productivity_multiplier': 'mean',
        'accommodations_cost': 'mean',
        'accommodation_roi': 'mean',
        'satisfaction_score': 'mean'
    }).round(2)
    
    dept_neurodiversity['nd_percentage'] = (dept_neurodiversity['employee_id'] / 
                                          dept_neurodiversity['employee_id'].sum() * 100).round(1)
    
    # Business impact metrics
    total_nd_employees = len(performance_data)
    total_accommodation_cost = performance_data['accommodations_cost'].sum()
    total_productivity_value = performance_data['productivity_value'].sum()
    baseline_value = baseline_productivity_value * total_nd_employees
    net_value_created = total_productivity_value - baseline_value - total_accommodation_cost
    
    business_impact = {
        'total_nd_employees': total_nd_employees,
        'total_accommodation_investment': total_accommodation_cost,
        'total_productivity_value': total_productivity_value,
        'net_value_created': net_value_created,
        'roi_percentage': (net_value_created / total_accommodation_cost * 100) if total_accommodation_cost > 0 else 0,
        'avg_performance_lift': performance_data['performance_score'].mean() - 3.5,  # vs baseline
        'innovation_premium': performance_data['innovation_score'].mean() - 3.5,
        'retention_advantage': performance_data['retention_months'].mean() - 36  # vs neurotypical avg
    }
    
    # Accommodation types and effectiveness
    accommodation_types = pd.DataFrame({
        'accommodation': [
            'Flexible Working Hours', 'Quiet Workspace', 'Written Instructions',
            'Regular Check-ins', 'Noise-Cancelling Headphones', 'Task Management Tools',
            'Sensory-Friendly Environment', 'Extended Deadlines', 'Video Call Alternatives',
            'Specialized Software', 'Mentorship Program', 'Custom Workspace Setup'
        ],
        'usage_rate': [0.78, 0.65, 0.72, 0.58, 0.45, 0.69, 0.34, 0.28, 0.41, 0.52, 0.67, 0.38],
        'cost_per_employee': [500, 1200, 200, 800, 300, 600, 2000, 0, 150, 1500, 2500, 1800],
        'effectiveness_score': [8.9, 8.7, 8.2, 7.8, 8.1, 8.5, 9.2, 7.5, 7.9, 8.8, 9.0, 8.3],
        'roi_multiplier': [4.2, 3.8, 5.1, 2.9, 3.2, 4.0, 2.1, 8.5, 4.8, 3.5, 2.2, 2.7]
    })
    
    return (neurodiversity_demographics, performance_data, dept_neurodiversity, 
            business_impact, accommodation_types)

def render_neurodiversity_overview(neurodiversity_demographics, business_impact):
    """Vue d'ensemble neurodiversité"""
    
    themes = GamingThemes()
    
    # Header neurodiversity
    st.markdown("""
    <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;'>
        <h1 style='color: white; font-family: "Orbitron", monospace; font-size: 3rem; margin: 0;'>🧠 NEURODIVERSITY ROI</h1>
        <h2 style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'>Unlocking Hidden Gaming Talent Value</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 0;'>Data-driven insights on neurodiversity's impact in gaming</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key ROI metrics
    st.markdown("### 💎 Neurodiversity ROI Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_html = themes.create_metric_card(
            "ROI on Accommodations", 
            f"{business_impact['roi_percentage']:.0f}%",
            "vs 15% industry avg",
            "success",
            "📈"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col2:
        metric_html = themes.create_metric_card(
            "Performance Premium", 
            f"+{business_impact['avg_performance_lift']:.1f} points",
            "vs neurotypical baseline",
            "success",
            "🎯"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col3:
        metric_html = themes.create_metric_card(
            "Innovation Boost", 
            f"+{business_impact['innovation_premium']:.1f} points",
            "Higher creative output",
            "success",
            "💡"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col4:
        metric_html = themes.create_metric_card(
            "Net Value Created", 
            f"${business_impact['net_value_created']:,.0f}",
            "Annual impact",
            "success",
            "💰"
        )
        st.markdown(metric_html, unsafe_allow_html=True)

def render_representation_analysis(neurodiversity_demographics):
    """Analyse de représentation neurodiversité"""
    
    st.markdown("### 🌈 Neurodiversity Representation Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gaming vs Industry representation
        comparison_data = neurodiversity_demographics[neurodiversity_demographics['condition'] != 'Neurotypical'].copy()
        
        fig_representation = go.Figure()
        
        fig_representation.add_trace(go.Bar(
            name='Gaming Industry (Our Company)',
            x=comparison_data['condition'],
            y=comparison_data['gaming_representation'],
            marker_color='#e74c3c'
        ))
        
        fig_representation.add_trace(go.Bar(
            name='Tech Industry Average',
            x=comparison_data['condition'],
            y=comparison_data['industry_avg_percentage'],
            marker_color='#3498db'
        ))
        
        fig_representation.update_layout(
            title='🎮 Gaming vs Industry ND Representation',
            barmode='group',
            yaxis_title='Percentage of Workforce',
            height=400
        )
        
        st.plotly_chart(fig_representation, use_container_width=True)
    
    with col2:
        # Neurodiversity breakdown pie
        nd_only = neurodiversity_demographics[neurodiversity_demographics['condition'] != 'Neurotypical']
        
        fig_breakdown = px.pie(
            nd_only,
            values='count',
            names='condition',
            title='🧩 Neurodivergent Population Breakdown',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig_breakdown.update_layout(height=400)
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    # ND representation insights
    st.markdown("#### 📊 Key Representation Insights")
    
    insights_cols = st.columns(3)
    
    total_nd = neurodiversity_demographics[neurodiversity_demographics['condition'] != 'Neurotypical']['count'].sum()
    total_workforce = neurodiversity_demographics['count'].sum()
    nd_percentage = (total_nd / total_workforce) * 100
    
    with insights_cols[0]:
        st.metric("Total ND Employees", f"{total_nd:,}")
        st.metric("ND Workforce %", f"{nd_percentage:.1f}%")
    
    with insights_cols[1]:
        # ADHD dominance in gaming
        adhd_gaming = neurodiversity_demographics.loc[0, 'gaming_representation']
        adhd_industry = neurodiversity_demographics.loc[0, 'industry_avg_percentage']
        st.metric("ADHD in Gaming", f"{adhd_gaming:.1f}%")
        st.metric("vs Industry Avg", f"{adhd_gaming - adhd_industry:+.1f}pp")
    
    with insights_cols[2]:
        # Autism representation
        autism_gaming = neurodiversity_demographics.loc[1, 'gaming_representation'] 
        autism_industry = neurodiversity_demographics.loc[1, 'industry_avg_percentage']
        st.metric("Autism in Gaming", f"{autism_gaming:.1f}%")
        st.metric("vs Industry Avg", f"{autism_gaming - autism_industry:+.1f}pp")

def render_performance_analysis(performance_data):
    """Analyse des performances par neurodiversité"""
    
    st.markdown("### 🎯 Performance Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance by condition
        perf_by_condition = performance_data.groupby('condition').agg({
            'performance_score': 'mean',
            'innovation_score': 'mean',
            'problem_solving': 'mean',
            'collaboration_score': 'mean'
        }).round(2)
        
        # Radar chart comparison
        categories = ['Performance', 'Innovation', 'Problem Solving', 'Collaboration']
        
        fig_radar = go.Figure()
        
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
        
        for i, condition in enumerate(perf_by_condition.index):
            values = [
                perf_by_condition.loc[condition, 'performance_score'],
                perf_by_condition.loc[condition, 'innovation_score'], 
                perf_by_condition.loc[condition, 'problem_solving'],
                perf_by_condition.loc[condition, 'collaboration_score']
            ]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=condition,
                line_color=colors[i % len(colors)]
            ))
        
        # Baseline neurotypical (simulated)
        neurotypical_baseline = [3.5, 3.5, 3.5, 3.8]
        fig_radar.add_trace(go.Scatterpolar(
            r=neurotypical_baseline,
            theta=categories,
            fill='toself',
            name='Neurotypical Baseline',
            line=dict(color='gray', dash='dash')
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[1, 5]
                )
            ),
            title="🎪 Performance Profile by ND Condition",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Productivity multiplier distribution
        fig_productivity = px.violin(
            performance_data,
            x='condition',
            y='productivity_multiplier',
            title='⚡ Productivity Distribution by Condition',
            color='condition'
        )
        
        fig_productivity.add_hline(
            y=1.0, line_dash="dash", line_color="gray",
            annotation_text="Baseline Productivity"
        )
        
        fig_productivity.update_xaxes(tickangle=45)
        fig_productivity.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_productivity, use_container_width=True)

def render_department_impact(dept_neurodiversity, performance_data):
    """Impact par département"""
    
    st.markdown("### 🏢 Departmental Neurodiversity Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ND representation by department  
        dept_nd_counts = performance_data['department'].value_counts().reset_index()
        dept_nd_counts.columns = ['department', 'nd_employees']
        
        # Estimated total employees per department (simulated)
        total_employees = {
            'Programming': 950, 'Art & Animation': 680, 'Game Design': 420,
            'QA': 380, 'Audio': 95
        }
        
        dept_nd_counts['total_employees'] = dept_nd_counts['department'].map(total_employees)
        dept_nd_counts['nd_percentage'] = (
            dept_nd_counts['nd_employees'] / dept_nd_counts['total_employees'] * 100
        ).round(1)
        
        fig_dept_nd = px.bar(
            dept_nd_counts,
            x='department',
            y='nd_percentage',
            title='🧩 ND Representation by Department',
            color='nd_percentage',
            color_continuous_scale='Viridis'
        )
        
        fig_dept_nd.update_layout(height=400)
        st.plotly_chart(fig_dept_nd, use_container_width=True)
    
    with col2:
        # Performance vs accommodation cost by department
        dept_summary = performance_data.groupby('department').agg({
            'accommodations_cost': 'mean',
            'performance_score': 'mean',
            'innovation_score': 'mean'
        }).round(2).reset_index()
        
        fig_perf_cost = px.scatter(
            dept_summary,
            x='accommodations_cost',
            y='performance_score',
            size='innovation_score',
            color='department',
            title='💰 Performance vs Accommodation Investment',
            labels={
                'accommodations_cost': 'Avg Accommodation Cost ($)',
                'performance_score': 'Avg Performance Score'
            }
        )
        
        fig_perf_cost.update_layout(height=400)
        st.plotly_chart(fig_perf_cost, use_container_width=True)
    
    # Department table
    st.markdown("#### 📋 Department ND Impact Summary")
    
    display_dept = dept_neurodiversity.reset_index()
    display_dept.columns = [
        'Department', 'ND Employees', 'Avg Performance', 'Avg Innovation',
        'Productivity Mult', 'Avg Accom Cost', 'ROI %', 'Satisfaction', 'ND %'
    ]
    
    # Format for display
    display_dept['Avg Accom Cost'] = display_dept['Avg Accom Cost'].apply(lambda x: f"${x:,.0f}")
    display_dept['ROI %'] = display_dept['ROI %'].apply(lambda x: f"{x:.1f}%")
    display_dept['Productivity Mult'] = display_dept['Productivity Mult'].apply(lambda x: f"{x:.2f}x")
    
    st.dataframe(display_dept, use_container_width=True)

def render_accommodation_analysis(accommodation_types):
    """Analyse des accommodations"""
    
    st.markdown("### 🛠️ Accommodation Effectiveness Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ROI by accommodation type
        fig_accom_roi = px.scatter(
            accommodation_types,
            x='cost_per_employee',
            y='roi_multiplier',
            size='usage_rate',
            color='effectiveness_score',
            hover_name='accommodation',
            title='💡 Accommodation ROI vs Cost Analysis',
            labels={
                'cost_per_employee': 'Cost per Employee ($)',
                'roi_multiplier': 'ROI Multiplier',
                'usage_rate': 'Usage Rate',
                'effectiveness_score': 'Effectiveness Score'
            },
            color_continuous_scale='RdYlGn'
        )
        
        fig_accom_roi.update_layout(height=400)
        st.plotly_chart(fig_accom_roi, use_container_width=True)
    
    with col2:
        # Effectiveness vs Usage
        fig_effectiveness = px.bar(
            accommodation_types.sort_values('effectiveness_score', ascending=True),
            x='effectiveness_score',
            y='accommodation',
            orientation='h',
            title='⭐ Accommodation Effectiveness Ranking',
            color='effectiveness_score',
            color_continuous_scale='RdYlGn'
        )
        
        fig_effectiveness.update_layout(height=400)
        st.plotly_chart(fig_effectiveness, use_container_width=True)
    
    # Top accommodations recommendations
    st.markdown("#### 🏆 Top Recommended Accommodations")
    
    # Calculate accommodation score (effectiveness * usage / cost factor)
    accommodation_types['recommendation_score'] = (
        accommodation_types['effectiveness_score'] * 
        accommodation_types['usage_rate'] * 
        accommodation_types['roi_multiplier'] /
        (accommodation_types['cost_per_employee'] / 1000 + 1)  # Cost factor
    ).round(2)
    
    top_accommodations = accommodation_types.nlargest(5, 'recommendation_score')
    
    for _, accom in top_accommodations.iterrows():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{accom['accommodation']}**")
            st.markdown(f"Usage Rate: {accom['usage_rate']:.0%} | Effectiveness: {accom['effectiveness_score']}/10")
        
        with col2:
            st.metric("Cost", f"${accom['cost_per_employee']:,}")
        
        with col3:
            st.metric("ROI", f"{accom['roi_multiplier']:.1f}x")

def render_business_case(business_impact, performance_data):
    """Business case pour neurodiversité"""
    
    st.markdown("### 💼 Business Case for Neurodiversity")
    
    # Financial impact summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Financial Impact (Annual)")
        
        financial_metrics = [
            ("Total Investment", f"${business_impact['total_accommodation_investment']:,.0f}"),
            ("Productivity Value", f"${business_impact['total_productivity_value']:,.0f}"),
            ("Net Value Created", f"${business_impact['net_value_created']:,.0f}"), 
            ("ROI Percentage", f"{business_impact['roi_percentage']:.1f}%"),
            ("Value per ND Employee", f"${business_impact['net_value_created']/business_impact['total_nd_employees']:,.0f}")
        ]
        
        for metric, value in financial_metrics:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.markdown(f"**{metric}:**")
            with col_b:
                st.markdown(value)
    
    with col2:
        # ROI breakdown chart
        roi_components = pd.DataFrame({
            'Component': ['Productivity Gains', 'Innovation Premium', 'Retention Savings', 'Accommodation Costs'],
            'Value': [
                business_impact['avg_performance_lift'] * 25000 * business_impact['total_nd_employees'],
                business_impact['innovation_premium'] * 15000 * business_impact['total_nd_employees'],
                business_impact['retention_advantage'] * 2000 * business_impact['total_nd_employees'],
                -business_impact['total_accommodation_investment']
            ]
        })
        
        fig_roi_breakdown = px.bar(
            roi_components,
            x='Component',
            y='Value',
            title='💎 ROI Component Breakdown',
            color='Value',
            color_continuous_scale='RdYlGn'
        )
        
        fig_roi_breakdown.update_layout(height=300)
        st.plotly_chart(fig_roi_breakdown, use_container_width=True)
    
    # Strategic recommendations
    st.markdown("#### 🎯 Strategic Neurodiversity Recommendations")
    
    recommendations = [
        {
            'title': '🎪 Expand ND Recruiting Programs',
            'impact': 'High',
            'investment': 'Medium',
            'timeline': '6-12 months',
            'description': 'Partner with ND-focused organizations and universities to build talent pipeline'
        },
        {
            'title': '🛠️ Optimize Accommodation Portfolio', 
            'impact': 'Medium',
            'investment': 'Low',
            'timeline': '3-6 months',
            'description': 'Focus on high-ROI accommodations like flexible hours and quiet workspaces'
        },
        {
            'title': '📚 ND Awareness Training',
            'impact': 'Medium',
            'investment': 'Low', 
            'timeline': '1-3 months',
            'description': 'Train managers and teams on ND strengths and effective collaboration'
        },
        {
            'title': '🔬 ND Innovation Labs',
            'impact': 'High',
            'investment': 'High',
            'timeline': '12-18 months',
            'description': 'Create specialized teams leveraging ND cognitive advantages for breakthrough projects'
        }
    ]
    
    for rec in recommendations:
        with st.expander(f"{rec['title']} - {rec['impact']} Impact"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {rec['description']}")
            
            with col2:
                st.metric("Impact", rec['impact'])
                st.metric("Investment", rec['investment'])
                st.metric("Timeline", rec['timeline'])

def render_success_stories():
    """Success stories neurodiversité"""
    
    st.markdown("### 🌟 Neurodiversity Success Stories")
    
    success_stories = [
        {
            'title': '🎮 ADHD Developer: Hyperfocus Advantage',
            'employee': 'Sarah M., Senior Game Programmer',
            'condition': 'ADHD',
            'achievement': 'Developed core optimization system increasing game performance by 40%',
            'accommodation': 'Flexible hours + noise-cancelling headphones',
            'cost': '$800',
            'value_created': '$450,000',
            'quote': "My ADHD hyperfocus lets me dive deep into complex problems others find frustrating."
        },
        {
            'title': '🧩 Autism: Pattern Recognition Excellence',
            'employee': 'Marcus T., Quality Assurance Lead', 
            'condition': 'Autism Spectrum',
            'achievement': 'Identified critical bug patterns, preventing 3 major release issues',
            'accommodation': 'Quiet workspace + written communication preferences',
            'cost': '$1,200',
            'value_created': '$2,800,000',
            'quote': "I see patterns in code that others miss. It's like having a superpower for debugging."
        },
        {
            'title': '📝 Dyslexia: Creative Problem Solving',
            'employee': 'Alex R., Game Designer',
            'condition': 'Dyslexia', 
            'achievement': 'Designed award-winning game mechanic through unique spatial thinking',
            'accommodation': 'Voice-to-text software + visual planning tools',
            'cost': '$1,500',
            'value_created': '$1,200,000',
            'quote': "Dyslexia forces me to think differently. That's exactly what game design needs."
        }
    ]
    
    for story in success_stories:
        with st.expander(f"{story['title']} - ROI: {int(story['value_created'].replace('$','').replace(',','')) / int(story['cost'].replace('$',''))}x"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Employee:** {story['employee']}")
                st.markdown(f"**Condition:** {story['condition']}")
                st.markdown(f"**Achievement:** {story['achievement']}")
                st.markdown(f"**Accommodation:** {story['accommodation']}")
                st.markdown(f"*\"{story['quote']}\"*")
            
            with col2:
                st.metric("Investment", story['cost'])
                st.metric("Value Created", story['value_created'])
                roi_multiplier = int(story['value_created'].replace('$','').replace(',','')) / int(story['cost'].replace('$',''))
                st.metric("ROI", f"{roi_multiplier:,.0f}x")

def main():
    """Fonction principale neurodiversity ROI"""
    
    initialize_neurodiversity_dashboard()
    
    # Génération des données
    (neurodiversity_demographics, performance_data, dept_neurodiversity, 
     business_impact, accommodation_types) = generate_neurodiversity_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🧠 Neurodiversity Intelligence")
        
        nd_sections = [
            "💎 ROI Overview",
            "🌈 Representation Analysis",
            "🎯 Performance Impact", 
            "🏢 Department Analysis",
            "🛠️ Accommodation Analysis",
            "💼 Business Case",
            "🌟 Success Stories"
        ]
        
        selected_section = st.selectbox(
            "Navigate to section:",
            nd_sections,
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📊 ND Quick Stats")
        
        total_nd = business_impact['total_nd_employees']
        nd_percentage = (total_nd / 1850) * 100  # Total workforce
        
        st.metric("ND Employees", f"{total_nd:,}")
        st.metric("ND Percentage", f"{nd_percentage:.1f}%") 
        st.metric("Avg ROI", f"{business_impact['roi_percentage']:.0f}%")
        
        # ND representation gauge
        themes = GamingThemes()
        nd_gauge_html = themes.create_progress_ring(
            nd_percentage, "ND Representation", "success"
        )
        st.markdown(nd_gauge_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📊 Generate ND Report"):
            st.success("Neurodiversity report generated!")
        
        if st.button("🎯 Accommodation Assessment"):
            st.success("Accommodation needs assessed!")
        
        if st.button("📧 Share Success Stories"):
            st.success("Success stories shared!")
    
    # Contenu principal
    if selected_section == "💎 ROI Overview":
        render_neurodiversity_overview(neurodiversity_demographics, business_impact)
    elif selected_section == "🌈 Representation Analysis":
        render_representation_analysis(neurodiversity_demographics)
    elif selected_section == "🎯 Performance Impact":
        render_performance_analysis(performance_data)
    elif selected_section == "🏢 Department Analysis":
        render_department_impact(dept_neurodiversity, performance_data)
    elif selected_section == "🛠️ Accommodation Analysis":
        render_accommodation_analysis(accommodation_types)
    elif selected_section == "💼 Business Case":
        render_business_case(business_impact, performance_data)
    elif selected_section == "🌟 Success Stories":
        render_success_stories()
    
    # Footer neurodiversité
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #667eea; font-weight: bold;'>"
        "🧠 NEURODIVERSITY = COMPETITIVE ADVANTAGE | "
        f"Proudly Supporting {business_impact['total_nd_employees']} ND Gaming Professionals | "
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
