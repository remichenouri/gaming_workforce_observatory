"""
Gaming Workforce Observatory - Neurodiversity ROI Calculator
Calculateur avancé du ROI de la neurodiversité dans l'industrie gaming
"""
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class NeurodiversityROICalculator:
    """Calculateur ROI neurodiversité gaming avec modèles financiers avancés"""
    
    def __init__(self):
        # Multiplicateurs de performance par condition et département
        self.performance_multipliers = {
            'ADHD': {
                'Programming': 1.15,
                'Game Design': 1.25,
                'Art & Animation': 1.20,
                'Quality Assurance': 1.10,
                'Production': 1.05
            },
            'Autism Spectrum': {
                'Programming': 1.30,
                'Quality Assurance': 1.40,
                'Art & Animation': 1.15,
                'Game Design': 1.20,
                'Production': 1.10
            },
            'Dyslexia': {
                'Game Design': 1.30,
                'Art & Animation': 1.25,
                'Programming': 1.05,
                'Quality Assurance': 1.08,
                'Production': 1.15
            }
        }
        
        # Coûts d'accommodation moyens (USD/an par employé)
        self.accommodation_costs = {
            'ADHD': {
                'equipment': 800,
                'training': 1200,
                'environment': 600,
                'ongoing_support': 400
            },
            'Autism Spectrum': {
                'equipment': 1200,
                'training': 1500,
                'environment': 1000,
                'ongoing_support': 600
            },
            'Dyslexia': {
                'equipment': 600,
                'training': 800,
                'environment': 300,
                'ongoing_support': 300
            }
        }
        
        # Métriques d'impact business
        self.business_impact_metrics = {
            'innovation_boost': 0.46,  # +46% innovation selon études
            'bug_detection_improvement': 0.30,  # +30% détection bugs
            'retention_improvement': 0.23,  # +23% rétention
            'satisfaction_boost': 0.18,  # +18% satisfaction équipe
            'problem_solving_speed': 0.30  # +30% vitesse résolution
        }
    
    @st.cache_data(ttl=3600)
    def calculate_comprehensive_roi(_self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Calcul ROI complet neurodiversité avec projections financières"""
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'configuration': config,
            'financial_analysis': _self._calculate_financial_impact(config),
            'productivity_analysis': _self._calculate_productivity_gains(config),
            'risk_mitigation': _self._calculate_risk_mitigation_value(config),
            'competitive_advantage': _self._calculate_competitive_advantage(config),
            'implementation_roadmap': _self._generate_implementation_plan(config),
            'scenario_analysis': _self._perform_scenario_analysis(config)
        }
        
        logger.info(f"Comprehensive ROI analysis completed for {config.get('total_employees', 0)} employees")
        return results
    
    def _calculate_financial_impact(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule l'impact financier détaillé"""
        
        total_employees = config.get('total_employees', 100)
        neurodiverse_percentage = config.get('neurodiverse_percentage', 20) / 100
        avg_salary = config.get('avg_salary', 95000)
        
        neurodiverse_count = int(total_employees * neurodiverse_percentage)
        neurotypical_count = total_employees - neurodiverse_count
        
        # Calcul des gains de productivité par département
        department_distribution = config.get('department_distribution', {
            'Programming': 0.35,
            'Art & Animation': 0.25,
            'Quality Assurance': 0.20,
            'Game Design': 0.15,
            'Production': 0.05
        })
        
        productivity_gains = {}
        total_productivity_value = 0
        
        for dept, percentage in department_distribution.items():
            dept_neurodiverse = int(neurodiverse_count * percentage)
            dept_neurotypical = int(neurotypical_count * percentage)
            
            # Moyenne des multiplicateurs pour les conditions neurodivergentes
            avg_multiplier = np.mean([
                self.performance_multipliers.get('ADHD', {}).get(dept, 1.0),
                self.performance_multipliers.get('Autism Spectrum', {}).get(dept, 1.0),
                self.performance_multipliers.get('Dyslexia', {}).get(dept, 1.0)
            ])
            
            baseline_output = (dept_neurodiverse + dept_neurotypical) * 100
            enhanced_output = dept_neurotypical * 100 + dept_neurodiverse * 100 * avg_multiplier
            
            productivity_gain = enhanced_output - baseline_output
            dept_salary_cost = (dept_neurodiverse + dept_neurotypical) * avg_salary
            productivity_value = (productivity_gain / 100) * dept_salary_cost
            
            productivity_gains[dept] = {
                'neurodiverse_employees': dept_neurodiverse,
                'productivity_multiplier': avg_multiplier,
                'productivity_gain_percent': ((enhanced_output / baseline_output) - 1) * 100,
                'annual_value_created': productivity_value
            }
            
            total_productivity_value += productivity_value
        
        # Calcul des coûts d'accommodation
        total_accommodation_cost = 0
        accommodation_breakdown = {}
        
        conditions_distribution = config.get('conditions_distribution', {
            'ADHD': 0.40,
            'Autism Spectrum': 0.35,
            'Dyslexia': 0.25
        })
        
        for condition, percentage in conditions_distribution.items():
            condition_count = int(neurodiverse_count * percentage)
            condition_costs = self.accommodation_costs.get(condition, {})
            
            annual_cost_per_employee = sum(condition_costs.values())
            total_condition_cost = condition_count * annual_cost_per_employee
            
            accommodation_breakdown[condition] = {
                'employees': condition_count,
                'cost_per_employee': annual_cost_per_employee,
                'total_annual_cost': total_condition_cost,
                'cost_breakdown': condition_costs
            }
            
            total_accommodation_cost += total_condition_cost
        
        # Calcul ROI final
        net_benefit = total_productivity_value - total_accommodation_cost
        roi_percentage = (net_benefit / total_accommodation_cost) * 100 if total_accommodation_cost > 0 else 0
        
        return {
            'total_productivity_value': total_productivity_value,
            'total_accommodation_cost': total_accommodation_cost,
            'net_annual_benefit': net_benefit,
            'roi_percentage': roi_percentage,
            'payback_period_months': (total_accommodation_cost / (net_benefit / 12)) if net_benefit > 0 else float('inf'),
            'productivity_gains_by_department': productivity_gains,
            'accommodation_costs_breakdown': accommodation_breakdown
        }
    
    def _calculate_productivity_gains(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse détaillée des gains de productivité"""
        
        gains_analysis = {
            'innovation_metrics': {},
            'quality_improvements': {},
            'efficiency_gains': {},
            'collaborative_benefits': {}
        }
        
        total_employees = config.get('total_employees', 100)
        neurodiverse_percentage = config.get('neurodiverse_percentage', 20) / 100
        
        # Innovation metrics
        baseline_innovation_score = 70
        enhanced_innovation_score = baseline_innovation_score * (1 + self.business_impact_metrics['innovation_boost'])
        
        gains_analysis['innovation_metrics'] = {
            'baseline_score': baseline_innovation_score,
            'enhanced_score': enhanced_innovation_score,
            'improvement_percentage': self.business_impact_metrics['innovation_boost'] * 100,
            'estimated_revenue_impact': enhanced_innovation_score * 50000  # $50K per innovation point
        }
        
        # Quality improvements
        baseline_bug_detection = 85  # 85% bug detection rate
        enhanced_bug_detection = baseline_bug_detection * (1 + self.business_impact_metrics['bug_detection_improvement'])
        
        avg_bug_cost = 2500  # Cost per bug in production
        bugs_prevented_monthly = total_employees * neurodiverse_percentage * 0.5  # 0.5 bugs prevented per neurodiverse employee
        
        gains_analysis['quality_improvements'] = {
            'baseline_detection_rate': baseline_bug_detection,
            'enhanced_detection_rate': min(98, enhanced_bug_detection),  # Cap at 98%
            'bugs_prevented_monthly': bugs_prevented_monthly,
            'monthly_cost_savings': bugs_prevented_monthly * avg_bug_cost,
            'annual_quality_savings': bugs_prevented_monthly * avg_bug_cost * 12
        }
        
        # Efficiency gains
        problem_solving_improvement = self.business_impact_metrics['problem_solving_speed']
        time_saved_hours_monthly = total_employees * neurodiverse_percentage * 8  # 8 hours saved per neurodiverse employee
        hourly_rate = config.get('avg_salary', 95000) / 2080  # Annual salary to hourly
        
        gains_analysis['efficiency_gains'] = {
            'problem_solving_improvement': problem_solving_improvement * 100,
            'time_saved_hours_monthly': time_saved_hours_monthly,
            'hourly_value_saved': hourly_rate,
            'monthly_efficiency_value': time_saved_hours_monthly * hourly_rate,
            'annual_efficiency_value': time_saved_hours_monthly * hourly_rate * 12
        }
        
        # Collaborative benefits
        satisfaction_boost = self.business_impact_metrics['satisfaction_boost']
        retention_improvement = self.business_impact_metrics['retention_improvement']
        
        avg_replacement_cost = config.get('avg_salary', 95000) * 0.75  # 75% of salary
        employees_retained_annually = total_employees * 0.15 * retention_improvement  # 15% baseline turnover
        
        gains_analysis['collaborative_benefits'] = {
            'team_satisfaction_boost': satisfaction_boost * 100,
            'retention_improvement': retention_improvement * 100,
            'employees_retained_annually': employees_retained_annually,
            'replacement_cost_savings': employees_retained_annually * avg_replacement_cost,
            'knowledge_retention_value': employees_retained_annually * (config.get('avg_salary', 95000) * 0.25)  # 25% knowledge premium
        }
        
        return gains_analysis
    
    def _calculate_risk_mitigation_value(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule la valeur de la mitigation des risques"""
        
        risk_mitigation = {
            'talent_shortage_mitigation': {},
            'diversity_compliance_benefits': {},
            'reputation_value': {},
            'innovation_risk_reduction': {}
        }
        
        total_employees = config.get('total_employees', 100)
        avg_salary = config.get('avg_salary', 95000)
        
        # Mitigation pénurie de talents
        gaming_talent_shortage_premium = 0.15  # 15% premium pour trouver talents
        neurodiverse_talent_pool_expansion = 0.08  # 8% d'élargissement du pool
        
        annual_hiring_cost_reduction = total_employees * 0.10 * avg_salary * gaming_talent_shortage_premium
        
        risk_mitigation['talent_shortage_mitigation'] = {
            'talent_pool_expansion': neurodiverse_talent_pool_expansion * 100,
            'hiring_premium_saved': gaming_talent_shortage_premium * 100,
            'annual_cost_reduction': annual_hiring_cost_reduction
        }
        
        # Benefits conformité diversité
        compliance_cost_avoidance = 150000  # Coût évité pour programmes diversité
        esg_rating_improvement_value = 500000  # Valeur amélioration rating ESG
        
        risk_mitigation['diversity_compliance_benefits'] = {
            'compliance_cost_avoidance': compliance_cost_avoidance,
            'esg_rating_value': esg_rating_improvement_value,
            'total_compliance_value': compliance_cost_avoidance + esg_rating_improvement_value
        }
        
        # Valeur réputation
        employer_brand_improvement = 0.12  # 12% amélioration attraction talents
        recruitment_cost_reduction = total_employees * 0.08 * 5000  # $5K économie par embauche
        
        risk_mitigation['reputation_value'] = {
            'employer_brand_improvement': employer_brand_improvement * 100,
            'recruitment_cost_reduction': recruitment_cost_reduction
        }
        
        return risk_mitigation
    
    def _calculate_competitive_advantage(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Évalue l'avantage concurrentiel obtenu"""
        
        competitive_analysis = {
            'market_differentiation': {},
            'talent_acquisition_advantage': {},
            'innovation_leadership': {},
            'client_perception_benefits': {}
        }
        
        # Différentiation marché
        competitors_with_programs = 0.35  # 35% des concurrents ont des programmes
        first_mover_advantage_duration = 24  # Mois d'avantage first-mover
        
        competitive_analysis['market_differentiation'] = {
            'competitors_with_similar_programs': competitors_with_programs * 100,
            'first_mover_advantage_months': first_mover_advantage_duration,
            'differentiation_score': (1 - competitors_with_programs) * 100
        }
        
        # Avantage acquisition talents
        talent_attraction_improvement = 0.25  # 25% amélioration attraction
        top_talent_capture_rate = 0.15  # 15% plus de top talents
        
        competitive_analysis['talent_acquisition_advantage'] = {
            'attraction_improvement': talent_attraction_improvement * 100,
            'top_talent_capture_boost': top_talent_capture_rate * 100
        }
        
        # Leadership innovation
        innovation_cycle_acceleration = 0.18  # 18% cycle innovation plus rapide
        breakthrough_innovation_probability = 0.32  # 32% plus de chance breakthrough
        
        competitive_analysis['innovation_leadership'] = {
            'cycle_acceleration': innovation_cycle_acceleration * 100,
            'breakthrough_probability_boost': breakthrough_innovation_probability * 100
        }
        
        return competitive_analysis
    
    def _generate_implementation_plan(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un plan d'implémentation détaillé"""
        
        total_employees = config.get('total_employees', 100)
        target_percentage = config.get('neurodiverse_percentage', 20)
        
        implementation_plan = {
            'phases': [
                {
                    'phase': 'Phase 1: Foundation (Months 1-3)',
                    'objectives': [
                        'Establish neurodiversity program framework',
                        'Train HR team and managers',
                        'Set up accommodation infrastructure'
                    ],
                    'budget': total_employees * 150,
                    'key_activities': [
                        'Policy development and approval',
                        'Manager training workshops',
                        'Accommodation assessment tools',
                        'Recruitment process adaptation'
                    ],
                    'success_metrics': [
                        '100% manager training completion',
                        'Accommodation infrastructure ready',
                        'Updated job descriptions and postings'
                    ]
                },
                {
                    'phase': 'Phase 2: Pilot Program (Months 4-9)',
                    'objectives': [
                        'Hire first cohort of neurodiverse employees',
                        'Implement accommodations',
                        'Monitor and adjust processes'
                    ],
                    'budget': total_employees * 300,
                    'key_activities': [
                        'Targeted recruitment campaigns',
                        'Onboarding program enhancement',
                        'Mentorship program launch',
                        'Performance tracking setup'
                    ],
                    'success_metrics': [
                        f'{target_percentage//2}% neurodiversity rate achieved',
                        '85%+ satisfaction scores from new hires',
                        'Zero accommodation-related issues'
                    ]
                },
                {
                    'phase': 'Phase 3: Scale & Optimize (Months 10-18)',
                    'objectives': [
                        'Reach target neurodiversity percentage',
                        'Optimize processes based on learnings',
                        'Measure ROI and business impact'
                    ],
                    'budget': total_employees * 200,
                    'key_activities': [
                        'Expanded recruitment efforts',
                        'Process optimization',
                        'ROI measurement and reporting',
                        'Best practices documentation'
                    ],
                    'success_metrics': [
                        f'{target_percentage}% neurodiversity rate achieved',
                        'Positive ROI demonstrated',
                        'Program sustainability established'
                    ]
                }
            ],
            'total_budget': total_employees * 650,
            'timeline_months': 18,
            'resource_requirements': {
                'dedicated_hr_fte': 1.5,
                'manager_training_hours': total_employees * 0.2 * 8,
                'accommodation_budget_annual': total_employees * target_percentage / 100 * 2000
            }
        }
        
        return implementation_plan
    
    def _perform_scenario_analysis(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse de scénarios optimiste/pessimiste/réaliste"""
        
        base_config = config.copy()
        scenarios = {}
        
        # Scénario pessimiste
        pessimistic_config = base_config.copy()
        pessimistic_config['neurodiverse_percentage'] = base_config.get('neurodiverse_percentage', 20) * 0.7
        pessimistic_multipliers = {k: {dept: mult * 0.8 for dept, mult in v.items()} 
                                 for k, v in self.performance_multipliers.items()}
        
        # Scénario optimiste  
        optimistic_config = base_config.copy()
        optimistic_config['neurodiverse_percentage'] = base_config.get('neurodiverse_percentage', 20) * 1.3
        optimistic_multipliers = {k: {dept: mult * 1.2 for dept, mult in v.items()} 
                                for k, v in self.performance_multipliers.items()}
        
        for scenario_name, scenario_config in [
            ('Pessimistic', pessimistic_config),
            ('Realistic', base_config),
            ('Optimistic', optimistic_config)
        ]:
            # Temporairement modifier les multiplicateurs pour le scénario
            original_multipliers = self.performance_multipliers.copy()
            
            if scenario_name == 'Pessimistic':
                self.performance_multipliers = pessimistic_multipliers
            elif scenario_name == 'Optimistic':
                self.performance_multipliers = optimistic_multipliers
            
            financial_impact = self._calculate_financial_impact(scenario_config)
            
            scenarios[scenario_name] = {
                'neurodiverse_percentage': scenario_config['neurodiverse_percentage'],
                'roi_percentage': financial_impact['roi_percentage'],
                'net_annual_benefit': financial_impact['net_annual_benefit'],
                'payback_period_months': financial_impact['payback_period_months'],
                'total_productivity_value': financial_impact['total_productivity_value']
            }
            
            # Restaurer multiplicateurs originaux
            self.performance_multipliers = original_multipliers
        
        return scenarios
    
    def render_roi_calculator_interface(self):
        """Interface interactive du calculateur ROI"""
        
        st.markdown("# 🧠 Neurodiversity ROI Calculator - Gaming Industry")
        st.markdown("*Calculate the business impact of neurodiversity programs in gaming studios*")
        
        # Configuration de base
        st.markdown("## ⚙️ Organization Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_employees = st.number_input(
                "Total Employees",
                min_value=10,
                max_value=10000,
                value=200,
                step=10
            )
            
            neurodiverse_percentage = st.slider(
                "Target Neurodiversity Percentage",
                min_value=5,
                max_value=30,
                value=20,
                step=1
            )
            
            avg_salary = st.number_input(
                "Average Annual Salary (USD)",
                min_value=40000,
                max_value=200000,
                value=95000,
                step=5000
            )
        
        with col2:
            st.markdown("### Department Distribution")
            prog_pct = st.slider("Programming %", 0, 60, 35)
            art_pct = st.slider("Art & Animation %", 0, 40, 25)
            qa_pct = st.slider("Quality Assurance %", 0, 30, 20)
            design_pct = st.slider("Game Design %", 0, 25, 15)
            prod_pct = 100 - prog_pct - art_pct - qa_pct - design_pct
            
            st.info(f"Production: {prod_pct}% (auto-calculated)")
        
        # Configuration des conditions
        st.markdown("### Neurodivergent Conditions Distribution")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            adhd_pct = st.slider("ADHD %", 0, 60, 40)
        with col2:
            autism_pct = st.slider("Autism Spectrum %", 0, 50, 35)
        with col3:
            dyslexia_pct = st.slider("Dyslexia %", 0, 40, 25)
        
        # Normaliser les pourcentages
        total_conditions = adhd_pct + autism_pct + dyslexia_pct
        if total_conditions != 100:
            st.warning(f"Condition percentages total {total_conditions}%. Adjusting proportionally to 100%.")
            adhd_pct = int(adhd_pct / total_conditions * 100)
            autism_pct = int(autism_pct / total_conditions * 100)
            dyslexia_pct = 100 - adhd_pct - autism_pct
        
        # Configuration finale
        config = {
            'total_employees': total_employees,
            'neurodiverse_percentage': neurodiverse_percentage,
            'avg_salary': avg_salary,
            'department_distribution': {
                'Programming': prog_pct / 100,
                'Art & Animation': art_pct / 100,
                'Quality Assurance': qa_pct / 100,
                'Game Design': design_pct / 100,
                'Production': prod_pct / 100
            },
            'conditions_distribution': {
                'ADHD': adhd_pct / 100,
                'Autism Spectrum': autism_pct / 100,
                'Dyslexia': dyslexia_pct / 100
            }
        }
        
        # Calcul ROI
        if st.button("🚀 Calculate ROI", use_container_width=True):
            with st.spinner("Calculating comprehensive ROI analysis..."):
                results = self.calculate_comprehensive_roi(config)
                
                # Affichage des résultats
                self._display_roi_results(results)
    
    def _display_roi_results(self, results: Dict[str, Any]):
        """Affiche les résultats du calcul ROI"""
        
        financial = results['financial_analysis']
        productivity = results['productivity_analysis']
        scenarios = results['scenario_analysis']
        
        # Métriques principales
        st.markdown("## 💰 Financial Impact Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💵 Annual ROI",
                f"{financial['roi_percentage']:.1f}%",
                delta=f"{financial['roi_percentage'] - 150:.1f}%" if financial['roi_percentage'] > 150 else None
            )
        
        with col2:
            st.metric(
                "💎 Net Benefit",
                f"${financial['net_annual_benefit']:,.0f}",
                delta="Annual"
            )
        
        with col3:
            payback = financial['payback_period_months']
            st.metric(
                "⏰ Payback Period",
                f"{payback:.1f} months" if payback != float('inf') else "∞",
                delta="Break-even time"
            )
        
        with col4:
            st.metric(
                "📈 Productivity Value",
                f"${financial['total_productivity_value']:,.0f}",
                delta="Annual value created"
            )
        
        # Analyse par scénarios
        st.markdown("## 📊 Scenario Analysis")
        
        scenario_df = pd.DataFrame(scenarios).T
        scenario_df['ROI %'] = scenario_df['roi_percentage'].round(1)
        scenario_df['Net Benefit'] = scenario_df['net_annual_benefit'].apply(lambda x: f"${x:,.0f}")
        scenario_df['Neurodiversity %'] = scenario_df['neurodiverse_percentage'].round(1)
        
        st.dataframe(scenario_df[['Neurodiversity %', 'ROI %', 'Net Benefit']], use_container_width=True)
        
        # Graphique ROI par département
        st.markdown("## 🏢 ROI by Department")
        
        dept_gains = financial['productivity_gains_by_department']
        dept_df = pd.DataFrame([
            {
                'Department': dept,
                'Neurodiverse Employees': data['neurodiverse_employees'],
                'Productivity Gain %': data['productivity_gain_percent'],
                'Annual Value': data['annual_value_created']
            }
            for dept, data in dept_gains.items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(
                dept_df,
                x='Department',
                y='Productivity Gain %',
                title='Productivity Improvement by Department',
                color='Productivity Gain %',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.pie(
                dept_df,
                values='Annual Value',
                names='Department',
                title='Value Distribution by Department'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Plan d'implémentation
        st.markdown("## 🗓️ Implementation Roadmap")
        
        implementation = results['implementation_roadmap']
        
        for phase in implementation['phases']:
            with st.expander(f"📋 {phase['phase']} - Budget: ${phase['budget']:,}"):
                st.write("**Objectives:**")
                for obj in phase['objectives']:
                    st.write(f"• {obj}")
                
                st.write("**Key Activities:**")
                for activity in phase['key_activities']:
                    st.write(f"• {activity}")
                
                st.write("**Success Metrics:**")
                for metric in phase['success_metrics']:
                    st.write(f"• {metric}")
        
        st.info(f"**Total Implementation Budget:** ${implementation['total_budget']:,} over {implementation['timeline_months']} months")
