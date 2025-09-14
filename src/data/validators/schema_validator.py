"""
Gaming Workforce Observatory - Schema Validator Enterprise
Validation avancée des schémas de données gaming avec JSONSchema
"""
import jsonschema
import json
import pandas as pd
from typing import Dict, List, Any, Optional, Union
import logging
from datetime import datetime
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)

class GamingSchemaValidator:
    """Validateur de schémas enterprise pour données gaming"""
    
    def __init__(self):
        self.schemas_directory = Path(__file__).parent.parent.parent / "schemas"
        self.loaded_schemas = {}
        self.validation_results = {}
        
        # Schémas gaming intégrés
        self.gaming_schemas = {
            'employee': self._get_employee_schema(),
            'studio': self._get_studio_schema(),
            'salary': self._get_salary_schema(),
            'performance': self._get_performance_schema(),
            'neurodiversity': self._get_neurodiversity_schema()
        }
    
    def validate_data(self, data: Union[Dict, List[Dict]], schema_name: str) -> Dict[str, Any]:
        """Valide des données contre un schéma"""
        
        validation_result = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'schema_used': schema_name,
            'timestamp': datetime.now().isoformat(),
            'records_validated': 0,
            'valid_records': 0,
            'invalid_records': 0
        }
        
        try:
            # Chargement du schéma
            schema = self._load_schema(schema_name)
            if not schema:
                validation_result['errors'].append(f"Schema '{schema_name}' not found")
                return validation_result
            
            # Validation selon le type de données
            if isinstance(data, list):
                validation_result = self._validate_list_data(data, schema, validation_result)
            else:
                validation_result = self._validate_single_record(data, schema, validation_result)
            
            # Détermination du statut global
            validation_result['is_valid'] = len(validation_result['errors']) == 0
            
            logger.info(f"Schema validation completed: {validation_result['valid_records']}/{validation_result['records_validated']} records valid")
            
        except Exception as e:
            validation_result['errors'].append(f"Validation error: {str(e)}")
            logger.error(f"Schema validation failed: {e}")
        
        return validation_result
    
    def _load_schema(self, schema_name: str) -> Optional[Dict]:
        """Charge un schéma depuis le cache ou les fichiers"""
        
        # Vérifier cache en mémoire
        if schema_name in self.loaded_schemas:
            return self.loaded_schemas[schema_name]
        
        # Vérifier schémas intégrés
        if schema_name in self.gaming_schemas:
            schema = self.gaming_schemas[schema_name]
            self.loaded_schemas[schema_name] = schema
            return schema
        
        # Charger depuis fichier
        schema_file = self.schemas_directory / f"{schema_name}.json"
        if schema_file.exists():
            try:
                with open(schema_file, 'r') as f:
                    schema = json.load(f)
                    self.loaded_schemas[schema_name] = schema
                    return schema
            except Exception as e:
                logger.error(f"Error loading schema file {schema_file}: {e}")
        
        # Essayer YAML
        yaml_file = self.schemas_directory / f"{schema_name}.yaml"
        if yaml_file.exists():
            try:
                with open(yaml_file, 'r') as f:
                    schema = yaml.safe_load(f)
                    self.loaded_schemas[schema_name] = schema
                    return schema
            except Exception as e:
                logger.error(f"Error loading YAML schema file {yaml_file}: {e}")
        
        return None
    
    def _validate_list_data(self, data_list: List[Dict], schema: Dict, 
                           validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Valide une liste de records"""
        
        validation_result['records_validated'] = len(data_list)
        
        for i, record in enumerate(data_list):
            try:
                jsonschema.validate(instance=record, schema=schema)
                validation_result['valid_records'] += 1
            except jsonschema.ValidationError as e:
                validation_result['invalid_records'] += 1
                validation_result['errors'].append({
                    'record_index': i,
                    'error_message': e.message,
                    'error_path': list(e.path),
                    'invalid_value': e.instance
                })
            except Exception as e:
                validation_result['invalid_records'] += 1
                validation_result['errors'].append({
                    'record_index': i,
                    'error_message': f"Unexpected error: {str(e)}"
                })
        
        return validation_result
    
    def _validate_single_record(self, data: Dict, schema: Dict, 
                               validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Valide un seul record"""
        
        validation_result['records_validated'] = 1
        
        try:
            jsonschema.validate(instance=data, schema=schema)
            validation_result['valid_records'] = 1
        except jsonschema.ValidationError as e:
            validation_result['invalid_records'] = 1
            validation_result['errors'].append({
                'error_message': e.message,
                'error_path': list(e.path),
                'invalid_value': e.instance
            })
        except Exception as e:
            validation_result['invalid_records'] = 1
            validation_result['errors'].append({
                'error_message': f"Unexpected error: {str(e)}"
            })
        
        return validation_result
    
    def validate_dataframe(self, df: pd.DataFrame, schema_name: str) -> Dict[str, Any]:
        """Valide un DataFrame contre un schéma"""
        
        # Convertir DataFrame en liste de dictionnaires
        data_list = df.to_dict('records')
        
        # Validation standard
        validation_result = self.validate_data(data_list, schema_name)
        
        # Ajout d'informations spécifiques DataFrame
        validation_result['dataframe_info'] = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'missing_values': df.isnull().sum().to_dict()
        }
        
        return validation_result
    
    def _get_employee_schema(self) -> Dict:
        """Schéma pour données employés gaming"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Gaming Employee Schema",
            "required": ["employee_id", "department", "experience_level"],
            "properties": {
                "employee_id": {
                    "type": ["string", "integer"],
                    "description": "Unique employee identifier"
                },
                "name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 100
                },
                "department": {
                    "type": "string",
                    "enum": ["Programming", "Art & Animation", "Game Design", 
                            "Quality Assurance", "Production", "Audio", "Marketing", "Management"]
                },
                "experience_level": {
                    "type": "string",
                    "enum": ["Intern", "Junior", "Mid", "Senior", "Lead", "Principal", "Director"]
                },
                "salary_usd": {
                    "type": "number",
                    "minimum": 20000,
                    "maximum": 500000
                },
                "satisfaction_score": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 10
                },
                "performance_score": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 5
                },
                "location": {
                    "type": "string",
                    "maxLength": 100
                },
                "hire_date": {
                    "type": "string",
                    "format": "date"
                },
                "is_remote": {
                    "type": "boolean"
                },
                "skills": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "neurodivergent_condition": {
                    "type": ["string", "null"],
                    "enum": ["ADHD", "Autism Spectrum", "Dyslexia", "Dyspraxia", "Other", null]
                },
                "weekly_hours": {
                    "type": "number",
                    "minimum": 10,
                    "maximum": 80
                },
                "project_phase": {
                    "type": "string",
                    "enum": ["pre_production", "production", "alpha", "beta", "gold_master", "post_launch"]
                }
            },
            "additionalProperties": false
        }
    
    def _get_studio_schema(self) -> Dict:
        """Schéma pour données studios gaming"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Gaming Studio Schema",
            "required": ["studio_name", "country", "employees"],
            "properties": {
                "studio_name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                },
                "country": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 100
                },
                "region": {
                    "type": "string",
                    "enum": ["North America", "Europe", "Asia-Pacific", "Latin America", "Africa"]
                },
                "employees": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 50000
                },
                "founded_year": {
                    "type": "integer",
                    "minimum": 1970,
                    "maximum": 2030
                },
                "revenue_usd": {
                    "type": ["number", "null"],
                    "minimum": 0
                },
                "avg_salary_usd": {
                    "type": "number",
                    "minimum": 20000,
                    "maximum": 300000
                },
                "retention_rate": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100
                },
                "headquarters": {
                    "type": "string",
                    "maxLength": 200
                },
                "website": {
                    "type": "string",
                    "format": "uri"
                },
                "studio_type": {
                    "type": "string",
                    "enum": ["AAA", "AA", "Indie", "Mobile", "VR/AR", "Casual"]
                },
                "game_genres": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["Action", "RPG", "Strategy", "Simulation", "Sports", 
                                "Racing", "Adventure", "Puzzle", "Fighting", "Shooter", 
                                "Platform", "MMO", "Mobile", "VR/AR", "Indie", "Casual"]
                    }
                },
                "neurodiversity_programs": {
                    "type": ["integer", "boolean"],
                    "minimum": 0,
                    "maximum": 1
                },
                "public_company": {
                    "type": "boolean"
                }
            },
            "additionalProperties": false
        }
    
    def _get_salary_schema(self) -> Dict:
        """Schéma pour données salaires gaming"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Gaming Salary Schema",
            "required": ["role", "salary_usd", "experience_level", "location"],
            "properties": {
                "role": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 150
                },
                "department": {
                    "type": "string",
                    "enum": ["Programming", "Art & Animation", "Game Design", 
                            "Quality Assurance", "Production", "Audio", "Marketing", "Management"]
                },
                "experience_level": {
                    "type": "string",
                    "enum": ["Intern", "Junior", "Mid", "Senior", "Lead", "Principal", "Director"]
                },
                "salary_usd": {
                    "type": "number",
                    "minimum": 20000,
                    "maximum": 500000
                },
                "bonus_usd": {
                    "type": ["number", "null"],
                    "minimum": 0,
                    "maximum": 200000
                },
                "equity_value_usd": {
                    "type": ["number", "null"],
                    "minimum": 0
                },
                "total_compensation_usd": {
                    "type": ["number", "null"],
                    "minimum": 20000,
                    "maximum": 1000000
                },
                "location": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 100
                },
                "company_name": {
                    "type": "string",
                    "maxLength": 150
                },
                "company_size": {
                    "type": "string",
                    "enum": ["Startup (1-50)", "Small (51-200)", "Medium (201-1000)", 
                            "Large (1001-5000)", "Enterprise (5000+)"]
                },
                "employment_type": {
                    "type": "string",
                    "enum": ["Full-time", "Part-time", "Contract", "Freelance", "Internship"]
                },
                "remote_work": {
                    "type": "string",
                    "enum": ["Fully Remote", "Hybrid", "On-site", "Flexible"]
                },
                "benefits_score": {
                    "type": ["number", "null"],
                    "minimum": 1,
                    "maximum": 10
                },
                "satisfaction_score": {
                    "type": ["number", "null"],
                    "minimum": 1,
                    "maximum": 10
                },
                "years_experience": {
                    "type": ["integer", "null"],
                    "minimum": 0,
                    "maximum": 50
                },
                "data_source": {
                    "type": "string",
                    "enum": ["Glassdoor", "LinkedIn", "Survey", "Internal", "Indeed", "Other"]
                },
                "report_date": {
                    "type": "string",
                    "format": "date"
                }
            },
            "additionalProperties": false
        }
    
    def _get_performance_schema(self) -> Dict:
        """Schéma pour données performance employés"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Gaming Performance Schema",
            "required": ["employee_id", "performance_score", "review_period"],
            "properties": {
                "employee_id": {
                    "type": ["string", "integer"]
                },
                "performance_score": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 5
                },
                "goals_achievement": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100
                },
                "technical_skills": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 5
                },
                "collaboration": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 5
                },
                "innovation": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 5
                },
                "problem_solving": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 5
                },
                "review_period": {
                    "type": "string",
                    "pattern": "^\\d{4}-(Q[1-4]|H[1-2]|Annual)$"
                },
                "reviewer_id": {
                    "type": ["string", "integer"]
                },
                "development_areas": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "achievements": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "promotion_recommended": {
                    "type": "boolean"
                }
            },
            "additionalProperties": false
        }
    
    def _get_neurodiversity_schema(self) -> Dict:
        """Schéma pour données neurodiversité"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Gaming Neurodiversity Schema",
            "required": ["employee_id", "condition_type"],
            "properties": {
                "employee_id": {
                    "type": ["string", "integer"]
                },
                "condition_type": {
                    "type": "string",
                    "enum": ["ADHD", "Autism Spectrum", "Dyslexia", "Dyspraxia", "Tourette's", "Other"]
                },
                "diagnosis_confirmed": {
                    "type": "boolean"
                },
                "accommodations_requested": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["Noise-canceling headphones", "Flexible working hours", 
                                "Quiet workspace", "Written instructions", "Regular breaks",
                                "Task prioritization support", "Mentoring", "Communication preferences"]
                    }
                },
                "accommodations_provided": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "performance_impact": {
                    "type": "number",
                    "minimum": -1,
                    "maximum": 2,
                    "description": "Performance multiplier relative to baseline"
                },
                "satisfaction_with_support": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 10
                },
                "disclosure_date": {
                    "type": "string",
                    "format": "date"
                },
                "support_cost_annual": {
                    "type": ["number", "null"],
                    "minimum": 0,
                    "maximum": 10000
                }
            },
            "additionalProperties": false
        }
    
    def generate_schema_from_data(self, data: Union[Dict, pd.DataFrame], 
                                 schema_name: str) -> Dict:
        """Génère un schéma à partir des données existantes"""
        
        if isinstance(data, pd.DataFrame):
            # Analyser DataFrame pour générer schéma
            return self._generate_schema_from_dataframe(data, schema_name)
        elif isinstance(data, list) and len(data) > 0:
            # Analyser liste de dictionnaires
            return self._generate_schema_from_list(data, schema_name)
        elif isinstance(data, dict):
            # Analyser dictionnaire unique
            return self._generate_schema_from_dict(data, schema_name)
        else:
            raise ValueError("Unsupported data type for schema generation")
    
    def _generate_schema_from_dataframe(self, df: pd.DataFrame, schema_name: str) -> Dict:
        """Génère un schéma à partir d'un DataFrame"""
        
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": f"Generated {schema_name} Schema",
            "properties": {},
            "required": []
        }
        
        for column in df.columns:
            column_data = df[column].dropna()
            
            if len(column_data) == 0:
                continue
                
            # Déterminer le type de données
            if pd.api.types.is_numeric_dtype(column_data):
                if pd.api.types.is_integer_dtype(column_data):
                    prop_type = "integer"
                    schema["properties"][column] = {
                        "type": prop_type,
                        "minimum": int(column_data.min()),
                        "maximum": int(column_data.max())
                    }
                else:
                    prop_type = "number"
                    schema["properties"][column] = {
                        "type": prop_type,
                        "minimum": float(column_data.min()),
                        "maximum": float(column_data.max())
                    }
            elif pd.api.types.is_bool_dtype(column_data):
                schema["properties"][column] = {"type": "boolean"}
            elif pd.api.types.is_datetime64_any_dtype(column_data):
                schema["properties"][column] = {
                    "type": "string",
                    "format": "date-time"
                }
            else:
                # String type
                max_length = column_data.astype(str).str.len().max()
                unique_values = column_data.unique()
                
                if len(unique_values) <= 20 and len(unique_values) > 1:
                    # Enumeration si peu de valeurs uniques
                    schema["properties"][column] = {
                        "type": "string",
                        "enum": unique_values.tolist()
                    }
                else:
                    schema["properties"][column] = {
                        "type": "string",
                        "maxLength": int(max_length) if max_length > 0 else 1000
                    }
            
            # Ajouter aux champs requis si peu de valeurs manquantes
            missing_percentage = df[column].isnull().sum() / len(df)
            if missing_percentage < 0.1:  # Moins de 10% manquant
                schema["required"].append(column)
        
        return schema
    
    def save_schema(self, schema: Dict, schema_name: str, format: str = "json") -> bool:
        """Sauvegarde un schéma sur disque"""
        
        try:
            # Créer le répertoire si nécessaire
            self.schemas_directory.mkdir(parents=True, exist_ok=True)
            
            if format.lower() == "json":
                schema_file = self.schemas_directory / f"{schema_name}.json"
                with open(schema_file, 'w') as f:
                    json.dump(schema, f, indent=2)
            elif format.lower() == "yaml":
                schema_file = self.schemas_directory / f"{schema_name}.yaml"
                with open(schema_file, 'w') as f:
                    yaml.dump(schema, f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            # Mettre en cache
            self.loaded_schemas[schema_name] = schema
            
            logger.info(f"Schema '{schema_name}' saved to {schema_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving schema '{schema_name}': {e}")
            return False
    
    def get_validation_report(self, validation_result: Dict[str, Any]) -> str:
        """Génère un rapport de validation formaté"""
        
        report = f"""
# SCHEMA VALIDATION REPORT

## Summary
- **Schema**: {validation_result.get('schema_used', 'Unknown')}
- **Validation Status**: {'✅ VALID' if validation_result.get('is_valid') else '❌ INVALID'}
- **Total Records**: {validation_result.get('records_validated', 0):,}
- **Valid Records**: {validation_result.get('valid_records', 0):,}
- **Invalid Records**: {validation_result.get('invalid_records', 0):,}
- **Validation Time**: {validation_result.get('timestamp', 'Unknown')}

## Validation Results
"""
        
        if validation_result.get('is_valid'):
            report += "🎉 All records passed validation successfully!\n"
        else:
            error_count = len(validation_result.get('errors', []))
            report += f"⚠️ Found {error_count} validation errors:\n\n"
            
            for i, error in enumerate(validation_result.get('errors', [])[:10], 1):
                if isinstance(error, dict):
                    record_info = f"Record {error.get('record_index', 'Unknown')}: " if 'record_index' in error else ""
                    report += f"{i}. {record_info}{error.get('error_message', 'Unknown error')}\n"
                else:
                    report += f"{i}. {error}\n"
            
            if error_count > 10:
                report += f"\n... and {error_count - 10} more errors.\n"
        
        # Ajouter informations DataFrame si disponibles
        if 'dataframe_info' in validation_result:
            df_info = validation_result['dataframe_info']
            report += f"""
## DataFrame Information
- **Shape**: {df_info.get('shape', 'Unknown')}
- **Columns**: {len(df_info.get('columns', []))}
- **Data Types**: {len(set(df_info.get('dtypes', {}).values()))} unique types
- **Missing Values**: {sum(df_info.get('missing_values', {}).values())} total missing
"""
        
        return report
