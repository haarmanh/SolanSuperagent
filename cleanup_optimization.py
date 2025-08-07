#!/usr/bin/env python3
"""
Solān Platform Cleanup & Optimization Script
Removes garbage files, optimizes performance, and cleans up project structure
"""

import os
import shutil
import glob
import json
from pathlib import Path
from datetime import datetime

class SolanCleanupOptimizer:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.cleanup_report = {
            "timestamp": datetime.now().isoformat(),
            "files_removed": [],
            "folders_removed": [],
            "space_saved_mb": 0,
            "optimizations": []
        }
    
    def remove_python_cache(self):
        """Remove all Python cache files (.pyc, __pycache__)"""
        print("🧹 Removing Python cache files...")
        
        # Remove __pycache__ directories
        for pycache_dir in self.project_root.rglob("__pycache__"):
            if pycache_dir.is_dir():
                size_mb = self.get_folder_size(pycache_dir) / (1024 * 1024)
                shutil.rmtree(pycache_dir)
                self.cleanup_report["folders_removed"].append(str(pycache_dir))
                self.cleanup_report["space_saved_mb"] += size_mb
                print(f"   ✅ Removed {pycache_dir} ({size_mb:.2f} MB)")
        
        # Remove .pyc files
        for pyc_file in self.project_root.rglob("*.pyc"):
            size_mb = pyc_file.stat().st_size / (1024 * 1024)
            pyc_file.unlink()
            self.cleanup_report["files_removed"].append(str(pyc_file))
            self.cleanup_report["space_saved_mb"] += size_mb
    
    def remove_log_files(self):
        """Remove old log files but keep recent ones"""
        print("📝 Cleaning up log files...")
        
        for log_file in self.project_root.rglob("*.log"):
            # Keep main solan.log but remove old dated logs
            if "2025-08-03" in str(log_file) or log_file.stat().st_size == 0:
                size_mb = log_file.stat().st_size / (1024 * 1024)
                log_file.unlink()
                self.cleanup_report["files_removed"].append(str(log_file))
                self.cleanup_report["space_saved_mb"] += size_mb
                print(f"   ✅ Removed {log_file.name} ({size_mb:.2f} MB)")
    
    def remove_backup_folders(self):
        """Remove old backup folders"""
        print("📦 Removing old backup folders...")
        
        backup_patterns = [
            "backup_before_conversion_*",
            "optimization_backup_*"
        ]
        
        for pattern in backup_patterns:
            for backup_dir in self.project_root.glob(pattern):
                if backup_dir.is_dir():
                    size_mb = self.get_folder_size(backup_dir) / (1024 * 1024)
                    shutil.rmtree(backup_dir)
                    self.cleanup_report["folders_removed"].append(str(backup_dir))
                    self.cleanup_report["space_saved_mb"] += size_mb
                    print(f"   ✅ Removed {backup_dir.name} ({size_mb:.2f} MB)")
    
    def clean_audio_files(self):
        """Remove old audio files but keep recent ones"""
        print("🔊 Cleaning up audio files...")
        
        audio_dir = self.project_root / "audio_output"
        if audio_dir.exists():
            audio_files = list(audio_dir.glob("*.wav"))
            # Keep only the 3 most recent audio files
            if len(audio_files) > 3:
                audio_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                for old_audio in audio_files[3:]:
                    size_mb = old_audio.stat().st_size / (1024 * 1024)
                    old_audio.unlink()
                    self.cleanup_report["files_removed"].append(str(old_audio))
                    self.cleanup_report["space_saved_mb"] += size_mb
                    print(f"   ✅ Removed {old_audio.name} ({size_mb:.2f} MB)")
    
    def optimize_node_modules(self):
        """Check if node_modules can be optimized"""
        print("📦 Analyzing node_modules...")
        
        node_modules = self.project_root / "node_modules"
        if node_modules.exists():
            size_mb = self.get_folder_size(node_modules) / (1024 * 1024)
            print(f"   📊 node_modules size: {size_mb:.2f} MB")
            
            # Check if package.json exists to determine if it's needed
            package_json = self.project_root / "package.json"
            if not package_json.exists():
                print("   ⚠️  No package.json found - node_modules might be unnecessary")
                self.cleanup_report["optimizations"].append("Consider removing node_modules if not needed")
            else:
                print("   ✅ node_modules appears to be in use")
    
    def remove_duplicate_files(self):
        """Remove obvious duplicate files"""
        print("🔍 Checking for duplicate files...")
        
        # Remove .old files
        for old_file in self.project_root.rglob("*.old"):
            size_mb = old_file.stat().st_size / (1024 * 1024)
            old_file.unlink()
            self.cleanup_report["files_removed"].append(str(old_file))
            self.cleanup_report["space_saved_mb"] += size_mb
            print(f"   ✅ Removed {old_file.name} ({size_mb:.2f} MB)")
    
    def get_folder_size(self, folder_path):
        """Calculate total size of a folder"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass
        return total_size
    
    def create_gitignore(self):
        """Create/update .gitignore for better project management"""
        print("📝 Creating/updating .gitignore...")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/

# Logs
*.log
logs/*.log

# Audio files
audio_output/*.wav

# Cache
.cache/
*.cache

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Node modules
node_modules/

# Backups
backup_*/
optimization_backup_*/

# Temporary files
*.tmp
*.temp
*.bak
*.old
"""
        
        gitignore_path = self.project_root / ".gitignore"
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        
        print("   ✅ .gitignore created/updated")
        self.cleanup_report["optimizations"].append("Created/updated .gitignore")
    
    def run_cleanup(self):
        """Run complete cleanup process"""
        print("🚀 Starting Solān Platform Cleanup & Optimization")
        print("=" * 60)
        
        self.remove_python_cache()
        self.remove_log_files()
        self.remove_backup_folders()
        self.clean_audio_files()
        self.remove_duplicate_files()
        self.optimize_node_modules()
        self.create_gitignore()
        
        # Save cleanup report
        report_path = self.project_root / "cleanup_report.json"
        with open(report_path, "w") as f:
            json.dump(self.cleanup_report, f, indent=2)
        
        print("\n" + "=" * 60)
        print("🎉 CLEANUP COMPLETED!")
        print(f"📊 Files removed: {len(self.cleanup_report['files_removed'])}")
        print(f"📁 Folders removed: {len(self.cleanup_report['folders_removed'])}")
        print(f"💾 Space saved: {self.cleanup_report['space_saved_mb']:.2f} MB")
        print(f"📝 Report saved to: {report_path}")
        
        return self.cleanup_report

if __name__ == "__main__":
    optimizer = SolanCleanupOptimizer()
    optimizer.run_cleanup()
