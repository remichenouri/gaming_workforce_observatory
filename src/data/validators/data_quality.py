"""
Gaming Workforce Observatory - Data Quality Validator
Validation complète de la qualité des données gaming avec scoring
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import logging
from datetime import datetime, timedelta
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class DataQualityMetric:
    """Métrique de qualité des données"""
    name: str
    score: float  # 0-100
    status: str   # 'excellent', 'good', 'warning', 'critical'
    details: str
    recommendations: List[str]

class DataQualityValidator:
    """Validateur de qualité des données gaming avec scoring avancé"""
    
    def __init__(self):
        self.quality_thresholds = {
            'excellent': 95,
            'good': 85,
            'warning': 70,
            'critical': 50
        }
        
        # Patterns de validation
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.url_pattern = re.compile(r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$')
        
        # Valeurs gaming spécifiques valides
        self.valid_departments = {
            'Programming', 'Art & Animation', 'Game Design', 'Quality Assurance',
            'Production', 'Audio', 'Marketing', 'Management', 'Other'
        }
        
        self.valid_experience_levels = {
            'Intern', 'Junior', 'Mid', 'Senior', 'Lead', 'Principal', 'Director'
        }
        
        self.valid_regions = {
            'North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Africa', 'Remote'
        }
    
    def validate_dataset(self, df: pd.DataFrame, dataset_name: str = "gaming_data") -> Dict[str, Any]:
        """Validation complète d'un dataset gaming"""
        if df.empty:
            return {
                'dataset_name': dataset_name,
                'overall_score': 0,
                'status': 'critical',
                'total_records': 0,
                'metrics': [],
                'summary': 'Dataset is empty'
            }
        
        metrics = []
        
        # Métriques de base
        metrics.append(self._check_completeness(df))
        metrics.append(self._check_consistency(df))
        metrics.append(self._check_validity(df))
        metrics.append(self._check_uniqueness(df))
        metrics.append(self._check_timeliness(df))
        metrics.append(self._check_gaming_specific_rules(df))
        
        # Score global
        overall_score = np.mean([m.score for m in metrics])
        overall_status = self._score_to_status(overall_score)
        
        # Recommandations consolidées
        all_recommendations = []
        for metric in metrics:
            all_recommendations.extend(metric.recommendations)
        
        result = {
            'dataset_name': dataset_name,
            'overall_score': round(overall_score, 2),
            'status': overall_status,
            'total_records': len(df),
            'timestamp': datetime.now().isoformat(),
            'metrics': [
                {
                    'name': m.name,
                    'score': round(m.score, 2),
                    'status': m.status,
                    'details': m.details
                } for m in metrics
            ],
            'recommendations': list(set(all_recommendations)),
            'data_profile': self._generate_data_profile(df)
        }
        
        logger.info(f"Data quality validation completed for {dataset_name}: {overall_score:.1f}% ({overall_status})")
        
        return result
    
    def _check_completeness(self, df: pd.DataFrame) -> DataQualityMetric:
        """Vérifie la complétude des données"""
        total_cells = df.size
        missing_cells = df.isnull().sum().sum()
        completeness_rate = ((total_cells - missing_cells) / total_cells) * 100
        
        status = self._score_to_status(completeness_rate)
        
        # Analyse par colonne
        missing_by_column = df.isnull().sum()
        high_missing_columns = missing_by_column[missing_by_column > len(df) * 0.2].index.tolist()
        
        details = f"Overall completeness: {completeness_rate:.1f}%. Missing values: {missing_cells:,} out of {total_cells:,} cells."
        
        recommendations = []
        if high_missing_columns:
            details += f" Columns with >20% missing: {', '.join(high_missing_columns)}"
            recommendations.append(f"Investigate high missing rate in columns: {', '.join(high_missing_columns[:3])}")
        
        if completeness_rate < 90:
            recommendations.append("Implement data collection improvements to reduce missing values")
        
        return DataQualityMetric(
            name="Data Completeness",
            score=completeness_rate,
            status=status,
            details=details,
            recommendations=recommendations
        )
    
    def _check_consistency(self, df: pd.DataFrame) -> DataQualityMetric:
        """Vérifie la cohérence des données"""
        consistency_issues = []
        consistency_score = 100
        
        # Cohérence des salaires
        if 'salary_usd' in df.columns:
            salary_issues = self._check_salary_consistency(df)
            consistency_issues.extend(salary_issues)
        
        # Cohérence des dates
        date_columns = df.select_dtypes(include=['datetime64']).columns
        for col in date_columns:
            date_issues = self._check_date_consistency(df, col)
            consistency_issues.extend(date_issues)
        
        # Cohérence gaming spécifique
        if 'department' in df.columns and 'role' in df.columns:
            role_dept_issues = self._check_role_department_consistency(df)
            consistency_issues.extend(role_dept_issues)
        
        # Calcul du score
        if consistency_issues:
            consistency_score = max(0, 100 - (len(consistency_issues) * 10))
        
        status = self._score_to_status(consistency_score)
        details = f"Found {len(consistency_issues)} consistency issues."
        
        recommendations = []
        if consistency_issues:
            recommendations.append("Review and resolve data consistency issues")
            if len(consistency_issues) > 5:
                recommendations.append("Implement automated data validation rules")
        
        return DataQualityMetric(
            name="Data Consistency",
            score=consistency_score,
            status=status,
            details=details,
            recommendations=recommendations
        )
    
    def _check_validity(self, df: pd.DataFrame) -> DataQualityMetric:
        """Vérifie la validité des formats et valeurs"""
        validity_issues = []
        total_validations = 0
        
        # Validation des emails
        if 'email' in df.columns:
            email_invalid = df['email'].dropna().apply(
                lambda x: not bool(self.email_pattern.match(str(x)))
            ).sum()
            total_validations += len(df['email'].dropna())
            validity_issues.extend(['invalid_email'] * email_invalid)
        
        # Validation des URLs
        url_columns = [col for col in df.columns if 'url' in col.lower() or 'website' in col.lower()]
        for col in url_columns:
            url_invalid = df[col].dropna().apply(
                lambda x: not bool(self.url_pattern.match(str(x)))
            ).sum()
            total_validations += len(df[col].dropna())
            validity_issues.extend(['invalid_url'] * url_invalid)
        
        # Validation des valeurs numériques
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if 'salary' in col.lower():
                invalid_salaries = ((df[col] < 0) | (df[col] > 1000000)).sum()
                total_validations += len(df[col].dropna())
                validity_issues.extend(['invalid_salary_range'] * invalid_salaries)
        
        # Score de validité
        validity_score = 100
        if total_validations > 0:
            validity_score = max(0, 100 - (len(validity_issues) / total_validations * 100))
        
        status = self._score_to_status(validity_score)
        details = f"Validity check: {len(validity_issues)} invalid values out of {total_validations} validated."
        
        recommendations = []
        if len(validity_issues) > 0:
            recommendations.append("Implement input validation at data collection points")
            recommendations.append("Review and correct invalid format values")
        
        return DataQualityMetric(
            name="Data Validity",
            score=validity_score,
            status=status,
            details=details,
            recommendations=recommendations
        )
    
    def _check_uniqueness(self, df: pd.DataFrame) -> DataQualityMetric:
        """Vérifie l'unicité des données"""
        uniqueness_issues = []
        
        # Colonnes qui devraient être uniques
        unique_columns = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['id', 'email', 'key']):
                unique_columns.append(col)
        
        duplicate_records = 0
        for col in unique_columns:
            duplicates = df[col].dropna().duplicated().sum()
            if duplicates > 0:
                uniqueness_issues.append(f"{col}: {duplicates} duplicates")
                duplicate_records += duplicates
        
        # Doublons complets
        full_duplicates = df.duplicated().sum()
        if full_duplicates > 0:
            uniqueness_issues.append(f"Full record duplicates: {full_duplicates}")
            duplicate_records += full_duplicates
        
        # Score d'unicité
        uniqueness_score = max(0, 100 - (duplicate_records / len(df) * 100))
        
        status = self._score_to_status(uniqueness_score)
        details = f"Uniqueness check: {len(uniqueness_issues)} uniqueness violations found."
        
        recommendations = []
        if uniqueness_issues:
            recommendations.append("Remove or consolidate duplicate records")
            recommendations.append("Implement unique constraints in data collection")
        
        return DataQualityMetric(
            name="Data Uniqueness",
            score=uniqueness_score,
            status=status,
            details=details,
            recommendations=recommendations
        )
    
    def _check_timeliness(self, df: pd.DataFrame) -> DataQualityMetric:
        """Vérifie la fraîcheur des données"""
        timeliness_score = 100
        recommendations = []
        
        # Recherche colonnes de dates
        date_columns = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['date', 'time', 'created', 'updated']):
                if df[col].dtype in ['datetime64[ns]', 'object']:
                    date_columns.append(col)
        
        if not date_columns:
            details = "No timestamp columns found for timeliness assessment."
            recommendations.append("Add timestamp columns to track data freshness")
            timeliness_score = 70  # Pénalité pour absence de timestamps
        else:
            # Analyse de la fraîcheur
            freshness_issues = []
            now = datetime.now()
            
            for col in date_columns:
                try:
                    dates = pd.to_datetime(df[col], errors='coerce').dropna()
                    if len(dates) > 0:
                        latest_date = dates.max()
                        oldest_date = dates.min()
                        
                        days_since_latest = (now - latest_date).days
                        
                        if days_since_latest > 30:
                            freshness_issues.append(f"{col}: Latest data is {days_since_latest} days old")
                        
                        # Données futures (problématique)
                        future_dates = (dates > now).sum()
                        if future_dates > 0:
                            freshness_issues.append(f"{col}: {future_dates} future dates detected")
                
                except Exception as e:
                    logger.warning(f"Error processing date column {col}: {e}")
            
            if freshness_issues:
                timeliness_score = max(30, 100 - len(freshness_issues) * 15)
                recommendations.append("Update data collection processes for fresher data")
            
            details = f"Timeliness analysis on {len(date_columns)} date columns. Issues: {len(freshness_issues)}"
        
        status = self._score_to_status(timeliness_score)
        
        return DataQualityMetric(
            name="Data Timeliness",
            score=timeliness_score,
            status=status,
            details=details,
            recommendations=recommendations
        )
    
    def _check_gaming_specific_rules(self, df: pd.DataFrame) -> DataQualityMetric:
        """Vérifie les règles spécifiques à l'industrie gaming"""
        gaming_issues = []
        gaming_score = 100
        
        # Validation départements gaming
        if 'department' in df.columns:
            invalid_departments = df[~df['department'].isin(self.valid_departments)]['department'].dropna()
            if len(invalid_departments) > 0:
                gaming_issues.append(f"Invalid departments: {len(invalid_departments)} records")
        
        # Validation niveaux d'expérience
        if 'experience_level' in df.columns:
            invalid_levels = df[~df['experience_level'].isin(self.valid_experience_levels)]['experience_level'].dropna()
            if len(invalid_levels) > 0:
                gaming_issues.append(f"Invalid experience levels: {len(invalid_levels)} records")
        
        # Validation salaires gaming
        if 'salary_usd' in df.columns:
            # Salaires gaming réalistes: 30K - 500K
            unrealistic_salaries = df[
                (df['salary_usd'] < 30000) | (df['salary_usd'] > 500000)
            ]['salary_usd'].dropna()
            if len(unrealistic_salaries) > 0:
                gaming_issues.append(f"Unrealistic gaming salaries: {len(unrealistic_salaries)} records")
        
        # Validation cohérence role/department
        if 'role' in df.columns and 'department' in df.columns:
            inconsistent_roles = self._find_inconsistent_gaming_roles(df)
            if inconsistent_roles > 0:
                gaming_issues.append(f"Role-department mismatches: {inconsistent_roles} records")
        
        # Score gaming
        if gaming_issues:
            gaming_score = max(50, 100 - len(gaming_issues) * 12)
        
        status = self._score_to_status(gaming_score)
        details = f"Gaming industry validation: {len(gaming_issues)} issues found."
        
        recommendations = []
        if gaming_issues:
            recommendations.append("Review gaming industry data standards")
            recommendations.append("Implement gaming-specific validation rules")
        
        return DataQualityMetric(
            name="Gaming Industry Rules",
            score=gaming_score,
            status=status,
            details=details,
            recommendations=recommendations
        )
    
    def _score_to_status(self, score: float) -> str:
        """Convertit un score en statut"""
        if score >= self.quality_thresholds['excellent']:
            return 'excellent'
        elif score >= self.quality_thresholds['good']:
            return 'good'
        elif score >= self.quality_thresholds['warning']:
            return 'warning'
        else:
            return 'critical'
    
    def _generate_data_profile(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Génère un profil des données"""
        profile = {
            'shape': df.shape,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'column_types': df.dtypes.astype(str).to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'unique_values': df.nunique().to_dict()
        }
        
        # Statistiques numériques
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            profile['numeric_stats'] = df[numeric_columns].describe().to_dict()
        
        # Top valeurs pour colonnes catégorielles
        categorical_columns = df.select_dtypes(include=['object']).columns
        profile['categorical_top_values'] = {}
        
        for col in categorical_columns:
            top_values = df[col].value_counts().head(5).to_dict()
            profile['categorical_top_values'][col] = top_values
        
        return profile
    
    def generate_quality_report(self, validation_result: Dict[str, Any]) -> str:
        """Génère un rapport de qualité formaté"""
        report = f"""
# DATA QUALITY REPORT: {validation_result['dataset_name']}

## Overall Assessment
- **Score**: {validation_result['overall_score']}% ({validation_result['status'].upper()})
- **Total Records**: {validation_result['total_records']:,}
- **Validation Date**: {validation_result['timestamp']}

## Quality Metrics
"""
        
        for metric in validation_result['metrics']:
            status_emoji = {
                'excellent': '🟢',
                'good': '🟡', 
                'warning': '🟠',
                'critical': '🔴'
            }.get(metric['status'], '⚪')
            
            report += f"""
### {status_emoji} {metric['name']}
- **Score**: {metric['score']}%
- **Status**: {metric['status'].title()}
- **Details**: {metric['details']}
"""
        
        if validation_result['recommendations']:
            report += "\n## Recommendations\n"
            for i, rec in enumerate(validation_result['recommendations'], 1):
                report += f"{i}. {rec}\n"
        
        return report
