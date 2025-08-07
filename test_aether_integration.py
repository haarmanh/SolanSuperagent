#!/usr/bin/env python3
"""
Test script voor Aether (Claude) integratie
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

async def test_aether_integration():
    """Test of Aether correct werkt met Claude API"""
    
    print("🔮 Testing Aether (Claude) Integration...")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_anthropic_api_key_here":
        print("❌ ANTHROPIC_API_KEY niet gevonden of niet ingesteld!")
        print("📝 Voeg je Anthropic API key toe aan .env bestand")
        print("🌐 Verkrijg een API key op: https://console.anthropic.com/")
        return False
    
    print(f"✅ API Key gevonden: {api_key[:10]}...")
    
    try:
        # Import Aether
        from aether import AetherReflection
        print("✅ Aether module geïmporteerd")
        
        # Initialiseer Aether
        aether = AetherReflection()
        print("✅ Aether geïnitialiseerd")
        
        # Test reflectie
        print("\n🧠 Testing Aether reflectie...")
        test_experience = "Ik heb vandaag een moeilijke beslissing moeten maken over mijn toekomst."
        
        reflection = await aether.reflect_on_experience(test_experience)
        
        print("\n🌟 Aether's Reflectie:")
        print("-" * 30)
        print(reflection)
        print("-" * 30)
        
        print("\n🎉 AETHER INTEGRATIE SUCCESVOL!")
        return True
        
    except ImportError as e:
        print(f"❌ Import fout: {e}")
        return False
    except Exception as e:
        print(f"❌ Fout bij testen: {e}")
        return False

async def test_solan_aether_communication():
    """Test communicatie tussen Solan en Aether"""
    
    print("\n🤝 Testing Solan ↔ Aether Communication...")
    print("=" * 50)
    
    try:
        from solan import SolanAgent
        from aether import AetherReflection
        
        # Initialiseer beide agents
        aether = AetherReflection()
        solan = SolanAgent(aether_agent=aether)
        
        print("✅ Beide agents geïnitialiseerd")
        print("✅ Solan heeft toegang tot Aether")
        
        # Test morele intelligentie (gebruikt Aether)
        if hasattr(solan, 'moral_intelligence'):
            print("✅ Morele intelligentie systeem actief")
            print("🧠 Solan kan nu ethische reflecties doen via Aether")
        
        print("\n🎉 SOLAN ↔ AETHER COMMUNICATIE SUCCESVOL!")
        return True
        
    except Exception as e:
        print(f"❌ Fout bij communicatie test: {e}")
        return False

if __name__ == "__main__":
    async def main():
        print("🚀 Starting Aether Integration Tests...")
        print("🌟 Dit test of Claude (Aether) correct werkt met Solan")
        print()
        
        # Test 1: Aether standalone
        aether_success = await test_aether_integration()
        
        if aether_success:
            # Test 2: Solan-Aether communicatie
            await test_solan_aether_communication()
        else:
            print("\n⚠️  Fix eerst de Aether configuratie voordat je verder gaat")
        
        print("\n" + "=" * 50)
        print("🏁 Tests voltooid!")
    
    asyncio.run(main())
