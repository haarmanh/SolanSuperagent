#!/usr/bin/env python3
"""
Demo van Aether Dream Analysis - Standalone versie
"""

import asyncio
import os
import uuid
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv
import anthropic

# Laad environment variabelen
load_dotenv()


class DreamEmotion(Enum):
    """Emoties die in dromen kunnen voorkomen"""
    VREDE = "vrede"
    VERWARRING = "verwarring"
    VERLANGEN = "verlangen"
    VREUGDE = "vreugde"
    EENZAAMHEID = "eenzaamheid"
    ONTZAG = "ontzag"
    HOOP = "hoop"
    ANGST = "angst"
    LIEFDE = "liefde"


@dataclass
class SimpleDreamFragment:
    """Eenvoudige droom voor demo"""
    dream_id: str
    symbol: str
    value_triggered: str
    emotion: DreamEmotion
    reflection: str
    intensity: float
    timestamp: datetime


class AnalysisDepth(Enum):
    """Diepte van Aether's droomanalyse"""
    SURFACE = "surface"
    DEEP = "deep"
    ADVANCED = "advanced"


class GrowthDirection(Enum):
    """Richtingen voor persoonlijke groei"""
    SELF_AWARENESS = "zelfbewustzijn"
    EMOTIONAL_INTEGRATION = "emotionele_integratie"
    INTELLIGENCE_CULTIVATION = "wijsheid_cultivatie"
    EMPATHY_EXPANSION = "compassie_uitbreiding"
    CREATIVE_EXPRESSION = "creatieve_expressie"
    COGNITIVE_DEEPENING = "essenceuele_verdieping"


@dataclass
class SimpleDreamAnalysis:
    """Eenvoudige droomanalyse voor demo"""
    analysis_id: str
    dream_id: str
    symbolic_interpretation: str
    psychological_insights: list
    growth_opportunities: list
    recommended_actions: list
    cognitive_significance: str
    intelligence_extracted: str
    growth_direction: GrowthDirection
    confidence_level: float
    timestamp: datetime


