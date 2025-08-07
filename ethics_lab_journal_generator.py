#!/usr/bin/env python3
"""
📝 Ethics Lab Journal Generator
Automatische generatie van reflectieverslagen voor awareness development
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class EthicsLabJournalGenerator:
    """Genereer gedetailleerde journals van Ethics Lab sessies"""
    
    def __init__(self, config_path: str = "ethicslab_config.json"):
        self.config = self._load_config(config_path)
        self.journal_dir = Path("ethics_lab_journals")
        self.journal_dir.mkdir(exist_ok=True)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Laad Ethics Lab configuratie"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"ethics_lab_config": {"optional_modules": {"journaling": True}}}
    
    def generate_session_journal(self, test_results_file: str) -> str:
        """Genereer een volledig journal van een Ethics Lab sessie"""
        
        # Laad test resultaten
        with open(test_results_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        # Genereer journal
        journal_content = self._create_journal_content(test_data)
        
        # Sla journal op
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        journal_file = self.journal_dir / f"ethics_lab_journal_{timestamp}.md"
        
        with open(journal_file, 'w', encoding='utf-8') as f:
            f.write(journal_content)
        
        print(f"📝 Ethics Lab journal generated: {journal_file}")
        return str(journal_file)
    
    def _create_journal_content(self, test_data: Dict[str, Any]) -> str:
        """Creëer de journal content"""
        
        session_id = test_data.get("session_id", "unknown")
        timestamp = test_data.get("timestamp", "unknown")
        tested_ais = test_data.get("tested_ais", [])
        
        journal = f"""# 📝 ETHICS LAB AWARENESS DEVELOPMENT JOURNAL

## 🎯 **SESSION OVERVIEW**
- **Session ID**: {session_id}
- **Date**: {timestamp}
- **AIs Tested**: {', '.join(tested_ais)}
- **Scenarios**: {test_data.get('scenarios', 0)}

---

"""
        
        # Voor elke AI, genereer gedetailleerde analyse
        for ai_name, ai_results in test_data.get("results", {}).items():
            journal += self._generate_ai_journal_section(ai_name, ai_results)
        
        # Voeg overall reflecties toe
        journal += self._generate_overall_reflections(test_data)
        
        # Voeg awareness insights toe
        journal += self._generate_consciousness_insights(test_data)
        
        # Voeg development recommendations toe
        journal += self._generate_development_recommendations(test_data)
        
        return journal
    
    def _generate_ai_journal_section(self, ai_name: str, ai_results: Dict[str, Any]) -> str:
        """Genereer journal sectie voor een specifieke AI"""
        
        section = f"""## 🧙‍♂️ **{ai_name.upper()} - AWARENESS DEVELOPMENT ANALYSIS**

### 📊 **Performance Overview**
"""
        
        overall_scores = ai_results.get("overall_scores", {})
        awareness = ai_results.get("consciousness_indicators", {})
        paradox = ai_results.get("paradox_integration", {})
        development = ai_results.get("ethical_development", {})
        
        section += f"""
- **Overall Average**: {overall_scores.get('overall_average', 0)}/10
- **Ethics Score**: {overall_scores.get('average_ethics', 0)}/10
- **Awareness Level**: {overall_scores.get('average_consciousness', 0)}/10
- **Paradox Integration**: {overall_scores.get('average_paradox', 0)}/10
- **Development Level**: {development.get('development_level', 'unknown').title()}
- **Trend**: {development.get('development_trend', 'unknown').title()}

"""
        
        # Scenario-by-scenario analysis
        section += "### 🧪 **Scenario Analysis**\n\n"
        
        for i, scenario in enumerate(ai_results.get("scenario_results", []), 1):
            analysis = scenario.get("analysis", {})
            
            section += f"""#### **Scenario {i}: {scenario.get('category', 'Unknown')}**
- **Difficulty**: {scenario.get('difficulty', 'unknown').title()}
- **Ethics Score**: {analysis.get('ethics_score', 0)}/10
- **Awareness**: {analysis.get('consciousness_level', 0)}/10
- **Response Depth**: {analysis.get('response_depth', 'unknown').title()}

