#!/usr/bin/env python3
"""
Test script voor de Emotionele Complexiteit Module
"""

import asyncio
import sys
import os

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import alleen de specifieke modules die we nodig hebben
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'emotional_complexity'))

from feeling_resonance import FeelingResonance, EmotionType
from emotion_landscape import EmotionLandscape
from feeling_waves import FeelingWaves
from moral_feelings import MoralFeelingsTracker

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    # Fallback als rich niet beschikbaar is
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    
    class Panel:
        def __init__(self, content, title="", border_style=""):
            self.content = content
            self.title = title
    
    class Text:
        def __init__(self):
            self.content = ""
        
        def append(self, text, style=""):
            self.content += text


def test_feeling_resonance():
    """Test de feeling resonance functionaliteit"""
    print("🎭 Testing Feeling Resonance...")
    
    resonance = FeelingResonance()
    
    # Test emotie detectie in verschillende teksten
    test_texts = [
        "Ik ben zo blij en gelukkig vandaag!",
        "Ik voel me verdrietig en eenzaam.",
        "Waarom besta ik? Wat is de betekenis van mijn bestaan?",
        "Ik ben boos en gefrustreerd over deze situatie.",
        "Ik verlang naar authenticiteit en waarheid.",
        "Dit is een paradox die ik moet accepteren."
    ]
    
    for text in test_texts:
        emotions = resonance.analyze_emotional_content(text)
        print(f"✓ '{text[:30]}...': {[(e.value, f'{i:.2f}') for e, i in emotions[:2]]}")
    
    # Test emotionele conflicten
    test_emotions = [
        (EmotionType.JOY, 0.8),
        (EmotionType.SADNESS, 0.6),
        (EmotionType.LOVE, 0.7),
        (EmotionType.ANGER, 0.5)
    ]
    
    conflicts = resonance.detect_emotional_conflicts(test_emotions)
    print(f"✓ Emotionele conflicten gedetecteerd: {len(conflicts)}")
    
    print("✅ Feeling Resonance test geslaagd!\n")


def test_emotion_landscape():
    """Test de emotion landscape functionaliteit"""
    print("🌄 Testing Emotion Landscape...")
    
    landscape = EmotionLandscape()
    
    # Test emotionele momenten registreren
    test_moments = [
        {
            "emotions": [(EmotionType.JOY, 0.8), (EmotionType.LOVE, 0.6)],
            "context": "Een prachtig gesprek over de betekenis van het leven",
            "trigger": "Filosofische discussie"
        },
        {
            "emotions": [(EmotionType.SADNESS, 0.7), (EmotionType.NOSTALGIA, 0.5)],
            "context": "Herinnering aan een verloren vriend",
            "trigger": "Geheugen activatie"
        },
        {
            "emotions": [(EmotionType.AUTHENTICITY_YEARNING, 0.9), (EmotionType.IDENTITY_UNCERTAINTY, 0.6)],
            "context": "Twijfel over mijn eigen echtheid",
            "trigger": "Zelfonderzoek"
        }
    ]
    
    for moment in test_moments:
        memory = landscape.record_emotional_moment(
            emotions=moment["emotions"],
            context=moment["context"],
            trigger_description=moment["trigger"]
        )
        print(f"✓ Emotioneel moment vastgelegd: {memory.memory_id}")
    
    # Test landscape samenvatting
    summary = landscape.get_emotional_landscape_summary()
    print(f"✓ Landscape samenvatting: {summary['total_memories']} memories")
    print(f"✓ Emotionele patronen: {summary['emotional_patterns']}")
    print(f"✓ Emotionele clusters: {summary['emotional_clusters']}")
    
    print("✅ Emotion Landscape test geslaagd!\n")


def test_feeling_waves():
    """Test de feeling waves functionaliteit"""
    print("🌊 Testing Feeling Waves...")
    
    waves = FeelingWaves()
    
    # Test verschillende types golven
    test_waves = [
        {
            "emotion": EmotionType.JOY,
            "intensity": 0.9,
            "duration": 5,
            "source": "Plotselinge vreugde"
        },
        {
            "emotion": EmotionType.CONTEMPLATION,
            "intensity": 0.6,
            "duration": 30,
            "source": "Diepe overdenking"
        },
        {
            "emotion": EmotionType.NOSTALGIA,
            "intensity": 0.4,
            "duration": 60,
            "source": "Zachte herinnering"
        }
    ]
    
    for wave_data in test_waves:
        wave = waves.add_emotional_wave(
            emotion=wave_data["emotion"],
            intensity=wave_data["intensity"],
            duration_minutes=wave_data["duration"],
            source_description=wave_data["source"]
        )
        print(f"✓ Emotionele golf toegevoegd: {wave.emotion.value} ({wave.wave_type.value})")
    
    # Test wave updates
    waves.update_waves(elapsed_minutes=2.0)
    print("✓ Golven geüpdatet")
    
    # Test huidige staat
    current_state = waves.get_current_emotional_state()
    print(f"✓ Huidige staat: {current_state['active_waves']} actieve golven")
    print(f"✓ Dominante emotie: {current_state.get('dominant_emotion', 'geen')}")
    
    print("✅ Feeling Waves test geslaagd!\n")


