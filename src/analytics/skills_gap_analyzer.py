"""
Gaming Workforce Observatory - Skills Gap Analyzer Enterprise
Analyse avancée des lacunes compétences dans l'industrie gaming
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class GamingSkillsGapAnalyzer:
    """Analyseur de lacunes compétences gaming avec IA et matching sémantique"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Taxonomie des compétences gaming
        self.gaming_skills_taxonomy = {
            'Programming': {
                'Core Languages': ['C++', 'C#', 'Python', 'JavaScript', 'Lua', 'UnrealScript'],
                'Game Engines': ['Unity', 'Unreal Engine', 'Godot', 'CryEngine', 'Custom Engine'],
                'Graphics Programming': ['DirectX', 'OpenGL', 'Vulkan', 'Metal', 'Shader Programming'],
                'Platform Development': ['iOS', 'Android', 'Console', 'PC', 'Web', 'VR/AR'],
                'Tools & Frameworks': ['Git', 'Perforce', 'Visual Studio', 'Debugging', 'Profiling']
            },
            'Art & Animation': {
                'Modeling': ['3ds Max', 'Maya', 'Blender', '3D Modeling', 'Sculpting'],
                'Texturing': ['Substance Painter', 'Photoshop', 'Substance Designer', 'UV Mapping'],
                'Animation': ['Character Animation', 'Rigging', 'Motion Capture', 'Facial Animation'],
                'Concept Art': ['Digital Painting', 'Concept Design', 'Environment Art', 'Character Design'],
                'Technical Art': ['Shaders', 'VFX', 'Lighting', 'Optimization', 'Pipeline Tools']
            },
            'Game Design': {
                'Core Design': ['Game Mechanics', 'Level Design', 'System Design', 'Balancing'],
                'UX/UI': ['User Experience', 'Interface Design', 'Usability', 'Accessibility'],
                'Narrative': ['Storytelling', 'Dialogue Writing', 'Quest Design', 'Character Development'],
                'Economy': ['Monetization', 'F2P Design', 'Analytics', 'Player Retention'],
                'Documentation': ['Design Documents', 'Specification Writing', 'Communication']
            },
            'Quality Assurance': {
                'Testing': ['Manual Testing', 'Automated Testing', 'Regression Testing', 'Performance Testing'],
                'Tools': ['TestRail', 'Jira', 'Jenkins', 'Unity Test Runner'],
                'Platforms': ['Console Testing', 'Mobile Testing', 'PC Testing', 'Compatibility'],
                'Specialized': ['Localization Testing', 'Compliance Testing', 'Security Testing'],
                'Methodologies': ['Agile Testing', 'Risk Assessment', 'Test Planning']
            },
            'Production': {
                'Project Management': ['Scrum', 'Agile', 'Kanban', 'Waterfall', 'Risk Management'],
                'Tools': ['Jira', 'Confluence', 'Slack', 'Microsoft Project', 'Hansoft'],
                'Leadership': ['Team Management', 'Stakeholder Management', 'Communication'],
                'Business': ['Budget Management', 'Resource Planning', 'Timeline Management'],
                'Analytics': ['KPI Tracking', 'Data Analysis', 'Reporting', 'Metrics']
            }
        }
        
        # Niveaux de compétence et leurs descriptions
        self.skill_levels = {
            'Beginner': {'score': 1, 'description': 'Basic understanding, requires guidance'},
            'Intermediate': {'score': 2, 'description': 'Can work independently on routine tasks'},
            'Advanced': {'score': 3, 'description': 'Proficient, can handle complex tasks'},
            'Expert': {'score': 4, 'description': 'Deep expertise, can mentor others'},
            'Master': {'score': 5, 'description': 'Industry leader, innovates in the field'}
        }
    
    @st.cache_data(ttl=3600)
    def analyze_skills_gaps(_self, current_team_skills: pd.DataFrame, 
                           target_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse complète des lacunes de compétences gaming"""
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'gap_analysis': {},
            'priority_gaps': [],
            'team_strengths': [],
            'hiring_recommendations': {},
            'training_recommendations': {},
            'skill_matrix': {},
            'market_comparison': {}
        }
        
        try:
            # Analyse des lacunes par département
            gap_analysis = _self._analyze_department_gaps(current_team_skills, target_requirements)
            analysis_results['gap_analysis'] = gap_analysis
            
            # Identification des lacunes prioritaires
            priority_gaps = _self._identify_priority_gaps(gap_analysis)
            analysis_results['priority_gaps'] = priority_gaps
            
            # Forces de l'équipe
            team_strengths = _self._identify_team_strengths(current_team_skills)
            analysis_results['team_strengths'] = team_strengths
            
            # Recommandations d'embauche
            hiring_recs = _self._generate_hiring_recommendations(gap_analysis, priority_gaps)
            analysis_results['hiring_recommendations'] = hiring_recs
            
            # Recommandations de formation
            training_recs = _self._generate_training_recommendations(gap_analysis, current_team_skills)
            analysis_results['training_recommendations'] = training_recs
            
            # Matrice de compétences
            skill_matrix = _self._build_skill_matrix(current_team_skills)
            analysis_results['skill_matrix'] = skill_matrix
            
            # Comparaison marché
            market_comparison = _self._compare_with_market_standards(current_team_skills)
            analysis_results['market_comparison'] = market_comparison
            
            logger.info("Skills gap analysis completed successfully")
            
        except Exception as e:
            analysis_results['status'] = 'error'
            analysis_results['message'] = str(e)
            logger.error(f"Skills gap analysis failed: {e}")
        
        return analysis_results
    
    def _analyze_department_gaps(self, team_skills: pd.DataFrame, 
                                target_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse les lacunes par département"""
        
        department_gaps = {}
        
        for department in team_skills.get('department', pd.Series()).unique():
            dept_team = team_skills[team_skills['department'] == department] if 'department' in team_skills.columns else team_skills
            dept_requirements = target_requirements.get(department, {})
            
            if not dept_requirements:
                continue
            
            # Compétences actuelles de l'équipe
            current_skills = _self._extract_team_skills(dept_team)
            
            # Compétences requises
            required_skills = dept_requirements.get('required_skills', {})
            
            # Calcul des gaps
            gaps = {}
            coverage = {}
            
            for skill_category, skills_list in required_skills.items():
                category_gaps = []
                category_coverage = 0
                
                for skill in skills_list:
                    required_level = skills_list.get(skill, 3) if isinstance(skills_list, dict) else 3
                    current_level = current_skills.get(skill, 0)
                    
                    if current_level < required_level:
                        gap_severity = required_level - current_level
                        category_gaps.append({
                            'skill': skill,
                            'required_level': required_level,
                            'current_level': current_level,
                            'gap_severity': gap_severity,
                            'priority': _self._calculate_skill_priority(skill, gap_severity, department)
                        })
                    
                    category_coverage += min(current_level / required_level, 1.0)
                
                gaps[skill_category] = category_gaps
                coverage[skill_category] = category_coverage / len(skills_list) if skills_list else 0
            
            department_gaps[department] = {
                'gaps': gaps,
                'coverage': coverage,
                'team_size': len(dept_team),
                'avg_coverage': np.mean(list(coverage.values())) if coverage else 0,
                'critical_gaps_count': sum(len([g for g in cat_gaps if g['gap_severity'] >= 2]) 
                                         for cat_gaps in gaps.values())
            }
        
        return department_gaps
    
    def _extract_team_skills(self, team_df: pd.DataFrame) -> Dict[str, float]:
        """Extrait et agrège les compétences de l'équipe"""
        
        team_skills = {}
        
        # Si colonnes de compétences directes
        skill_columns = [col for col in team_df.columns if 'skill_' in col.lower()]
        
        for col in skill_columns:
            skill_name = col.replace('skill_', '').replace('_', ' ').title()
            team_skills[skill_name] = team_df[col].mean()
        
        # Extraction depuis texte de compétences
        if 'skills' in team_df.columns:
            all_skills_text = ' '.join(team_df['skills'].fillna('').astype(str))
            extracted_skills = _self._extract_skills_from_text(all_skills_text)
            team_skills.update(extracted_skills)
        
        return team_skills
    
    def _extract_skills_from_text(self, skills_text: str) -> Dict[str, float]:
        """Extrait compétences depuis texte avec NLP"""
        
        extracted_skills = {}
        skills_text_lower = skills_text.lower()
        
        # Recherche dans taxonomie gaming
        for department, categories in self.gaming_skills_taxonomy.items():
            for category, skills_list in categories.items():
                for skill in skills_list:
                    skill_lower = skill.lower()
                    # Recherche mentions du skill
                    mentions = len(re.findall(r'\b' + re.escape(skill_lower) + r'\b', skills_text_lower))
                    
                    if mentions > 0:
                        # Score basé sur fréquence et contexte
                        score = min(5, 1 + mentions * 0.5)
                        extracted_skills[skill] = score
        
        return extracted_skills
    
    def _calculate_skill_priority(self, skill: str, gap_severity: float, department: str) -> str:
        """Calcule la priorité d'une lacune de compétence"""
        
        # Compétences critiques par département
        critical_skills = {
            'Programming': ['C++', 'C#', 'Unity', 'Unreal Engine'],
            'Art & Animation': ['3ds Max', 'Maya', 'Substance Painter'],
            'Game Design': ['Game Mechanics', 'Level Design', 'UX/UI'],
            'Quality Assurance': ['Manual Testing', 'Automated Testing'],
            'Production': ['Scrum', 'Agile', 'Project Management']
        }
        
        is_critical = skill in critical_skills.get(department, [])
        
        if gap_severity >= 3 or is_critical:
            return 'Critical'
        elif gap_severity >= 2:
            return 'High'
        elif gap_severity >= 1:
            return 'Medium'
        else:
            return 'Low'
    
    def _identify_priority_gaps(self, gap_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifie les lacunes prioritaires à travers tous les départements"""
        
        all_gaps = []
        
        for department, dept_data in gap_analysis.items():
            for category, gaps_list in dept_data['gaps'].items():
                for gap in gaps_list:
                    all_gaps.append({
                        **gap,
                        'department': department,
                        'category': category,
                        'business_impact': _self._assess_business_impact(
                            gap['skill'], department, gap['gap_severity']
                        )
                    })
        
        # Tri par priorité et impact business
        priority_order = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
        
        all_gaps.sort(key=lambda x: (
            priority_order.get(x['priority'], 0),
            x['business_impact'],
            x['gap_severity']
        ), reverse=True)
        
        return all_gaps[:20]  # Top 20 lacunes prioritaires
    
    def _assess_business_impact(self, skill: str, department: str, gap_severity: float) -> float:
        """Évalue l'impact business d'une lacune de compétence"""
        
        # Impact de base selon le département
        dept_impact = {
            'Programming': 0.9,
            'Game Design': 0.8,
            'Art & Animation': 0.7,
            'Quality Assurance': 0.6,
            'Production': 0.8
        }
        
        base_impact = dept_impact.get(department, 0.5)
        
        # Multiplicateur selon la compétence
        high_impact_skills = [
            'Unity', 'Unreal Engine', 'C++', 'C#', 'Game Mechanics',
            'Level Design', 'Project Management', 'Scrum'
        ]
        
        skill_multiplier = 1.5 if skill in high_impact_skills else 1.0
        
        # Impact final
        return base_impact * skill_multiplier * (gap_severity / 3)
    
    def _identify_team_strengths(self, team_skills: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identifie les forces de l'équipe"""
        
        strengths = []
        team_skills_dict = self._extract_team_skills(team_skills)
        
        # Top compétences de l'équipe
        top_skills = sorted(team_skills_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for skill, level in top_skills:
            if level >= 3.5:  # Seuil de force
                strengths.append({
                    'skill': skill,
                    'level': level,
                    'level_name': self._get_skill_level_name(level),
                    'competitive_advantage': level >= 4.0,
                    'can_mentor': level >= 4.5,
                    'market_differentiation': self._assess_market_rarity(skill)
                })
        
        return strengths
    
    def _get_skill_level_name(self, level: float) -> str:
        """Convertit score numérique en nom de niveau"""
        if level >= 4.5:
            return 'Master'
        elif level >= 3.5:
            return 'Expert'
        elif level >= 2.5:
            return 'Advanced'
        elif level >= 1.5:
            return 'Intermediate'
        else:
            return 'Beginner'
    
    def _assess_market_rarity(self, skill: str) -> str:
        """Évalue la rareté d'une compétence sur le marché"""
        
        rare_skills = [
            'Custom Engine', 'Vulkan', 'VR/AR', 'Machine Learning',
            'Procedural Generation', 'Network Programming'
        ]
        
        common_skills = [
            'Unity', 'Photoshop', 'Manual Testing', 'Agile'
        ]
        
        if skill in rare_skills:
            return 'Rare'
        elif skill in common_skills:
            return 'Common'
        else:
            return 'Moderate'
    
    def _generate_hiring_recommendations(self, gap_analysis: Dict[str, Any],
                                       priority_gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Génère recommandations d'embauche basées sur les lacunes"""
        
        hiring_recs = {
            'immediate_hires': [],
            'planned_hires': [],
            'contractor_needs': [],
            'budget_estimates': {}
        }
        
        # Regroupement des lacunes par département
        dept_gaps = {}
        for gap in priority_gaps:
            dept = gap['department']
            if dept not in dept_gaps:
                dept_gaps[dept] = []
            dept_gaps[dept].append(gap)
        
        # Recommandations par département
        for department, gaps in dept_gaps.items():
            critical_gaps = [g for g in gaps if g['priority'] == 'Critical']
            high_gaps = [g for g in gaps if g['priority'] == 'High']
            
            # Embauches immédiates pour lacunes critiques
            if critical_gaps:
                hiring_recs['immediate_hires'].append({
                    'department': department,
                    'role_type': self._suggest_role_type(critical_gaps),
                    'skills_needed': [g['skill'] for g in critical_gaps[:5]],
                    'urgency': 'Critical',
                    'estimated_time_to_hire': self._estimate_hiring_time(department, critical_gaps),
                    'budget_range': self._estimate_salary_range(department, critical_gaps)
                })
            
            # Embauches planifiées pour lacunes importantes
            if high_gaps:
                hiring_recs['planned_hires'].append({
                    'department': department,
                    'role_type': self._suggest_role_type(high_gaps),
                    'skills_needed': [g['skill'] for g in high_gaps[:5]],
                    'timeline': 'Q2-Q3',
                    'budget_range': self._estimate_salary_range(department, high_gaps)
                })
        
        return hiring_recs
    
    def _suggest_role_type(self, gaps: List[Dict[str, Any]]) -> str:
        """Suggère le type de poste à recruter"""
        
        gap_skills = [g['skill'] for g in gaps]
        
        # Patterns de rôles gaming
        if any(skill in gap_skills for skill in ['C++', 'C#', 'Unity', 'Unreal Engine']):
            return 'Senior Game Programmer'
        elif any(skill in gap_skills for skill in ['3ds Max', 'Maya', 'Substance Painter']):
            return 'Senior 3D Artist'
        elif any(skill in gap_skills for skill in ['Game Mechanics', 'Level Design']):
            return 'Senior Game Designer'
        elif any(skill in gap_skills for skill in ['Manual Testing', 'Automated Testing']):
            return 'QA Lead'
        elif any(skill in gap_skills for skill in ['Scrum', 'Project Management']):
            return 'Production Manager'
        else:
            return 'Specialist'
    
    def _estimate_hiring_time(self, department: str, gaps: List[Dict[str, Any]]) -> str:
        """Estime le temps de recrutement"""
        
        hiring_difficulty = {
            'Programming': 8,  # semaines
            'Art & Animation': 6,
            'Game Design': 6,
            'Quality Assurance': 4,
            'Production': 5
        }
        
        base_time = hiring_difficulty.get(department, 6)
        
        # Ajustement selon rareté des compétences
        rare_skills_count = sum(1 for gap in gaps 
                               if self._assess_market_rarity(gap['skill']) == 'Rare')
        
        if rare_skills_count > 2:
            base_time += 4
        elif rare_skills_count > 0:
            base_time += 2
        
        return f"{base_time}-{base_time + 2} weeks"
    
    def _estimate_salary_range(self, department: str, gaps: List[Dict[str, Any]]) -> str:
        """Estime la fourchette salariale"""
        
        base_salaries = {
            'Programming': (80000, 130000),
            'Art & Animation': (65000, 110000),
            'Game Design': (70000, 120000),
            'Quality Assurance': (50000, 85000),
            'Production': (75000, 125000)
        }
        
        min_sal, max_sal = base_salaries.get(department, (65000, 100000))
        
        # Ajustement selon niveau requis
        avg_gap_severity = np.mean([g['gap_severity'] for g in gaps])
        
        if avg_gap_severity >= 2.5:  # Senior level
            min_sal = int(min_sal * 1.3)
            max_sal = int(max_sal * 1.4)
        elif avg_gap_severity >= 1.5:  # Mid level
            min_sal = int(min_sal * 1.1)
            max_sal = int(max_sal * 1.2)
        
        return f"${min_sal:,} - ${max_sal:,}"
    
    def _generate_training_recommendations(self, gap_analysis: Dict[str, Any],
                                         team_skills: pd.DataFrame) -> Dict[str, Any]:
        """Génère recommandations de formation"""
        
        training_recs = {
            'internal_training': [],
            'external_courses': [],
            'mentorship_programs': [],
            'certification_paths': []
        }
        
        for department, dept_data in gap_analysis.items():
            for category, gaps in dept_data['gaps'].items():
                for gap in gaps:
                    if gap['gap_severity'] <= 2:  # Peut être comblé par formation
                        
                        training_type = self._determine_training_type(gap['skill'], gap['gap_severity'])
                        
                        recommendation = {
                            'skill': gap['skill'],
                            'department': department,
                            'current_level': gap['current_level'],
                            'target_level': gap['required_level'],
                            'duration': self._estimate_training_duration(gap['skill'], gap['gap_severity']),
                            'cost_estimate': self._estimate_training_cost(gap['skill'], training_type),
                            'roi_potential': self._calculate_training_roi(gap)
                        }
                        
                        training_recs[training_type].append(recommendation)
        
        return training_recs
    
    def _determine_training_type(self, skill: str, gap_severity: float) -> str:
        """Détermine le type de formation approprié"""
        
        if gap_severity <= 1:
            return 'internal_training'
        elif skill in ['Unity', 'Unreal Engine', 'Scrum', 'Agile']:
            return 'certification_paths'
        elif gap_severity >= 1.5:
            return 'external_courses'
        else:
            return 'mentorship_programs'
    
    def _build_skill_matrix(self, team_skills: pd.DataFrame) -> Dict[str, Any]:
        """Construit une matrice de compétences de l'équipe"""
        
        if team_skills.empty:
            return {}
        
        # Extraction compétences par personne
        team_matrix = {}
        
        for _, person in team_skills.iterrows():
            person_id = person.get('employee_id', person.get('name', 'Unknown'))
            person_skills = self._extract_person_skills(person)
            
            team_matrix[person_id] = {
                'department': person.get('department', 'Unknown'),
                'experience_years': person.get('years_experience', 0),
                'skills': person_skills,
                'skill_count': len(person_skills),
                'avg_skill_level': np.mean(list(person_skills.values())) if person_skills else 0
            }
        
        # Statistiques globales
        all_skills = {}
        for person_data in team_matrix.values():
            for skill, level in person_data['skills'].items():
                if skill not in all_skills:
                    all_skills[skill] = []
                all_skills[skill].append(level)
        
        skill_stats = {
            skill: {
                'avg_level': np.mean(levels),
                'max_level': max(levels),
                'people_count': len(levels),
                'coverage': len(levels) / len(team_matrix)
            }
            for skill, levels in all_skills.items()
        }
        
        return {
            'team_matrix': team_matrix,
            'skill_statistics': skill_stats,
            'total_people': len(team_matrix),
            'total_unique_skills': len(all_skills)
        }
    
    def _extract_person_skills(self, person_row: pd.Series) -> Dict[str, float]:
        """Extrait les compétences d'une personne"""
        
        person_skills = {}
        
        # Compétences depuis colonnes directes
        skill_columns = [col for col in person_row.index if 'skill_' in col.lower()]
        for col in skill_columns:
            skill_name = col.replace('skill_', '').replace('_', ' ').title()
            person_skills[skill_name] = person_row[col]
        
        # Compétences depuis texte
        if 'skills' in person_row.index and pd.notna(person_row['skills']):
            text_skills = self._extract_skills_from_text(str(person_row['skills']))
            person_skills.update(text_skills)
        
        return person_skills
    
    def render_skills_gap_dashboard(self, analysis_results: Dict[str, Any]):
        """Dashboard Streamlit pour l'analyse des lacunes de compétences"""
        
        st.markdown("## 🎯 Skills Gap Analysis Dashboard")
        st.markdown("*Strategic workforce capability assessment for gaming teams*")
        
        if 'status' in analysis_results and analysis_results['status'] == 'error':
            st.error(f"Analysis failed: {analysis_results.get('message', 'Unknown error')}")
            return
        
        # Vue d'ensemble des lacunes
        gap_analysis = analysis_results.get('gap_analysis', {})
        
        if gap_analysis:
            st.markdown("### 📊 Gap Analysis Overview")
            
            # Métriques principales
            total_gaps = sum(
                dept_data.get('critical_gaps_count', 0) 
                for dept_data in gap_analysis.values()
            )
            
            avg_coverage = np.mean([
                dept_data.get('avg_coverage', 0) 
                for dept_data in gap_analysis.values()
            ])
            
            departments_at_risk = sum(
                1 for dept_data in gap_analysis.values() 
                if dept_data.get('avg_coverage', 0) < 0.7
            )
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "🔴 Critical Gaps",
                    total_gaps,
                    delta=f"{total_gaps - 15}" if total_gaps != 15 else None,
                    delta_color="inverse"
                )
            
            with col2:
                st.metric(
                    "📈 Avg Coverage",
                    f"{avg_coverage:.1%}",
                    delta=f"{(avg_coverage - 0.75):.1%}" if avg_coverage != 0.75 else None
                )
            
            with col3:
                st.metric(
                    "⚠️ Depts at Risk",
                    departments_at_risk,
                    delta_color="inverse"
                )
            
            with col4:
                analyzed_depts = len(gap_analysis)
                st.metric(
                    "🏢 Departments",
                    analyzed_depts
                )
        
        # Lacunes prioritaires
        priority_gaps = analysis_results.get('priority_gaps', [])
        
        if priority_gaps:
            st.markdown("### 🚨 Priority Gaps")
            
            # Top 10 lacunes critiques
            top_gaps = priority_gaps[:10]
            
            gaps_df = pd.DataFrame([{
                'Skill': gap['skill'],
                'Department': gap['department'],
                'Priority': gap['priority'],
                'Gap Severity': gap['gap_severity'],
                'Business Impact': f"{gap['business_impact']:.2f}",
                'Required Level': gap['required_level'],
                'Current Level': gap['current_level']
            } for gap in top_gaps])
            
            # Colorisation par priorité
            def color_priority(val):
                colors = {'Critical': 'background-color: #ffebee', 
                         'High': 'background-color: #fff3e0',
                         'Medium': 'background-color: #f3e5f5'}
                return colors.get(val, '')
            
            styled_df = gaps_df.style.applymap(color_priority, subset=['Priority'])
            st.dataframe(styled_df, use_container_width=True)
        
        # Forces de l'équipe
        team_strengths = analysis_results.get('team_strengths', [])
        
        if team_strengths:
            st.markdown("### 💪 Team Strengths")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Graphique des forces
                strengths_df = pd.DataFrame([{
                    'Skill': strength['skill'],
                    'Level': strength['level'],
                    'Market Rarity': strength['market_differentiation']
                } for strength in team_strengths[:8]])
                
                fig = px.bar(
                    strengths_df,
                    x='Level',
                    y='Skill',
                    color='Market Rarity',
                    orientation='h',
                    title='Top Team Strengths',
                    color_discrete_map={
                        'Rare': '#e74c3c',
                        'Moderate': '#f39c12',
                        'Common': '#27ae60'
                    }
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Liste des forces avec détails
                for strength in team_strengths[:5]:
                    with st.expander(f"💎 {strength['skill']} - {strength['level_name']}"):
                        st.write(f"**Level:** {strength['level']:.1f}/5.0")
                        st.write(f"**Market Rarity:** {strength['market_differentiation']}")
                        
                        if strength['competitive_advantage']:
                            st.success("✅ Competitive Advantage")
                        if strength['can_mentor']:
                            st.info("👨‍🏫 Can Mentor Others")
        
        # Recommandations d'embauche
        hiring_recs = analysis_results.get('hiring_recommendations', {})
        
        if hiring_recs.get('immediate_hires') or hiring_recs.get('planned_hires'):
            st.markdown("### 🎯 Hiring Recommendations")
            
            # Embauches immédiates
            immediate = hiring_recs.get('immediate_hires', [])
            if immediate:
                st.markdown("#### 🚨 Immediate Hires Needed")
                
                for hire in immediate:
                    with st.expander(f"🔥 {hire['role_type']} - {hire['department']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Urgency:** {hire['urgency']}")
                            st.write(f"**Timeline:** {hire['estimated_time_to_hire']}")
                            st.write(f"**Budget:** {hire['budget_range']}")
                        
                        with col2:
                            st.write("**Key Skills Needed:**")
                            for skill in hire['skills_needed']:
                                st.write(f"• {skill}")
            
            # Embauches planifiées
            planned = hiring_recs.get('planned_hires', [])
            if planned:
                st.markdown("#### 📅 Planned Hires")
                
                planned_df = pd.DataFrame([{
                    'Department': hire['department'],
                    'Role Type': hire['role_type'],
                    'Timeline': hire['timeline'],
                    'Budget Range': hire['budget_range'],
                    'Key Skills': ', '.join(hire['skills_needed'][:3])
                } for hire in planned])
                
                st.dataframe(planned_df, use_container_width=True)
        
        # Matrice de compétences
        skill_matrix = analysis_results.get('skill_matrix', {})
        
        if skill_matrix.get('skill_statistics'):
            st.markdown("### 🎪 Skills Matrix Overview")
            
            skill_stats = skill_matrix['skill_statistics']
            
            # Top compétences par couverture équipe
            coverage_data = []
            for skill, stats in list(skill_stats.items())[:15]:
                coverage_data.append({
                    'Skill': skill,
                    'Team Coverage': stats['coverage'],
                    'Average Level': stats['avg_level'],
                    'People Count': stats['people_count']
                })
            
            coverage_df = pd.DataFrame(coverage_data)
            
            fig = px.bubble(
                coverage_df,
                x='Team Coverage',
                y='Average Level',
                size='People Count',
                hover_name='Skill',
                title='Skills Coverage vs Proficiency',
                labels={'Team Coverage': 'Team Coverage (%)', 'Average Level': 'Average Skill Level'}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistiques générales
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("👥 Team Members", skill_matrix['total_people'])
            with col2:
                st.metric("🎯 Unique Skills", skill_matrix['total_unique_skills'])
            with col3:
                avg_skills_per_person = skill_matrix['total_unique_skills'] / skill_matrix['total_people']
                st.metric("📊 Skills/Person", f"{avg_skills_per_person:.1f}")
