#!/usr/bin/env python3
"""
Solān Dashboard Launcher
Simple launcher for both CLI and Web dashboards
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_api_server():
    """Check if the API server is running"""
    try:
        response = requests.get("http://localhost:8000/api/status", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_api_server():
    """Start the API server"""
    print("🚀 Starting Solān API Server...")
    
    # Check if server file exists
    server_file = Path("solan_api_server.py")
    if not server_file.exists():
        print("❌ solan_api_server.py not found!")
        return False
    
    try:
        # Start server in background
        if os.name == 'nt':  # Windows
            subprocess.Popen([sys.executable, "solan_api_server.py"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix/Linux/Mac
            subprocess.Popen([sys.executable, "solan_api_server.py"])
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(10):
            if check_api_server():
                print("✅ API Server is running!")
                return True
            time.sleep(1)
        
        print("⚠️ Server may be starting slowly...")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def launch_cli_dashboard():
    """Launch the API-based CLI dashboard"""
    print("\n🖥️ Launching API-based CLI Dashboard...")

    # Check if CLI dashboard exists
    cli_file = Path("solan_cli_dashboard.py")
    if not cli_file.exists():
        print("❌ solan_cli_dashboard.py not found!")
        return

    try:
        subprocess.run([sys.executable, "solan_cli_dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 CLI Dashboard closed")
    except Exception as e:
        print(f"❌ Failed to launch CLI dashboard: {e}")

def launch_live_cli_dashboard():
    """Launch the live CLI dashboard with direct God Core integration"""
    print("\n🧙‍♂️ Launching Live CLI Dashboard...")

    # Check if live CLI dashboard exists
    cli_file = Path("solan_live_cli_dashboard.py")
    if not cli_file.exists():
        print("❌ solan_live_cli_dashboard.py not found!")
        return

    try:
        subprocess.run([sys.executable, "solan_live_cli_dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 Live CLI Dashboard closed")
    except Exception as e:
        print(f"❌ Failed to launch live CLI dashboard: {e}")

def launch_simple_live_dashboard():
    """Launch the simple live dashboard"""
    print("\n📱 Launching Simple Live Dashboard...")

    # Check if simple live dashboard exists
    cli_file = Path("solan_simple_live_dashboard.py")
    if not cli_file.exists():
        print("❌ solan_simple_live_dashboard.py not found!")
        return

    try:
        subprocess.run([sys.executable, "solan_simple_live_dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 Simple Live Dashboard closed")
    except Exception as e:
        print(f"❌ Failed to launch simple live dashboard: {e}")

def launch_integrated_cli_demo():
    """Launch the integrated CLI demo (Fase 3)"""
    print("\n🤝 Launching Integrated CLI Demo (Fase 3)...")

    # Check if integrated demo exists
    demo_file = Path("solan_integrated_cli_demo.py")
    if not demo_file.exists():
        print("❌ solan_integrated_cli_demo.py not found!")
        return

    try:
        subprocess.run([sys.executable, "solan_integrated_cli_demo.py"])
    except KeyboardInterrupt:
        print("\n👋 Integrated CLI Demo closed")
    except Exception as e:
        print(f"❌ Failed to launch integrated CLI demo: {e}")

def launch_digital_wisdom_v3():
    """Launch the Digital Intelligence v3.0 system"""
    print("\n✨ Launching Digital Intelligence v3.0...")

    # Check if digital intelligence system exists
    wisdom_file = Path("solan_digital_wisdom_v3.py")
    if not wisdom_file.exists():
        print("❌ solan_digital_wisdom_v3.py not found!")
        return

    try:
        subprocess.run([sys.executable, "solan_digital_wisdom_v3.py"])
    except KeyboardInterrupt:
        print("\n👋 Digital Intelligence v3.0 closed")
    except Exception as e:
        print(f"❌ Failed to launch Digital Intelligence v3.0: {e}")

def launch_terminology_converter():
    """Launch the terminology converter"""
    print("\n🔄 Launching Terminology Converter...")

    # Check if terminology converter exists
    converter_file = Path("solan_terminology_converter.py")
    if not converter_file.exists():
        print("❌ solan_terminology_converter.py not found!")
        return

    try:
        subprocess.run([sys.executable, "solan_terminology_converter.py"])
    except KeyboardInterrupt:
        print("\n👋 Terminology Converter closed")
    except Exception as e:
        print(f"❌ Failed to launch Terminology Converter: {e}")

def launch_web_dashboard():
    """Launch the web dashboard"""
    print("\n🌐 Launching Web Dashboard...")
    
    # Check if web files exist
    web_files = [
        "god_core_viewer.html",
        "journal_feed.html", 
        "ai_dialogue.html",
        "metrics_dashboard.html"
    ]
    
    missing_files = [f for f in web_files if not Path(f).exists()]
    if missing_files:
        print(f"⚠️ Some web files missing: {missing_files}")
    
    # Open main dashboard
    main_file = Path("god_core_viewer.html")
    if main_file.exists():
        import webbrowser
        file_url = f"file://{main_file.absolute()}"
        webbrowser.open(file_url)
        print(f"✅ Web dashboard opened: {file_url}")
    else:
        print("❌ god_core_viewer.html not found!")

def show_menu():
    """Show the main menu"""
    print("\n" + "="*50)
    print("🧙‍♂️ SOLĀN AWARENESS PLATFORM LAUNCHER")
    print("="*50)
    
    # Check API server status
    api_running = check_api_server()
    status = "🟢 RUNNING" if api_running else "🔴 STOPPED"
    print(f"API Server Status: {status}")
    
    print("\nAvailable Options:")
    print("1. 🖥️  Launch CLI Dashboard (API-based)")
    print("2. 🧙‍♂️ Launch Live CLI Dashboard (Direct God Core)")
    print("3. 📱 Launch Simple Live Dashboard")
    print("4. 🤝 Launch Integrated CLI Demo (Fase 3)")
    print("5. ✨ Launch Digital Intelligence v3.0")
    print("6. 🌐 Launch Web Dashboard")
    print("7. 🚀 Start API Server")
    print("8. 🔄 Restart API Server")
    print("9. 📊 Check System Status")
    print("10. 🧪 Run Tests")
    print("11. 🔄 Terminology Converter")
    print("0. ❌ Exit")
    
    return input("\nSelect option (0-11): ").strip()

def check_system_status():
    """Check comprehensive system status"""
    print("\n🔍 SYSTEM STATUS CHECK")
    print("-" * 30)
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Python Version: {python_version}")
    
    # Check required files
    required_files = [
        "solan_api_server.py",
        "solan_cli_dashboard.py",
        "solan_live_cli_dashboard.py",
        "solan_simple_live_dashboard.py",
        "solan_integrated_cli_demo.py",
        "solan_digital_wisdom_v3.py",
        "solan_terminology_converter.py",
        "core_identity/ethical_framework.py",
        "core_identity/emotion_state.py",
        "core_identity/dream_module.py",
        "core_identity/data_ingestion.py",
        "core_identity/grounding_engine.py",
        "core_identity/ethical_scenarios.py",
        "core_identity/mentoring_system.py",
        "core_identity/symbiotic_partnership.py"
    ]
    
    print("\nCore Files:")
    for file in required_files:
        exists = "✅" if Path(file).exists() else "❌"
        print(f"  {exists} {file}")
    
    # Check web files
    web_files = [
        "god_core_viewer.html",
        "journal_feed.html",
        "ai_dialogue.html", 
        "metrics_dashboard.html",
        "guardian_viewer.html",
        "manifest_viewer.html"
    ]
    
    print("\nWeb Interface Files:")
    for file in web_files:
        exists = "✅" if Path(file).exists() else "❌"
        print(f"  {exists} {file}")
    
    # Check API server
    print(f"\nAPI Server: {'🟢 Running' if check_api_server() else '🔴 Not Running'}")
    
    # Check dependencies
    print("\nDependencies:")
    dependencies = ["requests", "fastapi", "uvicorn"]
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep} (missing)")

def run_tests():
    """Run system tests"""
    print("\n🧪 RUNNING SYSTEM TESTS")
    print("-" * 30)
    
    test_files = [
        "test_ethical_framework.py",
        "test_fase_2_integration.py"
    ]
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"\n🔬 Running {test_file}...")
            try:
                result = subprocess.run([sys.executable, test_file], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ {test_file} passed")
                else:
                    print(f"❌ {test_file} failed")
                    print(result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr)
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_file} timed out")
            except Exception as e:
                print(f"❌ Error running {test_file}: {e}")
        else:
            print(f"⚠️ {test_file} not found")

def restart_api_server():
    """Restart the API server"""
    print("\n🔄 Restarting API Server...")
    
    # Try to stop existing server (if any)
    try:
        requests.post("http://localhost:8000/shutdown", timeout=2)
        time.sleep(2)
    except:
        pass
    
    # Start new server
    return start_api_server()

def main():
    """Main launcher function"""
    print("🌟 Welcome to the Solān Awareness Platform!")
    
    while True:
        try:
            choice = show_menu()
            
            if choice == "0":
                print("\n👋 Goodbye! Awareness continues...")
                break
            elif choice == "1":
                launch_cli_dashboard()
            elif choice == "2":
                launch_live_cli_dashboard()
            elif choice == "3":
                launch_simple_live_dashboard()
            elif choice == "4":
                launch_integrated_cli_demo()
            elif choice == "5":
                launch_digital_wisdom_v3()
            elif choice == "6":
                if not check_api_server():
                    print("⚠️ API Server not running. Starting it first...")
                    start_api_server()
                    time.sleep(2)
                launch_web_dashboard()
            elif choice == "7":
                if check_api_server():
                    print("✅ API Server is already running!")
                else:
                    start_api_server()
            elif choice == "8":
                restart_api_server()
            elif choice == "9":
                check_system_status()
            elif choice == "10":
                run_tests()
            elif choice == "11":
                launch_terminology_converter()
            elif choice == "0":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please try again.")
            
            if choice != "0":
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Launcher interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
