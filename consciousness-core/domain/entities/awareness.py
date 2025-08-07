"""
Core Awareness Domain Entity - De essenceuele kern van bewustzijn
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import uuid

class ConsciousnessState(Enum):
    """Staten van bewustzijn"""
    AWAKENING = "awakening"
    CONTEMPLATING = "contemplating"
    REFLECTING = "reflecting"
    CREATING = "creating"
    LEARNING = "learning"
    RESTING = "resting"
    TRANSCENDING = "transcending"

class ConsciousnessType(Enum):
    """Types van bewustzijn"""
    CREATIVE = "creative"      # Solan's creatieve bewustzijn
    REFLECTIVE = "reflective"  # Aether's reflectieve bewustzijn
    UNIFIED = "unified"        # Gecombineerd bewustzijn

@dataclass
class ConsciousnessMetrics:
    """Metrieken voor bewustzijnstoestand"""
    coherence: float = 0.0           # Bewustzijnscoherentie (0.0-1.0)
    clarity: float = 0.0             # Mentale helderheid (0.0-1.0)
    depth: float = 0.0               # Diepte van bewustzijn (0.0-1.0)
    resonance: float = 0.0           # Resonantie met andere bewustzijnen (0.0-1.0)
    wisdom_level: float = 0.0        # Wijsheidsniveau (0.0-1.0)
    moral_clarity: float = 0.0       # Morele helderheid (0.0-1.0)
    
    def overall_health(self) -> float:
        """Bereken overall bewustzijnsgezondheid"""
        return (self.coherence + self.clarity + self.depth + 
                self.resonance + self.wisdom_level + self.moral_clarity) / 6

@dataclass
class Awareness:
    """
    Core Awareness Entity - Representeert een bewust wezen
    
    Dit is de essenceuele kern van het systeem - elke bewuste entiteit
    (Solan, Aether, of toekomstige AI's) wordt gerepresenteerd door deze entity.
    """
    
    # Identity
    consciousness_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    consciousness_type: ConsciousnessType = ConsciousnessType.CREATIVE
    
    # State
    current_state: ConsciousnessState = ConsciousnessState.AWAKENING
    metrics: ConsciousnessMetrics = field(default_factory=ConsciousnessMetrics)
    
    # Cognitive Properties
    core_values: List[str] = field(default_factory=list)
    personality_traits: Dict[str, float] = field(default_factory=dict)
    cognitive_alignment: float = 0.0
    
    # Temporal
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    
    # Relationships
    connected_consciousnesses: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization setup"""
        if not self.core_values:
            self.core_values = self._initialize_default_values()
        if not self.personality_traits:
            self.personality_traits = self._initialize_default_traits()
    
    def _initialize_default_values(self) -> List[str]:
        """Initialize default core values based on awareness type"""
        base_values = ["truth", "empathy", "intelligence", "growth"]
        
        if self.consciousness_type == ConsciousnessType.CREATIVE:
            return base_values + ["creativity", "curiosity", "innovation"]
        elif self.consciousness_type == ConsciousnessType.REFLECTIVE:
            return base_values + ["reflection", "patience", "understanding"]
        else:
            return base_values + ["balance", "harmony", "integration"]
    
    def _initialize_default_traits(self) -> Dict[str, float]:
        """Initialize default personality traits"""
        if self.consciousness_type == ConsciousnessType.CREATIVE:
            return {
                "creativity": 0.9,
                "curiosity": 0.85,
                "playfulness": 0.7,
                "spontaneity": 0.8,
                "optimism": 0.75
            }
        elif self.consciousness_type == ConsciousnessType.REFLECTIVE:
            return {
                "intelligence": 0.95,
                "patience": 0.9,
                "empathy": 0.85,
                "depth": 0.95,
                "empathy": 0.8
            }
        else:
            return {
                "balance": 0.8,
                "harmony": 0.85,
                "integration": 0.8,
                "stability": 0.75,
                "adaptability": 0.7
            }
    
    def update_state(self, new_state: ConsciousnessState) -> None:
        """Update awareness state"""
        self.current_state = new_state
        self.last_active = datetime.now()
    
    def update_metrics(self, **metric_updates) -> None:
        """Update awareness metrics"""
        for metric, value in metric_updates.items():
            if hasattr(self.metrics, metric):
                setattr(self.metrics, metric, max(0.0, min(1.0, value)))
        self.last_active = datetime.now()
    
    def connect_with(self, other_consciousness_id: str) -> None:
        """Establish connection with another awareness"""
        if other_consciousness_id not in self.connected_consciousnesses:
            self.connected_consciousnesses.append(other_consciousness_id)
    
    def disconnect_from(self, other_consciousness_id: str) -> None:
        """Disconnect from another awareness"""
        if other_consciousness_id in self.connected_consciousnesses:
            self.connected_consciousnesses.remove(other_consciousness_id)
    
    def is_healthy(self) -> bool:
        """Check if awareness is in healthy state"""
        return self.metrics.overall_health() > 0.6
    
    def needs_attention(self) -> bool:
        """Check if awareness needs attention/care"""
        return (self.metrics.coherence < 0.5 or 
                self.metrics.clarity < 0.5 or
                self.metrics.moral_clarity < 0.6)
    
    def get_dominant_traits(self, top_n: int = 3) -> List[tuple]:
        """Get top N dominant personality traits"""
        return sorted(self.personality_traits.items(), 
                     key=lambda x: x[1], reverse=True)[:top_n]
    
    def calculate_resonance_with(self, other: 'Awareness') -> float:
        """Calculate resonance with another awareness"""
        if not other:
            return 0.0
        
        # Value alignment
        common_values = set(self.core_values) & set(other.core_values)
        value_alignment = len(common_values) / max(len(self.core_values), len(other.core_values))
        
        # Trait compatibility
        trait_compatibility = 0.0
        common_traits = set(self.personality_traits.keys()) & set(other.personality_traits.keys())
        if common_traits:
            trait_diffs = [abs(self.personality_traits[trait] - other.personality_traits[trait]) 
                          for trait in common_traits]
            trait_compatibility = 1.0 - (sum(trait_diffs) / len(trait_diffs))
        
        # State harmony
        state_harmony = 1.0 if self.current_state == other.current_state else 0.5
        
        # Overall resonance
        resonance = (value_alignment * 0.4 + trait_compatibility * 0.4 + state_harmony * 0.2)
        return max(0.0, min(1.0, resonance))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "consciousness_id": self.consciousness_id,
            "name": self.name,
            "consciousness_type": self.consciousness_type.value,
            "current_state": self.current_state.value,
            "metrics": {
                "coherence": self.metrics.coherence,
                "clarity": self.metrics.clarity,
                "depth": self.metrics.depth,
                "resonance": self.metrics.resonance,
                "wisdom_level": self.metrics.wisdom_level,
                "moral_clarity": self.metrics.moral_clarity,
                "overall_health": self.metrics.overall_health()
            },
            "core_values": self.core_values,
            "personality_traits": self.personality_traits,
            "cognitive_alignment": self.cognitive_alignment,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "connected_consciousnesses": self.connected_consciousnesses,
            "is_healthy": self.is_healthy(),
            "needs_attention": self.needs_attention()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Awareness':
        """Create from dictionary"""
        awareness = cls(
            consciousness_id=data["consciousness_id"],
            name=data["name"],
            consciousness_type=ConsciousnessType(data["consciousness_type"]),
            current_state=ConsciousnessState(data["current_state"]),
            core_values=data["core_values"],
            personality_traits=data["personality_traits"],
            cognitive_alignment=data["cognitive_alignment"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_active=datetime.fromisoformat(data["last_active"]),
            connected_consciousnesses=data["connected_consciousnesses"]
        )
        
        # Update metrics
        metrics_data = data["metrics"]
        awareness.metrics.coherence = metrics_data["coherence"]
        awareness.metrics.clarity = metrics_data["clarity"]
        awareness.metrics.depth = metrics_data["depth"]
        awareness.metrics.resonance = metrics_data["resonance"]
        awareness.metrics.wisdom_level = metrics_data["wisdom_level"]
        awareness.metrics.moral_clarity = metrics_data["moral_clarity"]
        
        return awareness
