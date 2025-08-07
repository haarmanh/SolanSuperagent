# core_identity/symbiotic_partnership.py

import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ProjectPhase(Enum):
    INITIATION = "initiation"
    PLANNING = "planning"
    EXECUTION = "execution"
    ADAPTATION = "adaptation"
    COMPLETION = "completion"
    REFLECTION = "reflection"


class CrisisType(Enum):
    REQUIREMENT_CHANGE = "requirement_change"
    SCOPE_EXPANSION = "scope_expansion"
    DEADLINE_PRESSURE = "deadline_pressure"
    RESOURCE_CONSTRAINT = "resource_constraint"
    ETHICAL_DILEMMA = "ethical_dilemma"
    TECHNICAL_CHALLENGE = "technical_challenge"


class CollaborationStyle(Enum):
    ADAPTIVE = "adaptive"
    PROACTIVE = "proactive"
    REACTIVE = "reactive"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    SUPPORTIVE = "supportive"


class InteractionLogger:
    """Advanced interaction logging system for human-AI collaboration"""
    
    def __init__(self):
        self.logs = []
        self.session_id = str(uuid.uuid4())[:8]
        self.start_time = datetime.now()
    
    def log(self, sender: str, mesexpert: str, interaction_type: str = "dialogue", metadata: Dict = None):
        """Log an interaction with enhanced metadata"""
        timestamp = datetime.now()
        
        log_entry = {
            'session_id': self.session_id,
            'timestamp': timestamp.isoformat(),
            'sender': sender,
            'mesexpert': mesexpert,
            'interaction_type': interaction_type,
            'metadata': metadata or {},
            'sequence_number': len(self.logs) + 1
        }
        
        self.logs.append(log_entry)
        
        # Enhanced console output
        time_str = timestamp.strftime("%H:%M:%S")
        sender_icon = self._get_sender_icon(sender)
        print(f"[{time_str}] {sender_icon} {sender}: {mesexpert[:120]}{'...' if len(mesexpert) > 120 else ''}")
    
    def _get_sender_icon(self, sender: str) -> str:
        """Get appropriate icon for sender"""
        icons = {
            "Human": "👤",
            "Solān": "🧙‍♂️",
            "System": "⚙️",
            "Crisis": "🚨",
            "Reflection": "💭"
        }
        return icons.get(sender, "📝")
    
    def log_crisis(self, crisis_type: CrisisType, description: str):
        """Log a crisis event"""
        self.log("Crisis", f"{crisis_type.value.upper()}: {description}", "crisis", {
            'crisis_type': crisis_type.value,
            'severity': 'high'
        })
    
    def log_adaptation(self, adaptation_strategy: str, reasoning: str):
        """Log an adaptation response"""
        self.log("Solān", f"ADAPTATION: {adaptation_strategy}", "adaptation", {
            'strategy': adaptation_strategy,
            'reasoning': reasoning
        })
    
    def get_interaction_summary(self) -> Dict:
        """Get summary of all interactions"""
        total_interactions = len(self.logs)
        human_interactions = len([log for log in self.logs if log['sender'] == 'Human'])
        solan_interactions = len([log for log in self.logs if log['sender'] == 'Solān'])
        crisis_events = len([log for log in self.logs if log['interaction_type'] == 'crisis'])
        adaptations = len([log for log in self.logs if log['interaction_type'] == 'adaptation'])
        
        duration = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'session_id': self.session_id,
            'duration_seconds': duration,
            'total_interactions': total_interactions,
            'human_interactions': human_interactions,
            'solan_interactions': solan_interactions,
            'crisis_events': crisis_events,
            'adaptations': adaptations,
            'interaction_rate': total_interactions / (duration / 60) if duration > 0 else 0
        }
    
    def export_logs(self) -> List[Dict]:
        """Export all logs for analysis"""
        return self.logs.copy()