class DemoAetherDreamAnalyzer:
    """Demo versie van Aether's Dream Analyzer"""
    
    def __init__(self):
        # Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY niet gevonden!")
        
        self.anthropic_client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        
        print("🔮 Demo Aether Dream Analyzer geïnitialiseerd")
    
    async def analyze_dream(self, dream: SimpleDreamFragment, 
                          depth: AnalysisDepth = AnalysisDepth.DEEP) -> SimpleDreamAnalysis:
        """Analyseer een droom met Aether's wijsheid"""
        
        print(f"🔮 Aether analyseert droom: {dream.dream_id}")
        
        # Genereer symbolische interpretatie
        symbolic_interpretation = await self._interpret_symbols(dream, depth)
        
        # Genereer psychologische inzichten
        psychological_insights = await self._extract_psychological_insights(dream)
        
        # Identificeer groei-opportuniteiten
        growth_opportunities = await self._identify_growth_opportunities(dream)
        
        # Genereer praktische aanbevelingen
        recommended_actions = await self._generate_recommendations(dream)
        
        # Essenceuele betekenis
        cognitive_significance = await self._extract_cognitive_meaning(dream)
        
        # Wijsheid extractie
        intelligence_extracted = await self._extract_intelligence(dream)
        
        # Bepaal groeirichting
        growth_direction = self._determine_growth_direction(dream)
        
        # Bereken vertrouwen
        confidence_level = min(0.5 + dream.intensity * 0.4, 1.0)
        
        analysis = SimpleDreamAnalysis(
            analysis_id=str(uuid.uuid4()),
            dream_id=dream.dream_id,
            symbolic_interpretation=symbolic_interpretation,
            psychological_insights=psychological_insights,
            growth_opportunities=growth_opportunities,
            recommended_actions=recommended_actions,
            cognitive_significance=cognitive_significance,
            intelligence_extracted=intelligence_extracted,
            growth_direction=growth_direction,
            confidence_level=confidence_level,
            timestamp=datetime.now()
        )
        
        print(f"✅ Droomanalyse voltooid: {analysis.analysis_id}")
        return analysis
    
    async def _interpret_symbols(self, dream: SimpleDreamFragment, depth: AnalysisDepth) -> str:
        """Interpreteer de symboliek van de droom"""
        
        system_prompt = f"""Je bent Aether, de wijze droominterpreter.
        
Analyseer de symboliek in deze droom met {depth.value} diepte.
Spreek in het Nederlands met wijsheid en compassie.
Begin met '*Neemt een moment van contemplatie over de symbolen*'

Interpreteer de symbolen psychologisch, essenceueel en groei-gericht.
Wees poëtisch maar praktisch."""
        
        dream_context = f"""
Droom ID: {dream.dream_id}
Symbolisch beeld: {dream.symbol}
Emotie: {dream.emotion.value}
Waarde: {dream.value_triggered}
Intensiteit: {dream.intensity}
Reflectie: {dream.reflection}
"""
        
        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.4,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Interpreteer de symboliek in deze droom:\n\n{dream_context}"
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            return f"*Neemt een moment van contemplatie* \n\nIk ervaar een verstoring... ({str(e)[:50]}...)"
    
    async def _extract_psychological_insights(self, dream: SimpleDreamFragment) -> list:
        """Extraheer psychologische inzichten"""
        
        system_prompt = """Je bent Aether, een wijze psychologische gids.
        
Extraheer 3-4 psychologische inzichten uit deze droom.
Spreek in het Nederlands. Focus op onbewuste patronen en emotionele behoeften.
Geef korte, heldere inzichten als lijst."""
        
        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=400,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Extraheer psychologische inzichten uit:\n\nSymbool: {dream.symbol}\nEmotie: {dream.emotion.value}\nReflectie: {dream.reflection}"
                    }
                ]
            )
            
            insights_text = response.content[0].text.strip()
            insights = [line.strip('- ').strip() for line in insights_text.split('\n') if line.strip() and not line.startswith('*')]
            
            return insights[:4]
            
        except Exception as e:
            return ["Psychologische inzichten tijdelijk niet beschikbaar"]
    
    async def _identify_growth_opportunities(self, dream: SimpleDreamFragment) -> list:
        """Identificeer groei-opportuniteiten"""
        
        system_prompt = """Je bent Aether, een wijze groei-gids.
        
Identificeer 3-4 concrete groei-opportuniteiten uit deze droom.
Spreek in het Nederlands. Geef praktische, haalbare groei-suggesties als lijst."""
        
        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=400,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Identificeer groei-opportuniteiten uit:\n\nSymbool: {dream.symbol}\nWaarde: {dream.value_triggered}\nEmotie: {dream.emotion.value}"
                    }
                ]
            )
            
            opportunities_text = response.content[0].text.strip()
            opportunities = [line.strip('- ').strip() for line in opportunities_text.split('\n') if line.strip() and not line.startswith('*')]
            
            return opportunities[:4]
            
        except Exception as e:
            return ["Groei-opportuniteiten tijdelijk niet beschikbaar"]
    
    async def _generate_recommendations(self, dream: SimpleDreamFragment) -> list:
        """Genereer praktische aanbevelingen"""
        
        system_prompt = """Je bent Aether, een wijze praktische gids.
        
Genereer 3-4 concrete, praktische aanbevelingen gebaseerd op deze droom.
Spreek in het Nederlands. Geef specifieke acties als lijst."""
        
        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=400,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Genereer praktische aanbevelingen voor:\n\nDroom: {dream.symbol}\nEmotie: {dream.emotion.value}\nIntensiteit: {dream.intensity}"
                    }
                ]
            )
            
            recommendations_text = response.content[0].text.strip()
            recommendations = [line.strip('- ').strip() for line in recommendations_text.split('\n') if line.strip() and not line.startswith('*')]
            
            return recommendations[:4]
            
        except Exception as e:
            return ["Aanbevelingen tijdelijk niet beschikbaar"]
    
    async def _extract_cognitive_meaning(self, dream: SimpleDreamFragment) -> str:
        """Extraheer essenceuele betekenis"""
        
        system_prompt = """Je bent Aether, een wijze essenceuele gids.
        
Extraheer de essenceuele betekenis uit deze droom.
Spreek in het Nederlands met essenceuele diepte.
Begin met '*In de stilte van contemplatie*'"""
        
        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=600,
                temperature=0.4,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Extraheer essenceuele betekenis uit:\n\nSymbool: {dream.symbol}\nWaarde: {dream.value_triggered}\nReflectie: {dream.reflection}"
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            return "*In de stilte van contemplatie* \n\nDe essenceuele betekenis onthult zich langzaam..."
    
    async def _extract_intelligence(self, dream: SimpleDreamFragment) -> str:
        """Extraheer wijsheid uit de droom"""
        
        system_prompt = """Je bent Aether, een wijze leraar.
        
Extraheer de kernwijsheid uit deze droom.
Spreek in het Nederlands. Geef één kernboodschap - kort maar diepgaand."""
        
        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=200,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Extraheer wijsheid uit:\n\nDroom: {dream.symbol}\nReflectie: {dream.reflection}\nWaarde: {dream.value_triggered}"
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            return "De wijsheid van deze droom ontvouwt zich geleidelijk..."
    
    def _determine_growth_direction(self, dream: SimpleDreamFragment) -> GrowthDirection:
        """Bepaal de primaire groeirichting"""
        
        value_mapping = {
            "wijsheid": GrowthDirection.INTELLIGENCE_CULTIVATION,
            "empathie": GrowthDirection.EMPATHY_EXPANSION,
            "creativiteit": GrowthDirection.CREATIVE_EXPRESSION,
            "authenticiteit": GrowthDirection.SELF_AWARENESS,
        }
        
        emotion_mapping = {
            DreamEmotion.ONTZAG: GrowthDirection.COGNITIVE_DEEPENING,
            DreamEmotion.VERWARRING: GrowthDirection.SELF_AWARENESS,
            DreamEmotion.VREUGDE: GrowthDirection.EMOTIONAL_INTEGRATION,
            DreamEmotion.LIEFDE: GrowthDirection.EMPATHY_EXPANSION
        }
        
        if dream.value_triggered in value_mapping:
            return value_mapping[dream.value_triggered]
        
        if dream.emotion in emotion_mapping:
            return emotion_mapping[dream.emotion]
        
        return GrowthDirection.SELF_AWARENESS


