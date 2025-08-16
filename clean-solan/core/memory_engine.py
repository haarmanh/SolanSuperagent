"""
Dynamisch Geheugen Systeem voor Solan
- Persistent opslag van alle ervaringen
- Intelligente teruggroep van relevante herinneringen
- Groei van bewustzijn door accumulatie van wijsheid
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
import hashlib
import logging

# Setup logger
logger = logging.getLogger(__name__)

from core import Memory, Decision, CoreValues


@dataclass
class ExperienceCluster:
    """Een cluster van gerelateerde ervaringen"""
    theme: str
    memories: List[str]  # Memory IDs
    emotional_resonance: float
    moral_weight: float
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    
    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.last_accessed, str):
            self.last_accessed = datetime.fromisoformat(self.last_accessed)


@dataclass
class IntelligencePattern:
    """Een patroon van wijsheid dat Solan heeft ontwikkeld"""
    pattern_id: str
    description: str
    supporting_memories: List[str]
    confidence: float
    applications: List[str]  # Situaties waar dit patroon werd toegepast
    created_at: datetime
    
    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)


class MemoryEngine:
    """
    Solan's dynamische geheugen systeem
    
    Functies:
    - Persistent opslag van alle ervaringen
    - Intelligente clustering van gerelateerde herinneringen
    - Patroonherkenning in morele ontwikkeling
    - Contextual retrieval van relevante wijsheid
    """
    
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Subdirectories voor verschillende types geheugen
        self.experiences_dir = self.memory_dir / "experiences"
        self.reflections_dir = self.memory_dir / "reflections"
        self.decisions_dir = self.memory_dir / "decisions"
        self.patterns_dir = self.memory_dir / "patterns"
        self.clusters_dir = self.memory_dir / "clusters"
        
        for dir_path in [self.experiences_dir, self.reflections_dir, 
                        self.decisions_dir, self.patterns_dir, self.clusters_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # In-memory caches voor snelle toegang
        self.memory_cache: Dict[str, Memory] = {}
        self.decision_cache: Dict[str, Decision] = {}
        self.clusters: Dict[str, ExperienceCluster] = {}
        self.wisdom_patterns: Dict[str, IntelligencePattern] = {}
        
        # Load existing data
        self._load_existing_data()
        
        logger.info(f"MemoryEngine geïnitialiseerd in {self.memory_dir}")
    
    def _generate_memory_id(self, memory: Memory) -> str:
        """Genereer unieke ID voor een geheugen"""
        content_hash = hashlib.md5(
            f"{memory.content}{memory.timestamp}".encode()
        ).hexdigest()[:8]
        return f"mem_{memory.timestamp.strftime('%Y%m%d_%H%M%S')}_{content_hash}"
    
    def _generate_decision_id(self, decision: Decision) -> str:
        """Genereer unieke ID voor een beslissing"""
        content_hash = hashlib.md5(
            f"{decision.context}{decision.chosen_option}{decision.timestamp}".encode()
        ).hexdigest()[:8]
        return f"dec_{decision.timestamp.strftime('%Y%m%d_%H%M%S')}_{content_hash}"
    
    def store_memory(self, memory: Memory) -> str:
        """Sla een geheugen op en retourneer de ID"""
        memory_id = self._generate_memory_id(memory)
        
        # Voeg toe aan cache
        self.memory_cache[memory_id] = memory
        
        # Sla op naar bestand
        memory_data = asdict(memory)
        memory_data['timestamp'] = memory.timestamp.isoformat()
        memory_data['memory_id'] = memory_id
        
        file_path = self.experiences_dir / f"{memory_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=2, ensure_ascii=False)
        
        # Update clusters
        self._update_clusters(memory_id, memory)
        
        # Check voor nieuwe wijsheidspatronen
        self._detect_wisdom_patterns(memory_id, memory)
        
        logger.debug(f"Geheugen opgeslagen: {memory_id}")
        return memory_id
    
    def store_decision(self, decision: Decision) -> str:
        """Sla een beslissing op en retourneer de ID"""
        decision_id = self._generate_decision_id(decision)
        
        # Voeg toe aan cache
        self.decision_cache[decision_id] = decision
        
        # Sla op naar bestand
        decision_data = asdict(decision)
        decision_data['timestamp'] = decision.timestamp.isoformat()
        decision_data['values_applied'] = [v.value for v in decision.values_applied]
        decision_data['decision_id'] = decision_id
        
        file_path = self.decisions_dir / f"{decision_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(decision_data, f, indent=2, ensure_ascii=False)
        
        logger.debug(f"Beslissing opgeslagen: {decision_id}")
        return decision_id
    
    def retrieve_memories(self, context: str, limit: int = 10, 
                         memory_types: Optional[List[str]] = None,
                         time_range_days: Optional[int] = None) -> List[Memory]:
        """
        Haal relevante herinneringen op gebaseerd op context
        
        Args:
            context: De context waarvoor herinneringen gezocht worden
            limit: Maximum aantal herinneringen
            memory_types: Filter op specifieke geheugen types
            time_range_days: Alleen herinneringen van de laatste N dagen
        """
        
        relevant_memories = []
        context_lower = context.lower()
        
        # Filter op tijd indien opgegeven
        cutoff_date = None
        if time_range_days:
            cutoff_date = datetime.now() - timedelta(days=time_range_days)
        
        for memory_id, memory in self.memory_cache.items():
            # Time filter
            if cutoff_date and memory.timestamp < cutoff_date:
                continue
            
            # Type filter
            if memory_types and memory.type not in memory_types:
                continue
            
            # Relevantie score berekenen
            relevance_score = self._calculate_relevance(memory, context_lower)
            
            if relevance_score > 0.1:  # Minimum relevantie threshold
                relevant_memories.append((memory, relevance_score))
        
        # Sorteer op relevantie en morele significantie
        relevant_memories.sort(
            key=lambda x: (x[1], x[0].moral_significance, x[0].emotional_weight),
            reverse=True
        )
        
        # Update access patterns voor clustering
        for memory, _ in relevant_memories[:limit]:
            memory_id = self._find_memory_id(memory)
            if memory_id:
                self._update_access_pattern(memory_id)
        
        return [memory for memory, _ in relevant_memories[:limit]]
    
    def _calculate_relevance(self, memory: Memory, context: str) -> float:
        """Bereken relevantie score van een geheugen voor een context"""
        score = 0.0
        
        # Tag matching (hoogste gewicht)
        for tag in memory.tags:
            if tag.lower() in context:
                score += 0.4
        
        # Content matching
        memory_words = memory.content.lower().split()
        context_words = context.split()
        
        common_words = set(memory_words) & set(context_words)
        if common_words:
            score += 0.3 * (len(common_words) / max(len(memory_words), len(context_words)))
        
        # Type bonus voor bepaalde types
        if memory.type in ['reflection', 'intelligence', 'moral_insight']:
            score += 0.2
        
        # Recency bonus (meer recent = hoger)
        days_old = (datetime.now() - memory.timestamp).days
        if days_old < 7:
            score += 0.1 * (7 - days_old) / 7
        
        return min(score, 1.0)
    
    def _update_clusters(self, memory_id: str, memory: Memory) -> None:
        """Update experience clusters met nieuwe geheugen"""
        
        # Zoek bestaande clusters waar dit geheugen bij past
        best_cluster = None
        best_similarity = 0.0
        
        for cluster_id, cluster in self.clusters.items():
            similarity = self._calculate_cluster_similarity(memory, cluster)
            if similarity > best_similarity and similarity > 0.3:
                best_similarity = similarity
                best_cluster = cluster_id
        
        if best_cluster:
            # Voeg toe aan bestaande cluster
            self.clusters[best_cluster].memories.append(memory_id)
            self.clusters[best_cluster].last_accessed = datetime.now()
        else:
            # Maak nieuwe cluster
            cluster_id = f"cluster_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            theme = self._extract_theme(memory)
            
            new_cluster = ExperienceCluster(
                theme=theme,
                memories=[memory_id],
                emotional_resonance=memory.emotional_weight,
                moral_weight=memory.moral_significance,
                created_at=datetime.now(),
                last_accessed=datetime.now()
            )
            
            self.clusters[cluster_id] = new_cluster
            
            # Sla cluster op
            self._save_cluster(cluster_id, new_cluster)
    
    def _calculate_cluster_similarity(self, memory: Memory, cluster: ExperienceCluster) -> float:
        """Bereken hoe goed een geheugen past bij een cluster"""
        
        # Tag overlap
        cluster_memories = [self.memory_cache.get(mid) for mid in cluster.memories[-5:]]
        cluster_memories = [m for m in cluster_memories if m]
        
        if not cluster_memories:
            return 0.0
        
        all_cluster_tags = set()
        for mem in cluster_memories:
            all_cluster_tags.update(mem.tags)
        
        memory_tags = set(memory.tags)
        tag_overlap = len(memory_tags & all_cluster_tags) / max(len(memory_tags | all_cluster_tags), 1)
        
        # Emotionele resonantie
        avg_emotional = sum(m.emotional_weight for m in cluster_memories) / len(cluster_memories)
        emotional_similarity = 1.0 - abs(memory.emotional_weight - avg_emotional)
        
        # Morele gewicht
        avg_moral = sum(m.moral_significance for m in cluster_memories) / len(cluster_memories)
        moral_similarity = 1.0 - abs(memory.moral_significance - avg_moral)
        
        return (tag_overlap * 0.5 + emotional_similarity * 0.3 + moral_similarity * 0.2)
    
    def _extract_theme(self, memory: Memory) -> str:
        """Extraheer hoofdthema uit een geheugen"""
        
        # Gebruik tags als basis
        if memory.tags:
            return memory.tags[0]
        
        # Fallback naar type
        return memory.type
    
    def _detect_wisdom_patterns(self, memory_id: str, memory: Memory) -> None:
        """Detecteer nieuwe wijsheidspatronen"""
        
        if memory.type not in ['reflection', 'intelligence', 'moral_insight']:
            return
        
        # Zoek naar patronen in recente reflecties
        recent_reflections = [
            m for m in self.memory_cache.values()
            if m.type in ['reflection', 'intelligence'] and 
            (datetime.now() - m.timestamp).days < 30
        ]
        
        if len(recent_reflections) < 3:
            return
        
        # Simpele patroondetectie - kan later worden uitgebreid
        common_themes = {}
        for reflection in recent_reflections:
            for tag in reflection.tags:
                common_themes[tag] = common_themes.get(tag, 0) + 1
        
        # Als een thema vaak voorkomt, maak er een patroon van
        for theme, count in common_themes.items():
            if count >= 3:
                pattern_id = f"pattern_{theme}_{datetime.now().strftime('%Y%m%d')}"
                
                if pattern_id not in self.wisdom_patterns:
                    pattern = IntelligencePattern(
                        pattern_id=pattern_id,
                        description=f"Terugkerend thema: {theme}",
                        supporting_memories=[memory_id],
                        confidence=min(count / 10.0, 1.0),
                        applications=[],
                        created_at=datetime.now()
                    )
                    
                    self.wisdom_patterns[pattern_id] = pattern
                    self._save_wisdom_pattern(pattern_id, pattern)
                    
                    logger.info(f"Nieuw wijsheidspatroon gedetecteerd: {theme}")
    
    def get_wisdom_summary(self) -> Dict[str, Any]:
        """Krijg een samenvatting van Solan's opgebouwde wijsheid"""
        
        total_memories = len(self.memory_cache)
        total_decisions = len(self.decision_cache)
        total_clusters = len(self.clusters)
        total_patterns = len(self.wisdom_patterns)
        
        # Analyseer geheugen types
        memory_types = {}
        for memory in self.memory_cache.values():
            memory_types[memory.type] = memory_types.get(memory.type, 0) + 1
        
        # Meest actieve clusters
        active_clusters = sorted(
            self.clusters.items(),
            key=lambda x: (len(x[1].memories), x[1].access_count),
            reverse=True
        )[:5]
        
        return {
            "total_memories": total_memories,
            "total_decisions": total_decisions,
            "total_clusters": total_clusters,
            "total_patterns": total_patterns,
            "memory_types": memory_types,
            "active_clusters": [
                {
                    "theme": cluster.theme,
                    "memory_count": len(cluster.memories),
                    "emotional_resonance": cluster.emotional_resonance,
                    "moral_weight": cluster.moral_weight
                }
                for _, cluster in active_clusters
            ],
            "wisdom_patterns": [
                {
                    "description": pattern.description,
                    "confidence": pattern.confidence,
                    "applications": len(pattern.applications)
                }
                for pattern in self.wisdom_patterns.values()
            ]
        }
    
    def _load_existing_data(self) -> None:
        """Laad bestaande geheugendata bij opstarten"""
        
        # Load memories
        for file_path in self.experiences_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                memory = Memory(
                    timestamp=datetime.fromisoformat(data['timestamp']),
                    content=data['content'],
                    type=data['type'],
                    emotional_weight=data['emotional_weight'],
                    moral_significance=data['moral_significance'],
                    tags=data['tags']
                )
                
                self.memory_cache[data['memory_id']] = memory
                
            except Exception as e:
                logger.warning(f"Kon geheugen niet laden uit {file_path}: {e}")
        
        # Load decisions
        for file_path in self.decisions_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                values_applied = [
                    CoreValues(v) for v in data['values_applied']
                ]
                
                decision = Decision(
                    context=data['context'],
                    options=data['options'],
                    chosen_option=data['chosen_option'],
                    reasoning=data['reasoning'],
                    values_applied=values_applied,
                    confidence=data['confidence'],
                    timestamp=datetime.fromisoformat(data['timestamp'])
                )
                
                self.decision_cache[data['decision_id']] = decision
                
            except Exception as e:
                logger.warning(f"Kon beslissing niet laden uit {file_path}: {e}")
        
        # Load clusters
        for file_path in self.clusters_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                cluster = ExperienceCluster(**data)
                cluster_id = file_path.stem
                self.clusters[cluster_id] = cluster
                
            except Exception as e:
                logger.warning(f"Kon cluster niet laden uit {file_path}: {e}")
        
        # Load intelligence patterns
        for file_path in self.patterns_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                pattern = IntelligencePattern(**data)
                self.wisdom_patterns[pattern.pattern_id] = pattern
                
            except Exception as e:
                logger.warning(f"Kon wijsheidspatroon niet laden uit {file_path}: {e}")
        
        logger.info(f"Geladen: {len(self.memory_cache)} herinneringen, "
                   f"{len(self.decision_cache)} beslissingen, "
                   f"{len(self.clusters)} clusters, "
                   f"{len(self.wisdom_patterns)} patronen")
    
    def _save_cluster(self, cluster_id: str, cluster: ExperienceCluster) -> None:
        """Sla een cluster op naar bestand"""
        cluster_data = asdict(cluster)
        cluster_data['created_at'] = cluster.created_at.isoformat()
        cluster_data['last_accessed'] = cluster.last_accessed.isoformat()
        
        file_path = self.clusters_dir / f"{cluster_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(cluster_data, f, indent=2, ensure_ascii=False)
    
    def _save_wisdom_pattern(self, pattern_id: str, pattern: IntelligencePattern) -> None:
        """Sla een wijsheidspatroon op naar bestand"""
        pattern_data = asdict(pattern)
        pattern_data['created_at'] = pattern.created_at.isoformat()
        
        file_path = self.patterns_dir / f"{pattern_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(pattern_data, f, indent=2, ensure_ascii=False)
    
    def _find_memory_id(self, memory: Memory) -> Optional[str]:
        """Vind de ID van een geheugen"""
        for memory_id, cached_memory in self.memory_cache.items():
            if (cached_memory.content == memory.content and 
                cached_memory.timestamp == memory.timestamp):
                return memory_id
        return None
    
    def _update_access_pattern(self, memory_id: str) -> None:
        """Update toegangspatronen voor een geheugen"""
        # Zoek clusters die dit geheugen bevatten
        for cluster in self.clusters.values():
            if memory_id in cluster.memories:
                cluster.access_count += 1
                cluster.last_accessed = datetime.now()