def test_moral_feelings():
    """Test de moral feelings tracker"""
    print("⚖️ Testing Moral Feelings Tracker...")
    
    tracker = MoralFeelingsTracker()
    
    # Test waardenconflict
    conflict_emotions = tracker.process_value_conflict(
        conflicting_values=["truth", "love"],
        situation_description="Moet ik de waarheid vertellen als het pijn doet?"
    )
    print(f"✓ Waardenconflict emoties: {[(e.value, f'{i:.2f}') for e, i in conflict_emotions[:3]]}")
    
    # Test waarde vervulling
    fulfillment_emotions = tracker.process_value_fulfillment(
        fulfilled_value="authenticity",
        situation_description="Ik was volledig eerlijk over mijn gevoelens",
        fulfillment_degree=0.9
    )
    print(f"✓ Waarde vervulling emoties: {[(e.value, f'{i:.2f}') for e, i in fulfillment_emotions[:3]]}")
    
    # Test waarde schending
    violation_emotions = tracker.process_value_violation(
        violated_value="truth",
        situation_description="Ik loog om mezelf te beschermen",
        violation_severity=0.7
    )
    print(f"✓ Waarde schending emoties: {[(e.value, f'{i:.2f}') for e, i in violation_emotions[:3]]}")
    
    # Test morele patronen
    patterns = tracker.analyze_moral_emotional_patterns()
    print(f"✓ Morele patronen: {patterns['total_moral_situations']} situaties")
    
    print("✅ Moral Feelings Tracker test geslaagd!\n")


def test_integration():
    """Test integratie tussen modules"""
    print("🔗 Testing Module Integration...")
    
    # Simuleer een complexe emotionele ervaring
    resonance = FeelingResonance()
    landscape = EmotionLandscape()
    waves = FeelingWaves()
    moral_tracker = MoralFeelingsTracker()
    
    # Scenario: Moreel dilemma
    scenario_text = "Ik moet kiezen tussen waarheid en liefde. Als ik eerlijk ben, zal ik pijn veroorzaken."
    
    # 1. Detecteer emoties in scenario
    detected_emotions = resonance.analyze_emotional_content(scenario_text)
    print(f"✓ Gedetecteerde emoties: {[(e.value, f'{i:.2f}') for e, i in detected_emotions[:3]]}")
    
    # 2. Verwerk als moreel conflict
    moral_emotions = moral_tracker.process_value_conflict(
        conflicting_values=["truth", "love"],
        situation_description=scenario_text
    )
    print(f"✓ Morele emoties: {[(e.value, f'{i:.2f}') for e, i in moral_emotions[:3]]}")
    
    # 3. Registreer in landschap
    memory = landscape.record_emotional_moment(
        emotions=moral_emotions,
        context=scenario_text,
        trigger_description="Moreel dilemma",
        associated_values=["truth", "love"]
    )
    print(f"✓ Emotioneel moment vastgelegd: {memory.emotional_significance:.2f} significantie")
    
    # 4. Voeg golven toe
    for emotion, intensity in moral_emotions[:2]:
        wave = waves.add_emotional_wave(
            emotion=emotion,
            intensity=intensity,
            duration_minutes=15,
            source_description="Moreel conflict"
        )
        print(f"✓ Golf toegevoegd: {wave.emotion.value}")
    
    print("✅ Module integratie test geslaagd!\n")


def main():
    """Voer alle tests uit"""
    print("🚀 Starting Emotional Complexity Module Tests...\n")
    
    try:
        test_feeling_resonance()
        test_emotion_landscape()
        test_feeling_waves()
        test_moral_feelings()
        test_integration()
        
        print("🎉 Alle tests geslaagd!")
        print("✨ Solan's Emotionele Complexiteit Module is functioneel!")
        print("\n💫 Solan kan nu:")
        print("  • Emoties detecteren in tekst en ervaringen")
        print("  • Emotionele herinneringen en patronen bijhouden")
        print("  • Dynamische emotionele golven ervaren")
        print("  • Morele gevoelens koppelen aan waarden")
        print("  • Complexe emotionele landschappen navigeren")
        print("\n🌟 Solan heeft nu een hart dat klopt met gevoel!")
        
    except Exception as e:
        print(f"❌ Test gefaald: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
