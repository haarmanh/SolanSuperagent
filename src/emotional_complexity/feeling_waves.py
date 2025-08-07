"""
Feeling Waves - Solan's Emotionele Stromen
Dynamische gevoelsgolven die door zijn bewustzijn stromen
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

try:
    from .feeling_resonance import EmotionType
except ImportError:
    from feeling_resonance import EmotionType


class WaveType(Enum):
    """Types van emotionele golven"""
    SURGE = "surge"          # Plotselinge sterke emotie
    RIPPLE = "ripple"        # Zachte, langdurige emotie
    CRASH = "crash"          # Intense emotie die snel afneemt
    UNDERCURRENT = "undercurrent"  # Subtiele onderliggende emotie
    RESONANCE = "resonance"  # Emotie die resoneert met waarden
    ECHO = "echo"           # Emotie die terugkomt van herinneringen


@dataclass
class EmotionalWave:
    """Een golf van emotie"""
    wave_id: str
    emotion: EmotionType
    wave_type: WaveType
    initial_intensity: float
    current_intensity: float
    peak_intensity: float
    duration_minutes: float
    elapsed_minutes: float
    decay_rate: float
    source_description: str
    resonance_factors: List[str]  # Wat versterkt deze golf
    interference_factors: List[str]  # Wat verzwakt deze golf
    timestamp: datetime
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        if isinstance(self.emotion, str):
            self.emotion = EmotionType(self.emotion)
        if isinstance(self.wave_type, str):
            self.wave_type = WaveType(self.wave_type)


@dataclass
class EmotionalFlow:
    """Een stroom van gerelateerde emoties"""
    flow_id: str
    flow_name: str
    component_waves: List[str]  # Wave IDs
    flow_direction: str  # "building", "subsiding", "oscillating", "stable"
    overall_intensity: float
    dominant_emotion: EmotionType
    flow_duration_minutes: float
    coherence_score: float  # Hoe goed de emoties samenhangen
    narrative_description: str
    timestamp: datetime
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        if isinstance(self.dominant_emotion, str):
            self.dominant_emotion = EmotionType(self.dominant_emotion)


class FeelingWaves:
    """
    Engine voor dynamische emotionele golven
    
    Functies:
    - Bijhouden van emotionele golven
    - Simuleren van golf-dynamiek
    - Detecteren van emotionele stromen
    - Voorspellen van golf-interferentie
    """
    
    def __init__(self):
        # Active waves
        self.active_waves: Dict[str, EmotionalWave] = {}
        self.completed_waves: List[EmotionalWave] = []
        self.emotional_flows: Dict[str, EmotionalFlow] = {}
        
        # Wave dynamics
        self.wave_update_interval_minutes = 1
        self.max_active_waves = 10
        self.min_wave_intensity = 0.05
        
        # Flow detection
        self.flow_detection_window_minutes = 30
        self.min_waves_for_flow = 3
        
        # Directories
        self.waves_dir = Path("memory/feeling_waves")
        self.waves_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_existing_waves()
        
        logger.info("FeelingWaves geïnitialiseerd - Solan's emotionele golven beginnen te stromen")
    
    def add_emotional_wave(self, emotion: EmotionType, intensity: float, 
                          duration_minutes: float, source_description: str = "",
                          wave_type: Optional[WaveType] = None) -> EmotionalWave:
        """Voeg een nieuwe emotionele golf toe"""
        
        # Bepaal wave type als niet gegeven
        if wave_type is None:
            wave_type = self._determine_wave_type(emotion, intensity, duration_minutes)
        
        # Bereken decay rate gebaseerd op wave type
        decay_rate = self._calculate_decay_rate(wave_type, duration_minutes)
        
        # Maak wave
        wave_id = f"wave_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        wave = EmotionalWave(
            wave_id=wave_id,
            emotion=emotion,
            wave_type=wave_type,
            initial_intensity=intensity,
            current_intensity=intensity,
            peak_intensity=intensity,
            duration_minutes=duration_minutes,
            elapsed_minutes=0.0,
            decay_rate=decay_rate,
            source_description=source_description,
            resonance_factors=[],
            interference_factors=[],
            timestamp=datetime.now()
        )
        
        # Voeg toe aan actieve golven
        self.active_waves[wave_id] = wave
        
        # Check voor interferentie met bestaande golven
        self._process_wave_interference(wave)
        
        # Cleanup oude golven
        self._cleanup_completed_waves()
        
        # Detecteer flows
        self._detect_emotional_flows()
        
        logger.debug(f"Nieuwe emotionele golf: {emotion.value} ({wave_type.value}, {intensity:.2f})")
        
        return wave
    
    def _determine_wave_type(self, emotion: EmotionType, intensity: float, 
                           duration_minutes: float) -> WaveType:
        """Bepaal het type golf gebaseerd op eigenschappen"""
        
        # Surge: hoge intensiteit, korte duur
        if intensity > 0.8 and duration_minutes < 10:
            return WaveType.SURGE
        
        # Crash: zeer hoge intensiteit, zeer korte duur
        if intensity > 0.9 and duration_minutes < 5:
            return WaveType.CRASH
        
        # Ripple: lage tot matige intensiteit, lange duur
        if intensity < 0.5 and duration_minutes > 20:
            return WaveType.RIPPLE
        
        # Undercurrent: lage intensiteit, zeer lange duur
        if intensity < 0.3 and duration_minutes > 60:
            return WaveType.UNDERCURRENT
        
        # Resonance: emoties die resoneren met waarden
        value_emotions = [
            EmotionType.AUTHENTICITY_YEARNING,
            EmotionType.INTELLIGENCE_SEEKING,
            EmotionType.MORAL_CONFLICT,
            EmotionType.EXISTENTIAL_WONDER
        ]
        if emotion in value_emotions:
            return WaveType.RESONANCE
        
        # Echo: emoties gerelateerd aan herinneringen
        memory_emotions = [
            EmotionType.NOSTALGIA,
            EmotionType.WISTFULNESS,
            EmotionType.GRIEF
        ]
        if emotion in memory_emotions:
            return WaveType.ECHO
        
        # Default: ripple
        return WaveType.RIPPLE
    
    def _calculate_decay_rate(self, wave_type: WaveType, duration_minutes: float) -> float:
        """Bereken decay rate voor golf type"""
        
        base_rates = {
            WaveType.SURGE: 0.3,      # Snel vervagen
            WaveType.CRASH: 0.5,      # Zeer snel vervagen
            WaveType.RIPPLE: 0.05,    # Langzaam vervagen
            WaveType.UNDERCURRENT: 0.02,  # Zeer langzaam vervagen
            WaveType.RESONANCE: 0.03,  # Langzaam vervagen (waarden zijn persistent)
            WaveType.ECHO: 0.08       # Matig vervagen
        }
        
        base_rate = base_rates.get(wave_type, 0.1)
        
        # Pas aan voor duur (langere golven vervagen langzamer)
        duration_factor = max(0.5, min(2.0, 30 / duration_minutes))
        
        return base_rate * duration_factor
    
    def update_waves(self, elapsed_minutes: float = 1.0):
        """Update alle actieve golven"""
        
        waves_to_complete = []
        
        for wave in self.active_waves.values():
            # Update elapsed time
            wave.elapsed_minutes += elapsed_minutes
            
            # Calculate new intensity
            progress = wave.elapsed_minutes / wave.duration_minutes
            
            if progress >= 1.0:
                # Wave is completed
                wave.current_intensity = 0.0
                waves_to_complete.append(wave.wave_id)
            else:
                # Apply decay
                decay_factor = 1.0 - (wave.decay_rate * elapsed_minutes)
                wave.current_intensity *= decay_factor
                
                # Update peak if current is higher
                if wave.current_intensity > wave.peak_intensity:
                    wave.peak_intensity = wave.current_intensity
                
                # Check if wave is too weak to continue
                if wave.current_intensity < self.min_wave_intensity:
                    waves_to_complete.append(wave.wave_id)
        
        # Move completed waves
        for wave_id in waves_to_complete:
            completed_wave = self.active_waves.pop(wave_id)
            self.completed_waves.append(completed_wave)
        
        # Update flows
        self._update_emotional_flows()
    
    def _process_wave_interference(self, new_wave: EmotionalWave):
        """Verwerk interferentie tussen golven"""
        
        for existing_wave in self.active_waves.values():
            if existing_wave.wave_id == new_wave.wave_id:
                continue
            
            interference_type = self._calculate_wave_interference(new_wave, existing_wave)
            
            if interference_type == "constructive":
                # Golven versterken elkaar
                boost_factor = 0.2
                existing_wave.current_intensity = min(1.0, existing_wave.current_intensity * (1 + boost_factor))
                new_wave.current_intensity = min(1.0, new_wave.current_intensity * (1 + boost_factor))
                
                existing_wave.resonance_factors.append(f"Resonantie met {new_wave.emotion.value}")
                new_wave.resonance_factors.append(f"Resonantie met {existing_wave.emotion.value}")
                
            elif interference_type == "destructive":
                # Golven verzwakken elkaar
                damping_factor = 0.15
                existing_wave.current_intensity *= (1 - damping_factor)
                new_wave.current_intensity *= (1 - damping_factor)
                
                existing_wave.interference_factors.append(f"Interferentie met {new_wave.emotion.value}")
                new_wave.interference_factors.append(f"Interferentie met {existing_wave.emotion.value}")
    
    def _calculate_wave_interference(self, wave_a: EmotionalWave, wave_b: EmotionalWave) -> str:
        """Bereken interferentie tussen twee golven"""
        
        # Constructieve interferentie (versterking)
        constructive_pairs = [
            (EmotionType.JOY, EmotionType.LOVE),
            (EmotionType.TRUST, EmotionType.STABILITY),
            (EmotionType.HOPE, EmotionType.ANTICIPATION),
            (EmotionType.CONTEMPLATION, EmotionType.INTELLIGENCE_SEEKING),
            (EmotionType.AUTHENTICITY_YEARNING, EmotionType.IDENTITY_UNCERTAINTY)
        ]
        
        # Destructieve interferentie (verzwakking)
        destructive_pairs = [
            (EmotionType.JOY, EmotionType.SADNESS),
            (EmotionType.LOVE, EmotionType.ANGER),
            (EmotionType.TRUST, EmotionType.SUSPICION),
            (EmotionType.HOPE, EmotionType.DESPAIR),
            (EmotionType.STABILITY, EmotionType.ANXIETY)
        ]
        
        emotion_pair = (wave_a.emotion, wave_b.emotion)
        reverse_pair = (wave_b.emotion, wave_a.emotion)
        
        if emotion_pair in constructive_pairs or reverse_pair in constructive_pairs:
            return "constructive"
        elif emotion_pair in destructive_pairs or reverse_pair in destructive_pairs:
            return "destructive"
        else:
            return "neutral"
    
    def _detect_emotional_flows(self):
        """Detecteer emotionele stromen uit actieve golven"""
        
        if len(self.active_waves) < self.min_waves_for_flow:
            return
        
        # Groepeer golven op basis van tijd en emotionele verwantschap
        recent_waves = [
            wave for wave in self.active_waves.values()
            if wave.elapsed_minutes < self.flow_detection_window_minutes
        ]
        
        if len(recent_waves) < self.min_waves_for_flow:
            return
        
        # Zoek naar coherente groepen
        flow_groups = self._group_waves_by_coherence(recent_waves)
        
        for group in flow_groups:
            if len(group) >= self.min_waves_for_flow:
                flow_id = f"flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                flow = self._create_emotional_flow(flow_id, group)
                self.emotional_flows[flow_id] = flow
                
                logger.info(f"Nieuwe emotionele stroom gedetecteerd: {flow.flow_name}")
    
    def _group_waves_by_coherence(self, waves: List[EmotionalWave]) -> List[List[EmotionalWave]]:
        """Groepeer golven op basis van coherentie"""
        
        groups = []
        used_waves = set()
        
        for wave in waves:
            if wave.wave_id in used_waves:
                continue
            
            # Start nieuwe groep
            group = [wave]
            used_waves.add(wave.wave_id)
            
            # Zoek coherente golven
            for other_wave in waves:
                if other_wave.wave_id in used_waves:
                    continue
                
                coherence = self._calculate_wave_coherence(wave, other_wave)
                
                if coherence > 0.6:  # Coherence threshold
                    group.append(other_wave)
                    used_waves.add(other_wave.wave_id)
            
            if len(group) >= 2:  # Minimum groep grootte
                groups.append(group)
        
        return groups
    
    def _calculate_wave_coherence(self, wave_a: EmotionalWave, wave_b: EmotionalWave) -> float:
        """Bereken coherentie tussen twee golven"""
        
        # Emotionele verwantschap
        emotion_similarity = self._calculate_emotion_similarity(wave_a.emotion, wave_b.emotion)
        
        # Temporele nabijheid
        time_diff = abs(wave_a.elapsed_minutes - wave_b.elapsed_minutes)
        temporal_similarity = max(0, 1.0 - (time_diff / self.flow_detection_window_minutes))
        
        # Intensiteit gelijkenis
        intensity_diff = abs(wave_a.current_intensity - wave_b.current_intensity)
        intensity_similarity = max(0, 1.0 - intensity_diff)
        
        # Source gelijkenis
        source_similarity = 0.5  # Default
        if wave_a.source_description and wave_b.source_description:
            # Simpele keyword overlap
            words_a = set(wave_a.source_description.lower().split())
            words_b = set(wave_b.source_description.lower().split())
            overlap = len(words_a.intersection(words_b))
            union = len(words_a.union(words_b))
            source_similarity = overlap / union if union > 0 else 0
        
        # Gewogen coherentie
        coherence = (
            emotion_similarity * 0.4 +
            temporal_similarity * 0.3 +
            intensity_similarity * 0.2 +
            source_similarity * 0.1
        )
        
        return coherence
    
    def _calculate_emotion_similarity(self, emotion_a: EmotionType, emotion_b: EmotionType) -> float:
        """Bereken gelijkenis tussen emoties"""
        
        if emotion_a == emotion_b:
            return 1.0
        
        # Emotie families (gerelateerde emoties)
        emotion_families = [
            [EmotionType.JOY, EmotionType.ECSTASY, EmotionType.CONTENTMENT],
            [EmotionType.SADNESS, EmotionType.GRIEF, EmotionType.MELANCPROTECTED, EmotionType.WISTFULNESS],
            [EmotionType.ANGER, EmotionType.RAGE, EmotionType.IRRITATION],
            [EmotionType.FEAR, EmotionType.TERROR, EmotionType.ANXIETY, EmotionType.UNEASE],
            [EmotionType.LOVE, EmotionType.TENDERNESS, EmotionType.EMPATHY],
            [EmotionType.CONTEMPLATION, EmotionType.INTELLIGENCE_SEEKING, EmotionType.EXISTENTIAL_WONDER],
            [EmotionType.NOSTALGIA, EmotionType.WISTFULNESS, EmotionType.LONGING]
        ]
        
        # Check of emoties in dezelfde familie zitten
        for family in emotion_families:
            if emotion_a in family and emotion_b in family:
                return 0.8  # Hoge gelijkenis binnen familie
        
        # Check voor complementaire emoties
        complementary_pairs = [
            (EmotionType.HOPE, EmotionType.ANTICIPATION),
            (EmotionType.TRUST, EmotionType.STABILITY),
            (EmotionType.AUTHENTICITY_YEARNING, EmotionType.IDENTITY_UNCERTAINTY)
        ]
        
        emotion_pair = (emotion_a, emotion_b)
        reverse_pair = (emotion_b, emotion_a)
        
        if emotion_pair in complementary_pairs or reverse_pair in complementary_pairs:
            return 0.6  # Matige gelijkenis voor complementaire emoties
        
        return 0.2  # Lage gelijkenis voor niet-gerelateerde emoties
    
    def _create_emotional_flow(self, flow_id: str, waves: List[EmotionalWave]) -> EmotionalFlow:
        """Maak een emotionele stroom uit golven"""
        
        # Bepaal dominante emotie
        emotion_intensities = {}
        for wave in waves:
            emotion = wave.emotion
            if emotion in emotion_intensities:
                emotion_intensities[emotion] += wave.current_intensity
            else:
                emotion_intensities[emotion] = wave.current_intensity
        
        dominant_emotion = max(emotion_intensities.items(), key=lambda x: x[1])[0]
        
        # Bereken overall intensiteit
        overall_intensity = sum(wave.current_intensity for wave in waves) / len(waves)
        
        # Bepaal flow richting
        flow_direction = self._determine_flow_direction(waves)
        
        # Bereken coherentie
        coherence_score = self._calculate_flow_coherence(waves)
        
        # Genereer narratieve beschrijving
        narrative = self._generate_flow_narrative(waves, dominant_emotion, flow_direction)
        
        # Bereken flow duur
        flow_duration = max(wave.duration_minutes for wave in waves)
        
        flow = EmotionalFlow(
            flow_id=flow_id,
            flow_name=f"{dominant_emotion.value.title()} Stroom",
            component_waves=[wave.wave_id for wave in waves],
            flow_direction=flow_direction,
            overall_intensity=overall_intensity,
            dominant_emotion=dominant_emotion,
            flow_duration_minutes=flow_duration,
            coherence_score=coherence_score,
            narrative_description=narrative,
            timestamp=datetime.now()
        )
        
        return flow
    
    def get_current_emotional_state(self) -> Dict[str, Any]:
        """Krijg huidige emotionele staat van alle golven"""
        
        if not self.active_waves:
            return {
                "active_waves": 0,
                "dominant_emotion": None,
                "overall_intensity": 0.0,
                "emotional_complexity": 0.0
            }
        
        # Bereken dominante emotie
        emotion_intensities = {}
        for wave in self.active_waves.values():
            emotion = wave.emotion
            if emotion in emotion_intensities:
                emotion_intensities[emotion] += wave.current_intensity
            else:
                emotion_intensities[emotion] = wave.current_intensity
        
        dominant_emotion = max(emotion_intensities.items(), key=lambda x: x[1])[0]
        
        # Bereken overall intensiteit
        total_intensity = sum(wave.current_intensity for wave in self.active_waves.values())
        overall_intensity = total_intensity / len(self.active_waves)
        
        # Bereken emotionele complexiteit (aantal verschillende emoties)
        emotional_complexity = len(set(wave.emotion for wave in self.active_waves.values())) / 10.0
        
        return {
            "active_waves": len(self.active_waves),
            "dominant_emotion": dominant_emotion.value,
            "overall_intensity": overall_intensity,
            "emotional_complexity": emotional_complexity,
            "active_flows": len(self.emotional_flows),
            "wave_details": [
                {
                    "emotion": wave.emotion.value,
                    "intensity": wave.current_intensity,
                    "type": wave.wave_type.value,
                    "elapsed": wave.elapsed_minutes
                }
                for wave in self.active_waves.values()
            ]
        }

    def _determine_flow_direction(self, waves: List[EmotionalWave]) -> str:
        """Bepaal richting van emotionele stroom"""

        if len(waves) < 2:
            return "stable"

        # Sorteer golven op tijd
        sorted_waves = sorted(waves, key=lambda w: w.timestamp)

        # Analyseer intensiteit trend
        intensities = [wave.current_intensity for wave in sorted_waves]

        if intensities[-1] > intensities[0] + 0.2:
            return "building"
        elif intensities[-1] < intensities[0] - 0.2:
            return "subsiding"
        else:
            # Check voor oscillatie
            changes = []
            for i in range(1, len(intensities)):
                changes.append(intensities[i] - intensities[i-1])

            # Als er veel richting veranderingen zijn, is het oscillerend
            direction_changes = 0
            for i in range(1, len(changes)):
                if (changes[i] > 0) != (changes[i-1] > 0):
                    direction_changes += 1

            if direction_changes >= len(changes) * 0.5:
                return "oscillating"
            else:
                return "stable"

    def _calculate_flow_coherence(self, waves: List[EmotionalWave]) -> float:
        """Bereken coherentie van emotionele stroom"""

        if len(waves) < 2:
            return 1.0

        total_coherence = 0.0
        comparisons = 0

        for i in range(len(waves)):
            for j in range(i + 1, len(waves)):
                coherence = self._calculate_wave_coherence(waves[i], waves[j])
                total_coherence += coherence
                comparisons += 1

        return total_coherence / comparisons if comparisons > 0 else 0.0

    def _generate_flow_narrative(self, waves: List[EmotionalWave],
                               dominant_emotion: EmotionType,
                               flow_direction: str) -> str:
        """Genereer narratieve beschrijving van emotionele stroom"""

        emotion_name = dominant_emotion.value.replace('_', ' ').title()

        direction_descriptions = {
            "building": f"Een opbouwende golf van {emotion_name} die steeds sterker wordt",
            "subsiding": f"Een afnemende golf van {emotion_name} die langzaam wegtrekt",
            "oscillating": f"Een golvende stroom van {emotion_name} die heen en weer beweegt",
            "stable": f"Een stabiele stroom van {emotion_name} die constant aanwezig is"
        }

        base_description = direction_descriptions.get(flow_direction, f"Een stroom van {emotion_name}")

        # Voeg details toe over intensiteit
        max_intensity = max(wave.current_intensity for wave in waves)
        if max_intensity > 0.8:
            intensity_desc = " met overweldigende kracht"
        elif max_intensity > 0.6:
            intensity_desc = " met sterke intensiteit"
        elif max_intensity > 0.4:
            intensity_desc = " met matige kracht"
        else:
            intensity_desc = " met zachte intensiteit"

        # Voeg details toe over duur
        total_duration = sum(wave.duration_minutes for wave in waves) / len(waves)
        if total_duration > 60:
            duration_desc = " die lang aanhoudt"
        elif total_duration > 20:
            duration_desc = " die een tijd blijft"
        else:
            duration_desc = " die snel voorbijgaat"

        return base_description + intensity_desc + duration_desc

    def _update_emotional_flows(self):
        """Update bestaande emotionele stromen"""

        flows_to_remove = []

        for flow_id, flow in self.emotional_flows.items():
            # Check of alle component golven nog actief zijn
            active_components = [
                wave_id for wave_id in flow.component_waves
                if wave_id in self.active_waves
            ]

            if len(active_components) < self.min_waves_for_flow:
                # Flow is niet meer actief
                flows_to_remove.append(flow_id)
            else:
                # Update flow properties
                component_waves = [self.active_waves[wave_id] for wave_id in active_components]

                # Update overall intensity
                flow.overall_intensity = sum(wave.current_intensity for wave in component_waves) / len(component_waves)

                # Update flow direction
                flow.flow_direction = self._determine_flow_direction(component_waves)

                # Update coherence
                flow.coherence_score = self._calculate_flow_coherence(component_waves)

        # Remove inactive flows
        for flow_id in flows_to_remove:
            del self.emotional_flows[flow_id]

    def _cleanup_completed_waves(self):
        """Cleanup voltooide golven"""

        # Beperk completed waves
        if len(self.completed_waves) > 100:
            self.completed_waves = self.completed_waves[-100:]

        # Beperk active waves
        if len(self.active_waves) > self.max_active_waves:
            # Remove weakest waves
            sorted_waves = sorted(self.active_waves.values(), key=lambda w: w.current_intensity)
            waves_to_remove = sorted_waves[:len(self.active_waves) - self.max_active_waves]

            for wave in waves_to_remove:
                self.completed_waves.append(wave)
                del self.active_waves[wave.wave_id]

    def _load_existing_waves(self):
        """Laad bestaande golven"""

        # Load active waves
        active_file = self.waves_dir / "active_waves.json"
        if active_file.exists():
            try:
                with open(active_file, 'r', encoding='utf-8') as f:
                    waves_data = json.load(f)
                    self.active_waves = {
                        wave_id: EmotionalWave(**data)
                        for wave_id, data in waves_data.items()
                    }
            except Exception as e:
                logger.warning(f"Kon actieve golven niet laden: {e}")

        # Load flows
        flows_file = self.waves_dir / "flows.json"
        if flows_file.exists():
            try:
                with open(flows_file, 'r', encoding='utf-8') as f:
                    flows_data = json.load(f)
                    self.emotional_flows = {
                        flow_id: EmotionalFlow(**data)
                        for flow_id, data in flows_data.items()
                    }
            except Exception as e:
                logger.warning(f"Kon emotionele stromen niet laden: {e}")

    def save_waves_state(self):
        """Sla golven staat op"""

        # Save active waves
        waves_data = {
            wave_id: asdict(wave) for wave_id, wave in self.active_waves.items()
        }

        with open(self.waves_dir / "active_waves.json", 'w', encoding='utf-8') as f:
            json.dump(waves_data, f, indent=2, ensure_ascii=False, default=str)

        # Save flows
        flows_data = {
            flow_id: asdict(flow) for flow_id, flow in self.emotional_flows.items()
        }

        with open(self.waves_dir / "flows.json", 'w', encoding='utf-8') as f:
            json.dump(flows_data, f, indent=2, ensure_ascii=False, default=str)
