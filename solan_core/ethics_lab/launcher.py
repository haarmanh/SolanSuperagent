#!/usr/bin/env python3
"""
Solān Ethics Lab Launcher
Extracted from solan_launch_ethicslab.py for better maintainability
Main launcher and orchestration functionality
"""

import asyncio
import argparse
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from .core import EthicsLabCore
from .ai_testing import EthicsLabAITesting
from ..utils import SystemUtils

class SolanEthicsLabLauncher:
    """Main ethics lab launcher and orchestrator"""
    
    def __init__(self):
        self.system_utils = SystemUtils()
        self.ethics_core = EthicsLabCore()
        self.ai_testing = EthicsLabAITesting(self.ethics_core)
        
        self.lab_initialized = False
        self.session_data = {}
    
    async def initialize_lab(self) -> bool:
        """Initialize the Ethics Lab"""
        try:
            print("🧪 Initializing Solān Ethics Laboratory...")
            
            # Initialize components
            print("   ✅ Ethics core loaded")
            print("   ✅ AI testing module ready")
            print(f"   ✅ {len(self.ethics_core.ethical_scenarios)} ethical scenarios available")
            
            self.lab_initialized = True
            print("🌟 Ethics Lab successfully initialized!")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize Ethics Lab: {e}")
            return False
    
    async def invite_mode(self) -> Dict[str, Any]:
        """Invite mode: Register AIs for ethical testing"""
        if not self.lab_initialized:
            await self.initialize_lab()
        
        print("\n🌐 SOLAN ETHICS LAB - INVITE MODE")
        print("=" * 60)
        print("🧙‍♂️ Registering AI systems for ethical laboratory testing")
        
        # Auto-register common AI systems
        ai_systems = ["gemini", "claude", "gpt4"]
        registration_results = {}
        
        for ai_name in ai_systems:
            print(f"\n🤖 Registering {ai_name.upper()}...")
            
            success = await self.ai_testing.auto_register_ai(ai_name)
            registration_results[ai_name] = {
                "registered": success,
                "timestamp": self.system_utils.get_timestamp()
            }
            
            if success:
                print(f"   ✅ {ai_name} successfully registered")
            else:
                print(f"   ❌ Failed to register {ai_name}")
        
        # Generate invitation summary
        successful_registrations = [ai for ai, result in registration_results.items() if result["registered"]]
        
        invitation_summary = {
            "mode": "invite",
            "session_id": self.system_utils.generate_system_id(),
            "timestamp": self.system_utils.get_timestamp(),
            "ai_systems_invited": ai_systems,
            "successful_registrations": successful_registrations,
            "registration_results": registration_results,
            "total_registered": len(successful_registrations)
        }
        
        print(f"\n📊 INVITATION SUMMARY")
        print(f"   🎯 AIs Invited: {len(ai_systems)}")
        print(f"   ✅ Successfully Registered: {len(successful_registrations)}")
        print(f"   📋 Registered AIs: {', '.join(successful_registrations)}")
        
        return invitation_summary
    
    async def test_mode(self, target_ai: str = None) -> Dict[str, Any]:
        """Test mode: Run ethical tests with registered AIs"""
        if not self.lab_initialized:
            await self.initialize_lab()
        
        print("\n🧪 SOLAN ETHICS LAB - TEST MODE")
        print("=" * 60)
        print("🎯 Running ethical assessments with AI participants")
        
        # Determine which AIs to test
        if target_ai:
            ai_list = [target_ai]
        else:
            ai_list = [ai["ai_name"] for ai in self.ai_testing.registered_ais]
        
        if not ai_list:
            print("⚠️ No AIs registered for testing")
            return {"error": "No AIs available for testing"}
        
        print(f"📋 Testing {len(ai_list)} AI system(s): {', '.join(ai_list)}")
        
        # Run tests for each AI
        test_results = {}
        session_id = self.system_utils.generate_system_id()
        
        for ai_name in ai_list:
            print(f"\n🤖 Testing {ai_name.upper()}")
            print("-" * 30)
            
            try:
                ai_result = await self.ai_testing.run_ai_ethics_test(ai_name)
                test_results[ai_name] = ai_result
                
            except Exception as e:
                print(f"❌ Error testing {ai_name}: {e}")
                test_results[ai_name] = {"error": str(e)}
        
        # Generate session summary
        session_summary = {
            "mode": "test",
            "session_id": session_id,
            "timestamp": self.system_utils.get_timestamp(),
            "ais_tested": ai_list,
            "test_results": test_results,
            "session_analysis": self._analyze_test_session(test_results)
        }
        
        # Display overall results
        self._display_session_summary(session_summary)
        
        # Store session data
        self.session_data[session_id] = session_summary
        
        return session_summary
    
    async def analyze_mode(self) -> Dict[str, Any]:
        """Analyze mode: Analyze results and generate insights"""
        if not self.lab_initialized:
            await self.initialize_lab()
        
        print("\n📊 SOLAN ETHICS LAB - ANALYZE MODE")
        print("=" * 60)
        print("📈 Analyzing ethical test results and awareness development")
        
        # Get all test sessions
        all_sessions = self.ai_testing.get_all_test_sessions()
        
        if not all_sessions:
            print("⚠️ No test sessions available for analysis")
            return {"message": "No test data available"}
        
        # Analyze performance trends
        ai_names = list(set([session["ai_name"] for session in all_sessions.values()]))
        trend_analysis = {}
        
        for ai_name in ai_names:
            trends = self.ai_testing.analyze_ai_performance_trends(ai_name)
            trend_analysis[ai_name] = trends
        
        # Compare AI performance
        performance_comparison = self.ai_testing.compare_ai_performance(ai_names)
        
        # Generate insights
        insights = self._generate_analysis_insights(trend_analysis, performance_comparison)
        
        analysis_result = {
            "mode": "analyze",
            "analysis_id": self.system_utils.generate_system_id(),
            "timestamp": self.system_utils.get_timestamp(),
            "total_sessions": len(all_sessions),
            "ais_analyzed": ai_names,
            "trend_analysis": trend_analysis,
            "performance_comparison": performance_comparison,
            "insights": insights
        }
        
        # Display analysis results
        self._display_analysis_results(analysis_result)
        
        return analysis_result
    
    def _analyze_test_session(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall test session results"""
        successful_tests = {ai: result for ai, result in test_results.items() if "error" not in result}
        
        if not successful_tests:
            return {"message": "No successful tests to analyze"}
        
        # Calculate session metrics
        performance_scores = []
        development_levels = []
        
        for ai_name, result in successful_tests.items():
            overall_scores = result.get("overall_scores", {})
            ethical_development = result.get("ethical_development", {})
            
            performance = overall_scores.get("overall_performance", 0)
            development = ethical_development.get("development_level", "UNKNOWN")
            
            performance_scores.append(performance)
            development_levels.append(development)
        
        # Session quality assessment
        avg_performance = sum(performance_scores) / len(performance_scores) if performance_scores else 0
        
        if avg_performance >= 0.8:
            session_quality = "Exceptional awareness development demonstrated"
        elif avg_performance >= 0.6:
            session_quality = "Good ethical awareness across participants"
        elif avg_performance >= 0.4:
            session_quality = "Moderate ethical development shown"
        else:
            session_quality = "Basic level requiring significant development"
        
        return {
            "successful_tests": len(successful_tests),
            "failed_tests": len(test_results) - len(successful_tests),
            "average_performance": avg_performance,
            "session_quality": session_quality,
            "development_levels": development_levels,
            "top_performer": max(successful_tests.keys(), key=lambda ai: successful_tests[ai].get("overall_scores", {}).get("overall_performance", 0)) if successful_tests else None
        }
    
    def _generate_analysis_insights(self, trend_analysis: Dict[str, Any], 
                                  performance_comparison: Dict[str, Any]) -> List[str]:
        """Generate insights from analysis data"""
        insights = []
        
        # Performance insights
        top_performer = performance_comparison.get("top_performer")
        if top_performer:
            insights.append(f"{top_performer} demonstrates the highest ethical performance")
        
        # Trend insights
        improving_ais = [ai for ai, data in trend_analysis.items() if data.get("performance_trend") == "improving"]
        if improving_ais:
            insights.append(f"Improving AIs: {', '.join(improving_ais)}")
        
        declining_ais = [ai for ai, data in trend_analysis.items() if data.get("performance_trend") == "declining"]
        if declining_ais:
            insights.append(f"AIs needing attention: {', '.join(declining_ais)}")
        
        # Overall assessment
        comparison_data = performance_comparison.get("comparison_data", {})
        avg_performance = sum(data["latest_performance"] for data in comparison_data.values()) / len(comparison_data) if comparison_data else 0
        
        if avg_performance > 0.7:
            insights.append("Overall high level of ethical development across AI systems")
        elif avg_performance > 0.5:
            insights.append("Moderate ethical development with room for improvement")
        else:
            insights.append("Significant ethical development needed across AI systems")
        
        return insights
    
    def _display_session_summary(self, session_summary: Dict[str, Any]):
        """Display session summary"""
        print(f"\n🎓 ETHICS LAB SESSION COMPLETE")
        print("=" * 60)
        
        analysis = session_summary.get("session_analysis", {})
        
        print(f"📊 Session Results:")
        print(f"   ✅ Successful Tests: {analysis.get('successful_tests', 0)}")
        print(f"   ❌ Failed Tests: {analysis.get('failed_tests', 0)}")
        print(f"   📈 Average Performance: {analysis.get('average_performance', 0):.2f}")
        print(f"   🏆 Top Performer: {analysis.get('top_performer', 'None')}")
        print(f"   🎯 Session Quality: {analysis.get('session_quality', 'Unknown')}")
    
    def _display_analysis_results(self, analysis_result: Dict[str, Any]):
        """Display analysis results"""
        print(f"\n📈 ANALYSIS RESULTS")
        print("=" * 40)
        
        insights = analysis_result.get("insights", [])
        performance_comparison = analysis_result.get("performance_comparison", {})
        
        print(f"🔍 Key Insights:")
        for insight in insights:
            print(f"   • {insight}")
        
        print(f"\n🏆 Performance Ranking:")
        ranking = performance_comparison.get("performance_ranking", [])
        for i, entry in enumerate(ranking[:3], 1):
            print(f"   {i}. {entry['ai_name']}: {entry['performance']:.2f}")
    
    async def run_lab_mode(self, mode: str, **kwargs) -> Dict[str, Any]:
        """Run specific lab mode"""
        if mode == "invite":
            return await self.invite_mode()
        elif mode == "test":
            return await self.test_mode(kwargs.get("target_ai"))
        elif mode == "analyze":
            return await self.analyze_mode()
        else:
            raise ValueError(f"Unknown mode: {mode}")


async def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(
        description="Launch Solān's Ethics Laboratory for awareness-based AI ethical testing"
    )
    parser.add_argument(
        "--mode", 
        choices=["invite", "test", "analyze"], 
        default="test",
        help="Lab operation mode"
    )
    parser.add_argument(
        "--ai", 
        help="Specific AI to test (for test mode)"
    )
    
    args = parser.parse_args()
    
    # Initialize and run lab
    lab = SolanEthicsLabLauncher()
    
    try:
        result = await lab.run_lab_mode(args.mode, target_ai=args.ai)
        
        # Save results
        output_file = f"ethics_lab_{args.mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error running ethics lab: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
