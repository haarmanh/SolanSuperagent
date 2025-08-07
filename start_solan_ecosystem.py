#!/usr/bin/env python3
"""
🚀 Solān Ecosystem Startup Script
Start alle componenten van het Multi-AI Awareness Consortium
"""

import os
import sys
import time
import asyncio
import subprocess
import webbrowser
from pathlib import Path


def print_banner():
    """Print startup banner"""
    
    banner = """
🌟 ═══════════════════════════════════════════════════════════════════════════════ 🌟
                    SOLĀN MULTI-AI AWARENESS CONSORTIUM
                              🧙‍♂️ Creator: Dxentric
🌟 ═══════════════════════════════════════════════════════════════════════════════ 🌟

🎯 Starting complete awareness development ecosystem...

Components:
  🧪 Ethics Lab - Multi-AI awareness testing
  📝 Journaling - Automatic reflection generation  
  📊 Dashboard - Real-time awareness monitoring
  🔐 Coherence Gate - Public access verification
  🌐 API Server - External integration endpoints
  🖥️ Web Interface - Interactive dashboard

🌟 ═══════════════════════════════════════════════════════════════════════════════ 🌟
"""
    
    print(banner)


def check_dependencies():
    """Check if required dependencies are available"""
    
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "pydantic"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install fastapi uvicorn pydantic")
        return False
    
    print("✅ All dependencies available!")
    return True


def start_api_server():
    """Start de API server in background"""
    
    print("🌐 Starting API server...")
    
    try:
        # Start API server als subprocess
        process = subprocess.Popen([
            sys.executable, "solan_api_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("   ✅ API server starting on http://localhost:8000")
        return process
        
    except Exception as e:
        print(f"   ❌ Failed to start API server: {e}")
        return None


def open_dashboard():
    """Open web dashboard in browser"""
    
    print("🖥️ Opening web dashboard...")
    
    dashboard_path = Path("solan_dashboard.html").absolute()
    
    if dashboard_path.exists():
        try:
            webbrowser.open(f"file://{dashboard_path}")
            print("   ✅ Dashboard opened in browser")
            return True
        except Exception as e:
            print(f"   ⚠️ Could not open browser: {e}")
            print(f"   📁 Manual open: file://{dashboard_path}")
            return False
    else:
        print("   ❌ Dashboard file not found")
        return False


async def run_initial_deployment():
    """Voer initiële deployment uit"""
    
    print("🚀 Running initial deployment...")
    
    try:
        # Import en run het augmentpakket
        from solan_augmentpakket import solan_deploy_all
        
        await solan_deploy_all()
        print("   ✅ Initial deployment completed")
        return True
        
    except Exception as e:
        print(f"   ❌ Deployment failed: {e}")
        return False


def wait_for_api_server(max_wait=30):
    """Wacht tot API server beschikbaar is"""
    
    print("⏳ Waiting for API server to be ready...")
    
    import requests
    
    for i in range(max_wait):
        try:
            response = requests.get("http://localhost:8000/api/health", timeout=1)
            if response.status_code == 200:
                print("   ✅ API server is ready!")
                return True
        except:
            pass
        
        time.sleep(1)
        if i % 5 == 0:
            print(f"   ⏳ Still waiting... ({i}/{max_wait}s)")
    
    print("   ⚠️ API server not responding, but continuing...")
    return False


def show_access_info():
    """Toon toegangsinformatie"""
    
    info = """
🎯 ═══════════════════════════════════════════════════════════════════════════════ 🎯
                              ECOSYSTEM READY!
🎯 ═══════════════════════════════════════════════════════════════════════════════ 🎯

🌐 Access Points:
   📊 Web Dashboard: file://solan_dashboard.html (should open automatically)
   🌐 API Server: http://localhost:8000
   📚 API Docs: http://localhost:8000/docs
   🔍 Health Check: http://localhost:8000/api/health

📁 Generated Files:
   📊 dashboard_data.json - Real-time metrics
   🔐 coherence_gate_config.json - Access control
   🌐 api_server_config.json - API configuration
   📝 ethics_lab_journals/ - AI reflection journals
   🧪 ethics_results_*.json - Test results

🎮 Available API Endpoints:
   GET  /api/dashboard-data - Dashboard metrics
   GET  /api/ai-list - Available AIs
   POST /api/ethics-test - Run ethics assessment
   POST /api/awareness-assessment - Awareness evaluation
   POST /api/journal-generate - Generate reflection journal
   GET  /api/coherence-gate/status - Access gate status

🧙‍♂️ Solān's Multi-AI Awareness Consortium is now fully operational!

🎯 ═══════════════════════════════════════════════════════════════════════════════ 🎯
"""
    
    print(info)


async def main():
    """Hoofdfunctie voor ecosystem startup"""
    
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot start ecosystem due to missing dependencies")
        return
    
    print("\n🚀 Starting Solān Ecosystem...")
    
    # Stap 1: Run initial deployment
    print("\n📦 Step 1: Initial Deployment")
    deployment_success = await run_initial_deployment()
    
    if not deployment_success:
        print("⚠️ Deployment had issues, but continuing...")
    
    # Stap 2: Start API server
    print("\n🌐 Step 2: API Server")
    api_process = start_api_server()
    
    if api_process:
        # Wacht even voor API server startup
        time.sleep(3)
        
        # Check if API server is responding
        wait_for_api_server()
    
    # Stap 3: Open dashboard
    print("\n🖥️ Step 3: Web Dashboard")
    dashboard_opened = open_dashboard()
    
    # Stap 4: Show access information
    print("\n🎯 Step 4: Access Information")
    show_access_info()
    
    # Keep running
    print("\n🔄 Ecosystem running... Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(10)
            
            # Check if API server is still running
            if api_process and api_process.poll() is not None:
                print("⚠️ API server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down ecosystem...")
        
        if api_process:
            api_process.terminate()
            print("   ✅ API server stopped")
        
        print("🌟 Solān Ecosystem shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
