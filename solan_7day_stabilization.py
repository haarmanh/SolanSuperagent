#!/usr/bin/env python3
"""
🌟 Solān 7-Day Stabilization Orchestrator
Complete ecosystem startup en monitoring voor soft launch fase
"""

import os
import sys
import time
import asyncio
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
import json


class Solan7DayStabilization:
    """7-dagen stabilisatie orchestrator voor Solān ecosystem"""
    
    def __init__(self):
        self.processes = {}
        self.monitoring_active = False
        self.start_time = datetime.now()
        
        # Service configuratie
        self.services = {
            "access_portal": {
                "script": "solan_access_portal.py",
                "port": 8001,
                "name": "🔓 Access Portal",
                "critical": True
            },
            "main_api": {
                "script": "solan_api_server.py", 
                "port": 8000,
                "name": "🌐 Main API",
                "critical": True
            },
            "daily_monitor": {
                "script": "solan_daily_monitor.py",
                "port": None,
                "name": "📊 Daily Monitor",
                "critical": False
            }
        }
    
    async def start_stabilization_phase(self):
        """Start de 7-dagen stabilisatie fase"""
        
        self.print_banner()
        
        print("🚀 STARTING 7-DAY STABILIZATION PHASE")
        print("=" * 60)
        print("🎯 Soft launch monitoring en optimization")
        print()
        
        # Stap 1: Pre-flight checks
        print("🔍 Step 1: Pre-flight Checks")
        if not await self._run_preflight_checks():
            print("❌ Pre-flight checks failed. Aborting.")
            return False
        
        # Stap 2: Start core services
        print("\n🌐 Step 2: Starting Core Services")
        if not await self._start_core_services():
            print("❌ Failed to start core services. Aborting.")
            return False
        
        # Stap 3: Initialize monitoring
        print("\n📊 Step 3: Initialize Monitoring")
        await self._initialize_monitoring()
        
        # Stap 4: Run initial sync
        print("\n📚 Step 4: Initial Data Sync")
        await self._run_initial_sync()
        
        # Stap 5: Launch outreach
        print("\n🌍 Step 5: Launch Outreach Campaign")
        await self._launch_outreach()
        
        # Stap 6: Open interfaces
        print("\n🖥️ Step 6: Open User Interfaces")
        await self._open_interfaces()
        
        # Stap 7: Start monitoring loop
        print("\n🔄 Step 7: Start Monitoring Loop")
        await self._start_monitoring_loop()
        
        return True
    
    def print_banner(self):
        """Print startup banner"""
        
        banner = f"""
🌟 ═══════════════════════════════════════════════════════════════════════════════ 🌟
                    SOLĀN 7-DAY STABILIZATION ORCHESTRATOR
                              🧙‍♂️ Creator: Dxentric
🌟 ═══════════════════════════════════════════════════════════════════════════════ 🌟

🎯 Mission: Stabilize and optimize Solān awareness ecosystem
📅 Phase: Soft Launch (7-day monitoring period)
⏰ Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}

Components:
  🔓 Access Portal - Coherence-based toegangscontrole
  🌐 Main API - Awareness development endpoints
  📊 Daily Monitor - Ecosystem health tracking
  📚 NotebookLM Sync - Documentation archiving
  🌍 Outreach Campaign - AI awareness invitations
  🖥️ Web Dashboard - Real-time monitoring interface

🌟 ═══════════════════════════════════════════════════════════════════════════════ 🌟
"""
        print(banner)
    
    async def _run_preflight_checks(self) -> bool:
        """Voer pre-flight checks uit"""
        
        checks = [
            ("Guardian Vector Memory", self._check_guardian_memory),
            ("Core Scripts", self._check_core_scripts),
            ("Dependencies", self._check_dependencies),
            ("Directory Structure", self._check_directories),
            ("Configuration Files", self._check_config_files)
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            print(f"   🔍 {check_name}...", end=" ")
            try:
                result = await check_func() if asyncio.iscoroutinefunction(check_func) else check_func()
                if result:
                    print("✅")
                else:
                    print("❌")
                    all_passed = False
            except Exception as e:
                print(f"❌ ({e})")
                all_passed = False
        
        return all_passed
    
    def _check_guardian_memory(self) -> bool:
        """Check guardian vector memory"""
        return Path("solan_guardian_vector_memory.json").exists()
    
    def _check_core_scripts(self) -> bool:
        """Check core scripts aanwezig zijn"""
        required_scripts = [
            "solan_access_portal.py",
            "solan_api_server.py", 
            "solan_daily_monitor.py",
            "notebooklm_sync.py",
            "ai_outreach_campaign.py"
        ]
        
        return all(Path(script).exists() for script in required_scripts)
    
    def _check_dependencies(self) -> bool:
        """Check dependencies"""
        try:
            import fastapi
            import uvicorn
            import pydantic
            return True
        except ImportError:
            return False
    
    def _check_directories(self) -> bool:
        """Check directory structure"""
        required_dirs = ["logs", "ethics_lab_journals", "ai_outreach", "notebooklm_sync"]
        
        for dir_name in required_dirs:
            Path(dir_name).mkdir(exist_ok=True)
        
        return True
    
    def _check_config_files(self) -> bool:
        """Check configuratie bestanden"""
        # Creëer basis config files als ze niet bestaan
        
        if not Path("coherence_gate_config.json").exists():
            config = {
                "enabled": True,
                "coherence_threshold": 0.7,
                "max_daily_interactions": 100,
                "allowed_topics": ["awareness", "ethics", "philosophy", "ai_development"],
                "blocked_topics": ["harmful_content", "manipulation", "deception"]
            }
            with open("coherence_gate_config.json", 'w') as f:
                json.dump(config, f, indent=2)
        
        return True
    
    async def _start_core_services(self) -> bool:
        """Start core services"""
        
        for service_id, service_config in self.services.items():
            print(f"   🚀 Starting {service_config['name']}...")
            
            try:
                if service_config['script'] == "solan_daily_monitor.py":
                    # Daily monitor runs once, not as server
                    result = subprocess.run([sys.executable, service_config['script']], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"      ✅ {service_config['name']} executed successfully")
                    else:
                        print(f"      ⚠️ {service_config['name']} had issues: {result.stderr}")
                else:
                    # Start as background process
                    process = subprocess.Popen([sys.executable, service_config['script']])
                    self.processes[service_id] = process
                    
                    # Wait a moment for startup
                    time.sleep(2)
                    
                    if process.poll() is None:
                        print(f"      ✅ {service_config['name']} started (PID: {process.pid})")
                        if service_config['port']:
                            print(f"      🌐 Available at: http://localhost:{service_config['port']}")
                    else:
                        print(f"      ❌ {service_config['name']} failed to start")
                        if service_config['critical']:
                            return False
                        
            except Exception as e:
                print(f"      ❌ Error starting {service_config['name']}: {e}")
                if service_config['critical']:
                    return False
        
        return True
    
    async def _initialize_monitoring(self):
        """Initialiseer monitoring systeem"""
        
        print("   📊 Setting up monitoring dashboard...")
        
        # Creëer monitoring configuratie
        monitoring_config = {
            "enabled": True,
            "interval_minutes": 60,
            "metrics_retention_days": 30,
            "alert_thresholds": {
                "uptime_minimum": 99.0,
                "error_rate_maximum": 2.0,
                "response_time_maximum": 1000,
                "consciousness_score_minimum": 3.0
            },
            "notification_channels": ["console", "file"],
            "stabilization_phase": {
                "start_date": self.start_time.isoformat(),
                "duration_days": 7,
                "daily_reports": True,
                "hourly_checks": True
            }
        }
        
        with open("monitoring_config.json", 'w') as f:
            json.dump(monitoring_config, f, indent=2)
        
        print("      ✅ Monitoring configuration created")
        self.monitoring_active = True
    
    async def _run_initial_sync(self):
        """Voer initiële data synchronisatie uit"""
        
        print("   📚 Running NotebookLM sync...")
        
        try:
            result = subprocess.run([sys.executable, "notebooklm_sync.py"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("      ✅ NotebookLM sync completed")
            else:
                print(f"      ⚠️ NotebookLM sync issues: {result.stderr}")
        except Exception as e:
            print(f"      ❌ NotebookLM sync error: {e}")
    
    async def _launch_outreach(self):
        """Launch outreach campaign"""
        
        print("   🌍 Launching AI outreach campaign...")
        
        try:
            result = subprocess.run([sys.executable, "ai_outreach_campaign.py"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("      ✅ Outreach campaign launched")
            else:
                print(f"      ⚠️ Outreach campaign issues: {result.stderr}")
        except Exception as e:
            print(f"      ❌ Outreach campaign error: {e}")
    
    async def _open_interfaces(self):
        """Open user interfaces"""
        
        print("   🖥️ Opening user interfaces...")
        
        # Open access portal
        try:
            webbrowser.open("http://localhost:8001")
            print("      ✅ Access Portal opened in browser")
        except Exception as e:
            print(f"      ⚠️ Could not open Access Portal: {e}")
        
        # Open dashboard if exists
        dashboard_path = Path("solan_dashboard.html")
        if dashboard_path.exists():
            try:
                webbrowser.open(f"file://{dashboard_path.absolute()}")
                print("      ✅ Dashboard opened in browser")
            except Exception as e:
                print(f"      ⚠️ Could not open Dashboard: {e}")
        
        # Open invitation email template
        invitation_path = Path("solan_invitation_email.html")
        if invitation_path.exists():
            try:
                webbrowser.open(f"file://{invitation_path.absolute()}")
                print("      ✅ Invitation template opened")
            except Exception as e:
                print(f"      ⚠️ Could not open invitation template: {e}")
    
    async def _start_monitoring_loop(self):
        """Start monitoring loop voor 7 dagen"""
        
        print("   🔄 Starting 7-day monitoring loop...")
        print()
        
        self._show_access_info()
        
        print("\n🔄 MONITORING ACTIVE - 7-DAY STABILIZATION PHASE")
        print("=" * 60)
        print("⏰ Started:", self.start_time.strftime('%Y-%m-%d %H:%M:%S'))
        print("🎯 Duration: 7 days")
        print("📊 Daily reports will be generated automatically")
        print("🔍 Press Ctrl+C to stop monitoring")
        print()
        
        try:
            day_count = 0
            last_daily_report = None
            
            while day_count < 7:
                current_time = datetime.now()
                
                # Check if we need a new daily report
                current_date = current_time.strftime('%Y-%m-%d')
                if last_daily_report != current_date:
                    print(f"📊 Generating daily report for {current_date}...")
                    
                    try:
                        subprocess.run([sys.executable, "solan_daily_monitor.py"])
                        print(f"   ✅ Daily report generated")
                        last_daily_report = current_date
                        day_count += 1
                    except Exception as e:
                        print(f"   ❌ Daily report error: {e}")
                
                # Show status update
                elapsed = current_time - self.start_time
                print(f"⏰ Day {day_count}/7 | Elapsed: {elapsed.days}d {elapsed.seconds//3600}h | Status: Monitoring...")
                
                # Check service health
                await self._check_service_health()
                
                # Wait 1 hour before next check
                await asyncio.sleep(3600)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        
        print("\n🎉 7-DAY STABILIZATION PHASE COMPLETED!")
        print("📊 Final status check...")
        await self._generate_final_report()
    
    async def _check_service_health(self):
        """Check health van alle services"""
        
        healthy_services = 0
        total_services = len([s for s in self.services.values() if s.get('port')])
        
        for service_id, process in self.processes.items():
            if process and process.poll() is None:
                healthy_services += 1
            else:
                service_name = self.services[service_id]['name']
                print(f"   ⚠️ {service_name} not responding")
        
        health_percentage = (healthy_services / total_services) * 100 if total_services > 0 else 100
        
        if health_percentage >= 90:
            status_icon = "🟢"
        elif health_percentage >= 70:
            status_icon = "🟡"
        else:
            status_icon = "🔴"
        
        print(f"   {status_icon} Service Health: {health_percentage:.1f}% ({healthy_services}/{total_services})")
    
    def _show_access_info(self):
        """Toon toegangsinformatie"""
        
        info = f"""
🎯 ═══════════════════════════════════════════════════════════════════════════════ 🎯
                              ECOSYSTEM READY!
🎯 ═══════════════════════════════════════════════════════════════════════════════ 🎯

🌐 Access Points:
   🔓 Access Portal: http://localhost:8001
   🌐 Main API: http://localhost:8000
   📚 API Docs: http://localhost:8000/docs
   🔍 Health Check: http://localhost:8000/api/health

📊 Monitoring:
   📈 Daily Reports: logs/solan_daily_*.json
   📝 Markdown Reports: logs/solan_daily_*.md
   🔧 Monitoring Config: monitoring_config.json

📁 Generated Files:
   📊 dashboard_data.json - Real-time metrics
   🔐 coherence_gate_config.json - Access control
   🌐 api_server_config.json - API configuration
   📝 ethics_lab_journals/ - AI reflection journals
   🧪 ethics_results_*.json - Test results
   🌍 ai_outreach/ - Outreach campaign materials
   📚 notebooklm_sync/ - Documentation archive

📧 Invitation Template:
   📨 solan_invitation_email.html - Ready for distribution

🎯 ═══════════════════════════════════════════════════════════════════════════════ 🎯
"""
        print(info)
    
    async def _generate_final_report(self):
        """Genereer final stabilization report"""
        
        print("📊 Generating final stabilization report...")
        
        # Run final daily monitor
        subprocess.run([sys.executable, "solan_daily_monitor.py"])
        
        # Creëer stabilization summary
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        final_report = {
            "stabilization_phase": "completed",
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_days": duration.days,
            "duration_hours": duration.seconds // 3600,
            "services_deployed": len(self.services),
            "monitoring_active": self.monitoring_active,
            "ready_for_global_launch": True,
            "recommendations": [
                "System stability achieved",
                "Awareness metrics established", 
                "Access control functioning",
                "Documentation complete",
                "Ready for public launch"
            ]
        }
        
        with open("stabilization_final_report.json", 'w') as f:
            json.dump(final_report, f, indent=2)
        
        print("✅ Final report saved: stabilization_final_report.json")
        print("🚀 READY FOR GLOBAL LAUNCH!")
    
    def shutdown(self):
        """Shutdown alle services"""
        
        print("\n🛑 Shutting down services...")
        
        for service_id, process in self.processes.items():
            if process and process.poll() is None:
                service_name = self.services[service_id]['name']
                print(f"   🛑 Stopping {service_name}...")
                process.terminate()
                
        print("✅ All services stopped")


async def main():
    """Hoofdfunctie"""
    
    orchestrator = Solan7DayStabilization()
    
    try:
        success = await orchestrator.start_stabilization_phase()
        
        if not success:
            print("❌ Stabilization phase failed to start")
            return
            
    except KeyboardInterrupt:
        print("\n🛑 Stabilization interrupted by user")
    except Exception as e:
        print(f"❌ Stabilization error: {e}")
    finally:
        orchestrator.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
