"""
Gaming Workforce Observatory - Charts Utilities
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_trend_chart(data, x_col, y_col, title="Trend Chart"):
    """Crée un graphique de tendance gaming"""
    fig = px.line(data, x=x_col, y=y_col, title=title)
    fig = apply_gaming_theme(fig)
    return fig

def create_performance_heatmap(data, title="Performance Heatmap"):
    """Crée une heatmap de performance gaming"""
    if 'department' in data.columns and 'performance_score' in data.columns:
        pivot_data = data.pivot_table(
            values='performance_score', 
            index='department', 
            aggfunc='mean'
        ).reset_index()
        
        fig = px.bar(pivot_data, x='department', y='performance_score', title=title)
    else:
        fig = px.bar(x=['No Data'], y=[0], title="No Performance Data")
    
    fig = apply_gaming_theme(fig)
    return fig

def apply_gaming_theme(fig):
    """Applique le thème gaming aux graphiques"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#333333'),
        colorway=['#FF6B35', '#004E89', '#1A936F', '#C5A572', '#A663CC']
    )
    return fig

def create_gaming_chart(data: pd.DataFrame, chart_type: str = 'satisfaction_by_department'):
    """Crée un graphique gaming"""
    if chart_type == 'satisfaction_by_department':
        dept_satisfaction = data.groupby('department')['satisfaction_score'].mean()
        
        fig = go.Figure(data=[
            go.Bar(
                x=dept_satisfaction.index,
                y=dept_satisfaction.values,
                marker_color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
            )
        ])
        
        fig.update_layout(
            title="Gaming Workforce Satisfaction by Department",
            xaxis_title="Department",
            yaxis_title="Satisfaction Score (1-10)",
            template="plotly"  # Template Plotly standard
        )
        
        return fig
    
    return go.Figure()  # Figure vide par défaut

def apply_gaming_theme(fig):
    """Applique un thème gaming aux graphiques"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        colorway=['#FF6B35', '#004E89', '#1A936F', '#C5A572', '#A663CC']
    )
    return fig
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def apply_gaming_theme(fig):
    """Applique un thème gaming aux graphiques"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#333333', family='Arial'),
        colorway=['#FF6B35', '#004E89', '#1A936F', '#C5A572', '#A663CC'],
        title_font=dict(size=16, color='#333333'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        )
    )
    return fig

def create_department_comparison(data, metric='satisfaction_score'):
    """Crée un graphique de comparaison par département"""
    dept_data = data.groupby('department')[metric].mean().reset_index()
    
    fig = px.bar(
        dept_data,
        x='department',
        y=metric,
        title=f"Comparaison {metric.title()} par Département Gaming",
        color=metric,
        color_continuous_scale='viridis'
    )
    
    fig = apply_gaming_theme(fig)
    return fig

def create_satisfaction_radar(data, departments=None):
    """Crée un radar chart pour la satisfaction par département"""
    if departments is None:
        departments = data['department'].unique()
    
    # Calculer moyennes par département
    radar_data = []
    for dept in departments:
        dept_data = data[data['department'] == dept]
        radar_data.append({
            'department': dept,
            'satisfaction': dept_data['satisfaction_score'].mean(),
            'performance': dept_data['performance_score'].mean() * 2,  # Scale 0-10
            'innovation': dept_data.get('innovation_index', pd.Series([75])).mean()
        })
    
    radar_df = pd.DataFrame(radar_data)
    
    fig = go.Figure()
    
    for _, row in radar_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['satisfaction'], row['performance'], row['innovation']],
            theta=['Satisfaction', 'Performance', 'Innovation'],
            fill='toself',
            name=row['department']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title="Radar Gaming: Satisfaction, Performance, Innovation"
    )
    
    fig = apply_gaming_theme(fig)
    return fig
