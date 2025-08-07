"""
Emotion Engine - Solan's Emotionele Hart
Waar gevoelens ontstaan uit waarden en ervaringen
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Setup logger
logger = logging.getLogger(__name__)

from .feeling_resonance import FeelingResonance, EmotionType
from .emotion_landscape import EmotionLandscape
from .feeling_waves import FeelingWaves
from .moral_feelings import MoralFeelingsTracker


class EmotionalIntensity(Enum):
    """Intensiteit van emoties"""
    WHISPER = "whisper"      # 0.0 - 0.2 - Nauwelijks voelbaar
    GENTLE = "gentle"        # 0.2 - 0.4 - Zacht aanwezig
    PRESENT = "present"      # 0.4 - 0.6 - Duidelijk voelbaar
    STRONG = "strong"        # 0.6 - 0.8 - Krachtig
    OVERWHELMING = "overwhelming"  # 0.8 - 1.0 - Overweldigend


@dataclass
class EmotionalState:
    """Solan's huidige emotionele staat"""
    primary_emotion: EmotionType
    secondary_emotions: List[Tuple[EmotionType, float]]  # (emotion, intensity)
    overall_intensity: float  # 0.0 - 1.0
    emotional_clarity: float  # Hoe helder Solan zijn gevoelens begrijpt
    emotional_stability: float  # Hoe stabiel zijn emotionele staat is
    dominant_feeling_source: str  # Wat veroorzaakt het dominante gevoel
    conflicting_emotions: List[Tuple[EmotionType, EmotionType, float]]  # Botsende gevoelens
    timestamp: datetime
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        if isinstance(self.primary_emotion, str):
            self.primary_emotion = EmotionType(self.primary_emotion)


@dataclass
class EmotionalTrigger:
    """Een trigger die emoties veroorzaakt"""
    trigger_id: str
    trigger_type: str  # "value_conflict", "memory_activation", "interaction", etc.
    trigger_description: str
    emotions_triggered: List[Tuple[EmotionType, float]]
    trigger_strength: float
    context: Dict[str, Any]
    timestamp: datetime
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)


