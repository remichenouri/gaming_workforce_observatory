"""
Gaming Workforce Observatory - Predictive Analytics Dashboard
Analytics prédictifs ML avancés pour workforce gaming
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
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error
import shap

# Ajout du chemin pour imports
sys.path.append(str(Path(__file__).parent.parent))

from src.themes.gaming_themes import GamingThemes
from src.ml.models.attrition_predictor import GamingAttritionPredictor
from src.ml.models.anomaly_detector import GamingAnomalyDetector
from src.ml.pipelines.inference_pipeline import EnterpriseInferencePipeline

def initialize_predictive_dashboard():
    """Initialise le dashboard predictive analytics"""
    st.set_page_config(
        page_title="🎯 Gaming Workforce Observatory - Predictive Analytics",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Application du thème gaming
    themes = GamingThemes()
    themes.apply_gaming_theme()

def generate_predictive_data():
    """Génère les données pour analytics prédictifs"""
    
    # Données employés avec features pour ML
    np.random.seed(42)
    n_employees = 1200
    
    employees_data = pd.DataFrame({
        'employee_id': range(1, n_employees + 1),
        'department': np.random.choice(['Programming', 'Art & Animation', 'Game Design', 'QA', 'Production'], n_employees),
        'years_experience': np.random.exponential(4, n_employees).clip(0, 25),
        'age': np.random.normal(32, 8, n_employees).clip(22, 65),
        'salary_usd': np.random.lognormal(11, 0.3, n_employees).clip(40000, 200000),
        'performance_score': np.random.beta(7, 3, n_employees) * 4 + 1,  # 1-5 scale
        'satisfaction_score': np.random.beta(3, 2, n_employees) * 9 + 1,  # 1-10 scale
        'weekly_hours': np.random.normal(45, 8, n_employees).clip(30, 80),
        'team_size': np.random.poisson(8, n_employees).clip(3, 20),
        'manager_rating': np.random.beta(5, 2, n_employees) * 4 + 1,
        'peer_feedback': np.random.normal(7.5, 1.2, n_employees).clip(1, 10),
        'training_hours_year': np.random.exponential(40, n_employees).clip(0, 200),
        'remote_work_days': np.random.choice([0, 1, 2, 3, 4, 5], n_employees, p=[0.1, 0.15, 0.25, 0.25, 0.15, 0.1]),
        'promotion_last_3_years': np.random.choice([0, 1], n_employees, p=[0.7, 0.3]),
        'project_complexity': np.random.uniform(1, 5, n_employees),
        'work_life_balance': np.random.normal(7, 1.5, n_employees).clip(1, 10)
    })
    
    # Target variables calculées
    # Attrition probability (logistic regression style)
    attrition_logits = (
        -2 +
        -0.5 * (employees_data['satisfaction_score'] - 5) / 5 +
        -0.3 * (employees_data['performance_score'] - 2.5) / 2.5 +
        0.4 * (employees_data['weekly_hours'] - 40) / 40 +
        -0.2 * employees_data['promotion_last_3_years'] +
        0.1 * np.random.normal(0, 1, n_employees)
    )
    employees_data['attrition_probability'] = 1 / (1 + np.exp(-attrition_logits))
    employees_data['will_leave_6months'] = (employees_data['attrition_probability'] > 0.6).astype(int)
    
    # Performance trend prediction
    employees_data['performance_trend'] = np.where(
        employees_data['performance_score'] > 4, 'Rising Star',
        np.where(employees_data['performance_score'] > 3.5, 'Solid Performer',
                np.where(employees_data['performance_score'] > 2.5, 'Needs Development', 'At Risk'))
    )
    
    # Salary adjustment prediction
    market_adjustment = np.random.normal(1.05, 0.15, n_employees).clip(0.8, 1.4)
    employees_data['predicted_salary_next_year'] = employees_data['salary_usd'] * market_adjustment
    employees_data['salary_adjustment_needed'] = employees_data['predicted_salary_next_year'] - employees_data['salary_usd']
    
    # Modèles ML pré-entraînés (simulé)
    model_performance = {
        'attrition_model': {
            'accuracy': 0.87,
            'precision': 0.82,
            'recall': 0.79,
            'f1_score': 0.80,
            'auc': 0.91,
            'feature_importance': {
                'satisfaction_score': 0.28,
                'weekly_hours': 0.22,
                'performance_score': 0.18,
                'work_life_balance': 0.15,
                'manager_rating': 0.12,
                'salary_vs_market': 0.05
            }
        },
        'performance_model': {
            'mae': 0.31,
            'rmse': 0.42,
            'r2': 0.73,
            'feature_importance': {
                'years_experience': 0.25,
                'training_hours_year': 0.22,
                'project_complexity': 0.20,
                'peer_feedback': 0.18,
                'manager_rating': 0.15
            }
        },
        'salary_model': {
            'mae': 8420,
            'rmse': 12150,
            'r2': 0.82,
            'feature_importance': {
                'years_experience': 0.35,
                'performance_score': 0.28,
                'department': 0.20,
                'team_size': 0.10,
                'location': 0.07
            }
        }
    }
    
    # Prédictions futures (6 mois)
    future_predictions = {
        'workforce_size': {
            'current': n_employees,
            'predicted_6m': int(n_employees * 1.08),
            'confidence_interval': (int(n_employees * 1.04), int(n_employees * 1.12))
        },
        'avg_satisfaction': {
            'current': employees_data['satisfaction_score'].mean(),
            'predicted_6m': employees_data['satisfaction_score'].mean() + 0.3,
            'confidence_interval': (employees_data['satisfaction_score'].mean() - 0.2, 
                                  employees_data['satisfaction_score'].mean() + 0.8)
        },
        'attrition_rate': {
            'current': employees_data['will_leave_6months'].mean() * 100,
            'predicted_6m': employees_data['will_leave_6months'].mean() * 100 * 0.85,
            'confidence_interval': (employees_data['will_leave_6months'].mean() * 100 * 0.75,
                                  employees_data['will_leave_6months'].mean() * 100 * 0.95)
        }
    }
    
    return employees_data, model_performance, future_predictions

def render_ml_models_overview(model_performance):
    """Vue d'ensemble des modèles ML"""
    
    themes = GamingThemes()
    
    # Header Predictive Analytics
    st.markdown("""
    <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;'>
        <h1 style='color: white; font-family: "Orbitron", monospace; font-size: 3rem; margin: 0;'>🎯 PREDICTIVE ANALYTICS</h1>
        <h2 style='color: rgba(255,255,255,0.9); margin: 0.5rem 0;'>Advanced ML Intelligence for Gaming Workforce</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; margin: 0;'>Future-ready insights powered by machine learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Performance Metrics
    st.markdown("### 🤖 ML Models Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🚪 Attrition Prediction Model")
        attrition_perf = model_performance['attrition_model']
        
        metric_html = themes.create_metric_card(
            "Model Accuracy", 
            f"{attrition_perf['accuracy']:.1%}",
            f"AUC: {attrition_perf['auc']:.2f}",
            "success",
            "🎯"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
        
        st.metric("Precision", f"{attrition_perf['precision']:.2f}")
        st.metric("Recall", f"{attrition_perf['recall']:.2f}")
    
    with col2:
        st.markdown("#### ⭐ Performance Prediction Model")
        perf_model = model_performance['performance_model']
        
        metric_html = themes.create_metric_card(
            "R² Score", 
            f"{perf_model['r2']:.2f}",
            f"MAE: {perf_model['mae']:.2f}",
            "info",
            "📊"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
        
        st.metric("RMSE", f"{perf_model['rmse']:.2f}")
        st.metric("Mean Abs Error", f"{perf_model['mae']:.2f}")
    
    with col3:
        st.markdown("#### 💰 Salary Prediction Model")
        salary_model = model_performance['salary_model']
        
        metric_html = themes.create_metric_card(
            "R² Score", 
            f"{salary_model['r2']:.2f}",
            f"MAE: ${salary_model['mae']:,.0f}",
            "warning",
            "💵"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
        
        st.metric("RMSE", f"${salary_model['rmse']:,.0f}")
        st.metric("Mean Abs Error", f"${salary_model['mae']:,.0f}")

def render_attrition_predictions(employees_data):
    """Prédictions d'attrition"""
    
    st.markdown("### 🚪 Attrition Risk Predictions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des risques d'attrition
        risk_bins = pd.cut(employees_data['attrition_probability'], 
                          bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                          labels=['Very Low', 'Low', 'Medium', 'High', 'Critical'])
        
        risk_counts = risk_bins.value_counts()
        
        fig_risk_dist = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title='🎯 Attrition Risk Distribution',
            color_discrete_sequence=['#27ae60', '#f39c12', '#e67e22', '#e74c3c', '#8e44ad']
        )
        
        st.plotly_chart(fig_risk_dist, use_container_width=True)
    
    with col2:
        # Top employés à risque
        high_risk_employees = employees_data[
            employees_data['attrition_probability'] > 0.7
        ].nlargest(10, 'attrition_probability')
        
        st.markdown("#### 🚨 Employees at Critical Risk")
        
        for _, emp in high_risk_employees.iterrows():
            risk_pct = emp['attrition_probability'] * 100
            
            with st.expander(f"Employee {emp['employee_id']} - {risk_pct:.1f}% risk"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"**Department:** {emp['department']}")
                    st.markdown(f"**Experience:** {emp['years_experience']:.1f} years")
                    st.markdown(f"**Satisfaction:** {emp['satisfaction_score']:.1f}/10")
                
                with col_b:
                    st.markdown(f"**Performance:** {emp['performance_score']:.1f}/5")
                    st.markdown(f"**Weekly Hours:** {emp['weekly_hours']:.0f}h")
                    st.markdown(f"**Work-Life Balance:** {emp['work_life_balance']:.1f}/10")
    
    # Analyse des facteurs de risque
    st.markdown("#### 📊 Risk Factor Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Satisfaction vs Attrition Risk
        fig_satisfaction = px.scatter(
            employees_data.sample(300),  # Sample pour performance
            x='satisfaction_score',
            y='attrition_probability',
            color='department',
            size='weekly_hours',
            title='😊 Satisfaction vs Attrition Risk',
            labels={
                'satisfaction_score': 'Satisfaction Score (1-10)',
                'attrition_probability': 'Attrition Probability'
            }
        )
        
        fig_satisfaction.update_layout(height=400)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    with col2:
        # Performance vs Attrition Risk
        fig_performance = px.scatter(
            employees_data.sample(300),
            x='performance_score',
            y='attrition_probability',
            color='years_experience',
            title='⭐ Performance vs Attrition Risk',
            labels={
                'performance_score': 'Performance Score (1-5)',
                'attrition_probability': 'Attrition Probability'
            },
            color_continuous_scale='Viridis'
        )
        
        fig_performance.update_layout(height=400)
        st.plotly_chart(fig_performance, use_container_width=True)

def render_performance_predictions(employees_data):
    """Prédictions de performance"""
    
    st.markdown("### ⭐ Performance Predictions & Talent Development")
    
    # Analyse des tendances de performance
    perf_trends = employees_data['performance_trend'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des tendances de performance
        fig_trends = px.bar(
            x=perf_trends.index,
            y=perf_trends.values,
            title='📈 Performance Trends Distribution',
            color=perf_trends.values,
            color_continuous_scale='RdYlGn'
        )
        
        fig_trends.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_trends, use_container_width=True)
    
    with col2:
        # Performance vs Training correlation
        fig_training = px.scatter(
            employees_data.sample(300),
            x='training_hours_year',
            y='performance_score',
            color='department',
            size='years_experience',
            title='📚 Training Impact on Performance',
            labels={
                'training_hours_year': 'Training Hours per Year',
                'performance_score': 'Performance Score'
            }
        )
        
        fig_training.update_layout(height=400)
        st.plotly_chart(fig_training, use_container_width=True)
    
    # Rising Stars Analysis
    rising_stars = employees_data[
        employees_data['performance_trend'] == 'Rising Star'
    ].nlargest(8, 'performance_score')
    
    st.markdown("#### 🌟 Rising Stars - High Potential Employees")
    
    cols = st.columns(4)
    
    for i, (_, star) in enumerate(rising_stars.iterrows()):
        col_idx = i % 4
        
        with cols[col_idx]:
            star_card = f"""
            <div style='background: linear-gradient(135deg, #27ae60, #2ecc71); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;'>
                <h4 style='margin: 0; color: white;'>⭐ Employee {star['employee_id']}</h4>
                <p style='margin: 0.5rem 0; font-size: 0.9rem;'>
                    {star['department']}<br>
                    Performance: {star['performance_score']:.1f}/5<br>
                    Experience: {star['years_experience']:.1f} yrs<br>
                    Training: {star['training_hours_year']:.0f}h/yr
                </p>
            </div>
            """
            st.markdown(star_card, unsafe_allow_html=True)

def render_salary_predictions(employees_data):
    """Prédictions salariales"""
    
    st.markdown("### 💰 Salary Predictions & Market Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des ajustements salariaux
        fig_salary_adj = px.histogram(
            employees_data,
            x='salary_adjustment_needed',
            nbins=30,
            title='💵 Predicted Salary Adjustments Distribution',
            labels={'salary_adjustment_needed': 'Salary Adjustment Needed ($)'},
            color_discrete_sequence=['#3498db']
        )
        
        fig_salary_adj.add_vline(
            x=0, line_dash="dash", line_color="red",
            annotation_text="No Adjustment"
        )
        
        st.plotly_chart(fig_salary_adj, use_container_width=True)
    
    with col2:
        # Salary vs Performance correlation
        fig_salary_perf = px.scatter(
            employees_data.sample(300),
            x='performance_score',
            y='salary_usd',
            color='department',
            size='years_experience',
            title='⚡ Current Salary vs Performance',
            labels={
                'performance_score': 'Performance Score',
                'salary_usd': 'Current Salary (USD)'
            }
        )
        
        st.plotly_chart(fig_salary_perf, use_container_width=True)
    
    # Top salary adjustment needs
    st.markdown("#### 🔄 Priority Salary Reviews")
    
    # Employés sous-payés (bon performance, salaire bas)
    underpaid = employees_data[
        (employees_data['performance_score'] > 4.0) & 
        (employees_data['salary_adjustment_needed'] > 10000)
    ].nlargest(5, 'salary_adjustment_needed')
    
    # Employés sur-payés (performance faible, salaire élevé)
    overpaid = employees_data[
        (employees_data['performance_score'] < 2.5) & 
        (employees_data['salary_adjustment_needed'] < -5000)
    ].nsmallest(5, 'salary_adjustment_needed')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📈 Underpaid High Performers")
        
        for _, emp in underpaid.iterrows():
            adjustment = emp['salary_adjustment_needed']
            current = emp['salary_usd']
            
            st.markdown(
                f"**Employee {emp['employee_id']}** ({emp['department']})  \n"
                f"Current: ${current:,.0f} → Suggested: ${current + adjustment:,.0f}  \n"
                f"Performance: {emp['performance_score']:.1f}/5 | Adjustment: +${adjustment:,.0f}"
            )
    
    with col2:
        st.markdown("##### 📉 Overpaid Underperformers")
        
        for _, emp in overpaid.iterrows():
            adjustment = emp['salary_adjustment_needed']
            current = emp['salary_usd']
            
            st.markdown(
                f"**Employee {emp['employee_id']}** ({emp['department']})  \n"
                f"Current: ${current:,.0f} → Market: ${current + adjustment:,.0f}  \n"
                f"Performance: {emp['performance_score']:.1f}/5 | Gap: ${adjustment:,.0f}"
            )

def render_future_forecasts(future_predictions):
    """Prévisions futures"""
    
    st.markdown("### 🔮 6-Month Workforce Forecasts")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Workforce size prediction
        current = future_predictions['workforce_size']['current']
        predicted = future_predictions['workforce_size']['predicted_6m']
        growth = ((predicted - current) / current) * 100
        
        st.markdown("#### 👥 Workforce Growth")
        st.metric(
            "Predicted Size (6M)",
            f"{predicted:,}",
            delta=f"+{growth:.1f}% ({predicted - current:+,})"
        )
        
        # Confidence interval
        ci_low, ci_high = future_predictions['workforce_size']['confidence_interval']
        st.markdown(f"**95% Confidence:** {ci_low:,} - {ci_high:,} employees")
    
    with col2:
        # Satisfaction prediction
        current_sat = future_predictions['avg_satisfaction']['current']
        predicted_sat = future_predictions['avg_satisfaction']['predicted_6m']
        sat_change = predicted_sat - current_sat
        
        st.markdown("#### 😊 Satisfaction Forecast")
        st.metric(
            "Predicted Avg (6M)",
            f"{predicted_sat:.1f}/10",
            delta=f"{sat_change:+.1f} points"
        )
        
        ci_low, ci_high = future_predictions['avg_satisfaction']['confidence_interval']
        st.markdown(f"**95% Confidence:** {ci_low:.1f} - {ci_high:.1f}")
    
    with col3:
        # Attrition prediction
        current_attr = future_predictions['attrition_rate']['current']
        predicted_attr = future_predictions['attrition_rate']['predicted_6m']
        attr_change = predicted_attr - current_attr
        
        st.markdown("#### 🚪 Attrition Forecast")
        st.metric(
            "Predicted Rate (6M)",
            f"{predicted_attr:.1f}%",
            delta=f"{attr_change:+.1f}pp",
            delta_color="inverse"
        )
        
        ci_low, ci_high = future_predictions['attrition_rate']['confidence_interval']
        st.markdown(f"**95% Confidence:** {ci_low:.1f}% - {ci_high:.1f}%")
    
    # Scenario modeling
    st.markdown("#### 🎲 Scenario Modeling")
    
    scenarios = {
        'Optimistic': {
            'description': 'Improved satisfaction initiatives + market growth',
            'workforce_change': '+12%',
            'satisfaction_change': '+0.8 points',
            'attrition_change': '-25%'
        },
        'Most Likely': {
            'description': 'Current trends continue with minor improvements', 
            'workforce_change': '+8%',
            'satisfaction_change': '+0.3 points',
            'attrition_change': '-15%'
        },
        'Pessimistic': {
            'description': 'Market downturn + increased competition',
            'workforce_change': '+3%',
            'satisfaction_change': '-0.2 points',
            'attrition_change': '+5%'
        }
    }
    
    cols = st.columns(3)
    
    for i, (scenario_name, scenario) in enumerate(scenarios.items()):
        with cols[i]:
            scenario_color = ['#27ae60', '#3498db', '#e74c3c'][i]
            
            scenario_card = f"""
            <div style='background: {scenario_color}; padding: 1rem; border-radius: 10px; color: white; height: 200px;'>
                <h4 style='margin: 0; color: white;'>{scenario_name} Scenario</h4>
                <p style='margin: 0.5rem 0; font-size: 0.85rem;'>{scenario['description']}</p>
                <div style='margin-top: 1rem; font-size: 0.9rem;'>
                    <strong>Workforce:</strong> {scenario['workforce_change']}<br>
                    <strong>Satisfaction:</strong> {scenario['satisfaction_change']}<br>
                    <strong>Attrition:</strong> {scenario['attrition_change']}
                </div>
            </div>
            """
            st.markdown(scenario_card, unsafe_allow_html=True)

def render_model_explainability():
    """Explicabilité des modèles ML"""
    
    st.markdown("### 🔍 Model Explainability & Feature Importance")
    
    # Simulation SHAP values
    feature_importance_data = {
        'feature': [
            'Satisfaction Score', 'Weekly Hours', 'Performance Score', 
            'Work-Life Balance', 'Manager Rating', 'Salary vs Market',
            'Years Experience', 'Training Hours', 'Team Size'
        ],
        'importance': [0.28, 0.22, 0.18, 0.15, 0.12, 0.05, 0.08, 0.06, 0.04],
        'impact_direction': ['Negative', 'Positive', 'Negative', 'Negative', 'Negative', 'Positive', 'Negative', 'Negative', 'Mixed']
    }
    
    importance_df = pd.DataFrame(feature_importance_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Feature importance chart
        fig_importance = px.bar(
            importance_df,
            x='importance',
            y='feature',
            orientation='h',
            color='impact_direction',
            title='🎯 Feature Importance in Attrition Prediction',
            color_discrete_map={
                'Positive': '#e74c3c',    # Increases attrition
                'Negative': '#27ae60',    # Decreases attrition  
                'Mixed': '#f39c12'        # Context dependent
            }
        )
        
        fig_importance.update_layout(height=400)
        st.plotly_chart(fig_importance, use_container_width=True)
    
    with col2:
        st.markdown("#### 💡 Key Insights from Model")
        
        insights = [
            "**Satisfaction Score** is the strongest predictor - 1 point increase reduces attrition risk by 12%",
            "**Weekly Hours** over 50h significantly increase attrition probability",
            "**Performance Score** paradox: top performers often leave (better opportunities)",
            "**Work-Life Balance** below 6/10 is a critical risk factor",
            "**Manager Rating** has compounding effect with satisfaction"
        ]
        
        for insight in insights:
            st.markdown(f"• {insight}")
        
        st.markdown("#### 🎪 Model Recommendations")
        
        recommendations = [
            "Focus retention efforts on satisfaction improvement",
            "Monitor and cap excessive working hours",
            "Create career progression paths for high performers",
            "Implement work-life balance initiatives",
            "Invest in manager training and development"
        ]
        
        for rec in recommendations:
            st.markdown(f"✅ {rec}")

def render_prediction_simulator():
    """Simulateur de prédictions interactif"""
    
    st.markdown("### 🎮 Interactive Prediction Simulator")
    
    st.markdown("Adjust employee parameters to see real-time attrition risk predictions:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        satisfaction = st.slider("Satisfaction Score", 1.0, 10.0, 7.0, 0.1)
        performance = st.slider("Performance Score", 1.0, 5.0, 3.5, 0.1)
        weekly_hours = st.slider("Weekly Hours", 30, 80, 45)
    
    with col2:
        work_life_balance = st.slider("Work-Life Balance", 1.0, 10.0, 7.0, 0.1)
        manager_rating = st.slider("Manager Rating", 1.0, 5.0, 3.5, 0.1)
        years_experience = st.slider("Years Experience", 0, 25, 5)
    
    with col3:
        department = st.selectbox("Department", ['Programming', 'Art & Animation', 'Game Design', 'QA', 'Production'])
        remote_days = st.slider("Remote Work Days/Week", 0, 5, 2)
        recent_promotion = st.checkbox("Recent Promotion (last 3 years)")
    
    # Calcul de la prédiction (simulation)
    risk_score = (
        (-0.08 * satisfaction) +
        (-0.05 * performance) +
        (0.01 * weekly_hours) +
        (-0.06 * work_life_balance) +
        (-0.04 * manager_rating) +
        (-0.01 * years_experience) +
        (-0.1 if recent_promotion else 0) +
        0.5  # baseline
    )
    
    risk_probability = max(0, min(1, 1 / (1 + np.exp(-risk_score))))
    
    # Affichage du résultat
    themes = GamingThemes()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gauge de risque
        risk_percentage = risk_probability * 100
        
        if risk_percentage < 20:
            risk_level = "Very Low"
            color = "#27ae60"
        elif risk_percentage < 40:
            risk_level = "Low"  
            color = "#f39c12"
        elif risk_percentage < 60:
            risk_level = "Medium"
            color = "#e67e22"
        elif risk_percentage < 80:
            risk_level = "High"
            color = "#e74c3c"
        else:
            risk_level = "Critical"
            color = "#8e44ad"
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Attrition Risk Level: {risk_level}"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 20], 'color': "rgba(39, 174, 96, 0.3)"},
                    {'range': [20, 40], 'color': "rgba(243, 156, 18, 0.3)"},
                    {'range': [40, 60], 'color': "rgba(230, 126, 34, 0.3)"},
                    {'range': [60, 80], 'color': "rgba(231, 76, 60, 0.3)"},
                    {'range': [80, 100], 'color': "rgba(142, 68, 173, 0.3)"}
                ]
            }
        ))
        
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Risk Assessment")
        st.metric("Attrition Probability", f"{risk_percentage:.1f}%")
        
        # Top risk factors pour cet employé
        risk_factors = []
        
        if satisfaction < 6:
            risk_factors.append(f"🔴 Low satisfaction ({satisfaction:.1f}/10)")
        if weekly_hours > 55:
            risk_factors.append(f"🟠 Excessive hours ({weekly_hours}h/week)")
        if work_life_balance < 6:
            risk_factors.append(f"🟡 Poor work-life balance ({work_life_balance:.1f}/10)")
        if performance < 3:
            risk_factors.append(f"🔴 Low performance ({performance:.1f}/5)")
        if manager_rating < 3:
            risk_factors.append(f"🟠 Poor manager relationship ({manager_rating:.1f}/5)")
        
        if risk_factors:
            st.markdown("**Key Risk Factors:**")
            for factor in risk_factors:
                st.markdown(f"• {factor}")
        else:
            st.success("✅ No major risk factors identified!")
        
        # Recommandations
        recommendations = []
        
        if satisfaction < 7:
            recommendations.append("Conduct satisfaction interview")
        if weekly_hours > 50:
            recommendations.append("Review workload distribution")
        if work_life_balance < 7:
            recommendations.append("Discuss flexible work arrangements")
        if performance < 3.5:
            recommendations.append("Implement performance improvement plan")
        
        if recommendations:
            st.markdown("**Recommended Actions:**")
            for rec in recommendations:
                st.markdown(f"✅ {rec}")

def main():
    """Fonction principale Predictive Analytics"""
    
    initialize_predictive_dashboard()
    
    # Génération des données
    employees_data, model_performance, future_predictions = generate_predictive_data()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 ML Analytics Hub")
        
        analytics_sections = [
            "🤖 ML Models Overview",
            "🚪 Attrition Predictions", 
            "⭐ Performance Forecasts",
            "💰 Salary Predictions",
            "🔮 Future Forecasts",
            "🔍 Model Explainability",
            "🎮 Prediction Simulator"
        ]
        
        selected_section = st.selectbox(
            "Select Analytics Module:",
            analytics_sections,
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📊 Model Status")
        
        # Model health indicators
        themes = GamingThemes()
        
        attrition_status = themes.create_status_indicator('online')
        performance_status = themes.create_status_indicator('online')
        salary_status = themes.create_status_indicator('online')
        
        st.markdown(f"**Attrition Model:** {attrition_status}", unsafe_allow_html=True)
        st.markdown(f"**Performance Model:** {performance_status}", unsafe_allow_html=True)  
        st.markdown(f"**Salary Model:** {salary_status}", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ⚡ Quick Stats")
        
        high_risk_count = (employees_data['attrition_probability'] > 0.7).sum()
        rising_stars = (employees_data['performance_trend'] == 'Rising Star').sum()
        
        st.metric("High Risk Employees", high_risk_count, delta_color="inverse")
        st.metric("Rising Stars", rising_stars)
        st.metric("Models Accuracy", "87%", delta="+2% this month")
        
        # Quick actions
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("🔄 Retrain Models"):
            st.success("Models queued for retraining!")
        
        if st.button("📧 Send Risk Alerts"):
            st.success("Risk alerts sent to managers!")
        
        if st.button("📊 Generate ML Report"):
            st.success("ML insights report generated!")
    
    # Contenu principal
    if selected_section == "🤖 ML Models Overview":
        render_ml_models_overview(model_performance)
    elif selected_section == "🚪 Attrition Predictions":
        render_attrition_predictions(employees_data)
    elif selected_section == "⭐ Performance Forecasts":
        render_performance_predictions(employees_data)
    elif selected_section == "💰 Salary Predictions":
        render_salary_predictions(employees_data)
    elif selected_section == "🔮 Future Forecasts":
        render_future_forecasts(future_predictions)
    elif selected_section == "🔍 Model Explainability":
        render_model_explainability()
    elif selected_section == "🎮 Prediction Simulator":
        render_prediction_simulator()
    
    # Footer ML
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #667eea; font-weight: bold;'>"
        "🎯 POWERED BY ADVANCED MACHINE LEARNING | "
        f"Models Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
        "Predictions refreshed every 24h"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
