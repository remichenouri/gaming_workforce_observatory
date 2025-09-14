"""
Gaming Workforce Observatory - LinkedIn API Connector
Extraction données emploi et salaires industrie gaming via LinkedIn API
"""
import requests
import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from ..processors.salary_processor import SalaryProcessor

logger = logging.getLogger(__name__)

class LinkedInAPIConnector:
    """Connecteur API LinkedIn pour données emploi gaming"""
    
    def __init__(self):
        self.client_id = st.secrets.get("LINKEDIN_CLIENT_ID")
        self.client_secret = st.secrets.get("LINKEDIN_CLIENT_SECRET")
        self.access_token = None
        self.base_url = "https://api.linkedin.com/v2"
        self.rate_limit_remaining = 500
        self.rate_limit_reset = datetime.now()
        
    def authenticate(self) -> bool:
        """Authentification OAuth2 LinkedIn"""
        if not self.client_id or not self.client_secret:
            logger.error("LinkedIn credentials not configured")
            return False
        
        auth_url = "https://www.linkedin.com/oauth/v2/accessToken"
        
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'r_organization_social r_organization_admin'
        }
        
        try:
            response = requests.post(auth_url, data=payload)
            if response.status_code == 200:
                auth_data = response.json()
                self.access_token = auth_data.get('access_token')
                logger.info("LinkedIn authentication successful")
                return True
            else:
                logger.error(f"LinkedIn auth failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"LinkedIn auth error: {e}")
            return False
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Effectue une requête API avec gestion rate limiting"""
        if not self.access_token:
            if not self.authenticate():
                return None
        
        # Vérification rate limit
        if self.rate_limit_remaining <= 10 and datetime.now() < self.rate_limit_reset:
            wait_time = (self.rate_limit_reset - datetime.now()).seconds
            logger.info(f"Rate limit reached, waiting {wait_time} seconds")
            time.sleep(wait_time)
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", 
                                  headers=headers, params=params)
            
            # Mise à jour rate limit
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            reset_time = response.headers.get('X-RateLimit-Reset')
            if reset_time:
                self.rate_limit_reset = datetime.fromtimestamp(int(reset_time))
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"LinkedIn API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"LinkedIn request error: {e}")
            return None
    
    def search_gaming_jobs(self, keywords: List[str] = None, 
                          location: str = None, limit: int = 100) -> List[Dict]:
        """Recherche offres d'emploi gaming"""
        keywords = keywords or ["game developer", "game designer", "gaming", "unity", "unreal"]
        
        params = {
            'keywords': ' OR '.join(keywords),
            'locationName': location,
            'count': min(limit, 50),  # LinkedIn limite à 50 par requête
            'facets': 'industry:(96)'  # Code industrie gaming
        }
        
        jobs_data = []
        
        try:
            response = self._make_request('/jobSearch', params)
            if response and 'elements' in response:
                for job in response['elements']:
                    job_info = self._extract_job_info(job)
                    if job_info:
                        jobs_data.append(job_info)
            
            logger.info(f"Retrieved {len(jobs_data)} gaming jobs from LinkedIn")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Gaming jobs search error: {e}")
            return []
    
    def _extract_job_info(self, job_data: Dict) -> Optional[Dict]:
        """Extrait informations pertinentes d'une offre d'emploi"""
        try:
            return {
                'job_id': job_data.get('id'),
                'title': job_data.get('title', ''),
                'company': job_data.get('companyDetails', {}).get('company', {}).get('name', ''),
                'location': job_data.get('formattedLocation', ''),
                'posted_date': job_data.get('listedAt'),
                'description': job_data.get('description', {}).get('text', ''),
                'experience_level': self._extract_experience_level(job_data),
                'salary_range': self._extract_salary_info(job_data),
                'skills': self._extract_skills(job_data),
                'department': self._classify_gaming_department(job_data.get('title', '')),
                'source': 'linkedin',
                'retrieved_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Job info extraction error: {e}")
            return None
    
    def _extract_experience_level(self, job_data: Dict) -> str:
        """Détermine le niveau d'expérience requis"""
        title = job_data.get('title', '').lower()
        description = job_data.get('description', {}).get('text', '').lower()
        
        if 'senior' in title or 'lead' in title or '5+ years' in description:
            return 'Senior'
        elif 'junior' in title or 'entry' in title or '0-2 years' in description:
            return 'Junior'
        elif 'principal' in title or 'director' in title:
            return 'Principal'
        else:
            return 'Mid'
    
    def _extract_salary_info(self, job_data: Dict) -> Optional[Dict]:
        """Extrait informations de salaire si disponibles"""
        # LinkedIn ne fournit pas toujours les salaires
        # Implémentation basique pour extraction du texte
        description = job_data.get('description', {}).get('text', '').lower()
        
        salary_info = None
        # Patterns de recherche de salaires
        import re
        
        # Recherche patterns comme "$80,000 - $120,000", "80k-120k", etc.
        salary_patterns = [
            r'\$(\d{1,3}(?:,\d{3})*)\s*-\s*\$(\d{1,3}(?:,\d{3})*)',
            r'(\d{1,3})k\s*-\s*(\d{1,3})k',
            r'salary.*?\$(\d{1,3}(?:,\d{3})*)'
        ]
        
        for pattern in salary_patterns:
            matches = re.search(pattern, description)
            if matches:
                if len(matches.groups()) == 2:
                    salary_info = {
                        'min_salary': int(matches.group(1).replace(',', '')),
                        'max_salary': int(matches.group(2).replace(',', '')),
                        'currency': 'USD'
                    }
                break
        
        return salary_info
    
    def _extract_skills(self, job_data: Dict) -> List[str]:
        """Extrait les compétences mentionnées"""
        description = job_data.get('description', {}).get('text', '').lower()
        
        # Compétences gaming communes
        gaming_skills = [
            'unity', 'unreal engine', 'c#', 'c++', 'python', 'javascript',
            'maya', 'blender', '3ds max', 'photoshop', 'substance painter',
            'git', 'perforce', 'agile', 'scrum', 'multiplayer', 'mobile',
            'console', 'vr', 'ar', 'ai', 'gameplay programming', 'shaders'
        ]
        
        found_skills = []
        for skill in gaming_skills:
            if skill in description:
                found_skills.append(skill.title())
        
        return found_skills
    
    def _classify_gaming_department(self, job_title: str) -> str:
        """Classifie le poste dans un département gaming"""
        title_lower = job_title.lower()
        
        if any(keyword in title_lower for keyword in ['programmer', 'developer', 'engineer', 'coding']):
            return 'Programming'
        elif any(keyword in title_lower for keyword in ['artist', '3d', 'animator', 'visual']):
            return 'Art & Animation'
        elif any(keyword in title_lower for keyword in ['designer', 'game design', 'level design']):
            return 'Game Design'
        elif any(keyword in title_lower for keyword in ['qa', 'test', 'quality assurance']):
            return 'Quality Assurance'
        elif any(keyword in title_lower for keyword in ['producer', 'product manager', 'project']):
            return 'Production'
        elif any(keyword in title_lower for keyword in ['audio', 'sound', 'music']):
            return 'Audio'
        elif any(keyword in title_lower for keyword in ['marketing', 'community', 'social']):
            return 'Marketing'
        else:
            return 'Other'
    
    def get_company_insights(self, company_name: str) -> Optional[Dict]:
        """Récupère des insights sur une entreprise gaming"""
        params = {
            'q': 'universalName',
            'universalName': company_name.lower().replace(' ', '')
        }
        
        try:
            response = self._make_request('/organizations', params)
            if response and 'elements' in response:
                company_data = response['elements'][0] if response['elements'] else None
                if company_data:
                    return self._extract_company_info(company_data)
        except Exception as e:
            logger.error(f"Company insights error: {e}")
        
        return None
    
    def _extract_company_info(self, company_data: Dict) -> Dict:
        """Extrait informations entreprise"""
        return {
            'name': company_data.get('localizedName', ''),
            'description': company_data.get('localizedDescription', ''),
            'industry': company_data.get('localizedIndustry', ''),
            'size': company_data.get('staffCountRange', {}).get('end', 0),
            'founded': company_data.get('foundedOn', {}).get('year'),
            'headquarters': company_data.get('locations', {}).get('headquarters', {}),
            'website': company_data.get('localizedWebsite', ''),
            'logo_url': company_data.get('logoV2', {}).get('original', ''),
            'follower_count': company_data.get('followersCount', 0)
        }
    
    def get_gaming_salary_trends(self, timeframe_months: int = 12) -> pd.DataFrame:
        """Analyse tendances salaires gaming sur période donnée"""
        # Implémentation simplifiée - LinkedIn ne fournit pas directement ces données
        # Dans un cas réel, il faudrait combiner plusieurs requêtes et faire de l'analyse
        
        sample_data = []
        for i in range(timeframe_months):
            month_date = datetime.now() - timedelta(days=30*i)
            sample_data.append({
                'month': month_date.strftime('%Y-%m'),
                'avg_salary_programming': 95000 + (i * 500),
                'avg_salary_art': 75000 + (i * 300),
                'avg_salary_design': 85000 + (i * 400),
                'avg_salary_qa': 55000 + (i * 200),
                'job_postings_count': 450 + (i * 20),
                'source': 'linkedin_trends'
            })
        
        return pd.DataFrame(sample_data)
