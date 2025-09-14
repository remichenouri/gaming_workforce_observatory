# Contributing to Gaming Workforce Observatory

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**

git clone https://github.com/your-username/gaming-workforce-observatory.git
cd gaming-workforce-observatory
text
3. **Create a virtual environment**

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
text
4. **Install development dependencies**

pip install -r requirements-dev.txt
pre-commit install
text

## 🔧 Development Workflow

### Setting up the environment

Generate sample data
python scripts/generate_sample_data.py
Run the application
streamlit run app.py
Run tests
pytest tests/ --cov=src
Run linting
make lint
Format code
make format
text

### Code Quality Standards

- **Python Style**: Follow PEP 8, enforced by `black` and `flake8`
- **Type Hints**: Use type hints for all functions
- **Documentation**: Document all public functions and classes
- **Testing**: Maintain >85% test coverage
- **Performance**: Keep load times <2s, chart rendering <500ms

### Commit Convention

type(scope): description
feat(dashboard): add real-time KPI updates
fix(charts): resolve mobile responsive issues
docs(readme): update installation instructions
test(kpis): add performance score calculations
text

## 🎮 Gaming Industry Focus

When contributing:
- **Use gaming terminology** (sprints, velocity, crunch, etc.)
- **Gaming-specific KPIs** preferred over generic HR metrics
- **Visual design** should maintain gaming aesthetic
- **Performance** is critical for real-time dashboards

## 📊 Data Contributions

### Adding New KPIs
1. Define in `config/kpi_definitions.yml`
2. Implement in `src/data/kpis.py`
3. Add tests in `tests/test_kpis.py`
4. Update documentation

### Sample Data Format
- Follow `config/data_schema.json`
- Realistic gaming industry values
- Include edge cases for testing
- Maintain data privacy

## 🧪 Testing Guidelines

### Test Structure

tests/
├── unit/ # Fast, isolated tests
├── integration/ # Component interaction tests
├── e2e/ # End-to-end user scenarios
└── fixtures/ # Test data
text

### Writing Tests
- Test one thing per test
- Use descriptive test names
- Include both happy path and edge cases
- Mock external dependencies

## 📝 Documentation

### Required Documentation
- **Code**: Docstrings for all public functions
- **Features**: Update relevant documentation
- **Changes**: Add entry to CHANGELOG.md
- **Breaking Changes**: Update migration guide

### Documentation Style

def calculate_gaming_kpi(
data: pd.DataFrame,
kpi_type: str,
period: int = 30
) -> Dict[str, float]:
"""
Calculate gaming-specific KPIs for workforce analytics.
text
Args:
    data: Employee performance data
    kpi_type: Type of KPI ('velocity', 'satisfaction', etc.)
    period: Analysis period in days
    
Returns:
    Dictionary with calculated KPI values
    
Raises:
    ValueError: If kpi_type is not supported
    
Example:
    >>> kpis = calculate_gaming_kpi(df, 'velocity', 14)
    >>> print(kpis['team_velocity'])
    42.5
"""

text

## 🚀 Pull Request Process

1. **Create Feature Branch**

git checkout -b feature/new-gaming-kpi
text

2. **Make Changes**
- Write code following our standards
- Add/update tests
- Update documentation

3. **Run Quality Checks**

make test
make lint
make format
text

4. **Submit Pull Request**
- Use our PR template
- Link related issues
- Add screenshots for UI changes
- Request appropriate reviewers

### PR Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact assessed
- [ ] Gaming industry context maintained

## 🎯 Issue Guidelines

### Bug Reports
Include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages/screenshots
- Sample data (if relevant)

### Feature Requests
Include:
- Gaming industry use case
- Proposed solution
- Alternative solutions considered
- Impact on existing features

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Invited to maintainer team (for significant contributions)

## 📞 Getting Help

- **Questions**: Open a Discussion
- **Bugs**: Create an Issue
- **Chat**: Join our Discord (gaming-data-analysts)
- **Email**: maintainers@gaming-workforce-observatory.com

## 🎮 Gaming Industry Resources

- [Game Industry Career Guide](https://gamecareerguide.com/)
- [IGDA Salary Survey](https://igda.org/resources-for/developers/salary-survey/)
- [Gamasutra Developer Surveys](https://gamasutra.com/category/developer-surveys/)

---

**Happy Contributing! Let's build the ultimate gaming workforce analytics platform! 🚀