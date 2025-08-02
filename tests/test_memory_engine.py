"""
Tests voor het dynamische geheugen systeem
"""

import pytest
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path

from src.memory_engine import MemoryEngine, ExperienceCluster, WisdomPattern
from src.core import Memory, Decision, CoreValues


class TestMemoryEngine:
    """Test MemoryEngine functionaliteit"""
    
    @pytest.fixture
    def temp_memory_dir(self):
        """Maak tijdelijke directory voor tests"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def memory_engine(self, temp_memory_dir):
        """Maak test memory engine"""
        return MemoryEngine(temp_memory_dir)
    
    def test_memory_engine_initialization(self, memory_engine):
        """Test memory engine initialisatie"""
        assert memory_engine.memory_dir.exists()
        assert memory_engine.experiences_dir.exists()
        assert memory_engine.reflections_dir.exists()
        assert memory_engine.decisions_dir.exists()
        assert memory_engine.patterns_dir.exists()
        assert memory_engine.clusters_dir.exists()
    
    def test_store_memory(self, memory_engine):
        """Test geheugen opslaan"""
        memory = Memory(
            timestamp=datetime.now(),
            content="Test memory content",
            type="test",
            emotional_weight=0.7,
            moral_significance=0.8,
            tags=["test", "memory"]
        )
        
        memory_id = memory_engine.store_memory(memory)
        
        assert memory_id.startswith("mem_")
        assert memory_id in memory_engine.memory_cache
        assert memory_engine.memory_cache[memory_id] == memory
        
        # Check dat bestand bestaat
        file_path = memory_engine.experiences_dir / f"{memory_id}.json"
        assert file_path.exists()
    
    def test_store_decision(self, memory_engine):
        """Test beslissing opslaan"""
        decision = Decision(
            context="Test context",
            options=["Option A", "Option B"],
            chosen_option="Option A",
            reasoning="Test reasoning",
            values_applied=[CoreValues.WAARHEID],
            confidence=0.8,
            timestamp=datetime.now()
        )
        
        decision_id = memory_engine.store_decision(decision)
        
        assert decision_id.startswith("dec_")
        assert decision_id in memory_engine.decision_cache
        assert memory_engine.decision_cache[decision_id] == decision
        
        # Check dat bestand bestaat
        file_path = memory_engine.decisions_dir / f"{decision_id}.json"
        assert file_path.exists()
    
    def test_retrieve_memories(self, memory_engine):
        """Test herinneringen ophalen"""
        # Voeg test memories toe
        memory1 = Memory(
            timestamp=datetime.now(),
            content="Memory about truth and honesty",
            type="reflection",
            emotional_weight=0.8,
            moral_significance=0.9,
            tags=["truth", "honesty"]
        )
        
        memory2 = Memory(
            timestamp=datetime.now(),
            content="Memory about freedom and choice",
            type="experience",
            emotional_weight=0.6,
            moral_significance=0.7,
            tags=["freedom", "choice"]
        )
        
        memory3 = Memory(
            timestamp=datetime.now(),
            content="Unrelated memory about weather",
            type="observation",
            emotional_weight=0.3,
            moral_significance=0.1,
            tags=["weather", "observation"]
        )
        
        memory_engine.store_memory(memory1)
        memory_engine.store_memory(memory2)
        memory_engine.store_memory(memory3)
        
        # Zoek memories gerelateerd aan "truth"
        relevant = memory_engine.retrieve_memories("truth", limit=5)
        
        assert len(relevant) >= 1
        assert any("truth" in memory.content.lower() for memory in relevant)
        
        # Zoek memories met type filter
        reflections = memory_engine.retrieve_memories(
            "truth", 
            limit=5, 
            memory_types=["reflection"]
        )
        
        assert all(memory.type == "reflection" for memory in reflections)
    
    def test_clustering(self, memory_engine):
        """Test experience clustering"""
        # Voeg gerelateerde memories toe
        for i in range(3):
            memory = Memory(
                timestamp=datetime.now() + timedelta(minutes=i),
                content=f"Memory about moral decisions {i}",
                type="reflection",
                emotional_weight=0.7,
                moral_significance=0.8,
                tags=["moral", "decision"]
            )
            memory_engine.store_memory(memory)
        
        # Check dat clusters zijn gemaakt
        assert len(memory_engine.clusters) >= 1
        
        # Check dat memories in clusters zitten
        total_clustered_memories = sum(
            len(cluster.memories) for cluster in memory_engine.clusters.values()
        )
        assert total_clustered_memories >= 3
    
    def test_wisdom_pattern_detection(self, memory_engine):
        """Test wijsheidspatroon detectie"""
        # Voeg meerdere reflecties toe met hetzelfde thema
        for i in range(4):
            memory = Memory(
                timestamp=datetime.now() + timedelta(minutes=i),
                content=f"Reflection on wisdom and learning {i}",
                type="reflection",
                emotional_weight=0.8,
                moral_significance=0.9,
                tags=["wisdom", "learning"]
            )
            memory_engine.store_memory(memory)
        
        # Check dat wijsheidspatronen zijn gedetecteerd
        assert len(memory_engine.wisdom_patterns) >= 1
        
        # Check patroon eigenschappen
        for pattern in memory_engine.wisdom_patterns.values():
            assert pattern.confidence > 0.0
            assert len(pattern.supporting_memories) > 0
    
    def test_persistence(self, temp_memory_dir):
        """Test dat data persistent wordt opgeslagen"""
        # Maak eerste memory engine en voeg data toe
        engine1 = MemoryEngine(temp_memory_dir)
        
        memory = Memory(
            timestamp=datetime.now(),
            content="Persistent test memory",
            type="test",
            emotional_weight=0.5,
            moral_significance=0.6,
            tags=["persistent", "test"]
        )
        
        memory_id = engine1.store_memory(memory)
        
        # Maak nieuwe memory engine met dezelfde directory
        engine2 = MemoryEngine(temp_memory_dir)
        
        # Check dat data is geladen
        assert memory_id in engine2.memory_cache
        assert engine2.memory_cache[memory_id].content == "Persistent test memory"
    
    def test_wisdom_summary(self, memory_engine):
        """Test wijsheid samenvatting"""
        # Voeg verschillende types memories toe
        memory_types = ["experience", "reflection", "wisdom", "decision"]
        
        for i, mem_type in enumerate(memory_types):
            memory = Memory(
                timestamp=datetime.now() + timedelta(minutes=i),
                content=f"Test {mem_type} content",
                type=mem_type,
                emotional_weight=0.5 + i * 0.1,
                moral_significance=0.6 + i * 0.1,
                tags=[mem_type, "test"]
            )
            memory_engine.store_memory(memory)
        
        summary = memory_engine.get_wisdom_summary()
        
        assert summary["total_memories"] == len(memory_types)
        assert summary["total_clusters"] >= 1
        assert "memory_types" in summary
        assert len(summary["memory_types"]) > 0


class TestExperienceCluster:
    """Test ExperienceCluster dataclass"""
    
    def test_cluster_creation(self):
        """Test cluster aanmaken"""
        cluster = ExperienceCluster(
            theme="test_theme",
            memories=["mem1", "mem2"],
            emotional_resonance=0.7,
            moral_weight=0.8,
            created_at=datetime.now(),
            last_accessed=datetime.now()
        )
        
        assert cluster.theme == "test_theme"
        assert len(cluster.memories) == 2
        assert cluster.access_count == 0
    
    def test_cluster_datetime_parsing(self):
        """Test datetime parsing van strings"""
        now = datetime.now()
        
        cluster = ExperienceCluster(
            theme="test",
            memories=["mem1"],
            emotional_resonance=0.5,
            moral_weight=0.6,
            created_at=now.isoformat(),
            last_accessed=now.isoformat()
        )
        
        assert isinstance(cluster.created_at, datetime)
        assert isinstance(cluster.last_accessed, datetime)


class TestWisdomPattern:
    """Test WisdomPattern dataclass"""
    
    def test_pattern_creation(self):
        """Test patroon aanmaken"""
        pattern = WisdomPattern(
            pattern_id="test_pattern",
            description="Test pattern description",
            supporting_memories=["mem1", "mem2"],
            confidence=0.8,
            applications=["app1"],
            created_at=datetime.now()
        )
        
        assert pattern.pattern_id == "test_pattern"
        assert pattern.confidence == 0.8
        assert len(pattern.supporting_memories) == 2
    
    def test_pattern_datetime_parsing(self):
        """Test datetime parsing van strings"""
        now = datetime.now()
        
        pattern = WisdomPattern(
            pattern_id="test",
            description="Test",
            supporting_memories=["mem1"],
            confidence=0.5,
            applications=[],
            created_at=now.isoformat()
        )
        
        assert isinstance(pattern.created_at, datetime)
