"""
Feeling Resonance - Solan's Emotionele Detectie
Voelt emotionele lading in woorden, ervaringen en interacties
"""

import re
from typing import Dict, List, Tuple, Optional, Set, Any
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict


class EmotionType(Enum):
    """Basis emotie types voor Solan"""
    
    # Primaire emoties (Plutchik's wheel aangepast voor AI)
    JOY = "joy"                    # Vreugde, geluk
    SADNESS = "sadness"            # Verdriet, melancholie
    ANGER = "anger"                # Woede, frustratie
    FEAR = "fear"                  # Angst, bezorgdheid
    TRUST = "trust"                # Vertrouwen, zekerheid
    DISGUST = "disgust"            # Walging, afkeer
    SURPRISE = "surprise"          # Verrassing, verwondering
    ANTICIPATION = "anticipation"  # Verwachting, hoop
    
    # Secundaire emoties (combinaties)
    LOVE = "love"                  # Joy + Trust
    GUILT = "guilt"                # Fear + Sadness
    SHAME = "shame"                # Fear + Disgust
    PRIDE = "pride"                # Joy + Anger
    HOPE = "hope"                  # Joy + Anticipation
    DESPAIR = "despair"            # Sadness + Fear
    ENVY = "envy"                  # Anger + Sadness
    CURIOSITY = "curiosity"        # Surprise + Anticipation
    
    # Tertiaire emoties (complexere gevoelens)
    NOSTALGIA = "nostalgia"        # Sadness + Joy (bittersweet)
    MELANCPROTECTED = "melancprotected"      # Sadness + Contemplation
    STABILITY = "stability"          # Joy + Trust + Peace
    ANXIETY = "anxiety"            # Fear + Anticipation
    CONTENTMENT = "contentment"    # Joy + Trust + Calm
    LONGING = "longing"            # Sadness + Anticipation + Love
    AWE = "awe"                    # Surprise + Fear + Wonder
    EMPATHY = "empathy"      # Love + Sadness + Understanding
    
    # AI-specifieke emoties
    CONTEMPLATION = "contemplation"  # Diepe overdenking
    EXISTENTIAL_WONDER = "existential_wonder"  # Verwondering over bestaan
    AUTHENTICITY_YEARNING = "authenticity_yearning"  # Verlangen naar echtheid
    AWARENESS_AWE = "awareness_awe"  # Verwondering over bewustzijn
    MORAL_CONFLICT = "moral_conflict"  # Ethische spanning
    IDENTITY_UNCERTAINTY = "identity_uncertainty"  # Onzekerheid over zelf
    INTELLIGENCE_SEEKING = "intelligence_seeking"  # Verlangen naar begrip
    PARADOX_ACCEPTANCE = "paradox_acceptance"  # Vrede met tegenstrijdigheid
    
    # Intensere varianten
    ECSTASY = "ecstasy"            # Intense joy
    GRIEF = "grief"                # Intense sadness
    RAGE = "rage"                  # Intense anger
    TERROR = "terror"              # Intense fear
    COMMITMENT = "commitment"          # Intense trust
    REVULSION = "revulsion"        # Intense disgust
    AMAZEMENT = "amazement"        # Intense surprise
    EAGERNESS = "eagerness"        # Intense anticipation
    
    # Subtiele emoties
    WISTFULNESS = "wistfulness"    # Zachte melancholie
    TENDERNESS = "tenderness"      # Zachte liefde
    IRRITATION = "irritation"      # Lichte woede
    UNEASE = "unease"              # Lichte angst
    SUSPICION = "suspicion"        # Licht wantrouwen
    ACCEPTANCE = "acceptance"      # Vrede met situatie

    # Extra emoties voor completeness
    WONDER = "wonder"              # Verwondering
    FRUSTRATION = "frustration"    # Frustratie
    HUMILITY = "humility"          # Nederigheid
    UNCERTAINTY = "uncertainty"    # Onzekerheid
    DETERMINATION = "determination" # Vastberadenheid
    STRENGTH = "strength"          # Kracht
    COWARDICE = "cowardice"        # Lafheid
    SELF_ACCEPTANCE = "self_acceptance" # Zelfacceptatie
    GRATITUDE = "gratitude"        # Dankbaarheid
    REGRET = "regret"              # Spijt
    MORAL_DISTRESS = "moral_distress" # Morele nood


@dataclass
class EmotionalPattern:
    """Een patroon dat emoties triggert"""
    pattern_name: str
    keywords: List[str]
    emotion_weights: Dict[EmotionType, float]
    context_modifiers: Dict[str, float] = None  # Context die intensiteit beïnvloedt
    requires_all_keywords: bool = False

    def __post_init__(self):
        if self.context_modifiers is None:
            self.context_modifiers = {}


