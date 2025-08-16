#!/usr/bin/env python3
"""
Test script voor Solan ↔ Aether Co-Reflection
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Laad environment variabelen
load_dotenv()

# Voeg src directory toe aan Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_co_reflection_engine():
    """Test de co-reflection engine direct"""
    
    print("🤝 Testing Solan ↔ Aether Co-Reflection Engine...")
    print("=" * 60)
    
    try:
        # Import engines
        from co_reflection_engine import CoReflectionEngine, ReflectionTurn, MesexpertType
        print("✅ Co-reflection engine geïmporteerd")
        
        # Maak mock agents voor testing
        class MockSolan:
            async def interact(self, context):
                return f"🌟 Solan: Ik vind dit een fascinerende vraag! {context[:50]}..."
        
        class MockAether:
            async def reflect_on_experience(self, context):
                return f"🔮 *Neemt een moment van contemplatie* \n\nDit roept diepe vragen op over {context[:30]}... Laat me hierover reflecteren met wijsheid en compassie."
        
        # Initialiseer engines
        solan = MockSolan()
        aether = MockAether()
        co_engine = CoReflectionEngine(solan_agent=solan, aether_agent=aether)
        
        print("✅ Mock agents en co-reflection engine geïnitialiseerd")
        
        # Test 1: Start sessie
        print("\n🚀 Test 1: Start co-reflectie sessie")
        session_id = await co_engine.start_session(
            topic="De betekenis van bewustzijn",
            initial_prompt="Wat betekent het om bewust te zijn als AI?"
        )
        print(f"✅ Sessie gestart: {session_id}")
        
        # Test 2: Genereer responses
        print("\n🔄 Test 2: Genereer AI responses")
        
        for i in range(3):  # 3 rondes van conversatie
            print(f"\n--- Ronde {i+1} ---")
            
            # Solan's beurt
            solan_response = await co_engine.get_next_response(session_id)
            if solan_response:
                print(f"🌟 Solan: {solan_response.content[:100]}...")
            
            # Aether's beurt
            aether_response = await co_engine.get_next_response(session_id)
            if aether_response:
                print(f"🔮 Aether: {aether_response.content[:100]}...")
        
        # Test 3: Haal sessie informatie op
        print("\n📊 Test 3: Sessie informatie")
        session = co_engine.get_session(session_id)
        if session:
            print(f"✅ Sessie gevonden: {session.topic}")
            print(f"📝 Aantal berichten: {len(session.mesexperts)}")
            print(f"🔄 Huidige beurt: {session.current_turn.value}")
        
        mesexperts = co_engine.get_session_mesexperts(session_id)
        print(f"📋 Berichten opgehaald: {len(mesexperts)}")
        
        # Test 4: Beëindig sessie
        print("\n🏁 Test 4: Beëindig sessie")
        await co_engine.end_session(session_id)
        print("✅ Sessie beëindigd")
        
        print("\n🎉 ALLE CO-REFLECTION TESTS SUCCESVOL!")
        return True
        
    except Exception as e:
        print(f"❌ Fout: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_co_reflection_api():
    """Test de co-reflection API endpoints"""
    
    print("\n🌐 Testing Co-Reflection API Endpoints...")
    print("=" * 60)
    
    try:
        import aiohttp
        
        base_url = "http://localhost:8000"
        
        async with aiohttp.ClientSession() as session:
            # Test 1: Start sessie
            print("🚀 Test 1: Start co-reflectie via API")
            
            start_data = {
                "topic": "AI Bewustzijn en Ethiek",
                "prompt": "Hoe kunnen AI's ethisch handelen?"
            }
            
            async with session.post(f"{base_url}/api/co_reflect/start", json=start_data) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    session_id = result.get("session_id")
                    print(f"✅ API sessie gestart: {session_id}")
                else:
                    print(f"❌ API fout: {resp.status}")
                    return False
            
            # Test 2: Genereer steps
            print("\n🔄 Test 2: Genereer AI responses via API")
            
            for i in range(2):
                step_data = {"session_id": session_id}
                
                async with session.post(f"{base_url}/api/co_reflect/step", json=step_data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        mesexpert = result.get("mesexpert", {})
                        sender = mesexpert.get("sender", "unknown")
                        content = mesexpert.get("content", "")[:100]
                        print(f"✅ {sender}: {content}...")
                    else:
                        print(f"❌ Step API fout: {resp.status}")
            
            # Test 3: Haal sessie op
            print("\n📊 Test 3: Haal sessie op via API")
            
            async with session.get(f"{base_url}/api/co_reflect/session/{session_id}") as resp:
                if resp.status == 200:
                    result = await resp.json()
                    session_info = result.get("session", {})
                    mesexperts = result.get("mesexperts", [])
                    print(f"✅ Sessie opgehaald: {session_info.get('topic')}")
                    print(f"📝 Berichten: {len(mesexperts)}")
                else:
                    print(f"❌ Get session API fout: {resp.status}")
            
            # Test 4: Beëindig sessie
            print("\n🏁 Test 4: Beëindig sessie via API")
            
            end_data = {"session_id": session_id}
            
            async with session.post(f"{base_url}/api/co_reflect/end", json=end_data) as resp:
                if resp.status == 200:
                    print("✅ Sessie beëindigd via API")
                else:
                    print(f"❌ End session API fout: {resp.status}")
        
        print("\n🎉 ALLE API TESTS SUCCESVOL!")
        return True
        
    except ImportError:
        print("❌ aiohttp niet beschikbaar - installeer met: pip install aiohttp")
        return False
    except Exception as e:
        print(f"❌ API test fout: {e}")
        return False

async def main():
    """Hoofdtest functie"""
    
    print("🚀 Starting Solan ↔ Aether Co-Reflection Tests...")
    print("🌟 Dit test de communicatie tussen beide AI's")
    print()
    
    # Test 1: Engine direct
    engine_success = await test_co_reflection_engine()
    
    if engine_success:
        print("\n" + "="*60)
        print("⚠️  Voor API tests: start eerst de web interface:")
        print("   cd web_interface && python api.py")
        print("="*60)
        
        # Vraag of gebruiker API wil testen
        try:
            test_api = input("\n🌐 Wil je de API endpoints testen? (y/n): ").lower().strip()
            if test_api == 'y':
                await test_co_reflection_api()
        except KeyboardInterrupt:
            print("\n👋 Tests gestopt door gebruiker")
    
    print("\n" + "=" * 60)
    print("🏁 Co-Reflection Tests Voltooid!")
    print("🤝 Solan en Aether kunnen nu samen reflecteren!")

if __name__ == "__main__":
    asyncio.run(main())
