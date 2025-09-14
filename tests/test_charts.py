"""
Gaming Workforce Observatory - Charts Tests
Tests pour les graphiques gaming Plotly
"""

import pytest
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestGamingCharts:
    """Tests pour les graphiques gaming"""
    
    @pytest.fixture
    def sample_gaming_data(self):
        """Données d'exemple pour les tests de graphiques gaming"""
        return pd.DataFrame({
            'employee_id': range(1, 21),
            'name': [f'Employee_{i}' for i in range(1, 21)],
            'department': ['Programming', 'Art', 'Game Design', 'QA', 'Marketing'] * 4,
            'level': ['Junior', 'Mid', 'Senior', 'Lead'] * 5,
            'salary': [45000, 65000, 95000, 120000] * 5,
            'satisfaction_score': [7.5, 8.2, 6.8, 9.1, 7.9] * 4,
            'performance_score': [3.8, 4.2, 3.5, 4.5, 4.0] * 4,
            'sprint_velocity': [35, 0, 42, 0, 0, 38, 0, 41, 0, 0] * 2,
            'bug_fix_rate': [0, 0, 0, 88, 0, 0, 0, 0, 92, 0] * 2,
            'innovation_index': [82, 75, 90, 68, 71] * 4,
            'years_experience': [2, 4, 7, 10, 5] * 4,
            'hire_date': pd.date_range('2020-01-01', periods=20, freq='ME')
        })
    
    def test_gaming_satisfaction_chart(self, sample_gaming_data):
        """Test du graphique de satisfaction gaming"""
        # Simuler la création d'un graphique de satisfaction par département
        dept_satisfaction = sample_gaming_data.groupby('department')['satisfaction_score'].mean()
        
        # Créer un graphique en barres gaming
        fig = go.Figure(data=[
            go.Bar(
                x=dept_satisfaction.index,
                y=dept_satisfaction.values,
                marker_color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']  # Gaming colors
            )
        ])
        
        fig.update_layout(
            title="🎮 Gaming Workforce Satisfaction by Department",
            xaxis_title="Gaming Department",
            yaxis_title="Satisfaction Score (1-10)",
            template="plotly_dark"  # Custom gaming theme
        )
        
        # Vérifications
        assert fig.data[0].type == 'bar'
        assert len(fig.data[0].x) == 5  # 5 départements gaming
        assert all(score >= 1 and score <= 10 for score in fig.data[0].y)
        assert "Gaming" in fig.layout.title.text
    
    def test_sprint_velocity_chart(self, sample_gaming_data):
        """Test du graphique de vélocité de sprint"""
        # Filtrer les départements avec sprint velocity
        dev_data = sample_gaming_data[
            sample_gaming_data['department'].isin(['Programming', 'Game Design'])
        ]
        dev_data = dev_data[dev_data['sprint_velocity'] > 0]
        
        # Créer un graphique de vélocité
        fig = px.scatter(
            dev_data,
            x='years_experience',
            y='sprint_velocity',
            color='department',
            size='performance_score',
            title="🚀 Gaming Sprint Velocity vs Experience",
            color_discrete_map={
                'Programming': '#667eea',
                'Game Design': '#764ba2'
            }
        )
        
        # Vérifications gaming
        assert len(fig.data) >= 1  # Au moins un département
        assert fig.layout.title.text.startswith("🚀")
        assert "Gaming" in fig.layout.title.text
    
    def test_bug_fix_rate_heatmap(self, sample_gaming_data):
        """Test de la heatmap des taux de correction de bugs"""
        # Créer une matrice QA vs autres départements
        qa_data = sample_gaming_data[sample_gaming_data['department'] == 'QA']
        
        if not qa_data.empty:
            # Créer une heatmap gaming
            heatmap_data = qa_data.pivot_table(
                values='bug_fix_rate',
                index='level',
                columns='years_experience',
                aggfunc='mean',
                fill_value=0
            )
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Blues',
                text=heatmap_data.values,
                texttemplate="%{text:.1f}%",
                textfont={"size": 10}
            ))
            
            fig.update_layout(
                title="🎯 Gaming QA Bug Fix Rate by Experience & Level",
                xaxis_title="Years Experience",
                yaxis_title="Gaming Level"
            )
            
            # Vérifications
            assert fig.data[0].type == 'heatmap'
            assert "Gaming" in fig.layout.title.text
    
    def test_innovation_index_radar(self, sample_gaming_data):
        """Test du graphique radar pour l'index d'innovation"""
        # Calculer l'innovation moyenne par département
        innovation_by_dept = sample_gaming_data.groupby('department')['innovation_index'].mean()
        
        # Créer un graphique radar gaming
        categories = list(innovation_by_dept.index)
        values = list(innovation_by_dept.values)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Gaming Innovation Index',
            line_color='#667eea',
            fillcolor='rgba(102, 126, 234, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="💡 Gaming Innovation Index by Department",
            showlegend=True
        )
        
        # Vérifications
        assert fig.data[0].type == 'scatterpolar'  
        assert len(fig.data[0].theta) == 5  # 5 départements
        assert all(0 <= val <= 100 for val in fig.data[0].r)
    
    def test_gaming_salary_distribution(self, sample_gaming_data):
        """Test du graphique de distribution des salaires gaming"""
        # Créer un box plot par niveau
        fig = px.box(
            sample_gaming_data,
            x='level',
            y='salary',
            color='level',
            title="💰 Gaming Salary Distribution by Level",
            color_discrete_map={
                'Junior': '#4facfe',
                'Mid': '#667eea', 
                'Senior': '#764ba2',
                'Lead': '#f093fb'
            }
        )
        
        # Ajouter les benchmarks gaming
        gaming_benchmarks = {
            'Junior': 50000,
            'Mid': 70000,
            'Senior': 95000,
            'Lead': 120000
        }
        
        for level, benchmark in gaming_benchmarks.items():
            fig.add_hline(
                y=benchmark,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Gaming Industry Avg: {level}"
            )
        
        # Vérifications
        assert len(fig.data) == 4  # 4 niveaux
        assert "Gaming" in fig.layout.title.text
        assert fig.layout.yaxis.title.text == "salary"
    
    def test_performance_vs_satisfaction_scatter(self, sample_gaming_data):
        """Test du scatter plot performance vs satisfaction"""
        fig = px.scatter(
            sample_gaming_data,
            x='performance_score',
            y='satisfaction_score',
            color='department',
            size='salary',
            hover_data=['name', 'level', 'years_experience'],
            title="📊 Gaming Performance vs Satisfaction Matrix",
            labels={
                'performance_score': 'Performance Score (1-5)',
                'satisfaction_score': 'Gaming Satisfaction (1-10)'
            }
        )
        
        # Ajouter des lignes de référence gaming
        fig.add_hline(y=7.5, line_dash="dash", line_color="green", 
                     annotation_text="Gaming Industry Target")
        fig.add_vline(x=4.0, line_dash="dash", line_color="green",
                     annotation_text="High Performance")
        
        # Vérifications
        assert len(fig.data) == 5  # 5 départements
        assert fig.layout.xaxis.title.text == 'Performance Score (1-5)'
        assert "Gaming" in fig.layout.title.text
    
    def test_gaming_theme_application(self, sample_gaming_data):
        """Test de l'application du thème gaming"""
        # Créer un graphique simple
        fig = px.bar(
            sample_gaming_data.groupby('department').size().reset_index(name='count'),
            x='department',
            y='count',
            title="Gaming Team Distribution"
        )
        
        # Appliquer le thème gaming personnalisé
        gaming_theme = {
            'layout': {
                'plot_bgcolor': '#0e1117',
                'paper_bgcolor': '#0e1117',
                'font_color': '#fafafa',
                'title': {
                    'font': {'size': 24, 'color': '#667eea'},
                    'x': 0.5
                },
                'xaxis': {
                    'gridcolor': '#2d3748',
                    'linecolor': '#667eea'
                },
                'yaxis': {
                    'gridcolor': '#2d3748', 
                    'linecolor': '#667eea'
                }
            }
        }
        
        fig.update_layout(**gaming_theme['layout'])
        
        # Vérifications du thème gaming
        assert fig.layout.plot_bgcolor == '#0e1117'  # Dark gaming background
        assert fig.layout.paper_bgcolor == '#0e1117'
        assert fig.layout.font.color == '#fafafa'    # Light text
        assert fig.layout.title.font.color == '#667eea'  # Gaming accent color
    
    def test_interactive_gaming_dashboard(self, sample_gaming_data):
        """Test du dashboard interactif gaming"""
        from plotly.subplots import make_subplots
        
        # Créer un dashboard avec multiple sous-graphiques
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "🎮 Satisfaction by Dept", "🚀 Sprint Velocity",
                "🎯 Bug Fix Rates", "💡 Innovation Index"
            ),
            specs=[
                [{"type": "bar"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "bar"}]
            ]
        )
        
        # Graphique 1: Satisfaction par département
        dept_satisfaction = sample_gaming_data.groupby('department')['satisfaction_score'].mean()
        fig.add_trace(
            go.Bar(x=dept_satisfaction.index, y=dept_satisfaction.values, name="Satisfaction"),
            row=1, col=1
        )
        
        # Graphique 2: Sprint Velocity
        dev_data = sample_gaming_data[sample_gaming_data['sprint_velocity'] > 0]
        fig.add_trace(
            go.Scatter(
                x=dev_data['years_experience'],
                y=dev_data['sprint_velocity'],
                mode='markers',
                name="Sprint Velocity"
            ),
            row=1, col=2
        )
        
        # Graphique 3: Bug Fix Rates
        qa_data = sample_gaming_data[sample_gaming_data['bug_fix_rate'] > 0]
        if not qa_data.empty:
            fig.add_trace(
                go.Bar(x=qa_data['name'], y=qa_data['bug_fix_rate'], name="Bug Fix Rate"),
                row=2, col=1
            )
        
        # Graphique 4: Innovation Index
        innovation_by_dept = sample_gaming_data.groupby('department')['innovation_index'].mean()
        fig.add_trace(
            go.Bar(x=innovation_by_dept.index, y=innovation_by_dept.values, name="Innovation"),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="🎮 Gaming Workforce Observatory Dashboard",
            showlegend=False,
            height=800
        )
        
        # Vérifications
        assert len(fig.data) >= 3  # Au moins 3 graphiques
        assert fig.layout.height == 800
        assert "Gaming" in fig.layout.title.text
    
    def test_chart_data_validation(self, sample_gaming_data):
        """Test de validation des données pour les graphiques"""
        # Vérifier que les données sont valides pour les graphiques gaming
        
        # Satisfaction: doit être entre 1 et 10
        satisfaction_valid = sample_gaming_data['satisfaction_score'].between(1, 10).all()
        assert satisfaction_valid, "Satisfaction scores must be between 1 and 10"
        
        # Performance: doit être entre 1 et 5
        performance_valid = sample_gaming_data['performance_score'].between(1, 5).all()
        assert performance_valid, "Performance scores must be between 1 and 5"
        
        # Innovation Index: doit être entre 0 et 100
        innovation_valid = sample_gaming_data['innovation_index'].between(0, 100).all()
        assert innovation_valid, "Innovation index must be between 0 and 100"
        
        # Sprint Velocity: doit être >= 0
        velocity_valid = (sample_gaming_data['sprint_velocity'] >= 0).all()
        assert velocity_valid, "Sprint velocity must be >= 0"
        
        # Bug Fix Rate: doit être entre 0 et 100
        bug_rate_valid = sample_gaming_data['bug_fix_rate'].between(0, 100).all()
        assert bug_rate_valid, "Bug fix rate must be between 0 and 100"
    
    def test_gaming_color_palette(self):
        """Test de la palette de couleurs gaming"""
        gaming_colors = {
            'primary': '#667eea',      # Blue gaming
            'secondary': '#764ba2',    # Purple tech
            'accent': '#f093fb',       # Pink highlight
            'success': '#4facfe',      # Success blue
            'warning': '#f5576c',      # Warning red
            'info': '#43e97b',         # Info green
            'dark': '#0e1117',         # Dark background
            'light': '#fafafa'         # Light text
        }
        
        # Vérifier que toutes les couleurs sont des codes hex valides
        import re
        hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        
        for color_name, color_code in gaming_colors.items():
            assert re.match(hex_pattern, color_code), f"Invalid color code for {color_name}: {color_code}"
        
        # Vérifier que nous avons assez de couleurs pour les départements gaming
        gaming_departments = ['Programming', 'Art', 'Game Design', 'QA', 'Marketing']
        available_colors = list(gaming_colors.values())[:5]  # 5 premières couleurs
        
        assert len(available_colors) >= len(gaming_departments), "Not enough colors for gaming departments"

class TestGamingChartPerformance:
    """Tests de performance pour les graphiques gaming"""
    
    def test_large_dataset_chart_performance(self):
        """Test de performance avec un grand dataset"""
        import time
        
        # Créer un grand dataset gaming
        large_data = pd.DataFrame({
            'department': ['Programming', 'Art', 'Game Design', 'QA', 'Marketing'] * 200,
            'satisfaction_score': [8.0] * 1000,
            'performance_score': [4.0] * 1000,
            'salary': [75000] * 1000
        })
        
        start_time = time.time()
        
        # Créer un graphique avec le grand dataset
        dept_summary = large_data.groupby('department')['satisfaction_score'].mean()
        fig = go.Figure(data=[go.Bar(x=dept_summary.index, y=dept_summary.values)])
        
        chart_creation_time = time.time() - start_time
        
        # Le graphique doit être créé rapidement même avec 1000 employés
        assert chart_creation_time < 1.0, f"Chart creation too slow: {chart_creation_time}s"
        assert len(fig.data[0].x) == 5  # 5 départements

if __name__ == "__main__":
    pytest.main([__file__])
