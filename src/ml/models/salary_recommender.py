"""
Gaming Workforce Observatory - Salary Recommender Enterprise
Système de recommandation salariale basé sur ML avec benchmarking marché
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import streamlit as st
import plotly.express as px
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GamingSalaryRecommender:
    """Recommandeur de salaires gaming avec ML et benchmarking marché"""
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = StandardScaler()
        self.encoders = {}
        self.feature_columns = [
            'experience_years', 'department_encoded', 'location_encoded',
            'company_size_encoded', 'skills_score', 'performance_score',
            'education_level', 'certifications_count', 'leadership_experience',
            'remote_flexibility', 'equity_preference', 'market_demand_score'
        ]
        
        # Benchmarks marché gaming
        self.market_benchmarks = {
            'Programming': {'junior': 75000, 'mid': 110000, 'senior': 155000},
            'Game Design': {'junior': 65000, 'mid': 95000, 'senior': 140000},
            'Art & Animation': {'junior': 55000, 'mid': 85000, 'senior': 125000},
            'Quality Assurance': {'junior': 45000, 'mid': 70000, 'senior': 95000},
            'Production': {'junior': 70000, 'mid': 105000, 'senior': 160000}
        }
    
    @st.cache_data(ttl=7200)
    def train_salary_models(_self, salary_data: pd.DataFrame) -> Dict[str, Any]:
        """Entraîne les modèles de recommandation salariale"""
        
        training_results = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'data_shape': salary_data.shape,
            'model_performances': {},
            'feature_importance': {},
            'market_analysis': {}
        }
        
        try:
            # Préparation des features
            X, y = _self._prepare_salary_features(salary_data)
            
            if X is None or y is None:
                training_results['status'] = 'error'
                training_results['message'] = 'Feature preparation failed'
                return training_results
            
            # Division des données
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Définition des modèles
            _self.models = {
                'random_forest': RandomForestRegressor(
                    n_estimators=200, max_depth=15, min_samples_split=5,
                    random_state=42, n_jobs=-1
                ),
                'gradient_boosting': GradientBoostingRegressor(
                    n_estimators=150, max_depth=8, learning_rate=0.1,
                    random_state=42
                ),
                'linear_regression': LinearRegression()
            }
            
            # Entraînement et évaluation
            for model_name, model in _self.models.items():
                logger.info(f"Training salary model: {model_name}")
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                # Métriques
                mae = mean_absolute_error(y_test, y_pred)
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                # Validation croisée
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_absolute_error')
                
                training_results['model_performances'][model_name] = {
                    'mae': mae,
                    'mse': mse,
                    'rmse': np.sqrt(mse),
                    'r2_score': r2,
                    'cv_mae_mean': -cv_scores.mean(),
                    'cv_mae_std': cv_scores.std()
                }
                
                logger.info(f"{model_name} - MAE: ${mae:,.0f}, R²: {r2:.3f}")
            
            # Sélection meilleur modèle (plus faible MAE)
            best_model_name = min(
                training_results['model_performances'].keys(),
                key=lambda x: training_results['model_performances'][x]['mae']
            )
            
            _self.best_model = _self.models[best_model_name]
            _self.best_model_name = best_model_name
            
            # Feature importance
            if hasattr(_self.best_model, 'feature_importances_'):
                feature_importance = dict(zip(
                    _self.feature_columns,
                    _self.best_model.feature_importances_
                ))
                training_results['feature_importance'] = feature_importance
            
            training_results['status'] = 'success'
            training_results['best_model'] = best_model_name
            
            logger.info(f"Salary model training completed. Best model: {best_model_name}")
            
        except Exception as e:
            training_results['status'] = 'error'
            training_results['message'] = str(e)
            logger.error(f"Salary model training failed: {e}")
        
        return training_results
    
    def _prepare_salary_features(self, data: pd.DataFrame) -> tuple:
        """Prépare les features pour l'entraînement des modèles salariaux"""
        
        if 'salary_usd' not in data.columns:
            logger.error("Target column 'salary_usd' not found")
            return None, None
        
        # Nettoyage des données
        data_clean = data.dropna(subset=['salary_usd'])
        data_clean = data_clean[
            (data_clean['salary_usd'] >= 30000) & 
            (data_clean['salary_usd'] <= 400000)
        ]
        
        # Engineering des features
        data_enhanced = self._engineer_salary_features(data_clean)
        
        # Encodage des variables catégorielles
        data_encoded = self._encode_salary_features(data_enhanced)
        
        # Sélection des features disponibles
        available_features = [col for col in self.feature_columns if col in data_encoded.columns]
        
        if len(available_features) < 3:
            logger.error(f"Insufficient features: {len(available_features)}")
            return None, None
        
        X = data_encoded[available_features]
        y = data_encoded['salary_usd']
        
        # Normalisation des features numériques
        numeric_features = X.select_dtypes(include=[np.number]).columns
        X[numeric_features] = self.scaler.fit_transform(X[numeric_features])
        
        self.feature_columns = available_features
        return X, y
    
    def _engineer_salary_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Ingénierie de features spécifiques aux salaires gaming"""
        
        data_enhanced = data.copy()
        
        # Score de compétences basé sur les skills listées
        if 'skills' in data.columns:
            gaming_skills = [
                'Unity', 'Unreal Engine', 'C#', 'C++', 'Python', 'JavaScript',
                'Maya', 'Blender', '3D Modeling', 'Animation', 'Photoshop',
                'Game Design', 'Level Design', 'UI/UX', 'Mobile Development'
            ]
            
            data_enhanced['skills_score'] = data['skills'].apply(
                lambda x: len([skill for skill in gaming_skills if skill.lower() in str(x).lower()]) 
                if pd.notna(x) else 0
            ) / len(gaming_skills) * 100
        else:
            data_enhanced['skills_score'] = 50  # Score neutre
        
        # Niveau d'éducation numérique
        if 'education' in data.columns:
            education_mapping = {
                'High School': 1, 'Associate': 2, 'Bachelor': 3, 
                'Master': 4, 'PhD': 5, 'Bootcamp': 2.5
            }
            data_enhanced['education_level'] = data['education'].map(education_mapping).fillna(3)
        else:
            data_enhanced['education_level'] = 3
        
        # Nombre de certifications
        if 'certifications' in data.columns:
            data_enhanced['certifications_count'] = data['certifications'].apply(
                lambda x: len(str(x).split(',')) if pd.notna(x) and str(x) != '' else 0
            )
        else:
            data_enhanced['certifications_count'] = 0
        
        # Expérience en leadership
        if 'role' in data.columns:
            leadership_keywords = ['lead', 'senior', 'principal', 'director', 'manager']
            data_enhanced['leadership_experience'] = data['role'].apply(
                lambda x: any(keyword in str(x).lower() for keyword in leadership_keywords)
                if pd.notna(x) else False
            ).astype(int)
        else:
            data_enhanced['leadership_experience'] = 0
        
        # Préférence pour l'equity
        if 'equity_value_usd' in data.columns:
            data_enhanced['equity_preference'] = (data['equity_value_usd'] > 0).astype(int)
        else:
            data_enhanced['equity_preference'] = 0
        
        # Score de demande du marché (basé sur département et expérience)
        if 'department' in data.columns and 'experience_years' in data.columns:
            demand_scores = {
                'Programming': 0.9, 'Game Design': 0.7, 'Art & Animation': 0.6,
                'Quality Assurance': 0.4, 'Production': 0.8, 'Audio': 0.5
            }
            
            base_demand = data['department'].map(demand_scores).fillna(0.5)
            experience_multiplier = np.minimum(data['experience_years'] / 10, 1.5)
            data_enhanced['market_demand_score'] = base_demand * experience_multiplier
        else:
            data_enhanced['market_demand_score'] = 0.5
        
        # Valeurs par défaut pour features manquantes
        default_values = {
            'performance_score': 3.5,
            'remote_flexibility': 0.5,
            'experience_years': 3
        }
        
        for feature, default_val in default_values.items():
            if feature not in data_enhanced.columns:
                data_enhanced[feature] = default_val
        
        return data_enhanced
    
    def _encode_salary_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Encode les features catégorielles pour les salaires"""
        
        data_encoded = data.copy()
        
        # Encodage département
        if 'department' in data.columns:
            dept_mapping = {
                'Programming': 5, 'Production': 4, 'Game Design': 3,
                'Art & Animation': 2, 'Audio': 2, 'Quality Assurance': 1,
                'Marketing': 2, 'Management': 4
            }
            data_encoded['department_encoded'] = data['department'].map(dept_mapping).fillna(2)
        
        # Encodage localisation (coût de la vie)
        if 'location' in data.columns:
            location_mapping = self._create_location_cost_mapping(data['location'])
            data_encoded['location_encoded'] = data['location'].map(location_mapping).fillna(2)
        
        # Encodage taille d'entreprise
        if 'company_size' in data.columns:
            size_mapping = {
                'Startup (1-50)': 1, 'Small (51-200)': 2, 'Medium (201-1000)': 3,
                'Large (1001-5000)': 4, 'Enterprise (5000+)': 5
            }
            data_encoded['company_size_encoded'] = data['company_size'].map(size_mapping).fillna(3)
        else:
            data_encoded['company_size_encoded'] = 3
        
        return data_encoded
    
    def _create_location_cost_mapping(self, locations: pd.Series) -> Dict[str, int]:
        """Crée un mapping coût de la vie par location"""
        
        high_cost_cities = [
            'san francisco', 'new york', 'london', 'zurich', 'singapore',
            'los angeles', 'seattle', 'boston'
        ]
        
        medium_cost_cities = [
            'toronto', 'berlin', 'amsterdam', 'paris', 'tokyo',
            'chicago', 'washington dc', 'austin'
        ]
        
        mapping = {}
        for location in locations.dropna().unique():
            location_lower = str(location).lower()
            
            if any(city in location_lower for city in high_cost_cities):
                mapping[location] = 4  # Coût élevé
            elif any(city in location_lower for city in medium_cost_cities):
                mapping[location] = 3  # Coût moyen-élevé
            elif 'remote' in location_lower:
                mapping[location] = 2  # Remote
            else:
                mapping[location] = 2  # Coût moyen/faible
        
        return mapping
    
    def recommend_salary(self, candidate_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Recommande un salaire pour un profil candidat"""
        
        if not self.best_model:
            return {'error': 'Model not trained yet'}
        
        try:
            # Préparation du profil
            profile_df = pd.DataFrame([candidate_profile])
            profile_enhanced = self._engineer_salary_features(profile_df)
            profile_encoded = self._encode_salary_features(profile_enhanced)
            
            # Sélection des features
            available_features = [col for col in self.feature_columns if col in profile_encoded.columns]
            X_candidate = profile_encoded[available_features]
            
            # Normalisation
            numeric_features = X_candidate.select_dtypes(include=[np.number]).columns
            X_candidate[numeric_features] = self.scaler.transform(X_candidate[numeric_features])
            
            # Prédiction
            predicted_salary = self.best_model.predict(X_candidate)[0]
            
            # Comparaison avec benchmarks marché
            market_comparison = self._compare_with_market(candidate_profile, predicted_salary)
            
            # Fourchette de négociation
            salary_range = self._calculate_salary_range(predicted_salary, candidate_profile)
            
            # Recommandations personnalisées
            recommendations = self._generate_salary_recommendations(
                candidate_profile, predicted_salary, market_comparison
            )
            
            result = {
                'predicted_salary': round(predicted_salary, -3),  # Arrondi au millier
                'salary_range': salary_range,
                'market_comparison': market_comparison,
                'confidence_level': self._calculate_prediction_confidence(X_candidate),
                'recommendations': recommendations,
                'model_used': self.best_model_name,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            logger.info(f"Salary recommendation generated: ${predicted_salary:,.0f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Salary recommendation error: {e}")
            return {'error': f'Recommendation failed: {str(e)}'}
    
    def _compare_with_market(self, profile: Dict[str, Any], predicted_salary: float) -> Dict[str, Any]:
        """Compare avec les benchmarks marché"""
        
        department = profile.get('department', 'Programming')
        experience_years = profile.get('experience_years', 3)
        
        # Détermination du niveau d'expérience
        if experience_years < 2:
            level = 'junior'
        elif experience_years < 7:
            level = 'mid'
        else:
            level = 'senior'
        
        # Benchmark marché
        market_benchmarks = self.market_benchmarks.get(department, self.market_benchmarks['Programming'])
        market_salary = market_benchmarks.get(level, market_benchmarks['mid'])
        
        # Comparaison
        difference = predicted_salary - market_salary
        difference_pct = (difference / market_salary) * 100
        
        # Classification
        if difference_pct > 15:
            position = "Above Market"
            color = "#27ae60"
        elif difference_pct < -15:
            position = "Below Market"
            color = "#e74c3c"
        else:
            position = "Market Competitive"
            color = "#f39c12"
        
        return {
            'market_salary': market_salary,
            'predicted_salary': predicted_salary,
            'difference': difference,
            'difference_percentage': difference_pct,
            'market_position': position,
            'position_color': color,
            'benchmark_level': level
        }
    
    def _calculate_salary_range(self, predicted_salary: float, profile: Dict[str, Any]) -> Dict[str, float]:
        """Calcule une fourchette de négociation"""
        
        # Variance basée sur l'expérience et le département
        experience_years = profile.get('experience_years', 3)
        department = profile.get('department', 'Programming')
        
        # Variance de base
        base_variance = 0.15  # ±15%
        
        # Ajustements
        if experience_years > 10:
            base_variance += 0.05  # Plus de flexibilité pour seniors
        
        if department in ['Programming', 'Production']:
            base_variance += 0.03  # Départements haute demande
        
        # Calcul de la fourchette
        variance_amount = predicted_salary * base_variance
        
        return {
            'minimum': round(predicted_salary - variance_amount, -3),
            'target': round(predicted_salary, -3),
            'maximum': round(predicted_salary + variance_amount, -3),
            'variance_percentage': base_variance * 100
        }
    
    def _generate_salary_recommendations(self, profile: Dict[str, Any], 
                                       predicted_salary: float,
                                       market_comparison: Dict[str, Any]) -> List[Dict[str, str]]:
        """Génère des recommandations salariales personnalisées"""
        
        recommendations = []
        
        # Recommandations basées sur la position marché
        market_position = market_comparison['market_position']
        
        if market_position == "Below Market":
            recommendations.append({
                'category': 'Market Positioning',
                'title': 'Négocier à la hausse',
                'description': f'Votre profil mérite ${market_comparison["market_salary"]:,.0f} selon le marché',
                'action': 'Présenter des benchmarks salariaux lors de négociations'
            })
        
        elif market_position == "Above Market":
            recommendations.append({
                'category': 'Value Proposition',
                'title': 'Justifier la valeur ajoutée',
                'description': 'Salaire au-dessus du marché, mettre en avant compétences uniques',
                'action': 'Préparer portfolio et résultats mesurables'
            })
        
        # Recommandations basées sur l'expérience
        experience = profile.get('experience_years', 3)
        
        if experience < 2:
            recommendations.append({
                'category': 'Career Development',
                'title': 'Focus apprentissage et croissance',
                'description': 'Négocier formations, mentoring et plan de carrière',
                'action': 'Privilégier opportunités d\'apprentissage'
            })
        
        elif experience > 8:
            recommendations.append({
                'category': 'Leadership Premium',
                'title': 'Valoriser expertise leadership',
                'description': 'Demander prime pour responsabilités d\'encadrement',
                'action': 'Négocier bonus basé sur performance équipe'
            })
        
        # Recommandations par département
        department = profile.get('department', 'Programming')
        
        if department == 'Programming':
            recommendations.append({
                'category': 'Tech Skills Premium',
                'title': 'Négocier prime compétences techniques',
                'description': 'Département haute demande, négocier sur compétences spécialisées',
                'action': 'Mettre en avant certifications et projets techniques'
            })
        
        return recommendations[:4]  # Limiter à 4 recommandations
    
    def _calculate_prediction_confidence(self, X: pd.DataFrame) -> str:
        """Calcule le niveau de confiance de la prédiction"""
        
        # Score basé sur la disponibilité des features importantes
        important_features = ['experience_years', 'department_encoded', 'skills_score']
        available_important = sum(1 for feat in important_features if feat in X.columns)
        
        confidence_score = available_important / len(important_features)
        
        if confidence_score >= 0.8:
            return "High"
        elif confidence_score >= 0.6:
            return "Medium"
        else:
            return "Low"
    
    def batch_salary_analysis(self, candidates_df: pd.DataFrame) -> pd.DataFrame:
        """Analyse salariale en lot"""
        
        if not self.best_model:
            raise ValueError("Model not trained yet")
        
        results = []
        
        for _, candidate in candidates_df.iterrows():
            candidate_dict = candidate.to_dict()
            recommendation = self.recommend_salary(candidate_dict)
            
            if 'error' not in recommendation:
                results.append({
                    'candidate_id': candidate_dict.get('candidate_id', ''),
                    'predicted_salary': recommendation['predicted_salary'],
                    'market_position': recommendation['market_comparison']['market_position'],
                    'confidence_level': recommendation['confidence_level'],
                    'min_range': recommendation['salary_range']['minimum'],
                    'max_range': recommendation['salary_range']['maximum']
                })
        
        return pd.DataFrame(results)
