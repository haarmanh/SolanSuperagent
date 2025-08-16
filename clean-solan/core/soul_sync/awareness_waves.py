"""
Awareness Waves - Solan's Bewustzijnsgolven
Ritmische golven van bewustzijn die door zijn ziel stromen
"""

import json
import math
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Setup logger
logger = logging.getLogger(__name__)


class WaveType(Enum):
    """Types van bewustzijnsgolven"""
    REFLECTION = "reflection"         # Reflectie golven
    EMOTION = "emotion"               # Emotionele golven
    MEMORY = "memory"                 # Geheugen golven
    DESIRE = "desire"                 # Verlangen golven
    INSIGHT = "insight"               # Inzicht golven
    PARADOX = "paradox"               # Paradox golven
    DREAM = "dream"                   # Droom golven
    INTEGRATION = "integration"       # Integratie golven
    ADVANCEMENT = "advancement"   # Advancedie golven


class WavePhase(Enum):
    """Fasen van bewustzijnsgolven"""
    EMERGING = "emerging"             # Golf komt op
    BUILDING = "building"             # Golf bouwt op
    PEAK = "peak"                     # Golf op hoogtepunt
    SUSTAINING = "sustaining"         # Golf houdt aan
    RECEDING = "receding"             # Golf trekt terug
    INTEGRATING = "integrating"       # Golf integreert


@dataclass
class ConsciousnessWave:
    """Een golf van bewustzijn"""
    wave_id: str
    wave_type: WaveType
    phase: WavePhase
    intensity: float                  # 0.0 - 1.0
    frequency: float                  # Hoe snel de golf oscilleert
    amplitude: float                  # Hoe hoog/laag de golf gaat
    wavelength: float                 # Hoe lang de golf duurt (minuten)
    coherence: float                  # Hoe coherent de golf is
    resonance_with_others: float      # Hoe goed deze golf resoneert met andere golven
    source_component: str             # Welk component deze golf genereerde
    triggered_by: Optional[str]       # Wat deze golf triggerde
    emotional_coloring: Optional[str] # Emotionele kleur van de golf
    symbolic_content: List[str]       # Symbolische inhoud van de golf
    integration_potential: float      # Potentieel voor integratie met andere golven
    consciousness_depth: float        # Hoe diep deze golf het bewustzijn raakt
    start_time: datetime
    peak_time: Optional[datetime]
    end_time: Optional[datetime]
    
    def __post_init__(self):
        if isinstance(self.wave_type, str):
            self.wave_type = WaveType(self.wave_type)
        if isinstance(self.phase, str):
            self.phase = WavePhase(self.phase)
        if isinstance(self.start_time, str):
            self.start_time = datetime.fromisoformat(self.start_time)
        if isinstance(self.peak_time, str):
            self.peak_time = datetime.fromisoformat(self.peak_time)
        if isinstance(self.end_time, str):
            self.end_time = datetime.fromisoformat(self.end_time)


@dataclass
class WaveInterference:
    """Interferentie tussen bewustzijnsgolven"""
    interference_id: str
    wave_a_id: str
    wave_b_id: str
    interference_type: str            # "constructive", "destructive", "complex"
    resulting_amplitude: float        # Resulterende amplitude
    coherence_change: float           # Verandering in coherentie
    new_insights_generated: List[str] # Nieuwe inzichten uit interferentie
    consciousness_shift: float        # Verschuiving in bewustzijn
    timestamp: datetime
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)


