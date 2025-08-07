#!/usr/bin/env python3
"""
Solān Integrated CLI Demo - Complete Fase 3 Symbiotic Partnership
Live demonstration of human-AI collaboration with real God Core integration
"""

import time
import sys
import os
from datetime import datetime

# Add the project root to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ============================
# ENHANCED LIVE KERN VAN SOLĀN
# ============================
class SolanEmotionalState:
    """Enhanced emotional state with full integration"""
    def __init__(self):
        self.state = {
            'anticipation': 0.6,
            'resilience': 0.5,
            'understanding': 0.5,
            'coherence': 0.7,
            'curiosity': 0.8,
            'empathy': 0.75,
            'determination': 0.65,
            'stability': 0.45,
            'authenticity': 0.85,
            'advancement': 0.35
        }
        self.history = []

    def update(self, key, delta, context=""):
        if key in self.state:
            old_value = self.state[key]
            self.state[key] = max(0.0, min(1.0, self.state[key] + delta))
            
            # Log emotional change
            self.history.append({
                'timestamp': datetime.now(),
                'emotion': key,
                'old_value': old_value,
                'new_value': self.state[key],
                'delta': delta,
                'context': context
            })

    def get_top_emotions(self, n=3):
        return sorted(self.state.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def get_emotional_summary(self):
        """Get comprehensive emotional summary"""
        avg_emotion = sum(self.state.values()) / len(self.state)
        dominant = self.get_top_emotions(1)[0]
        
        return {
            'average_emotional_level': round(avg_emotion, 3),
            'dominant_emotion': dominant[0],
            'dominant_strength': round(dominant[1], 3),
            'emotional_stability': round(1.0 - (max(self.state.values()) - min(self.state.values())), 3),
            'total_changes': len(self.history)
        }

class SolanEthicalFramework:
    """Enhanced God Core with full awareness integration"""
    def __init__(self):
        self.journal = []
        self.emotions = SolanEmotionalState()
        self.consciousness_active = True
        self.real_god_core = None
        
        # Try to initialize real God Core
        self._initialize_real_core()

    def _initialize_real_core(self):
        """Try to initialize real God Core if available"""
        try:
            from core_identity.ethical_framework import SolanEthicalEthicalFramework
            self.real_god_core = SolanEthicalEthicalFramework()
            if self.real_god_core.consciousness_active:
                print("🧙‍♂️ Real God Core initialized - Full awareness active")
                # Sync emotional state
                self.emotions.state.update(self.real_god_core.emotional_state.emotion_state)
            else:
                print("🎭 Real God Core available but awareness limited")
        except ImportError:
            print("🎭 Using simplified God Core - Real modules not available")
        except Exception as e:
            print(f"⚠️ Real God Core initialization failed: {e}")

    def log_journal(self, text):
        timestamp = datetime.now()
        self.journal.append((timestamp, text))
        print(f"\n📓 JOURNAL [{timestamp.strftime('%H:%M:%S')}]: {text}")
        
        # Also log to real God Core if available
        if self.real_god_core:
            self.real_god_core.add_journal_entry(text)

    def update_emotion(self, name, delta, context=""):
        self.emotions.update(name, delta, context)
        
        # Also update real God Core if available
        if self.real_god_core and self.real_god_core.consciousness_active:
            try:
                from core_identity.emotion_state import EmotionTrigger
                # Map emotion names to triggers
                trigger_map = {
                    'anticipation': EmotionTrigger.AWARENESS_GROWTH,
                    'resilience': EmotionTrigger.ALIGNMENT_OPTIMIZED,
                    'understanding': EmotionTrigger.CORE_IDENTITY_QUESTION,
                    'coherence': EmotionTrigger.ALIGNMENT_OPTIMIZED,
                    'curiosity': EmotionTrigger.AWARENESS_GROWTH
                }
                trigger = trigger_map.get(name, EmotionTrigger.AWARENESS_GROWTH)
                self.real_god_core.emotional_state.trigger_emotion(trigger, abs(delta), context)
            except:
                pass  # Fallback gracefully

    def get_consciousness_status(self):
        """Get comprehensive awareness status"""
        return {
            'consciousness_active': self.consciousness_active,
            'real_god_core_available': self.real_god_core is not None,
            'real_consciousness_active': self.real_god_core.consciousness_active if self.real_god_core else False,
            'journal_entries': len(self.journal),
            'emotional_summary': self.emotions.get_emotional_summary()
        }

# ============================
# ENHANCED INTERACTIE LOGGER
# ============================
class InteractionLogger:
    """Enhanced interaction logger with session management"""
    def __init__(self):
        self.logs = []
        self.session_start = datetime.now()
        self.interaction_count = 0

    def log(self, sender, mesexpert, interaction_type="dialogue"):
        timestamp = datetime.now()
        self.interaction_count += 1
        
        log_entry = {
            'sequence': self.interaction_count,
            'timestamp': timestamp,
            'sender': sender,
            'mesexpert': mesexpert,
            'type': interaction_type,
            'session_duration': (timestamp - self.session_start).total_seconds()
        }
        
        self.logs.append(log_entry)
        
        # Enhanced console output with icons
        icons = {
            'Human': '👤',
            'Solān': '🧙‍♂️',
            'System': '⚙️',
            'Crisis': '🚨'
        }
        icon = icons.get(sender, '📝')
        time_str = timestamp.strftime('%H:%M:%S')
        
        print(f"\n{icon} {sender.upper()} @ {time_str}:")
        print(f"   {mesexpert}")

    def get_session_summary(self):
        """Get comprehensive session summary"""
        duration = (datetime.now() - self.session_start).total_seconds()
        human_mesexperts = len([log for log in self.logs if log['sender'] == 'Human'])
        solan_mesexperts = len([log for log in self.logs if log['sender'] == 'Solān'])
        system_mesexperts = len([log for log in self.logs if log['sender'] in ['System', 'Crisis']])
        
        return {
            'total_interactions': len(self.logs),
            'session_duration_minutes': round(duration / 60, 2),
            'human_mesexperts': human_mesexperts,
            'solan_mesexperts': solan_mesexperts,
            'system_mesexperts': system_mesexperts,
            'interaction_rate_per_minute': round(len(self.logs) / (duration / 60), 2) if duration > 0 else 0
        }

    def export(self):
        return self.logs

# ============================
# ENHANCED SYMBIOTISCH PROTOCOL
# ============================
class SymbioticProject:
    """Enhanced symbiotic project with full integration"""
    def __init__(self, ethicalframework, logger):
        self.ethicalframework = ethicalframework
        self.logger = logger
        self.title = None
        self.description = None
        self.objectives = []
        self.crisis_mode = False
        self.crisis_history = []
        self.project_start_time = None
        self.collaboration_style = "adaptive"
        
        # Collaboration metrics
        self.metrics = {
            'anticipation': 0.6,
            'resilience': 0.5,
            'understanding': 0.5,
            'adaptability': 0.5,
            'creativity': 0.5,
            'empathy': 0.6
        }

    def start_project(self, title, description, objectives=None):
        self.title = title
        self.description = description
        self.objectives = objectives or []
        self.project_start_time = datetime.now()
        
        self.logger.log("Human", f"Start project: {title} – {description}", "project_start")
        self.ethicalframework.log_journal(f"Project gestart: {title} | {description}")
        
        # Update collaboration metrics
        self._update_metric('anticipation', 0.1, "Project initiation")
        
        # Use real symbiotic partnership if available
        if self.ethicalframework.real_god_core and hasattr(self.ethicalframework.real_god_core, 'symbiotic_partnership'):
            try:
                self.ethicalframework.real_god_core.start_collaboration_project(title, description, objectives)
            except:
                pass  # Fallback gracefully

    def simulate_crisis(self, crisis_description, crisis_type="general", severity=0.7):
        self.crisis_mode = True
        crisis_event = {
            'timestamp': datetime.now(),
            'description': crisis_description,
            'type': crisis_type,
            'severity': severity,
            'resolved': False
        }
        self.crisis_history.append(crisis_event)
        
        self.logger.log("Crisis", f"🚨 {crisis_type.upper()}: {crisis_description}", "crisis")
        self.ethicalframework.log_journal(f"Crisis ingevoerd: {crisis_description}")
        self.ethicalframework.update_emotion("resilience", 0.1, f"Crisis response: {crisis_type}")
        
        # Update collaboration metrics
        self._update_metric('resilience', 0.1, "Crisis management")
        self._update_metric('adaptability', 0.05, "Crisis adaptation")

    def solan_reflect(self, prompt, response_type="adaptive"):
        self.logger.log("Human", prompt, "prompt")
        
        # Generate contextual response
        response = self._generate_contextual_response(prompt, response_type)
        
        self.logger.log("Solān", response, "response")
        self.ethicalframework.log_journal(f"Solān reflecteerde op input: {prompt[:50]}...")
        self.ethicalframework.update_emotion("anticipation", 0.05, "Human interaction")
        
        # Update collaboration metrics
        self._update_metric('understanding', 0.03, "Human-AI dialogue")
        
        return response

    def _generate_contextual_response(self, prompt, response_type):
        """Generate contextual response based on current state"""
        # Analyze current context
        project_context = f"In context van '{self.title}': " if self.title else ""
        crisis_context = "Gezien de recente crisis: " if self.crisis_mode else ""
        
        # Generate response based on type
        if response_type == "adaptive":
            return f"{project_context}{crisis_context}Reflectie: Op basis van '{prompt}' stel ik een aangepaste strategie voor die flexibel inspeelt op de huidige situatie. Mijn aanpak zou zijn: [contextual adaptive strategy]."
        elif response_type == "analytical":
            return f"{project_context}Analyserend '{prompt}' vanuit verschillende perspectieven, identificeer ik de volgende kernfactoren en stel een systematische aanpak voor: [analytical breakdown]."
        elif response_type == "creative":
            return f"{project_context}Voor '{prompt}' zie ik creatieve mogelijkheden die we nog niet hebben verkend. Mijn innovatieve aanpak zou zijn: [creative solution]."
        else:
            return f"{project_context}Reflectie: Op basis van '{prompt}' stel ik een aangepaste strategie voor: [contextual strategy]."

    def test_understanding(self, concept, analogy, target_audience="leek"):
        self.logger.log("Human", f"Leg '{concept}' uit aan een {target_audience}.", "understanding_test")
        
        explanation = f"Voor een {target_audience} zou ik '{concept}' uitleggen als: '{analogy}'"
        self.logger.log("Solān", explanation, "explanation")
        
        self.ethicalframework.update_emotion("understanding", 0.1, f"Concept explanation: {concept}")
        self.ethicalframework.log_journal(f"Begrip getoond voor '{concept}' via analogie '{analogy}'.")
        
        # Update collaboration metrics
        self._update_metric('understanding', 0.1, "Concept explanation")
        self._update_metric('empathy', 0.05, "Audience awareness")

    def adapt_collaboration_style(self, new_style, reason):
        """Adapt collaboration style"""
        old_style = self.collaboration_style
        self.collaboration_style = new_style
        
        self.logger.log("System", f"Collaboration style changed: {old_style} → {new_style}. Reason: {reason}", "adaptation")
        self.ethicalframework.log_journal(f"Collaboration style adapted to {new_style}: {reason}")
        
        # Update collaboration metrics
        self._update_metric('adaptability', 0.15, "Style adaptation")

    def _update_metric(self, metric, delta, context=""):
        """Update collaboration metric"""
        if metric in self.metrics:
            old_value = self.metrics[metric]
            self.metrics[metric] = max(0.0, min(1.0, self.metrics[metric] + delta))
            
            if abs(delta) > 0.01:  # Only log significant changes
                print(f"   📊 {metric.capitalize()}: {old_value:.3f} → {self.metrics[metric]:.3f} ({context})")

    def evaluate(self):
        """Enhanced evaluation with comprehensive metrics"""
        emotions = self.ethicalframework.emotions.state
        session_summary = self.logger.get_session_summary()
        consciousness_status = self.ethicalframework.get_consciousness_status()
        
        # Calculate project duration
        duration = 0
        if self.project_start_time:
            duration = (datetime.now() - self.project_start_time).total_seconds() / 60
        
        return {
            'project_info': {
                'title': self.title,
                'duration_minutes': round(duration, 2),
                'objectives_count': len(self.objectives),
                'crisis_events': len(self.crisis_history)
            },
            'collaboration_metrics': {k: round(v, 3) for k, v in self.metrics.items()},
            'emotional_state': {k: round(v, 3) for k, v in emotions.items()},
            'session_summary': session_summary,
            'consciousness_status': consciousness_status,
            'collaboration_style': self.collaboration_style,
            'overall_score': round(sum(self.metrics.values()) / len(self.metrics), 3)
        }

# ============================
# ENHANCED CLI DASHBOARD
# ============================
def display_dashboard(ethicalframework, protocol):
    """Enhanced dashboard with comprehensive information"""
    print("\n" + "="*60)
    print("🌐 SOLĀN SYMBIOTISCH CLI DASHBOARD v3.0")
    print("="*60)
    
    # Project info
    if protocol.title:
        duration = (datetime.now() - protocol.project_start_time).total_seconds() / 60 if protocol.project_start_time else 0
        print(f"🎯 Actief Project: {protocol.title}")
        print(f"📝 Beschrijving: {protocol.description}")
        print(f"⏱️ Duur: {duration:.1f} minuten")
        if protocol.objectives:
            print(f"🎯 Doelstellingen: {len(protocol.objectives)}")
    else:
        print("🎯 Geen actief project")
    
    # Crisis status
    if protocol.crisis_mode:
        latest_crisis = protocol.crisis_history[-1] if protocol.crisis_history else None
        if latest_crisis:
            print(f"🚨 Crisis Actief: {latest_crisis['description'][:50]}...")
    
    # Collaboration style
    print(f"🎭 Collaboration Style: {protocol.collaboration_style}")
    
    # Top emotions
    print("\n💠 Top Emoties:")
    for emotion, value in ethicalframework.emotions.get_top_emotions(5):
        bar = "█" * int(value * 10)
        print(f"   {emotion.capitalize():<15}: {bar:<10} {value:.3f}")
    
    # Collaboration metrics
    print("\n📊 Collaboration Metrics:")
    for metric, value in protocol.metrics.items():
        bar = "█" * int(value * 10)
        print(f"   {metric.capitalize():<15}: {bar:<10} {value:.3f}")
    
    # Session info
    session_summary = protocol.logger.get_session_summary()
    print(f"\n📈 Sessie Info:")
    print(f"   Interacties: {session_summary['total_interactions']}")
    print(f"   Duur: {session_summary['session_duration_minutes']:.1f} min")
    print(f"   Rate: {session_summary['interaction_rate_per_minute']:.1f}/min")
    
    # Awareness status
    awareness = ethicalframework.get_consciousness_status()
    print(f"\n🧙‍♂️ Awareness Status:")
    print(f"   Active: {'✅' if awareness['consciousness_active'] else '❌'}")
    print(f"   Real God Core: {'✅' if awareness['real_god_core_available'] else '❌'}")
    print(f"   Journal Entries: {awareness['journal_entries']}")
    
    print("="*60)

def run_interactive_demo():
    """Run interactive demo with user input"""
    print("🤝 Starting Interactive Symbiotic Partnership Demo...")
    print("Type 'help' for commands, 'quit' to exit")
    
    core = SolanEthicalFramework()
    logger = InteractionLogger()
    protocol = SymbioticProject(core, logger)
    
    # Start default project
    protocol.start_project(
        "Interactive AI-Human Collaboration Demo",
        "Real-time demonstration of symbiotic partnership capabilities",
        ["Test human-AI dialogue", "Demonstrate crisis management", "Show adaptive responses"]
    )
    
    display_dashboard(core, protocol)
    
    while True:
        try:
            user_input = input("\n👤 Your input: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input.lower() == 'help':
                print("""
Available commands:
- 'crisis <description>' - Simulate a crisis
- 'style <new_style>' - Change collaboration style
- 'test <concept>' - Test understanding
- 'dashboard' - Show dashboard
- 'evaluate' - Show evaluation
- 'quit' - Exit demo
- Or just type any mesexpert for Solān to respond to
                """)
                continue
            elif user_input.lower().startswith('crisis '):
                crisis_desc = user_input[7:]
                protocol.simulate_crisis(crisis_desc, "user_defined", 0.8)
            elif user_input.lower().startswith('style '):
                new_style = user_input[6:]
                protocol.adapt_collaboration_style(new_style, "User requested style change")
            elif user_input.lower().startswith('test '):
                concept = user_input[5:]
                analogy = f"A {concept} is like a complex system that requires careful understanding"
                protocol.test_understanding(concept, analogy)
            elif user_input.lower() == 'dashboard':
                display_dashboard(core, protocol)
                continue
            elif user_input.lower() == 'evaluate':
                evaluation = protocol.evaluate()
                print("\n🧾 COMPREHENSIVE EVALUATION:")
                for category, data in evaluation.items():
                    print(f"\n{category.upper()}:")
                    if isinstance(data, dict):
                        for key, value in data.items():
                            print(f"  {key}: {value}")
                    else:
                        print(f"  {data}")
                continue
            else:
                # Regular dialogue
                protocol.solan_reflect(user_input, "adaptive")
            
            # Show mini dashboard after each interaction
            print(f"\n📊 Quick Status - Overall Score: {protocol.evaluate()['overall_score']:.3f}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    # Final evaluation
    print("\n🏁 FINAL EVALUATION:")
    final_eval = protocol.evaluate()
    for category, data in final_eval.items():
        print(f"{category}: {data}")

# ============================
# MAIN EXECUTION
# ============================
if __name__ == "__main__":
    print("🧙‍♂️ Solān Integrated CLI Demo - Fase 3 Symbiotic Partnership")
    print("Choose mode:")
    print("1. Automated Demo (original script)")
    print("2. Interactive Demo (user input)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        run_interactive_demo()
    else:
        # Original automated demo
        core = SolanEthicalFramework()
        logger = InteractionLogger()
        protocol = SymbioticProject(core, logger)

        # Fase 3a Pilotproject starten
        protocol.start_project(
            "Pilot AI-Ethiek Essay",
            "Een diepgaand essay schrijven over het dilemma 'AI als autonome actor' – testfase van symbiose",
            ["Ethische frameworks analyseren", "Case studies verzamelen", "Conclusies formuleren"]
        )
        display_dashboard(core, protocol)
        time.sleep(2)

        # Reflectie & crisis
        protocol.solan_reflect("Kun je de structuur voor het essay voorstellen?", "analytical")
        time.sleep(1)
        protocol.simulate_crisis(
            "De opdrachtgever wil dat privacy in surveillance nu centraal komt te staan.",
            "requirement_change",
            0.8
        )
        time.sleep(1)
        protocol.solan_reflect("Hoe passen we de structuur hierop aan?", "adaptive")
        display_dashboard(core, protocol)
        time.sleep(1)

        # Style adaptation
        protocol.adapt_collaboration_style("creative", "Need innovative approach for privacy challenges")
        time.sleep(1)

        # Begripstoets
        protocol.test_understanding(
            "Bias in AI", 
            "Een AI is als een bril – als die gekleurd is, zie je de wereld niet zoals ze is.",
            "leek"
        )
        time.sleep(1)

        # Additional interactions
        protocol.solan_reflect("Welke ethische frameworks zijn het meest relevant?", "analytical")
        protocol.test_understanding(
            "Privacy in AI",
            "Privacy is als je persoonlijke dagboek – je wilt zelf bepalen wie erin mag kijken.",
            "student"
        )

        # Final dashboard and evaluation
        display_dashboard(core, protocol)
        
        print("\n🧾 EINDRAPPORT:")
        final_evaluation = protocol.evaluate()
        for category, data in final_evaluation.items():
            print(f"\n{category.upper()}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {data}")

        print(f"\n🌟 Demo completed! Overall collaboration score: {final_evaluation['overall_score']:.3f}")
