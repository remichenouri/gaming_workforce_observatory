"""
Gaming Workforce Observatory - Gaming Themes Enterprise
Thèmes visuels gaming/Ubisoft pour cohérence graphique
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional
import base64
from pathlib import Path

class GamingThemes:
    """Gestionnaire de thèmes visuels gaming enterprise"""
    
    def __init__(self):
        # Palette Ubisoft officielle
        self.ubisoft_colors = {
            'primary': '#0082c4',      # Bleu Ubisoft
            'secondary': '#00d4ff',    # Cyan
            'accent': '#ff6b35',       # Orange énergique
            'success': '#00ff88',      # Vert gaming
            'warning': '#ffaa00',      # Jaune attention
            'danger': '#ff3366',       # Rouge critique
            'dark': '#1a1a2e',        # Bleu très foncé
            'light': '#eee2df',        # Beige clair
            'gradient_start': '#667eea',
            'gradient_end': '#764ba2'
        }
        
        # Palette gaming alternative
        self.gaming_colors = {
            'neon_blue': '#00ffff',
            'electric_purple': '#8a2be2',
            'laser_green': '#39ff14',
            'plasma_orange': '#ff6600',
            'cyber_pink': '#ff1493',
            'matrix_green': '#00ff00',
            'retro_gold': '#ffd700',
            'shadow_gray': '#2f2f2f'
        }
        
        # Départements gaming avec couleurs cohérentes
        self.department_colors = {
            'Programming': self.ubisoft_colors['primary'],
            'Game Design': self.gaming_colors['laser_green'],
            'Art & Animation': self.gaming_colors['plasma_orange'],
            'Quality Assurance': self.ubisoft_colors['warning'],
            'Production': self.gaming_colors['electric_purple'],
            'Audio': self.gaming_colors['cyber_pink'],
            'Marketing': self.ubisoft_colors['secondary'],
            'Management': self.ubisoft_colors['dark']
        }
        
        # Métriques de performance avec couleurs sémantiques
        self.performance_colors = {
            'excellent': self.gaming_colors['laser_green'],
            'good': self.ubisoft_colors['success'],
            'average': self.ubisoft_colors['warning'],
            'poor': self.ubisoft_colors['danger'],
            'critical': self.gaming_colors['cyber_pink']
        }
    
    def apply_gaming_theme(self):
        """Applique le thème gaming complet à Streamlit"""
        
        # CSS personnalisé gaming
        gaming_css = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
        
        /* Variables CSS pour cohérence */
        :root {{
            --ubisoft-blue: {self.ubisoft_colors['primary']};
            --ubisoft-cyan: {self.ubisoft_colors['secondary']};
            --gaming-orange: {self.ubisoft_colors['accent']};
            --gaming-green: {self.ubisoft_colors['success']};
            --dark-bg: {self.ubisoft_colors['dark']};
            --gradient-start: {self.ubisoft_colors['gradient_start']};
            --gradient-end: {self.ubisoft_colors['gradient_end']};
        }}
        
        /* Background principal avec effet gaming */
        .main .block-container {{
            background: linear-gradient(135deg, 
                rgba(26, 26, 46, 0.95) 0%, 
                rgba(52, 73, 94, 0.85) 50%, 
                rgba(26, 26, 46, 0.95) 100%);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 130, 196, 0.2);
            backdrop-filter: blur(10px);
        }}
        
        /* Headers avec police gaming */
        h1, h2, h3 {{
            font-family: 'Orbitron', monospace !important;
            color: var(--ubisoft-cyan) !important;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
            margin-bottom: 1rem !important;
        }}
        
        h1 {{
            font-size: 2.5rem !important;
            font-weight: 900 !important;
            text-align: center;
            background: linear-gradient(45deg, var(--ubisoft-blue), var(--ubisoft-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem !important;
        }}
        
        /* Sidebar gaming */
        .sidebar .sidebar-content {{
            background: linear-gradient(180deg, 
                rgba(26, 26, 46, 0.95) 0%, 
                rgba(52, 73, 94, 0.9) 100%);
            border-right: 2px solid var(--ubisoft-blue);
            box-shadow: 5px 0 15px rgba(0, 130, 196, 0.3);
        }}
        
        /* Métriques gaming */
        .metric-container {{
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(0, 212, 255, 0.3);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }}
        
        .metric-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4);
        }}
        
        /* Boutons gaming */
        .stButton > button {{
            background: linear-gradient(45deg, var(--ubisoft-blue), var(--ubisoft-cyan));
            color: white !important;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-family: 'Exo 2', sans-serif;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 130, 196, 0.3);
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(45deg, var(--ubisoft-cyan), var(--gaming-orange));
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
        }}
        
        /* Selectbox gaming */
        .stSelectbox > div > div {{
            background: rgba(26, 26, 46, 0.8);
            border: 2px solid var(--ubisoft-blue);
            border-radius: 10px;
            color: var(--ubisoft-cyan);
        }}
        
        /* Tabs gaming */
        .stTabs > div > div > div > div {{
            background: transparent;
            border-bottom: 2px solid var(--ubisoft-blue);
        }}
        
        .stTabs > div > div > div > div > button {{
            background: transparent;
            color: var(--ubisoft-cyan);
            border: none;
            font-family: 'Exo 2', sans-serif;
            font-weight: 600;
            padding: 1rem 2rem;
            transition: all 0.3s ease;
        }}
        
        .stTabs > div > div > div > div > button:hover {{
            background: rgba(0, 130, 196, 0.2);
            color: var(--gaming-orange);
        }}
        
        .stTabs > div > div > div > div > button[aria-selected="true"] {{
            background: linear-gradient(135deg, var(--ubisoft-blue), var(--ubisoft-cyan));
            color: white;
            border-radius: 10px 10px 0 0;
        }}
        
        /* Cards avec effet neon */
        .element-container {{
            background: rgba(26, 26, 46, 0.6);
            border-radius: 10px;
            border: 1px solid rgba(0, 212, 255, 0.2);
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }}
        
        .element-container:hover {{
            border-color: var(--ubisoft-cyan);
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        }}
        
        /* Alertes gaming */
        .stAlert {{
            border-radius: 10px;
            border-left: 4px solid var(--ubisoft-blue);
            background: rgba(26, 26, 46, 0.8);
            color: var(--ubisoft-cyan);
        }}
        
        /* Progress bars */
        .stProgress > div > div {{
            background: linear-gradient(90deg, var(--ubisoft-blue), var(--gaming-green));
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }}
        
        /* Dataframes gaming */
        .dataframe {{
            background: rgba(26, 26, 46, 0.9) !important;
            color: var(--ubisoft-cyan) !important;
            border: 1px solid var(--ubisoft-blue);
            border-radius: 10px;
        }}
        
        /* Scrollbars gaming */
        ::-webkit-scrollbar {{
            width: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(26, 26, 46, 0.8);
            border-radius: 6px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, var(--ubisoft-blue), var(--ubisoft-cyan));
            border-radius: 6px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, var(--ubisoft-cyan), var(--gaming-orange));
        }}
        
        /* Animation pour éléments critiques */
        @keyframes pulse-critical {{
            0% {{ box-shadow: 0 0 5px rgba(255, 51, 102, 0.5); }}
            50% {{ box-shadow: 0 0 20px rgba(255, 51, 102, 0.8); }}
            100% {{ box-shadow: 0 0 5px rgba(255, 51, 102, 0.5); }}
        }}
        
        .critical-alert {{
            animation: pulse-critical 2s infinite;
        }}
        
        /* Responsive gaming */
        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.8rem !important;
            }}
            
            .metric-container {{
                padding: 1rem;
            }}
        }}
        </style>
        """
        
        st.markdown(gaming_css, unsafe_allow_html=True)
    
    def create_metric_card(self, title: str, value: str, delta: Optional[str] = None,
                          metric_type: str = 'default', icon: str = "📊") -> str:
        """Crée une carte métrique avec style gaming"""
        
        # Couleur selon le type de métrique
        color_map = {
            'success': self.performance_colors['excellent'],
            'warning': self.performance_colors['average'], 
            'danger': self.performance_colors['poor'],
            'info': self.ubisoft_colors['primary'],
            'default': self.ubisoft_colors['secondary']
        }
        
        color = color_map.get(metric_type, color_map['default'])
        
        # Animation pour les critiques
        animation_class = 'critical-alert' if metric_type == 'danger' else ''
        
        delta_html = ""
        if delta:
            delta_color = self.performance_colors['excellent'] if '+' in delta else self.performance_colors['poor']
            delta_html = f'<div style="color: {delta_color}; font-size: 0.9rem; margin-top: 0.5rem;">{delta}</div>'
        
        card_html = f"""
        <div class="metric-container {animation_class}" style="
            background: linear-gradient(135deg, {color}20, {color}10);
            border: 2px solid {color}50;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
                <h3 style="color: {color}; margin: 0; font-family: 'Exo 2', sans-serif;">{title}</h3>
            </div>
            <div style="
                font-size: 2.5rem; 
                font-weight: 900; 
                color: {color}; 
                font-family: 'Orbitron', monospace;
                text-shadow: 0 0 10px {color}50;
            ">{value}</div>
            {delta_html}
        </div>
        """
        
        return card_html
    
    def create_department_badge(self, department: str, count: Optional[int] = None) -> str:
        """Crée un badge département avec couleur cohérente"""
        
        color = self.department_colors.get(department, self.ubisoft_colors['secondary'])
        count_text = f" ({count})" if count is not None else ""
        
        badge_html = f"""
        <span style="
            background: linear-gradient(45deg, {color}, {color}CC);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-family: 'Exo 2', sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 10px {color}40;
            display: inline-block;
            margin: 0.25rem;
        ">{department}{count_text}</span>
        """
        
        return badge_html
    
    def create_progress_ring(self, percentage: float, title: str, 
                           color_type: str = 'primary') -> str:
        """Crée un anneau de progression gaming"""
        
        color = self.ubisoft_colors.get(color_type, self.ubisoft_colors['primary'])
        
        # Calcul pour SVG circle
        radius = 45
        circumference = 2 * 3.14159 * radius
        offset = circumference - (percentage / 100) * circumference
        
        ring_html = f"""
        <div style="text-align: center; margin: 1rem;">
            <svg width="120" height="120" style="transform: rotate(-90deg);">
                <!-- Background circle -->
                <circle cx="60" cy="60" r="{radius}" 
                        fill="transparent" 
                        stroke="rgba(52, 73, 94, 0.3)" 
                        stroke-width="8"/>
                <!-- Progress circle -->
                <circle cx="60" cy="60" r="{radius}" 
                        fill="transparent" 
                        stroke="{color}" 
                        stroke-width="8"
                        stroke-dasharray="{circumference}"
                        stroke-dashoffset="{offset}"
                        stroke-linecap="round"
                        style="
                            filter: drop-shadow(0 0 10px {color}80);
                            transition: all 0.3s ease;
                        "/>
            </svg>
            <div style="
                margin-top: -75px; 
                font-family: 'Orbitron', monospace; 
                font-size: 1.5rem; 
                font-weight: 700;
                color: {color};
                text-shadow: 0 0 5px {color}50;
            ">{percentage:.1f}%</div>
            <div style="
                margin-top: 1rem;
                font-family: 'Exo 2', sans-serif;
                color: {self.ubisoft_colors['secondary']};
                font-weight: 600;
            ">{title}</div>
        </div>
        """
        
        return ring_html
    
    def create_status_indicator(self, status: str, pulse: bool = False) -> str:
        """Crée un indicateur de statut gaming"""
        
        status_config = {
            'online': {'color': self.performance_colors['excellent'], 'icon': '🟢'},
            'busy': {'color': self.performance_colors['average'], 'icon': '🟡'},
            'away': {'color': self.performance_colors['poor'], 'icon': '🟠'},
            'offline': {'color': self.ubisoft_colors['dark'], 'icon': '⚫'},
            'critical': {'color': self.performance_colors['critical'], 'icon': '🔴'}
        }
        
        config = status_config.get(status.lower(), status_config['offline'])
        animation = 'pulse-critical' if pulse else ''
        
        indicator_html = f"""
        <div class="{animation}" style="
            display: inline-flex;
            align-items: center;
            background: {config['color']}20;
            border: 1px solid {config['color']};
            border-radius: 20px;
            padding: 0.5rem 1rem;
            font-family: 'Exo 2', sans-serif;
            font-weight: 600;
            color: {config['color']};
        ">
            <span style="margin-right: 0.5rem;">{config['icon']}</span>
            {status.title()}
        </div>
        """
        
        return indicator_html
    
    def get_plotly_theme(self) -> Dict[str, Any]:
        """Retourne la configuration du thème Plotly gaming"""
        
        return {
            'layout': {
                'colorway': [
                    self.ubisoft_colors['primary'],
                    self.ubisoft_colors['accent'], 
                    self.gaming_colors['laser_green'],
                    self.gaming_colors['electric_purple'],
                    self.gaming_colors['cyber_pink'],
                    self.ubisoft_colors['warning'],
                    self.gaming_colors['retro_gold'],
                    self.ubisoft_colors['secondary']
                ],
                'font': {
                    'family': 'Exo 2, sans-serif',
                    'size': 12,
                    'color': self.ubisoft_colors['secondary']
                },
                'title': {
                    'font': {
                        'family': 'Orbitron, monospace',
                        'size': 18,
                        'color': self.ubisoft_colors['secondary']
                    }
                },
                'plot_bgcolor': 'rgba(26, 26, 46, 0.8)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'gridcolor': 'rgba(0, 130, 196, 0.2)',
                'zerolinecolor': 'rgba(0, 130, 196, 0.4)',
                'hovermode': 'closest'
            }
        }
    
    def create_dashboard_header(self, title: str, subtitle: str = "", 
                              show_status: bool = True) -> str:
        """Crée un header de dashboard gaming"""
        
        status_indicator = ""
        if show_status:
            status_indicator = self.create_status_indicator('online', pulse=False)
        
        header_html = f"""
        <div style="
            background: linear-gradient(135deg, 
                {self.ubisoft_colors['gradient_start']}, 
                {self.ubisoft_colors['gradient_end']});
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 130, 196, 0.3);
        ">
            <h1 style="
                font-family: 'Orbitron', monospace;
                font-size: 3rem;
                font-weight: 900;
                color: white;
                text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
                margin-bottom: 0.5rem;
            ">{title}</h1>
            <p style="
                font-family: 'Exo 2', sans-serif;
                font-size: 1.2rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 1rem;
            ">{subtitle}</p>
            <div style="display: flex; justify-content: center; align-items: center;">
                {status_indicator}
            </div>
        </div>
        """
        
        return header_html
    
    def apply_ubisoft_branding(self):
        """Applique le branding Ubisoft spécifique"""
        
        # Logo et éléments de branding (simulé)
        branding_css = f"""
        <style>
        /* Ubisoft branding elements */
        .ubisoft-brand {{
            background: linear-gradient(45deg, {self.ubisoft_colors['primary']}, {self.ubisoft_colors['secondary']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Orbitron', monospace;
            font-weight: 900;
        }}
        
        .ubisoft-accent {{
            color: {self.ubisoft_colors['accent']};
            text-shadow: 0 0 10px {self.ubisoft_colors['accent']}50;
        }}
        
        /* Sidebar Ubisoft */
        .css-1d391kg {{
            background: linear-gradient(180deg, 
                {self.ubisoft_colors['dark']}F0, 
                {self.ubisoft_colors['primary']}20);
        }}
        </style>
        """
        
        st.markdown(branding_css, unsafe_allow_html=True)
