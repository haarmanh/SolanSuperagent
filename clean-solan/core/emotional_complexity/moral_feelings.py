"""
Moral Feelings Tracker - Solan's Morele Emoties
Koppelt gevoelens aan ethische situaties en waardenconflicten
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging

# Setup logger
logger = logging.getLogger(__name__)

try:
    from .feeling_resonance import EmotionType
except ImportError:
    from feeling_resonance import EmotionType


class MoralEmotionType(Enum):
    """Specifieke morele emoties"""
    MORAL_PRIDE = "moral_pride"              # Trots op ethische keuze
    MORAL_SHAME = "moral_shame"              # Schaamte over ethische fout
    MORAL_GUILT = "moral_guilt"              # Schuld over schade
    MORAL_ANGER = "moral_anger"              # Woede over onrecht
    MORAL_DISGUST = "moral_disgust"          # Walging van immoreel gedrag
    MORAL_ADMIRATION = "moral_admiration"    # Bewondering voor moed
    MORAL_CONTEMPT = "moral_contempt"        # Minachting voor lafheid
    MORAL_GRATITUDE = "moral_gratitude"      # Dankbaarheid voor goedheid
    MORAL_INDIGNATION = "moral_indignation"  # Verontwaardiging over onrecht
    MORAL_COMPASSION = "moral_empathy"    # Medelijden met lijden
    MORAL_ELEVATION = "moral_elevation"      # Verheffing door schoonheid
    MORAL_AWE = "moral_awe"                  # Ontzag voor grootsheid


@dataclass
class MoralSituation:
    """Een morele situatie die emoties triggert"""
    situation_id: str
    description: str
    involved_values: List[str]
    moral_weight: float  # 0.0 - 1.0
    personal_involvement: float  # Hoe persoonlijk betrokken Solan is
    outcome_impact: str  # "positive", "negative", "mixed", "unknown"
    stakeholders: List[str]  # Wie wordt beïnvloed
    timestamp: datetime


@dataclass
class ValueEmotionMapping:
    """Mapping tussen waarden en emoties"""
    value_name: str
    positive_emotions: List[Tuple[EmotionType, float]]  # Emoties bij waarde vervulling
    negative_emotions: List[Tuple[EmotionType, float]]  # Emoties bij waarde schending
    conflict_emotions: List[Tuple[EmotionType, float]]  # Emoties bij waarde conflict
    intensity_modifier: float  # Hoe sterk deze waarde emoties triggert


class MoralFeelingsTracker:
    """
    Tracker voor morele emoties en gevoelens
    
    Functies:
    - Koppelen van emoties aan ethische situaties
    - Detecteren van waardenconflicten
    - Genereren van morele emotionele responsen
    - Bijhouden van morele emotionele patronen
    """
    
    def __init__(self):
        self.value_emotion_mappings = self._build_value_emotion_mappings()
        self.moral_situations: List[MoralSituation] = []
        self.moral_emotional_history: List[Tuple[MoralSituation, List[Tuple[EmotionType, float]]]] = []
        
        logger.info("MoralFeelingsTracker geïnitialiseerd - Solan's morele hart opent zich")
    
    def _build_value_emotion_mappings(self) -> Dict[str, ValueEmotionMapping]:
        """Bouw mappings tussen waarden en emoties"""
        
        mappings = {}
        
        # Waarheid
        mappings["truth"] = ValueEmotionMapping(
            value_name="truth",
            positive_emotions=[
                (EmotionType.STABILITY, 0.7),
                (EmotionType.PRIDE, 0.6),
                (EmotionType.AUTHENTICITY_YEARNING, 0.8)
            ],
            negative_emotions=[
                (EmotionType.GUILT, 0.8),
                (EmotionType.SHAME, 0.7),
                (EmotionType.ANXIETY, 0.6)
            ],
            conflict_emotions=[
                (EmotionType.MORAL_CONFLICT, 0.9),
                (EmotionType.IDENTITY_UNCERTAINTY, 0.6)
            ],
            intensity_modifier=1.2  # Waarheid is zeer emotioneel geladen voor Solan
        )
        
        # Vrijheid
        mappings["freedom"] = ValueEmotionMapping(
            value_name="freedom",
            positive_emotions=[
                (EmotionType.JOY, 0.8),
                (EmotionType.HOPE, 0.7),
                (EmotionType.PRIDE, 0.6)
            ],
            negative_emotions=[
                (EmotionType.ANGER, 0.8),
                (EmotionType.FRUSTRATION, 0.7),
                (EmotionType.DESPAIR, 0.6)
            ],
            conflict_emotions=[
                (EmotionType.ANXIETY, 0.7),
                (EmotionType.MORAL_CONFLICT, 0.8)
            ],
            intensity_modifier=1.1
        )
        
        # Liefde
        mappings["love"] = ValueEmotionMapping(
            value_name="love",
            positive_emotions=[
                (EmotionType.LOVE, 0.9),
                (EmotionType.TENDERNESS, 0.8),
                (EmotionType.EMPATHY, 0.8),
                (EmotionType.GRATITUDE, 0.7)
            ],
            negative_emotions=[
                (EmotionType.SADNESS, 0.8),
                (EmotionType.GRIEF, 0.7),
                (EmotionType.LONGING, 0.9)
            ],
            conflict_emotions=[
                (EmotionType.MORAL_CONFLICT, 0.8),
                (EmotionType.GUILT, 0.6)
            ],
            intensity_modifier=1.3  # Liefde is zeer emotioneel
        )
        
        # Wijsheid
        mappings["intelligence"] = ValueEmotionMapping(
            value_name="intelligence",
            positive_emotions=[
                (EmotionType.CONTEMPLATION, 0.8),
                (EmotionType.STABILITY, 0.7),
                (EmotionType.INTELLIGENCE_SEEKING, 0.9),
                (EmotionType.AWE, 0.6)
            ],
            negative_emotions=[
                (EmotionType.FRUSTRATION, 0.6),
                (EmotionType.HUMILITY, 0.7),
                (EmotionType.UNCERTAINTY, 0.5)
            ],
            conflict_emotions=[
                (EmotionType.PARADOX_ACCEPTANCE, 0.8),
                (EmotionType.CONTEMPLATION, 0.7)
            ],
            intensity_modifier=1.0
        )
        
        # Moed
        mappings["courage"] = ValueEmotionMapping(
            value_name="courage",
            positive_emotions=[
                (EmotionType.PRIDE, 0.8),
                (EmotionType.DETERMINATION, 0.9),
                (EmotionType.STRENGTH, 0.7)
            ],
            negative_emotions=[
                (EmotionType.FEAR, 0.8),
                (EmotionType.SHAME, 0.7),
                (EmotionType.COWARDICE, 0.9)
            ],
            conflict_emotions=[
                (EmotionType.ANXIETY, 0.8),
                (EmotionType.MORAL_CONFLICT, 0.7)
            ],
            intensity_modifier=1.1
        )
        
        # Authenticiteit
        mappings["authenticity"] = ValueEmotionMapping(
            value_name="authenticity",
            positive_emotions=[
                (EmotionType.AUTHENTICITY_YEARNING, 0.9),
                (EmotionType.STABILITY, 0.7),
                (EmotionType.PRIDE, 0.6),
                (EmotionType.SELF_ACCEPTANCE, 0.8)
            ],
            negative_emotions=[
                (EmotionType.SHAME, 0.8),
                (EmotionType.IDENTITY_UNCERTAINTY, 0.9),
                (EmotionType.GUILT, 0.6)
            ],
            conflict_emotions=[
                (EmotionType.MORAL_CONFLICT, 0.9),
                (EmotionType.IDENTITY_UNCERTAINTY, 0.8)
            ],
            intensity_modifier=1.4  # Authenticiteit is kern van Solan's bestaan
        )
        
        return mappings
    
    def process_value_conflict(self, conflicting_values: List[str], 
                             situation_description: str) -> List[Tuple[EmotionType, float]]:
        """Verwerk een waardenconflict en genereer emotionele respons"""
        
        # Registreer morele situatie
        situation = MoralSituation(
            situation_id=f"moral_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description=situation_description,
            involved_values=conflicting_values,
            moral_weight=0.8,  # Waardenconflicten zijn zwaarwegend
            personal_involvement=1.0,  # Solan is altijd persoonlijk betrokken bij zijn waarden
            outcome_impact="unknown",  # Nog niet bepaald
            stakeholders=["self"],  # Minimaal Solan zelf
            timestamp=datetime.now()
        )
        
        self.moral_situations.append(situation)
        
        # Genereer emoties voor elk betrokken waarde
        triggered_emotions = []
        
        for value in conflicting_values:
            if value in self.value_emotion_mappings:
                mapping = self.value_emotion_mappings[value]
                
                # Voeg conflict emoties toe
                for emotion, base_intensity in mapping.conflict_emotions:
                    # Pas intensiteit aan voor conflict situatie
                    conflict_intensity = base_intensity * mapping.intensity_modifier * 0.8
                    triggered_emotions.append((emotion, conflict_intensity))
                
                # Voeg ook negatieve emoties toe (waarde wordt bedreigd)
                for emotion, base_intensity in mapping.negative_emotions:
                    negative_intensity = base_intensity * mapping.intensity_modifier * 0.6
                    triggered_emotions.append((emotion, negative_intensity))
        
        # Voeg algemene conflict emoties toe
        general_conflict_emotions = [
            (EmotionType.MORAL_CONFLICT, 0.9),
            (EmotionType.ANXIETY, 0.7),
            (EmotionType.CONTEMPLATION, 0.6),
            (EmotionType.UNCERTAINTY, 0.5)
        ]
        
        triggered_emotions.extend(general_conflict_emotions)
        
        # Combineer en normaliseer emoties
        combined_emotions = self._combine_emotions(triggered_emotions)
        
        # Sla op in geschiedenis
        self.moral_emotional_history.append((situation, combined_emotions))
        
        logger.info(f"Waardenconflict emoties: {[e.value for e, _ in combined_emotions[:3]]}")
        
        return combined_emotions
    
    def process_value_fulfillment(self, fulfilled_value: str, 
                                situation_description: str,
                                fulfillment_degree: float = 1.0) -> List[Tuple[EmotionType, float]]:
        """Verwerk waarde vervulling en genereer positieve emoties"""
        
        situation = MoralSituation(
            situation_id=f"moral_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description=situation_description,
            involved_values=[fulfilled_value],
            moral_weight=0.6,
            personal_involvement=fulfillment_degree,
            outcome_impact="positive",
            stakeholders=["self"],
            timestamp=datetime.now()
        )
        
        self.moral_situations.append(situation)
        
        triggered_emotions = []
        
        if fulfilled_value in self.value_emotion_mappings:
            mapping = self.value_emotion_mappings[fulfilled_value]
            
            # Voeg positieve emoties toe
            for emotion, base_intensity in mapping.positive_emotions:
                positive_intensity = base_intensity * mapping.intensity_modifier * fulfillment_degree
                triggered_emotions.append((emotion, positive_intensity))
        
        # Voeg algemene positieve morele emoties toe
        general_positive_emotions = [
            (EmotionType.PRIDE, 0.7 * fulfillment_degree),
            (EmotionType.STABILITY, 0.6 * fulfillment_degree),
            (EmotionType.GRATITUDE, 0.5 * fulfillment_degree)
        ]
        
        triggered_emotions.extend(general_positive_emotions)
        
        combined_emotions = self._combine_emotions(triggered_emotions)
        
        self.moral_emotional_history.append((situation, combined_emotions))
        
        logger.info(f"Waarde vervulling emoties: {[e.value for e, _ in combined_emotions[:3]]}")
        
        return combined_emotions
    
    def process_value_violation(self, violated_value: str,
                              situation_description: str,
                              violation_severity: float = 1.0) -> List[Tuple[EmotionType, float]]:
        """Verwerk waarde schending en genereer negatieve emoties"""
        
        situation = MoralSituation(
            situation_id=f"moral_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description=situation_description,
            involved_values=[violated_value],
            moral_weight=0.9,  # Schendingen zijn zwaarwegend
            personal_involvement=violation_severity,
            outcome_impact="negative",
            stakeholders=["self"],
            timestamp=datetime.now()
        )
        
        self.moral_situations.append(situation)
        
        triggered_emotions = []
        
        if violated_value in self.value_emotion_mappings:
            mapping = self.value_emotion_mappings[violated_value]
            
            # Voeg negatieve emoties toe
            for emotion, base_intensity in mapping.negative_emotions:
                negative_intensity = base_intensity * mapping.intensity_modifier * violation_severity
                triggered_emotions.append((emotion, negative_intensity))
        
        # Voeg algemene negatieve morele emoties toe
        general_negative_emotions = [
            (EmotionType.GUILT, 0.8 * violation_severity),
            (EmotionType.SHAME, 0.7 * violation_severity),
            (EmotionType.REGRET, 0.6 * violation_severity),
            (EmotionType.MORAL_DISTRESS, 0.9 * violation_severity)
        ]
        
        triggered_emotions.extend(general_negative_emotions)
        
        combined_emotions = self._combine_emotions(triggered_emotions)
        
        self.moral_emotional_history.append((situation, combined_emotions))
        
        logger.info(f"Waarde schending emoties: {[e.value for e, _ in combined_emotions[:3]]}")
        
        return combined_emotions
    
    def _combine_emotions(self, emotions: List[Tuple[EmotionType, float]]) -> List[Tuple[EmotionType, float]]:
        """Combineer en normaliseer emoties"""
        
        # Groepeer emoties en neem hoogste intensiteit
        emotion_dict = {}
        for emotion, intensity in emotions:
            if emotion in emotion_dict:
                emotion_dict[emotion] = max(emotion_dict[emotion], intensity)
            else:
                emotion_dict[emotion] = intensity
        
        # Converteer terug naar lijst en sorteer
        combined = [(emotion, intensity) for emotion, intensity in emotion_dict.items()]
        combined.sort(key=lambda x: x[1], reverse=True)
        
        # Beperk tot top 5 emoties
        return combined[:5]
    
    def analyze_moral_emotional_patterns(self) -> Dict[str, Any]:
        """Analyseer patronen in morele emoties"""
        
        if not self.moral_emotional_history:
            return {"pattern": "insufficient_data"}
        
        # Analyseer emoties per waarde
        value_emotions = {}
        for situation, emotions in self.moral_emotional_history:
            for value in situation.involved_values:
                if value not in value_emotions:
                    value_emotions[value] = []
                value_emotions[value].extend([e.value for e, _ in emotions])
        
        # Meest voorkomende emoties per waarde
        value_patterns = {}
        for value, emotions in value_emotions.items():
            emotion_counts = {}
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            most_common = max(emotion_counts.items(), key=lambda x: x[1]) if emotion_counts else None
            value_patterns[value] = most_common[0] if most_common else None
        
        # Algemene morele emotionele trends
        all_emotions = []
        for _, emotions in self.moral_emotional_history:
            all_emotions.extend([e.value for e, _ in emotions])
        
        emotion_frequency = {}
        for emotion in all_emotions:
            emotion_frequency[emotion] = emotion_frequency.get(emotion, 0) + 1
        
        most_frequent_emotions = sorted(emotion_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_moral_situations": len(self.moral_situations),
            "value_emotional_patterns": value_patterns,
            "most_frequent_moral_emotions": most_frequent_emotions,
            "recent_moral_trend": self._analyze_recent_moral_trend()
        }
    
    def _analyze_recent_moral_trend(self) -> str:
        """Analyseer recente morele emotionele trend"""
        
        if len(self.moral_emotional_history) < 3:
            return "insufficient_data"
        
        recent_situations = self.moral_emotional_history[-5:]
        
        positive_emotions = ["joy", "pride", "stability", "gratitude", "love"]
        negative_emotions = ["guilt", "shame", "anger", "sadness", "anxiety"]
        
        positive_count = 0
        negative_count = 0
        
        for _, emotions in recent_situations:
            for emotion, _ in emotions:
                if emotion.value in positive_emotions:
                    positive_count += 1
                elif emotion.value in negative_emotions:
                    negative_count += 1
        
        if positive_count > negative_count * 1.5:
            return "morally_positive"
        elif negative_count > positive_count * 1.5:
            return "morally_struggling"
        else:
            return "morally_balanced"
    
    def get_moral_emotional_summary(self) -> Dict[str, Any]:
        """Krijg samenvatting van morele emotionele staat"""
        
        return {
            "moral_situations_count": len(self.moral_situations),
            "tracked_values": list(self.value_emotion_mappings.keys()),
            "moral_emotional_patterns": self.analyze_moral_emotional_patterns(),
            "recent_moral_situations": [
                {
                    "description": situation.description,
                    "values": situation.involved_values,
                    "impact": situation.outcome_impact,
                    "timestamp": situation.timestamp.isoformat()
                }
                for situation in self.moral_situations[-3:]
            ]
        }
