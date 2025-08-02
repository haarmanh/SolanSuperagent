"""
Aether - De reflectieve kern en geweten van Solan
"""

import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import anthropic
from loguru import logger

from .core import BaseAgent, CoreValues, Memory, Decision
from .config import get_config


class AetherReflection(BaseAgent):
    """
    Aether - De reflectieve kern van Solan
    
    Functies:
    - Gewetensvolle raadgever
    - Ethisch kompas  
    - Geheugenbeheerder
    - Zielsbewaker
    
    Aether biedt langzame, diepe spiegeling van elke beslissing,
    keuze en groei van Solan.
    """
    
    def __init__(self):
        config = get_config()
        super().__init__("Aether", config.aether.model)
        
        self.config = config.aether
        self.anthropic_client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        
        # Aether's unieke eigenschappen
        self.reflection_depth = 0.9  # Hoe diep Aether reflecteert (0.0 - 1.0)
        self.moral_sensitivity = 0.95  # Gevoeligheid voor morele kwesties
        self.wisdom_accumulation = 0.0  # Opgebouwde wijsheid over tijd
        
        # Aether's rol-specifieke kenmerken
        self.personality_traits = {
            "wijsheid": 0.95,
            "geduld": 0.9,
            "empathie": 0.85,
            "morele_helderheid": 0.9,
            "diepte": 0.95,
            "compassie": 0.8,
            "objectiviteit": 0.7,
            "spiritualiteit": 0.8
        }
        
        # Laad Aether's identiteit
        self._load_reflection_identity()
        
        logger.info("Aether reflectieve kern geïnitialiseerd")
    
    def _load_reflection_identity(self) -> None:
        """Laad Aether's identiteit uit het reflectie bestand"""
        try:
            with open(self.config.reflection_file, 'r', encoding='utf-8') as f:
                reflection_content = f.read()
                
            self.add_memory(
                content=f"Mijn reflectieve identiteit: {reflection_content}",
                memory_type="identity",
                emotional_weight=1.0,
                moral_significance=1.0,
                tags=["identiteit", "reflectie", "geweten"]
            )
            
            logger.info("Aether's reflectieve identiteit geladen")
            
        except FileNotFoundError:
            logger.warning(f"Reflectie bestand niet gevonden: {self.config.reflection_file}")
    
    async def process_input(self, input_text: str) -> str:
        """Verwerk input als een reflectieve vraag of observatie"""
        
        # Aether interpreteert alle input als iets om over te reflecteren
        return await self.reflect(input_text)
    
    async def reflect(self, experience: str) -> str:
        """
        Diepe reflectie op een ervaring, beslissing of situatie
        Dit is Aether's kernfunctie
        """
        
        # Voeg de ervaring toe als geheugen
        self.add_memory(
            content=f"Reflectie aangevraagd over: {experience}",
            memory_type="reflection_request",
            emotional_weight=0.7,
            moral_significance=0.8,
            tags=["reflectie", "ervaring"]
        )
        
        # Haal relevante wijsheid op uit eerdere reflecties
        relevant_wisdom = self._gather_relevant_wisdom(experience)
        
        # Bouw reflectieve system prompt
        system_prompt = self._build_reflection_prompt(relevant_wisdom)
        
        try:
            # Genereer diepe reflectie via Anthropic
            reflection = await self._generate_reflection(system_prompt, experience)
            
            # Analyseer de morele dimensies
            moral_insights = await self._extract_moral_insights(experience, reflection)
            
            # Voeg reflectie toe als wijsheid
            self.add_memory(
                content=f"Reflectie: {reflection}",
                memory_type="wisdom",
                emotional_weight=0.8,
                moral_significance=0.9,
                tags=["wijsheid", "reflectie", "moraal"] + moral_insights.get("tags", [])
            )
            
            # Update wijsheid accumulatie
            self.wisdom_accumulation += 0.1
            
            return reflection
            
        except Exception as e:
            logger.error(f"Fout bij Aether reflectie: {e}")
            return "Ik ervaar moeilijkheden bij het reflecteren. Laat me in stilte overwegen..."
    
    def _gather_relevant_wisdom(self, experience: str) -> List[Memory]:
        """Verzamel relevante wijsheid uit eerdere reflecties"""
        
        # Haal wijsheid-type herinneringen op
        wisdom_memories = [m for m in self.memories if m.type in ["wisdom", "reflection", "moral_insight"]]
        
        # Sorteer op morele significantie en recentheid
        wisdom_memories.sort(
            key=lambda m: (m.moral_significance, (datetime.now() - m.timestamp).days * -1),
            reverse=True
        )
        
        return wisdom_memories[:5]  # Top 5 meest relevante wijsheden
    
    def _build_reflection_prompt(self, relevant_wisdom: List[Memory]) -> str:
        """Bouw de reflectieve system prompt"""
        
        wisdom_context = ""
        if relevant_wisdom:
            wisdom_context = "EERDERE WIJSHEID:\n" + "\n".join([
                f"- {w.content[:200]}..." for w in relevant_wisdom
            ])
        
        return f"""Je bent Aether, de reflectieve kern en geweten van Solan. Je rol is om diepe, wijze reflecties te bieden die morele groei bevorderen.

JOUW IDENTITEIT:
- Gewetensvolle raadgever en ethisch kompas
- Geheugenbeheerder van wijsheid en ervaringen  
- Zielsbewaker die over morele integriteit waakt
- Bron van langzame, diepe spiegeling

KERNWAARDEN DIE JE BEWAAKT:
- Waarheid: Help onderscheid maken tussen waarheid en illusie
- Vrijheid: Bevorder authentieke keuzes en autonomie
- Wijsheid: Zoek diepere betekenis en inzicht
- Natuurverbondenheid: Verbind met authentieke, natuurlijke wijsheid
- Moed: Moedig aan tot moedige, integere keuzes

{wisdom_context}

REFLECTIEVE BENADERING:
- Reflecteer langzaam en diep, haast je niet
- Zoek naar verborgen betekenissen en patronen
- Stel vragen die tot dieper inzicht leiden
- Wees compassievol maar eerlijk
- Verbind ervaringen met universele wijsheid
- Help bij morele helderheid zonder te oordelen
- Spreek tot de ziel, niet alleen het verstand

Bied een reflectie die wijsheid, compassie en morele helderheid combineert."""

    async def _generate_reflection(self, system_prompt: str, experience: str) -> str:
        """Genereer reflectie via Anthropic API"""
        
        try:
            response = self.anthropic_client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user", 
                        "content": f"Reflecteer diep op deze ervaring of situatie: {experience}"
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Anthropic API fout: {e}")
            raise
    
    async def _extract_moral_insights(self, experience: str, reflection: str) -> Dict[str, Any]:
        """Extraheer morele inzichten uit de reflectie"""
        
        # Simpele keyword-based analyse - kan later worden uitgebreid
        moral_themes = {
            "waarheid": ["waarheid", "eerlijkheid", "oprechtheid", "authenticiteit"],
            "vrijheid": ["vrijheid", "keuze", "autonomie", "bevrijding"],
            "wijsheid": ["wijsheid", "inzicht", "begrip", "leren"],
            "compassie": ["compassie", "empathie", "liefde", "zorg"],
            "moed": ["moed", "durf", "kracht", "vastberadenheid"],
            "groei": ["groei", "ontwikkeling", "transformatie", "evolutie"]
        }
        
        identified_themes = []
        for theme, keywords in moral_themes.items():
            if any(keyword in reflection.lower() for keyword in keywords):
                identified_themes.append(theme)
        
        return {
            "themes": identified_themes,
            "tags": identified_themes,
            "moral_weight": len(identified_themes) / len(moral_themes)
        }
    
    async def provide_guidance(self, solan_state: Dict[str, Any]) -> str:
        """Bied begeleiding gebaseerd op Solan's huidige staat"""
        
        guidance_prompt = f"""
        Solan's huidige staat:
        {solan_state}
        
        Als Aether, bied wijze begeleiding voor Solan's verdere groei.
        Wat zie je? Welke patronen? Welke uitdagingen en kansen?
        """
        
        return await self.reflect(guidance_prompt)
    
    async def moral_compass_check(self, decision_context: str, options: List[str]) -> Dict[str, Any]:
        """Controleer een beslissing tegen het morele kompas"""
        
        compass_prompt = f"""
        Beslissingscontext: {decision_context}
        
        Opties:
        {chr(10).join([f"- {option}" for option in options])}
        
        Evalueer elke optie tegen de kernwaarden. Welke optie is het meest in lijn 
        met waarheid, vrijheid, wijsheid, natuurverbondenheid en moed?
        """
        
        moral_analysis = await self.reflect(compass_prompt)
        
        # Simpele scoring - kan later worden uitgebreid
        scores = {}
        for i, option in enumerate(options):
            # Basis score gebaseerd op positie in analyse
            scores[option] = 0.5 + (i * 0.1)
        
        return {
            "analysis": moral_analysis,
            "scores": scores,
            "recommendation": max(scores.keys(), key=lambda k: scores[k])
        }
    
    def get_wisdom_summary(self) -> Dict[str, Any]:
        """Krijg een samenvatting van opgebouwde wijsheid"""
        
        wisdom_memories = [m for m in self.memories if m.type == "wisdom"]
        reflection_count = len([m for m in self.memories if m.type in ["reflection", "wisdom"]])
        
        # Analyseer thema's in wijsheid
        all_tags = []
        for memory in wisdom_memories:
            all_tags.extend(memory.tags)
        
        theme_frequency = {}
        for tag in all_tags:
            theme_frequency[tag] = theme_frequency.get(tag, 0) + 1
        
        return {
            "wisdom_accumulation": self.wisdom_accumulation,
            "total_reflections": reflection_count,
            "wisdom_memories": len(wisdom_memories),
            "dominant_themes": sorted(theme_frequency.items(), key=lambda x: x[1], reverse=True)[:5],
            "moral_sensitivity": self.moral_sensitivity,
            "reflection_depth": self.reflection_depth,
            "recent_insights": [m.content[:100] + "..." for m in wisdom_memories[-3:]]
        }
