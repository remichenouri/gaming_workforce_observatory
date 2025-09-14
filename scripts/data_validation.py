"""
Gaming Workforce Observatory - Data Validation
Validation des données spécifique à l'industrie gaming
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime, date
import jsonschema
from jsonschema import validate, ValidationError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GamingDataValidator:
    """Validation des données pour l'industrie gaming"""
    
    def __init__(self, schema_path: Optional[str] = None):
        self.schema_path = schema_path or "config/data_schema.json"
        self.gaming_schema = self._load_gaming_schema()
        self.validation_results: List[Dict] = []
        
    def _load_gaming_schema(self) -> Dict:
        """Charge le schéma de validation gaming"""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Schema file not found: {self.schema_path}, using default")
            return self._get_default_gaming_schema()
    
    def _get_default_gaming_schema(self) -> Dict:
        """Schéma par défaut pour les données gaming"""
        return {
            "required_columns": [
                "employee_id", "name", "department", "level", 
                "salary", "hire_date", "satisfaction_score"
            ],
            "gaming_departments": [
                "Game Design", "Programming", "Art", "QA", 
                "Marketing", "Management", "Audio", "Production"
            ],
            "gaming_levels": [
                "Junior", "Mid", "Senior", "Lead", "Principal", "Director"
            ],
            "salary_ranges": {
                "Junior": {"min": 35000, "max": 65000},
                "Mid": {"min": 55000, "max": 90000},
                "Senior": {"min": 80000, "max": 130000},
                "Lead": {"min": 110000, "max": 180000},
                "Principal": {"min": 150000, "max": 250000},
                "Director": {"min": 180000, "max": 400000}
            },
            "score_ranges": {
                "satisfaction_score": {"min": 1, "max": 10},
                "performance_score": {"min": 1, "max": 5},
                "sprint_velocity": {"min": 0, "max": 100},
                "bug_fix_rate": {"min": 0, "max": 100},
                "innovation_index": {"min": 0, "max": 100}
            }
        }
    
    def validate_gaming_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation complète d'un DataFrame gaming"""
        validation_report = {
            "timestamp": datetime.now().isoformat(),
            "total_rows": len(df),
            "validation_status": "unknown",
            "errors": [],
            "warnings": [],
            "gaming_specific_checks": {},
            "data_quality_score": 0.0
        }
        
        try:
            # 1. Validation des colonnes requises
            missing_columns = self._check_required_columns(df)
            if missing_columns:
                validation_report["errors"].extend([
                    f"Missing required column: {col}" for col in missing_columns
                ])
            
            # 2. Validation des départements gaming
            invalid_departments = self._check_gaming_departments(df)
            if invalid_departments:
                validation_report["warnings"].extend([
                    f"Invalid gaming department: {dept}" for dept in invalid_departments
                ])
            
            # 3. Validation des niveaux gaming
            invalid_levels = self._check_gaming_levels(df)
            if invalid_levels:
                validation_report["warnings"].extend([
                    f"Invalid gaming level: {level}" for level in invalid_levels
                ])
            
            # 4. Validation des salaires gaming
            salary_issues = self._check_gaming_salaries(df)
            validation_report["gaming_specific_checks"]["salary_validation"] = salary_issues
            
            # 5. Validation des scores gaming
            score_issues = self._check_gaming_scores(df)
            validation_report["gaming_specific_checks"]["score_validation"] = score_issues
            
            # 6. Validation des données temporelles
            date_issues = self._check_date_consistency(df)
            validation_report["gaming_specific_checks"]["date_validation"] = date_issues
            
            # 7. Validation de la cohérence gaming
            consistency_issues = self._check_gaming_consistency(df)
            validation_report["gaming_specific_checks"]["consistency_validation"] = consistency_issues
            
            # 8. Calcul du score de qualité
            validation_report["data_quality_score"] = self._calculate_quality_score(validation_report)
            
            # 9. Détermination du statut final
            if len(validation_report["errors"]) == 0:
                if len(validation_report["warnings"]) == 0:
                    validation_report["validation_status"] = "excellent"
                else:
                    validation_report["validation_status"] = "good_with_warnings"
            else:
                validation_report["validation_status"] = "failed"
            
            logger.info(f"Gaming data validation completed: {validation_report['validation_status']}")
            
        except Exception as e:
            validation_report["errors"].append(f"Validation process failed: {str(e)}")
            validation_report["validation_status"] = "error"
            logger.error(f"Gaming data validation error: {str(e)}")
        
        return validation_report
    
    def _check_required_columns(self, df: pd.DataFrame) -> List[str]:
        """Vérifie les colonnes requises pour les données gaming"""
        required = self.gaming_schema["required_columns"]
        missing = [col for col in required if col not in df.columns]
        return missing
    
    def _check_gaming_departments(self, df: pd.DataFrame) -> List[str]:
        """Vérifie les départements gaming valides"""
        if "department" not in df.columns:
            return []
        
        valid_departments = self.gaming_schema["gaming_departments"]
        invalid = df[~df["department"].isin(valid_departments)]["department"].unique().tolist()
        return invalid
    
    def _check_gaming_levels(self, df: pd.DataFrame) -> List[str]:
        """Vérifie les niveaux gaming valides"""
        if "level" not in df.columns:
            return []
        
        valid_levels = self.gaming_schema["gaming_levels"]
        invalid = df[~df["level"].isin(valid_levels)]["level"].unique().tolist()
        return invalid
    
    def _check_gaming_salaries(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Vérifie la cohérence des salaires gaming"""
        issues = {
            "out_of_range_count": 0,
            "level_inconsistencies": [],
            "department_outliers": []
        }
        
        if "salary" not in df.columns or "level" not in df.columns:
            return issues
        
        salary_ranges = self.gaming_schema["salary_ranges"]
        
        for _, row in df.iterrows():
            level = row.get("level")
            salary = row.get("salary")
            
            if level in salary_ranges and pd.notna(salary):
                min_salary = salary_ranges[level]["min"]
                max_salary = salary_ranges[level]["max"]
                
                if salary < min_salary or salary > max_salary:
                    issues["out_of_range_count"] += 1
                    issues["level_inconsistencies"].append({
                        "employee": row.get("name", "Unknown"),
                        "level": level,
                        "salary": salary,
                        "expected_range": f"{min_salary}-{max_salary}"
                    })
        
        return issues
    
    def _check_gaming_scores(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Vérifie les scores gaming (satisfaction, performance, etc.)"""
        issues = {
            "invalid_scores": [],
            "missing_scores": []
        }
        
        score_ranges = self.gaming_schema["score_ranges"]
        
        for score_name, range_info in score_ranges.items():
            if score_name in df.columns:
                min_val = range_info["min"]
                max_val = range_info["max"]
                
                # Vérifier les valeurs hors limites
                invalid_mask = (df[score_name] < min_val) | (df[score_name] > max_val)
                if invalid_mask.any():
                    invalid_count = invalid_mask.sum()
                    issues["invalid_scores"].append({
                        "score_type": score_name,
                        "invalid_count": invalid_count,
                        "expected_range": f"{min_val}-{max_val}"
                    })
                
                # Vérifier les valeurs manquantes
                missing_count = df[score_name].isna().sum()
                if missing_count > 0:
                    issues["missing_scores"].append({
                        "score_type": score_name,
                        "missing_count": missing_count,
                        "percentage": round((missing_count / len(df)) * 100, 2)
                    })
        
        return issues
    
    def _check_date_consistency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Vérifie la cohérence des dates"""
        issues = {
            "future_dates": [],
            "invalid_sequences": [],
            "missing_dates": []
        }
        
        if "hire_date" in df.columns:
            # Convertir en datetime si nécessaire
            df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")
            
            # Vérifier les dates futures
            future_mask = df["hire_date"] > datetime.now()
            if future_mask.any():
                issues["future_dates"] = df[future_mask]["name"].tolist()
            
            # Vérifier les dates manquantes
            missing_count = df["hire_date"].isna().sum()
            if missing_count > 0:
                issues["missing_dates"] = {
                    "count": missing_count,
                    "percentage": round((missing_count / len(df)) * 100, 2)
                }
        
        return issues
    
    def _check_gaming_consistency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Vérifications de cohérence spécifiques au gaming"""
        issues = {
            "experience_level_mismatch": [],
            "department_specialization_issues": [],
            "performance_anomalies": []
        }
        
        # Vérifier cohérence expérience/niveau
        if "years_experience" in df.columns and "level" in df.columns:
            for _, row in df.iterrows():
                experience = row.get("years_experience")
                level = row.get("level")
                
                if pd.notna(experience) and level:
                    expected_min_exp = {
                        "Junior": 0, "Mid": 2, "Senior": 5, 
                        "Lead": 7, "Principal": 10, "Director": 12
                    }
                    
                    if level in expected_min_exp:
                        min_exp = expected_min_exp[level]
                        if experience < min_exp:
                            issues["experience_level_mismatch"].append({
                                "employee": row.get("name", "Unknown"),
                                "level": level,
                                "experience": experience,
                                "expected_min": min_exp
                            })
        
        return issues
    
    def _calculate_quality_score(self, validation_report: Dict) -> float:
        """Calcule un score de qualité des données (0-100)"""
        base_score = 100.0
        
        # Pénalités
        error_penalty = len(validation_report["errors"]) * 10
        warning_penalty = len(validation_report["warnings"]) * 2
        
        # Bonus pour les vérifications gaming spécifiques
        gaming_checks = validation_report.get("gaming_specific_checks", {})
        
        # Calcul du score final
        final_score = max(0, base_score - error_penalty - warning_penalty)
        
        return round(final_score, 1)
    
    def generate_validation_report(self, df: pd.DataFrame, output_path: Optional[str] = None) -> str:
        """Génère un rapport de validation détaillé"""
        validation_results = self.validate_gaming_dataframe(df)
        
        report = f"""
🎮 Gaming Workforce Observatory - Data Validation Report
======================================================

📊 Dataset Overview:
- Total Employees: {validation_results['total_rows']}
- Validation Status: {validation_results['validation_status'].upper()}
- Data Quality Score: {validation_results['data_quality_score']}/100

❌ Errors ({len(validation_results['errors'])}):
{chr(10).join([f"  • {error}" for error in validation_results['errors']]) if validation_results['errors'] else "  ✅ No errors found"}

⚠️  Warnings ({len(validation_results['warnings'])}):
{chr(10).join([f"  • {warning}" for warning in validation_results['warnings']]) if validation_results['warnings'] else "  ✅ No warnings"}

🎮 Gaming-Specific Validations:
"""
        
        # Ajouter les détails des vérifications gaming
        for check_name, check_results in validation_results.get("gaming_specific_checks", {}).items():
            report += f"\n📋 {check_name.replace('_', ' ').title()}:\n"
            if isinstance(check_results, dict):
                for key, value in check_results.items():
                    if isinstance(value, list) and value:
                        report += f"  • {key}: {len(value)} issues\n"
                    elif isinstance(value, (int, float)) and value > 0:
                        report += f"  • {key}: {value}\n"
                    elif not value:
                        report += f"  ✅ {key}: OK\n"
        
        report += f"\n🕐 Validation completed at: {validation_results['timestamp']}\n"
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
            logger.info(f"Validation report saved to {output_path}")
        
        return report

def validate_sample_gaming_data():
    """Exemple d'utilisation avec des données gaming"""
    # Créer des données d'exemple
    sample_data = pd.DataFrame({
        'employee_id': range(1, 11),
        'name': [f'Employee_{i}' for i in range(1, 11)],
        'department': ['Programming', 'Art', 'Game Design', 'QA', 'Marketing'] * 2,
        'level': ['Junior', 'Mid', 'Senior', 'Lead', 'Senior'] * 2,
        'salary': [45000, 65000, 95000, 120000, 85000] * 2,
        'hire_date': pd.date_range('2020-01-01', periods=10, freq='3M'),
        'satisfaction_score': [8.5, 7.2, 9.1, 6.8, 8.0, 7.5, 8.8, 6.5, 9.2, 7.8],
        'years_experience': [1, 3, 6, 8, 5, 4, 7, 2, 9, 3]
    })
    
    # Valider les données
    validator = GamingDataValidator()
    report = validator.generate_validation_report(sample_data)
    print(report)

if __name__ == "__main__":
    validate_sample_gaming_data()
