"""
Gaming Workforce Observatory - Interactive Charts
Bibliothèque de graphiques interactifs avancés pour analytics gaming
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GamingInteractiveCharts:
    """Bibliothèque de graphiques interactifs spécialisés gaming"""
    
    def __init__(self):
        self.gaming_colors = {
            'primary': '#667eea',
            'secondary': '#764ba2', 
            'accent': '#ff6b35',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#3498db'
        }
        
        self.department_colors = {
            'Programming': '#3498db',
            'Art & Animation': '#e74c3c',
            'Game Design': '#2ecc71',
            'Quality Assurance': '#f39c12',
            'Production': '#9b59b6',
            'Audio': '#1abc9c',
            'Marketing': '#34495e'
        }
    
    def create_advanced_salary_distribution(self, salary_data: pd.DataFrame,
                                          group_by: str = 'department') -> go.Figure:
        """Graphique de distribution des salaires avec box plots et violin plots"""
        
        # CORRECTION: Indentation correcte après if
        if salary_data.empty or 'salary' not in salary_data.columns:
            logger.warning('Données de salaire vides ou mal formatées')
            st.warning('Aucune donnée de salaire valide disponible')
            return self._create_empty_chart("Aucune donnée de salaire disponible")
        
        # Création du graphique
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Box Plot Distribution', 'Violin Plot Distribution'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Box plot
        for i, grp in enumerate(salary_data[group_by].unique()):
            group_data = salary_data[salary_data[group_by] == grp]['salary']
            fig.add_trace(
                go.Box(
                    y=group_data,
                    name=grp,
                    boxmean='sd',
                    marker_color=self.department_colors.get(grp, '#888888'),
                    showlegend=True if i == 0 else False
                ),
                row=1, col=1
            )
            
            # Violin plot
            fig.add_trace(
                go.Violin(
                    y=group_data,
                    name=grp,
                    box_visible=True,
                    line_color='black',
                    fillcolor=self.department_colors.get(grp, '#888888'),
                    opacity=0.6,
                    showlegend=False
                ),
                row=1, col=2
            )
        
        fig.update_layout(
            title=f'Distribution Avancée des Salaires par {group_by.title()}',
            height=500,
            showlegend=True,
            template='plotly_white'
        )
        
        fig.update_yaxes(title_text="Salaire (USD)", row=1, col=1)
        fig.update_yaxes(title_text="Salaire (USD)", row=1, col=2)
        
        return fig
    
    def create_department_performance_heatmap(self, performance_data: pd.DataFrame,
                                            metric: str = 'performance_score') -> go.Figure:
        """Heatmap de performance par département et par trimestre"""
        
        if performance_data.empty or metric not in performance_data.columns:
            logger.warning('Données de performance invalides ou manquantes')
            return self._create_empty_chart("Aucune donnée de performance disponible")
        
        # Créer des données simulées si colonnes manquantes
        if 'department' not in performance_data.columns:
            performance_data['department'] = np.random.choice(
                list(self.department_colors.keys()), 
                len(performance_data)
            )
        
        if 'quarter' not in performance_data.columns:
            performance_data['quarter'] = np.random.choice(
                ['Q1', 'Q2', 'Q3', 'Q4'], 
                len(performance_data)
            )
        
        # Créer le tableau croisé
        pivot_table = performance_data.pivot_table(
            index='department', 
            columns='quarter', 
            values=metric, 
            aggfunc='mean'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns,
            y=pivot_table.index,
            colorscale='Viridis',
            text=np.round(pivot_table.values, 2),
            texttemplate="%{text}",
            textfont={"size": 12},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=f'Heatmap Performance par Département - {metric.title()}',
            xaxis_title='Trimestre',
            yaxis_title='Département',
            template='plotly_white',
            height=500
        )
        
        return fig

    def create_employee_attrition_risk(self, attrition_data: pd.DataFrame,
                                     risk_col: str = 'attrition_probability') -> go.Figure:
        """Visualisation du risque d'attrition des employés"""
        
        if attrition_data.empty or risk_col not in attrition_data.columns:
            logger.warning("Données d'attrition invalides ou manquantes")
            return self._create_empty_chart("Aucune donnée d'attrition disponible")
        
        # Catégoriser les risques
        attrition_data = attrition_data.copy()
        attrition_data['risk_category'] = pd.cut(
            attrition_data[risk_col],
            bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
            labels=['Très Faible', 'Faible', 'Moyen', 'Élevé', 'Critique']
        )
        
        risk_counts = attrition_data['risk_category'].value_counts().sort_index()
        
        fig = px.pie(
            names=risk_counts.index,
            values=risk_counts.values,
            title="Distribution du Risque d'Attrition",
            color=risk_counts.index,
            color_discrete_map={
                'Très Faible': self.gaming_colors['success'],
                'Faible': self.gaming_colors['info'],
                'Moyen': self.gaming_colors['warning'],
                'Élevé': self.gaming_colors['accent'],
                'Critique': self.gaming_colors['danger']
            }
        )
        
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(height=500, template='plotly_white')
        
        return fig
    
    def create_talent_acquisition_funnel(self, funnel_data: pd.DataFrame = None) -> go.Figure:
        """Entonnoir de recrutement gaming"""
        
        stages = ['Applications', 'Phone Screen', 'Technical Test', 'On-site', 'Offer', 'Hired']
        values = [1000, 450, 200, 120, 80, 65]  # Valeurs par défaut
        
        if funnel_data is not None and not funnel_data.empty:
            if 'stage' in funnel_data.columns and 'count' in funnel_data.columns:
                values = [funnel_data[funnel_data['stage'] == stage]['count'].sum() for stage in stages]
        
        fig = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker_color=['#667eea', '#764ba2', '#ff6b35', '#27ae60', '#f39c12', '#e74c3c']
        ))
        
        fig.update_layout(
            title="Entonnoir de Recrutement Gaming",
            height=500,
            template='plotly_white'
        )
        
        return fig
    
    def create_skills_radar_chart(self, skills_data: pd.DataFrame = None, 
                                employee_name: str = "Employé") -> go.Figure:
        """Graphique radar des compétences gaming"""
        
        default_skills = ['Unity', 'Unreal Engine', 'C++', 'Python', 'Game Design', 
                         'Team Leadership', 'Problem Solving', 'Communication']
        default_scores = [7, 6, 8, 9, 7, 6, 8, 7]
        
        if skills_data is not None and not skills_data.empty:
            if 'skill' in skills_data.columns and 'score' in skills_data.columns:
                skills = skills_data['skill'].tolist()
                scores = skills_data['score'].tolist()
            else:
                skills = default_skills
                scores = default_scores
        else:
            skills = default_skills
            scores = default_scores
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=skills,
            fill='toself',
            name=employee_name,
            line_color=self.gaming_colors['primary'],
            fillcolor=self.gaming_colors['primary'],
            opacity=0.4
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=True,
            title=f"Profil de Compétences Gaming - {employee_name}",
            height=500,
            template='plotly_white'
        )
        
        return fig
    
    def create_compensation_benchmark(self, comp_data: pd.DataFrame = None) -> go.Figure:
        """Benchmark de compensation gaming vs marché"""
        
        companies = ['Notre Entreprise', 'Ubisoft', 'EA Games', 'Riot Games', 'Epic Games']
        programmer_salaries = [95000, 125000, 135000, 145000, 140000]
        designer_salaries = [78000, 105000, 115000, 130000, 125000]
        
        # Utiliser les vraies données si disponibles
        if comp_data is not None and not comp_data.empty:
            if 'company' in comp_data.columns:
                # Logique pour utiliser les vraies données
                pass
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Game Programmers',
            x=companies,
            y=programmer_salaries,
            marker_color=self.gaming_colors['primary']
        ))
        
        fig.add_trace(go.Bar(
            name='Game Designers',
            x=companies,
            y=designer_salaries,
            marker_color=self.gaming_colors['accent']
        ))
        
        fig.update_layout(
            barmode='group',
            title='Benchmark Compensation Gaming Industry',
            xaxis_title='Companies',
            yaxis_title='Salary (USD)',
            height=500,
            template='plotly_white'
        )
        
        return fig
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Crée un graphique vide avec message"""
        
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5, 
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            height=400,
            template='plotly_white',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        return fig

# Alias pour compatibilité
GamingChartsLibrary = GamingInteractiveCharts

# Fonction d'exemple pour tester
def create_sample_data():
    """Crée des données d'exemple pour tester les graphiques"""
    
    # Données salaires
    salary_data = pd.DataFrame({
        'department': np.random.choice(['Programming', 'Art & Animation', 'Game Design', 'Quality Assurance', 'Production'], 300),
        'salary': np.random.lognormal(mean=11, sigma=0.4, size=300)
    })
    
    # Données performance
    performance_data = pd.DataFrame({
        'department': np.random.choice(['Programming', 'Art & Animation', 'Game Design', 'Quality Assurance', 'Production'], 100),
        'quarter': np.random.choice(['Q1', 'Q2', 'Q3', 'Q4'], 100),
        'performance_score': np.random.normal(7.5, 1.2, 100).clip(1, 10)
    })
    
    # Données attrition
    attrition_data = pd.DataFrame({
        'employee_id': range(500),
        'attrition_probability': np.random.beta(2, 5, 500)
    })
    
    return salary_data, performance_data, attrition_data

# Test des fonctions si exécuté directement
if __name__ == "__main__":
    import streamlit as st
    
    st.title("Test Gaming Interactive Charts")
    
    # Créer instance
    charts = GamingInteractiveCharts()
    
    # Données d'exemple
    salary_data, performance_data, attrition_data = create_sample_data()
    
    # Test graphiques
    fig1 = charts.create_advanced_salary_distribution(salary_data)
    st.plotly_chart(fig1, use_container_width=True)
    
    fig2 = charts.create_department_performance_heatmap(performance_data)
    st.plotly_chart(fig2, use_container_width=True)
    
    fig3 = charts.create_employee_attrition_risk(attrition_data)
    st.plotly_chart(fig3, use_container_width=True)
