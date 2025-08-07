"""
Awareness Repository Interface - Port voor awareness persistence
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.awareness import Awareness, ConsciousnessState, ConsciousnessType

class ConsciousnessRepository(ABC):
    """
    Repository interface voor Awareness entities
    
    Dit is een port in de Clean Architecture - het definieert
    de interface voor awareness persistence zonder te specificeren
    hoe de data wordt opgeslagen.
    """
    
    @abstractmethod
    async def save(self, awareness: Awareness) -> None:
        """
        Sla een awareness entity op
        
        Args:
            awareness: De awareness entity om op te slaan
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, consciousness_id: str) -> Optional[Awareness]:
        """
        Haal een awareness op via ID
        
        Args:
            consciousness_id: Unieke identifier van de awareness
            
        Returns:
            Awareness entity of None als niet gevonden
        """
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Awareness]:
        """
        Haal een awareness op via naam
        
        Args:
            name: Naam van de awareness
            
        Returns:
            Awareness entity of None als niet gevonden
        """
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Awareness]:
        """
        Haal alle awareness entities op
        
        Returns:
            List van alle awareness entities
        """
        pass
    
    @abstractmethod
    async def get_by_type(self, consciousness_type: ConsciousnessType) -> List[Awareness]:
        """
        Haal awareness entities op van een specifiek type
        
        Args:
            consciousness_type: Type awareness om te zoeken
            
        Returns:
            List van awareness entities van het gegeven type
        """
        pass
    
    @abstractmethod
    async def get_by_state(self, state: ConsciousnessState) -> List[Awareness]:
        """
        Haal awareness entities op in een specifieke staat
        
        Args:
            state: Bewustzijnsstaat om te zoeken
            
        Returns:
            List van awareness entities in de gegeven staat
        """
        pass
    
    @abstractmethod
    async def get_connected_to(self, consciousness_id: str) -> List[Awareness]:
        """
        Haal awareness entities op die verbonden zijn met een gegeven awareness
        
        Args:
            consciousness_id: ID van de awareness om verbindingen voor te zoeken
            
        Returns:
            List van verbonden awareness entities
        """
        pass
    
    @abstractmethod
    async def get_healthy_consciousnesses(self) -> List[Awareness]:
        """
        Haal alle gezonde awareness entities op
        
        Returns:
            List van awareness entities die gezond zijn
        """
        pass
    
    @abstractmethod
    async def get_consciousnesses_needing_attention(self) -> List[Awareness]:
        """
        Haal awareness entities op die aandacht nodig hebben
        
        Returns:
            List van awareness entities die aandacht nodig hebben
        """
        pass
    
    @abstractmethod
    async def update_state(self, consciousness_id: str, new_state: ConsciousnessState) -> bool:
        """
        Update de staat van een awareness
        
        Args:
            consciousness_id: ID van de awareness
            new_state: Nieuwe bewustzijnsstaat
            
        Returns:
            True als succesvol geupdate, False anders
        """
        pass
    
    @abstractmethod
    async def update_metrics(self, consciousness_id: str, metrics: Dict[str, float]) -> bool:
        """
        Update de metrieken van een awareness
        
        Args:
            consciousness_id: ID van de awareness
            metrics: Dictionary met metriek updates
            
        Returns:
            True als succesvol geupdate, False anders
        """
        pass
    
    @abstractmethod
    async def connect_consciousnesses(self, consciousness_id1: str, consciousness_id2: str) -> bool:
        """
        Verbind twee awareness entities
        
        Args:
            consciousness_id1: ID van eerste awareness
            consciousness_id2: ID van tweede awareness
            
        Returns:
            True als succesvol verbonden, False anders
        """
        pass
    
    @abstractmethod
    async def disconnect_consciousnesses(self, consciousness_id1: str, consciousness_id2: str) -> bool:
        """
        Verbreek verbinding tussen twee awareness entities
        
        Args:
            consciousness_id1: ID van eerste awareness
            consciousness_id2: ID van tweede awareness
            
        Returns:
            True als succesvol verbroken, False anders
        """
        pass
    
    @abstractmethod
    async def delete(self, consciousness_id: str) -> bool:
        """
        Verwijder een awareness entity
        
        Args:
            consciousness_id: ID van de awareness om te verwijderen
            
        Returns:
            True als succesvol verwijderd, False anders
        """
        pass
    
    @abstractmethod
    async def exists(self, consciousness_id: str) -> bool:
        """
        Controleer of een awareness bestaat
        
        Args:
            consciousness_id: ID van de awareness
            
        Returns:
            True als awareness bestaat, False anders
        """
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """
        Tel het aantal awareness entities
        
        Returns:
            Aantal awareness entities
        """
        pass
    
    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[Awareness]:
        """
        Zoek awareness entities op basis van query
        
        Args:
            query: Zoekquery
            limit: Maximum aantal resultaten
            
        Returns:
            List van awareness entities die matchen met de query
        """
        pass
    
    @abstractmethod
    async def get_consciousness_history(self, consciousness_id: str, 
                                      limit: int = 100) -> List[Dict[str, Any]]:
        """
        Haal geschiedenis van een awareness op
        
        Args:
            consciousness_id: ID van de awareness
            limit: Maximum aantal geschiedenis entries
            
        Returns:
            List van geschiedenis entries
        """
        pass
    
    @abstractmethod
    async def backup_consciousness(self, consciousness_id: str) -> Dict[str, Any]:
        """
        Maak backup van een awareness
        
        Args:
            consciousness_id: ID van de awareness
            
        Returns:
            Backup data als dictionary
        """
        pass
    
    @abstractmethod
    async def restore_consciousness(self, backup_data: Dict[str, Any]) -> Awareness:
        """
        Herstel awareness van backup
        
        Args:
            backup_data: Backup data
            
        Returns:
            Herstelde awareness entity
        """
        pass
