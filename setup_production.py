#!/usr/bin/env python3
"""
Solān AI Observatorium - Production Setup Script
Automated setup for production deployment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class SolanProductionSetup:
    """Production setup manager for Solān AI Observatorium"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.platform = platform.system().lower()
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("🐍 Checking Python version...")
        
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ is required")
            return False
        
        print(f"   ✅ Python {self.python_version} detected")
        return True
    
    def create_virtual_environment(self):
        """Create virtual environment if it doesn't exist"""
        print("🔧 Setting up virtual environment...")
        
        venv_path = self.project_root / "venv"
        
        if venv_path.exists():
            print("   ✅ Virtual environment already exists")
            return True
        
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            print("   ✅ Virtual environment created")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to create virtual environment: {e}")
            return False
    
    def get_pip_command(self):
        """Get the correct pip command for the platform"""
        venv_path = self.project_root / "venv"
        
        if self.platform == "windows":
            return str(venv_path / "Scripts" / "pip.exe")
        else:
            return str(venv_path / "bin" / "pip")
    
    def install_dependencies(self):
        """Install production dependencies"""
        print("📦 Installing production dependencies...")
        
        pip_cmd = self.get_pip_command()
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("   ❌ requirements.txt not found")
            return False
        
        try:
            # Upgrade pip first
            subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
            print("   ✅ Pip upgraded")
            
            # Install requirements
            subprocess.run([pip_cmd, "install", "-r", str(requirements_file)], check=True)
            print("   ✅ Dependencies installed")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install dependencies: {e}")
            return False
    
    def create_environment_file(self):
        """Create .env file with production settings"""
        print("⚙️ Creating environment configuration...")
        
        env_file = self.project_root / ".env"
        
        if env_file.exists():
            print("   ✅ .env file already exists")
            return True
        
        env_content = """# Solān AI Observatorium - Production Environment
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://127.0.0.1:5500

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=10

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Cache Configuration
CACHE_ENABLED=true
CACHE_TTL=300

# Monitoring
METRICS_ENABLED=true
HEALTH_CHECK_ENABLED=true
"""
        
        try:
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("   ✅ .env file created")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create .env file: {e}")
            return False
    
    def create_startup_scripts(self):
        """Create startup scripts for different platforms"""
        print("🚀 Creating startup scripts...")
        
        # Windows startup script
        windows_script = self.project_root / "start_production.bat"
        windows_content = """@echo off
echo Starting Solān AI Observatorium...
cd /d "%~dp0"
call venv\\Scripts\\activate.bat
python main_server.py
pause
"""
        
        # Unix startup script
        unix_script = self.project_root / "start_production.sh"
        unix_content = """#!/bin/bash
echo "Starting Solān AI Observatorium..."
cd "$(dirname "$0")"
source venv/bin/activate
python main_server.py
"""
        
        try:
            # Create Windows script
            with open(windows_script, 'w') as f:
                f.write(windows_content)
            
            # Create Unix script
            with open(unix_script, 'w') as f:
                f.write(unix_content)
            
            # Make Unix script executable
            if self.platform != "windows":
                os.chmod(unix_script, 0o755)
            
            print("   ✅ Startup scripts created")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create startup scripts: {e}")
            return False
    
    def create_docker_files(self):
        """Create Docker configuration files"""
        print("🐳 Creating Docker configuration...")
        
        # Dockerfile
        dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash solan
RUN chown -R solan:solan /app
USER solan

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/api/status || exit 1

# Start application
CMD ["python", "main_server.py"]
"""
        
        # Docker Compose
        docker_compose_content = """version: '3.8'

services:
  solan-observatorium:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/status"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add Redis for caching
  # redis:
  #   image: redis:7-alpine
  #   ports:
  #     - "6379:6379"
  #   restart: unless-stopped

volumes:
  logs:
"""
        
        try:
            # Create Dockerfile
            with open(self.project_root / "Dockerfile", 'w') as f:
                f.write(dockerfile_content)
            
            # Create docker-compose.yml
            with open(self.project_root / "docker-compose.yml", 'w') as f:
                f.write(docker_compose_content)
            
            print("   ✅ Docker files created")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create Docker files: {e}")
            return False
    
    def run_tests(self):
        """Run production readiness tests"""
        print("🧪 Running production readiness tests...")
        
        test_files = [
            "test_main_server.py",
            "test_observatorium_integration.py"
        ]
        
        python_cmd = self.get_python_command()
        
        for test_file in test_files:
            test_path = self.project_root / test_file
            if test_path.exists():
                try:
                    result = subprocess.run([python_cmd, str(test_path)], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"   ✅ {test_file} passed")
                    else:
                        print(f"   ❌ {test_file} failed")
                        print(f"      {result.stderr}")
                        return False
                except Exception as e:
                    print(f"   ❌ Error running {test_file}: {e}")
                    return False
            else:
                print(f"   ⚠️ {test_file} not found")
        
        return True
    
    def get_python_command(self):
        """Get the correct Python command for the platform"""
        venv_path = self.project_root / "venv"
        
        if self.platform == "windows":
            return str(venv_path / "Scripts" / "python.exe")
        else:
            return str(venv_path / "bin" / "python")
    
    def display_completion_message(self):
        """Display setup completion message"""
        print("\n" + "="*60)
        print("🎉 SOLĀN AI OBSERVATORIUM PRODUCTION SETUP COMPLETE!")
        print("="*60)
        print("\n📋 NEXT STEPS:")
        print("1. Review and update .env file with your production settings")
        print("2. Update SECRET_KEY in .env with a secure random key")
        print("3. Configure ALLOWED_ORIGINS for your domain")
        print("4. Start the server:")
        
        if self.platform == "windows":
            print("   Windows: start_production.bat")
        else:
            print("   Unix/Linux: ./start_production.sh")
        
        print("5. Or use Docker: docker-compose up -d")
        print("\n🌐 Server will be available at: http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/api/docs")
        print("🔍 Observatorium Interface: Open solan_observatorium.html")
        print("\n🚀 Ready for production deployment!")
    
    def run_setup(self):
        """Run complete production setup"""
        print("🚀 SOLĀN AI OBSERVATORIUM - PRODUCTION SETUP")
        print("="*60)
        
        steps = [
            ("Python Version Check", self.check_python_version),
            ("Virtual Environment", self.create_virtual_environment),
            ("Dependencies Installation", self.install_dependencies),
            ("Environment Configuration", self.create_environment_file),
            ("Startup Scripts", self.create_startup_scripts),
            ("Docker Configuration", self.create_docker_files),
            ("Production Tests", self.run_tests)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            if not step_func():
                print(f"❌ Setup failed at: {step_name}")
                return False
        
        self.display_completion_message()
        return True

def main():
    """Main setup function"""
    setup = SolanProductionSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
