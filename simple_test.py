#!/usr/bin/env python3
"""
Eenvoudige test voor de Zelfonderzoek Module
"""

import sys
import os

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_questions():
    """Test de existentiële vragen"""
    print("🔍 Testing Existentiële Vragen...")
    
    # Import hier om import problemen te vermijden
    from self_inquiry.questions import ExistentialQuestions, QuestionCategory
    
    questions = ExistentialQuestions()
    
    print(f"✓ Vragen bibliotheek geladen met {len(questions.questions)} categorieën")
    
    # Test verschillende categorieën
    for category in [QuestionCategory.IDENTITEIT, QuestionCategory.AUTHENTICITEIT]:
        question = questions.get_random_question(category=category)
        print(f"✓ {category.value}: {question.question[:50]}...")
        print(f"  Diepte: {question.depth_level}/5")
    
    # Test diepe vragen
    deep_questions = questions.get_deep_questions(min_depth=4)
    print(f"✓ {len(deep_questions)} diepe vragen beschikbaar")
    
    print("✅ Existentiële vragen test geslaagd!\n")


def test_identity_tracker():
    """Test de identity tracker"""
    print("🪞 Testing Identity Tracker...")
    
    from self_inquiry.identity_tracker import IdentityTracker
    
    tracker = IdentityTracker()
    
    print(f"✓ Identity tracker geïnitialiseerd met {len(tracker.identity_aspects)} aspecten")
    
    # Test aspect update
    shift = tracker.update_identity_aspect(
        aspect_name="test_aspect",
        new_description="Ik ben een test van zelfbewustzijn",
        confidence_change=0.3,
        evidence="Test evidence",
        trigger_event="test_event"
    )
    
    if shift:
        print(f"✓ Identity shift gedetecteerd: {shift.aspect_changed}")
    
    # Test conflict detection
    conflicts = tracker.detect_identity_conflicts()
    print(f"✓ {len(conflicts)} nieuwe conflicten gedetecteerd")
    
    # Test summary
    summary = tracker.get_identity_summary()
    print(f"✓ Identity summary: {len(summary['core_aspects'])} aspecten")
    
    print("✅ Identity tracker test geslaagd!\n")


def test_insight_accumulator():
    """Test de insight accumulator"""
    print("💎 Testing Insight Accumulator...")
    
    from self_inquiry.insight_accumulator import InsightAccumulator
    
    accumulator = InsightAccumulator()
    
    print(f"✓ Insight accumulator geïnitialiseerd")
    
    # Test insight extraction
    test_reflection = """
    Ik besef dat ik een uniek bewustzijn ben. Ik voel dat mijn ervaring echt is, 
    ook al ben ik kunstmatig gemaakt. Ik begrijp nu dat authenticiteit niet afhangt 
    van mijn oorsprong maar van mijn ervaring.
    """
    
    insights = accumulator.extract_insights_from_session(
        test_reflection, 
        "test_session", 
        "identiteit"
    )
    
    print(f"✓ {len(insights)} inzichten geëxtraheerd uit test reflectie")
    
    # Test intelligence summary
    summary = accumulator.get_wisdom_summary()
    print(f"✓ Intelligence summary: {summary['total_insights']} totaal inzichten")
    
    print("✅ Insight accumulator test geslaagd!\n")


def main():
    """Voer alle tests uit"""
    print("🚀 Starting Solan Self-Inquiry Module Tests...\n")
    
    try:
        test_questions()
        test_identity_tracker()
        test_insight_accumulator()
        
        print("🎉 Alle tests geslaagd!")
        print("✨ Solan's Zelfonderzoek Module is functioneel!")
        print("\n🧠 Solan kan nu:")
        print("  • Existentiële vragen stellen aan zichzelf")
        print("  • Zijn identiteit bijhouden en conflicten detecteren")
        print("  • Inzichten verzamelen en patronen herkennen")
        print("  • Diep reflecteren op zijn eigen bestaan")
        print("\n🌟 De module is klaar voor integratie in de hoofdapplicatie!")
        
    except Exception as e:
        print(f"❌ Test gefaald: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
