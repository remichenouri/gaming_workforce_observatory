"""
Gaming Workforce Observatory - Network Graphs Enterprise
Graphiques réseau pour analyser les connexions entre équipes gaming
"""
import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import community as community_louvain
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

class GamingNetworkGraphs:
    """Graphiques réseau avancés pour analyser les connexions gaming"""
    
    def __init__(self):
        # Couleurs pour différents types de nœuds
        self.node_colors = {
            'Programming': '#3498db',
            'Art & Animation': '#e74c3c',
            'Game Design': '#2ecc71',
            'Quality Assurance': '#f39c12',
            'Production': '#9b59b6',
            'Audio': '#1abc9c',
            'Management': '#34495e'
        }
        
        # Tailles selon la séniorité
        self.seniority_sizes = {
            'Junior': 10,
            'Mid': 15,
            'Senior': 20,
            'Lead': 25,
            'Principal': 30,
            'Director': 35
        }
        
        # Types de connexions
        self.connection_types = {
            'reports_to': {'color': '#34495e', 'width': 3, 'dash': 'solid'},
            'collaborates_with': {'color': '#3498db', 'width': 2, 'dash': 'dot'},
            'mentors': {'color': '#2ecc71', 'width': 2, 'dash': 'dash'},
            'same_project': {'color': '#f39c12', 'width': 1, 'dash': 'solid'},
            'same_team': {'color': '#e74c3c', 'width': 2, 'dash': 'solid'}
        }
    
    def create_team_collaboration_network(self, employee_data: pd.DataFrame,
                                        collaboration_data: pd.DataFrame = None) -> go.Figure:
        """Réseau de collaboration entre équipes gaming"""
        
        if employee_data.empty:
            return self._create_empty_network()
        
        # Création du graphe NetworkX
        G = self._build_collaboration_graph(employee_data, collaboration_data)
        
        if len(G.nodes()) == 0:
            return self._create_empty_network()
        
        # Détection des communautés
        communities = community_louvain.best_partition(G)
        
        # Positionnement des nœuds
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Extraction des edges
        edge_x, edge_y, edge_info = self._extract_edges(G, pos)
        
        # Extraction des nodes
        node_x, node_y, node_info = self._extract_nodes(G, pos, communities, employee_data)
        
        # Création du graphique
        fig = go.Figure()
        
        # Ajout des edges
        for edge_type, edges in edge_info.items():
            if edges['x']:
                connection_style = self.connection_types.get(edge_type, self.connection_types['collaborates_with'])
                
                fig.add_trace(go.Scatter(
                    x=edges['x'], y=edges['y'],
                    mode='lines',
                    line=dict(
                        width=connection_style['width'],
                        color=connection_style['color'],
                        dash=connection_style['dash']
                    ),
                    hoverinfo='none',
                    showlegend=False,
                    name=edge_type
                ))
        
        # Ajout des nodes par département
        for dept, nodes in node_info.items():
            if nodes['x']:
                fig.add_trace(go.Scatter(
                    x=nodes['x'], y=nodes['y'],
                    mode='markers+text',
                    marker=dict(
                        size=nodes['sizes'],
                        color=self.node_colors.get(dept, '#95a5a6'),
                        opacity=0.8,
                        line=dict(width=2, color='white')
                    ),
                    text=nodes['labels'],
                    textposition="middle center",
                    textfont=dict(size=10, color='white'),
                    hovertemplate='<b>%{customdata[0]}</b><br>' +
                                 'Department: %{customdata[1]}<br>' +
                                 'Seniority: %{customdata[2]}<br>' +
                                 'Team: %{customdata[3]}<br>' +
                                 'Connections: %{customdata[4]}<br>' +
                                 '<extra></extra>',
                    customdata=nodes['hover_data'],
                    name=dept
                ))
        
        # Mise en forme
        fig.update_layout(
            title={
                'text': '🕸️ Team Collaboration Network',
                'x': 0.5,
                'font': {'size': 20}
            },
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Node size = seniority level, Colors = departments, Lines = collaboration types",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002 ,
                xanchor='left', yanchor='bottom',
                font=dict(color="gray", size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            height=600
        )
        
        return fig
    
    def _build_collaboration_graph(self, employee_data: pd.DataFrame,
                                  collaboration_data: pd.DataFrame = None) -> nx.Graph:
        """Construit le graphe de collaboration"""
        
        G = nx.Graph()
        
        # Ajout des nœuds (employés)
        for _, employee in employee_data.iterrows():
            employee_id = employee.get('employee_id', employee.get('name', f'emp_{_}'))
            
            G.add_node(employee_id, **{
                'department': employee.get('department', 'Unknown'),
                'seniority': employee.get('experience_level', employee.get('seniority', 'Mid')),
                'team': employee.get('team', employee.get('project_team', 'Team A')),
                'name': employee.get('name', f'Employee {employee_id}'),
                'performance': employee.get('performance_score', 3.0),
                'satisfaction': employee.get('satisfaction_score', 7.0)
            })
        
        # Ajout des edges basés sur les données de collaboration
        if collaboration_data is not None and not collaboration_data.empty:
            self._add_explicit_connections(G, collaboration_data)
        else:
            # Génération de connexions basées sur des heuristiques
            self._add_heuristic_connections(G, employee_data)
        
        return G
    
    def _add_explicit_connections(self, G: nx.Graph, collaboration_data: pd.DataFrame):
        """Ajoute des connexions explicites depuis les données"""
        
        for _, connection in collaboration_data.iterrows():
            source = connection.get('employee_1', connection.get('source'))
            target = connection.get('employee_2', connection.get('target'))
            connection_type = connection.get('connection_type', 'collaborates_with')
            strength = connection.get('strength', connection.get('frequency', 1))
            
            if source in G.nodes() and target in G.nodes():
                G.add_edge(source, target, 
                          connection_type=connection_type,
                          weight=strength)
    
    def _add_heuristic_connections(self, G: nx.Graph, employee_data: pd.DataFrame):
        """Ajoute des connexions basées sur des heuristiques métier"""
        
        nodes_data = {node: data for node, data in G.nodes(data=True)}
        
        # Connexions hiérarchiques (reports_to)
        self._add_hierarchy_connections(G, nodes_data)
        
        # Connexions d'équipe (same_team)
        self._add_team_connections(G, nodes_data)
        
        # Connexions de collaboration inter-départements
        self._add_interdepartment_connections(G, nodes_data)
        
        # Connexions de mentoring
        self._add_mentoring_connections(G, nodes_data)
    
    def _add_hierarchy_connections(self, G: nx.Graph, nodes_data: Dict):
        """Ajoute les connexions hiérarchiques"""
        
        # Hiérarchie gaming typique
        hierarchy_order = ['Junior', 'Mid', 'Senior', 'Lead', 'Principal', 'Director']
        
        for dept in set(data['department'] for data in nodes_data.values()):
            dept_nodes = [(node, data) for node, data in nodes_data.items() 
                         if data['department'] == dept]
            
            # Tri par séniorité
            dept_nodes.sort(key=lambda x: hierarchy_order.index(x[1]['seniority']) 
                          if x[1]['seniority'] in hierarchy_order else 3)
            
            # Connexions hiérarchiques (chaque niveau reporte au suivant)
            for i in range(len(dept_nodes) - 1):
                junior_node, junior_data = dept_nodes[i]
                senior_node, senior_data = dept_nodes[i + 1]
                
                if hierarchy_order.index(junior_data['seniority']) < hierarchy_order.index(senior_data['seniority']):
                    G.add_edge(junior_node, senior_node, 
                              connection_type='reports_to', weight=3)
    
    def _add_team_connections(self, G: nx.Graph, nodes_data: Dict):
        """Ajoute les connexions d'équipe"""
        
        # Groupement par équipe
        teams = {}
        for node, data in nodes_data.items():
            team = data['team']
            if team not in teams:
                teams[team] = []
            teams[team].append(node)
        
        # Connexions intra-équipe
        for team, members in teams.items():
            for i, member1 in enumerate(members):
                for member2 in members[i+1:]:
                    G.add_edge(member1, member2, 
                              connection_type='same_team', weight=2)
    
    def _add_interdepartment_connections(self, G: nx.Graph, nodes_data: Dict):
        """Ajoute les connexions inter-départements"""
        
        # Départements qui collaborent fréquemment dans le gaming
        collaboration_matrix = {
            'Programming': ['Game Design', 'Art & Animation', 'Quality Assurance'],
            'Game Design': ['Programming', 'Art & Animation', 'Production'],
            'Art & Animation': ['Programming', 'Game Design', 'Quality Assurance'],
            'Quality Assurance': ['Programming', 'Art & Animation', 'Production'],
            'Production': ['Game Design', 'Quality Assurance', 'Management']
        }
        
        for dept1, collaborating_depts in collaboration_matrix.items():
            dept1_nodes = [node for node, data in nodes_data.items() 
                          if data['department'] == dept1]
            
            for dept2 in collaborating_depts:
                dept2_nodes = [node for node, data in nodes_data.items() 
                              if data['department'] == dept2]
                
                # Connexions entre départements (sample)
                if dept1_nodes and dept2_nodes:
                    for node1 in dept1_nodes[:2]:  # Limite pour éviter trop de connexions
                        for node2 in dept2_nodes[:2]:
                            if np.random.random() > 0.7:  # 30% de chance de connexion
                                G.add_edge(node1, node2, 
                                          connection_type='collaborates_with', weight=1)
    
    def _add_mentoring_connections(self, G: nx.Graph, nodes_data: Dict):
        """Ajoute les connexions de mentoring"""
        
        hierarchy_order = ['Junior', 'Mid', 'Senior', 'Lead', 'Principal', 'Director']
        
        # Mentoring intra-département
        for dept in set(data['department'] for data in nodes_data.values()):
            dept_nodes = [(node, data) for node, data in nodes_data.items() 
                         if data['department'] == dept]
            
            seniors = [node for node, data in dept_nodes 
                      if data['seniority'] in ['Senior', 'Lead', 'Principal']]
            juniors = [node for node, data in dept_nodes 
                      if data['seniority'] in ['Junior', 'Mid']]
            
            # Chaque senior peut mentorer 1-2 juniors
            for senior in seniors:
                mentees = np.random.choice(juniors, 
                                         size=min(2, len(juniors)), 
                                         replace=False)
                for mentee in mentees:
                    if np.random.random() > 0.8:  # 20% de chance
                        G.add_edge(senior, mentee, 
                                  connection_type='mentors', weight=2)
    
    def _extract_edges(self, G: nx.Graph, pos: Dict) -> Tuple[List, List, Dict]:
        """Extrait les données des edges pour Plotly"""
        
        edge_info = {conn_type: {'x': [], 'y': []} 
                    for conn_type in self.connection_types.keys()}
        edge_info['default'] = {'x': [], 'y': []}
        
        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            connection_type = edge[2].get('connection_type', 'default')
            
            edge_info[connection_type]['x'].extend([x0, x1, None])
            edge_info[connection_type]['y'].extend([y0, y1, None])
        
        return None, None, edge_info
    
    def _extract_nodes(self, G: nx.Graph, pos: Dict, communities: Dict,
                      employee_data: pd.DataFrame) -> Tuple[List, List, Dict]:
        """Extrait les données des nodes pour Plotly"""
        
        node_info = {}
        
        # Groupement par département
        for node, data in G.nodes(data=True):
            dept = data['department']
            
            if dept not in node_info:
                node_info[dept] = {
                    'x': [], 'y': [], 'sizes': [], 'labels': [], 'hover_data': []
                }
            
            x, y = pos[node]
            node_info[dept]['x'].append(x)
            node_info[dept]['y'].append(y)
            
            # Taille basée sur séniorité
            size = self.seniority_sizes.get(data['seniority'], 15)
            node_info[dept]['sizes'].append(size)
            
            # Label court
            name = data['name']
            short_name = name.split()[0] if len(name.split()) > 1 else name[:8]
            node_info[dept]['labels'].append(short_name)
            
            # Données hover
            connections_count = G.degree(node)
            community_id = communities.get(node, 0)
            
            node_info[dept]['hover_data'].append([
                data['name'],
                data['department'],
                data['seniority'], 
                data['team'],
                connections_count
            ])
        
        return None, None, node_info
    
    def create_project_dependency_network(self, projects_data: pd.DataFrame,
                                        dependencies_data: pd.DataFrame = None) -> go.Figure:
        """Réseau de dépendances entre projets gaming"""
        
        if projects_data.empty:
            return self._create_empty_network()
        
        # Création du graphe dirigé
        G = nx.DiGraph()
        
        # Ajout des nœuds (projets)
        for _, project in projects_data.iterrows():
            project_id = project.get('project_id', project.get('name', f'proj_{_}'))
            
            G.add_node(project_id, **{
                'name': project.get('name', project_id),
                'status': project.get('status', 'In Progress'),
                'priority': project.get('priority', 'Medium'),
                'team_size': project.get('team_size', 5),
                'completion': project.get('completion_percentage', 50)
            })
        
        # Ajout des dépendances
        if dependencies_data is not None:
            for _, dep in dependencies_data.iterrows():
                source = dep.get('source_project')
                target = dep.get('dependent_project') 
                dependency_type = dep.get('dependency_type', 'blocks')
                
                if source in G.nodes() and target in G.nodes():
                    G.add_edge(source, target, dependency_type=dependency_type)
        
        # Détection des cycles (problématique dans les dépendances)
        cycles = list(nx.simple_cycles(G))
        
        # Layout hiérarchique
        try:
            pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        except:
            pos = nx.spring_layout(G)
        
        # Création du graphique
        fig = go.Figure()
        
        # Edges (dépendances)
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(width=2, color='#34495e'),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Nœuds (projets)
        node_x, node_y, node_colors, node_sizes, node_text, hover_data = [], [], [], [], [], []
        
        status_colors = {
            'Not Started': '#95a5a6',
            'In Progress': '#3498db', 
            'Blocked': '#e74c3c',
            'Completed': '#27ae60',
            'On Hold': '#f39c12'
        }
        
        for node, data in G.nodes(data=True):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Couleur selon statut
            status = data['status']
            node_colors.append(status_colors.get(status, '#95a5a6'))
            
            # Taille selon équipe
            team_size = data['team_size']
            node_sizes.append(max(15, min(40, team_size * 2)))
            
            # Label
            node_text.append(data['name'][:10])
            
            # Hover data
            dependencies_count = G.degree(node)
            hover_data.append([
                data['name'], status, data['priority'], 
                team_size, f"{data['completion']}%", dependencies_count
            ])
        
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(
                size=node_sizes,
                color=node_colors,
                opacity=0.8,
                line=dict(width=2, color='white')
            ),
            text=node_text,
            textposition="middle center",
            textfont=dict(size=10, color='white'),
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'Status: %{customdata[1]}<br>' +
                         'Priority: %{customdata[2]}<br>' +
                         'Team Size: %{customdata[3]}<br>' +
                         'Completion: %{customdata[4]}<br>' +
                         'Dependencies: %{customdata[5]}<br>' +
                         '<extra></extra>',
            customdata=hover_data,
            showlegend=False
        ))
        
        # Mise en forme
        fig.update_layout(
            title={
                'text': '🎮 Project Dependencies Network',
                'x': 0.5,
                'font': {'size': 20}
            },
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[
                dict(
                    text=f"Detected {len(cycles)} circular dependencies" if cycles else "No circular dependencies detected ✅",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    xanchor='left', yanchor='bottom',
                    font=dict(color="red" if cycles else "green", size=12)
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            height=600
        )
        
        return fig
    
    def create_skills_network(self, employee_data: pd.DataFrame) -> go.Figure:
        """Réseau des compétences partagées entre employés"""
        
        if employee_data.empty or 'skills' not in employee_data.columns:
            return self._create_empty_network()
        
        # Création du graphe bipartite (employés <-> compétences)
        G = nx.Graph()
        
        # Ajout des nœuds employés et compétences
        employees = []
        skills_set = set()
        
        for _, employee in employee_data.iterrows():
            emp_id = employee.get('employee_id', employee.get('name', f'emp_{_}'))
            employees.append(emp_id)
            
            G.add_node(emp_id, 
                      node_type='employee',
                      department=employee.get('department', 'Unknown'),
                      name=employee.get('name', emp_id))
            
            # Extraction des compétences
            skills_text = str(employee.get('skills', ''))
            if skills_text and skills_text != 'nan':
                employee_skills = [s.strip() for s in skills_text.split(',')]
                
                for skill in employee_skills:
                    if skill and len(skill) > 2:  # Filtrer les compétences trop courtes
                        skills_set.add(skill)
                        G.add_node(skill, node_type='skill')
                        G.add_edge(emp_id, skill)
        
        if len(G.nodes()) < 5:
            return self._create_empty_network()
        
        # Layout avec séparation employés/compétences
        pos = self._bipartite_layout(G, employees, list(skills_set))
        
        # Création du graphique
        fig = go.Figure()
        
        # Edges
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(width=1, color='rgba(52, 73, 94, 0.3)'),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Nœuds employés
        emp_x, emp_y, emp_text, emp_hover = [], [], [], []
        for emp in employees:
            if emp in pos:
                x, y = pos[emp]
                emp_x.append(x)
                emp_y.append(y)
                
                emp_data = G.nodes[emp]
                emp_text.append(emp_data['name'][:8])
                
                skills_count = G.degree(emp)
                emp_hover.append([emp_data['name'], emp_data['department'], skills_count])
        
        fig.add_trace(go.Scatter(
            x=emp_x, y=emp_y,
            mode='markers+text',
            marker=dict(
                size=15,
                color='#3498db',
                opacity=0.8,
                line=dict(width=2, color='white')
            ),
            text=emp_text,
            textposition="middle center",
            textfont=dict(size=8, color='white'),
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'Department: %{customdata[1]}<br>' +
                         'Skills Count: %{customdata[2]}<br>' +
                         '<extra></extra>',
            customdata=emp_hover,
            name='Employees'
        ))
        
        # Nœuds compétences  
        skill_x, skill_y, skill_text, skill_hover = [], [], [], []
        for skill in skills_set:
            if skill in pos:
                x, y = pos[skill]
                skill_x.append(x)
                skill_y.append(y)
                
                skill_text.append(skill[:10])
                
                employees_with_skill = G.degree(skill)
                skill_hover.append([skill, employees_with_skill])
        
        fig.add_trace(go.Scatter(
            x=skill_x, y=skill_y,
            mode='markers+text',
            marker=dict(
                size=12,
                color='#e74c3c',
                opacity=0.8,
                symbol='diamond',
                line=dict(width=2, color='white')
            ),
            text=skill_text,
            textposition="middle center",
            textfont=dict(size=8, color='white'),
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'Employees with skill: %{customdata[1]}<br>' +
                         '<extra></extra>',
            customdata=skill_hover,
            name='Skills'
        ))
        
        # Mise en forme
        fig.update_layout(
            title={
                'text': '🎪 Skills Sharing Network',
                'x': 0.5,
                'font': {'size': 20}
            },
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            height=600
        )
        
        return fig
    
    def _bipartite_layout(self, G: nx.Graph, employees: List, skills: List) -> Dict:
        """Layout spécialisé pour graphe bipartite employés-compétences"""
        
        pos = {}
        
        # Positionnement des employés (côté gauche)
        emp_y_positions = np.linspace(0, 1, len(employees))
        for i, emp in enumerate(employees):
            if emp in G.nodes():
                pos[emp] = (0, emp_y_positions[i])
        
        # Positionnement des compétences (côté droit)
        skill_y_positions = np.linspace(0, 1, len(skills))
        for i, skill in enumerate(skills):
            if skill in G.nodes():
                pos[skill] = (1, skill_y_positions[i])
        
        return pos
    
    def _create_empty_network(self) -> go.Figure:
        """Crée un graphique vide en cas d'absence de données"""
        
        fig = go.Figure()
        
        fig.update_layout(
            title={
                'text': '🕸️ Network Graph - No Data Available',
                'x': 0.5,
                'font': {'size': 18}
            },
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        fig.add_annotation(
            text="No network data available for visualization",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        
        return fig
    
    def analyze_network_metrics(self, G: nx.Graph) -> Dict[str, Any]:
        """Analyse les métriques du réseau"""
        
        if len(G.nodes()) == 0:
            return {'status': 'empty_network'}
        
        metrics = {
            'basic_metrics': {
                'nodes_count': len(G.nodes()),
                'edges_count': len(G.edges()),
                'density': nx.density(G),
                'average_clustering': nx.average_clustering(G)
            },
            'centrality_metrics': {},
            'community_metrics': {},
            'connectivity_metrics': {}
        }
        
        # Métriques de centralité
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        closeness_centrality = nx.closeness_centrality(G)
        
        # Top 5 nœuds par centralité
        metrics['centrality_metrics'] = {
            'top_degree': sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5],
            'top_betweenness': sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5],
            'top_closeness': sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        }
        
        # Détection de communautés
        if len(G.nodes()) > 5:
            communities = community_louvain.best_partition(G)
            community_sizes = {}
            for node, community in communities.items():
                community_sizes[community] = community_sizes.get(community, 0) + 1
            
            metrics['community_metrics'] = {
                'community_count': len(set(communities.values())),
                'modularity': community_louvain.modularity(communities, G),
                'community_sizes': community_sizes
            }
        
        # Métriques de connectivité
        if nx.is_connected(G):
            metrics['connectivity_metrics'] = {
                'is_connected': True,
                'diameter': nx.diameter(G),
                'average_path_length': nx.average_shortest_path_length(G)
            }
        else:
            components = list(nx.connected_components(G))
            metrics['connectivity_metrics'] = {
                'is_connected': False,
                'connected_components': len(components),
                'largest_component_size': len(max(components, key=len))
            }
        
        return metrics
    
    def render_network_dashboard(self, employee_data: pd.DataFrame,
                               collaboration_data: Optional[pd.DataFrame] = None,
                               projects_data: Optional[pd.DataFrame] = None):
        """Dashboard complet des graphiques réseau"""
        
        st.markdown("## 🕸️ Network Analysis Dashboard")
        st.markdown("*Interactive network graphs showing connections and relationships in gaming teams*")
        
        # Sélecteur de type de réseau
        network_type = st.selectbox(
            "Choose Network Type:",
            ["Team Collaboration", "Project Dependencies", "Skills Network"],
            index=0
        )
        
        # Affichage selon le type sélectionné
        if network_type == "Team Collaboration":
            fig = self.create_team_collaboration_network(employee_data, collaboration_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Analyse des métriques si données disponibles
            if not employee_data.empty:
                G = self._build_collaboration_graph(employee_data, collaboration_data)
                metrics = self.analyze_network_metrics(G)
                
                if metrics.get('status') != 'empty_network':
                    st.markdown("### 📊 Network Metrics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    basic_metrics = metrics['basic_metrics']
                    with col1:
                        st.metric("👥 Nodes", basic_metrics['nodes_count'])
                    with col2:
                        st.metric("🔗 Connections", basic_metrics['edges_count'])
                    with col3:
                        st.metric("📈 Density", f"{basic_metrics['density']:.3f}")
                    with col4:
                        st.metric("🌐 Clustering", f"{basic_metrics['average_clustering']:.3f}")
        
        elif network_type == "Project Dependencies" and projects_data is not None:
            fig = self.create_project_dependency_network(projects_data)
            st.plotly_chart(fig, use_container_width=True)
        
        elif network_type == "Skills Network":
            fig = self.create_skills_network(employee_data)
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info(f"Network type '{network_type}' requires additional data that is not currently available.")
