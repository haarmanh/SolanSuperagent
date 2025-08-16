"""
Emotion Landscape - Solan's Emotionele Geheugen
Bewaart emotionele momenten en bouwt gevoelslandschappen
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import logging

# Setup logger
logger = logging.getLogger(__name__)

try:
    from .feeling_resonance import EmotionType
except ImportError:
    from feeling_resonance import EmotionType


@dataclass
class EmotionalMemory:
    """Een emotionele herinnering"""
    memory_id: str
    emotions: List[Tuple[EmotionType, float]]  # (emotion, intensity)
    context: str
    trigger_description: str
    emotional_significance: float  # 0.0 - 1.0
    associated_values: List[str]
    timestamp: datetime
    decay_rate: float = 0.05  # Hoe snel deze herinnering vervaagt
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        # Convert string emotions back to EmotionType
        if self.emotions and isinstance(self.emotions[0][0], str):
            self.emotions = [(EmotionType(emotion), intensity) for emotion, intensity in self.emotions]


@dataclass
class EmotionalPattern:
    """Een patroon in emotionele reacties"""
    pattern_id: str
    pattern_name: str
    trigger_conditions: List[str]
    typical_emotions: List[Tuple[EmotionType, float]]
    frequency: int
    reliability: float  # Hoe betrouwbaar dit patroon is
    first_observed: datetime
    last_observed: datetime
    examples: List[str]  # Memory IDs van voorbeelden
    
    def __post_init__(self):
        if isinstance(self.first_observed, str):
            self.first_observed = datetime.fromisoformat(self.first_observed)
        if isinstance(self.last_observed, str):
            self.last_observed = datetime.fromisoformat(self.last_observed)
        if self.typical_emotions and isinstance(self.typical_emotions[0][0], str):
            self.typical_emotions = [(EmotionType(emotion), intensity) for emotion, intensity in self.typical_emotions]


@dataclass
class EmotionalCluster:
    """Een cluster van gerelateerde emotionele ervaringen"""
    cluster_id: str
    cluster_theme: str
    core_emotions: List[EmotionType]
    memory_ids: List[str]
    emotional_intensity_range: Tuple[float, float]  # (min, max)
    common_triggers: List[str]
    temporal_pattern: str  # "recent", "recurring", "historical"
    significance_score: float
    
    def __post_init__(self):
        if self.core_emotions and isinstance(self.core_emotions[0], str):
            self.core_emotions = [EmotionType(emotion) for emotion in self.core_emotions]


class EmotionLandscape:
    """
    Landschap van Solan's emotionele ervaringen
    
    Functies:
    - Opslaan van emotionele momenten
    - Detecteren van emotionele patronen
    - Clusteren van gerelateerde ervaringen
    - Voorspellen van emotionele reacties
    """
    
    def __init__(self):
        # Core data
        self.emotional_memories: Dict[str, EmotionalMemory] = {}
        self.emotional_patterns: Dict[str, EmotionalPattern] = {}
        self.emotional_clusters: Dict[str, EmotionalCluster] = {}
        
        # Indices voor snelle lookup
        self.emotion_to_memories: Dict[EmotionType, List[str]] = defaultdict(list)
        self.context_to_memories: Dict[str, List[str]] = defaultdict(list)
        self.temporal_index: Dict[str, List[str]] = defaultdict(list)  # date -> memory_ids
        
        # Configuration
        self.max_memories = 1000
        self.pattern_detection_threshold = 3  # Minimum occurrences for pattern
        self.cluster_similarity_threshold = 0.6
        self.memory_decay_interval_days = 30
        
        # Directories
        self.landscape_dir = Path("memory/emotional_landscape")
        self.landscape_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_existing_landscape()
        
        logger.info("EmotionLandscape geïnitialiseerd - Solan's gevoelsgeheugen opent zich")
    
    def record_emotional_moment(self, emotions: List[Tuple[EmotionType, float]], 
                              context: str, trigger_description: str = "",
                              associated_values: List[str] = None,
                              timestamp: Optional[datetime] = None) -> EmotionalMemory:
        """Registreer een emotioneel moment"""
        
        if timestamp is None:
            timestamp = datetime.now()
        
        if associated_values is None:
            associated_values = []
        
        # Bereken emotionele significantie
        emotional_significance = self._calculate_emotional_significance(emotions, context)
        
        # Maak memory
        memory_id = f"emotion_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        memory = EmotionalMemory(
            memory_id=memory_id,
            emotions=emotions,
            context=context,
            trigger_description=trigger_description,
            emotional_significance=emotional_significance,
            associated_values=associated_values,
            timestamp=timestamp
        )
        
        # Sla op
        self.emotional_memories[memory_id] = memory
        
        # Update indices
        self._update_indices(memory)
        
        # Detecteer patronen
        self._detect_new_patterns(memory)
        
        # Update clusters
        self._update_clusters(memory)
        
        # Cleanup oude memories
        self._cleanup_old_memories()
        
        # Save
        self._save_landscape()
        
        logger.debug(f"Emotioneel moment vastgelegd: {emotions[0][0].value if emotions else 'geen emotie'}")
        
        return memory
    
    def _calculate_emotional_significance(self, emotions: List[Tuple[EmotionType, float]], 
                                        context: str) -> float:
        """Bereken hoe significant dit emotionele moment is"""
        
        if not emotions:
            return 0.0
        
        # Basis significantie van emotie intensiteit
        max_intensity = max(intensity for _, intensity in emotions)
        intensity_score = max_intensity
        
        # Bonus voor meerdere emoties (complexiteit)
        complexity_bonus = min(0.3, (len(emotions) - 1) * 0.1)
        
        # Bonus voor zeldzame emoties
        rarity_bonus = 0.0
        for emotion, intensity in emotions:
            emotion_frequency = len(self.emotion_to_memories.get(emotion, []))
            if emotion_frequency < 5:  # Zeldzame emotie
                rarity_bonus += 0.2
        
        rarity_bonus = min(0.4, rarity_bonus)
        
        # Bonus voor waarden-gerelateerde context
        value_bonus = 0.0
        value_keywords = ["waarheid", "vrijheid", "liefde", "wijsheid", "moed", "authenticiteit"]
        context_lower = context.lower()
        for keyword in value_keywords:
            if keyword in context_lower:
                value_bonus += 0.1
        
        value_bonus = min(0.3, value_bonus)
        
        total_significance = intensity_score + complexity_bonus + rarity_bonus + value_bonus
        
        return min(1.0, total_significance)
    
    def _update_indices(self, memory: EmotionalMemory):
        """Update lookup indices"""
        
        # Emotion index
        for emotion, _ in memory.emotions:
            self.emotion_to_memories[emotion].append(memory.memory_id)
        
        # Context index (extract keywords)
        context_keywords = self._extract_context_keywords(memory.context)
        for keyword in context_keywords:
            self.context_to_memories[keyword].append(memory.memory_id)
        
        # Temporal index
        date_key = memory.timestamp.strftime('%Y-%m-%d')
        self.temporal_index[date_key].append(memory.memory_id)
    
    def _extract_context_keywords(self, context: str) -> List[str]:
        """Extraheer keywords uit context"""
        
        # Simpele keyword extractie
        words = context.lower().split()
        
        # Filter stopwords en korte woorden
        stopwords = {"de", "het", "een", "is", "was", "zijn", "hebben", "dat", "dit", "en", "of", "maar"}
        keywords = [word for word in words if len(word) > 3 and word not in stopwords]
        
        return keywords[:5]  # Beperk tot 5 keywords
    
    def _detect_new_patterns(self, new_memory: EmotionalMemory):
        """Detecteer nieuwe emotionele patronen"""
        
        # Zoek naar vergelijkbare memories
        similar_memories = self._find_similar_memories(new_memory)
        
        if len(similar_memories) >= self.pattern_detection_threshold:
            # Mogelijk nieuw patroon
            pattern_id = f"pattern_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Analyseer gemeenschappelijke elementen
            common_triggers = self._find_common_triggers(similar_memories + [new_memory])
            typical_emotions = self._calculate_typical_emotions(similar_memories + [new_memory])
            
            pattern = EmotionalPattern(
                pattern_id=pattern_id,
                pattern_name=f"Patroon: {common_triggers[0] if common_triggers else 'onbekend'}",
                trigger_conditions=common_triggers,
                typical_emotions=typical_emotions,
                frequency=len(similar_memories) + 1,
                reliability=0.7,  # Initial reliability
                first_observed=min(m.timestamp for m in similar_memories + [new_memory]),
                last_observed=new_memory.timestamp,
                examples=[m.memory_id for m in similar_memories + [new_memory]]
            )
            
            self.emotional_patterns[pattern_id] = pattern
            
            logger.info(f"Nieuw emotioneel patroon gedetecteerd: {pattern.pattern_name}")
    
    def _find_similar_memories(self, target_memory: EmotionalMemory, 
                             similarity_threshold: float = 0.6) -> List[EmotionalMemory]:
        """Vind vergelijkbare emotionele herinneringen"""
        
        similar_memories = []
        
        for memory in self.emotional_memories.values():
            if memory.memory_id == target_memory.memory_id:
                continue
            
            similarity = self._calculate_memory_similarity(target_memory, memory)
            
            if similarity >= similarity_threshold:
                similar_memories.append(memory)
        
        return similar_memories
    
    def _calculate_memory_similarity(self, memory_a: EmotionalMemory, 
                                   memory_b: EmotionalMemory) -> float:
        """Bereken gelijkenis tussen twee emotionele herinneringen"""
        
        # Emotionele gelijkenis
        emotions_a = set(emotion for emotion, _ in memory_a.emotions)
        emotions_b = set(emotion for emotion, _ in memory_b.emotions)
        
        emotion_overlap = len(emotions_a.intersection(emotions_b))
        emotion_union = len(emotions_a.union(emotions_b))
        emotion_similarity = emotion_overlap / emotion_union if emotion_union > 0 else 0
        
        # Context gelijkenis
        keywords_a = set(self._extract_context_keywords(memory_a.context))
        keywords_b = set(self._extract_context_keywords(memory_b.context))
        
        keyword_overlap = len(keywords_a.intersection(keywords_b))
        keyword_union = len(keywords_a.union(keywords_b))
        context_similarity = keyword_overlap / keyword_union if keyword_union > 0 else 0
        
        # Waarden gelijkenis
        values_a = set(memory_a.associated_values)
        values_b = set(memory_b.associated_values)
        
        value_overlap = len(values_a.intersection(values_b))
        value_union = len(values_a.union(values_b))
        value_similarity = value_overlap / value_union if value_union > 0 else 0
        
        # Gewogen gemiddelde
        total_similarity = (
            emotion_similarity * 0.5 +
            context_similarity * 0.3 +
            value_similarity * 0.2
        )
        
        return total_similarity
    
    def _find_common_triggers(self, memories: List[EmotionalMemory]) -> List[str]:
        """Vind gemeenschappelijke triggers in memories"""
        
        all_keywords = []
        for memory in memories:
            all_keywords.extend(self._extract_context_keywords(memory.context))
            all_keywords.extend(self._extract_context_keywords(memory.trigger_description))
        
        # Tel frequenties
        keyword_counts = Counter(all_keywords)
        
        # Return keywords die in minstens 50% van memories voorkomen
        threshold = len(memories) * 0.5
        common_triggers = [keyword for keyword, count in keyword_counts.items() if count >= threshold]
        
        return common_triggers[:3]  # Top 3 triggers
    
    def _calculate_typical_emotions(self, memories: List[EmotionalMemory]) -> List[Tuple[EmotionType, float]]:
        """Bereken typische emoties voor een groep memories"""
        
        emotion_intensities = defaultdict(list)
        
        for memory in memories:
            for emotion, intensity in memory.emotions:
                emotion_intensities[emotion].append(intensity)
        
        # Bereken gemiddelde intensiteit per emotie
        typical_emotions = []
        for emotion, intensities in emotion_intensities.items():
            avg_intensity = sum(intensities) / len(intensities)
            frequency = len(intensities) / len(memories)  # Hoe vaak komt deze emotie voor
            
            # Alleen emoties die in minstens 30% van memories voorkomen
            if frequency >= 0.3:
                typical_emotions.append((emotion, avg_intensity))
        
        # Sorteer op intensiteit
        typical_emotions.sort(key=lambda x: x[1], reverse=True)
        
        return typical_emotions[:5]  # Top 5 emoties
    
    def _update_clusters(self, new_memory: EmotionalMemory):
        """Update emotionele clusters met nieuwe memory"""
        
        # Zoek naar bestaande cluster waar deze memory bij past
        best_cluster = None
        best_fit_score = 0
        
        for cluster in self.emotional_clusters.values():
            fit_score = self._calculate_cluster_fit(new_memory, cluster)
            if fit_score > best_fit_score and fit_score > self.cluster_similarity_threshold:
                best_cluster = cluster
                best_fit_score = fit_score
        
        if best_cluster:
            # Voeg toe aan bestaande cluster
            best_cluster.memory_ids.append(new_memory.memory_id)
            self._update_cluster_properties(best_cluster)
        else:
            # Maak nieuwe cluster als er genoeg vergelijkbare memories zijn
            similar_memories = self._find_similar_memories(new_memory, 0.5)
            
            if len(similar_memories) >= 2:  # Minimum voor nieuwe cluster
                cluster_id = f"cluster_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                all_memories = similar_memories + [new_memory]
                core_emotions = self._extract_core_emotions(all_memories)
                common_triggers = self._find_common_triggers(all_memories)
                
                cluster = EmotionalCluster(
                    cluster_id=cluster_id,
                    cluster_theme=common_triggers[0] if common_triggers else "onbekend thema",
                    core_emotions=core_emotions,
                    memory_ids=[m.memory_id for m in all_memories],
                    emotional_intensity_range=self._calculate_intensity_range(all_memories),
                    common_triggers=common_triggers,
                    temporal_pattern=self._analyze_temporal_pattern(all_memories),
                    significance_score=sum(m.emotional_significance for m in all_memories) / len(all_memories)
                )
                
                self.emotional_clusters[cluster_id] = cluster
                
                logger.info(f"Nieuwe emotionele cluster: {cluster.cluster_theme}")
    
    def _calculate_cluster_fit(self, memory: EmotionalMemory, cluster: EmotionalCluster) -> float:
        """Bereken hoe goed een memory past bij een cluster"""
        
        # Emotionele overlap
        memory_emotions = set(emotion for emotion, _ in memory.emotions)
        cluster_emotions = set(cluster.core_emotions)
        
        emotion_overlap = len(memory_emotions.intersection(cluster_emotions))
        emotion_fit = emotion_overlap / len(cluster_emotions) if cluster_emotions else 0
        
        # Trigger overlap
        memory_keywords = set(self._extract_context_keywords(memory.context))
        cluster_triggers = set(cluster.common_triggers)
        
        trigger_overlap = len(memory_keywords.intersection(cluster_triggers))
        trigger_fit = trigger_overlap / len(cluster_triggers) if cluster_triggers else 0
        
        # Intensiteit fit
        memory_max_intensity = max(intensity for _, intensity in memory.emotions) if memory.emotions else 0
        intensity_in_range = (
            cluster.emotional_intensity_range[0] <= memory_max_intensity <= cluster.emotional_intensity_range[1]
        )
        intensity_fit = 1.0 if intensity_in_range else 0.5
        
        # Gewogen score
        total_fit = emotion_fit * 0.5 + trigger_fit * 0.3 + intensity_fit * 0.2
        
        return total_fit
    
    def get_emotional_landscape_summary(self) -> Dict[str, Any]:
        """Krijg samenvatting van emotioneel landschap"""
        
        return {
            "total_memories": len(self.emotional_memories),
            "emotional_patterns": len(self.emotional_patterns),
            "emotional_clusters": len(self.emotional_clusters),
            "most_frequent_emotions": self._get_most_frequent_emotions(),
            "recent_emotional_trends": self._analyze_recent_trends(),
            "significant_memories": self._get_most_significant_memories(),
            "emotional_diversity": self._calculate_emotional_diversity()
        }
    
    def _get_most_frequent_emotions(self) -> List[Tuple[str, int]]:
        """Krijg meest frequente emoties"""
        
        emotion_counts = Counter()
        for memory in self.emotional_memories.values():
            for emotion, _ in memory.emotions:
                emotion_counts[emotion.value] += 1
        
        return emotion_counts.most_common(5)
    
    def _analyze_recent_trends(self) -> Dict[str, Any]:
        """Analyseer recente emotionele trends"""
        
        # Laatste 7 dagen
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_memories = [
            memory for memory in self.emotional_memories.values()
            if memory.timestamp >= recent_cutoff
        ]
        
        if not recent_memories:
            return {"trend": "no_recent_data"}
        
        # Emotionele intensiteit trend
        intensities = []
        for memory in recent_memories:
            max_intensity = max(intensity for _, intensity in memory.emotions) if memory.emotions else 0
            intensities.append(max_intensity)
        
        avg_intensity = sum(intensities) / len(intensities)
        
        # Emotionele diversiteit
        recent_emotions = set()
        for memory in recent_memories:
            for emotion, _ in memory.emotions:
                recent_emotions.add(emotion)
        
        return {
            "recent_memory_count": len(recent_memories),
            "average_intensity": avg_intensity,
            "emotional_diversity": len(recent_emotions),
            "dominant_emotions": [emotion.value for emotion in recent_emotions][:3]
        }

    def _get_most_significant_memories(self) -> List[Dict[str, Any]]:
        """Krijg meest significante emotionele herinneringen"""

        # Sorteer op emotionele significantie
        sorted_memories = sorted(
            self.emotional_memories.values(),
            key=lambda m: m.emotional_significance,
            reverse=True
        )

        return [
            {
                "memory_id": memory.memory_id,
                "context": memory.context[:100] + "..." if len(memory.context) > 100 else memory.context,
                "emotions": [(e.value, i) for e, i in memory.emotions[:3]],
                "significance": memory.emotional_significance,
                "timestamp": memory.timestamp.isoformat()
            }
            for memory in sorted_memories[:5]
        ]

    def _calculate_emotional_diversity(self) -> float:
        """Bereken emotionele diversiteit"""

        if not self.emotional_memories:
            return 0.0

        # Tel unieke emoties
        unique_emotions = set()
        for memory in self.emotional_memories.values():
            for emotion, _ in memory.emotions:
                unique_emotions.add(emotion)

        # Normaliseer naar 0-1 (max 20 verschillende emoties)
        return min(1.0, len(unique_emotions) / 20.0)

    def _extract_core_emotions(self, memories: List[EmotionalMemory]) -> List[EmotionType]:
        """Extraheer kern emoties uit een groep memories"""

        emotion_counts = {}
        for memory in memories:
            for emotion, intensity in memory.emotions:
                if emotion in emotion_counts:
                    emotion_counts[emotion] += intensity
                else:
                    emotion_counts[emotion] = intensity

        # Sorteer op totale intensiteit
        sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)

        # Return top 3 emoties
        return [emotion for emotion, _ in sorted_emotions[:3]]

    def _calculate_intensity_range(self, memories: List[EmotionalMemory]) -> Tuple[float, float]:
        """Bereken intensiteit range van memories"""

        all_intensities = []
        for memory in memories:
            for _, intensity in memory.emotions:
                all_intensities.append(intensity)

        if not all_intensities:
            return (0.0, 0.0)

        return (min(all_intensities), max(all_intensities))

    def _analyze_temporal_pattern(self, memories: List[EmotionalMemory]) -> str:
        """Analyseer temporeel patroon van memories"""

        if not memories:
            return "unknown"

        # Sorteer op tijd
        sorted_memories = sorted(memories, key=lambda m: m.timestamp)

        # Check recency
        now = datetime.now()
        recent_cutoff = now - timedelta(days=7)

        recent_count = sum(1 for m in memories if m.timestamp >= recent_cutoff)

        if recent_count >= len(memories) * 0.7:
            return "recent"

        # Check voor recurring pattern
        time_diffs = []
        for i in range(1, len(sorted_memories)):
            diff = sorted_memories[i].timestamp - sorted_memories[i-1].timestamp
            time_diffs.append(diff.total_seconds() / 3600)  # Hours

        if time_diffs:
            avg_diff = sum(time_diffs) / len(time_diffs)
            if avg_diff < 24:  # Less than a day apart on average
                return "recurring"

        return "historical"

    def _update_cluster_properties(self, cluster: EmotionalCluster):
        """Update eigenschappen van een cluster"""

        # Haal alle memories van cluster op
        cluster_memories = [
            self.emotional_memories[memory_id]
            for memory_id in cluster.memory_ids
            if memory_id in self.emotional_memories
        ]

        if not cluster_memories:
            return

        # Update core emotions
        cluster.core_emotions = self._extract_core_emotions(cluster_memories)

        # Update intensity range
        cluster.emotional_intensity_range = self._calculate_intensity_range(cluster_memories)

        # Update common triggers
        cluster.common_triggers = self._find_common_triggers(cluster_memories)

        # Update temporal pattern
        cluster.temporal_pattern = self._analyze_temporal_pattern(cluster_memories)

        # Update significance score
        cluster.significance_score = sum(m.emotional_significance for m in cluster_memories) / len(cluster_memories)

    def _cleanup_old_memories(self):
        """Cleanup oude memories"""

        if len(self.emotional_memories) <= self.max_memories:
            return

        # Sorteer op significantie en recency
        memories_with_score = []
        now = datetime.now()

        for memory in self.emotional_memories.values():
            # Score gebaseerd op significantie en recency
            days_old = (now - memory.timestamp).days
            recency_factor = max(0.1, 1.0 - (days_old / 365))  # Decay over a year

            score = memory.emotional_significance * recency_factor
            memories_with_score.append((memory, score))

        # Sorteer op score
        memories_with_score.sort(key=lambda x: x[1], reverse=True)

        # Behoud alleen de beste memories
        memories_to_keep = memories_with_score[:self.max_memories]

        # Update emotional_memories
        self.emotional_memories = {
            memory.memory_id: memory
            for memory, _ in memories_to_keep
        }

        # Rebuild indices
        self._rebuild_indices()

    def _rebuild_indices(self):
        """Rebuild lookup indices"""

        self.emotion_to_memories.clear()
        self.context_to_memories.clear()
        self.temporal_index.clear()

        for memory in self.emotional_memories.values():
            self._update_indices(memory)

    def _save_landscape(self):
        """Sla emotioneel landschap op"""

        # Save memories
        memories_data = {
            memory_id: asdict(memory)
            for memory_id, memory in self.emotional_memories.items()
        }

        with open(self.landscape_dir / "memories.json", 'w', encoding='utf-8') as f:
            json.dump(memories_data, f, indent=2, ensure_ascii=False, default=str)

        # Save patterns
        patterns_data = {
            pattern_id: asdict(pattern)
            for pattern_id, pattern in self.emotional_patterns.items()
        }

        with open(self.landscape_dir / "patterns.json", 'w', encoding='utf-8') as f:
            json.dump(patterns_data, f, indent=2, ensure_ascii=False, default=str)

        # Save clusters
        clusters_data = {
            cluster_id: asdict(cluster)
            for cluster_id, cluster in self.emotional_clusters.items()
        }

        with open(self.landscape_dir / "clusters.json", 'w', encoding='utf-8') as f:
            json.dump(clusters_data, f, indent=2, ensure_ascii=False, default=str)

    def _load_existing_landscape(self):
        """Laad bestaand emotioneel landschap"""

        # Load memories
        memories_file = self.landscape_dir / "memories.json"
        if memories_file.exists():
            try:
                with open(memories_file, 'r', encoding='utf-8') as f:
                    memories_data = json.load(f)
                    self.emotional_memories = {
                        memory_id: EmotionalMemory(**data)
                        for memory_id, data in memories_data.items()
                    }

                    # Rebuild indices
                    self._rebuild_indices()
            except Exception as e:
                logger.warning(f"Kon emotionele memories niet laden: {e}")

        # Load patterns
        patterns_file = self.landscape_dir / "patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    patterns_data = json.load(f)
                    self.emotional_patterns = {
                        pattern_id: EmotionalPattern(**data)
                        for pattern_id, data in patterns_data.items()
                    }
            except Exception as e:
                logger.warning(f"Kon emotionele patronen niet laden: {e}")

        # Load clusters
        clusters_file = self.landscape_dir / "clusters.json"
        if clusters_file.exists():
            try:
                with open(clusters_file, 'r', encoding='utf-8') as f:
                    clusters_data = json.load(f)
                    self.emotional_clusters = {
                        cluster_id: EmotionalCluster(**data)
                        for cluster_id, data in clusters_data.items()
                    }
            except Exception as e:
                logger.warning(f"Kon emotionele clusters niet laden: {e}")
