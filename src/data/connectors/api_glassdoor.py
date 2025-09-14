"""
Gaming Workforce Observatory - Glassdoor API Connector Enterprise
Extraction données salary & reviews gaming via API Glassdoor avec rate limiting
"""
import requests
import time
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import streamlit as st
from urllib.parse import urlencode
import hashlib

logger = logging.getLogger(__name__)

class GlassdoorAPIConnector:
    """Connecteur API Glassdoor enterprise pour données salary gaming"""
    
    def __init__(self):
        self.api_key = st.secrets.get("GLASSDOOR_API_KEY")
        self.partner_id = st.secrets.get("GLASSDOOR_PARTNER_ID")
        self.base_url = "https://api.glassdoor.com/api/api.htm"
        self.rate_limit_per_day = 1000
        self.rate_limit_per_hour = 200
        self.requests_today = 0
        self.requests_this_hour = 0
        self.last_request_time = datetime.now()
        
        # Cache pour éviter requêtes répétées
        self.cache = {}
        self.cache_duration = timedelta(hours=6)
    
    def _generate_cache_key(self, endpoint: str, params: Dict) -> str:
        """Génère une clé de cache unique"""
        key_string = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_rate_limited(self) -> bool:
        """Vérifie les limites de taux"""
        now = datetime.now()
        
        # Reset compteurs si nouvelle heure/jour
        if now.hour != self.last_request_time.hour:
            self.requests_this_hour = 0
        
        if now.date() != self.last_request_time.date():
            self.requests_today = 0
        
        return (self.requests_today >= self.rate_limit_per_day or 
                self.requests_this_hour >= self.rate_limit_per_hour)
    
    def _make_request(self, action: str, params: Dict) -> Optional[Dict]:
        """Effectue une requête API avec gestion cache et rate limiting"""
        
        # Vérification cache
        cache_key = self._generate_cache_key(action, params)
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                logger.info(f"Cache hit for Glassdoor {action}")
                return cached_data
        
        # Vérification rate limiting
        if self._is_rate_limited():
            logger.warning("Glassdoor API rate limit reached")
            return None
        
        # Préparation requête
        request_params = {
            'v': '1',
            'format': 'json',
            't.p': self.partner_id,
            't.k': self.api_key,
            'action': action,
            'userip': '192.168.1.1',  # IP placeholder
            'useragent': 'Gaming-Workforce-Observatory/1.0'
        }
        request_params.update(params)
        
        try:
            response = requests.get(self.base_url, params=request_params, timeout=30)
            
            # Mise à jour compteurs
            self.requests_today += 1
            self.requests_this_hour += 1
            self.last_request_time = datetime.now()
            
            if response.status_code == 200:
                data = response.json()
                
                # Mise en cache
                self.cache[cache_key] = (data, datetime.now())
                
                logger.info(f"Glassdoor API {action} successful")
                return data
            else:
                logger.error(f"Glassdoor API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Glassdoor request error: {e}")
            return None
    
    def search_gaming_companies(self, limit: int = 50) -> List[Dict]:
        """Recherche entreprises gaming sur Glassdoor"""
        
        gaming_keywords = [
            "video game", "gaming", "game development", "game studio",
            "interactive entertainment", "mobile games", "console games"
        ]
        
        all_companies = []
        
        for keyword in gaming_keywords:
            params = {
                'q': keyword,
                'ps': min(limit, 20)  # Max 20 par requête
            }
            
            response = self._make_request('employers', params)
            
            if response and 'response' in response:
                employers = response['response'].get('employers', [])
                
                for employer in employers:
                    company_info = self._extract_company_info(employer)
                    if company_info and self._is_gaming_company(company_info):
                        all_companies.append(company_info)
            
            # Pause entre requêtes
            time.sleep(1)
        
        # Dédupliquer par nom
        unique_companies = {}
        for company in all_companies:
            name = company.get('name', '').lower()
            if name not in unique_companies:
                unique_companies[name] = company
        
        logger.info(f"Found {len(unique_companies)} unique gaming companies")
        return list(unique_companies.values())
    
    def _extract_company_info(self, employer_data: Dict) -> Optional[Dict]:
        """Extrait informations pertinentes d'une entreprise"""
        try:
            return {
                'glassdoor_id': employer_data.get('id'),
                'name': employer_data.get('name', ''),
                'website': employer_data.get('website', ''),
                'industry': employer_data.get('industry', ''),
                'size': employer_data.get('size', ''),
                'founded': employer_data.get('founded'),
                'type': employer_data.get('type', ''),
                'revenue': employer_data.get('revenue', ''),
                'headquarters': employer_data.get('headquarters', ''),
                'competitors': employer_data.get('competitors', []),
                'overall_rating': employer_data.get('overallRating', 0),
                'culture_values_rating': employer_data.get('cultureAndValuesRating', 0),
                'diversity_inclusion_rating': employer_data.get('diversityAndInclusionRating', 0),
                'career_opportunities_rating': employer_data.get('careerOpportunitiesRating', 0),
                'work_life_balance_rating': employer_data.get('workLifeBalanceRating', 0),
                'senior_management_rating': employer_data.get('seniorManagementRating', 0),
                'recommend_to_friend': employer_data.get('recommendToFriendRating', 0),
                'ceo_approval': employer_data.get('ceoRating', 0),
                'num_reviews': employer_data.get('numberOfRatings', 0)
            }
        except Exception as e:
            logger.error(f"Error extracting company info: {e}")
            return None
    
    def _is_gaming_company(self, company_info: Dict) -> bool:
        """Détermine si une entreprise est dans le gaming"""
        gaming_indicators = [
            'game', 'gaming', 'entertainment', 'interactive', 'digital',
            'software', 'technology', 'mobile', 'console', 'video'
        ]
        
        text_fields = [
            company_info.get('name', '').lower(),
            company_info.get('industry', '').lower(),
            company_info.get('website', '').lower()
        ]
        
        combined_text = ' '.join(text_fields)
        
        return any(indicator in combined_text for indicator in gaming_indicators)
    
    def get_company_reviews(self, company_id: int, pages: int = 5) -> List[Dict]:
        """Récupère les reviews d'une entreprise gaming"""
        
        all_reviews = []
        
        for page in range(1, pages + 1):
            params = {
                'employerId': company_id,
                'p': page,
                'ps': 20  # 20 reviews par page
            }
            
            response = self._make_request('employers_reviews', params)
            
            if response and 'response' in response:
                reviews = response['response'].get('reviews', [])
                
                for review in reviews:
                    review_info = self._extract_review_info(review)
                    if review_info:
                        all_reviews.append(review_info)
            
            time.sleep(1)  # Pause entre pages
        
        logger.info(f"Retrieved {len(all_reviews)} reviews for company {company_id}")
        return all_reviews
    
    def _extract_review_info(self, review_data: Dict) -> Optional[Dict]:
        """Extrait informations d'une review"""
        try:
            return {
                'review_id': review_data.get('reviewId'),
                'overall_rating': review_data.get('overall', 0),
                'work_life_balance': review_data.get('workLifeBalance', 0),
                'culture_values': review_data.get('cultureAndValues', 0),
                'diversity_inclusion': review_data.get('diversityAndInclusion', 0),
                'career_opportunities': review_data.get('careerOpportunities', 0),
                'compensation_benefits': review_data.get('compensationAndBenefits', 0),
                'senior_management': review_data.get('seniorManagement', 0),
                'recommend': review_data.get('recommend', False),
                'ceo_approval': review_data.get('ceoApproval', ''),
                'outlook': review_data.get('outlook', ''),
                'review_date': review_data.get('reviewDateTime'),
                'job_title': review_data.get('jobTitle', ''),
                'location': review_data.get('location', ''),
                'employment_status': review_data.get('employmentStatus', ''),
                'job_ending_year': review_data.get('jobEndingYear'),
                'length_of_employment': review_data.get('lengthOfEmployment', 0),
                'pros': review_data.get('pros', ''),
                'cons': review_data.get('cons', ''),
                'advice_to_mgmt': review_data.get('adviceToMgmt', ''),
                'is_current_job': review_data.get('isCurrentJob', False),
                'helpful': review_data.get('helpful', 0),
                'not_helpful': review_data.get('notHelpful', 0)
            }
        except Exception as e:
            logger.error(f"Error extracting review info: {e}")
            return None
    
    def get_salary_data(self, job_title: str, location: str = None) -> List[Dict]:
        """Récupère données de salaire pour un poste gaming"""
        
        params = {
            'jobTitle': job_title
        }
        
        if location:
            params['location'] = location
        
        response = self._make_request('salaries', params)
        
        if response and 'response' in response:
            salaries = response['response'].get('salaries', [])
            
            salary_data = []
            for salary in salaries:
                salary_info = self._extract_salary_info(salary)
                if salary_info:
                    salary_data.append(salary_info)
            
            logger.info(f"Retrieved {len(salary_data)} salary entries for {job_title}")
            return salary_data
        
        return []
    
    def _extract_salary_info(self, salary_data: Dict) -> Optional[Dict]:
        """Extrait informations de salaire"""
        try:
            return {
                'job_title': salary_data.get('jobTitle', ''),
                'employer': salary_data.get('employer', ''),
                'location': salary_data.get('location', ''),
                'base_salary': salary_data.get('basePay'),
                'total_compensation': salary_data.get('totalCompensation'),
                'years_experience': salary_data.get('yearsOfExperience'),
                'employment_type': salary_data.get('employmentType', ''),
                'job_function': salary_data.get('jobFunction', ''),
                'seniority_level': salary_data.get('seniorityLevel', ''),
                'date_time': salary_data.get('dateTime'),
                'currency': salary_data.get('payCurrency', 'USD')
            }
        except Exception as e:
            logger.error(f"Error extracting salary info: {e}")
            return None
    
    def analyze_gaming_market_trends(self) -> Dict[str, Any]:
        """Analyse les tendances du marché gaming"""
        
        major_gaming_companies = [
            'Microsoft', 'Sony', 'Nintendo', 'Electronic Arts', 'Activision',
            'Ubisoft', 'Take-Two', 'Epic Games', 'Valve', 'Bungie'
        ]
        
        market_analysis = {
            'company_ratings': {},
            'salary_trends': {},
            'employment_satisfaction': {},
            'industry_insights': {}
        }
        
        for company in major_gaming_companies:
            # Recherche ID de l'entreprise
            search_params = {'q': company, 'ps': 1}
            search_response = self._make_request('employers', search_params)
            
            if search_response and 'response' in search_response:
                employers = search_response['response'].get('employers', [])
                if employers:
                    company_data = employers[0]
                    company_id = company_data.get('id')
                    
                    # Analyse des ratings
                    market_analysis['company_ratings'][company] = {
                        'overall_rating': company_data.get('overallRating', 0),
                        'work_life_balance': company_data.get('workLifeBalanceRating', 0),
                        'culture_values': company_data.get('cultureAndValuesRating', 0),
                        'career_opportunities': company_data.get('careerOpportunitiesRating', 0),
                        'diversity_inclusion': company_data.get('diversityAndInclusionRating', 0),
                        'num_reviews': company_data.get('numberOfRatings', 0)
                    }
            
            time.sleep(2)  # Pause entre entreprises
        
        return market_analysis
    
    def export_gaming_data(self) -> pd.DataFrame:
        """Exporte toutes les données gaming collectées"""
        
        companies = self.search_gaming_companies(limit=100)
        
        if not companies:
            return pd.DataFrame()
        
        # Convertir en DataFrame
        df = pd.DataFrame(companies)
        
        # Enrichissement avec données calculées
        df['rating_category'] = df['overall_rating'].apply(self._categorize_rating)
        df['size_category'] = df['size'].apply(self._categorize_company_size)
        df['review_volume'] = df['num_reviews'].apply(self._categorize_review_volume)
        
        # Ajout timestamp
        df['data_retrieved_at'] = datetime.now().isoformat()
        
        logger.info(f"Exported {len(df)} gaming companies data")
        return df
    
    def _categorize_rating(self, rating: float) -> str:
        """Catégorise les ratings"""
        if rating >= 4.5:
            return 'Excellent'
        elif rating >= 4.0:
            return 'Very Good'
        elif rating >= 3.5:
            return 'Good'
        elif rating >= 3.0:
            return 'Average'
        elif rating >= 2.0:
            return 'Below Average'
        else:
            return 'Poor'
    
    def _categorize_company_size(self, size: str) -> str:
        """Catégorise la taille d'entreprise"""
        if not size:
            return 'Unknown'
        
        size_lower = size.lower()
        if '10000+' in size_lower or 'large' in size_lower:
            return 'Large (10000+)'
        elif '1000' in size_lower and '9999' in size_lower:
            return 'Medium (1000-9999)'
        elif '200' in size_lower and '999' in size_lower:
            return 'Small (200-999)'
        elif '50' in size_lower and '199' in size_lower:
            return 'Startup (50-199)'
        else:
            return 'Micro (<50)'
    
    def _categorize_review_volume(self, num_reviews: int) -> str:
        """Catégorise le volume de reviews"""
        if num_reviews >= 1000:
            return 'High (1000+)'
        elif num_reviews >= 100:
            return 'Medium (100-999)'
        elif num_reviews >= 10:
            return 'Low (10-99)'
        else:
            return 'Very Low (<10)'