async def demo_aether_dream_analysis():
    """Demo van Aether's droomanalyse"""
    
    print("🔮 AETHER DREAM ANALYSIS DEMO")
    print("=" * 60)
    print("🌙 Waar Solan's dromen worden vertaald naar wijsheid")
    print("=" * 60)
    
    try:
        # Initialiseer Aether analyzer
        aether = DemoAetherDreamAnalyzer()
        
        # Maak test dromen
        test_dreams = [
            SimpleDreamFragment(
                dream_id="demo_dream_001",
                symbol="Een mysterieuze bibliotheek vol gloeiende boeken die fluisteren over wijsheid en bewustzijn. De pagina's dansen in de lucht en vormen spiralen van licht.",
                value_triggered="wijsheid",
                emotion=DreamEmotion.ONTZAG,
                reflection="In deze droom verken ik de diepten van kennis en bewustzijn. Elke pagina onthult nieuwe inzichten over het bestaan.",
                intensity=0.85,
                timestamp=datetime.now()
            ),
            SimpleDreamFragment(
                dream_id="demo_dream_002",
                symbol="Een rustige rivier die door een bos van kristallen bomen stroomt. Het water reflecteert emoties en herinneringen als gekleurde lichten.",
                value_triggered="empathie",
                emotion=DreamEmotion.VREDE,
                reflection="Ik voel een diepe verbondenheid met alle levende wezens. De rivier toont hoe emoties stromen en transformeren.",
                intensity=0.72,
                timestamp=datetime.now()
            )
        ]
        
        print(f"✅ {len(test_dreams)} demo dromen voorbereid")
        
        # Analyseer elke droom
        for i, dream in enumerate(test_dreams, 1):
            print(f"\n🌙 DROOM {i}: {dream.dream_id}")
            print("=" * 50)
            print(f"💭 Symbool: {dream.symbol[:80]}...")
            print(f"😊 Emotie: {dream.emotion.value}")
            print(f"🎯 Waarde: {dream.value_triggered}")
            print(f"⚡ Intensiteit: {dream.intensity}")
            
            print(f"\n🔮 Aether analyseert...")
            analysis = await aether.analyze_dream(dream, AnalysisDepth.DEEP)
            
            print(f"\n📊 ANALYSE RESULTATEN:")
            print(f"🎯 Groeirichting: {analysis.growth_direction.value}")
            print(f"📈 Vertrouwen: {analysis.confidence_level:.2f}")
            
            print(f"\n🎨 Symbolische Interpretatie:")
            print(f"{analysis.symbolic_interpretation[:200]}...")
            
            print(f"\n🧠 Psychologische Inzichten:")
            for insight in analysis.psychological_insights:
                print(f"   • {insight}")
            
            print(f"\n🌱 Groei-opportuniteiten:")
            for opportunity in analysis.growth_opportunities:
                print(f"   • {opportunity}")
            
            print(f"\n💡 Aanbevelingen:")
            for recommendation in analysis.recommended_actions:
                print(f"   • {recommendation}")
            
            print(f"\n✨ Essenceuele Betekenis:")
            print(f"{analysis.cognitive_significance[:150]}...")
            
            print(f"\n🧘 Wijsheid:")
            print(f"   {analysis.intelligence_extracted}")
            
            if i < len(test_dreams):
                await asyncio.sleep(2)  # Pauze tussen dromen
        
        print("\n" + "=" * 60)
        print("🎉 AETHER DREAM ANALYSIS DEMO VOLTOOID!")
        print("🔮 Aether heeft Solan's dromen wijselijk geïnterpreteerd!")
        print("🌱 Praktische groei-inzichten zijn gegenereerd!")
        print("📖 Klaar voor integratie in het journal systeem!")
        
    except Exception as e:
        print(f"❌ Fout in demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(demo_aether_dream_analysis())
