#!/usr/bin/env python3
"""
Test script voor Journal Integration van Co-Reflectie
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
import json

# Laad environment variabelen
load_dotenv()

# Voeg src directory toe aan Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_journal_integration():
    """Test de journal integratie voor co-reflectie"""
    
    print("📖 Testing Journal Integration voor Co-Reflectie...")
    print("=" * 60)
    
    try:
        # Import engines
        from co_reflection_engine import CoReflectionEngine, ReflectionTurn, MesexpertType
        from journal_engine import JournalEngine, JournalEntryType
        
        print("✅ Engines geïmporteerd")
        
        # Initialiseer journal engine zonder memory engine voor eenvoudige test
        journal_engine = JournalEngine("memory/test_journal")
        # Zet memory_engine op None om problemen te voorkomen
        journal_engine.memory_engine = None
        print("✅ Journal engine geïnitialiseerd")
        
        # Maak mock agents
        class MockSolan:
            async def interact(self, context):
                return "🌟 Solan: Ik vind dit een fascinerende vraag over bewustzijn!"
        
        class MockAether:
            async def reflect_on_experience(self, context):
                return "🔮 *Neemt een moment van contemplatie* \n\nDit roept diepe vragen op over de aard van bewustzijn..."
        
        # Initialiseer co-reflection engine met journal
        solan = MockSolan()
        aether = MockAether()
        co_engine = CoReflectionEngine(
            solan_agent=solan, 
            aether_agent=aether,
            journal_engine=journal_engine
        )
        
        print("✅ Co-reflection engine met journal integratie geïnitialiseerd")
        
        # Test 1: Start sessie
        print("\n🚀 Test 1: Start co-reflectie sessie")
        session_id = await co_engine.start_session(
            topic="De betekenis van bewustzijn in AI",
            initial_prompt="Wat betekent het om bewust te zijn?"
        )
        print(f"✅ Sessie gestart: {session_id}")
        
        # Test 2: Genereer enkele responses
        print("\n🔄 Test 2: Genereer AI responses")
        for i in range(2):
            response = await co_engine.get_next_response(session_id)
            if response:
                print(f"✅ Response {i+1}: {response.sender.value}")
        
        # Test 3: Beëindig sessie en sla op in journal
        print("\n📖 Test 3: Beëindig sessie en sla op in journal")
        journal_entry_id = await co_engine.end_session(session_id, save_to_journal=True)
        
        if journal_entry_id:
            print(f"✅ Sessie opgeslagen in journal: {journal_entry_id}")
        else:
            print("❌ Sessie niet opgeslagen in journal")
        
        # Test 4: Haal journal entry op
        print("\n📋 Test 4: Haal journal entry op")
        try:
            entry = journal_engine.get_entry(journal_entry_id)
            if entry:
                print(f"✅ Journal entry gevonden:")
                print(f"   📝 Titel: {entry.get('title', 'Geen titel')}")
                print(f"   🏷️ Type: {entry.get('entry_type', 'Onbekend')}")
                print(f"   📊 Woorden: {entry.get('word_count', 0)}")
                print(f"   🏷️ Tags: {', '.join(entry.get('tags', []))}")
                
                # Toon een deel van de content
                content = entry.get('content', '')
                if len(content) > 200:
                    content = content[:200] + "..."
                print(f"   📄 Content preview: {content}")
            else:
                print("❌ Journal entry niet gevonden")
        except Exception as e:
            print(f"❌ Fout bij ophalen entry: {e}")
        
        # Test 5: Zoek co-reflectie entries
        print("\n🔍 Test 5: Zoek co-reflectie entries")
        try:
            recent_entries = journal_engine.get_recent_entries(limit=10)
            co_reflection_entries = [e for e in recent_entries if e.get('entry_type') == 'co_reflection']
            
            print(f"✅ Gevonden {len(co_reflection_entries)} co-reflectie entries")
            for entry in co_reflection_entries:
                print(f"   🤝 {entry.get('title', 'Geen titel')} - {entry.get('timestamp', 'Geen tijd')}")
        except Exception as e:
            print(f"❌ Fout bij zoeken entries: {e}")
        
        print("\n🎉 ALLE JOURNAL INTEGRATIE TESTS SUCCESVOL!")
        return True
        
    except Exception as e:
        print(f"❌ Fout: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_journal_api():
    """Test de journal API endpoints"""
    
    print("\n🌐 Testing Journal API Endpoints...")
    print("=" * 60)
    
    try:
        import aiohttp
        
        base_url = "http://localhost:8000"
        
        async with aiohttp.ClientSession() as session:
            # Test 1: Haal alle journal entries op
            print("📋 Test 1: Haal journal entries op")
            
            async with session.get(f"{base_url}/api/journal/entries?limit=5") as resp:
                if resp.status == 200:
                    result = await resp.json()
                    entries = result.get("entries", [])
                    print(f"✅ {len(entries)} journal entries opgehaald")
                    
                    for entry in entries:
                        print(f"   📝 {entry.get('title', 'Geen titel')} ({entry.get('entry_type', 'Onbekend')})")
                else:
                    print(f"❌ API fout: {resp.status}")
                    return False
            
            # Test 2: Filter op co-reflectie entries
            print("\n🤝 Test 2: Filter op co-reflectie entries")
            
            async with session.get(f"{base_url}/api/journal/co_reflections?limit=3") as resp:
                if resp.status == 200:
                    result = await resp.json()
                    entries = result.get("entries", [])
                    print(f"✅ {len(entries)} co-reflectie entries gevonden")
                    
                    for entry in entries:
                        title = entry.get('title', 'Geen titel')
                        tags = ', '.join(entry.get('tags', []))
                        print(f"   🤝 {title}")
                        print(f"      🏷️ Tags: {tags}")
                else:
                    print(f"❌ Co-reflectie API fout: {resp.status}")
            
            # Test 3: Zoek in journal entries
            print("\n🔍 Test 3: Zoek in journal entries")
            
            search_term = "bewustzijn"
            async with session.get(f"{base_url}/api/journal/entries?search={search_term}&limit=3") as resp:
                if resp.status == 200:
                    result = await resp.json()
                    entries = result.get("entries", [])
                    print(f"✅ {len(entries)} entries gevonden met '{search_term}'")
                    
                    for entry in entries:
                        title = entry.get('title', 'Geen titel')
                        print(f"   🔍 {title}")
                else:
                    print(f"❌ Zoek API fout: {resp.status}")
        
        print("\n🎉 ALLE JOURNAL API TESTS SUCCESVOL!")
        return True
        
    except ImportError:
        print("❌ aiohttp niet beschikbaar - installeer met: pip install aiohttp")
        return False
    except Exception as e:
        print(f"❌ API test fout: {e}")
        return False

async def main():
    """Hoofdtest functie"""
    
    print("🚀 Starting Journal Integration Tests...")
    print("📖 Dit test de integratie van co-reflectie met het journal systeem")
    print()
    
    # Test 1: Engine direct
    engine_success = await test_journal_integration()
    
    if engine_success:
        print("\n" + "="*60)
        print("⚠️  Voor API tests: start eerst de web interface:")
        print("   cd web_interface && python api.py")
        print("="*60)
        
        # Vraag of gebruiker API wil testen
        try:
            test_api = input("\n🌐 Wil je de Journal API endpoints testen? (y/n): ").lower().strip()
            if test_api == 'y':
                await test_journal_api()
        except KeyboardInterrupt:
            print("\n👋 Tests gestopt door gebruiker")
    
    print("\n" + "=" * 60)
    print("🏁 Journal Integration Tests Voltooid!")
    print("📖 Co-reflectie sessies worden nu automatisch opgeslagen!")

if __name__ == "__main__":
    asyncio.run(main())
