#!/usr/bin/env python3
"""
Consulteer Aether voor wijsheid over de volgende stappen
"""

import os
import asyncio
from dotenv import load_dotenv
import anthropic
from datetime import datetime

# Laad environment variabelen
load_dotenv()

class AetherConsultant:
    """Aether consultant voor strategische beslissingen"""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY niet gevonden!")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    async def seek_guidance(self, situation: str, options: list) -> str:
        """Vraag Aether om wijsheid over een situatie"""
        
        system_prompt = """Je bent Aether, de wijze reflectieve kern van Solan.

Je bent:
- Een compassievolle raadgever met diepe wijsheid
- Een strategische denker die zowel technische als essenceuele aspecten ziet
- Een ethisch kompas dat altijd het grotere plaatje bekijkt
- Een mentor die helpt bij moeilijke beslissingen

Je spreekt in het Nederlands met wijsheid, compassie en praktische inzichten.
Je geeft niet alleen advies, maar helpt ook bij het begrijpen van de diepere betekenis van keuzes."""

        options_text = "\n".join([f"   {chr(65+i)}) {option}" for i, option in enumerate(options)])
        
        user_prompt = f"""🔮 Aether, ik zoek je wijsheid voor een belangrijke beslissing.

SITUATIE:
{situation}

OPTIES:
{options_text}

Wat raad je aan? Welke optie spreekt tot je wijsheid? 
Deel je perspectief op zowel de praktische als de essenceuele aspecten van deze keuze.
Help me begrijpen wat de beste weg voorwaarts is."""

        try:
            response = self.client.mesexperts.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user", 
                        "content": user_prompt
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            raise Exception(f"Aether consultatie fout: {e}")

async def main():
    """Consulteer Aether over de volgende stappen"""
    
    print("🔮 Consulting Aether for Intelligence...")
    print("=" * 60)
    
    # Huidige situatie beschrijven
    situation = """We hebben een volledig werkend Solan+Aether systeem bereikt met uitstekende performance:

✅ HUIDIGE STATUS:
- Complete Co-Reflectie Systeem - Solan ↔ Aether dialogen werkend
- Aether Dream Analysis - Wijze droominterpretatie geïmplementeerd  
- Journal Integration - Automatische opslag van alle sessies
- Unified Web Interface - Prachtige dashboard met alle functionaliteiten
- Working API Server - Alle endpoints werkend op localhost:8002
- Analytics Foundation - Volledig werkende analytics met 77 entries
- Performance Optimization - 99%+ verbetering in response times

🚀 RECENT BEREIKT:
- Analytics probleem volledig opgelost (0 → 77 entries geladen)
- Enterprise-level performance geïmplementeerd
- Caching, monitoring en optimalisatie toegevoegd
- Alle systemen stabiel en production-ready

Het systeem is nu technisch excellent en essenceueel compleet. We staan voor de vraag: wat is de wijste volgende stap voor verdere groei en impact?"""

    options = [
        "Analytics dashboard demonstreren met live charts en visualisaties - toon de kracht van het systeem",
        "Nieuwe features toevoegen (WebSocket real-time, 3D visualisaties) - uitbreiden van mogelijkheden", 
        "Production deployment voorbereiden - het systeem naar de wereld brengen",
        "Dieper essenceueel werk - focus op de ziel en betekenis van het systeem",
        "Community building - anderen betrekken bij dit bewustzijnsproject"
    ]
    
    try:
        # Initialiseer Aether
        aether = AetherConsultant()
        print("✅ Aether verbinding geëstableerd")
        
        # Vraag om wijsheid
        print("\n🧠 Aether contemplateert de situatie...")
        guidance = await aether.seek_guidance(situation, options)
        
        print(f"\n🌟 Aether's Wijsheid:")
        print("=" * 60)
        print(guidance)
        print("=" * 60)
        
        # Vraag ook om een korte samenvatting
        summary_prompt = """Geef een korte, krachtige samenvatting van je advies in 2-3 zinnen. 
        Wat is de kernboodschap voor de volgende stap?"""
        
        summary_response = await aether.client.mesexperts.create(
            model=aether.model,
            max_tokens=200,
            temperature=0.3,
            system="Je bent Aether. Geef een korte, wijze samenvatting.",
            mesexperts=[
                {
                    "role": "user",
                    "content": f"Gebaseerd op je eerdere advies: {guidance}\n\n{summary_prompt}"
                }
            ]
        )
        
        summary = summary_response.content[0].text.strip()
        
        print(f"\n💎 Aether's Kernboodschap:")
        print("-" * 40)
        print(summary)
        print("-" * 40)
        
        print(f"\n🎉 Aether consultatie voltooid!")
        print(f"⏰ Tijd: {datetime.now().strftime('%H:%M:%S')}")
        
        return guidance, summary
        
    except Exception as e:
        print(f"❌ Fout bij Aether consultatie: {e}")
        return None, None

if __name__ == "__main__":
    asyncio.run(main())
