"""
Gaming Workforce Observatory - Cache Manager Enterprise
Système de cache intelligent multi-niveaux avec stratégies d'éviction
"""
import streamlit as st
import redis
import pickle
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, List
import pandas as pd
from functools import wraps
import threading
import time

logger = logging.getLogger(__name__)

class CacheManager:
    """Gestionnaire de cache enterprise avec Redis et fallback mémoire"""
    
    def __init__(self):
        self.local_cache = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
        self.max_local_cache_size = 1000
        self.default_ttl = 3600  # 1 heure
        
        # Configuration Redis
        try:
            self.redis_client = redis.Redis(
                host=st.secrets.get("REDIS_HOST", "localhost"),
                port=st.secrets.get("REDIS_PORT", 6379),
                db=st.secrets.get("REDIS_DB", 0),
                decode_responses=False
            )
            self.redis_available = self.redis_client.ping()
            logger.info("Redis cache connected successfully")
        except:
            self.redis_client = None
            self.redis_available = False
            logger.warning("Redis not available, using local cache only")
    
    def _generate_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Génère une clé de cache unique"""
        key_data = f"{func_name}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache (Redis puis local)"""
        # Essayer Redis d'abord
        if self.redis_available:
            try:
                data = self.redis_client.get(f"gaming_cache:{key}")
                if data:
                    self.cache_stats['hits'] += 1
                    return pickle.loads(data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
        
        # Fallback cache local
        if key in self.local_cache:
            cache_entry = self.local_cache[key]
            if datetime.now() < cache_entry['expires_at']:
                self.cache_stats['hits'] += 1
                return cache_entry['value']
            else:
                del self.local_cache[key]
                self.cache_stats['evictions'] += 1
        
        self.cache_stats['misses'] += 1
        return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Stocke une valeur dans le cache"""
        ttl = ttl or self.default_ttl
        
        # Stocker dans Redis
        if self.redis_available:
            try:
                serialized_value = pickle.dumps(value)
                self.redis_client.setex(f"gaming_cache:{key}", ttl, serialized_value)
            except Exception as e:
                logger.error(f"Redis set error: {e}")
        
        # Stocker dans cache local
        if len(self.local_cache) >= self.max_local_cache_size:
            self._evict_oldest_local()
        
        self.local_cache[key] = {
            'value': value,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=ttl)
        }
        
        return True
    
    def delete(self, key: str) -> bool:
        """Supprime une clé du cache"""
        deleted = False
        
        # Supprimer de Redis
        if self.redis_available:
            try:
                deleted = bool(self.redis_client.delete(f"gaming_cache:{key}"))
            except Exception as e:
                logger.error(f"Redis delete error: {e}")
        
        # Supprimer du cache local
        if key in self.local_cache:
            del self.local_cache[key]
            deleted = True
        
        return deleted
    
    def clear_all(self) -> bool:
        """Nettoie tout le cache"""
        # Nettoyer Redis
        if self.redis_available:
            try:
                keys = self.redis_client.keys("gaming_cache:*")
                if keys:
                    self.redis_client.delete(*keys)
            except Exception as e:
                logger.error(f"Redis clear error: {e}")
        
        # Nettoyer cache local
        self.local_cache.clear()
        return True
    
    def _evict_oldest_local(self):
        """Évince l'entrée la plus ancienne du cache local"""
        if not self.local_cache:
            return
        
        oldest_key = min(self.local_cache.keys(), 
                        key=lambda k: self.local_cache[k]['created_at'])
        del self.local_cache[oldest_key]
        self.cache_stats['evictions'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'evictions': self.cache_stats['evictions'],
            'hit_rate': hit_rate,
            'local_cache_size': len(self.local_cache),
            'redis_available': self.redis_available
        }

# Décorateur pour cache automatique
def cached_function(ttl: int = 3600, key_prefix: str = ""):
    """Décorateur pour mise en cache automatique des fonctions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_manager = st.session_state.get('cache_manager')
            if not cache_manager:
                cache_manager = CacheManager()
                st.session_state['cache_manager'] = cache_manager
            
            # Génération clé cache
            cache_key = f"{key_prefix}{func.__name__}:{hashlib.md5(str((args, kwargs)).encode()).hexdigest()}"
            
            # Tentative récupération cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Exécution fonction et mise en cache
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Cache spécialisé pour données gaming
class GamingDataCache:
    """Cache spécialisé pour les données gaming avec invalidation intelligente"""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager
        self.gaming_cache_keys = set()
    
    @cached_function(ttl=3600, key_prefix="gaming_salary_")
    def get_salary_data(self, department: str, region: str) -> pd.DataFrame:
        """Cache des données de salaire gaming"""
        # Simulation - remplacer par vraie logique
        return pd.DataFrame({
            'department': [department] * 100,
            'region': [region] * 100,
            'salary': range(50000, 150000, 1000)
        })
    
    @cached_function(ttl=7200, key_prefix="gaming_studio_")
    def get_studio_data(self, studio_name: str) -> Dict[str, Any]:
        """Cache des données de studios gaming"""
        return {
            'name': studio_name,
            'employees': 1000,
            'avg_salary': 95000,
            'retention_rate': 0.85
        }
    
    def invalidate_gaming_cache(self, pattern: str = "gaming_*"):
        """Invalide le cache gaming selon un pattern"""
        if self.cache_manager.redis_available:
            try:
                keys = self.cache_manager.redis_client.keys(f"gaming_cache:{pattern}")
                if keys:
                    self.cache_manager.redis_client.delete(*keys)
            except Exception as e:
                logger.error(f"Cache invalidation error: {e}")
        
        # Invalidation cache local
        keys_to_delete = [k for k in self.cache_manager.local_cache.keys() if pattern.replace('*', '') in k]
        for key in keys_to_delete:
            del self.cache_manager.local_cache[key]