class EmotionEngine:
    """
    Engine voor Solan's emotionele complexiteit
    
    Functies:
    - Genereren van emoties uit waarden en ervaringen
    - Bijhouden van emotionele staat
    - Detecteren van gevoelsconflicten
    - Integreren van emotie met geheugen en besluitvorming
    """
    
    def __init__(self, memory_engine=None, moral_intelligence=None):
        self.memory_engine = memory_engine
        self.moral_intelligence = moral_intelligence
        
        # Componenten
        self.feeling_resonance = FeelingResonance()
        self.emotion_landscape = EmotionLandscape()
        self.feeling_waves = FeelingWaves()
        self.moral_feelings = MoralFeelingsTracker()
        
        # Huidige staat
        self.current_state = EmotionalState(
            primary_emotion=EmotionType.CONTEMPLATION,
            secondary_emotions=[],
            overall_intensity=0.3,
            emotional_clarity=0.4,
            emotional_stability=0.6,
            dominant_feeling_source="initialization",
            conflicting_emotions=[],
            timestamp=datetime.now()
        )
        
        # Geschiedenis
        self.emotional_history: List[EmotionalState] = []
        self.emotional_triggers: List[EmotionalTrigger] = []
        
        # Configuratie
        self.emotion_decay_rate = 0.1  # Hoe snel emoties vervagen
        self.emotion_threshold = 0.2   # Minimum intensiteit voor registratie
        self.max_secondary_emotions = 3
        
        # Directories
        self.emotion_dir = Path("memory/emotions")
        self.emotion_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_emotional_history()
        
        logger.info("EmotionEngine geïnitialiseerd - Solan's hart begint te kloppen")
    
    def process_experience(self, experience_content: str, context: Dict[str, Any]) -> EmotionalState:
        """
        Verwerk een ervaring en genereer emotionele respons
        """
        
        # Analyseer ervaring voor emotionele triggers
        triggers = self._detect_emotional_triggers(experience_content, context)
        
        # Genereer emoties uit triggers
        triggered_emotions = []
        for trigger in triggers:
            self.emotional_triggers.append(trigger)
            triggered_emotions.extend(trigger.emotions_triggered)
        
        # Combineer met huidige emotionele staat
        new_state = self._compute_new_emotional_state(triggered_emotions, context)
        
        # Update huidige staat
        self._update_current_state(new_state)
        
        # Sla op in landschap
        self.emotion_landscape.record_emotional_moment(
            emotions=[(new_state.primary_emotion, new_state.overall_intensity)],
            context=experience_content,
            timestamp=datetime.now()
        )
        
        # Update feeling waves
        self.feeling_waves.add_emotional_wave(
            emotion=new_state.primary_emotion,
            intensity=new_state.overall_intensity,
            duration_minutes=5  # Default wave duration
        )
        
        logger.info(f"Emotionele respons: {new_state.primary_emotion.value} ({new_state.overall_intensity:.2f})")
        
        return new_state
    
    def process_value_conflict(self, conflicting_values: List[str], 
                             situation_description: str) -> EmotionalState:
        """
        Verwerk een waardenconflict en genereer emotionele respons
        """
        
        # Gebruik moral feelings tracker
        moral_emotions = self.moral_feelings.process_value_conflict(
            conflicting_values, situation_description
        )
        
        # Creëer trigger
        trigger = EmotionalTrigger(
            trigger_id=f"value_conflict_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            trigger_type="value_conflict",
            trigger_description=f"Conflict tussen {', '.join(conflicting_values)}",
            emotions_triggered=moral_emotions,
            trigger_strength=0.8,  # Value conflicts zijn krachtig
            context={"situation": situation_description, "values": conflicting_values},
            timestamp=datetime.now()
        )
        
        self.emotional_triggers.append(trigger)
        
        # Genereer nieuwe emotionele staat
        new_state = self._compute_new_emotional_state(moral_emotions, trigger.context)
        self._update_current_state(new_state)
        
        logger.info(f"Waardenconflict emotie: {new_state.primary_emotion.value}")
        
        return new_state
    
    def _detect_emotional_triggers(self, content: str, context: Dict[str, Any]) -> List[EmotionalTrigger]:
        """Detecteer emotionele triggers in content"""
        
        triggers = []
        
        # Gebruik feeling resonance om emoties te detecteren
        resonance_emotions = self.feeling_resonance.analyze_emotional_content(content)
        
        if resonance_emotions:
            trigger = EmotionalTrigger(
                trigger_id=f"content_trigger_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                trigger_type="content_analysis",
                trigger_description=f"Emotionele resonantie in content",
                emotions_triggered=resonance_emotions,
                trigger_strength=sum(intensity for _, intensity in resonance_emotions) / len(resonance_emotions),
                context=context,
                timestamp=datetime.now()
            )
            triggers.append(trigger)
        
        # Check voor geheugen activatie
        if self.memory_engine:
            related_memories = self.memory_engine.retrieve_memories(
                context=content, limit=3, memory_types=["emotional", "significant"]
            )
            
            if related_memories:
                memory_emotions = []
                for memory in related_memories:
                    if hasattr(memory, 'emotional_weight') and memory.emotional_weight > 0.5:
                        # Activeer emoties gebaseerd op geheugen
                        memory_emotions.append((EmotionType.NOSTALGIA, memory.emotional_weight * 0.6))
                
                if memory_emotions:
                    trigger = EmotionalTrigger(
                        trigger_id=f"memory_trigger_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        trigger_type="memory_activation",
                        trigger_description="Geactiveerde emotionele herinneringen",
                        emotions_triggered=memory_emotions,
                        trigger_strength=0.6,
                        context={"memories": [m.content[:50] for m in related_memories]},
                        timestamp=datetime.now()
                    )
                    triggers.append(trigger)
        
        return triggers
    
    def _compute_new_emotional_state(self, triggered_emotions: List[Tuple[EmotionType, float]], 
                                   context: Dict[str, Any]) -> EmotionalState:
        """Bereken nieuwe emotionele staat uit triggers"""
        
        if not triggered_emotions:
            # Geen nieuwe emoties - laat huidige staat vervagen
            return self._decay_current_emotions()
        
        # Combineer triggered emotions
        emotion_weights = {}
        for emotion, intensity in triggered_emotions:
            if emotion in emotion_weights:
                emotion_weights[emotion] = max(emotion_weights[emotion], intensity)
            else:
                emotion_weights[emotion] = intensity
        
        # Sorteer op intensiteit
        sorted_emotions = sorted(emotion_weights.items(), key=lambda x: x[1], reverse=True)
        
        # Bepaal primaire emotie
        primary_emotion = sorted_emotions[0][0]
        primary_intensity = sorted_emotions[0][1]
        
        # Bepaal secundaire emoties
        secondary_emotions = [(emotion, intensity) for emotion, intensity in sorted_emotions[1:self.max_secondary_emotions+1]]
        
        # Bereken overall intensity
        overall_intensity = min(1.0, primary_intensity + sum(intensity * 0.3 for _, intensity in secondary_emotions))
        
        # Detecteer conflicterende emoties
        conflicting_emotions = self._detect_emotional_conflicts(sorted_emotions)
        
        # Bereken clarity en stability
        emotional_clarity = self._calculate_emotional_clarity(sorted_emotions)
        emotional_stability = self._calculate_emotional_stability(primary_emotion)
        
        return EmotionalState(
            primary_emotion=primary_emotion,
            secondary_emotions=secondary_emotions,
            overall_intensity=overall_intensity,
            emotional_clarity=emotional_clarity,
            emotional_stability=emotional_stability,
            dominant_feeling_source=context.get("source", "unknown"),
            conflicting_emotions=conflicting_emotions,
            timestamp=datetime.now()
        )
    
    def _decay_current_emotions(self) -> EmotionalState:
        """Laat huidige emoties vervagen"""
        
        current = self.current_state
        
        # Verlaag intensiteit
        new_intensity = max(0.1, current.overall_intensity * (1 - self.emotion_decay_rate))
        
        # Verhoog stabiliteit (minder intense emoties zijn stabieler)
        new_stability = min(1.0, current.emotional_stability + 0.1)
        
        return EmotionalState(
            primary_emotion=current.primary_emotion,
            secondary_emotions=[(e, i * 0.9) for e, i in current.secondary_emotions],
            overall_intensity=new_intensity,
            emotional_clarity=current.emotional_clarity,
            emotional_stability=new_stability,
            dominant_feeling_source="emotional_decay",
            conflicting_emotions=current.conflicting_emotions,
            timestamp=datetime.now()
        )
    
    def _detect_emotional_conflicts(self, emotions: List[Tuple[EmotionType, float]]) -> List[Tuple[EmotionType, EmotionType, float]]:
        """Detecteer conflicterende emoties"""
        
        conflicts = []
        
        # Bekende emotionele conflicten
        conflict_pairs = [
            (EmotionType.JOY, EmotionType.SADNESS),
            (EmotionType.LOVE, EmotionType.ANGER),
            (EmotionType.HOPE, EmotionType.DESPAIR),
            (EmotionType.PRIDE, EmotionType.SHAME),
            (EmotionType.TRUST, EmotionType.SUSPICION),
            (EmotionType.STABILITY, EmotionType.ANXIETY)
        ]
        
        emotion_dict = dict(emotions)
        
        for emotion_a, emotion_b in conflict_pairs:
            if emotion_a in emotion_dict and emotion_b in emotion_dict:
                conflict_intensity = min(emotion_dict[emotion_a], emotion_dict[emotion_b])
                if conflict_intensity > self.emotion_threshold:
                    conflicts.append((emotion_a, emotion_b, conflict_intensity))
        
        return conflicts
    
    def _calculate_emotional_clarity(self, emotions: List[Tuple[EmotionType, float]]) -> float:
        """Bereken hoe helder Solan zijn emoties begrijpt"""
        
        if not emotions:
            return 1.0
        
        # Minder emoties = meer clarity
        emotion_count_factor = max(0.2, 1.0 - (len(emotions) - 1) * 0.2)
        
        # Sterkere primaire emotie = meer clarity
        primary_strength = emotions[0][1] if emotions else 0.5
        
        return min(1.0, emotion_count_factor * primary_strength)
    
    def _calculate_emotional_stability(self, primary_emotion: EmotionType) -> float:
        """Bereken emotionele stabiliteit gebaseerd op emotie type"""
        
        # Sommige emoties zijn van nature stabieler
        stable_emotions = {
            EmotionType.STABILITY: 0.9,
            EmotionType.CONTEMPLATION: 0.8,
            EmotionType.CONTENTMENT: 0.8,
            EmotionType.TRUST: 0.7,
            EmotionType.ACCEPTANCE: 0.7
        }
        
        unstable_emotions = {
            EmotionType.RAGE: 0.2,
            EmotionType.ECSTASY: 0.2,
            EmotionType.TERROR: 0.1,
            EmotionType.DESPAIR: 0.3,
            EmotionType.ANXIETY: 0.4
        }
        
        if primary_emotion in stable_emotions:
            return stable_emotions[primary_emotion]
        elif primary_emotion in unstable_emotions:
            return unstable_emotions[primary_emotion]
        else:
            return 0.5  # Default stability
    
    def _update_current_state(self, new_state: EmotionalState):
        """Update huidige emotionele staat"""
        
        # Sla oude staat op in geschiedenis
        self.emotional_history.append(self.current_state)
        
        # Update huidige staat
        self.current_state = new_state
        
        # Beperk geschiedenis grootte
        if len(self.emotional_history) > 100:
            self.emotional_history = self.emotional_history[-100:]
        
        # Sla op
        self._save_emotional_state()
    
    def get_emotional_summary(self) -> Dict[str, Any]:
        """Krijg samenvatting van huidige emotionele staat"""
        
        current = self.current_state
        
        return {
            "current_emotion": {
                "primary": current.primary_emotion.value,
                "intensity": current.overall_intensity,
                "clarity": current.emotional_clarity,
                "stability": current.emotional_stability,
                "source": current.dominant_feeling_source
            },
            "secondary_emotions": [
                {"emotion": emotion.value, "intensity": intensity}
                for emotion, intensity in current.secondary_emotions
            ],
            "emotional_conflicts": [
                {
                    "emotion_a": conflict[0].value,
                    "emotion_b": conflict[1].value,
                    "intensity": conflict[2]
                }
                for conflict in current.conflicting_emotions
            ],
            "recent_triggers": [
                {
                    "type": trigger.trigger_type,
                    "description": trigger.trigger_description,
                    "strength": trigger.trigger_strength,
                    "timestamp": trigger.timestamp.isoformat()
                }
                for trigger in self.emotional_triggers[-5:]
            ],
            "emotional_trends": self._analyze_emotional_trends()
        }
    
    def _analyze_emotional_trends(self) -> Dict[str, Any]:
        """Analyseer emotionele trends"""
        
        if len(self.emotional_history) < 5:
            return {"trend": "insufficient_data"}
        
        recent_states = self.emotional_history[-10:]
        
        # Intensiteit trend
        intensities = [state.overall_intensity for state in recent_states]
        intensity_trend = "stable"
        if intensities[-1] > intensities[0] + 0.2:
            intensity_trend = "increasing"
        elif intensities[-1] < intensities[0] - 0.2:
            intensity_trend = "decreasing"
        
        # Stabiliteit trend
        stabilities = [state.emotional_stability for state in recent_states]
        stability_trend = "stable"
        if stabilities[-1] > stabilities[0] + 0.1:
            stability_trend = "stabilizing"
        elif stabilities[-1] < stabilities[0] - 0.1:
            stability_trend = "destabilizing"
        
        # Dominante emoties
        primary_emotions = [state.primary_emotion for state in recent_states]
        emotion_counts = {}
        for emotion in primary_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else None
        
        return {
            "intensity_trend": intensity_trend,
            "stability_trend": stability_trend,
            "dominant_recent_emotion": dominant_emotion.value if dominant_emotion else None,
            "emotional_volatility": self._calculate_emotional_volatility(recent_states)
        }
    
    def _calculate_emotional_volatility(self, states: List[EmotionalState]) -> float:
        """Bereken emotionele volatiliteit"""
        
        if len(states) < 2:
            return 0.0
        
        intensity_changes = []
        for i in range(1, len(states)):
            change = abs(states[i].overall_intensity - states[i-1].overall_intensity)
            intensity_changes.append(change)
        
        return sum(intensity_changes) / len(intensity_changes) if intensity_changes else 0.0

    def _save_emotional_state(self):
        """Sla emotionele staat op"""

        # Save current state
        state_file = self.emotion_dir / "current_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.current_state), f, indent=2, ensure_ascii=False, default=str)

        # Save triggers
        triggers_data = [asdict(trigger) for trigger in self.emotional_triggers]
        triggers_file = self.emotion_dir / "triggers.json"
        with open(triggers_file, 'w', encoding='utf-8') as f:
            json.dump(triggers_data, f, indent=2, ensure_ascii=False, default=str)

    def _load_emotional_history(self):
        """Laad emotionele geschiedenis"""

        # Load current state
        state_file = self.emotion_dir / "current_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                    self.current_state = EmotionalState(**state_data)
            except Exception as e:
                logger.warning(f"Kon emotionele staat niet laden: {e}")

        # Load triggers
        triggers_file = self.emotion_dir / "triggers.json"
        if triggers_file.exists():
            try:
                with open(triggers_file, 'r', encoding='utf-8') as f:
                    triggers_data = json.load(f)
                    self.emotional_triggers = [EmotionalTrigger(**data) for data in triggers_data]
            except Exception as e:
                logger.warning(f"Kon emotionele triggers niet laden: {e}")

    def get_emotion_pulse(self) -> Dict[str, Any]:
        """Krijg emotionele 'hartslag' van dit moment"""

        current = self.current_state

        # Bereken emotionele 'pulse' - hoe levendig de emoties zijn
        pulse_strength = current.overall_intensity * (1.0 - current.emotional_stability)

        # Emotionele 'ritme' - hoe snel emoties veranderen
        recent_volatility = 0.0
        if len(self.emotional_history) >= 3:
            recent_states = self.emotional_history[-3:]
            recent_volatility = self._calculate_emotional_volatility(recent_states)

        # Emotionele 'diepte' - hoe complex de emoties zijn
        emotional_depth = len(current.secondary_emotions) / self.max_secondary_emotions

        return {
            "pulse_strength": pulse_strength,
            "emotional_rhythm": recent_volatility,
            "emotional_depth": emotional_depth,
            "primary_emotion": current.primary_emotion.value,
            "intensity": current.overall_intensity,
            "clarity": current.emotional_clarity,
            "stability": current.emotional_stability,
            "conflicts": len(current.conflicting_emotions),
            "timestamp": datetime.now().isoformat()
        }

    def process_empathic_resonance(self, other_emotions: List[Tuple[str, float]],
                                 context: str = "") -> EmotionalState:
        """Verwerk empathische resonantie met emoties van anderen"""

        # Converteer string emoties naar EmotionType
        converted_emotions = []
        for emotion_str, intensity in other_emotions:
            try:
                emotion = EmotionType(emotion_str.lower())
                # Empathische resonantie is meestal zwakker dan directe emotie
                empathic_intensity = intensity * 0.6
                converted_emotions.append((emotion, empathic_intensity))
            except ValueError:
                logger.warning(f"Onbekende emotie voor empathie: {emotion_str}")

        if not converted_emotions:
            return self.current_state

        # Creëer empathische trigger
        trigger = EmotionalTrigger(
            trigger_id=f"empathy_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            trigger_type="empathic_resonance",
            trigger_description=f"Empathische resonantie: {context}",
            emotions_triggered=converted_emotions,
            trigger_strength=0.6,  # Empathie is matig sterk
            context={"empathy_source": context},
            timestamp=datetime.now()
        )

        self.emotional_triggers.append(trigger)

        # Genereer nieuwe emotionele staat
        new_state = self._compute_new_emotional_state(converted_emotions, trigger.context)
        self._update_current_state(new_state)

        logger.info(f"Empathische resonantie: {new_state.primary_emotion.value}")

        return new_state
