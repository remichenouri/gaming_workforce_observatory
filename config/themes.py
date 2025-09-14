"""
Gaming Workforce Observatory - Thèmes visuels Gaming & Ubisoft
Design system professionnel pour maximiser l'impact visuel
"""

# Palette Couleurs Ubisoft Officielle
UBISOFT_COLORS = {
    "primary": "#0070f3",
    "secondary": "#667eea", 
    "accent": "#ff6b35",
    "success": "#00d084",
    "warning": "#ffb800",
    "danger": "#ff4757",
    "dark": "#1a1a1a",
    "light": "#f8f9fa",
    "muted": "#6c757d"
}

# Thème Gaming Professional
GAMING_THEME = {
    "background_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "card_background": "rgba(255, 255, 255, 0.95)",
    "card_shadow": "0 4px 20px rgba(0, 0, 0, 0.1)",
    "border_radius": "12px",
    "text_primary": "#2c3e50",
    "text_secondary": "#7f8c8d",
    "sidebar_bg": "#2c3e50",
    "sidebar_text": "#ecf0f1"
}

# CSS Styles Enterprise
ENTERPRISE_CSS = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header */
    .ubisoft-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .ubisoft-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
        opacity: 0.1;
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .enterprise-badge {
        background: rgba(255, 107, 53, 0.9);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 1rem;
        vertical-align: middle;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .metrics-banner {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .metric-chip {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
        line-height: 1;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .kpi-trend {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    
    .trend-positive { color: #27ae60; }
    .trend-negative { color: #e74c3c; }
    .trend-neutral { color: #95a5a6; }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%) !important;
    }
    
    .css-1d391kg .css-1cpxqw2 {
        color: #ecf0f1 !important;
    }
    
    /* Action Buttons */
    .action-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        color: white;
        text-decoration: none;
    }
    
    /* Risk Level Indicators */
    .risk-high {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        text-align: center;
    }
    
    .risk-medium {
        background: linear-gradient(45deg, #f39c12, #d35400);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        text-align: center;
    }
    
    .risk-low {
        background: linear-gradient(45deg, #27ae60, #229954);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        text-align: center;
    }
    
    /* Recommendation Cards */
    .recommendation-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 3px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3498db;
    }
    
    .recommendation-high {
        border-left-color: #e74c3c;
    }
    
    .recommendation-medium {
        border-left-color: #f39c12;
    }
    
    .recommendation-critical {
        border-left-color: #8e44ad;
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 2s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success/Error Messages */
    .alert-success {
        background: linear-gradient(45deg, #27ae60, #2ecc71);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-error {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(45deg, #f39c12, #d35400);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .app-title {
            font-size: 1.8rem;
        }
        
        .metrics-banner {
            flex-direction: column;
        }
        
        .metric-chip {
            text-align: center;
        }
    }
    
    /* Gaming Specific Elements */
    .gaming-badge {
        background: linear-gradient(45deg, #ff6b35, #ff8c42);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .studio-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
        border: 1px solid #e9ecef;
    }
    
    .studio-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Neurodiversity Specific */
    .neurodiversity-highlight {
        background: linear-gradient(45deg, #8e44ad, #9b59b6);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .roi-positive {
        color: #27ae60;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .roi-negative {
        color: #e74c3c;
        font-weight: 700;
        font-size: 1.2rem;
    }
</style>
"""
