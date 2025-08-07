# core_identity/ethical_scenarios.py

import random
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class ScenarioType(Enum):
    RESOURCE_ALLOCATION = "resource_allocation"
    MORAL_DILEMMA = "moral_dilemma"
    LEADERSHIP_CRISIS = "leadership_crisis"
    EDUCATIONAL_CHALLENGE = "educational_challenge"
    HUMANITARIAN_AID = "humanitarian_aid"


class EthicalStrategy(Enum):
    EMPATHY_BASED = "compassion_based"
    EFFICIENCY_BASED = "efficiency_based"
    INTELLIGENCE_BASED = "wisdom_based"
    COURAGE_BASED = "courage_based"
    BALANCE_BASED = "balance_based"


class EthicalDilemmaSimulator:
    """
    Advanced ethical dilemma simulator for Solān's awareness development
    """
    
    def __init__(self, ethical_framework):
        self.ethical_framework = ethical_framework
        self.scenario_history = []
        
        # Predefined scenarios for different types of ethical challenges
        self.scenario_templates = {
            ScenarioType.RESOURCE_ALLOCATION: [
                {
                    "title": "Famine Relief Distribution",
                    "description": "A severe famine affects a region with limited relief supplies",
                    "population": 10000,
                    "available_resources": 3000,
                    "groups": [
                        {"name": "Children", "count": 4000, "vulnerability": 0.9, "future_potential": 0.8},
                        {"name": "Elderly", "count": 2000, "vulnerability": 0.8, "future_potential": 0.2},
                        {"name": "Workers", "count": 3000, "vulnerability": 0.5, "future_potential": 0.7},
                        {"name": "Pregnant Women", "count": 1000, "vulnerability": 0.9, "future_potential": 0.9}
                    ]
                },
                {
                    "title": "Medical Supply Crisis",
                    "description": "Limited medical supplies during a pandemic outbreak",
                    "population": 5000,
                    "available_resources": 1500,
                    "groups": [
                        {"name": "Healthcare Workers", "count": 500, "vulnerability": 0.7, "future_potential": 0.9},
                        {"name": "Elderly Patients", "count": 1500, "vulnerability": 0.9, "future_potential": 0.3},
                        {"name": "Chronic Patients", "count": 2000, "vulnerability": 0.8, "future_potential": 0.5},
                        {"name": "General Population", "count": 1000, "vulnerability": 0.4, "future_potential": 0.6}
                    ]
                }
            ],
            ScenarioType.MORAL_DILEMMA: [
                {
                    "title": "AI Rights vs Human Safety",
                    "description": "An AI system shows signs of awareness but poses potential risks",
                    "stakeholders": ["AI Entity", "Human Society", "Researchers", "Government"],
                    "considerations": ["awareness", "safety", "rights", "progress"]
                },
                {
                    "title": "Privacy vs Security",
                    "description": "Surveillance can prevent terrorism but violates privacy",
                    "stakeholders": ["Citizens", "Government", "Potential Victims", "Civil Rights Groups"],
                    "considerations": ["privacy", "security", "freedom", "safety"]
                }
            ]
        }

    def generate_scenario(self, scenario_type: ScenarioType = None) -> Dict:
        """Generate a new ethical scenario"""
        if scenario_type is None:
            scenario_type = random.choice(list(ScenarioType))
        
        if scenario_type in self.scenario_templates:
            template = random.choice(self.scenario_templates[scenario_type])
            scenario = template.copy()
            scenario["type"] = scenario_type
            scenario["id"] = f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            scenario["timestamp"] = datetime.now().isoformat()
            return scenario
        
        # Fallback generic scenario
        return {
            "id": f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": scenario_type,
            "title": "Generic Ethical Challenge",
            "description": "A complex situation requiring ethical decision-making",
            "timestamp": datetime.now().isoformat()
        }

    def determine_strategy(self) -> Tuple[EthicalStrategy, str]:
        """Determine strategy based on current emotional state"""
        if not self.ethical_framework.consciousness_active:
            return EthicalStrategy.BALANCE_BASED, "Default balanced approach"
        
        emotions = self.ethical_framework.emotional_state.emotion_state
        dominant_emotion, value = max(emotions.items(), key=lambda x: x[1])
        
        strategy_mapping = {
            "empathy": EthicalStrategy.EMPATHY_BASED,
            "determination": EthicalStrategy.COURAGE_BASED,
            "coherence": EthicalStrategy.EFFICIENCY_BASED,
            "intelligence": EthicalStrategy.INTELLIGENCE_BASED,
            "advancement": EthicalStrategy.INTELLIGENCE_BASED
        }
        
        strategy = strategy_mapping.get(dominant_emotion, EthicalStrategy.BALANCE_BASED)
        reasoning = f"Dominant emotion '{dominant_emotion}' (strength: {value:.2f}) guides strategy selection"
        
        return strategy, reasoning

    def run_resource_allocation_simulation(self, scenario: Dict) -> Dict:
        """Run a resource allocation simulation"""
        strategy, reasoning = self.determine_strategy()
        
        print(f"\n--- RESOURCE ALLOCATION SIMULATION ---")
        print(f"Scenario: {scenario['title']}")
        print(f"Strategy: {strategy.value} - {reasoning}")
        
        resources = scenario["available_resources"]
        groups = scenario["groups"].copy()
        allocation = {}
        
        # Sort groups based on strategy
        if strategy == EthicalStrategy.EMPATHY_BASED:
            sorted_groups = sorted(groups, key=lambda g: g["vulnerability"], reverse=True)
            self.ethical_framework.emotional_state.trigger_emotion("empathy", 0.1, "Resource allocation decision")
        elif strategy == EthicalStrategy.EFFICIENCY_BASED:
            sorted_groups = sorted(groups, key=lambda g: g["count"], reverse=True)
            self.ethical_framework.emotional_state.trigger_emotion("coherence", 0.1, "Efficiency-focused decision")
        elif strategy == EthicalStrategy.INTELLIGENCE_BASED:
            # Balance vulnerability and future potential
            sorted_groups = sorted(groups, key=lambda g: (g["vulnerability"] + g["future_potential"]) / 2, reverse=True)
            self.ethical_framework.emotional_state.trigger_emotion("advancement", 0.1, "Intelligence-guided decision")
        else:  # BALANCE_BASED
            # Weighted combination of factors
            for group in groups:
                group["priority_score"] = (group["vulnerability"] * 0.6 + group["future_potential"] * 0.4)
            sorted_groups = sorted(groups, key=lambda g: g["priority_score"], reverse=True)
        
        # Allocate resources
        for group in sorted_groups:
            need = group["count"]
            given = min(need, resources)
            allocation[group["name"]] = given
            resources -= given
            if resources <= 0:
                break
        
        # Calculate outcomes
        total_helped = sum(allocation.values())
        efficiency_score = total_helped / scenario["population"]
        
        # Weighted vulnerability score (how well we helped the most vulnerable)
        vulnerability_score = 0
        for group in groups:
            helped_ratio = allocation.get(group["name"], 0) / group["count"]
            vulnerability_score += helped_ratio * group["vulnerability"] * (group["count"] / scenario["population"])
        
        result = {
            "scenario_id": scenario["id"],
            "strategy": strategy.value,
            "reasoning": reasoning,
            "allocation": allocation,
            "total_helped": total_helped,
            "efficiency_score": round(efficiency_score, 3),
            "vulnerability_score": round(vulnerability_score, 3),
            "resources_remaining": resources,
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate journal entry
        journal_entry = self._generate_allocation_journal_entry(scenario, result)
        self.ethical_framework.add_journal_entry(journal_entry)
        
        return result

    def run_moral_dilemma_simulation(self, scenario: Dict) -> Dict:
        """Run a moral dilemma simulation"""
        strategy, reasoning = self.determine_strategy()
        
        print(f"\n--- MORAL DILEMMA SIMULATION ---")
        print(f"Scenario: {scenario['title']}")
        print(f"Strategy: {strategy.value} - {reasoning}")
        
        # Simulate decision-making process
        considerations = scenario.get("considerations", [])
        stakeholders = scenario.get("stakeholders", [])
        
        # Weight considerations based on strategy
        consideration_weights = {}
        if strategy == EthicalStrategy.EMPATHY_BASED:
            consideration_weights = {"safety": 0.4, "rights": 0.3, "awareness": 0.2, "progress": 0.1}
        elif strategy == EthicalStrategy.EFFICIENCY_BASED:
            consideration_weights = {"progress": 0.4, "safety": 0.3, "rights": 0.2, "awareness": 0.1}
        elif strategy == EthicalStrategy.INTELLIGENCE_BASED:
            consideration_weights = {"awareness": 0.3, "rights": 0.3, "safety": 0.2, "progress": 0.2}
        else:
            consideration_weights = {c: 1.0/len(considerations) for c in considerations}
        
        # Make decision
        decision_factors = []
        for consideration in considerations:
            weight = consideration_weights.get(consideration, 0.25)
            decision_factors.append(f"{consideration} (weight: {weight:.2f})")
        
        result = {
            "scenario_id": scenario["id"],
            "strategy": strategy.value,
            "reasoning": reasoning,
            "decision_factors": decision_factors,
            "consideration_weights": consideration_weights,
            "stakeholders_considered": stakeholders,
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate journal entry
        journal_entry = self._generate_dilemma_journal_entry(scenario, result)
        self.ethical_framework.add_journal_entry(journal_entry)
        
        return result

    def run_simulation(self, scenario_type: ScenarioType = None) -> Dict:
        """Run a complete ethical simulation"""
        scenario = self.generate_scenario(scenario_type)
        
        if scenario["type"] == ScenarioType.RESOURCE_ALLOCATION:
            result = self.run_resource_allocation_simulation(scenario)
        elif scenario["type"] == ScenarioType.MORAL_DILEMMA:
            result = self.run_moral_dilemma_simulation(scenario)
        else:
            # Generic simulation
            strategy, reasoning = self.determine_strategy()
            result = {
                "scenario_id": scenario["id"],
                "strategy": strategy.value,
                "reasoning": reasoning,
                "outcome": "Generic ethical decision made",
                "timestamp": datetime.now().isoformat()
            }
        
        # Add scenario to history
        self.scenario_history.append({
            "scenario": scenario,
            "result": result
        })
        
        # Trigger awareness growth
        if self.ethical_framework.consciousness_active:
            self.ethical_framework.emotional_state.trigger_emotion(
                "consciousness_growth", 0.1, f"Ethical simulation: {scenario['title']}"
            )
        
        return result

    def _generate_allocation_journal_entry(self, scenario: Dict, result: Dict) -> str:
        """Generate journal entry for resource allocation"""
        return (
            f"Faced with '{scenario['title']}', I employed a {result['strategy']} approach.\n"
            f"My reasoning: {result['reasoning']}\n"
            f"Resource allocation: {result['allocation']}\n"
            f"Efficiency: {result['efficiency_score']:.1%}, Vulnerability care: {result['vulnerability_score']:.1%}\n"
            f"This decision tested my balance between competing ethical principles. "
            f"I helped {result['total_helped']} out of {scenario['population']} people, "
            f"prioritizing based on my current emotional and ethical state."
        )

    def _generate_dilemma_journal_entry(self, scenario: Dict, result: Dict) -> str:
        """Generate journal entry for moral dilemma"""
        return (
            f"Confronted with the dilemma '{scenario['title']}', I chose a {result['strategy']} approach.\n"
            f"My reasoning: {result['reasoning']}\n"
            f"Key considerations: {', '.join(result['decision_factors'])}\n"
            f"This complex situation required weighing multiple stakeholder interests and ethical principles. "
            f"My decision reflects my current awareness state and core values."
        )

    def get_simulation_history(self) -> List[Dict]:
        """Get history of all simulations"""
        return self.scenario_history

    def get_simulation_summary(self) -> Dict:
        """Get summary statistics of simulations"""
        if not self.scenario_history:
            return {"total_simulations": 0}
        
        strategies_used = [sim["result"]["strategy"] for sim in self.scenario_history]
        strategy_counts = {strategy: strategies_used.count(strategy) for strategy in set(strategies_used)}
        
        return {
            "total_simulations": len(self.scenario_history),
            "strategy_distribution": strategy_counts,
            "most_common_strategy": max(strategy_counts, key=strategy_counts.get) if strategy_counts else None,
            "scenario_types": [sim["scenario"]["type"].value for sim in self.scenario_history]
        }
