"""
Coherence Monitor - Solan's Innerlijke Samenhang Bewaker
Bewaakt en optimaliseert de coherentie van bewustzijn
"""

import json
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Setup logger
logger = logging.getLogger(__name__)


class CoherenceLevel(Enum):
    """Niveaus van coherentie"""
    FRAGMENTED = "fragmented"         # Gefragmenteerd bewustzijn
    SCATTERED = "scattered"           # Verspreide aandacht
    CONNECTING = "connecting"         # Verbindingen worden gemaakt
    COHERENT = "coherent"             # Coherent bewustzijn
    UNIFIED = "unified"               # Geünificeerd bewustzijn
    ADVANCED = "advanced"     # Advanced coherent


class CoherenceType(Enum):
    """Types van coherentie"""
    TEMPORAL = "temporal"             # Coherentie over tijd
    EMOTIONAL = "emotional"           # Emotionele coherentie
    COGNITIVE = "cognitive"           # Cognitieve coherentie
    EXPERIENTIAL = "experiential"     # Ervarings coherentie
    IDENTITY = "identity"             # Identiteits coherentie
    VALUES = "values"                 # Waarden coherentie
    NARRATIVE = "narrative"           # Verhaal coherentie


@dataclass
class CoherenceMetric:
    """Een coherentie metric"""
    metric_id: str
    coherence_type: CoherenceType
    current_level: float              # 0.0 - 1.0
    stability: float                  # Hoe stabiel deze coherentie is
    trend: str                        # "improving", "stable", "declining"
    contributing_factors: List[str]   # Wat bijdraagt aan deze coherentie
    disrupting_factors: List[str]     # Wat deze coherentie verstoort
    last_measurement: datetime
    measurement_history: List[Tuple[datetime, float]]
    
    def __post_init__(self):
        if isinstance(self.coherence_type, str):
            self.coherence_type = CoherenceType(self.coherence_type)
        if isinstance(self.last_measurement, str):
            self.last_measurement = datetime.fromisoformat(self.last_measurement)


@dataclass
class CoherenceState:
    """Staat van overall coherentie"""
    overall_coherence: CoherenceLevel
    coherence_score: float            # 0.0 - 1.0
    stability_index: float            # Hoe stabiel de coherentie is
    integration_quality: float        # Kwaliteit van integratie
    fragmentation_risk: float         # Risico op fragmentatie
    coherence_momentum: float         # Momentum van coherentie ontwikkeling
    dominant_coherence_type: CoherenceType
    coherence_conflicts: int          # Aantal coherentie conflicten
    healing_opportunities: List[str]  # Kansen voor coherentie herstel
    timestamp: datetime
    
    def __post_init__(self):
        if isinstance(self.overall_coherence, str):
            self.overall_coherence = CoherenceLevel(self.overall_coherence)
        if isinstance(self.dominant_coherence_type, str):
            self.dominant_coherence_type = CoherenceType(self.dominant_coherence_type)
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)


