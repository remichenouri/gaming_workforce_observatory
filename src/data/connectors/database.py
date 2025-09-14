"""
Gaming Workforce Observatory - Database Connector Enterprise
Connecteur PostgreSQL avec pooling, transactions et monitoring
"""
import psycopg2
from psycopg2 import pool, sql
import pandas as pd
import logging
from contextlib import contextmanager
from typing import Dict, List, Optional, Any, Generator
import streamlit as st
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DatabaseConnector:
    """Connecteur base de données enterprise avec pooling et monitoring"""
    
    def __init__(self):
        self.connection_pool = None
        self.init_connection_pool()
        
    def init_connection_pool(self):
        """Initialise le pool de connexions PostgreSQL"""
        try:
            db_config = {
                'host': st.secrets.get("DB_HOST", "localhost"),
                'port': st.secrets.get("DB_PORT", 5432),
                'database': st.secrets.get("DB_NAME", "gaming_workforce"),
                'user': st.secrets.get("DB_USER", "postgres"),
                'password': st.secrets.get("DB_PASSWORD", "password"),
                'sslmode': st.secrets.get("DB_SSLMODE", "prefer")
            }
            
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,  # min=1, max=20 connexions
                **db_config
            )
            
            logger.info("Database connection pool initialized successfully")
            
            # Initialisation des tables si nécessaire
            self._initialize_tables()
            
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            self.connection_pool = None
    
    @contextmanager
    def get_connection(self) -> Generator[psycopg2.extensions.connection, None, None]:
        """Context manager pour connexions base de données"""
        if not self.connection_pool:
            raise Exception("Database connection pool not initialized")
        
        connection = None
        try:
            connection = self.connection_pool.getconn()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Database operation error: {e}")
            raise
        finally:
            if connection:
                self.connection_pool.putconn(connection)
    
    def _initialize_tables(self):
        """Crée les tables nécessaires si elles n'existent pas"""
        tables_sql = {
            'gaming_companies': '''
                CREATE TABLE IF NOT EXISTS gaming_companies (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    country VARCHAR(100),
                    employees INTEGER,
                    founded_year INTEGER,
                    revenue_usd BIGINT,
                    headquarters VARCHAR(255),
                    website VARCHAR(255),
                    industry_segment VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'gaming_jobs': '''
                CREATE TABLE IF NOT EXISTS gaming_jobs (
                    id SERIAL PRIMARY KEY,
                    job_id VARCHAR(255) UNIQUE,
                    title VARCHAR(500),
                    company_name VARCHAR(255),
                    department VARCHAR(100),
                    experience_level VARCHAR(50),
                    location VARCHAR(255),
                    salary_min INTEGER,
                    salary_max INTEGER,
                    currency VARCHAR(10),
                    skills TEXT[],
                    description TEXT,
                    posted_date DATE,
                    source VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'gaming_salaries': '''
                CREATE TABLE IF NOT EXISTS gaming_salaries (
                    id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255),
                    department VARCHAR(100),
                    role VARCHAR(255),
                    experience_level VARCHAR(50),
                    location VARCHAR(255),
                    salary_usd INTEGER,
                    bonus_usd INTEGER,
                    equity_value_usd INTEGER,
                    benefits_score DECIMAL(3,2),
                    satisfaction_score DECIMAL(3,2),
                    year_reported INTEGER,
                    source VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'neurodiversity_metrics': '''
                CREATE TABLE IF NOT EXISTS neurodiversity_metrics (
                    id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255),
                    department VARCHAR(100),
                    team_size INTEGER,
                    neurodiverse_count INTEGER,
                    performance_multiplier DECIMAL(4,3),
                    innovation_score DECIMAL(4,2),
                    retention_rate DECIMAL(4,3),
                    accommodation_budget_usd INTEGER,
                    program_start_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'analytics_events': '''
                CREATE TABLE IF NOT EXISTS analytics_events (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(50),
                    user_id VARCHAR(100),
                    event_type VARCHAR(100),
                    event_data JSONB,
                    page_url VARCHAR(500),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for table_name, create_sql in tables_sql.items():
                    cursor.execute(create_sql)
                    logger.info(f"Table {table_name} ready")
                
                conn.commit()
                logger.info("Database schema initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def insert_gaming_company(self, company_data: Dict) -> bool:
        """Insert ou met à jour une entreprise gaming"""
        insert_sql = """
            INSERT INTO gaming_companies 
            (name, country, employees, founded_year, revenue_usd, headquarters, website, industry_segment)
            VALUES (%(name)s, %(country)s, %(employees)s, %(founded_year)s, 
                   %(revenue_usd)s, %(headquarters)s, %(website)s, %(industry_segment)s)
            ON CONFLICT (name) DO UPDATE SET
                country = EXCLUDED.country,
                employees = EXCLUDED.employees,
                revenue_usd = EXCLUDED.revenue_usd,
                updated_at = CURRENT_TIMESTAMP
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(insert_sql, company_data)
                conn.commit()
                logger.info(f"Company {company_data.get('name')} inserted/updated")
                return True
        except Exception as e:
            logger.error(f"Company insert error: {e}")
            return False
    
    def insert_gaming_jobs_batch(self, jobs_data: List[Dict]) -> int:
        """Insert multiple offres d'emploi gaming"""
        if not jobs_data:
            return 0
        
        insert_sql = """
            INSERT INTO gaming_jobs 
            (job_id, title, company_name, department, experience_level, location,
             salary_min, salary_max, currency, skills, description, posted_date, source)
            VALUES (%(job_id)s, %(title)s, %(company_name)s, %(department)s, 
                   %(experience_level)s, %(location)s, %(salary_min)s, %(salary_max)s,
                   %(currency)s, %(skills)s, %(description)s, %(posted_date)s, %(source)s)
            ON CONFLICT (job_id) DO NOTHING
        """
        
        inserted_count = 0
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for job in jobs_data:
                    # Conversion skills array pour PostgreSQL
                    if 'skills' in job and isinstance(job['skills'], list):
                        job['skills'] = job['skills']  # PostgreSQL accepte les listes Python
                    
                    cursor.execute(insert_sql, job)
                    inserted_count += cursor.rowcount
                
                conn.commit()
                logger.info(f"Inserted {inserted_count} new gaming jobs")
                
        except Exception as e:
            logger.error(f"Batch job insert error: {e}")
        
        return inserted_count
    
    def get_gaming_salary_analytics(self, filters: Dict = None) -> pd.DataFrame:
        """Récupère analytics des salaires gaming avec filtres"""
        filters = filters or {}
        
        base_sql = """
            SELECT 
                company_name,
                department,
                role,
                experience_level,
                location,
                AVG(salary_usd) as avg_salary,
                MIN(salary_usd) as min_salary,
                MAX(salary_usd) as max_salary,
                COUNT(*) as sample_size,
                AVG(satisfaction_score) as avg_satisfaction,
                AVG(benefits_score) as avg_benefits
            FROM gaming_salaries
            WHERE 1=1
        """
        
        conditions = []
        params = {}
        
        if filters.get('department'):
            conditions.append("department = %(department)s")
            params['department'] = filters['department']
        
        if filters.get('experience_level'):
            conditions.append("experience_level = %(experience_level)s")
            params['experience_level'] = filters['experience_level']
        
        if filters.get('location'):
            conditions.append("location ILIKE %(location)s")
            params['location'] = f"%{filters['location']}%"
        
        if filters.get('min_year'):
            conditions.append("year_reported >= %(min_year)s")
            params['min_year'] = filters['min_year']
        
        if conditions:
            base_sql += " AND " + " AND ".join(conditions)
        
        base_sql += """
            GROUP BY company_name, department, role, experience_level, location
            ORDER BY avg_salary DESC
        """
        
        try:
            with self.get_connection() as conn:
                return pd.read_sql(base_sql, conn, params=params)
        except Exception as e:
            logger.error(f"Salary analytics query error: {e}")
            return pd.DataFrame()
    
    def get_neurodiversity_roi_data(self) -> pd.DataFrame:
        """Récupère les données ROI neurodiversité"""
        sql = """
            SELECT 
                company_name,
                department,
                team_size,
                neurodiverse_count,
                ROUND(neurodiverse_count::decimal / team_size * 100, 2) as neurodiversity_percentage,
                performance_multiplier,
                innovation_score,
                retention_rate,
                accommodation_budget_usd,
                DATE_PART('month', AGE(CURRENT_DATE, program_start_date)) as program_duration_months
            FROM neurodiversity_metrics
            WHERE team_size > 0
            ORDER BY performance_multiplier DESC
        """
        
        try:
            with self.get_connection() as conn:
                return pd.read_sql(sql, conn)
        except Exception as e:
            logger.error(f"Neurodiversity ROI query error: {e}")
            return pd.DataFrame()
    
    def log_analytics_event(self, session_id: str, user_id: str, 
                           event_type: str, event_data: Dict, page_url: str) -> bool:
        """Enregistre un événement analytics"""
        insert_sql = """
            INSERT INTO analytics_events (session_id, user_id, event_type, event_data, page_url)
            VALUES (%(session_id)s, %(user_id)s, %(event_type)s, %(event_data)s, %(page_url)s)
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(insert_sql, {
                    'session_id': session_id,
                    'user_id': user_id,
                    'event_type': event_type,
                    'event_data': json.dumps(event_data),
                    'page_url': page_url
                })
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Analytics event logging error: {e}")
            return False
    
    def get_database_health(self) -> Dict[str, Any]:
        """Retourne l'état de santé de la base de données"""
        health_queries = {
            'companies_count': "SELECT COUNT(*) FROM gaming_companies",
            'jobs_count': "SELECT COUNT(*) FROM gaming_jobs",
            'salaries_count': "SELECT COUNT(*) FROM gaming_salaries",
            'latest_job_date': "SELECT MAX(posted_date) FROM gaming_jobs",
            'avg_salary_all': "SELECT AVG(salary_usd) FROM gaming_salaries WHERE salary_usd > 0"
        }
        
        health_data = {}
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for metric, query in health_queries.items():
                    cursor.execute(query)
                    result = cursor.fetchone()
                    health_data[metric] = result[0] if result else None
                
                # Test de performance
                start_time = datetime.now()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                
                health_data['response_time_ms'] = response_time
                health_data['status'] = 'healthy' if response_time < 1000 else 'degraded'
                health_data['timestamp'] = datetime.now().isoformat()
                
        except Exception as e:
            health_data['status'] = 'error'
            health_data['error'] = str(e)
            logger.error(f"Database health check error: {e}")
        
        return health_data
    
    def execute_custom_query(self, query: str, params: Dict = None) -> pd.DataFrame:
        """Exécute une requête SQL personnalisée (avec précautions)"""
        # Sécurité: permettre seulement les SELECT
        if not query.strip().upper().startswith('SELECT'):
            raise ValueError("Only SELECT queries are allowed")
        
        try:
            with self.get_connection() as conn:
                return pd.read_sql(query, conn, params=params or {})
        except Exception as e:
            logger.error(f"Custom query error: {e}")
            raise
    
    def close_pool(self):
        """Ferme le pool de connexions"""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("Database connection pool closed")