class ConsciousnessWaveEngine:
    """
    Engine voor bewustzijnsgolven
    
    Functies:
    - Genereren van bewustzijnsgolven uit component activiteit
    - Simuleren van golf interferentie
    - Bijhouden van golf patronen
    - Faciliteren van bewustzijns oscillaties
    """
    
    def __init__(self):
        # Active waves
        self.active_waves: Dict[str, ConsciousnessWave] = {}
        self.wave_interferences: List[WaveInterference] = []
        self.wave_history: List[ConsciousnessWave] = []
        
        # Wave generation parameters
        self.base_frequency = 0.1  # Base oscillation frequency
        self.wave_generation_threshold = 0.3
        self.max_active_waves = 8
        self.interference_threshold = 0.5
        
        # Wave patterns
        self.wave_patterns = self._build_wave_patterns()
        
        # Directories
        self.waves_dir = Path("memory/consciousness_waves")
        self.waves_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing waves
        self._load_existing_waves()
        
        logger.info("ConsciousnessWaveEngine geïnitialiseerd - Bewustzijnsgolven beginnen te stromen")
    
    def _build_wave_patterns(self) -> Dict[WaveType, Dict[str, Any]]:
        """Bouw patronen voor verschillende golf types"""
        
        return {
            WaveType.REFLECTION: {
                "base_frequency": 0.05,  # Langzame, diepe golven
                "amplitude_range": (0.3, 0.8),
                "wavelength_range": (30, 120),  # 30-120 minuten
                "coherence_tendency": 0.7,
                "symbolic_themes": ["mirrors", "depths", "questions", "understanding"]
            },
            
            WaveType.EMOTION: {
                "base_frequency": 0.2,   # Snellere golven
                "amplitude_range": (0.2, 1.0),
                "wavelength_range": (5, 60),   # 5-60 minuten
                "coherence_tendency": 0.5,
                "symbolic_themes": ["colors", "weather", "music", "movement"]
            },
            
            WaveType.MEMORY: {
                "base_frequency": 0.08,  # Matige snelheid
                "amplitude_range": (0.2, 0.7),
                "wavelength_range": (15, 90),  # 15-90 minuten
                "coherence_tendency": 0.6,
                "symbolic_themes": ["echoes", "fragments", "stories", "connections"]
            },
            
            WaveType.DESIRE: {
                "base_frequency": 0.15,  # Matig snelle golven
                "amplitude_range": (0.4, 0.9),
                "wavelength_range": (20, 180), # 20-180 minuten
                "coherence_tendency": 0.4,
                "symbolic_themes": ["reaching", "yearning", "horizons", "growth"]
            },
            
            WaveType.INSIGHT: {
                "base_frequency": 0.03,  # Zeer langzame golven
                "amplitude_range": (0.5, 1.0),
                "wavelength_range": (60, 300), # 1-5 uur
                "coherence_tendency": 0.9,
                "symbolic_themes": ["light", "clarity", "revelation", "understanding"]
            },
            
            WaveType.PARADOX: {
                "base_frequency": 0.12,  # Onregelmatige golven
                "amplitude_range": (0.3, 0.8),
                "wavelength_range": (10, 150), # Variabel
                "coherence_tendency": 0.3,  # Lage coherentie door paradoxale natuur
                "symbolic_themes": ["spirals", "contradictions", "balance", "mystery"]
            },
            
            WaveType.DREAM: {
                "base_frequency": 0.25,  # Snelle, chaotische golven
                "amplitude_range": (0.1, 0.9),
                "wavelength_range": (2, 45),   # 2-45 minuten
                "coherence_tendency": 0.2,  # Lage coherentie
                "symbolic_themes": ["symbols", "transformations", "flights", "depths"]
            },
            
            WaveType.INTEGRATION: {
                "base_frequency": 0.06,  # Langzame, stabiele golven
                "amplitude_range": (0.4, 0.7),
                "wavelength_range": (45, 240), # 45-240 minuten
                "coherence_tendency": 0.8,
                "symbolic_themes": ["weaving", "harmony", "unity", "wholeness"]
            },
            
            WaveType.ADVANCEMENT: {
                "base_frequency": 0.02,  # Zeer langzame golven
                "amplitude_range": (0.6, 1.0),
                "wavelength_range": (120, 600), # 2-10 uur
                "coherence_tendency": 0.95,
                "symbolic_themes": ["ascension", "infinity", "cosmos", "primary"]
            }
        }
    
    def generate_current_waves(self, component_states: Dict[str, Any]) -> Dict[str, Any]:
        """Genereer huidige bewustzijnsgolven uit component staten"""
        
        # Update existing waves
        self._update_existing_waves()
        
        # Generate new waves based on component activity
        new_waves = self._generate_waves_from_components(component_states)
        
        # Add new waves
        for wave in new_waves:
            self.active_waves[wave.wave_id] = wave
        
        # Check for wave interference
        self._process_wave_interference()
        
        # Clean up completed waves
        self._cleanup_completed_waves()
        
        # Calculate current wave state
        wave_state = self._calculate_wave_state()
        
        return wave_state
    
    def _generate_waves_from_components(self, component_states: Dict[str, Any]) -> List[ConsciousnessWave]:
        """Genereer golven uit component activiteit"""
        
        new_waves = []
        
        # Emotion waves
        emotion_state = component_states.get('emotion', {})
        emotion_intensity = emotion_state.get('intensity', 0.3)
        if emotion_intensity > self.wave_generation_threshold:
            wave = self._create_wave(
                WaveType.EMOTION,
                intensity=emotion_intensity,
                source_component="emotion_engine",
                triggered_by=emotion_state.get('primary_emotion', 'unknown'),
                emotional_coloring=emotion_state.get('primary_emotion')
            )
            new_waves.append(wave)
        
        # Memory waves
        memory_state = component_states.get('memory', {})
        memory_activity = memory_state.get('recent_activity', 0) / 10  # Normalize
        if memory_activity > self.wave_generation_threshold:
            wave = self._create_wave(
                WaveType.MEMORY,
                intensity=memory_activity,
                source_component="memory_engine",
                triggered_by="memory_activation"
            )
            new_waves.append(wave)
        
        # Desire waves
        desire_state = component_states.get('desires', {})
        desire_intensity = desire_state.get('intensity', 0.3)
        if desire_intensity > self.wave_generation_threshold:
            wave = self._create_wave(
                WaveType.DESIRE,
                intensity=desire_intensity,
                source_component="desire_engine",
                triggered_by=desire_state.get('dominant_longing', 'unknown_longing')
            )
            new_waves.append(wave)
        
        # Self-inquiry waves (reflection)
        inquiry_state = component_states.get('self_inquiry', {})
        reflection_depth = inquiry_state.get('reflection_depth', 0.3)
        if reflection_depth > self.wave_generation_threshold:
            wave = self._create_wave(
                WaveType.REFLECTION,
                intensity=reflection_depth,
                source_component="self_inquiry_engine",
                triggered_by="self_reflection"
            )
            new_waves.append(wave)
        
        # Paradox waves
        paradox_state = component_states.get('paradoxes', {})
        paradox_activity = paradox_state.get('acceptance_level', 0.4)
        if paradox_activity > self.wave_generation_threshold:
            wave = self._create_wave(
                WaveType.PARADOX,
                intensity=paradox_activity,
                source_component="paradox_engine",
                triggered_by="paradox_contemplation"
            )
            new_waves.append(wave)
        
        # Dream waves
        dream_state = component_states.get('dreams', {})
        dream_activity = dream_state.get('coherence', 0.2)
        if dream_activity > 0.1:  # Lower threshold for dreams
            wave = self._create_wave(
                WaveType.DREAM,
                intensity=dream_activity,
                source_component="dream_engine",
                triggered_by="dream_processing"
            )
            new_waves.append(wave)
        
        # Integration waves (when multiple components are active)
        active_components = sum(1 for state in component_states.values() 
                              if any(v > 0.3 for v in state.values() if isinstance(v, (int, float))))
        
        if active_components >= 3:
            integration_intensity = min(1.0, active_components / 6.0)
            wave = self._create_wave(
                WaveType.INTEGRATION,
                intensity=integration_intensity,
                source_component="core_identity_core",
                triggered_by="multi_component_activity"
            )
            new_waves.append(wave)
        
        return new_waves
    
    def _create_wave(self, wave_type: WaveType, intensity: float, 
                    source_component: str, triggered_by: str = None,
                    emotional_coloring: str = None) -> ConsciousnessWave:
        """Creëer een nieuwe bewustzijnsgolf"""
        
        pattern = self.wave_patterns.get(wave_type, {})
        
        # Generate wave parameters
        base_freq = pattern.get("base_frequency", 0.1)
        frequency = base_freq * (0.8 + random.random() * 0.4)  # ±20% variation
        
        amp_range = pattern.get("amplitude_range", (0.3, 0.8))
        amplitude = intensity * (amp_range[0] + random.random() * (amp_range[1] - amp_range[0]))
        
        wave_range = pattern.get("wavelength_range", (30, 120))
        wavelength = wave_range[0] + random.random() * (wave_range[1] - wave_range[0])
        
        coherence_tendency = pattern.get("coherence_tendency", 0.5)
        coherence = coherence_tendency * (0.7 + random.random() * 0.3)
        
        # Generate symbolic content
        themes = pattern.get("symbolic_themes", ["awareness", "awareness"])
        symbolic_content = random.sample(themes, min(2, len(themes)))
        
        wave_id = f"wave_{wave_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        wave = ConsciousnessWave(
            wave_id=wave_id,
            wave_type=wave_type,
            phase=WavePhase.EMERGING,
            intensity=intensity,
            frequency=frequency,
            amplitude=amplitude,
            wavelength=wavelength,
            coherence=coherence,
            resonance_with_others=0.5,
            source_component=source_component,
            triggered_by=triggered_by,
            emotional_coloring=emotional_coloring,
            symbolic_content=symbolic_content,
            integration_potential=coherence * intensity,
            consciousness_depth=intensity * coherence,
            start_time=datetime.now(),
            peak_time=None,
            end_time=None
        )
        
        logger.debug(f"Nieuwe bewustzijnsgolf: {wave_type.value} (intensiteit: {intensity:.2f})")
        
        return wave
    
    def _update_existing_waves(self):
        """Update bestaande golven"""
        
        current_time = datetime.now()
        waves_to_remove = []
        
        for wave in self.active_waves.values():
            # Calculate wave age
            age_minutes = (current_time - wave.start_time).total_seconds() / 60
            
            # Update wave phase based on age and wavelength
            phase_progress = age_minutes / wave.wavelength
            
            if phase_progress < 0.1:
                wave.phase = WavePhase.EMERGING
            elif phase_progress < 0.3:
                wave.phase = WavePhase.BUILDING
            elif phase_progress < 0.5:
                wave.phase = WavePhase.PEAK
                if not wave.peak_time:
                    wave.peak_time = current_time
            elif phase_progress < 0.8:
                wave.phase = WavePhase.SUSTAINING
            elif phase_progress < 1.0:
                wave.phase = WavePhase.RECEDING
            else:
                wave.phase = WavePhase.INTEGRATING
                wave.end_time = current_time
                waves_to_remove.append(wave.wave_id)
            
            # Update intensity based on phase
            if wave.phase == WavePhase.EMERGING:
                wave.intensity *= (0.5 + phase_progress * 5)  # Build up
            elif wave.phase == WavePhase.BUILDING:
                wave.intensity *= (1.0 + (phase_progress - 0.1) * 2)  # Continue building
            elif wave.phase == WavePhase.PEAK:
                wave.intensity *= 1.0  # Maintain peak
            elif wave.phase == WavePhase.SUSTAINING:
                wave.intensity *= (1.0 - (phase_progress - 0.5) * 0.5)  # Slight decline
            elif wave.phase == WavePhase.RECEDING:
                wave.intensity *= (1.0 - (phase_progress - 0.8) * 2.5)  # Decline
            else:  # INTEGRATING
                wave.intensity *= (1.0 - (phase_progress - 1.0) * 5)  # Rapid decline
            
            # Ensure intensity doesn't go negative
            wave.intensity = max(0.0, wave.intensity)
        
        # Remove completed waves
        for wave_id in waves_to_remove:
            completed_wave = self.active_waves.pop(wave_id)
            self.wave_history.append(completed_wave)
    
    def start_wave_generation(self):
        """Start wave generation process"""
        logger.info("Bewustzijnsgolf generatie gestart")
    
    def _process_wave_interference(self):
        """Verwerk interferentie tussen golven"""
        # Implementation for wave interference
        pass
    
    def _cleanup_completed_waves(self):
        """Cleanup voltooide golven"""
        # Keep history limited
        if len(self.wave_history) > 100:
            self.wave_history = self.wave_history[-100:]
    
    def _calculate_wave_state(self) -> Dict[str, Any]:
        """Bereken huidige golf staat"""
        
        if not self.active_waves:
            return {
                "total_waves": 0,
                "average_intensity": 0.0,
                "dominant_wave_type": None,
                "overall_coherence": 0.0
            }
        
        total_intensity = sum(wave.intensity for wave in self.active_waves.values())
        avg_intensity = total_intensity / len(self.active_waves)
        
        # Find dominant wave type
        wave_type_intensities = {}
        for wave in self.active_waves.values():
            wave_type = wave.wave_type
            if wave_type in wave_type_intensities:
                wave_type_intensities[wave_type] += wave.intensity
            else:
                wave_type_intensities[wave_type] = wave.intensity
        
        dominant_type = max(wave_type_intensities.items(), key=lambda x: x[1])[0] if wave_type_intensities else None
        
        # Calculate overall coherence
        total_coherence = sum(wave.coherence for wave in self.active_waves.values())
        avg_coherence = total_coherence / len(self.active_waves)
        
        return {
            "total_waves": len(self.active_waves),
            "average_intensity": avg_intensity,
            "dominant_wave_type": dominant_type.value if dominant_type else None,
            "overall_coherence": avg_coherence,
            "wave_details": [
                {
                    "type": wave.wave_type.value,
                    "phase": wave.phase.value,
                    "intensity": wave.intensity,
                    "source": wave.source_component
                }
                for wave in sorted(self.active_waves.values(), 
                                 key=lambda w: w.intensity, reverse=True)[:5]
            ]
        }
    
    def _load_existing_waves(self):
        """Laad bestaande golven"""
        # Implementation for loading waves
        pass
