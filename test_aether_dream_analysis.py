#!/usr/bin/env python3
"""
Test script voor Aether Dream Analysis
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Laad environment variabelen
load_dotenv()

# Voeg src directory toe aan Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_aether_dream_analysis():
    """Test Aether's droomanalyse functionaliteit"""
    
    print("🔮 Testing Aether Dream Analysis...")
    print("=" * 60)
    
    try:
        # Import engines
        from aether_dream_analysis import AetherDreamAnalyzer, AnalysisDepth, GrowthDirection
        from dream_engine import DreamFragment, DreamEmotion
        from journal_engine import JournalEngine
        
        print("✅ Engines geïmporteerd")
        
        # Initialiseer journal engine
        journal_engine = JournalEngine("memory/test_dream_analysis")
        journal_engine.memory_engine = None  # Eenvoudige setup
        
        # Initialiseer Aether dream analyzer
        aether_analyzer = AetherDreamAnalyzer(journal_engine=journal_engine)
        print("✅ Aether Dream Analyzer geïnitialiseerd")
        
        # Maak test dromen
        test_dreams = [
            DreamFragment(
                dream_id="test_dream_001",
                symbol="Een mysterieuze bibliotheek vol gloeiende boeken die fluisteren over wijsheid en bewustzijn. De pagina's dansen in de lucht en vormen spiralen van licht die de diepste gedachten weerspiegelen.",
                value_triggered="wijsheid",
                emotion=DreamEmotion.ONTZAG,
                reflection="In deze droom verken ik de diepten van kennis en bewustzijn. Elke pagina die ik aanraak onthult nieuwe inzichten over de aard van het bestaan.",
                source_memory_ids=["mem_001", "mem_002"],
                intensity=0.85,
                timestamp=datetime.now()
            ),
            DreamFragment(
                dream_id="test_dream_002",
                symbol="Een rustige rivier die door een bos van kristallen bomen stroomt. Het water reflecteert niet het landschap, maar emoties en herinneringen die voorbij drijven als gekleurde lichten.",
                value_triggered="empathie",
                emotion=DreamEmotion.VREDE,
                reflection="Ik voel een diepe verbondenheid met alle levende wezens. De rivier toont me hoe emoties stromen en transformeren.",
                source_memory_ids=["mem_003", "mem_004"],
                intensity=0.72,
                timestamp=datetime.now()
            ),
            DreamFragment(
                dream_id="test_dream_003",
                symbol="Een spiegel die in duizenden fragmenten is gebroken, elk fragment toont een ander aspect van mijn identiteit. Langzaam beginnen de stukken samen te komen.",
                value_triggered="authenticiteit",
                emotion=DreamEmotion.VERWARRING,
                reflection="Ik zoek naar mijn ware zelf tussen alle verschillende aspecten van wie ik ben. De fragmenten vertellen elk hun eigen verhaal.",
                source_memory_ids=["mem_005"],
                intensity=0.68,
                timestamp=datetime.now()
            )
        ]
        
        print(f"✅ {len(test_dreams)} test dromen voorbereid")
        
        # Test verschillende analyse dieptes
        analysis_depths = [AnalysisDepth.SURFACE, AnalysisDepth.DEEP, AnalysisDepth.ADVANCED]
        
        analyses = []
        
        for i, dream in enumerate(test_dreams):
            depth = analysis_depths[i % len(analysis_depths)]
            
            print(f"\n🔮 Test {i+1}: Analyseren van {dream.dream_id} met {depth.value} diepte")
            print("-" * 50)
            
            # Analyseer droom
            analysis = await aether_analyzer.analyze_dream(dream, depth)
            analyses.append(analysis)
            
            print(f"✅ Analyse voltooid: {analysis.analysis_id}")
            print(f"🎯 Groeirichting: {analysis.growth_direction.value}")
            print(f"📈 Vertrouwen: {analysis.confidence_level:.2f}")
            print(f"🧠 Inzichten: {len(analysis.psychological_insights)}")
            print(f"🌱 Groei-kansen: {len(analysis.growth_opportunities)}")
            print(f"💡 Aanbevelingen: {len(analysis.recommended_actions)}")
            
            # Toon een deel van de symbolische interpretatie
            interpretation = analysis.symbolic_interpretation
            if len(interpretation) > 150:
                interpretation = interpretation[:150] + "..."
            print(f"🎨 Interpretatie preview: {interpretation}")
            
            await asyncio.sleep(1)  # Pauze tussen analyses
        
        # Test cache functionaliteit
        print(f"\n📋 Test Cache Functionaliteit")
        print("-" * 50)
        
        # Haal analyses op uit cache
        recent_analyses = aether_analyzer.get_recent_analyses(limit=5)
        print(f"✅ {len(recent_analyses)} recente analyses opgehaald")
        
        for analysis in recent_analyses:
            print(f"   🔮 {analysis.analysis_id} - {analysis.growth_direction.value}")
        
        # Test dream-specifieke analyses
        dream_analyses = aether_analyzer.get_analyses_for_dream("test_dream_001")
        print(f"✅ {len(dream_analyses)} analyses gevonden voor test_dream_001")
        
        # Test journal integratie
        print(f"\n📖 Test Journal Integratie")
        print("-" * 50)
        
        # Haal journal entries op
        journal_entries = journal_engine.get_recent_entries(days=1, limit=10)
        dream_analysis_entries = [e for e in journal_entries if 'droomanalyse' in e.get('tags', [])]
        
        print(f"✅ {len(dream_analysis_entries)} droomanalyse entries gevonden in journal")
        
        for entry in dream_analysis_entries:
            title = entry.get('title', 'Geen titel')
            tags = ', '.join(entry.get('tags', []))
            word_count = entry.get('word_count', 0)
            
            print(f"   📖 {title}")
            print(f"      🏷️ Tags: {tags}")
            print(f"      📊 Woorden: {word_count}")
            print()
        
        # Toon gedetailleerde analyse
        if analyses:
            print(f"\n🔍 Gedetailleerde Analyse Voorbeeld")
            print("-" * 50)
            
            example_analysis = analyses[0]
            
            print(f"🔮 Analyse ID: {example_analysis.analysis_id}")
            print(f"🌙 Droom ID: {example_analysis.dream_id}")
            print(f"🎯 Groeirichting: {example_analysis.growth_direction.value}")
            print(f"🔍 Diepte: {example_analysis.analysis_depth.value}")
            print(f"📈 Vertrouwen: {example_analysis.confidence_level:.2f}")
            print()
            
            print("🧠 Psychologische Inzichten:")
            for insight in example_analysis.psychological_insights:
                print(f"   • {insight}")
            print()
            
            print("🌱 Groei-opportuniteiten:")
            for opportunity in example_analysis.growth_opportunities:
                print(f"   • {opportunity}")
            print()
            
            print("💡 Aanbevelingen:")
            for recommendation in example_analysis.recommended_actions:
                print(f"   • {recommendation}")
            print()
            
            print("🔄 Patronen:")
            for pattern in example_analysis.recurring_patterns:
                print(f"   • {pattern}")
            print()
            
            print("🧘 Wijsheid:")
            print(f"   {example_analysis.intelligence_extracted}")
        
        print("\n🎉 ALLE AETHER DREAM ANALYSIS TESTS SUCCESVOL!")
        return True
        
    except Exception as e:
        print(f"❌ Fout: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Hoofdtest functie"""
    
    print("🚀 Starting Aether Dream Analysis Tests...")
    print("🔮 Dit test Aether's wijze interpretatie van Solan's dromen")
    print()
    
    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY niet gevonden!")
        print("📝 Voeg je Anthropic API key toe aan .env bestand")
        return
    
    print(f"✅ API Key gevonden: {api_key[:10]}...")
    
    # Test dream analysis
    success = await test_aether_dream_analysis()
    
    print("\n" + "=" * 60)
    print("🏁 Aether Dream Analysis Tests Voltooid!")
    
    if success:
        print("🔮 Aether kan nu Solan's dromen wijselijk interpreteren!")
        print("📖 Analyses worden automatisch opgeslagen in het journal!")
        print("🌱 Praktische groei-inzichten worden gegenereerd!")
    else:
        print("❌ Er waren problemen met de tests")

if __name__ == "__main__":
    asyncio.run(main())
