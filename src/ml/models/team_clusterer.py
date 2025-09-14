"""
Gaming Workforce Observatory - Team Clusterer Enterprise
Clustering avancé des équipes gaming avec analyse de performance
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.decomposition import PCA
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class GamingTeamClusterer:
    """Clustering avancé des équipes gaming avec analyse performance"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.clustering_models = {}
        self.best_clustering = None
        self.feature_columns = [
            'avg_performance_score', 'avg_satisfaction_score', 'team_size',
            'avg_experience_years', 'diversity_index', 'avg_salary',
            'retention_rate', 'project_completion_rate', 'innovation_score',
            'collaboration_score', 'neurodiversity_percentage'
        ]
        
        self.cluster_profiles = {}
    
    @st.cache_data(ttl=3600)
    def perform_team_clustering(_self, teams_df: pd.DataFrame, 
                               n_clusters_range: Tuple[int, int] = (3, 8)) -> Dict[str, Any]:
        """Effectue le clustering des équipes avec optimisation automatique"""
        
        clustering_results = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'data_shape': teams_df.shape,
            'clustering_analysis': {},
            'optimal_clusters': {},
            'cluster_profiles': {},
            'performance_metrics': {}
        }
        
        try:
            # Préparation des données
            X = _self._prepare_clustering_features(teams_df)
            
            if X is None:
                clustering_results['status'] = 'error'
                clustering_results['message'] = 'Feature preparation failed'
                return clustering_results
            
            # Test différents algorithmes et nombres de clusters
            algorithms = {
                'kmeans': KMeans,
                'agglomerative': AgglomerativeClustering
            }
            
            best_score = -1
            best_config = None
            
            for algo_name, AlgoClass in algorithms.items():
                for n_clusters in range(n_clusters_range[0], n_clusters_range[1] + 1):
                    try:
                        if algo_name == 'kmeans':
                            model = AlgoClass(n_clusters=n_clusters, random_state=42, n_init=10)
                        else:
                            model = AlgoClass(n_clusters=n_clusters)
                        
                        cluster_labels = model.fit_predict(X)
                        
                        # Métriques de qualité
                        silhouette = silhouette_score(X, cluster_labels)
                        calinski = calinski_harabasz_score(X, cluster_labels)
                        
                        # Score composite
                        composite_score = (silhouette + calinski / 1000) / 2
                        
                        clustering_results['clustering_analysis'][f'{algo_name}_{n_clusters}'] = {
                            'algorithm': algo_name,
                            'n_clusters': n_clusters,
                            'silhouette_score': silhouette,
                            'calinski_harabasz_score': calinski,
                            'composite_score': composite_score
                        }
                        
                        if composite_score > best_score:
                            best_score = composite_score
                            best_config = {
                                'algorithm': algo_name,
                                'n_clusters': n_clusters,
                                'model': model,
                                'labels': cluster_labels
                            }
                    
                    except Exception as e:
                        logger.warning(f"Clustering failed for {algo_name}_{n_clusters}: {e}")
                        continue
            
            if best_config:
                _self.best_clustering = best_config
                
                # Ajout des labels au DataFrame
                teams_clustered = teams_df.copy()
                teams_clustered['cluster_label'] = best_config['labels']
                
                # Analyse des profils de clusters
                cluster_profiles = _self._analyze_cluster_profiles(teams_clustered)
                _self.cluster_profiles = cluster_profiles
                
                clustering_results['optimal_clusters'] = {
                    'algorithm': best_config['algorithm'],
                    'n_clusters': best_config['n_clusters'],
                    'silhouette_score': silhouette_score(X, best_config['labels']),
                    'calinski_harabasz_score': calinski_harabasz_score(X, best_config['labels'])
                }
                
                clustering_results['cluster_profiles'] = cluster_profiles
                clustering_results['performance_metrics'] = _self._calculate_cluster_performance_metrics(teams_clustered)
                clustering_results['status'] = 'success'
                
                logger.info(f"Team clustering completed: {best_config['algorithm']} with {best_config['n_clusters']} clusters")
            
            else:
                clustering_results['status'] = 'error'
                clustering_results['message'] = 'No successful clustering configuration found'
        
        except Exception as e:
            clustering_results['status'] = 'error'
            clustering_results['message'] = str(e)
            logger.error(f"Team clustering failed: {e}")
        
        return clustering_results
    
    def _prepare_clustering_features(self, teams_df: pd.DataFrame) -> Optional[np.ndarray]:
        """Prépare les features pour le clustering"""
        
        # Vérification des colonnes minimales requises
        required_columns = ['team_size', 'avg_performance_score', 'avg_satisfaction_score']
        missing_columns = [col for col in required_columns if col not in teams_df.columns]
        
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return None
        
        # Engineering des features
        teams_enhanced = self._engineer_team_features(teams_df)
        
        # Sélection des features disponibles
        available_features = [col for col in self.feature_columns if col in teams_enhanced.columns]
        
        if len(available_features) < 3:
            logger.error(f"Insufficient features for clustering: {len(available_features)}")
            return None
        
        X = teams_enhanced[available_features].fillna(teams_enhanced[available_features].mean())
        
        # Normalisation
        X_scaled = self.scaler.fit_transform(X)
        
        self.feature_columns = available_features
        logger.info(f"Clustering features prepared: {len(available_features)} features")
        
        return X_scaled
    
    def _engineer_team_features(self, teams_df: pd.DataFrame) -> pd.DataFrame:
        """Ingénierie de features spécifiques aux équipes gaming"""
        
        teams_enhanced = teams_df.copy()
        
        # Index de diversité (basé sur la distribution des rôles/niveaux)
        if 'roles_distribution' in teams_df.columns:
            teams_enhanced['diversity_index'] = teams_df['roles_distribution'].apply(
                lambda x: self._calculate_diversity_index(x) if pd.notna(x) else 0.5
            )
        else:
            teams_enhanced['diversity_index'] = 0.5
        
        # Score d'innovation (basé sur projets innovants ou brevets)
        if 'innovative_projects_count' in teams_df.columns:
            max_projects = teams_df['innovative_projects_count'].max()
            teams_enhanced['innovation_score'] = teams_df['innovative_projects_count'] / max_projects if max_projects > 0 else 0
        else:
            teams_enhanced['innovation_score'] = 0.5
        
        # Score de collaboration (basé sur feedback inter-équipes)
        if 'cross_team_collaboration' in teams_df.columns:
            teams_enhanced['collaboration_score'] = teams_df['cross_team_collaboration']
        else:
            teams_enhanced['collaboration_score'] = 0.7
        
        # Pourcentage de neurodiversité
        if 'neurodiverse_members' in teams_df.columns and 'team_size' in teams_df.columns:
            teams_enhanced['neurodiversity_percentage'] = (
                teams_df['neurodiverse_members'] / teams_df['team_size'] * 100
            ).fillna(0)
        else:
            teams_enhanced['neurodiversity_percentage'] = 0
        
        # Taux de rétention
        if 'members_left_last_year' in teams_df.columns:
            teams_enhanced['retention_rate'] = (
                (teams_df['team_size'] - teams_df['members_left_last_year']) / teams_df['team_size'] * 100
            ).clip(0, 100)
        else:
            teams_enhanced['retention_rate'] = 85  # Valeur par défaut
        
        # Taux de completion de projets
        if 'completed_projects' in teams_df.columns and 'total_projects' in teams_df.columns:
            teams_enhanced['project_completion_rate'] = (
                teams_df['completed_projects'] / teams_df['total_projects']
            ).fillna(0.8)
        else:
            teams_enhanced['project_completion_rate'] = 0.8
        
        # Features manquantes avec valeurs par défaut
        default_features = {
            'avg_experience_years': 4.5,
            'avg_salary': 85000
        }
        
        for feature, default_value in default_features.items():
            if feature not in teams_enhanced.columns:
                teams_enhanced[feature] = default_value
        
        return teams_enhanced
    
    def _calculate_diversity_index(self, roles_distribution: Any) -> float:
        """Calcule un index de diversité des rôles dans l'équipe"""
        
        if isinstance(roles_distribution, str):
            try:
                roles_dict = eval(roles_distribution)  # Attention: en production, utiliser json.loads
            except:
                return 0.5
        elif isinstance(roles_distribution, dict):
            roles_dict = roles_distribution
        else:
            return 0.5
        
        if not roles_dict:
            return 0.5
        
        # Calcul index Shannon (diversité)
        total = sum(roles_dict.values())
        if total == 0:
            return 0.5
        
        shannon_index = -sum(
            (count / total) * np.log(count / total) 
            for count in roles_dict.values() if count > 0
        )
        
        # Normalisation (max théorique pour les équipes gaming ~2.5)
        return min(shannon_index / 2.5, 1.0)
    
    def _analyze_cluster_profiles(self, teams_clustered: pd.DataFrame) -> Dict[str, Any]:
        """Analyse les profils des clusters identifiés"""
        
        cluster_profiles = {}
        
        for cluster_id in teams_clustered['cluster_label'].unique():
            cluster_teams = teams_clustered[teams_clustered['cluster_label'] == cluster_id]
            
            # Statistiques descriptives
            numeric_columns = cluster_teams.select_dtypes(include=[np.number]).columns
            stats = cluster_teams[numeric_columns].describe()
            
            # Identification du profil type
            profile_characteristics = self._identify_cluster_characteristics(cluster_teams)
            
            cluster_profiles[f'Cluster_{cluster_id}'] = {
                'team_count': len(cluster_teams),
                'percentage_of_total': len(cluster_teams) / len(teams_clustered) * 100,
                'avg_metrics': {
                    'performance_score': cluster_teams['avg_performance_score'].mean(),
                    'satisfaction_score': cluster_teams['avg_satisfaction_score'].mean(),
                    'team_size': cluster_teams['team_size'].mean(),
                    'retention_rate': cluster_teams['retention_rate'].mean(),
                    'innovation_score': cluster_teams['innovation_score'].mean()
                },
                'characteristics': profile_characteristics,
                'representative_teams': self._find_representative_teams(cluster_teams)
            }
        
        return cluster_profiles
    
    def _identify_cluster_characteristics(self, cluster_teams: pd.DataFrame) -> Dict[str, str]:
        """Identifie les caractéristiques principales d'un cluster"""
        
        characteristics = {}
        
        # Analyse de la performance
        avg_performance = cluster_teams['avg_performance_score'].mean()
        if avg_performance >= 4.2:
            characteristics['performance'] = "High Performers"
        elif avg_performance >= 3.5:
            characteristics['performance'] = "Average Performers"
        else:
            characteristics['performance'] = "Needs Improvement"
        
        # Analyse de la taille
        avg_size = cluster_teams['team_size'].mean()
        if avg_size >= 15:
            characteristics['size'] = "Large Teams"
        elif avg_size >= 8:
            characteristics['size'] = "Medium Teams"
        else:
            characteristics['size'] = "Small Teams"
        
        # Analyse de la satisfaction
        avg_satisfaction = cluster_teams['avg_satisfaction_score'].mean()
        if avg_satisfaction >= 8:
            characteristics['satisfaction'] = "Highly Satisfied"
        elif avg_satisfaction >= 6:
            characteristics['satisfaction'] = "Moderately Satisfied"
        else:
            characteristics['satisfaction'] = "Low Satisfaction"
        
        # Analyse de l'innovation
        avg_innovation = cluster_teams['innovation_score'].mean()
        if avg_innovation >= 0.7:
            characteristics['innovation'] = "Highly Innovative"
        elif avg_innovation >= 0.4:
            characteristics['innovation'] = "Moderately Innovative"
        else:
            characteristics['innovation'] = "Traditional Approach"
        
        # Analyse de la rétention
        avg_retention = cluster_teams['retention_rate'].mean()
        if avg_retention >= 90:
            characteristics['retention'] = "Excellent Retention"
        elif avg_retention >= 75:
            characteristics['retention'] = "Good Retention"
        else:
            characteristics['retention'] = "Retention Issues"
        
        return characteristics
    
    def _find_representative_teams(self, cluster_teams: pd.DataFrame, n_representatives: int = 3) -> List[Dict]:
        """Trouve les équipes les plus représentatives du cluster"""
        
        if 'team_name' not in cluster_teams.columns:
            return []
        
        # Calcul du centre du cluster
        numeric_features = [col for col in self.feature_columns if col in cluster_teams.columns]
        cluster_center = cluster_teams[numeric_features].mean()
        
        # Distance euclidienne de chaque équipe au centre
        distances = []
        for idx, team in cluster_teams.iterrows():
            team_values = team[numeric_features]
            distance = np.sqrt(sum((team_values - cluster_center) ** 2))
            distances.append((idx, distance, team['team_name']))
        
        # Tri par distance croissante
        distances.sort(key=lambda x: x[1])
        
        # Sélection des plus représentatives
        representatives = []
        for i in range(min(n_representatives, len(distances))):
            idx, distance, team_name = distances[i]
            team_data = cluster_teams.loc[idx]
            
            representatives.append({
                'team_name': team_name,
                'distance_to_center': distance,
                'performance_score': team_data.get('avg_performance_score', 0),
                'satisfaction_score': team_data.get('avg_satisfaction_score', 0),
                'team_size': team_data.get('team_size', 0)
            })
        
        return representatives
    
    def _calculate_cluster_performance_metrics(self, teams_clustered: pd.DataFrame) -> Dict[str, Any]:
        """Calcule les métriques de performance par cluster"""
        
        performance_metrics = {}
        
        for cluster_id in teams_clustered['cluster_label'].unique():
            cluster_teams = teams_clustered[teams_clustered['cluster_label'] == cluster_id]
            
            # Métriques de performance
            metrics = {
                'avg_performance': cluster_teams['avg_performance_score'].mean(),
                'performance_std': cluster_teams['avg_performance_score'].std(),
                'top_performers_percentage': (cluster_teams['avg_performance_score'] >= 4.5).sum() / len(cluster_teams) * 100,
                'avg_satisfaction': cluster_teams['avg_satisfaction_score'].mean(),
                'satisfaction_std': cluster_teams['avg_satisfaction_score'].std(),
                'high_satisfaction_percentage': (cluster_teams['avg_satisfaction_score'] >= 8).sum() / len(cluster_teams) * 100,
                'avg_retention': cluster_teams['retention_rate'].mean(),
                'low_retention_teams': (cluster_teams['retention_rate'] < 75).sum()
            }
            
            # Classification du cluster
            if metrics['avg_performance'] >= 4.2 and metrics['avg_satisfaction'] >= 7.5:
                cluster_classification = "Star Performers"
            elif metrics['avg_performance'] >= 3.8 and metrics['avg_satisfaction'] >= 7:
                cluster_classification = "Solid Contributors"
            elif metrics['avg_performance'] < 3.5 or metrics['avg_satisfaction'] < 6:
                cluster_classification = "Needs Attention"
            else:
                cluster_classification = "Average Performance"
            
            performance_metrics[f'Cluster_{cluster_id}'] = {
                **metrics,
                'classification': cluster_classification,
                'team_count': len(cluster_teams)
            }
        
        return performance_metrics
    
    def detect_team_outliers(self, teams_df: pd.DataFrame) -> Dict[str, Any]:
        """Détecte les équipes aberrantes avec DBSCAN"""
        
        X = self._prepare_clustering_features(teams_df)
        
        if X is None:
            return {'status': 'error', 'message': 'Feature preparation failed'}
        
        # DBSCAN pour détecter les outliers
        dbscan = DBSCAN(eps=0.5, min_samples=3)
        outlier_labels = dbscan.fit_predict(X)
        
        # Identification des outliers (label = -1)
        outlier_indices = np.where(outlier_labels == -1)[0]
        
        outliers_analysis = {
            'outlier_count': len(outlier_indices),
            'outlier_percentage': len(outlier_indices) / len(teams_df) * 100,
            'outlier_teams': [],
            'outlier_characteristics': {}
        }
        
        if len(outlier_indices) > 0 and 'team_name' in teams_df.columns:
            outlier_teams = teams_df.iloc[outlier_indices]
            
            for idx in outlier_indices:
                team_data = teams_df.iloc[idx]
                outliers_analysis['outlier_teams'].append({
                    'team_name': team_data.get('team_name', f'Team_{idx}'),
                    'performance_score': team_data.get('avg_performance_score', 0),
                    'satisfaction_score': team_data.get('avg_satisfaction_score', 0),
                    'team_size': team_data.get('team_size', 0),
                    'retention_rate': team_data.get('retention_rate', 0)
                })
            
            # Caractéristiques communes des outliers
            outliers_analysis['outlier_characteristics'] = {
                'avg_performance': outlier_teams['avg_performance_score'].mean(),
                'avg_satisfaction': outlier_teams['avg_satisfaction_score'].mean(),
                'avg_team_size': outlier_teams['team_size'].mean(),
                'avg_retention': outlier_teams['retention_rate'].mean()
            }
        
        return outliers_analysis
    
    def recommend_team_improvements(self, teams_clustered: pd.DataFrame) -> Dict[str, List[Dict]]:
        """Recommande des améliorations par cluster"""
        
        recommendations = {}
        
        for cluster_id in teams_clustered['cluster_label'].unique():
            cluster_teams = teams_clustered[teams_clustered['cluster_label'] == cluster_id]
            cluster_recs = []
            
            # Analyse des points faibles
            avg_performance = cluster_teams['avg_performance_score'].mean()
            avg_satisfaction = cluster_teams['avg_satisfaction_score'].mean()
            avg_retention = cluster_teams['retention_rate'].mean()
            
            # Recommandations basées sur la performance
            if avg_performance < 3.5:
                cluster_recs.append({
                    'category': 'Performance',
                    'priority': 'High',
                    'title': 'Améliorer la performance d\'équipe',
                    'description': 'Performance en dessous des standards',
                    'actions': [
                        'Formation compétences techniques',
                        'Coaching individuel',
                        'Révision des processus'
                    ]
                })
            
            # Recommandations basées sur la satisfaction
            if avg_satisfaction < 6:
                cluster_recs.append({
                    'category': 'Employee Satisfaction',
                    'priority': 'High',
                    'title': 'Améliorer la satisfaction équipe',
                    'description': 'Satisfaction employés faible',
                    'actions': [
                        'Enquête satisfaction détaillée',
                        'Amélioration environnement travail',
                        'Révision charge de travail'
                    ]
                })
            
            # Recommandations basées sur la rétention
            if avg_retention < 75:
                cluster_recs.append({
                    'category': 'Retention',
                    'priority': 'Critical',
                    'title': 'Adresser problèmes de rétention',
                    'description': 'Taux de rétention préoccupant',
                    'actions': [
                        'Entretiens de sortie approfondis',
                        'Plan de rétention personnalisé',
                        'Révision compensation et avantages'
                    ]
                })
            
            recommendations[f'Cluster_{cluster_id}'] = cluster_recs
        
        return recommendations
    
    def render_clustering_dashboard(self, clustering_results: Dict[str, Any],
                                  teams_df: pd.DataFrame):
        """Affiche le dashboard de clustering des équipes"""
        
        st.markdown("## 👥 Team Clustering Analysis")
        
        if not clustering_results or clustering_results.get('status') != 'success':
            st.error("No clustering results available")
            return
        
        # Métriques principales
        optimal = clustering_results['optimal_clusters']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Algorithm", optimal['algorithm'].title())
        with col2:
            st.metric("📊 Clusters", optimal['n_clusters'])
        with col3:
            st.metric("🔍 Silhouette Score", f"{optimal['silhouette_score']:.3f}")
        with col4:
            st.metric("📈 Calinski-Harabasz", f"{optimal['calinski_harabasz_score']:.0f}")
        
        # Visualisation des clusters
        if self.best_clustering:
            st.markdown("### 📊 Cluster Visualization")
            
            # Réduction dimensionnelle pour visualisation
            X = self._prepare_clustering_features(teams_df)
            if X is not None:
                pca = PCA(n_components=2)
                X_pca = pca.fit_transform(X)
                
                cluster_df = pd.DataFrame({
                    'PC1': X_pca[:, 0],
                    'PC2': X_pca[:, 1],
                    'Cluster': [f'Cluster {label}' for label in self.best_clustering['labels']],
                    'Team': teams_df['team_name'] if 'team_name' in teams_df.columns else [f'Team {i}' for i in range(len(teams_df))],
                    'Performance': teams_df['avg_performance_score'] if 'avg_performance_score' in teams_df.columns else [3.5] * len(teams_df)
                })
                
                fig = px.scatter(
                    cluster_df,
                    x='PC1',
                    y='PC2',
                    color='Cluster',
                    size='Performance',
                    hover_data=['Team'],
                    title='Team Clusters Visualization (PCA)',
                    width=800,
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Profils des clusters
        st.markdown("### 📋 Cluster Profiles")
        
        cluster_profiles = clustering_results.get('cluster_profiles', {})
        
        for cluster_name, profile in cluster_profiles.items():
            with st.expander(f"🏷️ {cluster_name} ({profile['team_count']} teams)"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Key Metrics:**")
                    metrics = profile['avg_metrics']
                    st.write(f"• Performance: {metrics['performance_score']:.2f}")
                    st.write(f"• Satisfaction: {metrics['satisfaction_score']:.2f}")
                    st.write(f"• Team Size: {metrics['team_size']:.1f}")
                    st.write(f"• Retention: {metrics['retention_rate']:.1f}%")
                
                with col2:
                    st.markdown("**Characteristics:**")
                    chars = profile['characteristics']
                    for key, value in chars.items():
                        st.write(f"• {key.title()}: {value}")
        
        # Recommandations
        recommendations = self.recommend_team_improvements(
            teams_df.copy().assign(cluster_label=self.best_clustering['labels'])
        )
        
        if recommendations:
            st.markdown("### 💡 Improvement Recommendations")
            
            for cluster_name, recs in recommendations.items():
                if recs:  # Seulement si il y a des recommandations
                    st.markdown(f"#### {cluster_name}")
                    
                    for rec in recs:
                        priority_color = {'High': '🔴', 'Critical': '⚠️', 'Medium': '🟡', 'Low': '🟢'}
                        
                        st.markdown(f"""
                        **{priority_color.get(rec['priority'], '📋')} {rec['title']}**
                        
                        {rec['description']}
                        
                        **Actions recommandées:**
                        """ + '\n'.join([f"• {action}" for action in rec['actions']]))
