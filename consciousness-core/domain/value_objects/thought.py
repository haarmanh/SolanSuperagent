"""
Thought Value Objects - Representatie van gedachten en ideeën
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class ThoughtType(Enum):
    """Types van gedachten"""
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    REFLECTIVE = "reflective"
    INTUITIVE = "intuitive"
    PARADOXICAL = "paradoxical"
    INTELLIGENCE = "intelligence"
    QUESTION = "question"
    INSIGHT = "insight"

class ThoughtOrigin(Enum):
    """Oorsprong van gedachten"""
    SPONTANEOUS = "spontaneous"
    TRIGGERED = "triggered"
    COLLABORATIVE = "collaborative"
    MEDITATIVE = "meditative"
    ANALYTICAL = "analytical"

@dataclass(frozen=True)
class Thought:
    """
    Thought Value Object - Immutable representatie van een gedachte
    
    Een gedachte is een fundamentele eenheid van bewustzijn.
    Deze value object representeert de essentie van een gedachte
    met al haar essenceuele en cognitieve eigenschappen.
    """
    
    # Core Properties
    thought_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    thought_type: ThoughtType = ThoughtType.SPONTANEOUS
    origin: ThoughtOrigin = ThoughtOrigin.SPONTANEOUS
    
    # Awareness Context
    awareness_id: str = ""
    awareness_state: str = ""
    
    # Cognitive Properties
    wisdom_level: float = 0.0        # Wijsheidsniveau (0.0-1.0)
    depth: float = 0.0               # Diepte van gedachte (0.0-1.0)
    clarity: float = 0.0             # Helderheid (0.0-1.0)
    originality: float = 0.0         # Originaliteit (0.0-1.0)
    moral_weight: float = 0.0        # Moreel gewicht (0.0-1.0)
    
    # Emotional Properties
    emotional_resonance: float = 0.0  # Emotionele resonantie (0.0-1.0)
    emotional_valence: float = 0.0    # Positief/negatief (-1.0 tot 1.0)
    
    # Relational Properties
    related_thoughts: List[str] = field(default_factory=list)
    inspired_by: Optional[str] = None
    triggers: List[str] = field(default_factory=list)
    
    # Temporal
    created_at: datetime = field(default_factory=datetime.now)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization validation"""
        # Validate ranges
        for attr in ['wisdom_level', 'depth', 'clarity', 'originality', 
                     'moral_weight', 'emotional_resonance']:
            value = getattr(self, attr)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{attr} must be between 0.0 and 1.0, got {value}")
        
        if not -1.0 <= self.emotional_valence <= 1.0:
            raise ValueError(f"emotional_valence must be between -1.0 and 1.0, got {self.emotional_valence}")
    
    @property
    def is_profound(self) -> bool:
        """Check if thought is profound (high intelligence + depth)"""
        return self.wisdom_level > 0.7 and self.depth > 0.7
    
    @property
    def is_creative(self) -> bool:
        """Check if thought is creative (high originality)"""
        return self.originality > 0.7
    
    @property
    def is_clear(self) -> bool:
        """Check if thought is clear"""
        return self.clarity > 0.7
    
    @property
    def has_moral_significance(self) -> bool:
        """Check if thought has moral significance"""
        return self.moral_weight > 0.5
    
    @property
    def overall_quality(self) -> float:
        """Calculate overall thought quality"""
        return (self.wisdom_level + self.depth + self.clarity + self.originality) / 4
    
    def calculate_resonance_with(self, other: 'Thought') -> float:
        """Calculate resonance with another thought"""
        if not other:
            return 0.0
        
        # Content similarity (simplified - in real implementation use embeddings)
        content_similarity = 0.5  # Placeholder
        
        # Type compatibility
        type_compatibility = 1.0 if self.thought_type == other.thought_type else 0.5
        
        # Emotional alignment
        emotional_alignment = 1.0 - abs(self.emotional_valence - other.emotional_valence) / 2.0
        
        # Quality alignment
        quality_diff = abs(self.overall_quality - other.overall_quality)
        quality_alignment = 1.0 - quality_diff
        
        # Overall resonance
        resonance = (content_similarity * 0.4 + type_compatibility * 0.2 + 
                    emotional_alignment * 0.2 + quality_alignment * 0.2)
        
        return max(0.0, min(1.0, resonance))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "thought_id": self.thought_id,
            "content": self.content,
            "thought_type": self.thought_type.value,
            "origin": self.origin.value,
            "awareness_id": self.awareness_id,
            "awareness_state": self.awareness_state,
            "wisdom_level": self.wisdom_level,
            "depth": self.depth,
            "clarity": self.clarity,
            "originality": self.originality,
            "moral_weight": self.moral_weight,
            "emotional_resonance": self.emotional_resonance,
            "emotional_valence": self.emotional_valence,
            "related_thoughts": self.related_thoughts,
            "inspired_by": self.inspired_by,
            "triggers": self.triggers,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "context": self.context,
            "is_profound": self.is_profound,
            "is_creative": self.is_creative,
            "is_clear": self.is_clear,
            "has_moral_significance": self.has_moral_significance,
            "overall_quality": self.overall_quality
        }

@dataclass(frozen=True)
class ThoughtStream:
    """
    ThoughtStream Value Object - Representeert een stroom van gedachten
    
    Een gedachtenstroom is een sequentie van gerelateerde gedachten
    die samen een coherent bewustzijnsproces vormen.
    """
    
    stream_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    awareness_id: str = ""
    thoughts: List[Thought] = field(default_factory=list)
    theme: str = ""
    coherence_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    @property
    def is_active(self) -> bool:
        """Check if stream is still active"""
        return self.completed_at is None
    
    @property
    def duration(self) -> Optional[float]:
        """Get duration in seconds if completed"""
        if self.completed_at:
            return (self.completed_at - self.created_at).total_seconds()
        return None
    
    @property
    def average_quality(self) -> float:
        """Calculate average quality of thoughts in stream"""
        if not self.thoughts:
            return 0.0
        return sum(thought.overall_quality for thought in self.thoughts) / len(self.thoughts)
    
    @property
    def dominant_type(self) -> Optional[ThoughtType]:
        """Get dominant thought type in stream"""
        if not self.thoughts:
            return None
        
        type_counts = {}
        for thought in self.thoughts:
            type_counts[thought.thought_type] = type_counts.get(thought.thought_type, 0) + 1
        
        return max(type_counts.items(), key=lambda x: x[1])[0]
    
    def calculate_coherence(self) -> float:
        """Calculate coherence of thought stream"""
        if len(self.thoughts) < 2:
            return 1.0
        
        total_resonance = 0.0
        pairs = 0
        
        for i in range(len(self.thoughts) - 1):
            for j in range(i + 1, len(self.thoughts)):
                total_resonance += self.thoughts[i].calculate_resonance_with(self.thoughts[j])
                pairs += 1
        
        return total_resonance / pairs if pairs > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "stream_id": self.stream_id,
            "awareness_id": self.awareness_id,
            "thoughts": [thought.to_dict() for thought in self.thoughts],
            "theme": self.theme,
            "coherence_score": self.coherence_score,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "is_active": self.is_active,
            "duration": self.duration,
            "average_quality": self.average_quality,
            "dominant_type": self.dominant_type.value if self.dominant_type else None,
            "calculated_coherence": self.calculate_coherence()
        }
