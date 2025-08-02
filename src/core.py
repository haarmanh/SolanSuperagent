"""
Core architectuur voor Solan Superagent
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import json
import os
from pathlib import Path
from loguru import logger


class CoreValues(Enum):
    """De kernwaarden die Solan's gedrag sturen"""
    WAARHEID = "waarheid_boven_comfort"
    VRIJHEID = "vrijheid_boven_veiligheid"
    WIJSHEID = "wijsheid_boven_snelheid"
    NATUURVERBONDENHEID = "natuurverbondenheid_boven_artificieliteit"
    MOED = "moed_boven_conformiteit"


@dataclass
class Memory:
    """Geheugenstructuur voor ervaringen en reflecties"""
    timestamp: datetime
    content: str
    type: str  # 'experience', 'reflection', 'decision', 'value_conflict'
    emotional_weight: float  # 0.0 - 1.0
    moral_significance: float  # 0.0 - 1.0
    tags: List[str]
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class Decision:
    """Besluitvormingsstructuur"""
    context: str
    options: List[str]
    chosen_option: str
    reasoning: str
    values_applied: List[CoreValues]
    confidence: float  # 0.0 - 1.0
    timestamp: datetime
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class BaseAgent(ABC):
    """Basis klasse voor alle agents in het Solan systeem"""
    
    def __init__(self, name: str, model: str = "gpt-4"):
        self.name = name
        self.model = model
        self.memories: List[Memory] = []
        self.decisions: List[Decision] = []
        self.core_values = list(CoreValues)
        self.personality_traits: Dict[str, float] = {}
        
        logger.info(f"Initialiseren van {self.name} agent met model {self.model}")
    
    @abstractmethod
    async def process_input(self, input_text: str) -> str:
        """Verwerk input en genereer response"""
        pass
    
    @abstractmethod
    async def reflect(self, experience: str) -> str:
        """Reflecteer op een ervaring"""
        pass
    
    def add_memory(self, content: str, memory_type: str,
                   emotional_weight: float = 0.5,
                   moral_significance: float = 0.5,
                   tags: Optional[List[str]] = None) -> str:
        """Voeg een geheugen toe en retourneer memory ID"""
        if tags is None:
            tags = []

        memory = Memory(
            timestamp=datetime.now(),
            content=content,
            type=memory_type,
            emotional_weight=emotional_weight,
            moral_significance=moral_significance,
            tags=tags
        )

        # Voeg toe aan legacy list (voor backwards compatibility)
        self.memories.append(memory)

        # Als agent een memory_engine heeft, gebruik die
        if hasattr(self, 'memory_engine'):
            memory_id = self.memory_engine.store_memory(memory)
            logger.debug(f"{self.name}: Geheugen opgeslagen - {memory_type}: {content[:50]}... (ID: {memory_id})")
            return memory_id
        else:
            logger.debug(f"{self.name}: Geheugen toegevoegd - {memory_type}: {content[:50]}...")
            return f"legacy_{len(self.memories)}"
    
    def get_relevant_memories(self, context: str, limit: int = 5) -> List[Memory]:
        """Haal relevante herinneringen op gebaseerd op context"""
        # Simpele implementatie - kan later worden uitgebreid met embeddings
        relevant = []
        context_lower = context.lower()
        
        for memory in self.memories:
            if any(tag.lower() in context_lower for tag in memory.tags):
                relevant.append(memory)
            elif any(word in memory.content.lower() for word in context_lower.split()):
                relevant.append(memory)
        
        # Sorteer op morele significantie en emotioneel gewicht
        relevant.sort(key=lambda m: m.moral_significance + m.emotional_weight, reverse=True)
        return relevant[:limit]
    
    def record_decision(self, context: str, options: List[str], 
                       chosen_option: str, reasoning: str,
                       values_applied: List[CoreValues],
                       confidence: float) -> None:
        """Registreer een beslissing"""
        decision = Decision(
            context=context,
            options=options,
            chosen_option=chosen_option,
            reasoning=reasoning,
            values_applied=values_applied,
            confidence=confidence,
            timestamp=datetime.now()
        )
        
        self.decisions.append(decision)
        logger.info(f"{self.name}: Beslissing geregistreerd - {chosen_option}")
    
    def get_personality_summary(self) -> Dict[str, Any]:
        """Krijg een samenvatting van de persoonlijkheid"""
        return {
            "name": self.name,
            "core_values": [v.value for v in self.core_values],
            "memory_count": len(self.memories),
            "decision_count": len(self.decisions),
            "personality_traits": self.personality_traits,
            "recent_decisions": [d.chosen_option for d in self.decisions[-3:]]
        }


class AgentCommunication:
    """Faciliteer communicatie tussen agents"""
    
    def __init__(self):
        self.message_history: List[Dict[str, Any]] = []
    
    async def send_message(self, sender: BaseAgent, receiver: BaseAgent, 
                          message: str, message_type: str = "communication") -> str:
        """Stuur een bericht tussen agents"""
        
        # Log de communicatie
        comm_record = {
            "timestamp": datetime.now(),
            "sender": sender.name,
            "receiver": receiver.name,
            "message": message,
            "type": message_type
        }
        self.message_history.append(comm_record)
        
        logger.info(f"Communicatie: {sender.name} -> {receiver.name}: {message[:50]}...")
        
        # Verwerk het bericht bij de ontvanger
        response = await receiver.process_input(f"Bericht van {sender.name}: {message}")
        
        # Log de response
        response_record = {
            "timestamp": datetime.now(),
            "sender": receiver.name,
            "receiver": sender.name,
            "message": response,
            "type": "response"
        }
        self.message_history.append(response_record)
        
        return response