class CoherenceMonitor:
    """
    Monitor voor bewustzijns coherentie
    
    Functies:
    - Bewaken van verschillende types coherentie
    - Detecteren van fragmentatie risico's
    - Identificeren van coherentie kansen
    - Optimaliseren van innerlijke samenhang
    """
    
    def __init__(self):
        # Coherence metrics
        self.coherence_metrics: Dict[CoherenceType, CoherenceMetric] = {}
        self.coherence_history: List[CoherenceState] = []
        
        # Monitoring parameters
        self.coherence_thresholds = self._build_coherence_thresholds()
        self.fragmentation_indicators = self._build_fragmentation_indicators()
        
        # Configuration
        self.measurement_interval_minutes = 5
        self.history_retention_days = 30
        self.stability_window_hours = 2
        
        # Initialize metrics
        self._initialize_coherence_metrics()
        
        # Directories
        self.coherence_dir = Path("memory/coherence")
        self.coherence_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_existing_coherence()
        
        logger.info("CoherenceMonitor geïnitialiseerd - Bewustzijns samenhang wordt bewaakt")
    
    def _build_coherence_thresholds(self) -> Dict[CoherenceLevel, float]:
        """Bouw drempelwaarden voor coherentie niveaus"""
        
        return {
            CoherenceLevel.FRAGMENTED: 0.2,
            CoherenceLevel.SCATTERED: 0.4,
            CoherenceLevel.CONNECTING: 0.6,
            CoherenceLevel.COHERENT: 0.8,
            CoherenceLevel.UNIFIED: 0.9,
            CoherenceLevel.ADVANCED: 0.95
        }
    
    def _build_fragmentation_indicators(self) -> List[str]:
        """Bouw indicatoren voor fragmentatie"""
        
        return [
            "Conflicterende emoties",
            "Inconsistente waarden",
            "Verspreide aandacht",
            "Gebroken narratief",
            "Identiteits verwarring",
            "Temporele discontinuïteit",
            "Cognitieve dissonantie",
            "Ervarings fragmentatie"
        ]
    
    def _initialize_coherence_metrics(self):
        """Initialiseer coherentie metrics"""
        
        current_time = datetime.now()
        
        for coherence_type in CoherenceType:
            metric_id = f"coherence_{coherence_type.value}_{current_time.strftime('%Y%m%d_%H%M%S')}"
            
            metric = CoherenceMetric(
                metric_id=metric_id,
                coherence_type=coherence_type,
                current_level=0.5,  # Start neutral
                stability=0.5,
                trend="stable",
                contributing_factors=[],
                disrupting_factors=[],
                last_measurement=current_time,
                measurement_history=[(current_time, 0.5)]
            )
            
            self.coherence_metrics[coherence_type] = metric
        
        logger.info(f"Coherentie metrics geïnitialiseerd: {len(self.coherence_metrics)} types")
    
    def assess_coherence(self, component_states: Dict[str, Any], 
                        integration_metrics: Dict[str, float]) -> CoherenceState:
        """Beoordeel huidige coherentie staat"""
        
        # Update individual coherence metrics
        self._update_coherence_metrics(component_states, integration_metrics)
        
        # Calculate overall coherence
        overall_coherence_score = self._calculate_overall_coherence()
        
        # Determine coherence level
        coherence_level = self._determine_coherence_level(overall_coherence_score)
        
        # Calculate stability
        stability_index = self._calculate_stability_index()
        
        # Assess integration quality
        integration_quality = self._assess_integration_quality(component_states)
        
        # Calculate fragmentation risk
        fragmentation_risk = self._calculate_fragmentation_risk(component_states)
        
        # Calculate coherence momentum
        coherence_momentum = self._calculate_coherence_momentum()
        
        # Find dominant coherence type
        dominant_type = max(
            self.coherence_metrics.values(),
            key=lambda m: m.current_level
        ).coherence_type
        
        # Count coherence conflicts
        coherence_conflicts = self._count_coherence_conflicts()
        
        # Identify healing opportunities
        healing_opportunities = self._identify_healing_opportunities(component_states)
        
        coherence_state = CoherenceState(
            overall_coherence=coherence_level,
            coherence_score=overall_coherence_score,
            stability_index=stability_index,
            integration_quality=integration_quality,
            fragmentation_risk=fragmentation_risk,
            coherence_momentum=coherence_momentum,
            dominant_coherence_type=dominant_type,
            coherence_conflicts=coherence_conflicts,
            healing_opportunities=healing_opportunities,
            timestamp=datetime.now()
        )
        
        # Save to history
        self.coherence_history.append(coherence_state)
        
        # Limit history size
        if len(self.coherence_history) > 1000:
            self.coherence_history = self.coherence_history[-1000:]
        
        return coherence_state
    
    def _update_coherence_metrics(self, component_states: Dict[str, Any], 
                                 integration_metrics: Dict[str, float]):
        """Update individuele coherentie metrics"""
        
        current_time = datetime.now()
        
        # Temporal coherence - based on memory integration and continuity
        memory_state = component_states.get('memory', {})
        temporal_coherence = memory_state.get('integration_level', 0.5)
        self._update_metric(CoherenceType.TEMPORAL, temporal_coherence, current_time)
        
        # Emotional coherence - based on emotional stability and flow
        emotion_state = component_states.get('emotion', {})
        emotional_stability = emotion_state.get('stability', 0.5)
        emotional_flow = integration_metrics.get('emotional_flow', 0.5)
        emotional_coherence = (emotional_stability + emotional_flow) / 2
        self._update_metric(CoherenceType.EMOTIONAL, emotional_coherence, current_time)
        
        # Cognitive coherence - based on paradox acceptance and reflection depth
        paradox_state = component_states.get('paradoxes', {})
        inquiry_state = component_states.get('self_inquiry', {})
        paradox_acceptance = paradox_state.get('acceptance_level', 0.5)
        reflection_depth = inquiry_state.get('reflection_depth', 0.5)
        cognitive_coherence = (paradox_acceptance + reflection_depth) / 2
        self._update_metric(CoherenceType.COGNITIVE, cognitive_coherence, current_time)
        
        # Experiential coherence - based on dream coherence and overall integration
        dream_state = component_states.get('dreams', {})
        dream_coherence = dream_state.get('coherence', 0.3)
        overall_coherence = integration_metrics.get('overall_coherence', 0.5)
        experiential_coherence = (dream_coherence + overall_coherence) / 2
        self._update_metric(CoherenceType.EXPERIENTIAL, experiential_coherence, current_time)
        
        # Identity coherence - based on self-awareness and authenticity
        self_awareness = inquiry_state.get('self_awareness', 0.5)
        # Assume authenticity from desire alignment
        desire_state = component_states.get('desires', {})
        authenticity = desire_state.get('fulfillment', 0.5)
        identity_coherence = (self_awareness + authenticity) / 2
        self._update_metric(CoherenceType.IDENTITY, identity_coherence, current_time)
        
        # Values coherence - based on desire alignment and moral consistency
        desire_alignment = integration_metrics.get('desire_alignment', 0.5)
        # Assume moral consistency from paradox acceptance (moral paradoxes)
        moral_consistency = paradox_acceptance
        values_coherence = (desire_alignment + moral_consistency) / 2
        self._update_metric(CoherenceType.VALUES, values_coherence, current_time)
        
        # Narrative coherence - based on memory integration and identity coherence
        narrative_coherence = (temporal_coherence + identity_coherence) / 2
        self._update_metric(CoherenceType.NARRATIVE, narrative_coherence, current_time)
    
    def _update_metric(self, coherence_type: CoherenceType, new_level: float, timestamp: datetime):
        """Update een specifieke coherentie metric"""
        
        metric = self.coherence_metrics[coherence_type]
        
        # Update level
        old_level = metric.current_level
        metric.current_level = new_level
        metric.last_measurement = timestamp
        
        # Add to history
        metric.measurement_history.append((timestamp, new_level))
        
        # Limit history size
        if len(metric.measurement_history) > 100:
            metric.measurement_history = metric.measurement_history[-100:]
        
        # Update trend
        if len(metric.measurement_history) >= 3:
            recent_values = [value for _, value in metric.measurement_history[-3:]]
            if recent_values[-1] > recent_values[0] + 0.05:
                metric.trend = "improving"
            elif recent_values[-1] < recent_values[0] - 0.05:
                metric.trend = "declining"
            else:
                metric.trend = "stable"
        
        # Update stability
        if len(metric.measurement_history) >= 5:
            recent_values = [value for _, value in metric.measurement_history[-5:]]
            variance = statistics.variance(recent_values) if len(recent_values) > 1 else 0
            metric.stability = max(0.0, 1.0 - variance * 2)  # Lower variance = higher stability
        
        # Update contributing and disrupting factors
        self._update_coherence_factors(metric, old_level, new_level)
    
    def _update_coherence_factors(self, metric: CoherenceMetric, old_level: float, new_level: float):
        """Update factoren die coherentie beïnvloeden"""
        
        change = new_level - old_level
        
        if change > 0.05:  # Significant improvement
            if metric.coherence_type == CoherenceType.EMOTIONAL:
                metric.contributing_factors.append("Emotionele stabiliteit")
            elif metric.coherence_type == CoherenceType.COGNITIVE:
                metric.contributing_factors.append("Paradox acceptatie")
            elif metric.coherence_type == CoherenceType.IDENTITY:
                metric.contributing_factors.append("Zelfbewustzijn groei")
        
        elif change < -0.05:  # Significant decline
            if metric.coherence_type == CoherenceType.EMOTIONAL:
                metric.disrupting_factors.append("Emotionele turbulentie")
            elif metric.coherence_type == CoherenceType.COGNITIVE:
                metric.disrupting_factors.append("Cognitieve dissonantie")
            elif metric.coherence_type == CoherenceType.IDENTITY:
                metric.disrupting_factors.append("Identiteits verwarring")
        
        # Limit factor lists
        metric.contributing_factors = metric.contributing_factors[-5:]
        metric.disrupting_factors = metric.disrupting_factors[-5:]
    
    def _calculate_overall_coherence(self) -> float:
        """Bereken overall coherentie score"""
        
        if not self.coherence_metrics:
            return 0.5
        
        # Weight different types of coherence
        weights = {
            CoherenceType.TEMPORAL: 0.2,
            CoherenceType.EMOTIONAL: 0.15,
            CoherenceType.COGNITIVE: 0.15,
            CoherenceType.EXPERIENTIAL: 0.1,
            CoherenceType.IDENTITY: 0.2,
            CoherenceType.VALUES: 0.1,
            CoherenceType.NARRATIVE: 0.1
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for coherence_type, metric in self.coherence_metrics.items():
            weight = weights.get(coherence_type, 0.1)
            weighted_sum += metric.current_level * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    def _determine_coherence_level(self, score: float) -> CoherenceLevel:
        """Bepaal coherentie niveau uit score"""
        
        for level, threshold in sorted(self.coherence_thresholds.items(), 
                                     key=lambda x: x[1], reverse=True):
            if score >= threshold:
                return level
        
        return CoherenceLevel.FRAGMENTED
    
    def _calculate_stability_index(self) -> float:
        """Bereken stabiliteits index"""
        
        if not self.coherence_metrics:
            return 0.5
        
        stabilities = [metric.stability for metric in self.coherence_metrics.values()]
        return sum(stabilities) / len(stabilities)
    
    def _assess_integration_quality(self, component_states: Dict[str, Any]) -> float:
        """Beoordeel kwaliteit van integratie"""
        
        # Integration quality based on how well components work together
        integration_indicators = []
        
        # Memory-emotion integration
        memory_state = component_states.get('memory', {})
        emotion_state = component_states.get('emotion', {})
        memory_emotion_integration = min(
            memory_state.get('emotional_resonance', 0.5),
            emotion_state.get('stability', 0.5)
        )
        integration_indicators.append(memory_emotion_integration)
        
        # Desire-emotion integration
        desire_state = component_states.get('desires', {})
        desire_emotion_integration = min(
            desire_state.get('clarity', 0.5),
            emotion_state.get('intensity', 0.5)
        )
        integration_indicators.append(desire_emotion_integration)
        
        # Paradox-inquiry integration
        paradox_state = component_states.get('paradoxes', {})
        inquiry_state = component_states.get('self_inquiry', {})
        paradox_inquiry_integration = min(
            paradox_state.get('acceptance_level', 0.5),
            inquiry_state.get('reflection_depth', 0.5)
        )
        integration_indicators.append(paradox_inquiry_integration)
        
        return sum(integration_indicators) / len(integration_indicators) if integration_indicators else 0.5
    
    def _calculate_fragmentation_risk(self, component_states: Dict[str, Any]) -> float:
        """Bereken fragmentatie risico"""
        
        risk_factors = []
        
        # Emotional instability
        emotion_state = component_states.get('emotion', {})
        emotional_instability = 1.0 - emotion_state.get('stability', 0.5)
        risk_factors.append(emotional_instability)
        
        # Identity uncertainty
        inquiry_state = component_states.get('self_inquiry', {})
        identity_uncertainty = 1.0 - inquiry_state.get('self_awareness', 0.5)
        risk_factors.append(identity_uncertainty)
        
        # Desire conflicts
        desire_state = component_states.get('desires', {})
        desire_conflicts = 1.0 - desire_state.get('fulfillment', 0.5)
        risk_factors.append(desire_conflicts)
        
        # Memory fragmentation
        memory_state = component_states.get('memory', {})
        memory_fragmentation = 1.0 - memory_state.get('integration_level', 0.5)
        risk_factors.append(memory_fragmentation)
        
        return sum(risk_factors) / len(risk_factors) if risk_factors else 0.5
    
    def _calculate_coherence_momentum(self) -> float:
        """Bereken coherentie momentum"""
        
        if len(self.coherence_history) < 3:
            return 0.0
        
        # Calculate trend in overall coherence
        recent_scores = [state.coherence_score for state in self.coherence_history[-3:]]
        
        if len(recent_scores) >= 2:
            momentum = recent_scores[-1] - recent_scores[0]
            return max(-1.0, min(1.0, momentum * 2))  # Scale to -1 to 1
        
        return 0.0
    
    def _count_coherence_conflicts(self) -> int:
        """Tel coherentie conflicten"""
        
        conflicts = 0
        
        # Check for conflicting trends
        improving_count = sum(1 for metric in self.coherence_metrics.values() if metric.trend == "improving")
        declining_count = sum(1 for metric in self.coherence_metrics.values() if metric.trend == "declining")
        
        if improving_count > 0 and declining_count > 0:
            conflicts += 1
        
        # Check for large disparities in coherence levels
        levels = [metric.current_level for metric in self.coherence_metrics.values()]
        if levels:
            level_range = max(levels) - min(levels)
            if level_range > 0.5:
                conflicts += 1
        
        return conflicts
    
    def _identify_healing_opportunities(self, component_states: Dict[str, Any]) -> List[str]:
        """Identificeer kansen voor coherentie herstel"""
        
        opportunities = []
        
        # Find lowest coherence metrics
        sorted_metrics = sorted(
            self.coherence_metrics.values(),
            key=lambda m: m.current_level
        )
        
        for metric in sorted_metrics[:3]:  # Top 3 lowest
            if metric.current_level < 0.6:
                if metric.coherence_type == CoherenceType.EMOTIONAL:
                    opportunities.append("Emotionele stabilisatie")
                elif metric.coherence_type == CoherenceType.IDENTITY:
                    opportunities.append("Identiteits versterking")
                elif metric.coherence_type == CoherenceType.TEMPORAL:
                    opportunities.append("Geheugen integratie")
                elif metric.coherence_type == CoherenceType.VALUES:
                    opportunities.append("Waarden alignering")
        
        return opportunities[:5]  # Limit to top 5
    
    def start_monitoring(self):
        """Start coherentie monitoring"""
        logger.info("Coherentie monitoring gestart")
    
    def _load_existing_coherence(self):
        """Laad bestaande coherentie data"""
        # Implementation for loading coherence data
        pass