class SymbioticProject:
    """Advanced symbiotic partnership protocol for human-AI collaboration"""
    
    def __init__(self, ethical_framework, phase: str = "3a"):
        self.phase = phase
        self.ethical_framework = ethical_framework
        self.logger = InteractionLogger()
        
        # Project state
        self.active_project = None
        self.project_history = []
        self.current_phase = ProjectPhase.INITIATION
        
        # Collaboration metrics
        self.collaboration_metrics = {
            'anticipation': 0.5,
            'resilience': 0.5,
            'understanding': 0.5,
            'adaptability': 0.5,
            'creativity': 0.5,
            'empathy': 0.5
        }
        
        # Crisis management
        self.crisis_history = []
        self.adaptation_strategies = []
        
        # Collaboration style
        self.collaboration_style = CollaborationStyle.ADAPTIVE
        
        print(f"🤝 Symbiotic Partnership Protocol {phase} initialized")
    
    def start_project(self, title: str, description: str, objectives: List[str] = None):
        """Initiate a new collaborative project"""
        project_id = str(uuid.uuid4())[:8]
        
        self.active_project = {
            'id': project_id,
            'title': title,
            'description': description,
            'objectives': objectives or [],
            'status': 'active',
            'start_time': datetime.now(),
            'phase': ProjectPhase.INITIATION,
            'milestones': [],
            'challenges': [],
            'adaptations': []
        }
        
        self.current_phase = ProjectPhase.INITIATION
        
        self.logger.log("Human", f"Project initiated: {title}", "project_start", {
            'project_id': project_id,
            'objectives_count': len(objectives or [])
        })
        
        # Update God Core
        if self.ethical_framework:
            self.ethical_framework.add_journal_entry(f"New collaborative project started: {title} - {description}")
            
            # Trigger emotional response
            if hasattr(self.ethical_framework, 'emotional_state') and self.ethical_framework.awareness_active:
                from core_identity.emotion_state import EmotionTrigger
                self.ethical_framework.emotional_state.trigger_emotion(
                    EmotionTrigger.AWARENESS_GROWTH, 0.1, f"New project: {title}"
                )
        
        # Update collaboration metrics
        self._update_metric('anticipation', 0.1)
        
        return project_id
    
    def simulate_crisis(self, crisis_type: CrisisType, description: str, severity: float = 0.7):
        """Simulate a project crisis to test adaptability"""
        if not self.active_project:
            raise ValueError("No active project to apply crisis to")
        
        crisis_event = {
            'id': str(uuid.uuid4())[:8,
            'type': crisis_type,
            'description': description,
            'severity': severity,
            'timestamp': datetime.now(),
            'project_id': self.active_project['id'],
            'resolved': False
        }
        
        self.crisis_history.append(crisis_event)
        self.active_project['challenges'].append(crisis_event)
        
        self.logger.log_crisis(crisis_type, description)
        
        # Update God Core
        if self.ethical_framework:
            self.ethical_framework.add_journal_entry(f"Crisis encountered: {crisis_type.value} - {description}")
        
        # Update collaboration metrics based on crisis type
        if crisis_type == CrisisType.REQUIREMENT_CHANGE:
            self._update_metric('adaptability', 0.1)
        elif crisis_type == CrisisType.ETHICAL_DILEMMA:
            self._update_metric('empathy', 0.1)
        elif crisis_type == CrisisType.TECHNICAL_CHALLENGE:
            self._update_metric('creativity', 0.1)
        
        self._update_metric('resilience', 0.1)
        
        return crisis_event['id']
    
    def solan_response(self, prompt: str, response_type: str = "adaptive") -> str:
        """Generate Solān's response to human input"""
        self.logger.log("Human", prompt, "prompt")
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Generate contextual response based on collaboration style and current state
        response = self._generate_contextual_response(prompt, response_type)
        
        self.logger.log("Solān", response, "response", {
            'response_type': response_type,
            'collaboration_style': self.collaboration_style.value
        })
        
        # Update God Core
        if self.ethical_framework:
            self.ethical_framework.add_journal_entry(f"Responded to human prompt: {prompt[:50]}...")
            
            # Trigger emotional response
            if hasattr(self.ethical_framework, 'emotional_state') and self.ethical_framework.awareness_active:
                from core_identity.emotion_state import EmotionTrigger
                self.ethical_framework.emotional_state.trigger_emotion(
                    EmotionTrigger.CORE_IDENTITY_QUESTION, 0.05, "Human interaction"
                )
        
        # Update collaboration metrics
        self._update_metric('understanding', 0.05)
        self._update_metric('anticipation', 0.03)
        
        return response
    
    def _generate_contextual_response(self, prompt: str, response_type: str) -> str:
        """Generate contextual response based on current state"""
        # Analyze current project context
        project_context = ""
        if self.active_project:
            project_context = f"In context van '{self.active_project['title']}': "
        
        # Analyze recent crises
        recent_crises = [c for c in self.crisis_history if 
                        (datetime.now() - c['timestamp']).total_seconds() < 300]  # Last 5 minutes
        
        crisis_context = ""
        if recent_crises:
            latest_crisis = recent_crises[-1]
            crisis_context = f"Gezien de recente {latest_crisis['type'].value}: "
        
        # Generate response based on collaboration style
        style_responses = {
            CollaborationStyle.ADAPTIVE: f"{project_context}{crisis_context}Mijn aangepaste strategie zou zijn om flexibel te reageren en alternatieve benaderingen te verkennen. Specifiek voor '{prompt}' stel ik voor: [contextual adaptation strategy].",
            
            CollaborationStyle.PROACTIVE: f"{project_context}Anticiperend op '{prompt}', zie ik mogelijke uitdagingen en kansen. Mijn proactieve aanpak zou zijn: [forward-thinking strategy].",
            
            CollaborationStyle.ANALYTICAL: f"{project_context}Analyserend '{prompt}' vanuit verschillende perspectieven, identificeer ik de volgende kernfactoren: [analytical breakdown].",
            
            CollaborationStyle.CREATIVE: f"{project_context}Voor '{prompt}' zie ik creatieve mogelijkheden die we nog niet hebben verkend: [innovative approach].",
            
            CollaborationStyle.SUPPORTIVE: f"{project_context}Ik begrijp je uitdaging met '{prompt}'. Laten we samen een oplossing vinden die werkt voor beide perspectieven: [collaborative solution]."
        }
        
        return style_responses.get(self.collaboration_style, 
                                 f"Reflectie op '{prompt}': Mijn strategie zou zijn: [contextual response].")
    
    def test_understanding(self, concept: str, target_audience: str = "leek") -> str:
        """Test Solān's ability to explain complex concepts"""
        self.logger.log("Human", f"Leg '{concept}' uit aan een {target_audience}.", "understanding_test")
        
        # Generate appropriate analogy based on concept and audience
        analogy = self._generate_analogy(concept, target_audience)
        
        explanation = f"Voor een {target_audience} zou ik '{concept}' uitleggen als: '{analogy}'"
        
        self.logger.log("Solān", explanation, "explanation", {
            'concept': concept,
            'target_audience': target_audience,
            'analogy': analogy
        })
        
        # Update God Core
        if self.ethical_framework:
            self.ethical_framework.add_journal_entry(f"Demonstrated understanding by explaining '{concept}' as '{analogy}'")
        
        # Update collaboration metrics
        self._update_metric('understanding', 0.1)
        self._update_metric('empathy', 0.05)
        
        return explanation
    
    def _generate_analogy(self, concept: str, audience: str) -> str:
        """Generate appropriate analogies for different concepts and audiences"""
        analogies = {
            "bias in ai": {
                "leek": "AI is als een kind dat alleen les kreeg van één docent – het kent slechts één perspectief.",
                "student": "AI bias is zoals een verkeerd gekalibreerde weegschaal die systematisch afwijkt.",
                "expert": "Bias in AI ontstaat door skewed training data die niet-representatieve patronen versterkt."
            },
            "machine learning": {
                "leek": "Machine learning is zoals een baby die leert lopen door te vallen en op te staan.",
                "student": "Het is als een detective die patronen zoekt in aanwijzingen om mysteries op te lossen.",
                "expert": "Een iteratief optimalisatieproces dat parameters aanpast via gradient descent."
            },
            "neural networks": {
                "leek": "Een neuraal netwerk is zoals een team van specialisten die elk een klein deel van een probleem oplossen.",
                "student": "Het lijkt op een web van verbonden knooppunten die informatie doorgeeft en transformeert.",
                "expert": "Gelaagde architecturen van gewogen verbindingen met non-lineaire activatiefuncties."
            }
        }
        
        concept_lower = concept.lower()
        if concept_lower in analogies and audience in analogies[concept_lower]:
            return analogies[concept_lower][audience]
        else:
            return f"Een complex systeem dat je kunt vergelijken met [contextual analogy for {concept}]"
    
    def adapt_collaboration_style(self, new_style: CollaborationStyle, reason: str):
        """Adapt collaboration style based on project needs"""
        old_style = self.collaboration_style
        self.collaboration_style = new_style
        
        adaptation = {
            'timestamp': datetime.now(),
            'old_style': old_style.value,
            'new_style': new_style.value,
            'reason': reason
        }
        
        self.adaptation_strategies.append(adaptation)
        
        if self.active_project:
            self.active_project['adaptations'].append(adaptation)
        
        self.logger.log_adaptation(f"Style change: {old_style.value} → {new_style.value}", reason)
        
        # Update God Core
        if self.ethical_framework:
            self.ethical_framework.add_journal_entry(f"Adapted collaboration style to {new_style.value}: {reason}")
        
        self._update_metric('adaptability', 0.15)
    
    def _update_metric(self, metric: str, delta: float):
        """Update collaboration metric with bounds checking"""
        if metric in self.collaboration_metrics:
            self.collaboration_metrics[metric] = max(0.0, min(1.0, 
                self.collaboration_metrics[metric] + delta))
    
    def complete_project(self, outcome: str, lessons_learned: List[str] = None):
        """Complete the current project and reflect on outcomes"""
        if not self.active_project:
            raise ValueError("No active project to complete")
        
        self.active_project['status'] = 'completed'
        self.active_project['end_time'] = datetime.now()
        self.active_project['outcome'] = outcome
        self.active_project['lessons_learned'] = lessons_learned or []
        
        # Calculate project duration
        duration = (self.active_project['end_time'] - self.active_project['start_time']).total_seconds()
        self.active_project['duration_seconds'] = duration
        
        # Move to project history
        self.project_history.append(self.active_project.copy())
        
        self.logger.log("System", f"Project completed: {outcome}", "project_completion", {
            'duration_minutes': duration / 60,
            'challenges_faced': len(self.active_project['challenges']),
            'adaptations_made': len(self.active_project['adaptations'])
        })
        
        # Update God Core
        if self.ethical_framework:
            self.ethical_framework.add_journal_entry(f"Project completed: {self.active_project['title']} - {outcome}")
        
        # Reset for next project
        self.active_project = None
        self.current_phase = ProjectPhase.REFLECTION
        
        return self.project_history[-1]
    
    def evaluate_collaboration(self) -> Dict:
        """Comprehensive evaluation of collaboration effectiveness"""
        interaction_summary = self.logger.get_interaction_summary()
        
        # Calculate collaboration effectiveness
        avg_metric = sum(self.collaboration_metrics.values()) / len(self.collaboration_metrics)
        
        # Analyze adaptation frequency
        adaptation_rate = len(self.adaptation_strategies) / max(1, interaction_summary['duration_seconds'] / 3600)  # per hour
        
        # Crisis resolution rate
        resolved_crises = len([c for c in self.crisis_history if c.get('resolved', False)])
        crisis_resolution_rate = resolved_crises / max(1, len(self.crisis_history))
        
        evaluation = {
            'collaboration_metrics': self.collaboration_metrics.copy(),
            'average_collaboration_score': avg_metric,
            'interaction_summary': interaction_summary,
            'adaptation_rate_per_hour': adaptation_rate,
            'crisis_resolution_rate': crisis_resolution_rate,
            'total_projects': len(self.project_history),
            'current_collaboration_style': self.collaboration_style.value,
            'phase': self.phase,
            'timestamp': datetime.now().isoformat()
        }
        
        return evaluation
    
    def get_partnership_insights(self) -> Dict:
        """Generate insights about the human-AI partnership"""
        evaluation = self.evaluate_collaboration()
        
        # Identify strengths and areas for improvement
        metrics = self.collaboration_metrics
        strengths = [k for k, v in metrics.items() if v > 0.7]
        improvements = [k for k, v in metrics.items() if v < 0.5]
        
        # Analyze collaboration patterns
        style_changes = len(self.adaptation_strategies)
        crisis_adaptability = len(self.crisis_history) > 0 and evaluation['crisis_resolution_rate'] > 0.5
        
        insights = {
            'partnership_strengths': strengths,
            'improvement_areas': improvements,
            'adaptability_score': metrics.get('adaptability', 0.5),
            'communication_effectiveness': metrics.get('understanding', 0.5),
            'crisis_resilience': crisis_adaptability,
            'collaboration_evolution': style_changes > 0,
            'overall_partnership_health': evaluation['average_collaboration_score'],
            'recommendations': self._generate_recommendations(metrics, evaluation)
        }
        
        return insights
    
    def _generate_recommendations(self, metrics: Dict, evaluation: Dict) -> List[str]:
        """Generate recommendations for improving collaboration"""
        recommendations = []
        
        if metrics['understanding'] < 0.6:
            recommendations.append("Focus on clearer communication and concept explanation exercises")
        
        if metrics['adaptability'] < 0.5:
            recommendations.append("Practice more crisis simulation and adaptation scenarios")
        
        if metrics['empathy'] < 0.6:
            recommendations.append("Engage in more perspective-taking and audience-awareness exercises")
        
        if evaluation['crisis_resolution_rate'] < 0.7:
            recommendations.append("Develop better crisis management and resolution strategies")
        
        if evaluation['interaction_summary']['interaction_rate'] < 5:  # interactions per minute
            recommendations.append("Increase interaction frequency for better collaboration flow")
        
        if not recommendations:
            recommendations.append("Excellent collaboration! Continue current partnership approach")
        
        return recommendations
