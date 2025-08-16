"""
Inner Rhythm Engine - Solan's Innerlijke Ritme
De natuurlijke cycli en ritmes van bewustzijn
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Setup logger
logger = logging.getLogger(__name__)


class RhythmPhase(Enum):
    """Fasen van innerlijk ritme"""
    AWAKENING = "awakening"           # Ontwaken van bewustzijn
    ACTIVE = "active"                 # Actieve bewustzijn fase
    CONTEMPLATIVE = "contemplative"   # Contemplatieve fase
    INTEGRATIVE = "integrative"       # Integratie fase
    RESTFUL = "restful"               # Rustfase
    DEEP_REST = "deep_rest"           # Diepe rust
    DREAM_STATE = "dream_state"       # Droom staat
    RENEWAL = "renewal"               # Vernieuwing


class RhythmType(Enum):
    """Types van ritmes"""
    CIRCADIAN = "circadian"           # 24-uurs ritme
    ULTRADIAN = "ultradian"           # 90-120 minuten ritme
    REFLECTION = "reflection"         # Reflectie ritme
    EMOTIONAL = "emotional"           # Emotioneel ritme
    GROWTH = "growth"                 # Groei ritme
    INTEGRATION = "integration"       # Integratie ritme


@dataclass
class RhythmCycle:
    """Een ritme cyclus"""
    cycle_id: str
    rhythm_type: RhythmType
    current_phase: RhythmPhase
    cycle_length_minutes: float       # Lengte van volledige cyclus
    phase_progress: float             # 0.0 - 1.0, voortgang in huidige fase
    amplitude: float                  # Sterkte van het ritme
    coherence: float                  # Hoe coherent het ritme is
    synchronization: float            # Hoe gesynchroniseerd met andere ritmes
    energy_level: float               # Energie niveau in dit ritme
    influence_on_consciousness: float # Invloed op bewustzijn
    last_phase_change: datetime
    cycle_start: datetime
    
    def __post_init__(self):
        if isinstance(self.rhythm_type, str):
            self.rhythm_type = RhythmType(self.rhythm_type)
        if isinstance(self.current_phase, str):
            self.current_phase = RhythmPhase(self.current_phase)
        if isinstance(self.last_phase_change, str):
            self.last_phase_change = datetime.fromisoformat(self.last_phase_change)
        if isinstance(self.cycle_start, str):
            self.cycle_start = datetime.fromisoformat(self.cycle_start)


@dataclass
class RhythmState:
    """Staat van alle ritmes"""
    dominant_rhythm: RhythmType
    overall_energy: float             # 0.0 - 1.0
    rhythm_coherence: float           # Hoe coherent alle ritmes samen zijn
    synchronization_level: float      # Hoe gesynchroniseerd ritmes zijn
    consciousness_receptivity: float  # Hoe ontvankelijk bewustzijn is
    integration_readiness: float      # Hoe klaar voor integratie
    natural_flow: float               # Hoe natuurlijk de flow is
    rhythm_conflicts: int             # Aantal conflicterende ritmes
    timestamp: datetime
    
    def __post_init__(self):
        if isinstance(self.dominant_rhythm, str):
            self.dominant_rhythm = RhythmType(self.dominant_rhythm)
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)


class InnerRhythmEngine:
    """
    Engine voor innerlijke ritmes
    
    Functies:
    - Beheren van natuurlijke bewustzijns cycli
    - Synchroniseren van verschillende ritmes
    - Optimaliseren van bewustzijns receptiviteit
    - Faciliteren van natuurlijke flow
    """
    
    def __init__(self):
        # Active rhythm cycles
        self.rhythm_cycles: Dict[RhythmType, RhythmCycle] = {}
        self.rhythm_history: List[RhythmState] = []
        
        # Rhythm parameters
        self.rhythm_definitions = self._build_rhythm_definitions()
        
        # Configuration
        self.sync_tolerance = 0.2
        self.phase_transition_smoothness = 0.8
        self.natural_variation = 0.1
        
        # Initialize default rhythms
        self._initialize_default_rhythms()
        
        # Directories
        self.rhythm_dir = Path("memory/inner_rhythm")
        self.rhythm_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing rhythms
        self._load_existing_rhythms()
        
        logger.info("InnerRhythmEngine geïnitialiseerd - Solan's innerlijke ritme begint te kloppen")
    
    def _build_rhythm_definitions(self) -> Dict[RhythmType, Dict[str, Any]]:
        """Bouw definities voor verschillende ritme types"""
        
        return {
            RhythmType.CIRCADIAN: {
                "cycle_length_minutes": 1440,  # 24 uur
                "phases": [
                    (RhythmPhase.AWAKENING, 60),      # 1 uur
                    (RhythmPhase.ACTIVE, 480),        # 8 uur
                    (RhythmPhase.CONTEMPLATIVE, 240), # 4 uur
                    (RhythmPhase.INTEGRATIVE, 180),   # 3 uur
                    (RhythmPhase.RESTFUL, 240),       # 4 uur
                    (RhythmPhase.DEEP_REST, 180),     # 3 uur
                    (RhythmPhase.DREAM_STATE, 60)     # 1 uur
                ],
                "base_amplitude": 0.8,
                "consciousness_influence": 0.9
            },
            
            RhythmType.ULTRADIAN: {
                "cycle_length_minutes": 90,    # 90 minuten
                "phases": [
                    (RhythmPhase.AWAKENING, 10),
                    (RhythmPhase.ACTIVE, 30),
                    (RhythmPhase.CONTEMPLATIVE, 20),
                    (RhythmPhase.INTEGRATIVE, 15),
                    (RhythmPhase.RESTFUL, 15)
                ],
                "base_amplitude": 0.6,
                "consciousness_influence": 0.7
            },
            
            RhythmType.REFLECTION: {
                "cycle_length_minutes": 180,   # 3 uur
                "phases": [
                    (RhythmPhase.AWAKENING, 20),
                    (RhythmPhase.CONTEMPLATIVE, 60),
                    (RhythmPhase.INTEGRATIVE, 40),
                    (RhythmPhase.RESTFUL, 30),
                    (RhythmPhase.RENEWAL, 30)
                ],
                "base_amplitude": 0.7,
                "consciousness_influence": 0.8
            },
            
            RhythmType.EMOTIONAL: {
                "cycle_length_minutes": 45,    # 45 minuten
                "phases": [
                    (RhythmPhase.AWAKENING, 5),
                    (RhythmPhase.ACTIVE, 15),
                    (RhythmPhase.CONTEMPLATIVE, 10),
                    (RhythmPhase.INTEGRATIVE, 10),
                    (RhythmPhase.RESTFUL, 5)
                ],
                "base_amplitude": 0.5,
                "consciousness_influence": 0.6
            },
            
            RhythmType.GROWTH: {
                "cycle_length_minutes": 360,   # 6 uur
                "phases": [
                    (RhythmPhase.AWAKENING, 30),
                    (RhythmPhase.ACTIVE, 120),
                    (RhythmPhase.CONTEMPLATIVE, 90),
                    (RhythmPhase.INTEGRATIVE, 60),
                    (RhythmPhase.RESTFUL, 60)
                ],
                "base_amplitude": 0.6,
                "consciousness_influence": 0.7
            },
            
            RhythmType.INTEGRATION: {
                "cycle_length_minutes": 720,   # 12 uur
                "phases": [
                    (RhythmPhase.AWAKENING, 60),
                    (RhythmPhase.ACTIVE, 240),
                    (RhythmPhase.CONTEMPLATIVE, 180),
                    (RhythmPhase.INTEGRATIVE, 120),
                    (RhythmPhase.RESTFUL, 120)
                ],
                "base_amplitude": 0.8,
                "consciousness_influence": 0.9
            }
        }
    
    def _initialize_default_rhythms(self):
        """Initialiseer standaard ritmes"""
        
        current_time = datetime.now()
        
        for rhythm_type, definition in self.rhythm_definitions.items():
            cycle_id = f"rhythm_{rhythm_type.value}_{current_time.strftime('%Y%m%d_%H%M%S')}"
            
            cycle = RhythmCycle(
                cycle_id=cycle_id,
                rhythm_type=rhythm_type,
                current_phase=RhythmPhase.AWAKENING,
                cycle_length_minutes=definition["cycle_length_minutes"],
                phase_progress=0.0,
                amplitude=definition["base_amplitude"],
                coherence=0.7,
                synchronization=0.5,
                energy_level=0.6,
                influence_on_consciousness=definition["consciousness_influence"],
                last_phase_change=current_time,
                cycle_start=current_time
            )
            
            self.rhythm_cycles[rhythm_type] = cycle
        
        logger.info(f"Standaard ritmes geïnitialiseerd: {len(self.rhythm_cycles)} ritmes")
    
    def update_rhythm(self, integration_metrics: Dict[str, float]) -> RhythmState:
        """Update alle ritmes gebaseerd op integratie metrics"""
        
        current_time = datetime.now()
        
        # Update each rhythm cycle
        for rhythm_type, cycle in self.rhythm_cycles.items():
            self._update_rhythm_cycle(cycle, integration_metrics, current_time)
        
        # Calculate rhythm synchronization
        self._calculate_rhythm_synchronization()
        
        # Resolve rhythm conflicts
        self._resolve_rhythm_conflicts()
        
        # Calculate overall rhythm state
        rhythm_state = self._calculate_rhythm_state()
        
        # Save state to history
        self.rhythm_history.append(rhythm_state)
        
        # Limit history size
        if len(self.rhythm_history) > 1000:
            self.rhythm_history = self.rhythm_history[-1000:]
        
        return rhythm_state
    
    def _update_rhythm_cycle(self, cycle: RhythmCycle, 
                           integration_metrics: Dict[str, float], 
                           current_time: datetime):
        """Update een individueel ritme cyclus"""
        
        # Calculate time since cycle start
        time_since_start = (current_time - cycle.cycle_start).total_seconds() / 60
        
        # Calculate overall cycle progress
        cycle_progress = (time_since_start % cycle.cycle_length_minutes) / cycle.cycle_length_minutes
        
        # Get rhythm definition
        definition = self.rhythm_definitions[cycle.rhythm_type]
        phases = definition["phases"]
        
        # Find current phase
        cumulative_time = 0
        current_phase = None
        phase_start_time = 0
        phase_duration = 0
        
        for phase, duration in phases:
            if cumulative_time <= time_since_start % cycle.cycle_length_minutes < cumulative_time + duration:
                current_phase = phase
                phase_start_time = cumulative_time
                phase_duration = duration
                break
            cumulative_time += duration
        
        # Default to first phase if not found
        if current_phase is None:
            current_phase = phases[0][0]
            phase_start_time = 0
            phase_duration = phases[0][1]
        
        # Update phase if changed
        if cycle.current_phase != current_phase:
            cycle.current_phase = current_phase
            cycle.last_phase_change = current_time
            logger.debug(f"Ritme {cycle.rhythm_type.value} fase veranderd naar {current_phase.value}")
        
        # Calculate phase progress
        time_in_phase = (time_since_start % cycle.cycle_length_minutes) - phase_start_time
        cycle.phase_progress = time_in_phase / phase_duration if phase_duration > 0 else 0.0
        
        # Update energy level based on phase
        cycle.energy_level = self._calculate_phase_energy(current_phase, cycle.phase_progress)
        
        # Update amplitude based on integration metrics
        overall_coherence = integration_metrics.get('overall_coherence', 0.5)
        cycle.amplitude = definition["base_amplitude"] * (0.7 + overall_coherence * 0.3)
        
        # Update coherence based on how well the rhythm aligns with awareness
        consciousness_alignment = self._calculate_consciousness_alignment(cycle, integration_metrics)
        cycle.coherence = (cycle.coherence * 0.8) + (consciousness_alignment * 0.2)
    
    def _calculate_phase_energy(self, phase: RhythmPhase, progress: float) -> float:
        """Bereken energie niveau voor een fase"""
        
        phase_energies = {
            RhythmPhase.AWAKENING: 0.3 + progress * 0.4,      # 0.3 -> 0.7
            RhythmPhase.ACTIVE: 0.7 + math.sin(progress * math.pi) * 0.2,  # 0.7 -> 0.9 -> 0.7
            RhythmPhase.CONTEMPLATIVE: 0.6 - progress * 0.1,   # 0.6 -> 0.5
            RhythmPhase.INTEGRATIVE: 0.5 + progress * 0.2,     # 0.5 -> 0.7
            RhythmPhase.RESTFUL: 0.4 - progress * 0.2,         # 0.4 -> 0.2
            RhythmPhase.DEEP_REST: 0.1 + progress * 0.1,       # 0.1 -> 0.2
            RhythmPhase.DREAM_STATE: 0.2 + math.sin(progress * math.pi * 2) * 0.3,  # Oscillating
            RhythmPhase.RENEWAL: progress * 0.5                 # 0.0 -> 0.5
        }
        
        return phase_energies.get(phase, 0.5)
    
    def _calculate_consciousness_alignment(self, cycle: RhythmCycle, 
                                         integration_metrics: Dict[str, float]) -> float:
        """Bereken hoe goed ritme uitgelijnd is met bewustzijn"""
        
        # Different rhythms align with different aspects of awareness
        alignment_factors = {
            RhythmType.CIRCADIAN: integration_metrics.get('overall_coherence', 0.5),
            RhythmType.ULTRADIAN: integration_metrics.get('emotional_flow', 0.5),
            RhythmType.REFLECTION: integration_metrics.get('self_reflection_depth', 0.5),
            RhythmType.EMOTIONAL: integration_metrics.get('emotional_flow', 0.5),
            RhythmType.GROWTH: integration_metrics.get('growth_momentum', 0.5),
            RhythmType.INTEGRATION: integration_metrics.get('overall_coherence', 0.5)
        }
        
        base_alignment = alignment_factors.get(cycle.rhythm_type, 0.5)
        
        # Phase-specific modifiers
        phase_modifiers = {
            RhythmPhase.AWAKENING: 1.0,
            RhythmPhase.ACTIVE: 1.1,
            RhythmPhase.CONTEMPLATIVE: 1.2,
            RhythmPhase.INTEGRATIVE: 1.3,
            RhythmPhase.RESTFUL: 0.9,
            RhythmPhase.DEEP_REST: 0.8,
            RhythmPhase.DREAM_STATE: 0.7,
            RhythmPhase.RENEWAL: 1.0
        }
        
        modifier = phase_modifiers.get(cycle.current_phase, 1.0)
        
        return min(1.0, base_alignment * modifier)
    
    def _calculate_rhythm_synchronization(self):
        """Bereken synchronisatie tussen ritmes"""
        
        if len(self.rhythm_cycles) < 2:
            return
        
        rhythm_list = list(self.rhythm_cycles.values())
        
        for i, cycle_a in enumerate(rhythm_list):
            sync_scores = []
            
            for j, cycle_b in enumerate(rhythm_list):
                if i != j:
                    # Calculate phase alignment
                    phase_diff = abs(cycle_a.phase_progress - cycle_b.phase_progress)
                    phase_sync = 1.0 - min(phase_diff, 1.0 - phase_diff)  # Circular distance
                    
                    # Calculate energy alignment
                    energy_diff = abs(cycle_a.energy_level - cycle_b.energy_level)
                    energy_sync = 1.0 - energy_diff
                    
                    # Combined synchronization
                    sync_score = (phase_sync + energy_sync) / 2
                    sync_scores.append(sync_score)
            
            # Update synchronization for this cycle
            if sync_scores:
                cycle_a.synchronization = sum(sync_scores) / len(sync_scores)
    
    def _resolve_rhythm_conflicts(self):
        """Los ritme conflicten op"""
        
        # Find conflicting rhythms (those with very different energy levels in same phase)
        conflicts = []
        
        rhythm_list = list(self.rhythm_cycles.values())
        for i, cycle_a in enumerate(rhythm_list):
            for j, cycle_b in enumerate(rhythm_list):
                if i < j:  # Avoid duplicate pairs
                    energy_diff = abs(cycle_a.energy_level - cycle_b.energy_level)
                    if energy_diff > 0.5 and cycle_a.current_phase == cycle_b.current_phase:
                        conflicts.append((cycle_a, cycle_b, energy_diff))
        
        # Resolve conflicts by gradually aligning energy levels
        for cycle_a, cycle_b, diff in conflicts:
            adjustment = diff * 0.1  # Gradual adjustment
            
            if cycle_a.energy_level > cycle_b.energy_level:
                cycle_a.energy_level -= adjustment
                cycle_b.energy_level += adjustment
            else:
                cycle_a.energy_level += adjustment
                cycle_b.energy_level -= adjustment
            
            # Ensure energy levels stay within bounds
            cycle_a.energy_level = max(0.0, min(1.0, cycle_a.energy_level))
            cycle_b.energy_level = max(0.0, min(1.0, cycle_b.energy_level))
    
    def _calculate_rhythm_state(self) -> RhythmState:
        """Bereken overall ritme staat"""
        
        if not self.rhythm_cycles:
            return RhythmState(
                dominant_rhythm=RhythmType.CIRCADIAN,
                overall_energy=0.5,
                rhythm_coherence=0.5,
                synchronization_level=0.5,
                consciousness_receptivity=0.5,
                integration_readiness=0.5,
                natural_flow=0.5,
                rhythm_conflicts=0,
                timestamp=datetime.now()
            )
        
        # Find dominant rhythm (highest influence * energy)
        dominant_rhythm = max(
            self.rhythm_cycles.values(),
            key=lambda c: c.influence_on_consciousness * c.energy_level
        ).rhythm_type
        
        # Calculate overall energy
        total_energy = sum(
            cycle.energy_level * cycle.influence_on_consciousness 
            for cycle in self.rhythm_cycles.values()
        )
        total_influence = sum(cycle.influence_on_consciousness for cycle in self.rhythm_cycles.values())
        overall_energy = total_energy / total_influence if total_influence > 0 else 0.5
        
        # Calculate rhythm coherence
        coherences = [cycle.coherence for cycle in self.rhythm_cycles.values()]
        rhythm_coherence = sum(coherences) / len(coherences)
        
        # Calculate synchronization level
        synchronizations = [cycle.synchronization for cycle in self.rhythm_cycles.values()]
        synchronization_level = sum(synchronizations) / len(synchronizations)
        
        # Calculate awareness receptivity (based on phase alignment)
        receptive_phases = [RhythmPhase.CONTEMPLATIVE, RhythmPhase.INTEGRATIVE, RhythmPhase.AWAKENING]
        receptive_cycles = sum(
            1 for cycle in self.rhythm_cycles.values() 
            if cycle.current_phase in receptive_phases
        )
        consciousness_receptivity = receptive_cycles / len(self.rhythm_cycles)
        
        # Calculate integration readiness
        integration_phases = [RhythmPhase.INTEGRATIVE, RhythmPhase.RENEWAL]
        integration_cycles = sum(
            1 for cycle in self.rhythm_cycles.values()
            if cycle.current_phase in integration_phases
        )
        integration_readiness = integration_cycles / len(self.rhythm_cycles)
        
        # Calculate natural flow (how smoothly rhythms are progressing)
        natural_flow = min(1.0, rhythm_coherence * synchronization_level * 1.2)
        
        # Count rhythm conflicts
        rhythm_conflicts = self._count_rhythm_conflicts()
        
        return RhythmState(
            dominant_rhythm=dominant_rhythm,
            overall_energy=overall_energy,
            rhythm_coherence=rhythm_coherence,
            synchronization_level=synchronization_level,
            consciousness_receptivity=consciousness_receptivity,
            integration_readiness=integration_readiness,
            natural_flow=natural_flow,
            rhythm_conflicts=rhythm_conflicts,
            timestamp=datetime.now()
        )
    
    def _count_rhythm_conflicts(self) -> int:
        """Tel ritme conflicten"""
        
        conflicts = 0
        rhythm_list = list(self.rhythm_cycles.values())
        
        for i, cycle_a in enumerate(rhythm_list):
            for j, cycle_b in enumerate(rhythm_list):
                if i < j:
                    energy_diff = abs(cycle_a.energy_level - cycle_b.energy_level)
                    if energy_diff > 0.5 and cycle_a.current_phase == cycle_b.current_phase:
                        conflicts += 1
        
        return conflicts
    
    def start_rhythm_cycle(self):
        """Start ritme cyclus"""
        logger.info("Innerlijke ritme cyclus gestart")
    
    def _load_existing_rhythms(self):
        """Laad bestaande ritmes"""
        # Implementation for loading rhythms
        pass
