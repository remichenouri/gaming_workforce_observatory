"""
Backup scripts for Gaming Workforce Observatory data and configuration
"""
import os
import shutil
import datetime
import json
import pandas as pd
import zipfile
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BackupManager:
    """Manage backups for the application"""
    
    def __init__(self, backup_dir: str = "./backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self, include_data=True, include_config=True, include_logs=True):
        """Create a complete backup of the application"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"gaming_workforce_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        logger.info(f"Creating backup: {backup_name}")
        
        backup_info = {
            'timestamp': timestamp,
            'version': '1.0.0',
            'includes': {
                'data': include_data,
                'config': include_config,
                'logs': include_logs
            }
        }
        
        try:
            # Backup data files
            if include_data and os.path.exists('./data'):
                data_backup = backup_path / 'data'
                shutil.copytree('./data', data_backup)
                logger.info("✅ Data files backed up")
            
            # Backup configuration files
            if include_config:
                config_backup = backup_path / 'config'
                config_backup.mkdir(exist_ok=True)
                
                config_files = [
                    '.env',
                    'requirements.txt',
                    'requirements-dev.txt',
                    '.streamlit/config.toml',
                    'data_schema.json',
                    'docker-compose.yml',
                    'Dockerfile'
                ]
                
                for file_path in config_files:
                    if os.path.exists(file_path):
                        dest = config_backup / os.path.basename(file_path)
                        shutil.copy2(file_path, dest)
                
                logger.info("✅ Configuration files backed up")
            
            # Backup logs
            if include_logs and os.path.exists('./logs'):
                logs_backup = backup_path / 'logs'
                shutil.copytree('./logs', logs_backup)
                logger.info("✅ Log files backed up")
            
            # Backup source code
            src_backup = backup_path / 'src'
            if os.path.exists('./src'):
                shutil.copytree('./src', src_backup)
            
            pages_backup = backup_path / 'pages'
            if os.path.exists('./pages'):
                shutil.copytree('./pages', pages_backup)
            
            # Copy main app file
            if os.path.exists('./app.py'):
                shutil.copy2('./app.py', backup_path / 'app.py')
            
            logger.info("✅ Source code backed up")
            
            # Save backup info
            with open(backup_path / 'backup_info.json', 'w') as f:
                json.dump(backup_info, f, indent=2)
            
            # Create ZIP archive
            zip_path = self.backup_dir / f"{backup_name}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_path)
                        zipf.write(file_path, arcname)
            
            # Remove uncompressed backup
            shutil.rmtree(backup_path)
            
            logger.info(f"✅ Backup completed: {zip_path}")
            return str(zip_path)
            
        except Exception as e:
            logger.error(f"❌ Backup failed: {str(e)}")
            raise
    
    def restore_backup(self, backup_path: str, restore_data=True, restore_config=True):
        """Restore from a backup file"""
        backup_file = Path(backup_path)
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        logger.info(f"Restoring from backup: {backup_file.name}")
        
        # Create temporary extraction directory
        temp_dir = self.backup_dir / "temp_restore"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()
        
        try:
            # Extract backup
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Read backup info
            backup_info_path = temp_dir / 'backup_info.json'
            if backup_info_path.exists():
                with open(backup_info_path, 'r') as f:
                    backup_info = json.load(f)
                logger.info(f"Backup version: {backup_info.get('version', 'unknown')}")
                logger.info(f"Backup timestamp: {backup_info.get('timestamp', 'unknown')}")
            
            # Restore data
            if restore_data and (temp_dir / 'data').exists():
                if os.path.exists('./data'):
                    shutil.rmtree('./data')
                shutil.copytree(temp_dir / 'data', './data')
                logger.info("✅ Data restored")
            
            # Restore configuration
            if restore_config and (temp_dir / 'config').exists():
                config_dir = temp_dir / 'config'
                for config_file in config_dir.iterdir():
                    if config_file.is_file():
                        dest_path = Path('.') / config_file.name
                        if config_file.name == 'config.toml':
                            dest_path = Path('.streamlit') / config_file.name
                        shutil.copy2(config_file, dest_path)
                logger.info("✅ Configuration restored")
            
            # Restore source code (be careful!)
            if (temp_dir / 'src').exists():
                logger.warning("⚠️ Source code restore available but skipped for safety")
            
            logger.info("✅ Restore completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Restore failed: {str(e)}")
            raise
        finally:
            # Cleanup
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        for backup_file in self.backup_dir.glob("gaming_workforce_backup_*.zip"):
            stat = backup_file.stat()
            backups.append({
                'name': backup_file.name,
                'path': str(backup_file),
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created': datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def cleanup_old_backups(self, keep_days=30):
        """Remove backups older than specified days"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=keep_days)
        
        removed_count = 0
        for backup_file in self.backup_dir.glob("gaming_workforce_backup_*.zip"):
            if datetime.datetime.fromtimestamp(backup_file.stat().st_mtime) < cutoff_date:
                backup_file.unlink()
                removed_count += 1
                logger.info(f"Removed old backup: {backup_file.name}")
        
        logger.info(f"Cleanup completed. Removed {removed_count} old backups.")
        return removed_count

def main():
    """CLI interface for backup operations"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gaming Workforce Observatory Backup Manager')
    parser.add_argument('action', choices=['create', 'restore', 'list', 'cleanup'], 
                       help='Action to perform')
    parser.add_argument('--backup-path', help='Path to backup file (for restore)')
    parser.add_argument('--no-data', action='store_true', help='Exclude data from backup')
    parser.add_argument('--no-config', action='store_true', help='Exclude config from backup')
    parser.add_argument('--keep-days', type=int, default=30, help='Days to keep backups (for cleanup)')
    
    args = parser.parse_args()
    
    backup_manager = BackupManager()
    
    if args.action == 'create':
        backup_path = backup_manager.create_backup(
            include_data=not args.no_data,
            include_config=not args.no_config
        )
        print(f"Backup created: {backup_path}")
    
    elif args.action == 'restore':
        if not args.backup_path:
            print("Error: --backup-path is required for restore")
            return
        backup_manager.restore_backup(
            args.backup_path,
            restore_data=not args.no_data,
            restore_config=not args.no_config
        )
        print("Restore completed")
    
    elif args.action == 'list':
        backups = backup_manager.list_backups()
        if backups:
            print(f"{'Name':<40} {'Size (MB)':<10} {'Created':<20}")
            print("-" * 70)
            for backup in backups:
                print(f"{backup['name']:<40} {backup['size_mb']:<10} {backup['created']:<20}")
        else:
            print("No backups found")
    
    elif args.action == 'cleanup':
        removed = backup_manager.cleanup_old_backups(args.keep_days)
        print(f"Removed {removed} old backups")

if __name__ == "__main__":
    main()
