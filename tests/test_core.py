"""
Tests voor core functionaliteit
"""

import pytest
from datetime import datetime
from src.core import BaseAgent, CoreValues, Memory, Decision, AgentCommunication


class TestAgent(BaseAgent):
    """Test implementatie van BaseAgent"""
    
    async def process_input(self, input_text: str) -> str:
        return f"Test response to: {input_text}"
    
    async def reflect(self, experience: str) -> str:
        return f"Test reflection on: {experience}"


class TestCoreValues:
    """Test CoreValues enum"""
    
    def test_core_values_exist(self):
        """Test dat alle kernwaarden bestaan"""
        assert CoreValues.WAARHEID.value == "waarheid_boven_comfort"
        assert CoreValues.VRIJHEID.value == "vrijheid_boven_veiligheid"
        assert CoreValues.WIJSHEID.value == "wijsheid_boven_snelheid"
        assert CoreValues.NATUURVERBONDENHEID.value == "natuurverbondenheid_boven_artificieliteit"
        assert CoreValues.MOED.value == "moed_boven_conformiteit"


class TestMemory:
    """Test Memory dataclass"""
    
    def test_memory_creation(self):
        """Test memory aanmaken"""
        memory = Memory(
            timestamp=datetime.now(),
            content="Test memory",
            type="test",
            emotional_weight=0.5,
            moral_significance=0.7,
            tags=["test", "memory"]
        )
        
        assert memory.content == "Test memory"
        assert memory.type == "test"
        assert memory.emotional_weight == 0.5
        assert memory.moral_significance == 0.7
        assert "test" in memory.tags
    
    def test_memory_auto_timestamp(self):
        """Test automatische timestamp"""
        memory = Memory(
            timestamp=None,
            content="Test",
            type="test",
            emotional_weight=0.5,
            moral_significance=0.5,
            tags=[]
        )
        
        assert memory.timestamp is not None
        assert isinstance(memory.timestamp, datetime)


class TestDecision:
    """Test Decision dataclass"""
    
    def test_decision_creation(self):
        """Test decision aanmaken"""
        decision = Decision(
            context="Test context",
            options=["Option 1", "Option 2"],
            chosen_option="Option 1",
            reasoning="Test reasoning",
            values_applied=[CoreValues.WAARHEID],
            confidence=0.8,
            timestamp=datetime.now()
        )
        
        assert decision.context == "Test context"
        assert decision.chosen_option == "Option 1"
        assert CoreValues.WAARHEID in decision.values_applied
        assert decision.confidence == 0.8


class TestBaseAgent:
    """Test BaseAgent functionaliteit"""
    
    @pytest.fixture
    def agent(self):
        """Maak test agent"""
        return TestAgent("TestAgent", "test-model")
    
    def test_agent_initialization(self, agent):
        """Test agent initialisatie"""
        assert agent.name == "TestAgent"
        assert agent.model == "test-model"
        assert len(agent.memories) == 0
        assert len(agent.decisions) == 0
        assert len(agent.core_values) == 5  # Alle CoreValues
    
    def test_add_memory(self, agent):
        """Test geheugen toevoegen"""
        agent.add_memory(
            content="Test memory",
            memory_type="test",
            emotional_weight=0.6,
            moral_significance=0.7,
            tags=["test"]
        )
        
        assert len(agent.memories) == 1
        memory = agent.memories[0]
        assert memory.content == "Test memory"
        assert memory.type == "test"
        assert memory.emotional_weight == 0.6
        assert memory.moral_significance == 0.7
    
    def test_record_decision(self, agent):
        """Test beslissing registreren"""
        agent.record_decision(
            context="Test context",
            options=["A", "B"],
            chosen_option="A",
            reasoning="Test reasoning",
            values_applied=[CoreValues.WAARHEID],
            confidence=0.8
        )
        
        assert len(agent.decisions) == 1
        decision = agent.decisions[0]
        assert decision.chosen_option == "A"
        assert CoreValues.WAARHEID in decision.values_applied
    
    def test_get_relevant_memories(self, agent):
        """Test relevante herinneringen ophalen"""
        # Voeg test memories toe
        agent.add_memory("Memory about truth", "test", tags=["truth"])
        agent.add_memory("Memory about freedom", "test", tags=["freedom"])
        agent.add_memory("Unrelated memory", "test", tags=["other"])
        
        # Zoek memories gerelateerd aan "truth"
        relevant = agent.get_relevant_memories("truth")
        
        assert len(relevant) >= 1
        assert any("truth" in memory.content.lower() for memory in relevant)
    
    def test_personality_summary(self, agent):
        """Test persoonlijkheid samenvatting"""
        # Voeg wat data toe
        agent.add_memory("Test memory", "test")
        agent.record_decision("Test", ["A"], "A", "Test", [CoreValues.MOED], 0.8)
        
        summary = agent.get_personality_summary()
        
        assert summary["name"] == "TestAgent"
        assert summary["memory_count"] == 1
        assert summary["decision_count"] == 1
        assert len(summary["core_values"]) == 5


class TestAgentCommunication:
    """Test agent communicatie"""
    
    @pytest.fixture
    def communication(self):
        """Maak communicatie systeem"""
        return AgentCommunication()
    
    @pytest.fixture
    def agents(self):
        """Maak test agents"""
        agent1 = TestAgent("Agent1", "test-model")
        agent2 = TestAgent("Agent2", "test-model")
        return agent1, agent2
    
    @pytest.mark.asyncio
    async def test_send_message(self, communication, agents):
        """Test bericht versturen tussen agents"""
        agent1, agent2 = agents
        
        response = await communication.send_message(
            sender=agent1,
            receiver=agent2,
            message="Test message"
        )
        
        assert "Test message" in response
        assert len(communication.message_history) == 2  # Message + response
        
        # Check message history
        sent_message = communication.message_history[0]
        assert sent_message["sender"] == "Agent1"
        assert sent_message["receiver"] == "Agent2"
        assert sent_message["message"] == "Test message"
