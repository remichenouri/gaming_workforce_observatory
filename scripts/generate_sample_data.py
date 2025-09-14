#!/usr/bin/env python3
"""
Gaming Workforce Observatory - Générateur de données exemple
Génère des datasets réalistes pour démonstration de l'application
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data():
    """Génère tous les fichiers de données exemple"""

    # Créer dossiers si nécessaire
    os.makedirs('data/processed', exist_ok=True)

    print("🎮 Génération des données Gaming Workforce Observatory...")

    # Paramètres réalistes gaming
    np.random.seed(42)

    departments = [
        'Game Development', 'Art & Design', 'QA Testing', 
        'Data Analytics', 'DevOps', 'Product Management'
    ]
    experience_levels = ['Junior', 'Mid', 'Senior', 'Lead']

    # 1. Données employés
    print("👥 Génération données employés...")

    employees_data = []
    employee_id = 1

    for dept in departments:
        # Nombre réaliste par département
        dept_sizes = {
            'Game Development': 35,
            'Art & Design': 20, 
            'QA Testing': 25,
            'Data Analytics': 15,
            'DevOps': 18,
            'Product Management': 12
        }

        n_employees = dept_sizes.get(dept, 20)

        for i in range(n_employees):
            # Distribution réaliste des niveaux
            exp_weights = [0.4, 0.35, 0.2, 0.05]  # Plus de Junior/Mid
            exp_level = np.random.choice(experience_levels, p=exp_weights)

            # Salaires gaming réalistes (€)
            salary_ranges = {
                'Junior': (42000, 58000),
                'Mid': (58000, 78000),
                'Senior': (78000, 110000),
                'Lead': (110000, 150000)
            }

            salary = np.random.randint(*salary_ranges[exp_level])

            # Date d'embauche réaliste
            days_ago = np.random.exponential(365)  # Distribution exponentielle
            hire_date = datetime.now() - timedelta(days=min(days_ago, 2000))

            employees_data.append({
                'employee_id': employee_id,
                'department': dept,
                'experience_level': exp_level,
                'hire_date': hire_date.strftime('%Y-%m-%d'),
                'salary': salary,
                'is_active': np.random.choice([True, False], p=[0.92, 0.08])  # 92% actifs
            })
            employee_id += 1

    df_employees = pd.DataFrame(employees_data)
    df_employees.to_csv('data/processed/employees_data.csv', index=False)
    print(f"   ✅ {len(df_employees)} employés générés")

    # 2. Données performance
    print("⚡ Génération données performance...")

    performance_data = []

    for _, employee in df_employees.iterrows():
        if employee['is_active']:
            # Performance basée sur expérience + aléatoire réaliste
            exp_multipliers = {
                'Junior': np.random.normal(0.75, 0.15),
                'Mid': np.random.normal(1.0, 0.15),
                'Senior': np.random.normal(1.25, 0.12),
                'Lead': np.random.normal(1.4, 0.10)
            }

            multiplier = max(0.3, exp_multipliers[employee['experience_level']])

            # Gaming-specific adjustments
            dept_bonuses = {
                'Game Development': 1.1,  # Développeurs performants
                'Data Analytics': 1.05,
                'Art & Design': 0.95,
                'QA Testing': 0.9,
                'DevOps': 1.05,
                'Product Management': 1.0
            }

            dept_bonus = dept_bonuses.get(employee['department'], 1.0)

            base_productivity = np.random.uniform(45, 85)
            productivity = min(95, base_productivity * multiplier * dept_bonus)

            # Collaboration légèrement indépendante de productivité
            collaboration = np.random.uniform(60, 95)

            # Innovation corrélée avec expérience
            innovation_base = np.random.uniform(40, 80)
            innovation = min(95, innovation_base * multiplier)

            performance_data.append({
                'employee_id': employee['employee_id'],
                'department': employee['department'],
                'experience_level': employee['experience_level'],
                'productivity_score': round(productivity, 1),
                'collaboration_score': round(collaboration, 1),
                'innovation_score': round(innovation, 1),
                'last_performance_review': np.random.choice(['Exceeds', 'Meets', 'Below'], p=[0.25, 0.65, 0.1]),
                'certifications_earned': np.random.poisson(2)  # Moyenne 2 certifications
            })

    df_performance = pd.DataFrame(performance_data)
    df_performance.to_csv('data/processed/performance_data.csv', index=False)
    print(f"   ✅ {len(df_performance)} évaluations performance générées")

    # 3. Métriques mensuelles
    print("📊 Génération métriques mensuelles...")

    monthly_data = []

    # 18 derniers mois de données
    for month_offset in range(18):
        date = datetime.now() - timedelta(days=30 * month_offset)

        for dept in departments:
            dept_employees = df_employees[df_employees['department'] == dept]
            active_count = len(dept_employees[dept_employees['is_active']])

            # Métriques gaming avec tendances réalistes
            seasonal_factor = 1 + 0.1 * np.sin(month_offset * np.pi / 6)  # Saisonnalité

            monthly_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'department': dept,
                'active_employees': max(1, int(active_count * seasonal_factor)),
                'projects_completed': np.random.poisson(4) + 1,  # 1-8 projets
                'bug_fix_rate': np.random.uniform(82, 97),
                'employee_satisfaction': np.random.uniform(6.2, 9.1),
                'avg_sprint_velocity': np.random.uniform(18, 42),
                'code_review_time_hours': np.random.uniform(2.5, 8.0),
                'feature_delivery_time_days': np.random.randint(3, 18),
                'training_hours': np.random.randint(6, 28)
            })

    df_monthly = pd.DataFrame(monthly_data)
    df_monthly.to_csv('data/processed/monthly_metrics.csv', index=False)
    print(f"   ✅ {len(df_monthly)} métriques mensuelles générées")

    # Statistiques finales
    print("\n📈 Statistiques des données générées:")
    print(f"   👥 Total employés: {len(df_employees)}")
    print(f"   ✅ Employés actifs: {len(df_employees[df_employees['is_active']])}")
    print(f"   🏢 Départements: {len(departments)}")
    print(f"   📊 Mois de données: 18")
    print(f"   ⚡ Performance moyenne: {df_performance['productivity_score'].mean():.1f}%")
    print(f"   😊 Satisfaction moyenne: {df_monthly['employee_satisfaction'].mean():.1f}/10")

    print("\n🎉 Génération terminée avec succès!")
    print("   Fichiers créés dans data/processed/:")
    print("   - employees_data.csv")  
    print("   - performance_data.csv")
    print("   - monthly_metrics.csv")

if __name__ == "__main__":
    generate_sample_data()
