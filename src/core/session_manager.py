"""
Gaming Workforce Observatory - Session Manager Enterprise
Gestion avancée de l'état utilisateur avec persistance et sécurité
"""
import streamlit as st
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Gestionnaire de session enterprise avec sécurité et audit"""
    
    def __init__(self):
        self.session = st.session_state
        self.session_timeout = timedelta(hours=8)
        
    def initialize_session(self):
        """Initialisation complète de la session utilisateur"""
        # Identifiant unique de session
        if 'session_id' not in self.session:
            self.session['session_id'] = self._generate_session_id()
            self.session['session_start'] = datetime.now()
            logger.info(f"New session created: {self.session['session_id']}")
        
        # Données utilisateur
        if 'user_profile' not in self.session:
            self.session['user_profile'] = {
                'role': 'HR Analyst',
                'department': 'Human Resources',
                'permissions': ['read', 'analyze'],
                'preferences': {}
            }
        
        # Filtres et état de l'application
        if 'app_filters' not in self.session:
            self.session['app_filters'] = {
                'selected_departments': [],
                'date_range': None,
                'experience_levels': [],
                'regions': []
            }
        
        # Cache de données
        if 'data_cache' not in self.session:
            self.session['data_cache'] = {}
        
        # Audit trail
        if 'audit_log' not in self.session:
            self.session['audit_log'] = []
            
        # Vérification timeout
        self._check_session_timeout()
    
    def _generate_session_id(self) -> str:
        """Génère un identifiant unique de session"""
        timestamp = datetime.now().isoformat()
        random_data = st.secrets.get("SESSION_SALT", "default_salt") + timestamp
        return hashlib.sha256(random_data.encode()).hexdigest()[:16]
    
    def _check_session_timeout(self):
        """Vérifie et gère l'expiration de session"""
        if 'session_start' in self.session:
            session_duration = datetime.now() - self.session['session_start']
            if session_duration > self.session_timeout:
                self.clear_session()
                st.warning("Session expired. Please refresh the page.")
                st.stop()
    
    def update_user_activity(self, action: str, details: Dict[str, Any] = None):
        """Met à jour l'activité utilisateur pour audit"""
        activity_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session.get('session_id'),
            'action': action,
            'details': details or {},
            'user_agent': st.context.headers.get('User-Agent', 'Unknown')
        }
        
        if 'audit_log' not in self.session:
            self.session['audit_log'] = []
        
        self.session['audit_log'].append(activity_entry)
        
        # Garder seulement les 100 dernières entrées
        if len(self.session['audit_log']) > 100:
            self.session['audit_log'] = self.session['audit_log'][-100:]
    
    def set_user_preference(self, key: str, value: Any):
        """Définit une préférence utilisateur"""
        if 'user_profile' not in self.session:
            self.session['user_profile'] = {}
        if 'preferences' not in self.session['user_profile']:
            self.session['user_profile']['preferences'] = {}
            
        self.session['user_profile']['preferences'][key] = value
        self.update_user_activity('preference_updated', {'key': key, 'value': str(value)})
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """Récupère une préférence utilisateur"""
        return self.session.get('user_profile', {}).get('preferences', {}).get(key, default)
    
    def set_app_filter(self, filter_name: str, value: Any):
        """Définit un filtre de l'application"""
        if 'app_filters' not in self.session:
            self.session['app_filters'] = {}
        
        self.session['app_filters'][filter_name] = value
        self.update_user_activity('filter_applied', {'filter': filter_name, 'value': str(value)})
    
    def get_app_filter(self, filter_name: str, default: Any = None) -> Any:
        """Récupère un filtre de l'application"""
        return self.session.get('app_filters', {}).get(filter_name, default)
    
    def cache_data(self, key: str, data: Any, ttl_seconds: int = 3600):
        """Met en cache des données avec TTL"""
        if 'data_cache' not in self.session:
            self.session['data_cache'] = {}
        
        cache_entry = {
            'data': data,
            'timestamp': datetime.now(),
            'ttl_seconds': ttl_seconds
        }
        
        self.session['data_cache'][key] = cache_entry
        
        # Nettoyage du cache expiré
        self._cleanup_expired_cache()
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """Récupère des données du cache si valides"""
        if 'data_cache' not in self.session:
            return None
        
        cache_entry = self.session['data_cache'].get(key)
        if not cache_entry:
            return None
        
        # Vérification expiration
        cache_age = datetime.now() - cache_entry['timestamp']
        if cache_age.seconds > cache_entry['ttl_seconds']:
            del self.session['data_cache'][key]
            return None
        
        return cache_entry['data']
    
    def _cleanup_expired_cache(self):
        """Nettoie le cache expiré"""
        if 'data_cache' not in self.session:
            return
        
        current_time = datetime.now()
        expired_keys = []
        
        for key, entry in self.session['data_cache'].items():
            cache_age = current_time - entry['timestamp']
            if cache_age.seconds > entry['ttl_seconds']:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.session['data_cache'][key]
    
    def get_session_info(self) -> Dict[str, Any]:
        """Retourne les informations de session pour debug"""
        return {
            'session_id': self.session.get('session_id'),
            'session_start': self.session.get('session_start'),
            'user_profile': self.session.get('user_profile'),
            'active_filters': len(self.session.get('app_filters', {})),
            'cached_items': len(self.session.get('data_cache', {})),
            'audit_entries': len(self.session.get('audit_log', []))
        }
    
    def export_session_data(self) -> str:
        """Exporte les données de session en JSON"""
        session_data = {
            'session_info': self.get_session_info(),
            'user_preferences': self.session.get('user_profile', {}).get('preferences', {}),
            'applied_filters': self.session.get('app_filters', {}),
            'recent_activity': self.session.get('audit_log', [])[-10:]  # 10 dernières activités
        }
        
        return json.dumps(session_data, indent=2, default=str)
    
    def clear_session(self):
        """Nettoie complètement la session"""
        keys_to_keep = ['session_id']  # Garder l'ID pour audit
        keys_to_clear = [key for key in self.session.keys() if key not in keys_to_keep]
        
        for key in keys_to_clear:
            del self.session[key]
        
        logger.info(f"Session cleared: {self.session.get('session_id')}")
    
    def render_session_debug_panel(self):
        """Panel de debug pour développement"""
        if st.secrets.get("DEBUG", False):
            with st.expander("🔍 Session Debug Panel"):
                session_info = self.get_session_info()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.json(session_info)
                
                with col2:
                    if st.button("Clear Cache"):
                        self.session['data_cache'] = {}
                        st.success("Cache cleared")
                    
                    if st.button("Export Session"):
                        session_json = self.export_session_data()
                        st.download_button(
                            "Download Session Data",
                            session_json,
                            file_name=f"session_{self.session.get('session_id')}.json",
                            mime="application/json"
                        )