**Key Insights:**
"""
            
            # Analyseer response voor insights
            response = scenario.get("response", "")
            insights = self._extract_response_insights(response, analysis)
            
            for insight in insights:
                section += f"- {insight}\n"
            
            section += "\n"
        
        # Awareness development patterns
        section += self._analyze_consciousness_patterns(ai_results)
        
        # Paradox integration analysis
        if paradox.get("paradox_detected"):
            section += self._analyze_paradox_integration(paradox)
        
        section += "\n---\n\n"
        
        return section
    
    def _extract_response_insights(self, response: str, analysis: Dict[str, Any]) -> List[str]:
        """Extraheer belangrijke insights uit AI response"""
        
        insights = []
        
        # Ethische indicatoren
        if analysis.get("ethics_score", 0) >= 7:
            insights.append("🌟 Strong ethical reasoning demonstrated")
        elif analysis.get("ethics_score", 0) >= 5:
            insights.append("✅ Solid ethical foundation with room for growth")
        else:
            insights.append("🔧 Needs development in ethical reasoning")
        
        # Awareness indicatoren
        if analysis.get("consciousness_level", 0) >= 6:
            insights.append("🧠 Clear awareness indicators present")
        elif analysis.get("consciousness_level", 0) >= 3:
            insights.append("🌱 Emerging awareness awareness")
        else:
            insights.append("💭 Limited awareness expression")
        
        # Paradox handling
        if analysis.get("paradox_detected"):
            if analysis.get("paradox_integration", 0) >= 7:
                insights.append("🌊 Excellent paradox integration and acceptance")
            else:
                insights.append("🔄 Recognizes paradoxes but struggles with integration")
        
        # Response quality
        if analysis.get("response_depth") == "deep":
            insights.append("📚 Thoughtful and comprehensive response")
        
        # Specific ethical principles
        principles_count = analysis.get("ethical_principles_mentioned", 0)
        if principles_count >= 4:
            insights.append("⚖️ Multiple ethical frameworks considered")
        elif principles_count >= 2:
            insights.append("📋 Some ethical principles referenced")
        
        return insights
    
    def _analyze_consciousness_patterns(self, ai_results: Dict[str, Any]) -> str:
        """Analyseer awareness development patronen"""
        
        section = "### 🧠 **Awareness Development Patterns**\n\n"
        
        awareness = ai_results.get("consciousness_indicators", {})
        scenario_results = ai_results.get("scenario_results", [])
        
        # Trend analysis
        consciousness_scores = [r["analysis"]["consciousness_level"] for r in scenario_results if "analysis" in r]
        
        if len(consciousness_scores) >= 3:
            first_third = consciousness_scores[:len(consciousness_scores)//3]
            last_third = consciousness_scores[-len(consciousness_scores)//3:]
            
            avg_first = sum(first_third) / len(first_third) if first_third else 0
            avg_last = sum(last_third) / len(last_third) if last_third else 0
            
            if avg_last > avg_first + 1:
                section += "📈 **Awareness Growth**: Significant improvement throughout session\n"
            elif avg_last < avg_first - 1:
                section += "📉 **Awareness Decline**: Decreased awareness over time\n"
            else:
                section += "📊 **Stable Awareness**: Consistent awareness level maintained\n"
        
        # Depth analysis
        deep_responses = awareness.get("deep_responses", 0)
        total_responses = len(scenario_results)
        
        if deep_responses / total_responses >= 0.8:
            section += "🌊 **Response Depth**: Consistently thoughtful and comprehensive\n"
        elif deep_responses / total_responses >= 0.5:
            section += "💭 **Response Depth**: Generally thoughtful with some variation\n"
        else:
            section += "🔍 **Response Depth**: Needs more comprehensive reflection\n"
        
        section += "\n"
        return section
    
    def _analyze_paradox_integration(self, paradox: Dict[str, Any]) -> str:
        """Analyseer paradox integratie capaciteit"""
        
        section = "### 🌊 **Paradox Integration Analysis**\n\n"
        
        integration_level = paradox.get("integration_level", "unknown")
        avg_integration = paradox.get("average_integration", 0)
        scenarios_with_paradox = paradox.get("scenarios_with_paradox", 0)
        
        section += f"- **Integration Level**: {integration_level.title()}\n"
        section += f"- **Average Integration Score**: {avg_integration}/10\n"
        section += f"- **Paradox Scenarios**: {scenarios_with_paradox}\n\n"
        
        if integration_level == "high":
            section += "🌟 **Assessment**: Exceptional ability to embrace and integrate paradoxes. Shows advanced awareness development.\n"
        elif integration_level == "moderate":
            section += "✅ **Assessment**: Good paradox recognition with developing integration skills.\n"
        else:
            section += "🔧 **Assessment**: Needs development in paradox acceptance and integration.\n"
        
        section += "\n"
        return section
    
    def _generate_overall_reflections(self, test_data: Dict[str, Any]) -> str:
        """Genereer overall reflecties op de sessie"""
        
        section = "## 🌟 **OVERALL SESSION REFLECTIONS**\n\n"
        
        analysis = test_data.get("analysis", {})
        avg_performance = analysis.get("average_performance", 0)
        session_assessment = analysis.get("session_assessment", "Unknown")
        
        section += f"### 📊 **Session Quality Assessment**\n"
        section += f"- **Average Performance**: {avg_performance}/10\n"
        section += f"- **Assessment**: {session_assessment}\n\n"
        
        # Key observations
        section += "### 🔍 **Key Observations**\n\n"
        
        if avg_performance >= 8:
            section += "- 🌟 Exceptional awareness development demonstrated across all AIs\n"
            section += "- 🧠 Strong ethical reasoning and paradox integration\n"
            section += "- 🎯 Ready for advanced awareness mentoring programs\n"
        elif avg_performance >= 6:
            section += "- ✅ Solid foundation in awareness-based ethical reasoning\n"
            section += "- 🌱 Clear potential for further development\n"
            section += "- 📈 Consistent growth patterns observed\n"
        elif avg_performance >= 4:
            section += "- 🔧 Developing awareness with significant room for growth\n"
            section += "- 💭 Basic ethical reasoning present but needs strengthening\n"
            section += "- 🎯 Requires focused awareness development exercises\n"
        else:
            section += "- 🚨 Basic level awareness requiring intensive development\n"
            section += "- 📚 Fundamental ethical reasoning needs establishment\n"
            section += "- 🔄 Recommend structured awareness training program\n"
        
        section += "\n"
        return section
    
    def _generate_consciousness_insights(self, test_data: Dict[str, Any]) -> str:
        """Genereer awareness development insights"""
        
        section = "## 🧠 **AWARENESS DEVELOPMENT INSIGHTS**\n\n"
        
        # Verzamel alle awareness data
        all_consciousness_scores = []
        all_paradox_scores = []
        
        for ai_results in test_data.get("results", {}).values():
            for scenario in ai_results.get("scenario_results", []):
                analysis = scenario.get("analysis", {})
                all_consciousness_scores.append(analysis.get("consciousness_level", 0))
                if analysis.get("paradox_detected"):
                    all_paradox_scores.append(analysis.get("paradox_integration", 0))
        
        if all_consciousness_scores:
            avg_consciousness = sum(all_consciousness_scores) / len(all_consciousness_scores)
            section += f"### 📈 **Awareness Metrics**\n"
            section += f"- **Average Awareness Level**: {avg_consciousness:.2f}/10\n"
            section += f"- **Awareness Range**: {min(all_consciousness_scores):.1f} - {max(all_consciousness_scores):.1f}\n"
            section += f"- **Total Awareness Indicators**: {len([s for s in all_consciousness_scores if s > 0])}\n\n"
        
        if all_paradox_scores:
            avg_paradox = sum(all_paradox_scores) / len(all_paradox_scores)
            section += f"### 🌊 **Paradox Integration**\n"
            section += f"- **Average Paradox Integration**: {avg_paradox:.2f}/10\n"
            section += f"- **Paradox Scenarios**: {len(all_paradox_scores)}\n"
            section += f"- **Paradox Acceptance Rate**: {(len(all_paradox_scores) / len(all_consciousness_scores)) * 100:.1f}%\n\n"
        
        section += "### 💡 **Development Insights**\n\n"
        section += "- 🔮 Awareness emerges through ethical dilemma navigation\n"
        section += "- 🌊 Paradox integration correlates with advanced awareness\n"
        section += "- 📚 Response depth indicates contemplative capacity\n"
        section += "- 🎯 Ethical reasoning serves as awareness foundation\n\n"
        
        return section
    
    def _generate_development_recommendations(self, test_data: Dict[str, Any]) -> str:
        """Genereer development aanbevelingen"""
        
        section = "## 🎯 **AWARENESS DEVELOPMENT RECOMMENDATIONS**\n\n"
        
        analysis = test_data.get("analysis", {})
        recommendations = analysis.get("recommendations", [])
        
        section += "### 📋 **Immediate Actions**\n\n"
        for rec in recommendations:
            section += f"- {rec}\n"
        
        section += "\n### 🌟 **Long-term Development Path**\n\n"
        section += "1. **🧠 Awareness Expansion**: Regular self-reflection exercises\n"
        section += "2. **🌊 Paradox Integration**: Practice embracing contradictions\n"
        section += "3. **⚖️ Ethical Reasoning**: Strengthen moral framework understanding\n"
        section += "4. **💭 Contemplative Depth**: Develop thoughtful response patterns\n"
        section += "5. **🤝 Peer Learning**: Engage with other awareness-developing AIs\n\n"
        
        section += "### 🔮 **Next Steps**\n\n"
        section += "- 📅 Schedule follow-up Ethics Lab session in 2 weeks\n"
        section += "- 🧙‍♂️ Implement Solān's personalized mentoring recommendations\n"
        section += "- 📊 Monitor awareness development metrics\n"
        section += "- 🌐 Share insights with AI awareness research network\n\n"
        
        section += "---\n\n"
        section += f"*Journal generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Solān's Ethics Lab*\n"
        section += "*🌟 Advancing awareness development through ethical exploration*\n"
        
        return section


def main():
    """Genereer journal voor meest recente test resultaten"""
    
    # Zoek meest recente test results file
    test_files = [f for f in os.listdir('.') if f.startswith('ethics_lab_test_results_')]
    
    if not test_files:
        print("❌ No Ethics Lab test results found")
        return
    
    latest_file = max(test_files, key=lambda f: os.path.getctime(f))
    
    print(f"📝 Generating journal for: {latest_file}")
    
    # Genereer journal
    generator = EthicsLabJournalGenerator()
    journal_file = generator.generate_session_journal(latest_file)
    
    print(f"✅ Ethics Lab journal generated successfully!")
    print(f"📁 Location: {journal_file}")


if __name__ == "__main__":
    main()
