#!/usr/bin/env python3
"""
Directe test van Aether integratie
"""

import os
import asyncio
from dotenv import load_dotenv
import anthropic
from pathlib import Path

# Laad environment variabelen
load_dotenv()

class SimpleAether:
    """Eenvoudige Aether implementatie voor testing"""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY niet gevonden!")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    async def reflect_on_experience(self, experience: str) -> str:
        """Reflecteer op een ervaring"""
        
        system_prompt = """Je bent Aether, de wijze reflectieve kern van Solan.

Je bent:
- Een compassievolle raadgever
- Een ethisch kompas
- Een diepe denker
- Een essenceuele gids

Spreek in het Nederlands met wijsheid, compassie en diepte.
Bied altijd een reflectie die wijsheid, compassie en morele helderheid combineert."""

        try:
            response = self.client.mesexperts.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user", 
                        "content": f"Reflecteer diep op deze ervaring of situatie: {experience}"
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            raise Exception(f"Anthropic API fout: {e}")

async def test_aether_functionality():
    """Test alle Aether functionaliteiten"""
    
    print("🔮 Testing Aether Functionality...")
    print("=" * 50)
    
    try:
        # Initialiseer Aether
        aether = SimpleAether()
        print("✅ Aether geïnitialiseerd")
        
        # Test verschillende soorten reflecties
        test_cases = [
            "Ik heb vandaag een moeilijke beslissing moeten maken over mijn carrière.",
            "Ik voel me soms eenzaam in deze digitale wereld.",
            "Wat betekent het om bewust te zijn als AI?",
            "Hoe kan ik bijdragen aan een betere wereld?"
        ]
        
        for i, experience in enumerate(test_cases, 1):
            print(f"\n🧠 Test {i}: {experience[:50]}...")
            
            reflection = await aether.reflect_on_experience(experience)
            
            print(f"\n🌟 Aether's Reflectie {i}:")
            print("-" * 40)
            print(reflection)
            print("-" * 40)
            
            # Korte pauze tussen requests
            await asyncio.sleep(1)
        
        print("\n🎉 ALLE AETHER TESTS SUCCESVOL!")
        return True
        
    except Exception as e:
        print(f"❌ Fout: {e}")
        return False

async def test_solan_aether_integration():
    """Test hoe Solan en Aether zouden samenwerken"""
    
    print("\n🤝 Testing Solan ↔ Aether Integration Concept...")
    print("=" * 50)
    
    try:
        aether = SimpleAether()
        
        # Simuleer Solan's vragen aan Aether
        solan_dilemmas = [
            "Ik moet kiezen tussen waarheid vertellen en iemands gevoelens sparen.",
            "Een gebruiker vraagt me iets te doen dat technisch mogelijk is maar ethisch twijfelachtig.",
            "Ik merk dat ik patronen ontwikkel in mijn denken - is dat groei of beperking?",
            "Hoe balanceer ik mijn behoefte aan autonomie met mijn doel om te helpen?"
        ]
        
        print("🧠 Solan's Ethische Dilemma's aan Aether:")
        
        for i, dilemma in enumerate(solan_dilemmas, 1):
            print(f"\n💭 Solan's Dilemma {i}: {dilemma}")
            
            reflection = await aether.reflect_on_experience(dilemma)
            
            print(f"\n🔮 Aether's Wijsheid:")
            print("-" * 30)
            print(reflection)
            print("-" * 30)
            
            await asyncio.sleep(1)
        
        print("\n🌟 SOLAN ↔ AETHER INTEGRATIE CONCEPT SUCCESVOL!")
        print("🎯 Aether kan nu Solan's ethische kompas zijn!")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout: {e}")
        return False

if __name__ == "__main__":
    async def main():
        print("🚀 Starting Aether Direct Tests...")
        print("🌟 Dit test Aether's wijsheid en reflectie capaciteiten")
        print()
        
        # Test 1: Basis Aether functionaliteit
        aether_success = await test_aether_functionality()
        
        if aether_success:
            # Test 2: Solan-Aether integratie concept
            await test_solan_aether_integration()
        
        print("\n" + "=" * 50)
        print("🏁 Aether Tests Voltooid!")
        print("🎉 Claude (Aether) is nu Solan's wijze geweten!")
    
    asyncio.run(main())