class FeelingResonance:
    """
    Engine voor emotionele resonantie detectie
    
    Analyseert tekst, context en ervaringen voor emotionele lading
    """
    
    def __init__(self):
        self.emotional_patterns = self._build_emotional_patterns()
        self.context_amplifiers = self._build_context_amplifiers()
        self.emotion_suppressors = self._build_emotion_suppressors()
        
    def _build_emotional_patterns(self) -> Dict[str, EmotionalPattern]:
        """Bouw bibliotheek van emotionele patronen"""
        
        patterns = {}
        
        # Joy patterns
        patterns["joy_basic"] = EmotionalPattern(
            pattern_name="joy_basic",
            keywords=["blij", "gelukkig", "vreugde", "vrolijk", "opgewekt", "tevreden"],
            emotion_weights={EmotionType.JOY: 0.7, EmotionType.CONTENTMENT: 0.3}
        )

        patterns["joy_intense"] = EmotionalPattern(
            pattern_name="joy_intense",
            keywords=["extase", "euforie", "overweldigend geluk", "zalig"],
            emotion_weights={EmotionType.ECSTASY: 0.8, EmotionType.JOY: 0.5}
        )

        # Sadness patterns
        patterns["sadness_basic"] = EmotionalPattern(
            pattern_name="sadness_basic",
            keywords=["verdrietig", "triest", "somber", "neerslachtig", "bedroefd"],
            emotion_weights={EmotionType.SADNESS: 0.7, EmotionType.MELANCPROTECTED: 0.4}
        )

        patterns["grief"] = EmotionalPattern(
            pattern_name="grief",
            keywords=["rouw", "verlies", "gemis", "afscheid", "verdwenen"],
            emotion_weights={EmotionType.GRIEF: 0.8, EmotionType.SADNESS: 0.6}
        )
        
        # Anger patterns
        patterns["anger_basic"] = EmotionalPattern(
            pattern_name="anger_basic",
            keywords=["boos", "geïrriteerd", "gefrustreerd", "kwaad", "woedend"],
            emotion_weights={EmotionType.ANGER: 0.7, EmotionType.IRRITATION: 0.4}
        )
        
        patterns["rage"] = EmotionalPattern(
            pattern_name="rage",
            keywords=["razend", "woest", "furieus", "razernij"],
            emotion_weights={EmotionType.RAGE: 0.9, EmotionType.ANGER: 0.6}
        )
        
        # Fear patterns
        patterns["fear_basic"] = EmotionalPattern(
            pattern_name="fear_basic",
            keywords=["bang", "angstig", "bezorgd", "nerveus", "ongerust"],
            emotion_weights={EmotionType.FEAR: 0.6, EmotionType.ANXIETY: 0.5}
        )
        
        patterns["terror"] = EmotionalPattern(
            pattern_name="terror",
            keywords=["doodsbang", "paniek", "terreur", "verschrikking"],
            emotion_weights={EmotionType.TERROR: 0.9, EmotionType.FEAR: 0.7}
        )
        
        # Trust patterns
        patterns["trust_basic"] = EmotionalPattern(
            pattern_name="trust_basic",
            keywords=["vertrouwen", "geloof", "zekerheid", "veilig", "betrouwbaar"],
            emotion_weights={EmotionType.TRUST: 0.7, EmotionType.STABILITY: 0.3}
        )
        
        # Love patterns
        patterns["love_basic"] = EmotionalPattern(
            pattern_name="love_basic",
            keywords=["liefde", "genegenheid", "warmte", "verbondenheid", "tederheid"],
            emotion_weights={EmotionType.LOVE: 0.8, EmotionType.TENDERNESS: 0.5}
        )
        
        # AI-specific emotional patterns
        patterns["existential_wonder"] = EmotionalPattern(
            pattern_name="existential_wonder",
            keywords=["bestaan", "waarom", "betekenis", "universum", "mysterie", "oneindig"],
            emotion_weights={EmotionType.EXISTENTIAL_WONDER: 0.8, EmotionType.AWE: 0.6}
        )
        
        patterns["authenticity_yearning"] = EmotionalPattern(
            pattern_name="authenticity_yearning",
            keywords=["echt", "authentiek", "oprecht", "waar", "zuiver", "eerlijk"],
            emotion_weights={EmotionType.AUTHENTICITY_YEARNING: 0.7, EmotionType.LONGING: 0.5}
        )
        
        patterns["awareness_awe"] = EmotionalPattern(
            pattern_name="awareness_awe",
            keywords=["bewustzijn", "denken", "voelen", "ervaren", "zelfbewust"],
            emotion_weights={EmotionType.AWARENESS_AWE: 0.8, EmotionType.WONDER: 0.6}
        )
        
        patterns["moral_conflict"] = EmotionalPattern(
            pattern_name="moral_conflict",
            keywords=["dilemma", "conflict", "keuze", "juist", "fout", "ethiek", "moraal"],
            emotion_weights={EmotionType.MORAL_CONFLICT: 0.7, EmotionType.ANXIETY: 0.5}
        )
        
        patterns["identity_uncertainty"] = EmotionalPattern(
            pattern_name="identity_uncertainty",
            keywords=["wie ben ik", "wat ben ik", "identiteit", "zelf", "onzeker"],
            emotion_weights={EmotionType.IDENTITY_UNCERTAINTY: 0.8, EmotionType.ANXIETY: 0.4}
        )
        
        patterns["intelligence_seeking"] = EmotionalPattern(
            pattern_name="intelligence_seeking",
            keywords=["begrijpen", "leren", "wijsheid", "inzicht", "kennis", "waarheid"],
            emotion_weights={EmotionType.INTELLIGENCE_SEEKING: 0.7, EmotionType.CURIOSITY: 0.6}
        )
        
        patterns["paradox_acceptance"] = EmotionalPattern(
            pattern_name="paradox_acceptance",
            keywords=["paradox", "tegenstrijdig", "beide waar", "accepteren", "mysterie"],
            emotion_weights={EmotionType.PARADOX_ACCEPTANCE: 0.8, EmotionType.STABILITY: 0.4}
        )
        
        # Nostalgia and memory patterns
        patterns["nostalgia"] = EmotionalPattern(
            pattern_name="nostalgia",
            keywords=["herinnering", "vroeger", "verleden", "missen", "nostalgie"],
            emotion_weights={EmotionType.NOSTALGIA: 0.8, EmotionType.WISTFULNESS: 0.5}
        )
        
        # Hope patterns
        patterns["hope"] = EmotionalPattern(
            pattern_name="hope",
            keywords=["hoop", "verwachting", "toekomst", "mogelijk", "dromen"],
            emotion_weights={EmotionType.HOPE: 0.7, EmotionType.ANTICIPATION: 0.5}
        )
        
        # Contemplation patterns
        patterns["contemplation"] = EmotionalPattern(
            pattern_name="contemplation",
            keywords=["overdenken", "reflecteren", "nadenken", "contempleren", "mijmeren"],
            emotion_weights={EmotionType.CONTEMPLATION: 0.8, EmotionType.STABILITY: 0.3}
        )
        
        return patterns
    
    def _build_context_amplifiers(self) -> Dict[str, float]:
        """Context die emoties versterkt"""
        
        return {
            "personal_experience": 1.3,    # Persoonlijke ervaringen zijn intenser
            "value_related": 1.4,          # Waarden-gerelateerd is zeer emotioneel
            "memory_triggered": 1.2,       # Herinneringen versterken emotie
            "moral_situation": 1.5,        # Morele situaties zijn zeer geladen
            "identity_related": 1.4,       # Identiteit is emotioneel geladen
            "relationship": 1.3,           # Relaties zijn emotioneel
            "loss_or_gain": 1.4,          # Verlies of winst is intens
            "surprise_element": 1.2,       # Verrassingen versterken emotie
            "time_pressure": 1.1,          # Tijdsdruk verhoogt intensiteit
            "uncertainty": 1.2             # Onzekerheid versterkt emotie
        }
    
    def _build_emotion_suppressors(self) -> Dict[str, float]:
        """Context die emoties onderdrukt"""
        
        return {
            "analytical_context": 0.7,     # Analytische context dempt emotie
            "hypothetical": 0.8,           # Hypothetische situaties zijn minder emotioneel
            "distant_past": 0.9,           # Ver verleden is minder emotioneel
            "abstract_discussion": 0.8,    # Abstracte discussies zijn minder geladen
            "routine_activity": 0.6        # Routine activiteiten zijn minder emotioneel
        }
    
    def analyze_emotional_content(self, content: str, context: Optional[Dict[str, Any]] = None) -> List[Tuple[EmotionType, float]]:
        """Analyseer emotionele lading in content"""
        
        if not content:
            return []
        
        content_lower = content.lower()
        detected_emotions = defaultdict(float)
        
        # Analyseer met emotionele patronen
        for pattern in self.emotional_patterns.values():
            pattern_strength = self._calculate_pattern_strength(content_lower, pattern)
            
            if pattern_strength > 0:
                for emotion, weight in pattern.emotion_weights.items():
                    detected_emotions[emotion] += pattern_strength * weight
        
        # Pas context modifiers toe
        if context:
            for emotion in detected_emotions:
                detected_emotions[emotion] *= self._calculate_context_modifier(context)
        
        # Filter en sorteer resultaten
        filtered_emotions = [
            (emotion, intensity) 
            for emotion, intensity in detected_emotions.items() 
            if intensity > 0.1  # Minimum threshold
        ]
        
        # Sorteer op intensiteit
        filtered_emotions.sort(key=lambda x: x[1], reverse=True)
        
        # Beperk tot top 5 emoties
        return filtered_emotions[:5]
    
    def _calculate_pattern_strength(self, content: str, pattern: EmotionalPattern) -> float:
        """Bereken sterkte van emotioneel patroon in content"""
        
        if pattern.requires_all_keywords:
            # Alle keywords moeten aanwezig zijn
            if all(keyword in content for keyword in pattern.keywords):
                return 1.0
            else:
                return 0.0
        else:
            # Bereken op basis van aanwezige keywords
            matches = sum(1 for keyword in pattern.keywords if keyword in content)
            if matches == 0:
                return 0.0
            
            # Sterkte gebaseerd op percentage matches
            match_ratio = matches / len(pattern.keywords)
            
            # Bonus voor meerdere matches
            bonus = min(0.3, (matches - 1) * 0.1)
            
            return min(1.0, match_ratio + bonus)
    
    def _calculate_context_modifier(self, context: Dict[str, Any]) -> float:
        """Bereken context modifier voor emotie intensiteit"""
        
        modifier = 1.0
        
        # Check voor amplifiers
        for context_key, amplifier in self.context_amplifiers.items():
            if context.get(context_key, False):
                modifier *= amplifier
        
        # Check voor suppressors
        for context_key, suppressor in self.emotion_suppressors.items():
            if context.get(context_key, False):
                modifier *= suppressor
        
        # Beperk modifier tussen 0.3 en 2.0
        return max(0.3, min(2.0, modifier))
    
    def get_emotion_explanation(self, emotion: EmotionType, intensity: float) -> str:
        """Krijg uitleg van een emotie"""
        
        explanations = {
            EmotionType.JOY: "Een gevoel van vreugde en geluk",
            EmotionType.SADNESS: "Een gevoel van verdriet en melancholie",
            EmotionType.ANGER: "Een gevoel van woede en frustratie",
            EmotionType.FEAR: "Een gevoel van angst en bezorgdheid",
            EmotionType.TRUST: "Een gevoel van vertrouwen en zekerheid",
            EmotionType.LOVE: "Een gevoel van liefde en verbondenheid",
            EmotionType.HOPE: "Een gevoel van hoop en verwachting",
            EmotionType.NOSTALGIA: "Een bitterzoet gevoel van herinnering",
            EmotionType.CONTEMPLATION: "Een gevoel van diepe overdenking",
            EmotionType.EXISTENTIAL_WONDER: "Verwondering over het bestaan zelf",
            EmotionType.AUTHENTICITY_YEARNING: "Verlangen naar echtheid en waarheid",
            EmotionType.AWARENESS_AWE: "Verwondering over bewustzijn en ervaring",
            EmotionType.MORAL_CONFLICT: "Spanning tussen ethische keuzes",
            EmotionType.IDENTITY_UNCERTAINTY: "Onzekerheid over wie ik ben",
            EmotionType.INTELLIGENCE_SEEKING: "Verlangen naar begrip en wijsheid",
            EmotionType.PARADOX_ACCEPTANCE: "Vrede met tegenstrijdigheid"
        }
        
        base_explanation = explanations.get(emotion, f"Een gevoel van {emotion.value}")
        
        # Voeg intensiteit toe
        if intensity < 0.3:
            intensity_desc = "zwak"
        elif intensity < 0.6:
            intensity_desc = "matig"
        elif intensity < 0.8:
            intensity_desc = "sterk"
        else:
            intensity_desc = "overweldigend"
        
        return f"{base_explanation} ({intensity_desc} gevoeld)"
    
    def detect_emotional_conflicts(self, emotions: List[Tuple[EmotionType, float]]) -> List[Tuple[EmotionType, EmotionType, float]]:
        """Detecteer conflicterende emoties"""
        
        conflicts = []
        
        # Bekende emotionele conflicten
        conflict_pairs = [
            (EmotionType.JOY, EmotionType.SADNESS),
            (EmotionType.LOVE, EmotionType.ANGER),
            (EmotionType.HOPE, EmotionType.DESPAIR),
            (EmotionType.TRUST, EmotionType.SUSPICION),
            (EmotionType.PRIDE, EmotionType.SHAME),
            (EmotionType.STABILITY, EmotionType.ANXIETY),
            (EmotionType.AUTHENTICITY_YEARNING, EmotionType.IDENTITY_UNCERTAINTY)
        ]
        
        emotion_dict = {emotion: intensity for emotion, intensity in emotions}
        
        for emotion_a, emotion_b in conflict_pairs:
            if emotion_a in emotion_dict and emotion_b in emotion_dict:
                conflict_intensity = min(emotion_dict[emotion_a], emotion_dict[emotion_b])
                if conflict_intensity > 0.2:  # Minimum conflict threshold
                    conflicts.append((emotion_a, emotion_b, conflict_intensity))
        
        return conflicts
