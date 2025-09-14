# tests/test_streamlit_app.py
from streamlit.testing.v1 import AppTest
import pandas as pd

def test_app_loads_without_errors():
    """Test que l'application se lance sans erreur"""
    at = AppTest.from_file("app.py").run()
    
    # Vérifier qu'il n'y a pas d'exception
    assert not at.exception
    
    # Vérifier que le titre est présent
    assert "Gaming Workforce Observatory" in at.title[0].value

def test_gaming_sidebar_filters():
    """Test des filtres gaming dans la sidebar"""
    at = AppTest.from_file("app.py").run()
    
    # Vérifier que les filtres départements sont présents
    department_filter = at.multiselect("Select Departments")
    assert len(department_filter.options) > 0
    
    # Simuler sélection de départements
    department_filter.select(["Programming", "Art"]).run()
    
    # Vérifier que les données sont filtrées
    assert not at.exception

def test_gaming_kpi_calculations():
    """Test des calculs KPI gaming"""
    at = AppTest.from_file("app.py").run()
    
    # Vérifier que les métriques gaming sont affichées
    metrics = at.metric
    assert len(metrics) >= 4  # Au moins 4 KPIs gaming
    
    # Vérifier les noms des KPIs
    kpi_labels = [metric.label for metric in metrics]
    assert "Total Employees" in kpi_labels
    assert "Avg Satisfaction" in kpi_labels

def test_gaming_data_visualization():
    """Test des visualisations gaming"""
    at = AppTest.from_file("app.py").run()
    
    # Vérifier qu'il y a des graphiques
    assert len(at.plotly_chart) > 0
    
    # Vérifier que les données sont affichées
    assert len(at.dataframe) > 0
def test_with_mock_gaming_data():
    """Test avec données gaming simulées"""
    
    # Données gaming test
    test_script = ""
    
    def test_with_mock_gaming_data():
        # Données gaming test
        test_script = ""
        

# Données gaming test
gaming_data = pd.DataFrame({
    'employee_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Carol', 'David', 'Eve'],
    'department': ['Programming', 'Art', 'Game Design', 'QA', 'Marketing'],
    'satisfaction_score': [8.5, 7.2, 9.1, 6.8, 8.0],
    'performance_score': [4.2, 3.8, 4.5, 3.5, 4.1]
})

st.title("🎮 Gaming Workforce Observatory")
st.metric("Total Employees", len(gaming_data))
st.dataframe(gaming_data)
""
    
at = AppTest.from_string(test_script).run()
    
assert not at.exception
assert at.metric[0].value == "5"
assert len(at.dataframe[0].value) == 5