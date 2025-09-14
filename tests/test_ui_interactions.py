# tests/test_ui_interactions.py
import pytest
from playwright.sync_api import Page, expect
import subprocess
import time
import os
import signal

class TestGamingWorkforceUI:
    
    @pytest.fixture(scope="class", autouse=True)
    def streamlit_server(self):
        """Démarre serveur Streamlit pour tests UI"""
        # Démarrer Streamlit en arrière-plan
        process = subprocess.Popen([
            "streamlit", "run", "app.py", 
            "--server.port=8502",  # Port différent pour tests
            "--server.headless=true"
        ])
        
        # Attendre que le serveur démarre
        time.sleep(5)
        
        yield
        
        # Arrêter le serveur après tests
        process.terminate()
        process.wait()
    
    def test_gaming_dashboard_loads(self, page: Page):
        """Test chargement dashboard gaming"""
        page.goto("http://localhost:8502")
        
        # Vérifier titre
        expect(page.locator("h1")).to_contain_text("Gaming Workforce Observatory")
        
        # Vérifier présence KPIs
        expect(page.locator('[data-testid="metric-container"]')).to_have_count(4)
    
    def test_gaming_department_filter(self, page: Page):
        """Test filtres départements gaming"""
        page.goto("http://localhost:8502")
        
        # Cliquer sur le filtre départements
        department_filter = page.locator('label:has-text("Select Departments")')
        department_filter.click()
        
        # Sélectionner Programming
        page.locator('div[data-value="Programming"]').click()
        
        # Vérifier que les données sont mises à jour
        expect(page.locator('[data-testid="dataframe"]')).to_be_visible()
    
    def test_gaming_visualizations(self, page: Page):
        """Test visualisations gaming"""
        page.goto("http://localhost:8502")
        
        # Vérifier présence graphiques Plotly
        expect(page.locator('.js-plotly-plot')).to_have_count_greater_than(0)
        
        # Test interaction graphique (hover, zoom)
        chart = page.locator('.js-plotly-plot').first
        chart.hover()
        
        # Vérifier tooltip gaming
        expect(page.locator('.hoverlayer')).to_be_visible()
